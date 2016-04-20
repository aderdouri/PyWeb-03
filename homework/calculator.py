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
  http://localhost:8080/divide/6/0     => HTTP "400 Bad Request"
  http://localhost:8080/               => <html>Here's how to use this page...</html>
```

To submit your homework:

  * Fork this repository (Session03).
  * Edit this file to meet the homework requirements.
  * Your script should be runnable using `$ python calculator.py`
  * When the script is running, I should be able to view your
    application in my browser.
  * I should also be able to see a home page (http://localhost:8080/)
    that explains how to perform calculations.
  * Commit and push your changes to your fork.
  * Submit a link to your Session03 fork repository!


"""


def multiply(*args):
    """ Returns a STRING with the multiplication of the arguments """

    # TODO: Fill mult with the correct value, based on the
    # args provided.
    a = int(args[0])
    b = int(args[1])
    res = a * b
    return str(res)
    raise ValueError

# TODO: Add functions for handling more arithmetic operations.

def add(*args):
    """ Returns a STRING with the sum of the arguments """

    # TODO: Fill sum with the correct value, based on the
    # args provided.
    a = int(args[0])
    b = int(args[1])
    res = a + b
    return str(res)
    raise ValueError

def subtract(*args):
    """ Returns a STRING with the substraction of the arguments """

    # TODO: Fill sum with the correct value, based on the
    # args provided.
    a = int(args[0])
    b = int(args[1])
    res = a - b
    return str(res)
    raise ValueError

def divide(*args):
    """ Returns a STRING with the division of the arguments """

    # TODO: Fill res with the correct value, based on the
    # args provided.
    a = int(args[0])
    b = int(args[1])
    if b == 0:
        raise ZeroDivisionError("divide by zero")
    else:
        res = a/b

    return str(res)
    raise ValueError

def resolve_path(path):
    """
    Should return two values: a callable and an iterable of
    arguments.
    """

    # TODO: Provide correct values for func and args. The
    # examples provide the correct *syntax*, but you should
    # determine the actual values of func and args using the
    # path.

    lstripedPath = path.lstrip('/')
    funcArgs = []
    funcArgs = lstripedPath.split('/')
    x= len(funcArgs)
    if len(funcArgs) < 2:
        raise ValueError
    func = eval(funcArgs[0])
    args = funcArgs[1:]

    return func, args
    # we get here if no url matches
    raise NameError

def application(environ, start_response):
    # TODO: Your application code from the book database
    # work here as well! Remember that your application must
    # invoke start_response(status, headers) and also return
    # the body of the response in BYTE encoding.
    headers = [("Content-type", "text/html")]
    try:
        path = environ.get('PATH_INFO', None)
        if path is None:
            raise NameError
        func, args = resolve_path(path)
        body = "{0} {1} and {2} equals {3}".format(func.__name__, args[0], args[1], func(*args))

        status = "200 OK"
    except NameError:
        status = "404 Not Found"
        body = "<h1>Not Found</h1>"
    except ZeroDivisionError:
        status = "400 HTTP Bad Request"
        body = "<h1>divide by zero</h1>"
    except ValueError:
        status = "500 Internal Server Error"


        page = """
        <!DOCTYPE html>
        <html>
        <body>
        This page explains how to perform calculations. Supported operations are Addition, Subtractions, Multiplication and Division. 

        <p>Addition Example: <a href="http://localhost:8080/add/23/42">http://localhost:8080/add/23/42</a> Excepected result: 15 </p>

        <p>Multiplication Example: <a href="http://localhost:8080/multiply/3/5">http://localhost:8080/multiply/3/5</a> Excepected result: 65 </p>

        <p>Subtractions Example: <a href="http://localhost:8080/subtract/23/42">http://localhost:8080/subtract/23/42</a> Excepected result: 19 </p>

        <p>Division Example: <a href="http://localhost:8080/divide/22/11">http://localhost:8080/divide/22/11</a> Excepected result: 2 </p>

        <p>Division by zero Example: <a href="http://localhost:8080/divide/6/0">http://localhost:8080/divide/6/0</a> Excepected result: Bad Request </p>

        <p>Here's how to use this page: <a href="http://localhost:8080/">Home page</a> </p>

        </body>
        </html>
        """
        body = page
        #body = "<html>Bad argument. Here's how to use this page...</html>"
    except Exception:
        status = "500 Internal Server Error"
        body = "<h1>Internal Server Error</h1>"
    finally:
        headers.append(('Content-length', str(len(body))))
        start_response(status, headers)
        return [body.encode('utf8')]

    #
    # TODO (bonus): Add error handling for a user attempting
    # to divide by zero.
    # Abderrazak DERDOURI: One solution is to catch the exception ZeroDivisionError above
    #

if __name__ == '__main__':
    # TODO: Insert the same boilerplate wsgiref simple
    # server creation that you used in the book database.
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()
