# itch batch downloader

A Python script that downloads all items bound to your itch.io account in batch.

The downloader:
- retrieves every item in your itch.io library
- downloads all available files
- optionally captures product pages as PNG and PDF
- downloads embedded videos
- preserves historical versions where possible
- supports interrupting and resuming downloads

The goal of the tool is to create a complete local archive of your itch.io purchases.

This script only downloads items bound to your account and does not bypass itch.io permissions.

## Features

- batch download of your entire itch.io library
- resume interrupted downloads
- skip files that are already identical
- capture product pages as:
  - PNG screenshot
  - PDF print
- download embedded videos
- version older metadata captures instead of overwriting
- sanitize filenames to avoid filesystem issues
- debug mode for detailed download tracking

## Requirements

- Python 3.9 or newer
- Python packages listed in `requirements.txt`
- Sufficient disk space for your library
- Exported itch.io cookies in Netscape format

Optional (only needed for some features):

- [Google Chrome](https://www.google.com/intl/en_us/chrome/) (required if Selenium-based page rendering is enabled)
- [Microsoft Visual C++ Redistributable](https://www.microsoft.com/en-gb/download/details.aspx?id=48145) (Windows only, usually already installed). Install the **x64 version** if you are using 64-bit Python (most systems).

The script has primarily been tested on Windows, but most of the code is cross-platform and should work on Linux and macOS.

## Usage

### 1. Login to itch.io

Open https://itch.io in your web browser and login to your account.

The script requires your authenticated session cookies in order to
access your library and download owned content.

------------------------------------------------------------------------

### 2. Export your itch.io cookies

Export the cookies for `itch.io` from your browser and save them to a
text file.

Recommended browser extensions:

-   **Get cookies.txt LOCALLY** (Chrome / Chromium browsers)
-   **cookies.txt** (Firefox)

Export **only itch.io cookies**.

Save the exported file in the same directory as the script and rename it
to:

    cookies-itch.txt

------------------------------------------------------------------------

### 3. Configure the downloader

Edit the configuration file:

    itch-batch-downloader.ini

Set at minimum:

-   the download directory
-   any optional behaviour flags

If the configuration file does not exist, run the script once and it
will be created automatically. The first run will exit after generating
the default configuration.

------------------------------------------------------------------------

### 4. Run the script

From the script directory run:

    python itch-downloader.py

or if your system uses `python3`:

    python3 itch-downloader.py

If unsure, try the first command.

------------------------------------------------------------------------

### What happens when the script runs

Once started the downloader will:

1.  Read your configuration file
2.  Load the cookies from `cookies-itch.txt`
3.  Connect to itch.io
4.  Retrieve your library
5.  Iterate through each owned product
6.  Download all available files while attempting to avoid duplicates
7.  Save the files into your configured download directory

Progress and warnings are printed to the console.

------------------------------------------------------------------------

### Stopping the script

The downloader runs continuously until it finishes processing your
library.

To stop it manually press:

    CTRL + C

This sends an interrupt signal and safely stops the script.

Any files that were already fully downloaded will remain on disk.
Incomplete downloads may remain as partial files depending on the
downloader state.

### Detailed usage information

- install [Python for Windows](https://www.python.org/downloads/windows/). This itch-batch-downloader version has been tested against version [3.14.3](https://www.python.org/downloads/release/python-3143/) - Windows installer (64-bit). Install with "Install Now", tick "Add Python 3.14 to PATH" and "Disable path length limit"
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
py -m pip install beautifulsoup4
py -m pip install colorama
py -m pip install cryptography
py -m pip install dateparser
py -m pip install ffmpeg-python
py -m pip install pillow
py -m pip install pyinstaller
py -m pip install pyOpenSSL
py -m pip install python-dotenv
py -m pip install regex
py -m pip install requests
py -m pip install selenium
py -m pip install trio
py -m pip install trio-websocket
py -m pip install webdriver-manager
py -m pip install websocket-client
py -m pip install yt-dlp
```
- note - while you could install those as suggested here above, in order to to keep the packages to the correct tested version, I suggest to run the following command instead:
```
pip install -r requirements.txt
```
- download [upx](https://upx.github.io/). This version has been tested against [v5.1.1](https://github.com/upx/upx/releases/tag/v5.1.1)
- unzip the files from upx-5.1.1-win64.zip (or your version number) in the same directory as the itch-batch-downloader.py script and rename the directory to just "upx" (rather than the full version you are using as originally in the name)
- install [pyinstaller](https://pyinstaller.org/en/stable/installation.html) and run buildbinary.cmd to compile the .exe on Windows
- note: you could o the same on macOS and Linux via pyinstaller. upx is not supported on these platforms so you will just run buildbinary.cmd after having installed pyinstaller

- from time to time, if you wish to upgrade your packages in your virtual environment, use (remember this will break the testing I did on the release. If you see problems you might need to rollback to the versions mentioned here):
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
- if you would like to associate free games to your account in batch, you could do so by using tools such as [ItchClaim](https://github.com/Smart123s/ItchClaim)
- for binding your games to your account (itch.io does not do that automatically with bundles) you should install an
  user script extension (like [Tampermonkey](https://www.tampermonkey.net/) for [Chrome](https://chrome.google.com/webstore/detail/tampermonkey/dhdgffkkebhmkfjojejmpbldmpobfkfo?hl=en) or for [Firefox](https://addons.mozilla.org/en-US/firefox/addon/tampermonkey/)) and a user scripts which can bind games automatically to your account,
  like "[itch.io bundle to library](https://greasyfork.org/en/scripts/427686-itch-io-bundle-to-library)". It allows you to add all the items in a single page in just one click. This way you can add page by page (very large bundles with 500+ items should be around 30 pages, so you can add all those items in a fraction of the clicks). This script will download all of the items you have under "https://itch.io/my-purchases" and bundles initially are not in there (your library) until items are not added one by one by or using the "itch.io bundle to library" script here above. I more recently found out about this Chrome extension but I cannot guarantee it works [itch.io Bundle Auto Add to Library](https://chromewebstore.google.com/detail/itchio-bundle-auto-add-to/pbolegaohnnpillkpklefebilhanameg). 
- for exporting cookies, there is the addon "[cookies.txt](https://addons.mozilla.org/en-US/firefox/addon/cookies-txt/)" for Firefox or "[Get cookies.txt](https://chromewebstore.google.com/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc)" for Chrome
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
