#!/usr/bin/env python3
"""
For your homework this week, you'll be creating a wsgi application of
your own.

You'll create an online calculator that can perform several operations.

You'll need to support:

  * Addition
  * Subtractions
  * Multiplication
  * Division

Your users should be able to send appropriate requests and get back
proper responses. For example, if I open a browser to your wsgi
application at `http://localhost:8080/multiple/3/5' then the response
body in my browser should be `15`.

Consider the following URL/Response body pairs as tests:

```
  http://localhost:8080/multiply/3/5   => 15
  http://localhost:8080/add/23/42      => 65
  http://localhost:8080/subtract/23/42 => -19
  http://localhost:8080/divide/22/11   => 2
  http://localhost:8080/               => <html>Here's how to use this page...</html>
```

To submit your homework:

  * Fork this repository (Session04).
  * Edit this file to meet the homework requirements.
  * Your script should be runnable using `$ python calculator.py`
  * When the script is running, I should be able to view your
    application in my browser.
  * I should also be able to see a home page (http://localhost:8080/)
    that explains how to perform calculations.
  * Commit and push your changes to your fork.
  * Submit a link to your Session04 fork repository!

"""

import functools
import operator
from loguru import logger

# I did these in a functional style because I was bored.
#   Yes I understand the code and that it might be better
#   to do it in a more traditional style, but this is more fun.
#
# We can also do strings like
#   http://localhost:8080/add/10/10/10/10 => 40.
#   http://localhost:8080/subtract/40/10/5/5 => 20.


def add(*args):
    """ Returns a STRING with the sum of the arguments """
    logger.debug("Entering add")
    return str(functools.reduce(operator.add, list(map(float, args))))


def subtract(*args):
    """ Returns a STRING with the difference of the arguments """
    logger.debug("Entering subtract")
    return str(functools.reduce(operator.sub, list(map(float, args))))


def multiply(*args):
    """ Returns a STRING with the product of the arguments """
    logger.debug("Entering multiply")
    return str(functools.reduce(operator.mul, list(map(float, args))))


def divide(*args):
    """ Returns a STRING with the quotient of the arguments """
    logger.debug("Entering divide")
    try:
        return str(functools.reduce(operator.truediv, list(map(float, args))))
    except ZeroDivisionError:
        return "Divide by 0 error"


def modulus(*args):
    """ Returns a STRING with the product of the arguments """
    logger.debug("Entering modulus")
    return str(functools.reduce(operator.mod, list(map(float, args))))


def root(*args):
    """ Returns basic root page """
    # In production I'd probably just use static text instead of the extra calls.
    #   There really just here for fun and learning.
    return """
<style>
th, td, h1{
    text-align: center;
}
th, td{
    padding: 5px;
}
</style>
<h1>WSGI Calculator:</h1>
<table align="center">
  <tr>
    <th>Examples</th>
  </tr>
  <tr bgcolor=lightgrey><td>
    <a href="http://localhost:8080/add/23/42">/add/23/42</a> => """ + add(*(23, 42)) + """<br>
    <a href="http://localhost:8080/add/23/42/10">/add/23/42/10</a> => """ + add(*(23, 42, 10)) + """<br>
  </td></tr>
  <tr><td>
    <a href="http://localhost:8080/subtract/23/42">/subtract/23/42</a> => """ + subtract(*(23, 42)) + """<br>
    <a href="http://localhost:8080/subtract/23/42/10">/subtract/23/42/10</a> => """ + subtract(*(23, 42, 10)) + """<br>
  </td></tr>
  <tr bgcolor=lightgrey><td>
    <a href="http://localhost:8080/divide/22/11">/divide/22/11</a> => """ + divide(*(22, 11)) + """<br>
    <a href="http://localhost:8080/divide/22/11/.5">/divide/22/11/.5</a> => """ + divide(*(22, 11, .5)) + """<br>
  </td></tr>
  <tr><td>
    <a href="http://localhost:8080/multiply/3/5">/multiply/3/5</a> => """ + multiply(*(3, 5)) + """<br>
    <a href="http://localhost:8080/multiply/3/5/10">/multiply/3/5/10</a> => """ + multiply(*(3, 5, 10)) + """<br>
  </td></tr>
  <tr bgcolor=lightgrey><td>
    <a href="http://localhost:8080/modulus/81/9">/modulus/81/9</a> => """ + modulus(*(81, 9)) + """<br>
    <a href="http://localhost:8080/modulus/88/45/20">/modulus/88/45/20</a> => """ + modulus(*(88, 45, 20)) + """<br>
  </td></tr>
</table>
"""


def resolve_path(path):
    """
    Resolves path into function call and arguments

    Arguments:
        path {string} -- URI

    Raises:
        NameError: Tried to call a function that doesn't exist

    Returns:
        Return two values: a callable and an iterable of arguments.

    """
    funcs = {
        '': root,
        'add': add,
        'subtract': subtract,
        'multiply': multiply,
        'divide': divide,
        'modulus': modulus,
    }

    path = path.strip('/').split('/')
    func_name = path[0]
    args = path[1:]

    try:
        func = funcs[func_name]
    except KeyError:
        raise NameError

    return func, args


def application(environ, start_response):
    """ WSGI Application """
    headers = [("Content-type", "text/html")]
    try:
        path = environ.get('PATH_INFO', None)
        if path is None:
            raise NameError
        func, args = resolve_path(path)
        body = func(*args)
        status = "200 OK"
    except NameError:
        status = "404 Not Found"
        body = "<h1>Not Found</h1>"
    except Exception:
        status = "500 Internal Server Error"
        body = "<h1>Internal Server Error</h1>"
        print(traceback.format_exc())
    finally:
        headers.append(('Content-length', str(len(body))))
        start_response(status, headers)
        return [body.encode('utf8')]


def main():
    """ Main is main """
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()


if __name__ == '__main__':
    main()
