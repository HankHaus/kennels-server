from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from views import get_all_animals, get_single_animal, get_animals_by_location
from views import get_animals_by_status, delete_animal, update_animal
# from views import create_animal, delete_animal, update_animal
from views import get_all_locations, get_single_location
# from views import delete_location, update_location
from views import get_all_employees, get_single_employee, get_employees_by_location
# from views import create_employee, delete_employee, update_employee
from views import get_all_customers, get_single_customer, get_customers_by_email
# from views import create_customer, delete_customer, update_customer

# Q: the purpose of this module is to handle HTTP methods, basically the brains/innerworkings
# of when we would do a "PUT" or "POST" etc when interacting with an API in the past, correct?
# A: y


# Here's a class. It inherits from another class.

# Q: we are defining a new class, HandleRequests,
# which is inheriting from BaseHTTPRequestHandler, correct?
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

    # Q: I understand that we're writing this
    # Docstring to give a description of the class or function,
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

    # Q: is _set_headers the name of our class
    # function, and it has self and status defined as parameters?
    # _set_headers is a method
    # underscore at the beginning of the method name means don't call this method directly,
    # internal to the class. another method of this class can call it
    # A:y

    # Q:do we call this a "class function"
    # because it is a function, _set_headers, inside the class HandleRequests?
    # A:...

    def parse_url(self, path):
        """_summary_

        Args:
            path (_type_): _description_

        Returns:
            _type_: _description_
        """
        path_params = path.split("/")
        resource = path_params[1]

        # Check if there is a query string parameter
        if "?" in resource:
            # GIVEN: /customers?email=jenna@solis.com

            param = resource.split("?")[1]  # email=jenna@solis.com
            resource = resource.split("?")[0]  # 'customers'
            pair = param.split("=")  # [ 'email', 'jenna@solis.com' ]
            key = pair[0]  # 'email'
            value = pair[1]  # 'jenna@solis.com'

            return ( resource, key, value )

        # No query string parameter
        else:
            id = None

            try:
                id = int(path_params[2])
            except IndexError:
                pass  # No route parameter exists: /animals
            except ValueError:
                pass  # Request had trailing slash: /animals/

            return (resource, id)

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

        # Q: this is just like the OPTIONS one above,
        # only this one will run when the request method is GET, correct?
        # A: y
    def do_GET(self):
        """_summary_
        """
        self._set_headers(200)

        response = {}

        # Parse URL and store entire tuple in a variable
        parsed = self.parse_url(self.path)

        # Response from parse_url() is a tuple with 2
        # items in it, which means the request was for
        # `/animals` or `/animals/2`
        if len(parsed) == 2:
            ( resource, id ) = parsed

            if resource == "animals":
                if id is not None:
                    response = f"{get_single_animal(id)}"
                else:
                    response = f"{get_all_animals()}"
            elif resource == "customers":
                if id is not None:
                    response = f"{get_single_customer(id)}"
                else:
                    response = f"{get_all_customers()}"

        # Response from parse_url() is a tuple with 3
        # items in it, which means the request was for
        # `/resource?parameter=value`
        elif len(parsed) == 3:
            ( resource, key, value ) = parsed

            # Is the resource `customers` and was there a
            # query parameter that specified the customer
            # email as a filtering value?
            if key == "email" and resource == "customers":
                response = get_customers_by_email(value)

            elif key == "location_id" and resource == "animals":
                response = get_animals_by_location(value)

            elif key == "location_id" and resource == "employees":
                response = get_employees_by_location(value)

            elif key == "status" and resource == "animals":
                response = get_animals_by_status(value)

        self.wfile.write(response.encode())

    # Here's a method on the class that overrides the parent's method.
    # It handles any POST request.
    def do_POST(self):
        """_summary_
        """
        self._set_headers(201)
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)

        # Convert JSON string to a Python dictionary
        post_body = json.loads(post_body)

        # Parse the URL
        resource = self.parse_url(self.path)[0]

        # Initialize new animal
        new_animal = None

        # Add a new animal to the list. Don't worry about
        # the orange squiggle, you'll define the create_animal
        # function next.
        if resource == "animals":
            new_animal = create_animal(post_body)

        # Encode the new animal and send in response
        self.wfile.write(f"{new_animal}".encode())

        new_employee = None

        # Add a new animal to the list. Don't worry about
        # the orange squiggle, you'll define the create_animal
        # function next.
        if resource == "employees":
            new_employee = create_employee(post_body)

        # Encode the new animal and send in response
        self.wfile.write(f"{new_employee}".encode())

        new_customer = None

        # Add a new animal to the list. Don't worry about
        # the orange squiggle, you'll define the create_animal
        # function next.
        if resource == "customers":
            new_customer = create_customer(post_body)

        # Encode the new animal and send in response
        self.wfile.write(f"{new_customer}".encode())

    def do_PUT(self):
        """_summary_
        """
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        success = False

        if resource == "animals":
            success = update_animal(id, post_body)
        # rest of the elif's

        if success:
            self._set_headers(204)
        else:
            self._set_headers(404)

        self.wfile.write("".encode())

    # self.do_POST()

    def do_DELETE(self):
        """_summary_
        """
        # Set a 204 response code
        self._set_headers(204)

    # Parse the URL
        (resource, id) = self.parse_url(self.path)

    # Delete a single animal from the list
        if resource == "animals":
            delete_animal(id)

        if resource == "locations":
            delete_location(id)

        if resource == "employees":
            delete_employee(id)

        if resource == "customers":
            delete_customer(id)
    # Encode the new animal and send in response
        self.wfile.write("".encode())


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
