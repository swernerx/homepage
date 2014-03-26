#!/usr/bin/env python3

import requests
import xml.etree.ElementTree as ElementTree
import markdownify
import hashlib
import datetime
import os.path
import jasy.core.Console as Console
import re

#
# LOGGING CONFIGURATION
#

import logging

# Configure log level for root logger first (enable debug level when either logfile or console verbosity is activated)
loglevel = logging.INFO
# if options.log or options.verbose is True:
#    loglevel = logging.DEBUG

# Basic configuration of console logging
logging.basicConfig(level=loglevel, format="%(message)s")

logging.getLogger("requests").setLevel(logging.WARNING)


#
# TEMPLATES FOR OUTPUT FILES
#

quoteTemplate = """slug: %s
date: %s
title: %s
type: quote
---

%s
"""

photoTemplate = """slug: %s
date: %s
title: %s
type: photo
---

%s
"""

linkTemplate = """slug: %s
date: %s
title: %s
type: link
---

%s
"""

videoTemplate = """slug: %s
date: %s
title: %s
type: video
---

%s
"""

regularTemplate = """slug: %s
date: %s
title: %s
type: regular
---

%s
"""


#
# PROJECT CONFIGURATION
#

projectName = "swerner"

photoAssetFolder = "tumblr"

postFolder = "source/content/post"
photoFolder = "source/asset/%s" % photoAssetFolder



#
# MAIN
#

# Pre-create photo folder
if not os.path.isdir(photoFolder):
    os.mkdir(photoFolder)


def ellipseTitle(content, maxlength=70):
    result = ""
    splits = content.split(" ")
    ellipse = False
    for split in splits:
        if result:
            temp = "%s %s" % (result, split)
        else:
            temp = split

        if len(temp) < maxlength:
            result = temp
        else:
            if result.endswith("!") or result.endswith("?"):
                pass
            elif result.endswith("."):
                result += ".."
            else:
                result += "..."

            break

    return result




