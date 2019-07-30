# WSGI Calculator

I did these in a functional style using map / filter / reduce because I was bored.
  Yes I understand the code and that it might be better to do it in a more traditional
  style, but this was more fun.  We can also do strings like:

  * http://localhost:8080/add/10/10/10/10 => 40.
  * http://localhost:8080/subtract/40/10/5/5 => 20.

While it has been linted, I didn't include pylint disables for things as _most_ were
from instructor code.  My pylint gripes were from line too long, but considering it's
HTML content, I'm not too worried about it.  Otherwise, the code should follow
proper pepage.

Also added a Modulus operation because why not.  Added an extra test for it as well.


## How to Know When You're Done

When you have completed the TODOs, you should be able to visit the following pages and see a page with the indicated content.:
  * http://localhost:8080/multiply/3/5  => 15
  * http://localhost:8080/add/23/42  => 65
  * http://localhost:8080/subtract/23/42  => -19
  * http://localhost:8080/divide/22/11  => 2
  * http://localhost:8080/  => Here's how to use this page... (etc.)

There is also a set of tests for you to run, using `python tests.py`.
