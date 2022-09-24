"""
References

    Full page screenshot: https://stackoverflow.com/questions/41721734/take-screenshot-of-full-page-with-selenium-python-with-chromedriver/57338909#57338909
    selenium_wait_for_images_loaded.py: https://gist.github.com/munro/7f81bd1657499866f7c2
"""

import os
import time

from PIL import Image
Image.MAX_IMAGE_PIXELS = None
from textwrap import dedent
from datetime import datetime

def fullpage_screenshot(driver, file, debugon=False):

        if debugon: 
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " " + "[DEBUG] " + "Starting chrome full page screenshot workaround ...")

        total_width = driver.execute_script("return document.body.offsetWidth")
        total_height = driver.execute_script("return document.body.parentNode.scrollHeight")
        viewport_width = driver.execute_script("return document.body.clientWidth")
        viewport_height = driver.execute_script("return window.innerHeight")
        if debugon: 
            print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " " + "[DEBUG] " + "Total: ({0}, {1}), Viewport: ({2},{3})".format(total_width, total_height,viewport_width,viewport_height))
        rectangles = []

        i = 0
        while i < total_height:
            ii = 0
            top_height = i + viewport_height

            if top_height > total_height:
                top_height = total_height

            while ii < total_width:
                top_width = ii + viewport_width

                if top_width > total_width:
                    top_width = total_width

                if debugon: 
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " " + "[DEBUG] " + "Appending rectangle ({0},{1},{2},{3})".format(ii, i, top_width, top_height))
        
                rectangles.append((ii, i, top_width,top_height))

                ii = ii + viewport_width

            i = i + viewport_height

        stitched_image = Image.new('RGB', (total_width, total_height))
        previous = None
        part = 0

        for rectangle in rectangles:
            if not previous is None:
                lenOfPage = driver.execute_script("window.scrollTo({0}, {1})".format(rectangle[0], rectangle[1])+";var lenOfPage=document.body.scrollHeight;return lenOfPage;")
                match=False
                while(match==False):
                    lastCount = lenOfPage
                    time.sleep(3)
                    lenOfPage = driver.execute_script("window.scrollTo({0}, {1})".format(rectangle[0], rectangle[1])+";var lenOfPage=document.body.scrollHeight;return lenOfPage;")
                    if lastCount==lenOfPage:
                        match=True
                     
                if debugon: 
                    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " " + "[DEBUG] " + "Scrolled To ({0},{1})".format(rectangle[0], rectangle[1]))
        
                time.sleep(0.2)

            file_name = "part_{0}.png".format(part)
            if debugon: 
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " " + "[DEBUG] " + "Capturing {0} ...".format(file_name))

            driver.get_screenshot_as_file(file_name)
            screenshot = Image.open(file_name)

            if rectangle[1] + viewport_height > total_height:
                offset = (rectangle[0], total_height - viewport_height)
            else:
                offset = (rectangle[0], rectangle[1])

            if debugon: 
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " " + "[DEBUG] " + "Adding to stitched image with offset ({0}, {1})".format(offset[0],offset[1]))
            stitched_image.paste(screenshot, offset)

            del screenshot
            os.remove(file_name)
            part = part + 1
            previous = rectangle

        stitched_image.save(file)
        if debugon: 
                print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " " + "[DEBUG] " + "Finishing chrome full page screenshot workaround ...")
            
        return True
        
def wait_until_images_loaded(driver, timeout=30):
    """ Waits for all images & background images to load """
    driver.set_script_timeout(timeout)
    driver.execute_async_script(dedent('''
        function extractCSSURL(text) {
            var url_str = text.replace(/.*url\((.*)\).*/, '$1');
            if (url_str[0] === '"') {
                return JSON.parse(url_str);
            }
            if (url_str[0] === "'") {
                return JSON.parse(
                    url_str
                        .replace(/'/g, '__DOUBLE__QUOTE__HERE__')
                        .replace(/"/g, "'")
                        .replace(/__DOUBLE__QUOTE__HERE__/g, '"')
                );
            }
            return url_str;
        }

        function imageResolved(url) {
            return new $.Deferred(function (d) {
                var img = new Image();
                img.onload = img.onload = function () {
                    d.resolve(url);
                };
                img.src = url;
                if (img.complete) {
                    d.resolve(url);
                }
            }).promise();
        }

        var callback = arguments[arguments.length - 1];
        $.when.apply($, [].concat(
            $('img[src]')
                .map(function (elem) { return $(this).attr('src'); })
                .toArray(),
            $('[style*="url("]')
                .map(function () { return extractCSSURL($(this).attr('style')); })
                .toArray()
                .map(function (url) { return imageResolved(url); })
        )).then(function () { callback(arguments); });
        return undefined;
    '''))