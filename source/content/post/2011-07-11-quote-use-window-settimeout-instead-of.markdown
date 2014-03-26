slug: use-window-settimeout-instead-of
date: 2011-07-11 02:49:56
title: Use window.setTimeout instead of window.setInterval to ensure that...
type: quote
---

> Use window.setTimeout instead of window.setInterval to ensure that the browser has enough time to update between every single iteration. This is necessary because window.setInterval(callback, ms) tries to fire its callback every n milliseconds rather than providing n milliseconds between each time it fires.

Interesting: [JavaScript Timer Congestion @ fitzgeraldnick.com](http://fitzgeraldnick.com/weblog/40/)
