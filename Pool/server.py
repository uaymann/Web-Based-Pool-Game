import sys
import cgi
import os
import math

from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse

import Physics

class MyHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        # Parse the URL to get the path and form data
        parsed = urlparse(self.path)

        # Handle GET requests based on the path
        if parsed.path == '/shoot.html':
            self.handle_shoot_html()
        elif parsed.path.startswith("/table-") and parsed.path.endswith(".svg"):
            try:
                self.handle_svg_file()
            except FileNotFoundError:
                # If table number does not exist on the server, return a 404 response with an error message
                self.send_error_response(404, f"Could not find %s" % self.path)
        else:
            # Generate 404 for GET requests that aren't the files above
            self.send_error_response(404, f"Could not find %s" % self.path)


    def do_POST(self):
        # Handle post request
        # Parse the URL to get the path and form data
        parsed = urlparse(self.path)

        if parsed.path in ["/display.html"]:
            form = cgi.FieldStorage(fp=self.rfile,
                                    headers=self.headers,
                                    environ={'REQUEST_METHOD': 'POST',
                                            'CONTENT_TYPE':
                                                self.headers['Content-Type'],
                                            })
            
            try:
                # If required form fields are empty, raise KeyError
                if not all(form[field].value for field in ["sb_x", "sb_y", "sb_number", "rb_x", "rb_y", "rb_number", "rb_dx", "rb_dy"]):
                    raise KeyError("Required form fields are missing!")

                # Perform input validation for range
                self.validate_input_range(form)

                # Delete existing SVG files
                self.delete_existing_svg_files()

                # Compute acceleration for the rolling ball
                dx, dy, acc_x, acc_y = self.compute_acceleration(form)

                # Construct table and add balls
                table = Physics.Table()
                sb, rb = self.construct_balls(form, dx, dy, acc_x, acc_y)
                table += sb
                table += rb

                # Generate SVG tables
                self.generate_svg_tables(table)

                # Generate HTML string to display
                html_str = self.generate_html_str(form)

                # Send the response to the client
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.send_header("Content-length", len(html_str))
                self.end_headers()
                self.wfile.write(bytes(html_str, "utf-8"))
        
            except KeyError:
                # Generate 404 for missing fields
                self.send_error_response(404, f"Required form fields are missing!")
                return
            except ValueError as e:
                # Handle invalid input range
                self.send_error_response(404, f"Invalid input: {e}")
                return

        else:
            # Generate 404 for POST requests that aren't the file above
            self.send_error_response(404, f"Could not find %s" % self.path)


    def compute_acceleration(self, form):
        # Compute acceleration for the rolling ball based on its velocity
        dx = float(form["rb_dx"].value)
        dy = float(form["rb_dy"].value)
        acc_x = 0
        acc_y = 0

        speed = math.sqrt((dx * dx) + (dy * dy))

        if speed > Physics.VEL_EPSILON:
            acc_x = (-(dx) / speed * Physics.DRAG)
            acc_y = (-(dy) / speed * Physics.DRAG)

        return dx, dy, acc_x, acc_y


    def construct_balls(self, form, dx, dy, acc_x, acc_y):
        # Construct still ball and rolling ball based on form data
        pos_sb = Physics.Coordinate(float(form["sb_x"].value), float(form["sb_y"].value))
        sb = Physics.StillBall(int(form["sb_number"].value), pos_sb)

        pos_rb = Physics.Coordinate(float(form["rb_x"].value), float(form["rb_y"].value))
        vel_rb = Physics.Coordinate(dx, dy)
        acc_rb = Physics.Coordinate(acc_x, acc_y)
        rb = Physics.RollingBall(int(form["rb_number"].value), pos_rb, vel_rb, acc_rb)

        return sb, rb


    def generate_svg_tables(self, table):
        # Generate SVG tables for different segments of the table
        def phylib_print_table(table, svgIndex):
            # Function to print the SVG representation of table to a file
            if not table:
                # If the table is empty, print a message and return
                print("NULL")
                return

            # Get the svg string representation of the table
            svg_str = table.svg()

            # Create a filename based on the table index
            filename = f"table-{svgIndex}.svg"

            # Increment the index for the next table svg
            svgIndex += 1

            # Write the svg string to the file
            with open(filename, "w") as file:
                file.write(svg_str)

        # Initialize the svg table index to 0
        svgIndex = 0

        # Generate and save the svg for the initial table
        phylib_print_table(table, svgIndex)
        svgIndex += 1

        # Generate and save the svg for the next table segment
        new = table.segment()
        phylib_print_table(new, svgIndex)
        svgIndex += 1

        # Continue generating and saving svgs for subsequent table segments
        while new:
            new = new.segment()
            phylib_print_table(new, svgIndex)
            svgIndex += 1


    def generate_html_str(self, form):
        # Generate HTML string to display
        html_str = """<!DOCTYPE html>
        <html>
        <head>
            <title>Billiards</title>
            <style>
                body {
                    text-align: center;
                    background-color: sienna;
                }
                h1 {
                    margin-top: 25px;
                    font-size: 35px;
                }
                .image-container {
                    display: inline-block;
                    position: relative;
                    margin: 5px;
                    margin-top: 20px
                }
                img {
                    width: 200px;
                    height: auto;
                }
                .caption {
                    position: absolute;
                    top: 0;
                    left: 50%;
                    transform: translateX(-50%);
                    color: black;
                    font-size: 12px;
                    padding: 2px;
                    background: none;
                    margin-top: -17px;
                }
            </style>
        </head>
        <body>
            <h1>Pool Table Segments</h1>
        """

        html_str += f'<h4><p>Still Ball Original Position: ({form["sb_x"].value}, {form["sb_y"].value})'
        html_str += f'<br><br>Rolling Ball Original Position: ({form["rb_x"].value}, {form["rb_y"].value}) Velocity: ({form["rb_dx"].value}, {form["rb_dy"].value})</h4></p>'

        # Get SVG files, sort them, and include them in the HTML
        svg_files = [file for file in os.listdir(".") if file.startswith("table-") and file.endswith(".svg")]
        svg_files.sort(key=lambda x: int(x.split('-')[1].split('.')[0]))

        for file in svg_files:
            html_str += f'<div class="image-container"><img src="{file}" method="get" alt="{file}">'
            html_str += f'<div class="caption">{file}</div></div>'

        # Add a "Back" link to the shoot.html page
        html_str += """<h3><a href="/shoot.html">Back</a></h3></body></html>"""

        return html_str


    def delete_existing_svg_files(self):
        # Delete existing SVG files in the current directory
        directory = os.getcwd()
        files = os.listdir(directory)

        for file in files:
            if file.startswith("table-") and file.endswith(".svg"):
                os.remove(os.path.join(directory, file))


    def handle_shoot_html(self):
        # Handle GET request for shoot.html
        fp = open('.' + self.path)
        content = fp.read()
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.send_header("Content-length", len(content))
        self.end_headers()
        self.wfile.write(bytes(content, "utf-8"))
        fp.close()


    def handle_svg_file(self):
        # Handle GET request for SVG file
        fp = open('.' + self.path, 'rb')
        content = fp.read()
        self.send_response(200)
        self.send_header("Content-type", "image/svg+xml")
        self.send_header("Content-length", len(content))
        self.end_headers()
        self.wfile.write(content)
        fp.close()


    def send_error_response(self, code, message):
        # Send error response with status code and message
        error_html = f"""
        <html>
            <head>
                <title>{code} {self.responses[code][0]}</title>
            </head>
            <body style="
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                height: 100vh;
                background-color: midnightblue;
                color: white;
            ">
                <h1>{code} {self.responses[code][0]} :(</h1>
                <p>{message}</p>
            </body>
        </html>
        """
        self.send_response(code)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes(error_html, "utf-8"))


    def validate_input_range(self, form):
        # Validate input range for Still Ball
        sb_x = float(form["sb_x"].value)
        sb_y = float(form["sb_y"].value)
        sb_number = int(form["sb_number"].value)
        if not (28.5 <= sb_x <= 1321.5 and 28.5 <= sb_y <= 2671.5 and 1 <= sb_number <= 15):
            raise ValueError("Still Ball number or position out of range")

        # Validate input range for Rolling Ball
        rb_x = float(form["rb_x"].value)
        rb_y = float(form["rb_y"].value)
        rb_dx = float(form["rb_dx"].value)
        rb_dy = float(form["rb_dy"].value)
        if not (28.5 <= rb_x <= 1321.5 and 28.5 <= rb_y <= 2671.5):
            raise ValueError("Rolling Ball position out of range")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 server.py <port#>")
        sys.exit(1)

    try:
        port = int(sys.argv[1])
    except ValueError:
        print("Invalid port number. Please provide a valid integer port.")
        sys.exit(1)

    httpd = HTTPServer(('localhost', port), MyHandler)
    print(f"Server listening in port: {port}")
    httpd.serve_forever()
