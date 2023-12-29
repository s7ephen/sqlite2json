#!/usr/bin/env python
# This python file will walk through a directory assumed to be full of Kasts extractions (json and mp3 files).
# It will read mp3 metadata from each .json file, read the associated mp3 file, and copy into a new mp3 file
# containing both the metadata and the audio. The new filename will also be based on some data from the json. (the title field)
# EXAMPLE:
#   After this was run:
#  
# ./sqlite2json.py database.db3 kastsextract ./kast_extracted_mp3s ~/.var/app/org.kde.kasts/data/KDE/kasts/enclosures
#  
#   A directory of mp3s and json extracted from the Kasts SQL DB is in "kast_extracted_mp3s":
#   
#        s7:~/Desktop/sqlite2json_and_kasts_extract$ ls kast_extracted_mp3s/*.mp3 | wc -l
#        636
#        s7:~/Desktop/sqlite2json_and_kasts_extract$ ls kast_extracted_mp3s/*.json | wc -l
#        636
#        s7:~/Desktop/sqlite2json_and_kasts_extract$ ls kast_extracted_mp3s/ | head -n 3
#        00ae9915b9dc86ad41b910d4c82e5df1.json
#        00ae9915b9dc86ad41b910d4c82e5df1.mp3
#        01ae8e431256b6c6d3075c2dc328ac0d.json
#        01ae8e431256b6c6d3075c2dc328ac0d.mp3
#        s7:~/Desktop/sqlite2json_and_kasts_extract$ cat kast_extracted_mp3s/00ae99*.json | grep -i title
#            "title": "591-Matthew Tartaglia vs The View", 
#        s7:~/Desktop/sqlite2json_and_kasts_extract$
#
#   This tool will walk through the "kasts_extracted_mp3s" directory and copy the mp3 to whatever the
#   "title" field contains. Along the way it will:
#    --> Add the "title" field to the mp3 "title" metadata field.
#    --> Add the "kasts_dl_url" field to the mp3 "encoded_by" metadata field.
#    --> Add the "feed" field to the mp3 "publisher" metadata field.
#    --> Add the "updated" field to the mp3 "date" metadata field.
#    --> Add the "created" field to the mp3 "creation_time" metadata field.
# 
# THis is the basic idea: 
# ffmpeg -i input.mp3 -c copy -metadata artist="Someone" output.mp3 
# you can keep adding more -metadata fields:
# -metadata artist="artist name" -metadata title="track title
#
#    ********************************
#    ******** EXAMPLE USAGE *********
#    ********************************
#
#    s7:~/Desktop/sqlite2json_and_kasts_extract$ ./merge_json_and_mp3.py /home/s7/Desktop/sqlite2json_and_kasts_extract/kast_extracted_mp3s/ renamed_kasts_archives
#    Looking in directory:  /home/s7/Desktop/sqlite2json_and_kasts_extract/kast_extracted_mp3s/
#        [+] Checking:  f503b3a79bb57aef97b05b3fdee3ed32.json
#            [-] Matching MP3 found for:  f503b3a79bb57aef97b05b3fdee3ed32
#            [-] Attempting to load json for: f503b3a79bb57aef97b05b3fdee3ed32.json
#                [-] Success loading JSON from:  f503b3a79bb57aef97b05b3fdee3ed32.json
#            [-] TITLE LOCATED: '30-The Brothers Eckstein on Illuminist Symbology and Literature'
#        [+] Directory 'renamed_kasts_archives' does not exist, creating it.
#            [-]Copying '/home/s7/Desktop/sqlite2json_and_kasts_extract/kast_extracted_mp3s/f503b3a79bb57aef97b05b3fdee3ed32.mp3' --> 'renamed_kasts_archives/30-The Brothers Eckstein on Illuminist Symbology and Literature.mp3'
#        [+] Checking:  72766f748be99acd7ef365d20b3c9297.json
#            [-] Matching MP3 found for:  72766f748be99acd7ef365d20b3c9297
#            [-] Attempting to load json for: 72766f748be99acd7ef365d20b3c9297.json
#                [-] Success loading JSON from:  72766f748be99acd7ef365d20b3c9297.json
#            [-] TITLE LOCATED: '233-Rigorous Intuition-Jeff Wells'
#            [-]Copying '/home/s7/Desktop/sqlite2json_and_kasts_extract/kast_extracted_mp3s/72766f748be99acd7ef365d20b3c9297.mp3' --> 'renamed_kasts_archives/233-Rigorous Intuition-Jeff Wells.mp3'
#        [+] Checking:  44ccc38079274c06060929040422db48.json
#            [-] Matching MP3 found for:  44ccc38079274c06060929040422db48
#            [-] Attempting to load json for: 44ccc38079274c06060929040422db48.json
#                [-] Success loading JSON from:  44ccc38079274c06060929040422db48.json
#            [-] TITLE LOCATED: '18-Lost Their Brains-Vyz_s First Live Show'
#            [-]Copying '/home/s7/Desktop/sqlite2json_and_kasts_extract/kast_extracted_mp3s/44ccc38079274c06060929040422db48.mp3' --> 'renamed_kasts_archives/18-Lost Their Brains-Vyz_s First Live Show.mp3'
#        [+] Checking:  34ac521ca481b0c2571b91122ad20eef.json
#            [-] Matching MP3 found for:  34ac521ca481b0c2571b91122ad20eef
#            [-] Attempting to load json for: 34ac521ca481b0c2571b91122ad20eef.json
#                [-] Success loading JSON from:  34ac521ca481b0c2571b91122ad20eef.json
#            [-] TITLE LOCATED: '114-Disdainable Envelopment-Tom DeWeese'
#            [-]Copying '/home/s7/Desktop/sqlite2json_and_kasts_extract/kast_extracted_mp3s/34ac521ca481b0c2571b91122ad20eef.mp3' --> 'renamed_kasts_archives/114-Disdainable Envelopment-Tom DeWeese.mp3'
# 
#             [*** LINES FOR 600 FILES REMOVED ***]
#
#            [+] Checking:  b0419c40a7070426c2197370163723bb.json
#                [-] Matching MP3 found for:  b0419c40a7070426c2197370163723bb
#                [-] Attempting to load json for: b0419c40a7070426c2197370163723bb.json
#                    [-] Success loading JSON from:  b0419c40a7070426c2197370163723bb.json
#                [-] TITLE LOCATED: 'Bioweapon Blues 42: Rochelle Walensky is a Monster!'
#                [-]Copying '/home/s7/Desktop/sqlite2json_and_kasts_extract/kast_extracted_mp3s/b0419c40a7070426c2197370163723bb.mp3' --> 'renamed_kasts_archives/Bioweapon Blues 42: Rochelle Walensky is a Monster!.mp3'
#        s7:~/Desktop/sqlite2json_and_kasts_extract$
 
