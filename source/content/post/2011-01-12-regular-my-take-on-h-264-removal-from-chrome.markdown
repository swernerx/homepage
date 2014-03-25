slug: my-take-on-h-264-removal-from-chrome
date: 2011-01-12 09:26:27
title: My take on H.264 removal from Chrome
type: regular
---

Google will remove H.264 playback support for video tags in one of the next updates.

 **The obvious things:**

 * Using hardware for decoding is good (better battery life, better performance).
 * Video playback on smartphones and tablets is not realistic without hardware acceleration.
 * Hardware decoding of codecs would be useful on devices sold the last years.
 * There are no WebM-supporting chips in devices at the moment.
 * At the moment H.264 is seen as the better quality codec compared to WebM by most experts.
 * WebM is for the web only. It is nowhere outside the web at the moment. Not even a single Blu-Ray player or other gadget supporting WebM.
 * The industry (Sony, Microsoft, LG, Samsung, …) has already chosen H.264 for established products like Blu-Ray or digital TV broadcast (DVB in Germany).
 * Supporting two different codes (with maybe different qualities/resolutions results in higher costs with no benefit except device support).
 * The natural fallback for HTML5 video is Flash.
 * Flash is widely available.
 * Flash supports H.264 (even with hardware decoding on some platforms).
 * Flash is able to pretty quickly add new codecs.
 * Next Flash version will add support for WebM (with no hardware decoding at all).
 * Adoption to new Flash versions on desktop machines is also pretty fast.
 * It’s easier to software decode videos on desktop computers than on mobile devices.
 * Switching to WebM would be easier with some hardware supporting it already.
 * WebM is not even playable on currently sold devices (not even via software only).
 * Content producers can’t drop H.264 for WebM until WebM is supported on all interesting devices.
 **Conclusion:**

 If the web goes another way then the rest of the industry we might fallback to software playback for video on desktop. As the desktop is the only area where one can realistically use software to decode video without too much tradeoffs.

 I think it is out of question that there will be ever home entertainment systems and personal audio devices supporting software decoding of any video format. Battery life and low heat production is that important.

 The question is if Google would disable H.264 on Android and Chrome on Android in the same time frame as removing it from the desktop browser. There is no official word on this at the moment.

 **Suggestion for publishers:**

 Go with Flash for H.264 in Chrome. As long as Android still supports H.264 this seems to be the simplest and least expensive choice. 
