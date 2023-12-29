#!/usr/bin/env python
# *********************************************************************************
# This thing can do two things using ONLY python standard libs (no modules):
#   1. Convert a SQLite Databse file to a JSON file
#         or
#   2. Extract all the downloaded files (mp3s, videos, etc) from a Kasts app
#      installation (including all the related metadata)
#
#   It may seem obscure but Kasts is the most regularly maintained opensource Podcast client
#   that doesnt require subscription or use a cloud service. It also runs on mobile devices (like
#   Librem, Pinephone, etc). But it DOESNT have a "export" feature lol.
#   It also stores everything in an sqlite db, so that's why this tool does both things.
#
#   Kasts will download and ENTIRE series from a feed URL.
#   So this tool is meant for bulk offline archival. 
# *********************************************************************************
#    EXAMPLE USAGE SQLITE TO JSON:
# *********************************************************************************
# 
# s7:~/Desktop/$ ./sqlite2json.py ./database.db3 db2json ./database.json
# 
# ***
# Converting sqllite to JSON.
# *** 
# 	Database file:  ./database.db3
# 	JSON outputfile:  ./database.json
# s7:~/Desktop/$ 
# *********************************************************************************
# EXAMPLE USAGE KASTS EXTRACT:
# *********************************************************************************
# s7:~/Desktop/$ ./sqlite2json.py database.db3 kastsextract ./kast_extracted_mp3s ~/.var/app/org.kde.kasts/data/KDE/kasts/enclosures
# ***
# Extracting downloads from Kasts.
# ***
# Database file:  database.db3
# Output directory:  ./kast_extracted_mp3s
# Kasts downloads directory:  /home/s7/.var/app/org.kde.kasts/data/KDE/kasts/enclosures
# **************
# *** TABLES ***
# **************
# [u'Errors', u'SyncTimestamps', u'Enclosures', u'FeedActions', u'Entries', u'Chapters', u'Queue', u'EpisodeActions', u'Authors', u'Feeds']
# **************
# *** VALUES ***
# **************
# 
# FOUND A DOWNLOAD IN THE DB FOR:  https://traffic.megaphone.fm/WIRI6081250993.mp3?updated=1691011645 
# 	FOUND ON DISK HERE:  /home/s7/.var/app/org.kde.kasts/data/KDE/kasts/enclosures/204384b3adc4952bc0a89ad84e6d610c
# 	FOUND, matching metadata for downloaded file!!! ID:  d200af16-3178-11ee-b9e3-ab4a5da9178f
# 	TITLE FOUND:  Bioweapon Blues 43: Welcome to the Era of Subclinical Myocarditis and Turbo Cancer.
# 	COPIED DOWNLOAD TO:  ./kast_extracted_mp3s/204384b3adc4952bc0a89ad84e6d610c.mp3
# 	COPIED DOWNLOAD METADATA TO:  ./kast_extracted_mp3s/204384b3adc4952bc0a89ad84e6d610c.json
# 
#     [ A LOT OF LINES REMOVED]
# 
# **************
# *** COUNTS ***
# **************
# Total downloads found:  635
# Matching Metadata for download found:  635
# Total URLs in Kasts database w/out downloads:  28346
# s7:~/Desktop/$ 
# *********************************************************************************
#    USAGE MESSAGES FROM THE TOOL:
#    
# Python argparse makes the help EXTREMELY unintuitive. It is retarded. I hate it. 
# But anyway here's what it looks like:
# 
# s7:~/Desktop/$ ./sqlite2json.py -h
# usage: sqlite2json.py [-h] sqldbfile {db2json,kastsextract} ...
# 
# positional arguments:
#   sqldbfile             The full path to the sqllite database, including the
#                         file.
#   {db2json,kastsextract}
# 
# optional arguments:
#   -h, --help            show this help message and exit


# s7:~/Desktop/sqlite2json_and_kasts_extract$ ./sqlite2json.py file.db db2json -h
# usage: sqlite2json.py sqldbfile db2json [-h] outfile
# 
# positional arguments:
#   outfile     The name of the file you want to send the JSON output.
# 
# optional arguments:
#   -h, --help  show this help message and exit


# s7:~/Desktop/$ ./sqlite2json.py file.db kastsextract -h
# usage: sqlite2json.py sqldbfile kastsextract [-h] outputdir enclosures
# 
# positional arguments:
#   outputdir   The directory all the media from Kasts will be extracted to. If
#               directory doesn't exist, it will be created.
#   enclosures  The directory used by Kasts app to store downloads, or
#               'enclosures' as Kasts calls them. usually in a dir named
#                 'enclosures/' in Kasts app directory.
# optional arguments:
#   -h, --help  show this help message and exit
#
#
# s7:~/Desktop/$ 
# s7:~/Desktop/$


import sys
import sqlite3
import json
import os
import hashlib
import shutil # for os agnostic file moving/copying
import argparse

def sqlite2json(dbfilename, outputfilename):
# Straight forward function to just open a sqlite3 database and convert it
# into a straight json file using the sqlite2dict() helper function.
    db_content = {}
    db_content = sqlite2dict(dbfilename)
    # dump contents to json file
    with open(outputfilename, "w") as f:
        json.dump(db_content, f, indent=4)

def sqlite2dict(dbfilename):
# helper function to fetch data sqlite database and return a dict.
    # open database file
    with sqlite3.connect(dbfilename) as conn:
        # builtin Row object is easy to convert to dict
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        # get the names of the tables
        c.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [a["name"] for a in c.fetchall()]
        # get content from each table
        db_content = {}
        for table in tables:
            c.execute("SELECT * FROM {0}".format(table))
            db_content[table] = [dict(a) for a in c.fetchall()]
        return db_content

