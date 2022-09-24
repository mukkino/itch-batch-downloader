# itch batch downloader

itch batch downloader is a python script that allows you to download all items bound to your itch.io account

note that you can only download games from itch.io with this which are bound to your account. You cannot pirate games on
itch.io with that

## Requirements

- enough storage for your games
- itch.io login cookies in a Netscape cookies.txt format (see below)
- an operating system which is supported by Python 3. Note that this script has been tested only on Microsoft Windows

## Usage

- login to itch.io with your web browser
- export your cookies to a file. You only need the cookies for itch.io, you can delete the rest (with a text editor, see below)
- copy the cookie file in the same directory and rename it to 'cookies-itch.txt'
- edit the itch-batch-downloader.ini to set up your download directory and the other options available (see below). If not available run the script for the first time. It won't do anything but create the itch-batch-downloader.ini file
- run the script with (if unsure about which to use start with the first one):
```
python itch-downloader.py
```
or
```
python3 itch-downloader.py
```
Detailed usage information
- install [Chrome](https://www.google.com/intl/en_us/chrome/)
- install [Visual C++ Redistributable for Visual Studio 2015](https://www.microsoft.com/en-gb/download/details.aspx?id=48145) (64-bit) version
- install [Python for Windows](https://www.python.org/downloads/windows/). This itch-batch-downloader version has been tested against version [3.10.7](https://www.python.org/downloads/release/python-3107/) - Windows installer (64-bit). Install with "Install Now", tick "Add Python 3.10 to PATH" AND "Disable path lenght limit"
- open cmd shell (no need to be Administrator). At the command promprt go to the same directory where you have your itch-batch-downloader.py script and from there execute the following commands:
```
py -m pip install --upgrade pip
py -m pip install --user virtualen
py -m venv env
.\env\Scripts\activate
```
- what they do is (in the same order as above):
  - upgrade pip
  - install virtual environment
  - create a virtual environment
  - activate your virtual environment

- install the following packages
```
py -m pip install wheel
py -m pip install requests
py -m pip install dateparser
py -m pip install bs4
py -m pip install selenium
py -m pip install webdriver_manager
py -m pip install Pillow
py -m pip install pyinstaller
py -m pip install yt-dlp
py -m pip install ffmpeg-python
py -m pip install pyOpenSSL
py -m pip install colorama
```
- note: The above packages can also be installed with the following command:
```
pip install -r requirements.txt
```
- download [UPX](https://upx.github.io/). This version has been tested against [upx-3.96-win64.zip](https://github.com/upx/upx/releases/tag/v3.96)
- unzip the files from upx-3.96-win64.zip (or your version number) in the same directory as the itch-batch-downloader.py script and rename the directory to just "upx" (rather than the full version you are using as originally in the name)

- from time to time, if you wish to upgrade your packages in your virtual environment, use:
```
pip install -r requirements.txt --upgrade
```
- if you would like to update your requirements.txt at this point use:
```
py -m pip freeze > requirements.txt
```
- to leave the virtual environment use
```
deactivate
```
- to reactivate the virtual environment use (from the same directory where the itch-batch-downloader.py script is located):
```
.\env\Scripts\activate
```

## Tips and Tricks

- downloaded files are checked with the online version. if they are identical, they will be skipped
- for binding your games to your account (itch.io does not do that automatically with bundles) you should install an
  user script extension (like [Tampermonkey](https://www.tampermonkey.net/) for [Chrome](https://chrome.google.com/webstore/detail/tampermonkey/dhdgffkkebhmkfjojejmpbldmpobfkfo?hl=en) or for [Firefox](https://addons.mozilla.org/en-US/firefox/addon/tampermonkey/)) and a user scripts which can bind games automatically to your account,
  like "[itch.io bundle to library](https://greasyfork.org/en/scripts/427686-itch-io-bundle-to-library)". It allows you to add all the items in a single page in just one click. This way you can add page by page (very large bundles with 500+ items should be around 30 pages, so you can add all those items in a fraction of the clicks). This script will download all of the items you have under "https://itch.io/my-purchases" and bundles initially are not in there (your library) until items are not added one by one by or using the script here above
- for exporting cookies, there is the addon "[cookies.txt](https://addons.mozilla.org/en-US/firefox/addon/cookies-txt/)" for Firefox or "[Get cookies.txt](https://chrome.google.com/webstore/detail/get-cookiestxt/bgaddhkoddajcdgocldbbfleckgcbcid?hl=en)" for Chrome
- once you start downloading something, you will notice in the same folder as your downloads, a file called itch-batch-downloader-track.txt. This file contains a number and is basically the number of the download currently being processed. If you would like to restart the downloads from the first item, just delete the file or change the number to the download number of the item you are interered in. You can obtain a list of the downloads and their order by activating the debug more (see below)

## Known bugs and caveats

These known limitations may be fixed in the future, pull requests for extending the functionality and fixing bugs are
welcome.

- once the script runs, you can only stop it with control+c
- there may be games which cannot be downloaded, because the developers put them on a dropbox or google drive, though this will be written to stdout as a warning that the script is unable to download it.
- currently, there is no filtering by operating system. everything is downloaded.
- currently, there is no blacklist for not downloading stuff.
- currently, non-games (PDFs, art assets or similar things are not downloaded)
- currently, the list of downloads in debug mode won't show an actual download number (you will need to figure out the number by counting the rows)

## honorable mention

This script was originally based on https://github.com/shakeyourbunny/itch-downloader with some modifications
