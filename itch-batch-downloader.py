"""
Based on https://github.com/shakeyourbunny/itch-downloader
"""

import configparser
import json
import os
import sys
import time
from http.cookiejar import MozillaCookieJar

import dateparser
import requests
import requests.cookies
from bs4 import BeautifulSoup

import dltool
import unicodedata
import re
import pickle

from datetime import datetime
import subprocess
import codecs

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.expected_conditions import staleness_of

import util
import pathlib
from pathlib import Path
import glob
import base64
import yt_dlp
import traceback

from colorama import Fore
from colorama import Style

version = "0.1.0"

# used to count if a certain page received an update in terms of contents. if it did this is used for creating a new version of
# the .png and .pdf files
global newDownloads

# yt-dlp logger class, used to make the yt-dlp output formatted the same as the rest of the logs
class ydLogger:
    def debug(self, msg):
        # For compatibility with youtube-dl, both debug and info are passed into debug
        # You can distinguish them by the prefix '[debug] '
        if msg.startswith('[debug] '):
            if config["DEFAULT"]["debug_logs"] == "ON": 
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " " + "[DEBUG] External links downloader: " + msg)
        else:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " " + "[INFO] External links downloader: " + msg)

    def info(self, msg):
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " " + "[INFO] External links downloader: " + msg)

    def warning(self, msg):
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " " + f"{Fore.YELLOW}[WARNING]{Style.RESET_ALL} External links downloader: " + msg)

    def error(self, msg):
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " " + f"{Fore.RED}[ERROR]{Style.RESET_ALL} External links downloader: " + msg)

# yt-dlp hook
def yd_hook(d):
    if d['status'] == 'finished':
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " " + "[INFO] External links downloader: done downloading, now post-processing ...")

def local_file_sanity_check(localfile, localsize, localdate, remotesize, remotedate):
    if not os.path.isfile(localfile):
        return False

    if localsize != remotesize:
        return False

    # date is a string, has to be converted to timestamp.
    if localdate != remotedate:
        return False

    # fall through, at this point the conditions above are satisfied
    return True
    
