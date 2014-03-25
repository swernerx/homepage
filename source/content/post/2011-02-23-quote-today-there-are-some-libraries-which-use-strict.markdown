slug: today-there-are-some-libraries-which-use-strict
date: 2011-02-23 10:32:37
type: quote
---

> Today there are some libraries which use strict equal with typeof and similar constructs that are completely safe for == checks. At the same time, there are also libraries which do not do this. Nit-picking on micro-optimization, non-strict == operator, comparing with the same types, is faster in many current implementations than === operator. With different types, obviously === is faster.

[ECMA-262 - Equality operators](http://dmitrysoshnikov.com/notes/note-2-ecmascript-equality-operators/)