def findDownloadMetadata(db_content, enclosure_url, enclosure_id):
# Find first matching entry in the [Entries] table. (there *shouldnt* be duplicates I dont think)
# The thing that links [Enclosures] table to the [Entities] table is the 'id' field.
# Inside the [Enclosure] table, each entry should have an 'url' field and 'id' field.
# the same 'id' is used in the [Entries] table which has additional metadata about the "enclosure".
    for thing in db_content['Entries']:
        if thing['id'] == enclosure_id:
            print "\tFOUND, matching metadata for downloaded file!!! ID: ", enclosure_id
            print "\tTITLE FOUND: ",thing['title']
            return thing 
            
def kasts_extract(dbfilename, enclosure_dir, output_dir):
# The downloaded files in kasts are called "enclosures". 
# which seems to be an abstracted name because feeds can
# technically contain any kind of media (ogg,mp3,mp4,avi,etc).
# So this walks through the kasts database finding downloads and copying
# to your selected output directory along with metadata about
# the file that was found.
    if os.path.isdir(output_dir):
        print "This directory already exists, saving there anyway: ", output_dir
    else:
        if os.mkdir(output_dir) == 0:
            print "Created directory: ", output_dir
    db_content = {}
    db_content = sqlite2dict(dbfilename)
    print ("**************\n*** TABLES ***\n**************")
    print repr(db_content.keys())
    i = 0
    i2 = 0
    i3 = 0
    print ("**************\n*** VALUES ***\n**************")
    for thing in db_content['Enclosures']:
        #print thing['url']
        urlhash = hashlib.md5(thing['url']).hexdigest()
        # check if a file of the same name exists
        fullpath = enclosure_dir+os.path.sep+urlhash
        if os.path.isfile(fullpath):
            i+=1
            print "\n\nFOUND A DOWNLOAD IN THE DB FOR: ", thing['url'],"\n\tFOUND ON DISK HERE: ", fullpath
            download_meta = {}
            download_meta = findDownloadMetadata(db_content, thing['url'],thing['id'])
            if download_meta != {}:
                i2+=1
                # Smash some additional data from the [Enclosures] table
                # into the resuls from the [Entries] table metadata.
                download_meta["kasts_dl_url"]=thing['url']
                download_meta["kasts_dl_hash"]=urlhash
                download_meta["kasts_dl_original_file_location"]=fullpath
                shutil.copy(fullpath, output_dir+os.path.sep+urlhash+".mp3")
                print "\tCOPIED DOWNLOAD TO: ", output_dir+os.path.sep+urlhash+".mp3"        
                with open(output_dir+os.path.sep+urlhash+".json", "w") as f:
                    json.dump(download_meta, f, indent=4)
                    print "\tCOPIED DOWNLOAD METADATA TO: ", output_dir+os.path.sep+urlhash+".json"
                
        else:
            i3+=1
    
    print ("**************\n*** COUNTS ***\n**************")
    print "Total downloads found: ", i
    print "Matching Metadata for download found: ", i2 
    print "Total URLs in Kasts database w/out downloads: ", i3

if __name__ == "__main__":
    # Python getopt doesnt allow for 'conditional arguments'. 
    # (i.e. only require some arguments if others are present)
    # but argparse does let you do this kinda, and is standard library like getopt is.
    # (i.e. it does not requiring a module installation)
    # 
    # in other words, with getopt you cant do this:
    # $ ./script.py --dothis --with-these-reqd-args --and-these-too
    #       but have the same script also accept:
    # $ ./script.py --dothat --with-these-other-reqd-args --and-deez-2
    #
    # so this uses argparse but because I am retarded I forgot 
    # halfway through coding the Kasts stuff, that's why I was using argparse 
    # and didnt even end up using it the way i intended. oh well. maybe someday I'll
    # actually change it and figure out copy-pastable way to do argparse conditional python
    # arguments so i never have to look at this crap again.
    #
    # So what follows is a buncha argparse nonsense.

    parser = argparse.ArgumentParser()
    parser.add_argument('sqldbfile', help='The full path to the sqllite database, including the file.')
    subparsers = parser.add_subparsers(dest='subcommand')
    subparsers.required = True # I dont know what this does.

    # add subparser for db2json 
    parser_mode1 = subparsers.add_parser('db2json')
    # add the outputfile required argument for the db2json command 
    parser_mode1.add_argument('outfile', help='The name of the file you want to send the JSON output.')

    # add subparser for kastsextract
    parser_mode2 = subparsers.add_parser('kastsextract')
    # add the outputdir required argument for kastsextract 
    parser_mode2.add_argument('outputdir', help="The directory all the media from Kasts will be extracted to. If directory doesn't exist, it will be created.")
    # add the enclosures directory required argument for kastsextract
    parser_mode2.add_argument('enclosures', help="The directory used by Kasts app to store downloads, or 'enclosures' as Kasts calls them. usually in a dir named 'enclosures/' in Kasts app directory.")

    args = parser.parse_args()
#    print args
    if args.subcommand == "db2json":
        print "\n\n***\nConverting sqllite to JSON.\n*** "
        print "\tDatabase file: ", args.sqldbfile
        print "\tJSON outputfile: ", args.outfile
#        sqlite2json(sys.argv[1], sys.argv[2]) #the ghetto way i usually do it
        sqlite2json(args.sqldbfile, args.outfile)
    if args.subcommand == "kastsextract":
        print "***\nExtracting downloads from Kasts.\n***"
        print "Database file: ", args.sqldbfile
        print "Output directory: ", args.outputdir
        print "Kasts downloads directory: ", args.enclosures
#        kasts_extract(sys.argv[1], sys.argv[2], sys.argv[3]) #the ghetto way I usually do it
        kasts_extract(args.sqldbfile, args.enclosures, args.outputdir) 
