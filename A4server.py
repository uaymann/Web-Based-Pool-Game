import sys
import cgi
import os
import math
import mimetypes
import json

from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse

import Physics

# HTTP server that includes a connection to the database
class EnhancedHTTPServer(HTTPServer):
    # initializes the server with an address, request handler class, and database connection
    def __init__(self, server_address, RequestHandlerClass, db):
        super().__init__(server_address, RequestHandlerClass)  # initializes the parent class
        self.db = db  # here we store the database connection in the server instance

# Create an instance of the Table class
table_instance = Physics.Table()
# Generate the initial SVG content for the table
initial_svg_content = table_instance.initializeEntireTable()
# Define global variables to store player names and game name
stored_player1_name = ''
stored_player2_name = ''
stored_game_name = ''
current_player = None
loser = None
winner = None
ball_set = None
player1Balls = 0
player2Balls = 0

def write_file(html_content, callback):
        # Write file logic here
        with open('animate.html', 'w') as file:
            file.write(html_content)
        # Call the callback function once the file is written
        callback()

class MyHandler(BaseHTTPRequestHandler):

    # method that sets up the handler
    #def setup(self):
     #   super().setup()
      #  self.db = self.server.db # stores the dabatase connection

    #def db(self):
     #   return self.server.db

    def do_GET(self):

        parsed = urlparse(self.path)

        if parsed.path.startswith('/'):
            filepath = '.' + self.path  # Assuming files are served from the current directory
            if os.path.isfile(filepath):
                # Determine the file's MIME type and serve it
                mimetype, _ = mimetypes.guess_type(filepath)
                try:
                    global current_player
                    global stored_player1_name
                    global stored_player2_name
                    global loser
                    global winner
                    global player1Balls
                    global player2Balls
                    
                    with open(filepath, 'rb') as file:
                        content = file.read().decode('utf-8')
                    
                    svg_content = initial_svg_content.svg()
                    # Replace the placeholder for SVG content with the actual SVG string
                    content = content.replace('<!-- SVG_CONTENT -->', svg_content)
                    # Add the current player's name to the content
                    if loser is not None:
                        if stored_player1_name == loser:
                            winner = stored_player2_name
                        else:
                            winner = stored_player1_name
                        current = None
                        content += f"var winner = '{winner}';"  # Set winner in JavaScript
                        content += "window.localStorage.setItem('winner', winner);"  # Store winner in localStorage
                        content += f"var currentPlayerName = '{current}'"
                    elif winner is not None:
                        current = None
                        print("winner: ", winner)
                        print("player1balls:", player1Balls)
                        print("player2balls:", player2Balls)
                        content += f"var winner = '{winner}';"  # Set winner in JavaScript
                        content += "window.localStorage.setItem('winner', winner);"  # Store winner in localStorage
                        content += f"var currentPlayerName = '{current}'"
                    elif current_player is None:
                        current = stored_player1_name
                        content += f"var currentPlayerName = '{current}'"
                    elif current_player == stored_player1_name:
                        current = stored_player2_name
                        content += f"var currentPlayerName = '{current}'"
                    elif current_player == stored_player2_name:
                        current = stored_player1_name
                        content += f"var currentPlayerName = '{current}'"
                    
                    # Add the current player's name to the content
                    self.send_response(200)
                    self.send_header('Content-type', mimetype or 'application/octet-stream')
                    self.end_headers()
                    self.wfile.write(content.encode('utf-8'))
                except FileNotFoundError:
                    self.send_error(404, 'File Not Found: %s' % self.path)

        elif parsed.path.endswith(".js"):
            try:
                with open('.' + self.path, 'rb') as file:
                    content = file.read()
                self.send_response(200)
                self.send_header("Content-type", "application/javascript")
                self.send_header("Content-length", len(content))
                self.end_headers()
                self.wfile.write(content)
            except FileNotFoundError:
                self.send_error(404, 'File Not Found: %s' % self.path)

        elif parsed.path.startswith('/table-') and parsed.path.endswith('.svg'):
            # Serve SVG files
            table_file = parsed.path[1:]
            if os.path.exists(table_file):
                with open(table_file, 'rb') as file:
                    content = file.read()
                self.send_response(200)
                self.send_header('Content-type', 'image/svg+xml')
                self.end_headers()
                self.wfile.write(content);
                
            else:
                self.send_error(404, 'File Not Found: %s' % self.path)

        else:
            # generate 404 for GET requests that aren't the 3 files above
            self.send_response( 404 );
            self.end_headers();
            self.wfile.write( bytes( "404: %s not found" % self.path, "utf-8" ) );


    def do_POST(self):

        global stored_player1_name, stored_player2_name, stored_game_name
       
        parsed = urlparse(self.path) #get data by parsing url

        if parsed.path in ['/send']:

            global initial_svg_content
            global html_content
            global player1Balls
            global player2Balls

            # Access stored player names and game name
            player1Name = stored_player1_name
            player2Name = stored_player2_name
            gameName = stored_game_name

            self.set_player_and_ball_set(player1Name, player2Name)
            
            #read data 
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')

            #conver the sent data from json into python
            parsed_data = json.loads(post_data)
            velocity_x = parsed_data['velocity_x']
            velocity_y = parsed_data['velocity_y']

            print("Received velocity data: x =", velocity_x, ", y =", velocity_y)  # Add this line for debugging

            html_content = "<html><head><title>Pool Game</title><link rel='stylesheet' href='style.css'>"
            html_content += "<script src='https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js'></script><script src='game.js'></script></head><body>"
   
            # Call the shoot function with the game, table, and velocity data
            game = Physics.Game(gameName=gameName, player1Name=player1Name, player2Name=player2Name)

            if (current_player == player1Name):
                low = 1
            elif (current_player == player2Name):
                low = 0

            print("LOW=", low)
            
            result = game.shoot(gameName, current_player, initial_svg_content, velocity_x, velocity_y, low)
            if isinstance(result, tuple):
                if len(result) == 5:
                    svg_tables, table, playerName, numShot, gameName = result
                    initial_svg_content = table
                    if (playerName == player1Name):
                        player1Balls += numShot
                    elif (playerName == player2Name):
                        player2Balls += numShot

                    print("player1balls:", player1Balls)
                    print("player2balls:", player2Balls)
                elif len(result) == 3:
                    global loser
                    svg_tables, table, loser = result
                    initial_svg_content = table
                elif len(result) == 4:
                    global winner
                    svg_tables, table, playerName, numShot = result
                    initial_svg_content = table
                    if (playerName == player1Name):
                        winner = player1Name
                    elif (playerName == player2Name):
                        winner = player2Name
                    else:
                        winner = "Everyone"
                    print("winner: ", winner)
                    print("player1balls:", player1Balls)
                    print("player2balls:", player2Balls)
            else:
                table = result
                svg_tables = table.svg()
                initial_svg_content = table
                self.set_player_and_ball_set(player1Name, player2Name)

            html_content += f"""<div id="svgContainer" style="position: relative;">"""

            # Concatenate SVGs with a delimiter
            svg_data = ''.join(svg_tables)

            html_content += f"""<input type="hidden" id="svgData" value="{svg_data}">"""

            html_content += "</div>"
            html_content += '</body></html>' 

            write_file(html_content, lambda: self.navigate_to_animate_html())

        if parsed.path in ['/formresponse']:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')

    	    # Convert the POST data from JSON to a Python dictionary
            parsed_data = json.loads(post_data)
            # Extract player names and game name from the parsed data
            stored_player1_name = parsed_data.get('player1_name', '')
            stored_player2_name = parsed_data.get('player2_name', '')
            stored_game_name = parsed_data.get('game_name', '')
            
            # Now you have the player names and game name, you can use them as needed
            print("Player 1 Name:", stored_player1_name)
            print("Player 2 Name:", stored_player2_name)
            print("Game Name:", stored_game_name)
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"message": "Success"}).encode('utf-8'))

        else:
            # Generate 404 for POST requests that aren't the file above
            self.send_error_response(404, f"Could not find %s" % self.path)

        
    def navigate_to_animate_html(self):
        global html_content
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Location', '/animate.html')
        self.end_headers()
        self.wfile.write(json.dumps(html_content).encode('utf-8'))

    def set_player_and_ball_set(self, player1_name, player2_name):
        global current_player, ball_set
        if current_player is None or current_player == player2_name:
            current_player = player1_name
            ball_set = "low"
        else:
            current_player = player2_name
            ball_set = "high"

        
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



if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 server.py <port#>")
        sys.exit(1)

    try:
        port = int(sys.argv[1])
    except ValueError:
        print("Invalid port number. Please provide a valid integer port.")
        sys.exit(1)

    
    db = Physics.Database(True)
    db.createDB()  
    

    server_address = ('localhost', port)
    httpd = EnhancedHTTPServer(server_address, MyHandler, db)
    print(f"Server listening in port: {port}")
    httpd.serve_forever()
