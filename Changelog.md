# Changelog for itch-batch-downloader

## 0.1.0 (2022-09-24)

- project forked from itch-downloader 0.5.3, initial release of itch-batch-downloader 0.1.0
- ability to download any purchased item (removed distinction between games and non-games)
- replaced code for downloading dumping webpages, screenshots and videos
- added support to export product page as .png and .pdf
- added support in tool (rather then external) for downloading iframe embedded videos, etc. within a product page
- file renaming for filesystem compatibility (unicode)
- logging system with debug info added (unicode, both for output to file and/or console)
- misc bug fixes, stability improvements and special cases handling

## 0.5.3 (2022-04-16)

- download now adds datestamp to archives
- renames already downloaded files appropriately
- added webpage screenshot of gamepage (user has to provide service url)
- added screenshot download option
- added operating system selection (not yet active)
- still hardcoded that only windows and android will be downloaded

## 0.5.2 (2022-04-12)

- added a primitive download continue (tracks download position and resumes download at number)
- fixed (hopefully) "SSL: DECRYPTION_FAILED_OR_BAD_RECORD_MAC"
- fixed missing content-disposition
- some reformatting

## 0.5.1 (2022-04-10)

- fixed config file reading
- some adjustments for win32 platform

## 0.5 (2022-04-10)

- first numbered revision
- configuration put into proper .ini file
- rewritten README.md
- Changelog.md
- displays xxx / number of games during downloading games
- proper requirements.txt

## unnamed revisions (2022-04-10)

- basic working revisions, ironed out bugs and such
- configuration baked into script
- total rewrite of bundle downloader