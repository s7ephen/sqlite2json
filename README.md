# SQLITE2JSON & KastsExtract
Convert SQLITE (DB3) to JSON.
or extract MP3 files from Kasts.

Note: this too is designed to require no libraries (for the python version) or 
a single-source executable for any other versions.

# Why Kasts?
I was looking for a well maintained, non-cloud-backed/subscription, podcast client that
would take a feed URL as user-input and bulk download entire podcasts WITHOUT restrictions.
Kasts fit the bill.
https://apps.kde.org/kasts/
|||
|-|-|
|![kastsdesktop.png](https://cdn.kde.org/screenshots/kasts/kasts-desktop.png)|![kastsmobile.png](https://cdn.kde.org/screenshots/kasts/kasts-mobile.png)|

Kasts can runon Linux mobile and desktop (responsive) but unfortunately it doesnt have an "export mp3" feature.

So this tool will extract those mp3s for archival purposes. 

Additionally, it will use some of the feed metadata and insert it as ID3 information into the corresponding mp3 file.
as well as storing the metadata as information in a file alongside the mp3 on the filesystem.

# Example Usage: 
The two ways to use this.

## SQLite to JSON
``` 
 s7:~/Desktop/$ ./sqlite2json.py ./database.db3 db2json ./database.json
 
 ***
 Converting sqllite to JSON.
 *** 
   Database file:  ./database.db3
   JSON outputfile:  ./database.json
 s7:~/Desktop/$ 
```

## Kasts Extraction
```
s7:~/Desktop/$ ./sqlite2json.py database.db3 kastsextract ./kast_extracted_mp3s ~/.var/app/org.kde.kasts/data/KDE/kasts/enclosures
 ***
 Extracting downloads from Kasts.
 ***
 Database file:  database.db3
 Output directory:  ./kast_extracted_mp3s
 Kasts downloads directory:  /home/s7/.var/app/org.kde.kasts/data/KDE/kasts/enclosures
 **************
 *** TABLES ***
 **************
 [u'Errors', u'SyncTimestamps', u'Enclosures', u'FeedActions', u'Entries', u'Chapters', u'Queue', u'EpisodeActions', u'Authors', u'Feeds']
 **************
 *** VALUES ***
 **************
 
 FOUND A DOWNLOAD IN THE DB FOR:  https://traffic.megaphone.fm/WIRI6081250993.mp3?updated=1691011645 
   FOUND ON DISK HERE:  /home/s7/.var/app/org.kde.kasts/data/KDE/kasts/enclosures/204384b3adc4952bc0a89ad84e6d610c
   FOUND, matching metadata for downloaded file!!! ID:  d200af16-3178-11ee-b9e3-ab4a5da9178f
   TITLE FOUND:  Bioweapon Blues 43: Welcome to the Era of Subclinical Myocarditis and Turbo Cancer.
   COPIED DOWNLOAD TO:  ./kast_extracted_mp3s/204384b3adc4952bc0a89ad84e6d610c.mp3
   COPIED DOWNLOAD METADATA TO:  ./kast_extracted_mp3s/204384b3adc4952bc0a89ad84e6d610c.json
 
     [ A LOT OF LINES REMOVED]
 
 **************
 *** COUNTS ***
 **************
 Total downloads found:  635
 Matching Metadata for download found:  635
 Total URLs in Kasts database w/out downloads:  28346
 s7:~/Desktop/$ 
```
# An Additional side-tool called: merge_json_and_mp3.py 
Since the extracted Kasts files are left as their digest filenames (mp3 and json), this tool
will use the title data in the json to copy the mp3 to a new file using the "title" field of
the json metadata.

## Example Usage:
```
    s7:~/Desktop/sqlite2json_and_kasts_extract$ ./merge_json_and_mp3.py /home/s7/Desktop/sqlite2json_and_kasts_extract/kast_extracted_mp3s/ renamed_kasts_archives
    Looking in directory:  /home/s7/Desktop/sqlite2json_and_kasts_extract/kast_extracted_mp3s/
        [+] Checking:  f503b3a79bb57aef97b05b3fdee3ed32.json
            [-] Matching MP3 found for:  f503b3a79bb57aef97b05b3fdee3ed32
            [-] Attempting to load json for: f503b3a79bb57aef97b05b3fdee3ed32.json
                [-] Success loading JSON from:  f503b3a79bb57aef97b05b3fdee3ed32.json
            [-] TITLE LOCATED: '30-The Brothers Eckstein on Illuminist Symbology and Literature'
        [+] Directory 'renamed_kasts_archives' does not exist, creating it.
            [-]Copying '/home/s7/Desktop/sqlite2json_and_kasts_extract/kast_extracted_mp3s/f503b3a79bb57aef97b05b3fdee3ed32.mp3' --> 'renamed_kasts_archives/30-The Brothers Eckstein on Illuminist Symbology and Literature.mp3'
        [+] Checking:  72766f748be99acd7ef365d20b3c9297.json
            [-] Matching MP3 found for:  72766f748be99acd7ef365d20b3c9297
            [-] Attempting to load json for: 72766f748be99acd7ef365d20b3c9297.json
                [-] Success loading JSON from:  72766f748be99acd7ef365d20b3c9297.json
            [-] TITLE LOCATED: '233-Rigorous Intuition-Jeff Wells'
            [-]Copying '/home/s7/Desktop/sqlite2json_and_kasts_extract/kast_extracted_mp3s/72766f748be99acd7ef365d20b3c9297.mp3' --> 'renamed_kasts_archives/233-Rigorous Intuition-Jeff Wells.mp3'
        [+] Checking:  44ccc38079274c06060929040422db48.json
            [-] Matching MP3 found for:  44ccc38079274c06060929040422db48
            [-] Attempting to load json for: 44ccc38079274c06060929040422db48.json
                [-] Success loading JSON from:  44ccc38079274c06060929040422db48.json
            [-] TITLE LOCATED: '18-Lost Their Brains-Vyz_s First Live Show'
            [-]Copying '/home/s7/Desktop/sqlite2json_and_kasts_extract/kast_extracted_mp3s/44ccc38079274c06060929040422db48.mp3' --> 'renamed_kasts_archives/18-Lost Their Brains-Vyz_s First Live Show.mp3'
        [+] Checking:  34ac521ca481b0c2571b91122ad20eef.json
            [-] Matching MP3 found for:  34ac521ca481b0c2571b91122ad20eef
            [-] Attempting to load json for: 34ac521ca481b0c2571b91122ad20eef.json
                [-] Success loading JSON from:  34ac521ca481b0c2571b91122ad20eef.json
            [-] TITLE LOCATED: '114-Disdainable Envelopment-Tom DeWeese'
            [-]Copying '/home/s7/Desktop/sqlite2json_and_kasts_extract/kast_extracted_mp3s/34ac521ca481b0c2571b91122ad20eef.mp3' --> 'renamed_kasts_archives/114-Disdainable Envelopment-Tom DeWeese.mp3'
 
             [*** LINES FOR 600 FILES REMOVED ***]

            [+] Checking:  b0419c40a7070426c2197370163723bb.json
                [-] Matching MP3 found for:  b0419c40a7070426c2197370163723bb
                [-] Attempting to load json for: b0419c40a7070426c2197370163723bb.json
                    [-] Success loading JSON from:  b0419c40a7070426c2197370163723bb.json
                [-] TITLE LOCATED: 'Bioweapon Blues 42: Rochelle Walensky is a Monster!'
                [-]Copying '/home/s7/Desktop/sqlite2json_and_kasts_extract/kast_extracted_mp3s/b0419c40a7070426c2197370163723bb.mp3' --> 'renamed_kasts_archives/Bioweapon Blues 42: Rochelle Walensky is a Monster!.mp3'
        s7:~/Desktop/sqlite2json_and_kasts_extract$
```
# Appendices
Some additional useful information

## The Kasts database file location:
This depends on your version and distribution, but on Debian based linux systems or flatpak systems it should be in:
`~/.var/app/org.kde.kasts/data/KDE/kasts`

## The Kasts Database Schema
```
$ sqlite
SQLite version 3.34.1 2021-01-20 14:10:07
Enter ".help" for usage hints.
Connected to a transient in-memory database.
Use ".open FILENAME" to reopen on a persistent database.
sqlite> .open database.db3
sqlite> .tables
Authors         Enclosures      EpisodeActions  FeedActions     Queue         
Chapters        Entries         Errors          Feeds           SyncTimestamps
sqlite> .schema
CREATE TABLE Feeds (name TEXT, url TEXT, image TEXT, link TEXT, description TEXT, deleteAfterCount INTEGER, deleteAfterType INTEGER, subscribed INTEGER, lastUpdated INTEGER, new BOOL, notify BOOL);
CREATE TABLE Entries (feed TEXT, id TEXT UNIQUE, title TEXT, content TEXT, created INTEGER, updated INTEGER, link TEXT, read bool, new bool, hasEnclosure BOOL, image TEXT);
CREATE TABLE Authors (feed TEXT, id TEXT, name TEXT, uri TEXT, email TEXT);
CREATE TABLE Queue (listnr INTEGER, feed TEXT, id TEXT, playing BOOL);
CREATE TABLE IF NOT EXISTS "Enclosures" (feed TEXT, id TEXT, duration INTEGER, size INTEGER, title TEXT, type TEXT, url TEXT, playposition INTEGER, downloaded INTEGER);
CREATE TABLE Errors (type INTEGER, url TEXT, id TEXT, code INTEGER, message TEXT, date INTEGER, title TEXT);
CREATE TABLE Chapters (feed TEXT, id TEXT, start INTEGER, title TEXT, link TEXT, image TEXT);
CREATE TABLE SyncTimestamps (syncservice TEXT, timestamp INTEGER);
CREATE TABLE FeedActions (url TEXT, action TEXT, timestamp INTEGER);
CREATE TABLE EpisodeActions (podcast TEXT, url TEXT, id TEXT, action TEXT, started INTEGER, position INTEGER, total INTEGER, timestamp INTEGER);
sqlite> 
```


