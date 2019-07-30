#!/usr/bin/env python3
"""
I did these in a functional style using map / filter / reduce because I was bored.
  Yes I understand the code and that it might be better to do it in a more traditional
  style, but this was more fun.  We can also do strings like:

  http://localhost:8080/add/10/10/10/10 => 40.
  http://localhost:8080/subtract/40/10/5/5 => 20.

While it has been linted, I didn't include pylint disables for things as _most_ were
from instructor code.  My pylint gripes were from line too long, but considering it's
HTML content, I'm not too worried about it.  Otherwise, the code should follow
proper pepage.

Also added a Modulus operation because why not...
"""

import functools
import operator
from loguru import logger


def operator_func(op_func, args):
    logger.debug(f"Entering {op_func.__name__}")
    try:
        return str(functools.reduce(op_func, list(map(float, args))))
    except ValueError:
        return error_message(*args)
    except ZeroDivisionError:
        return "<h2>Zero Division Error</h2>"


def add(*args):
    """ Returns a STRING with the sum of the arguments """
    return operator_func(operator.add, args)


def subtract(*args):
    """ Returns a STRING with the difference of the arguments """
    return operator_func(operator.sub, args)


def multiply(*args):
    """ Returns a STRING with the product of the arguments """
    return operator_func(operator.mul, args)


def divide(*args):
    """ Returns a STRING with the quotient of the arguments """
    return operator_func(operator.truediv, args)


def modulus(*args):
    """ Returns a STRING with the remainder of the arguments """
    return operator_func(operator.mod, args)


def filter_func(arg):
    """ Attempts to float the argument, returns False if float, True otherwise """
    try:
        float(arg)
        return False
    except ValueError:
        return True


def error_message(*args):
    """ Displays the problematic arguments """
    logger.debug("Entering error_message")

    body = "<h2>Bad values:</h2><ul><li>"
    body += '</li><li>'.join(filter(filter_func, args)) + "</li></ul>"
    return body

    # Other version...
    # body = "<h2>Bad values:</h2><ul><li>"
    # body += '<li>'.join([x + "</li>" for x in args if filter_func(x)]) + "</ul>"
    # return body

    # One liner...
    # return "<h2>Bad values:</h2><ul><li>" + '<li>'.join([x + "</li>" for x in args if filter_func(x)]) + "</ul>"


# # Original function before I  went all filter on it...
# def error_message(*args):
#     """ Displays the problematic arguments """
#     logger.debug("Entering error_message")

#     body = 'Bad values:<br>'
#     for arg in args:
#         try:
#             float(arg)
#         except ValueError:
#             body += f"{arg}<br>"
#     return body


def root(*args):
    """ Returns basic root page """
    # In production I'd probably just use static text instead of the extra calls.
    #   There really just here for fun and learning.  And yes they'd clearly break
    #   if this was run anywhere but on localhost.  Again, just for fun.
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
