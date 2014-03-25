#!/usr/bin/env python3

import requests
import xml.etree.ElementTree as ElementTree
import markdownify
import hashlib
import datetime
import os.path

quoteTemplate = """slug: %s
date: %s
type: quote
---

%s
"""

photoTemplate = """slug: %s
date: %s
type: photo
---

%s
"""

linkTemplate = """slug: %s
date: %s
type: link
---

%s
"""

videoTemplate = """slug: %s
date: %s
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


projectName = "swerner"

photoAssetFolder = "tumblr"

articleFolder = "source/content/article"
photoFolder = "source/asset/%s" % photoAssetFolder





# Pre-create photo folder
if not os.path.isdir(photoFolder):
    os.mkdir(photoFolder)


def process(url):
    """ Main processing engine """

    pos = 0
    fetch = 50
    end = fetch

    while pos < end:
        print("Requesting %s-%s of %s" % (pos, pos+fetch, end))

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
                quoteSourceComment = post.find("quote-source").text

                quoteText = markdownify.markdownify("<blockquote>" + quoteText + "</blockquote>").rstrip("\n").lstrip("\n")
                quoteSourceComment = markdownify.markdownify(quoteSourceComment).rstrip("\n")

                fileContent = quoteTemplate % (postSlug, postExportDate, quoteText + "\n\n" + quoteSourceComment)

            elif postType == "photo":
                photoText = post.find("photo-caption").text
                photoLinkUrl = post.find("photo-link-url").text
                photoUrl = post.find("photo-url").text

                photoText = markdownify.markdownify(photoText).rstrip("\n")

                photoExtension = os.path.splitext(photoUrl)[1]
                photoResponse = requests.get(photoUrl)
                photoHash = hashlib.sha1(photoResponse.content).hexdigest()

                photoFileName = "%s-%s-%s%s" % (postExportDate, postSlug, photoHash[0:10], photoExtension)
                photoFile = open(os.path.join(photoFolder, photoFileName), "wb")
                photoFile.write(photoResponse.content)
                photoFile.close()

                photoAsset = '<img src="{{@asset.url %s/%s/%s}}"/>' % (projectName, photoAssetFolder, photoFileName)
                photoAsset = markdownify.markdownify(photoAsset).rstrip("\n")

                fileContent = photoTemplate % (postSlug, postExportDate, photoAsset + "\n\n" + photoText)

            elif postType == "link":
                linkUrl = post.find("link-url").text
                try:
                    linkText = post.find("link-text").text
                    linkText = markdownify.markdownify(linkText).rstrip("\n")
                except:
                    linkText = linkUrl

                fileContent = linkTemplate % (postSlug, postExportDate, "[%s](%s)" % (linkText, linkUrl))

            elif postType == "video":
                videoCode = post.find("video-source").text
                videoText = post.find("video-caption").text

                videoText = markdownify.markdownify(videoText).rstrip("\n")

                fileContent = videoTemplate % (postSlug, postExportDate, videoCode + "\n\n" + videoText)

            elif postType == "regular":
                postTitle = post.find("regular-title").text
                postText = post.find("regular-body").text

                postText = markdownify.markdownify(postText).rstrip("\n")
                fileContent = regularTemplate % (postExportDate, postTitle, postSlug, postText)

            else:
                print("Unknown POST-TYPE: %s" % postType)
                print(ElementTree.dump(post))
                continue

            # Write post file
            fileHandle = open(os.path.join(articleFolder, postDateOnly + "-" + postType + "-" + postSlug + ".markdown"), "w")
            fileHandle.write(fileContent)
            fileHandle.close()

        # Update for next requests
        pos = pos + fetch




process("http://sebastian-werner.com/api/read?start=%s&num=%s")
