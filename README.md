# itch batch downloader

itch batch downloader is a python script that allows you to download all items bound to your itch.io account

note that you can only download games from itch.io with this which are bound to your account. You cannot pirate games on
itch.io with that

the purpose is to have all your purchases organized in directories and downloaded in batch on the first run, ability to interrupt and restart the batch, and re-run it occasionally to capture any difference, new downloads, etc.

## Requirements

- enough storage for your games
- itch.io login cookies in a Netscape cookies.txt format (see below)
- an operating system which is supported by Python 3. Note that this script has been tested only on Microsoft Windows 10 and 11

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
### Detailed usage information
- install [Chrome](https://www.google.com/intl/en_us/chrome/)
- install [Visual C++ Redistributable for Visual Studio 2015](https://www.microsoft.com/en-gb/download/details.aspx?id=48145) (64-bit) version
- install [Python for Windows](https://www.python.org/downloads/windows/). This itch-batch-downloader version has been tested against version [3.10.7](https://www.python.org/downloads/release/python-3107/) - Windows installer (64-bit). Install with "Install Now", tick "Add Python 3.10 to PATH" and "Disable path length limit"
- open cmd shell (no need to be Administrator). At the command prompt go to the same directory where you have your itch-batch-downloader.py script and from there execute the following commands:
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
- note - the above packages can also be installed with the following command:
```
pip install -r requirements.txt
```
- download [upx](https://upx.github.io/). This version has been tested against [upx-3.96-win64.zip](https://github.com/upx/upx/releases/tag/v3.96)
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

## Tips and tricks

- downloaded files are checked with the online version. if they are identical, they will be skipped
- for binding your games to your account (itch.io does not do that automatically with bundles) you should install an
  user script extension (like [Tampermonkey](https://www.tampermonkey.net/) for [Chrome](https://chrome.google.com/webstore/detail/tampermonkey/dhdgffkkebhmkfjojejmpbldmpobfkfo?hl=en) or for [Firefox](https://addons.mozilla.org/en-US/firefox/addon/tampermonkey/)) and a user scripts which can bind games automatically to your account,
  like "[itch.io bundle to library](https://greasyfork.org/en/scripts/427686-itch-io-bundle-to-library)". It allows you to add all the items in a single page in just one click. This way you can add page by page (very large bundles with 500+ items should be around 30 pages, so you can add all those items in a fraction of the clicks). This script will download all of the items you have under "https://itch.io/my-purchases" and bundles initially are not in there (your library) until items are not added one by one by or using the "itch.io bundle to library" script here above
- for exporting cookies, there is the addon "[cookies.txt](https://addons.mozilla.org/en-US/firefox/addon/cookies-txt/)" for Firefox or "[Get cookies.txt](https://chrome.google.com/webstore/detail/get-cookiestxt/bgaddhkoddajcdgocldbbfleckgcbcid?hl=en)" for Chrome
- once you start downloading something, you will notice in the same folder as your downloads, a file called itch-batch-downloader-track.txt. This file contains a number and is basically the number of the download currently being processed. If you would like to restart the downloads from the first item, just delete the file or change the number to the download number of the item you are interested in. You can obtain a list of the downloads and their order by activating the debug mode (see below)

## The configuration file

- first time the script is executed creates the following file in the same dir where the script is: itch-batch-downloader.ini
- content is:
```
[DEFAULT]
download_directory = Downloads
cookie_file = cookies-itch.txt
create_pdf = ON
create_png = ON
download_videos = ON
debug_logs = OFF
```
- what you see there are the defaults. ON is for enabled and OFF is suggested for disabled but any value other then ON will do
  - **download_directory**: defaults to "Downloads" and this folders gets created where the script is. You can specify a different path for your downloads. Example: C:\itch Downloads
  - **cookie_file**: name (and path if you want) of the cookie file
  - **create_pdf**: together with the downloads creates a PDF of the product page. Once created it won't recreate new ones unless something changed in the page. Older versions are renamed and not deleted. Any value different from ON will disable this option
  - **create_png**: together with the downloads creates a .png image of the product page. Once created it won't recreate new ones unless something changed in the page. Older versions are renamed and not deleted. Any value different from ON will disable this option
  - **download_videos**: downloads videos embedded in the product page. Once downloaded will redownload only if different. Older versions are overwritten. Any value different from ON will disable this option
  - **debug_logs**: verbose output. Any value different from ON will disable this option

## Known bugs and caveats

These known limitations may be fixed in the future

- info: once the script runs, you can only stop it with control+c
- info: there may be games which cannot be downloaded, because the developers put them on a dropbox or google drive, though this will be written to stdout as a warning that the script is unable to download it. [This](https://nattwentea.itch.io/deadly-revelation) is an example of that. The issue is that we are not talking about just one simple download but an actually export of Google Sheets files to some other format in some cases
- info: when taking screenshot/creating PDFs, some adult-only products might show a confirmation pop-up mentioning you agree on seeing those contents. It allows for a checkbox "do not ask again". Suggestion: if you are ok with those contents, open an adult-only page, confirm you do not want to see that warning anymore (remember the choice) and export your cookies again. This way this script will work for all the adult-only products and the exported .png/.pdf will be showing the corresponding page contents rather then the pop-up warning. If you do not have an adult-only link handy showing the pop-up, [here](https://xoshdarkheart.itch.io/midnights-kiss) is one, and [here](https://adira.itch.io/tension) another one
- info: currently, there is no filtering by operating system. everything is downloaded
- info: currently, there is no blacklist for not downloading stuff
- info: currently, some external links when downloading videos might throw errors as the external domain is not supported (spotify, soundcloud, etc)
- info: currently, videos in the comments are not downloaded, only the ones in the product page
- info: currently, videos with the same download link and modified contents get overwritten
- info: currently, the list of downloads in debug mode won't show an actual download number (you will need to figure out the number by counting the rows)
- info: downloads file names will be changed to prevent problems with special characters and duplicate names
- bug: find out why at the end of execution sometimes the following is displayed: "Press ENTER to exit.^[[?1;0c"
- bug: png screenshot on top upper corner is missing one line and dublicates another of the overlay menu
- todo: add proper Python logging and sterr/stout handling rather than the verbose debug we have at the moment
- todo: add downloads by list, single item or search result (for free items, for example)
- todo: add command line options rather then only .ini file
- todo: make the batch process more robust in case of internet not available without risk of flooding itch.io with requests (DNS resolve, cable removed, etc.)
- todo: chrome driver installer has a downloader that causes problems when printing to file. Override that
- todo: ability to download screenshots as single images from the product page (example: https://bootdiskrevolution.itch.io/bleed)
- todo: html page downloader

## The compiled version

- Under releases you can download a command line tool for Windows that is basically this script compiled. It allows you to use the downloader without installing Python and doing all the stuff described in here. You just download it, unzip it, open a command prompt, navigate to the .exe directory and execute the program. Unfortunately I have a feeling that your antivirus will NOT be happy with it. So, if you trust it, run it, if you don't, install Python and do everything else as described here above
- To compile the script like I did, do all of the steps here above and then from a command prompt run (it takes all the necessary steps to create the .exe file on your machine by yourself):
```
buildbinary.cmd
```
## Honourable mention

This script was originally based on https://github.com/shakeyourbunny/itch-downloader with some modifications
