slug: if-the-history-of-web-standards-has-shown-us
date: 2010-07-08 14:26:54
type: quote
---

> If the history of web standards has shown us anything, it’s that hacks will be necessary. By front-loading the hacks using vendor prefixes and enshrining them in the standards process, we can actually fix some of the potential problems with the process and possibly accelerate CSS development.

Well written argumentation on vendor prefixes: [Prefix or Posthack](http://www.alistapart.com/articles/prefix-or-posthack/)

 I don’t think that try are the right tool for the job, though. The prefix thing is OK, but I don’t get why it needs to be explicitly limited to vendors. A prefix is only necessary if either the syntax of the value is different (e.g. gradients) or the value is interpreted differently (e.g. box model, clip, …). If the value is just displayed differently (e.g. rendering of corners with border radius), then we don’t need prefixes.

 In my opinion prefixes should be named without relation to vendors most of the time. Only in cases where a new property is explicitly defined by a vendor e.g. Webkit’s transforms they might be prefixed with “-webkit”. But in this case other vendors implementing this to the same level as the original author should use the same vendor prefix. Why use your own vendor prefix, when you implement it exactly as original innovator? Same for gradients. Two different vendors with different syntaxes: Keep using the current prefixes. But if Opera now starts supporting the Firefox variant they should also use the “-moz” prefix by Mozilla.

 You hopefully got the idea: vendor prefixes needs to be morphed into origin-prefixes. They need to be named according to where a specific feature comes from.

 This approach has a lot of benefits. You may starting directly to use new features as the arise. They are automatically brought to other browsers supporting the same property e.g. Opera starts supporting Mozillas gradient implementation. It limits the number of variants to the lowest possible set as it only deals with the public permutations of a property/feature. And finally: one vendor might add an implementation innovated by another vendor e.g. Webkit starts to support the gradient syntax by Mozilla in parallel to their own syntax.

 What do you think about this?
