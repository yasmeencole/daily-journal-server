# import statements
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from entries import get_all_entries, get_single_entry
from moods import get_all_moods, get_single_mood


# Here's a class. It inherits from another class.
# For now, think of a class as a container for functions that
# work together for a common purpose. In this case, that
# common purpose is to respond to HTTP requests from a client.
class HandleRequests(BaseHTTPRequestHandler):
    # self is the first parameter, it is getting passed in automatically for us
    # self is props?
    def parse_url(self, path):
        # Just like splitting a string in JavaScript. If the
        # path is "/entries/1", the resulting list will
        # have "" at index 0, "entries" at index 1, and "1"
        # at index 2.
        # slipts on / string and returns a list
        # path is the route?
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

            # Try to get interger from path parameters at index 2 [2]
            try:
                # Convert the string "2" to the integer 2
                # This is the new parseInt() == int()
                id = int(path_params[2])
            except IndexError:
                # No route parameter exists: /entries
                pass
            except ValueError:
                # Request had trailing slash: /entries/
                pass

# it is a tuple if the return has a comma in it (resource, id)
            return (resource, id)  # This is a tuple 

    # Here's a class function
    # status is what we passed in the 200 or the 201
    def _set_headers(self, status):
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    # Another method! This supports requests with the OPTIONS verb.
    # setting up functions and something about front end
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers', 'X-Requested-With, Content-Type, Accept')
        self.end_headers()

    # Here's a method on the class that overrides the parent's method.
    # It handles any GET request.
    def do_GET(self):
        self._set_headers(200)
        response = {}  # Default response

        # Parse the URL and capture the tuple that is returned
        # this (resource, id), the stuff on the left hand side, is unpacking a tuple
        # Parse URL and store entire tuple in a variable
        parsed = self.parse_url(self.path)

        # Response from parse_url() is a tuple with 2
        # items in it, which means the request was for
        # `/entries` or `/entries/2`
        if len(parsed) == 2:
            ( resource, id ) = parsed
            
            if resource == "entries":
                # if this is true then get a signle entry
                if id is not None:
                # In Python, this is a list of dictionaries
                # In JavaScript, you would call it an array of objects
                # gets a signle entry
                    response = f"{get_single_entry(id)}"
                # else, this is false, then it gets back all of the entries
                else:
                    response = f"{get_all_entries()}"   
            elif resource == "moods":
                # if this is true then get a signle mood
                if id is not None:
                # In Python, this is a list of dictionaries
                # In JavaScript, you would call it an array of objects
                # gets a signle mood
                    response = f"{get_single_mood(id)}"
                # else, this is false, then it gets back all of the moods
                else:
                    response = f"{get_all_moods()}"

        # Response from parse_url() is a tuple with 3
        # items in it, which means the request was for
        # `/resource?parameter=value`
        # elif len(parsed) == 3:
        #     ( resource, key, value ) = parsed

            # Is the resource `moods` and was there a
            # query parameter that specified the mood
            # email as a filtering value?
            # if key == "email" and resource == "customers":
            #     response = get_customers_by_email(value)
        # wfile contains the output stream for writing a response back to the client. Proper adherence to the HTTP protocol
        # must be used when writing to this stream in order to achieve successful interoperation with HTTP clients.
        # sends a response back to the client
        self.wfile.write(response.encode())


    # Here's a method on the class that overrides the parent's method.
    # It handles any POST request.
    def do_POST(self):
    #     # Set response code to 201 'Created'
        self._set_headers(201)

        content_len = int(self.headers.get('content-length', 0))
    #     # rfile reads response from server
        post_body = self.rfile.read(content_len)

        # Convert JSON string to a Python dictionary
        post_body = json.loads(post_body)

    #     # Parse the URL
        (resource, id) = self.parse_url(self.path)

    #     # Initialize new entry
        new_object = None

        # Add a new entry to the list. Don't worry about
        # the orange squiggle, you'll define the create_entry
        # function next.
        # if resource == "entries":
        #     new_object  = create_entry(post_body)

        # # if resource == "moods":
        #     new_object  = create_mood(post_body)         
        
        # Encode the new entry and send in response
        self.wfile.write(f"{new_object }".encode())

    # Here's a method on the class that overrides the parent's method.
    # It handles any PUT request.
    # PUT request is used to update resource
    # def do_PUT(self):
    #     self._set_headers(201)
    #     # content-length tells what to read and how far to read
    #     content_len = int(self.headers.get('content-length', 0))
    #     post_body = self.rfile.read(content_len)
    #     # turns into post body when json loads
    #     post_body = json.loads(post_body)

    #     # Parse the URL
    #     (resource, id) = self.parse_url(self.path)
        
    #     success = False

    #     # checks for resourse, passes id and post body
    #     if resource == "entries":
    #         success = update_entry(id, post_body)
    #     if success:
    #         self._set_headers(204)
    #     else:
    #         self._set_headers(404)

    #     if resource == "moods":
    #         update_mood(id, post_body)    

    #     # Encode the new entry and send in response
    #     self.wfile.write("".encode())


    # def do_DELETE(self):
    # # Set a 204 response code
    # # A 204 response code in HTTP means, "I, the server, successfully processed your request, 
    # # but I have no information to send back to you."
    #     self._set_headers(204)

    # # Parse the URL
    #     (resource, id) = self.parse_url(self.path)

    # # Delete a single entry from the list
    #     if resource == "entries":
    #         delete_entry(id)

    #     if resource == "moods":
    #         delete_mood(id)

    # # Encode the new entry and send in response
    #     self.wfile.write("".encode())    


# This function is not inside the class. It is the starting
# point of this application.
def main():
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()

if __name__ == "__main__":
    main()

# run pipenv shell to create virtul environment