import sys 
import sqlite3
import json
import os
import hashlib
import shutil # for os agnostic file moving/copying
import distutils.spawn
import argparse
import urllib2

global FFMPEGCOPY
FFMPEGCOPY = False

def copy_mp3(outputdir, filename, title):
    if not os.path.exists(outputdir):
        print("\t[+] Directory '%s' does not exist, creating it."%outputdir)
        os.mkdir(outputdir)
    print("\t\t[-]Copying '%s' --> '%s'"%(filename, outputdir+os.path.sep+title+".mp3")) 
    shutil.copy(filename, outputdir+os.path.sep+title+".mp3")
#    if FFMPEGCOPY:
#        distutils.spawn
#    HERE WAS WHERE I WAS GOING TO DO A WHOLE FFMPEG COPY THAT WOULD DO MP3 INSERTION BUT I AM SKIPPNG THAT
#    FOR NOW UNTIL I FIGURE OUT WHICH ID3 FIELD IS RESPONSIBLE FOR ORDERING A SERIES OF MP3s (like audiobooks have mp3 'parts').
#
    
def findall_kasts_json(kastsdir, outputdir):
    for dirpath, dirnames, filenames in os.walk(kastsdir):
        print "Looking in directory: ", dirpath
        for f in filenames:
            ext = os.path.splitext(f)[1]
            if ext == ".json": # Find all the json files in the directory
                print "\t[+] Checking: ", f
                #check if the mp3 of the same file exists.
                if os.path.exists(os.path.join(dirpath, os.path.splitext(f)[0]+".mp3")):
                    print "\t\t[-] Matching MP3 found for: ", os.path.splitext(f)[0] 
                    print "\t\t[-] Attempting to load json for:", f
                    try: 
                        json_f = open(os.path.join(dirpath, f))
                        data = json.load(json_f)
#                        print repr(data)
                        json_f.close()
                    except:
                        print "Fatal Error Reading JSON from: ",f
                    else:
                        print "\t\t\t[-] Success loading JSON from: ",f
                    json_title = data['title']
                    print("\t\t[-] TITLE LOCATED: '%s'" % json_title)
                    copy_mp3(outputdir, os.path.join(dirpath, os.path.splitext(f)[0]+".mp3"), json_title)
#                os.path.splitext(f)
#                abspath = os.path.join(dirpath, f)
#            with open(abspath) as f:
#                function(f.read())

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('kastsextractdir', help='The full path to the extracted kasts directory.')
    parser.add_argument('outputdir', help='The directory to place all the output files. If directory doesnt exist, it will be created.')
    args = parser.parse_args()
    if distutils.spawn.find_executable("ffmpeg") is not None:
        print "\t[+] FFMpeg was found! This maybe be used to copy files while inserting mp3 metadata!"
        FFMPEGCOPY = True
    else:
        print "\t[+] FFMpeg was not found, performing basic copy with no metadata insertion."
    findall_kasts_json(args.kastsextractdir, args.outputdir)
