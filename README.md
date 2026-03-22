# itch batch downloader

A Python script that downloads all items bound to your itch.io account in batch.

The downloader:
- retrieves items currently bound to your itch.io account/library
- attempts to download all available files
- optionally captures product pages as PNG and PDF
- downloads embedded videos
- preserves historical versions where possible
- supports interrupting and resuming downloads

The goal of the tool is to create the most complete local archive possible of your itch.io purchases.

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
- filename sanitization is not yet fully implemented
- debug mode for detailed download tracking

## Requirements

- Python 3.9 or newer
- Python packages listed in `requirements.txt`
- Sufficient disk space for your library
- Exported itch.io cookies in cookies.txt / Netscape-style format

Optional (only needed for some features):

- **[Google Chrome](https://www.google.com/intl/en_us/chrome/)**

  Required for features that use Selenium browser automation.

  If Chrome is not installed:
  - product page **PDF snapshots will not be created** (`create_pdf`)
  - product page **PNG screenshots will not be created** (`create_png`)

  The rest of the downloader will still work (library scanning and file downloads).

  If Chrome is not available you can disable these features in the configuration file:

  create_pdf = OFF
  create_png = OFF

- [Microsoft Visual C++ Redistributable](https://www.microsoft.com/en-gb/download/details.aspx?id=48145) (Windows only). Install the **x64 version** if you are using 64-bit Python (most systems).

  Some Python packages used by the downloader include native compiled components (for example `cryptography`, `cffi`, and other compiled wheels).

  If the runtime is missing on Windows:
  - the script **may fail to start**
  - HTTPS connections used for downloading files **may fail**
  - some dependencies may fail to import

  On most Windows systems this runtime is already installed.

The script has primarily been tested on Windows, but most of the code is cross-platform and should work on Linux and macOS.

## Usage

### 1. Login to itch.io

Open https://itch.io in your web browser and log in to your account.

The script requires your authenticated session cookies in order to
access your library and download owned content.

------------------------------------------------------------------------

### 2. Export your itch.io cookies

Export the cookies for `itch.io` from your browser and save them to a
text file.

Recommended browser extensions:

-   [**Get cookies.txt LOCALLY**](https://chromewebstore.google.com/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc) (Chrome / Chromium browsers)
-   [**cookies.txt**](https://addons.mozilla.org/en-US/firefox/addon/cookies-txt/) (Firefox)

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
will be created automatically.\
The first run will exit after generating the default configuration.

------------------------------------------------------------------------

### 4. Run the script

From the script directory run:

    python itch-batch-downloader.py

or if your system uses `python3`:

    python3 itch-batch-downloader.py

If unsure, try the first command.

------------------------------------------------------------------------

## What happens when the script runs

Once started the downloader will:

1.  Read your configuration file
2.  Load the cookies from `cookies-itch.txt`
3.  Connect to itch.io
4.  Retrieve your library
5.  Iterate through each owned product
6.  Download all available files while attempting to avoid duplicates
7.  Save the files into your configured download directory

Progress and warnings are printed to the console.

Downloaded files are compared with the online version.\
If the files are identical, the download will be **skipped**.

------------------------------------------------------------------------

## Debug mode

You can enable verbose debug output by editing the configuration file
and setting:

    debug_logs = ON

When debug mode is enabled the script prints additional information to
the console, including:

-   detailed progress information
-   the list of downloads discovered
-   the order in which items will be processed
-   additional diagnostic information useful for troubleshooting

This can also be used to see the **exact download order** of your
library.

------------------------------------------------------------------------

## Download progress tracking

While the script is running, a file named:

    itch-batch-downloader-track.txt

will appear in the same directory as your downloads.

This file contains a number representing the **download currently being
processed**.

This mechanism allows the downloader to resume work if it is
interrupted.

### Restarting from the beginning

If you want to restart downloads from the beginning:

-   delete the file `itch-batch-downloader-track.txt`

### Restarting from a specific item

If you want to resume from a specific item:

-   open `itch-batch-downloader-track.txt`
-   change the number to the download index you want to start from

You can determine the correct download number by enabling **debug
mode**, which prints the full list of downloads and their order.

If the tracking file becomes corrupted or contains an invalid number,
simply delete it to restart from the beginning.

------------------------------------------------------------------------

## Stopping the script

The downloader runs continuously until it finishes processing your
library.

To stop it manually press:

    CTRL + C

This sends an interrupt signal and safely stops the script.

Any files that were already fully downloaded will remain on disk.\
Incomplete downloads may remain as partial files depending on the
downloader state.

## Tips and tricks

- If you would like to associate free games with your account in batch, you can use tools such as [ItchClaim](https://github.com/Smart123s/ItchClaim).

- If you purchased bundles, you may notice that **itch.io does not automatically add all bundle items to your library**. Many items remain only inside the bundle purchase page and do not appear under:

  https://itch.io/my-purchases

  Since the downloader reads items from your library/purchases list, those bundle items need to be added to your account first.

  One convenient way to do this is by using a **user script**.

  First install a user-script extension such as **Tampermonkey**:

  - [Tampermonkey](https://www.tampermonkey.net/)
  - Chrome version: https://chrome.google.com/webstore/detail/tampermonkey/dhdgffkkebhmkfjojejmpbldmpobfkfo?hl=en
  - Firefox version: https://addons.mozilla.org/en-US/firefox/addon/tampermonkey/

  Then install a script that can automatically bind bundle items to your library, such as:

  - **itch.io bundle to library**  
    https://greasyfork.org/en/scripts/427686-itch-io-bundle-to-library

  This script allows you to add **all the items from a single bundle page with one click**.

  Large bundles (for example 500+ items) may span **many pages (around 30 pages)**, but using the script you can add them page by page with only a fraction of the manual clicks normally required.

  Once items are added to your library, they will appear under:

  https://itch.io/my-purchases

  and the downloader will be able to process them.

- I also recently discovered a Chrome extension that may automate this process as well, although I cannot guarantee that it works:

  https://chromewebstore.google.com/detail/itchio-bundle-auto-add-to/pbolegaohnnpillkpklefebilhanameg

## Configuration file

When the script is executed for the first time it automatically creates
a configuration file in the same directory as the script:

    itch-batch-downloader.ini

The default content of the file is:

    [DEFAULT]
    download_directory = Downloads
    cookie_file = cookies-itch.txt
    create_pdf = ON
    create_png = ON
    download_videos = ON
    debug_logs = OFF

These values represent the **default behaviour of the downloader**.

Options that use `ON` / `OFF` act as simple switches:

-   `ON` → feature enabled\
-   any value **other than `ON`** → feature disabled

------------------------------------------------------------------------

### download_directory

Default: `Downloads`

This is the directory where all downloaded content will be saved.

If the directory does not exist it will be **created automatically** in
the same location as the script.

You can also specify an absolute path. Example:

    C:\itch Downloads

------------------------------------------------------------------------

### cookie_file

Default: `cookies-itch.txt`

Specifies the file containing the exported itch.io cookies.

You may provide either:

-   just the filename (if it is in the script directory), or\
-   a full path to the cookie file.

------------------------------------------------------------------------

### create_pdf

Default: `ON`

When enabled, the script creates a **PDF snapshot of the product page**
alongside the downloaded files.

The script detects changes in the page:

-   if the page has **not changed**, the PDF is not recreated\
-   if the page **changes**, a new PDF is generated

Older versions are **renamed and preserved** rather than deleted.

Set to any value other than `ON` to disable.

------------------------------------------------------------------------

### create_png

Default: `ON`

When enabled, the script captures a **PNG screenshot of the product
page**.

Behaviour is the same as for PDFs:

-   screenshots are only recreated if the page changes\
-   older versions are **renamed and preserved**

Set to any value other than `ON` to disable.

------------------------------------------------------------------------

### download_videos

Default: `ON`

Downloads videos embedded in the product page.

If the video changes, it will be downloaded again.\
Existing videos may be overwritten when a newer version is detected.

Set to any value other than `ON` to disable.

------------------------------------------------------------------------

### debug_logs

Default: `OFF`

Enables verbose logging in the console.

This option is useful for troubleshooting or understanding what the
script is doing internally.

Set to `ON` to enable detailed debug output.

## Known bugs and caveats

These known limitations may be fixed in the future

- todo: currently, there is no filtering by operating system. everything is downloaded
- todo: currently, there is no blacklist for not downloading stuff
- todo: currently, some external links when downloading videos might throw errors as the external domain is not supported (spotify, soundcloud, etc)
- todo: currently, videos in the comments are not downloaded, only the ones in the product page
- todo: currently, videos with the same download link and modified contents get overwritten
- todo: currently, the list of downloads in debug mode won't show an actual download number (you will need to figure out the number by counting the rows)
- todo: add proper Python logging and sterr/stout handling rather than the verbose debug we have at the moment
- todo: add downloads by list, single item or search result (for free items, for example)
- todo: add command line options rather then only .ini file
- todo: make the batch process more robust in case of internet not available without risk of flooding itch.io with requests (DNS resolve, cable removed, etc.)
- todo: chrome driver installer has a downloader that causes problems when printing to file. Override that
- todo: ability to download screenshots as single images from the product page (example: https://bootdiskrevolution.itch.io/bleed)
- todo: html page downloader
- todo: download file names should be sanitized to prevent problems with special characters, unsafe names, and path-related filename collisions
- todo: detect expired cookies and warn the user
- todo: make HTML parsing more resilient to itch.io layout changes
- todo: prevent failures caused by excessively long file paths
- bug: find out why at the end of execution sometimes the following is displayed: "Press ENTER to exit.^[[?1;0c" (On Microsoft Windows)

## Corner cases to keep in mind for testing

- there may be games which cannot be downloaded, because the developers put them on a dropbox or google drive, though this will be written to stdout as a warning that the script is unable to download it. [This](https://nattwentea.itch.io/deadly-revelation) is an example of that. The issue is that we are not talking about just one simple download but an actually export of Google Sheets files to some other format in some cases
- when taking screenshot/creating PDFs, some adult-only products might show a confirmation pop-up mentioning you agree on seeing those contents. It allows for a checkbox "do not ask again". Suggestion: if you are ok with those contents, open an adult-only page, confirm you do not want to see that warning anymore (remember the choice) and export your cookies again. This way this script will work for all the adult-only products and the exported .png/.pdf will be showing the corresponding page contents rather then the pop-up warning. If you do not have an adult-only link handy showing the pop-up, [here](https://xoshdarkheart.itch.io/midnights-kiss) is one, and [here](https://adira.itch.io/tension) another one
- download screenshots as single images from the product page (example: https://bootdiskrevolution.itch.io/bleed)

## How to compile

Prebuilt command-line binaries for **Windows** and **macOS** are
available in the **Releases** section.\
These are compiled versions of the script and allow you to use the
downloader **without installing Python**.

To use a release binary:

1.  Download the archive for your platform.
2.  Extract it.
3.  Open a terminal (Command Prompt / Terminal).
4.  Navigate to the directory containing the executable.
5.  Run the program.

Because the binary is produced with **PyInstaller** and may also be
compressed with **UPX**, some antivirus software may flag it as
suspicious. If you prefer not to run the prebuilt binary, you can
compile the tool yourself as described below.

------------------------------------------------------------------------

# Build from source

The following instructions create a standalone executable **similar to
the ones provided in the Releases section**.

The process is:

1.  Install Python
2.  Create a virtual environment
3.  Install dependencies
4.  (Optional) install UPX
5.  Build the executable

------------------------------------------------------------------------

# 1. Install Python

Download Python from:

https://www.python.org/downloads/

This project has been **tested with Python 3.14.3**, but **any Python
3.9+ version should work**.

### Windows

Download:

https://www.python.org/downloads/windows/

During installation:

-   click **Install Now**
-   enable **Add Python to PATH**
-   enable **Disable path length limit**

### macOS

Install Python using one of the following:

-   official installer from python.org
-   Homebrew:

```{=html}
<!-- -->
```
    brew install python

### Linux

Install Python from your distribution repository.

Example (Ubuntu / Debian):

    sudo apt install python3 python3-venv python3-pip

------------------------------------------------------------------------

# 2. Create a virtual environment

Navigate to the directory containing the script:

    itch-batch-downloader.py

### Windows

Open a **Command Prompt (no need to run it as Administrator)** and
execute:

    py -m pip install --upgrade pip
    py -m venv env
    .\env\Scripts\activate

### macOS / Linux

    python3 -m pip install --upgrade pip
    python3 -m venv env
    source env/bin/activate

What these commands do:

1.  upgrade `pip`
2.  create a **virtual environment**
3.  activate the environment

------------------------------------------------------------------------

# 3. Install required packages

Install the dependencies listed in `requirements.txt`:

    pip install -r requirements.txt

------------------------------------------------------------------------

# 4. Optional: install UPX (Windows only)

**UPX** is an executable packer/compressor.\
In this project it is used to reduce the size of the generated Windows
executable.

The program can be built **without UPX**, so this step is optional.

Download:

https://upx.github.io/

Tested version:

https://github.com/upx/upx/releases/tag/v5.1.1

Steps:

1.  Download the archive (for example `upx-5.1.1-win64.zip`)
2.  Extract it in the same directory as `itch-batch-downloader.py`
3.  Rename the extracted directory to just:

```{=html}
<!-- -->
```
    upx

The rename matters because the build setup expects the folder to be
named **`upx`** rather than the full version name.

Example:

-   original folder: `upx-5.1.1-win64`
-   renamed folder: `upx`

------------------------------------------------------------------------

# 5. Build the executable

## Windows (using the provided build script)

A Windows build script is already included:

    buildbinary.cmd

Run it from a Command Prompt opened in the same directory as the script:

    buildbinary.cmd

The script will:

-   run PyInstaller
-   produce the standalone `.exe`
-   use UPX compression if the `upx` folder is present

This is the **recommended method** on Windows.

------------------------------------------------------------------------

## Windows (manual build without the script)

If you prefer to run the build process manually instead of using
`buildbinary.cmd`, you can do it directly with PyInstaller. This
produces an executable **similar to the ones distributed in the Releases
section**.

First install PyInstaller:

    pip install pyinstaller

Then run:

    pyinstaller --onefile itch-batch-downloader.py

The executable will be created inside the `dist` directory.

If UPX is installed and available in the `upx` folder, PyInstaller may
automatically use it during the build to reduce the executable size.

------------------------------------------------------------------------

## macOS / Linux

`buildbinary.cmd` is a Windows batch file, so it is **not used on macOS
or Linux**.

Instead build the binary directly with PyInstaller:

    pip install pyinstaller
    pyinstaller --onefile itch-batch-downloader.py

UPX compression is typically **not used on macOS and Linux**.

------------------------------------------------------------------------

# Updating dependencies (optional)

If you want to upgrade packages inside the virtual environment:

    pip install -r requirements.txt --upgrade

Note: upgrading dependencies may break compatibility with the tested
release.\
**If problems appear after upgrading, you may need to roll back to the
tested versions listed in `requirements.txt`.**

------------------------------------------------------------------------

# Updating requirements.txt

To regenerate the dependency list:

### Windows

    py -m pip freeze > requirements.txt

### macOS / Linux

    pip freeze > requirements.txt

------------------------------------------------------------------------

# Managing the virtual environment

Deactivate the virtual environment:

    deactivate

Reactivate it later from the project directory.

### Windows

    .\env\Scripts\activate

### macOS / Linux

    source env/bin/activate

## FAQ

### Why are some bundle items missing from the downloader?

The downloader only processes items that appear in your purchases list:

https://itch.io/my-purchases

If you own a bundle, many items may **not automatically be added to your
library** by itch.io.\
Until they are added, they will not appear in your purchases list and
the downloader will not see them.

To fix this, make sure all bundle items are added to your library first
(for example using the tools mentioned in the **Tips and tricks**
section).

Once they appear under:

https://itch.io/my-purchases

the downloader will be able to process them normally.

------------------------------------------------------------------------

### Why do some downloads fail or show warnings?

Some projects on itch.io host their downloadable files on **external
platforms** such as:

-   Dropbox\
-   Google Drive\
-   SoundCloud\
-   Spotify\
-   other third‑party hosting services

In these cases the download process may be controlled by the external
website and cannot always be automated by the downloader.

When this happens the script usually prints a **warning message in the
console**.

If a file cannot be retrieved automatically, you may need to download it
manually from the project page.

## Honourable mention

This script was originally based on https://github.com/shakeyourbunny/itch-downloader with some modifications