def slugify(value, allow_unicode=False, is_value_a_filename=False):
    """
    Taken from https://github.com/django/django/blob/master/django/utils/text.py
    and modified to prevent the fuction to interfere with the file extension
    and to specify if the input is a filename or a generic string
    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')

    if is_value_a_filename:

        fext = pathlib.Path(value).suffix
        fname = Path(value).stem
        
        value = re.sub(r'[^\w\s-]', '', fname.lower())
        value = re.sub(r'[-\s]+', '-', value).strip('-_')
        
        fext = re.sub(r'[^\w\s-]', '', fext.lower())
        fext = re.sub(r'[-\s]+', '-', fext).strip('-_')
        
        if fext is None or fext.strip() == "":
            pass
        else:
            value = value + "." + fext
        
    else:
    
        value = value.strip()
    
    return value

def fetch_upload(uploads_soup, dlurl, session, params, csfrtoken, gamedirectory, fileNr, full_page_soup=None):
    # returns true if the file was downloaded
    # Find the upload identifier – try the old attribute first, then fall back to the newer href‑based format.
    try:
        # Old style (in case it's an older page)
        downloadid = uploads_soup.find("a")["data-upload_id"]
        use_direct_endpoint = False
    except (TypeError, KeyError):
        # New style – look for a link that contains "/download/"
        dl_link = None

        # Search for any button that has an href with the substring "/download/".
        for candidate in uploads_soup.find_all(["a", "button"]):
            href = candidate.get("href", "")
            if "/download/" in href:
                dl_link = href
                break
        
        # If the upload block did NOT contain a download link, fall back to the whole page.
        if not dl_link and full_page_soup is not None:
            banner_btn = full_page_soup.find(
                "a",
                class_="button",
                href=lambda h: h and "/download/" in h,
            )
            if banner_btn:
                dl_link = banner_btn["href"]

        # Otherwise give up
        if not dl_link:
            print(
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                + " "
                + f"{Fore.YELLOW}[WARNING]{Style.RESET_ALL} Skipped a file (no download button found): {dlurl}"
            )
            return False

        dlurl = dl_link
        use_direct_endpoint = True
    # for everything else use original code
    except:
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " " + f"{Fore.YELLOW}[WARNING]{Style.RESET_ALL} Skipped a file: {dlurl}")
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " " + f"{Fore.YELLOW}[WARNING]{Style.RESET_ALL} =====================================")
        traceback.print_exc()
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " " + f"{Fore.YELLOW}[WARNING]{Style.RESET_ALL} =====================================")
        return False

    # Build the request that yields the JSON with the real file URL.
    if use_direct_endpoint:
        # The endpoint returns JSON directly – just GET it.
        dlj = session.get(dlurl, params=params, cookies=session.cookies).json()
    else:
        # Use the original code
        dlurl_final = f"{dlurl}/file/{downloadid}"
        dlj = session.post(dlurl_final, params=params, data=csfrtoken).json()

    domain = dlj["url"].split("/")[2]

    # Cloudflare‑mirrored URLs (don't have a "Last Modified" header)
    if "cloudflarestorage.com" in domain or domain.startswith("itchio-mirror"):
        # Build the directory where the file will be stored (same as the original script does for CDN files).
        fulldldir = os.path.join(
            config["DEFAULT"]["download_directory"], gamedirectory
        )
        os.makedirs(fulldldir, exist_ok=True)

        # Call the downloader.  `debugon` mirrors the original behaviour.
        debugon = config["DEFAULT"]["debug_logs"] == "ON"
        was_the_file_downloaded = dltool.download_a_file(
            dlj["url"],               # the Cloudflare‑mirrored URL
            filename=fulldldir,     # empty filename → use server‑provided name
            session=session,
            debugon=debugon,
        )
        return was_the_file_downloaded

    # Original code
    elif domain == "w3g3a5v6.ssl.hwcdn.net":
        # remote file check
        x = 0
        while x < 3:
            try:                
                dlhead = session.head(dlj["url"])
                dldate = dlhead.headers["last-modified"]
                if "content-disposition" in dlhead.headers:
                    dlfilename = dlhead.headers["content-disposition"].split('"')[1]
                else:
                    dlfilename = dlj["url"].split("?")[0].split("/")[-1]
                dlsize = dlhead.headers["content-length"]
                x = 4
            except:
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " " + f"{Fore.RED}[ERROR]{Style.RESET_ALL} Connection error. Retry " + str(x+1) + " of 3")
                x = x + 1
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " " + f"{Fore.RED}[ERROR]{Style.RESET_ALL} =====================================")
                traceback.print_exc()
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " " + f"{Fore.RED}[ERROR]{Style.RESET_ALL} =====================================")
            finally:
                if x == 3:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " " + f"{Fore.RED}[ERROR]{Style.RESET_ALL} Cannot recover from connection error. Quitting ...")
                    sys.exit(1)
        
        # make filename unique and unicode compatible
        dlfilename = str(fileNr) + "_" + slugify(dlfilename, False, True)

        # local preparation
        fulldldir = os.path.join(config["DEFAULT"]["download_directory"], gamedirectory)
        os.makedirs(fulldldir, exist_ok=True)
        fulldname = os.path.join(fulldldir, dlfilename)

        # rename files if exist
        suf = pathlib.Path(dlfilename).suffix
        suf.strip()
        if len(suf) > 0:
            if (suf[0] == "."):
                suf = suf[1:]
        if not suf or suf == "":
            newdlname = dlfilename + "_{}".format(dateparser.parse(dldate).strftime("%Y%m%d"))
        else:
            newdlname = dlfilename.replace("." + suf, "_{}.{}".format(dateparser.parse(dldate).strftime("%Y%m%d"), suf))
        
        newfulldname = os.path.join(fulldldir, newdlname)
        
        # old format
        if os.path.isfile(fulldname):
            if os.path.exists(fulldname):
                if os.path.exists(newfulldname):
                    os.remove(newfulldname)
                os.rename(fulldname, newfulldname)
                fulldname = newfulldname

        # new filename with date stamp
        fulldname = newfulldname
        
        # do the download
        wasTheFileDownloaded = False
        downloadRetries = 0
        while downloadRetries < 3:
            try:
                if config["DEFAULT"]["debug_logs"] == "ON":
                    debugon = True
                    wasTheFileDownloaded = dltool.download_a_file(dlj["url"], filename=fulldname, session=session, debugon=debugon)
                    downloadRetries = 4
                else:
                    debugon = False
                    wasTheFileDownloaded = dltool.download_a_file(dlj["url"], filename=fulldname, session=session, debugon=debugon)
                    downloadRetries = 4
            except:
                wasTheFileDownloaded = False
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " " + f"{Fore.RED}[ERROR]{Style.RESET_ALL}" + " Error while downloading - url: {}, filename: {}".format(dlj["url"], fulldname))
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " " + f"{Fore.RED}[ERROR]{Style.RESET_ALL} =====================================")
                traceback.print_exc()
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " " + f"{Fore.RED}[ERROR]{Style.RESET_ALL} =====================================")
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " " + f"{Fore.RED}[ERROR]{Style.RESET_ALL}" + " Retry " + str(downloadRetries + 1) + " of 3")
                downloadRetries = downloadRetries + 1
            finally:
                if downloadRetries == 3:
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " " + f"{Fore.RED}[ERROR]{Style.RESET_ALL} Cannot recover from connection error. Quitting ...")
                    sys.exit(1)

        return wasTheFileDownloaded

    else:
        tempUrl = dlj["url"]
        if domain == "drive.google.com":
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " " + f"{Fore.YELLOW}[WARNING]{Style.RESET_ALL} Download from Google Drive is UNSUPPORTED: {tempUrl}")
        else:
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " " + f"{Fore.YELLOW}[WARNING]{Style.RESET_ALL} Skipped a file: {tempUrl}")
        return False

def main(config):
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " " + "[INFO] Download directory is '{}'".format(config["DEFAULT"]["download_directory"]))
    time.sleep(3)

    # basic setup
    session = requests.Session()
    cookiejar = requests.cookies.RequestsCookieJar()

    cookies = MozillaCookieJar(config["DEFAULT"]["cookie_file"])
    cookies.load(ignore_expires=True, ignore_discard=True)
    cookiejar.update(cookies)

    session.cookies = cookiejar

    os.makedirs(config["DEFAULT"]["download_directory"], exist_ok=True)

    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " " + "[INFO] Loading and parsing my claimed purchases: ", end='')
    mypurchases_url = "https://itch.io/my-purchases"

    pagecounter = 1
    gamelist = list()
    r = session.get(mypurchases_url)
    if r.status_code == 200:
        if r.url != mypurchases_url:
            print("") # carriage return
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " " + f"{Fore.RED}[ERROR]{Style.RESET_ALL} Not properly authenticated, please provide cookies.")
            sys.exit(1)

        # parse first page
        soup_gamepage = BeautifulSoup(r.text, "html.parser").find_all("div", class_="game_cell_data")
        for game in soup_gamepage:
            gtitle = slugify(game.find("a", class_="title game_link").text)
            gurl = game.find("a", class_="button")["href"]
            if config["DEFAULT"]["debug_logs"] == "ON": 
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " " + "[DEBUG] Item found - " + "Title: " + gtitle + ". url: " + gurl)
            platform_soup = game.find("div", class_="game_platform")
            gamelist.append(
                {
                    "title": slugify(gtitle),
                    "dlurl": gurl
                }
            )

        soup_nextpage = BeautifulSoup(r.text, "html.parser").find("div", attrs={"class": "next_page forward_link"})
        while soup_nextpage:
            pagecounter = pagecounter + 1
            print(".", flush=True, end="")

            r = session.get(mypurchases_url + "?page={}".format(pagecounter))
            if r.status_code != 200:
                print(" [{}]".format(pagecounter), flush=True)
                break

            soup_gamepage = BeautifulSoup(r.text, "html.parser").find_all("div", class_="game_cell_data")
            for game in soup_gamepage:
                gtitle = slugify(game.find("a", class_="title game_link").text)
                gurl = game.find("a", class_="button")["href"]
                if config["DEFAULT"]["debug_logs"] == "ON": 
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " " + "[DEBUG] Item found - " + "Title: " + gtitle + ". url: " + gurl)
                platform_soup = game.find("div", class_="game_platform")
                gamelist.append(
                    {
                        "title": slugify(gtitle),
                        "dlurl": gurl
                    }
                )

            soup_nextpage = BeautifulSoup(r.text, "html.parser").find("div", attrs={"class": "next_page forward_link"})

        print("")  # carriage return
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " " + "[INFO] {} items found.".format(len(gamelist)))

        trackfile = os.path.join(config["DEFAULT"]["download_directory"], "itch-batch-downloader-track.txt")
        trackNum = 0
        if os.path.exists(trackfile):
            with open(trackfile, "r", encoding="utf-8") as f:
                trackNum = json.loads(f.read())
            f.close()
            os.remove(trackfile)

        numGames = len(gamelist)
        curGame = 0
                    
        for g in gamelist:
            curGame = curGame + 1
            if curGame >= trackNum:
                print("")
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " " + "[INFO] Analysing item {} of {}. Title: ".format(curGame, numGames) + slugify(g["title"]))

                # trackfile
                with open(trackfile, "w", encoding="utf-8") as f:
                    json.dump(curGame, f)
                f.close()

                r = session.get(g["dlurl"])
                if r.status_code == 200:

                    dlpage_soup = BeautifulSoup(r.text, "html.parser")
                    dlpage_dlbuttons = dlpage_soup.find_all("a", class_="button download_btn")
                    dlurl = g['dlurl'].rsplit("/", 2)[0]
                    gamedirectory = g["dlurl"].split("/")[3]
                    paramPost = {"source": "game_download", "key": g["dlurl"].split("/")[5]}
                    csfrToken = dlpage_soup.find("meta", attrs={"name": "csrf_token"})["value"]
                    uploads = dlpage_soup.find("div", class_="upload_list_widget").find_all(class_="upload")
                    newDownloads = False
                    
                    fileNr = 1
                    for u in uploads:
                        if config["DEFAULT"]["debug_logs"] == "ON": 
                            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " " + "[DEBUG] fetch_upload - " + "u: " + str(u) + ". durl: " + str(dlurl) + ". session: " + str(session) + ". paramPost: " + str(paramPost) + ". csfrToken: " + str(csfrToken) + ". gamedirectory: " + str(gamedirectory) + ". fileNr: " + str(fileNr))
                        newDownloadsTemp = fetch_upload(u, dlurl, session, paramPost, csfrToken, gamedirectory, fileNr, full_page_soup=dlpage_soup)
                        fileNr = fileNr + 1
                        if not newDownloads:
                            newDownloads = newDownloadsTemp

                    # product webpage screenshot is exported to image and PDF
                    URL = "https://" + g["dlurl"].split("/")[2] + "/" + g["dlurl"].split("/")[3]
                    
                    now = datetime.now()
                    dateyearmonthday = now.strftime("%Y%m%d")
                    
                    # selenium 4
                    options = Options()
                    options.add_experimental_option('excludeSwitches', ['enable-logging'])
                    options.add_argument('--headless')
                    options.add_argument('--disable-gpu')
                    options.add_argument("--disable-3d-apis")
                    options.add_argument('--no-sandbox')
                    options.add_argument('--disable-dev-shm-usage')
                    options.add_argument('--hide-scrollbars')
                    options.add_argument('--disable-web-security')

                    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

                    driver.cookies = cookiejar
                    
                    try:
                        driver.get(URL)
                    except:
                        driver.get(URL, verify=False)
                        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " " + f"{Fore.RED}[ERROR]{Style.RESET_ALL} Cannot verify domain, connection insicure")
                        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " " + f"{Fore.RED}[ERROR]{Style.RESET_ALL} =====================================")
                        traceback.print_exc()
                        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " " + f"{Fore.RED}[ERROR]{Style.RESET_ALL} =====================================")
 
                    try:
                        util.wait_until_images_loaded(driver, 30)
                    except TimeoutException:
                        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " " + f"{Fore.RED}[ERROR]{Style.RESET_ALL} Timeout error on: " + URL)
                        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " " + f"{Fore.RED}[ERROR]{Style.RESET_ALL} =====================================")
                        traceback.print_exc()
                        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " " + f"{Fore.RED}[ERROR]{Style.RESET_ALL} =====================================")
                                     
                    try:

                        height = 1024 + driver.execute_script("return document.documentElement.scrollHeight;")
                        width = 1024 + driver.execute_script("return document.body.offsetWidth;")
                        driver.set_window_size(width, height)
                        driver.maximize_window()
                            
                        # product webpage screenshot is exported to image
                        download_dir = os.path.join(os.path.abspath(config["DEFAULT"]["download_directory"]), gamedirectory)
                        fullscrname = os.path.join(download_dir, gamedirectory + "_webpage_screenshot_" + dateyearmonthday + ".png")                      
       
                        if config["DEFAULT"]["debug_logs"] == "ON": 
                            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " " + "[DEBUG] " + "Taking screenshot and creating PDF with Selenium, width: " + str(width) + ", height: " + str(height))
                        
                        try:
                            dir_check = Path(download_dir)
                            if not dir_check.is_dir():
                                os.mkdir(download_dir)
                            
                            screenshotsFound = 0
                            for name in glob.glob(os.path.join(download_dir, gamedirectory + "_webpage_screenshot_" + "*" + ".png")):
                                screenshotsFound = screenshotsFound + 1

                            if newDownloads or screenshotsFound <= 0:
                                if config["DEFAULT"]["create_png"] == "ON":
                                    debugon = True
                                    util.fullpage_screenshot(driver, fullscrname, debugon)
                                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " " + "[INFO] Screenshot taken: " + fullscrname)
                                else:
                                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " " + "[INFO] Screenshot creation disabled as config setting not equal to ON")
                            else:
                                if config["DEFAULT"]["create_png"] == "ON":
                                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " " + "[INFO] Recent screenshot exists. Skipped.")
                                else:
                                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " " + "[INFO] Screenshot creation disabled as config setting not equal to ON")
                        except:
                            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " " + f"{Fore.RED}[ERROR]{Style.RESET_ALL} Error while writing file: " + fullscrname)
                            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " " + f"{Fore.RED}[ERROR]{Style.RESET_ALL} =====================================")
                            traceback.print_exc()
                            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " " + f"{Fore.RED}[ERROR]{Style.RESET_ALL} =====================================")
                            
                        # product webpage screenshot is exported to pdf
                        fullpdfname = os.path.join(download_dir, f"{gamedirectory}_webpage_screenshot_{dateyearmonthday}.pdf")                         
                        
                        try:
                            
                            pdfsFound = 0
                            for name in glob.glob(os.path.join(download_dir, gamedirectory + "_webpage_screenshot_" + "*" + ".pdf")):
                                pdfsFound = pdfsFound + 1 
                            if newDownloads or pdfsFound <= 0:
                              
                                if config["DEFAULT"]["create_pdf"] == "ON": 
                                    # Selenium 4 helper returns a dict with a base‑64‑encoded PDF.
                                    try:
                                        pdf_bytes = driver.print_page(
                                            {
                                                "landscape": True,
                                                "displayHeaderFooter": True,
                                                "printBackground": True,
                                                "preferCSSPageSize": False,
                                                "shrinkToFit": True,
                                                'paper_width': '46.81', 'paper_height': '33.11',
                                            }
                                        )
                                        # `pdf_bytes` is already a binary blob (bytes) – write it straight to disk.
                                        with open(fullpdfname, "wb") as f:
                                            f.write(pdf_bytes)
                                        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " " + "[INFO] PDF created: " + fullpdfname)
                                    except Exception as error:
                                        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " " + "[ERROR] " + "PDF generation get response: ")
                                        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " " + f"{Fore.RED}[ERROR]{Style.RESET_ALL} =====================================")
                                        traceback.print_exc()
                                        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " " + f"{Fore.RED}[ERROR]{Style.RESET_ALL} =====================================")
                                elif config["DEFAULT"]["debug_logs"] == "ON":
                                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " " + "[INFO] PDF creation disabled as config setting not equal to ON")
                            else:
                                if config["DEFAULT"]["create_pdf"] == "ON":
                                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " " + "[INFO] Recent PDF exists. Skipped.")
                                else:
                                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " " + "[INFO] PDF creation disabled as config setting not equal to ON")
                        except:
                            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " " + f"{Fore.RED}[ERROR]{Style.RESET_ALL} Error while writing file: " + fullpdfname)
                            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " " + f"{Fore.RED}[ERROR]{Style.RESET_ALL} =====================================")
                            traceback.print_exc()
                            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " " + f"{Fore.RED}[ERROR]{Style.RESET_ALL} =====================================")
                            
                        # product videos are downloaded (youtube, vimeo, etc)  
                        if config["DEFAULT"]["download_videos"] == "ON": 
  
                            ydl_opts = {
                                'ignoreerrors': True,
                                'outtmpl': os.path.join(download_dir, gamedirectory + "_" + '%(id)s.%(ext)s'),
                                'logger': ydLogger(),
                                'progress_hooks': [yd_hook],
                            }
                
                            if config["DEFAULT"]["debug_logs"] == "ON": 
                                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " " + "[DEBUG] " + "Downloading page: {}".format(URL))
                            
                            res = requests.get(URL)

                            if config["DEFAULT"]["debug_logs"] == "ON": 
                                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " " + "[DEBUG] " + f"Got back response: {res.status_code}")
                                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " " + "[DEBUG] " + f"Page length: {len(res.text)}")

                            pageHtml = res.text
                            bsParser = BeautifulSoup(pageHtml, features='html.parser')
                            hrefs = bsParser.find_all('iframe')
                            for href in hrefs:
                                raw_src = href.get("src")                # e.g. "https://itch.io/embed/3347678?... "
                                # Normalise the URL:
                                if raw_src.startswith("//"):                 # protocol‑relative URLs (//domain/…)
                                    video_url = "https:" + raw_src
                                elif raw_src.startswith("http://") or raw_src.startswith("https://"):
                                    video_url = raw_src                      # already a full URL – keep it as‑is
                                else:                                        # fallback – assume HTTPS
                                    video_url = "https://" + raw_src.lstrip("/")

                                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " " + f"[INFO] Found video URL: {video_url}")

                                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                                    error_code = ydl.download(video_url)
                                    
                        else:
                        
                            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " " + "[INFO] Video downloads disabled as config setting not equal to ON")

                    finally:
                        newDownloads = False
                        driver.quit()

                else:
                    tempUrl = g["dlurl"]
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " " + f"{Fore.RED}[ERROR]{Style.RESET_ALL} Could not access download page {tempUrl}")
                    
        # trackfile
        with open(trackfile, "w", encoding="utf-8") as f:
            json.dump(0, f)
        f.close()
    else:
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " " + f"{Fore.RED}[ERROR]{Style.RESET_ALL} Could not access {mypurchases_url} properly [{r.status_code}]")

if __name__ == "__main__":
    print("itch-batch-downloader.py {} (c) 2022 mukkino".format(version))
    print("")

    config = configparser.ConfigParser()

    # initialize and load defaults
    configfile = "itch-batch-downloader.ini"
    config['DEFAULT'] = {
        "download_directory": "Downloads",
        "cookie_file": "cookies-itch.txt",
        "create_pdf": "ON",
        "create_png": "ON",
        "download_videos": "ON",
        "debug_logs": "OFF"
    }

    if not os.path.isfile(configfile):
        with open(configfile, "w", encoding="utf-8") as f:
            config.write(f)
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " " + "[INFO] Created new configuration. please edit {}".format(configfile))
        if sys.platform == "win32":
            x = input("Press ENTER to exit")
            sys.exit(1)

    config.read(configfile)

    main(config)
    
    newDownloads = 0

    print("")
    print("Done")
    if sys.platform == "win32":
        x = input("Press ENTER to exit")