def process(url, start=0, fetch=50):
    """ Main processing engine """

    pos = start

    # End will be updated during each request with incoming data
    end = pos + fetch

    Console.header("Tumblr Import")
    Console.info("Importing data...")
    Console.indent()

    while pos < end:
        Console.info("Requesting %s-%s of %s" % (pos, pos+fetch-1, end))

        response = requests.get(url % (pos, fetch))

        if response.status_code != 200:
            raise Exception("Error during communication with Tumblr: %s" % r.status)

        tree = ElementTree.fromstring(response.content)

        # This element contains all posts
        allPosts = tree.find("posts")

        # Update end pointer
        end = int(allPosts.get("total"))

        # Iterate trough all posts
        for post in allPosts:
            postType = post.get("type")
            postTimeStamp = post.get("unix-timestamp")
            postExportDate = str(datetime.datetime.fromtimestamp(int(postTimeStamp)))

            postSlug = post.get("slug")
            postFormat = post.get("format")
            postDateOnly = postExportDate[0:postExportDate.find(" ")]
            postFileName = "%s-%s" % (postDateOnly, postSlug)

            if postType == "quote":
                quoteText = post.find("quote-text").text
                quoteComment = post.find("quote-source").text
                quoteTitle = ellipseTitle(quoteText)

                # Post-process
                quoteText = markdownify.markdownify("<blockquote>" + quoteText + "</blockquote>").rstrip("\n").lstrip("\n")
                quoteComment = markdownify.markdownify(quoteComment).rstrip("\n")
                quoteTitle = markdownify.markdownify(quoteTitle).rstrip("\n")

                fileContent = quoteTemplate % (postSlug, postExportDate, quoteTitle, quoteText + "\n\n" + quoteComment)

            elif postType == "photo":
                photoText = post.find("photo-caption").text
                try:
                    photoLinkUrl = post.find("photo-link-url").text
                except:
                    photoLinkUrl = None
                photoUrl = post.find("photo-url").text
                photoTitle = ellipseTitle(photoText)

                # Post-process
                photoText = markdownify.markdownify(photoText).rstrip("\n")
                photoTitle = markdownify.markdownify(photoTitle).rstrip("\n")

                # Downloading image
                photoResponse = requests.get(photoUrl, allow_redirects=True)
                if photoResponse.status_code != 200:
                    Console.error("Unable to load photo. Status: %s; URL: %s", photoResponse.status_code, photoUrl)
                    continue

                # Build extension based on response headers (safer than using file extension)
                photoType = photoResponse.headers["content-type"]

                if "png" in photoType:
                    photoExtension = ".png"
                elif "jpeg" in photoType or "jpg" in photoType:
                    photoExtension = ".jpeg"
                elif "gif" in photoType:
                    photoExtension = ".gif"
                else:
                    Console.error("Unknown photo format: %s; Status: %s; URL: %s", photoType, photoResponse.status_code, photoUrl)
                    continue

                # Generating checksum
                photoHash = hashlib.sha1(photoResponse.content).hexdigest()

                # Generate file name and path from existing data
                photoFileName = "%s-%s-%s%s" % (postDateOnly, postSlug, photoHash[0:10], photoExtension)
                photoPath = os.path.join(photoFolder, photoFileName)

                # Do not repeatly write identical files
                if not os.path.exists(photoPath):
                    photoFile = open(photoPath, "wb")
                    photoFile.write(photoResponse.content)
                    photoFile.close()

                # Generate basic image tag
                photoAsset = '<img src="{{@asset.url %s/%s/%s}}" alt=""/>' % (projectName, photoAssetFolder, photoFileName)

                # Wrap with a link when it should be link to an external site
                if photoLinkUrl:
                    photoAsset = '<a href="%s">%s</a>' % (photoLinkUrl, photoAsset)

                fileContent = photoTemplate % (postSlug, postExportDate, photoTitle, photoAsset + "\n\n" + photoText)

            elif postType == "link":
                linkUrl = post.find("link-url").text
                try:
                    linkText = post.find("link-text").text
                except:
                    linkText = linkUrl

                # Post-process
                if linkText != linkUrl:
                    linkText = markdownify.markdownify(linkText).rstrip("\n")
                    linkTitle = ellipseTitle(linkText)
                else:
                    shortLinkMatch = re.compile("(.*//.*?/)").search(linkUrl)
                    if shortLinkMatch:
                        linkTitle = "Link to %s" % shortLinkMatch.group(0)
                    else:
                        linkTitle = "Link to: %s" % linkUrl

                fileContent = linkTemplate % (postSlug, postExportDate, linkTitle, "[%s](%s)" % (linkText, linkUrl))

            elif postType == "video":
                videoCode = post.find("video-source").text
                videoText = post.find("video-caption").text
                videoTitle = ellipseTitle(videoText)

                # Post-process
                videoText = markdownify.markdownify(videoText).rstrip("\n")
                videoTitle = markdownify.markdownify(videoTitle).rstrip("\n")

                fileContent = videoTemplate % (postSlug, postExportDate, videoTitle, videoCode + "\n\n" + videoText)

            elif postType == "regular":
                postText = post.find("regular-body").text

                try:
                    postTitle = post.find("regular-title").text
                except:
                    postTitle = ellipseTitle(postText)

                postText = markdownify.markdownify(postText).rstrip("\n")
                fileContent = regularTemplate % (postSlug, postExportDate, postTitle, postText)

            else:
                print("Unknown POST-TYPE: %s" % postType)
                print(ElementTree.dump(post))
                continue

            # Write post file
            fileHandle = open(os.path.join(postFolder, postDateOnly + "-" + postType + "-" + postSlug + ".markdown"), "w")
            fileHandle.write(fileContent)
            fileHandle.close()

        # Update for next requests
        pos = pos + fetch

    Console.outdent()

    Console.info("Successfully imported")


#
# EXECUTE
#

process("http://sebastian-werner.com/api/read?start=%s&num=%s")
