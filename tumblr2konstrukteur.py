#!/usr/bin/env python3

import requests
import xml.etree.ElementTree as ElementTree
import markdownify
import hashlib
import os.path

template = """
title: %s
date: %s
---

%s
"""

photoAssetFolder = "tumblr"
photoFolder = "source/asset/%s" % photoAssetFolder
projectName = "swerner"

if not os.path.isdir(photoFolder):
    os.mkdir(photoFolder)


def process(url):
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
        #end = allPosts.get("total")


        # Iterate trough all posts
        for post in allPosts:
            postType = post.get("type")
            postDate = post.get("date-gmt")
            postSlug = post.get("slug")
            postFormat = post.get("format")

            if postType == "quote":
                quoteText = post.find("quote-text").text
                quoteSourceComment = post.find("quote-source").text

                quoteText = markdownify.markdownify(quoteText).rstrip("\n")
                quoteSourceComment = markdownify.markdownify(quoteSourceComment).rstrip("\n")
                print(">>> QUOTE: %s " % quoteText)

            elif postType == "photo":
                photoText = post.find("photo-caption").text
                photoLinkUrl = post.find("photo-link-url").text
                photoUrl = post.find("photo-url").text

                photoText = markdownify.markdownify(photoText).rstrip("\n")
                print(">>> PHOTO: %s" % photoText)

                photoExtension = os.path.splitext(photoUrl)[1]
                photoResponse = requests.get(photoUrl)
                photoHash = hashlib.sha1(photoResponse.content).hexdigest()

                photoFileName = "%s%s" % (photoHash, photoExtension)
                photoFile = open(os.path.join(photoFolder, photoFileName), "wb")
                photoFile.write(photoResponse.content)
                photoFile.close()

                photoAsset = '<img src="{{@asset.url %s/%s/%s}}"/>' % (projectName, photoAssetFolder, photoFileName)
                print(">>> PHOTO ASSET: %s" % photoAsset)

            elif postType == "link":
                linkText = post.find("link-text").text
                linkUrl = post.find("link-url").text

                linkText = markdownify.markdownify(linkText).rstrip("\n")
                print(">>> LINK: %s" % linkText)

            elif postType == "regular":
                postTitle = post.find("regular-title").text
                postText = post.find("regular-body").text

                postText = markdownify.markdownify(postText).rstrip("\n")
                print(">>> REGULAR: %s" % postText)

            else:
                print("Unknown POST-TYPE: %s" % postType)
                print(ElementTree.dump(post))









        # Update for next requests
        pos = pos + fetch




process("http://sebastian-werner.com/api/read?start=%s&num=%s")
