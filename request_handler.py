from http.server import BaseHTTPRequestHandler, HTTPServer
from views import get_all_animals


        # Q: the purpose of this module is to handle HTTP methods, basically the brains/innerworkings 
        # of when we would do a "PUT" or "POST" etc when interacting with an API in the past, correct?
        # A: y


# Here's a class. It inherits from another class.


        # Q: we are defining a new class, HandleRequests, which is inheriting from BaseHTTPRequestHandler, correct?
        # A:y


        # Q: where is BaseHTTPRequestHandler importing from?
        # A: builtin for python. importing from python.


        # Q: can i go to where BaseHTTPRequestHandler is importing from so that I can read the 
        # code and get a better understanding of what HandleRequests is inheriting from it?
        # A:y, https://docs.python.org/3/library/index.html

# For now, think of a class as a container for functions that
# work together for a common purpose. In this case, that
# common purpose is to respond to HTTP requests from a client.
class HandleRequests(BaseHTTPRequestHandler):
    # This is a Docstring it should be at the beginning of all classes and functions
    # It gives a description of the class or function

        # Q: I understand that we're writing this Docstring to give a description of the class or function, 
        # in what way is it beneficial to have a Docstring instead of just a comment?
        # A: docstring pops out more so it's easier to recognize
        # you generate documentation from your docstrings


        # Q: I understand that the "linter" is part of why we have to write the Docstring, 
        # because it is best practices, but what is a brief description of a "linter"?
        # A: grammar nazi, best practices enforcer


        # Q: Am I seeing that a Docstring uses triple quotes around it, and on separate lines?
        # A: y
    
    
    """Controls the functionality of any GET, PUT, POST, DELETE requests to the server
    """

    # Here's a class function


        # Q: is "def" used similarly to how const let and var are used?
        # A:indicates that you're defining specifically a function


        # Q: is _set_headers the name of our class function, and it has self and status defined as parameters?
        # _set_headers is a method
        # underscore at the beginning of the method name means don't call this method directly, 
        # internal to the class. another method of this class can call it
        # A:y


        # Q:do we call this a "class function" because it is a function, _set_headers, inside the class HandleRequests?
        # A:...


    def _set_headers(self, status):
        # Notice this Docstring also includes information about the arguments passed to the function
        """Sets the status code, Content-Type and Access-Control-Allow-Origin
        headers on the response

        Args:
            status (number): the status code to return to the front end
        """

            # Q: I do not understand the next four lines whatsoever, can I get a brief explanation?
            # A: self references the object that will be created

        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    # Another method! This supports requests with the OPTIONS verb.

            # Q: is this what runs if the requests has the OPTIONS as the http method?
            # A: y
    def do_OPTIONS(self):
        """Sets the options headers
        """
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers', 'X-Requested-With, Content-Type, Accept')
        self.end_headers()

    # Here's a method on the class that overrides the parent's method.
    # It handles any GET request.

            # Q: this is just like the OPTIONS one above, only this one will run when the request method is GET, correct?
            # A: y
    def do_GET(self):
        """Handles GET requests to the server
        """
        # Set the response code to 'Ok'
        self._set_headers(200)

        # Your new console.log() that outputs to the terminal
        print(self.path)

        # It's an if..else statement
        if self.path == "/animals":
            # In Python, this is a list of dictionaries
            # In JavaScript, you would call it an array of objects
            response = get_all_animals()

        else:
            response = []

        # This weird code sends a response back to the client
        self.wfile.write(f"{response}".encode())

    # Here's a method on the class that overrides the parent's method.
    # It handles any POST request.
    def do_POST(self):
        """Handles POST requests to the server
        """
        # Set response code to 'Created'
        self._set_headers(201)

        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        response = f"received post request:<br>{post_body}"
        self.wfile.write(response.encode())

    # Here's a method on the class that overrides the parent's method.
    # It handles any PUT request.

    def do_PUT(self):
        """Handles PUT requests to the server
        """
        self.do_POST()


# This function is not inside the class. It is the starting
# point of this application.

        # Q: this is the brains of why we've been serving our api on localhost:8088 correct?
        # A:y
def main():
    """Starts the server on port 8088 using the HandleRequests class
    """
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()


if __name__ == "__main__":
    main()
