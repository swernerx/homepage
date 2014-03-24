#!/usr/bin/env python3

import requests
import xml.etree.ElementTree as ElementTree
import markdownify

template = """
title: %s
date: %s
---

%s
"""


def process(url):
    pos = 0
    fetch = 10
    end = fetch

    while pos < end:
        print("Requesting %s-%s of %s" % (pos, pos+fetch, end))

        response = requests.get(url % pos)

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

            if postType == "quote":
                postTitle = None
                quoteText = post.find("quote-text").text
                quoteSourceComment = post.find("quote-source").text
                print(">>> QUOTE: %s " % quoteText)

            elif postType == "photo":
                photoDescription = post.find("photo-caption").text
                photoLinkUrl = post.find("photo-link-url").text
                photoUrl = post.find("photo-url").text

                photoText = markdownify.markdownify(photoDescription)
                print(">>> PHOTO: %s" % photoText)

            elif postType == "link":
                linkText = post.find("link-text").text
                linkUrl = post.find("link-url").text

                print(">>> LINK: %s" % linkText)

            else:
                print("Unknown POST-TYPE: %s" % postType)
                print(ElementTree.dump(post))









        # Update for next requests
        pos = pos + fetch




process("http://sebastian-werner.com/api/read?start=%s&num=10")
