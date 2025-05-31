import phylib;
import sqlite3;
import os;

################################################################################
# import constants from phylib to global varaibles

BALL_RADIUS   = phylib.PHYLIB_BALL_RADIUS;
BALL_DIAMETER = phylib.PHYLIB_BALL_DIAMETER;
HOLE_RADIUS = phylib.PHYLIB_HOLE_RADIUS;
TABLE_LENGTH = phylib.PHYLIB_TABLE_LENGTH;
TABLE_WIDTH = phylib.PHYLIB_TABLE_WIDTH;
SIM_RATE = phylib.PHYLIB_SIM_RATE;
VEL_EPSILON = phylib.PHYLIB_VEL_EPSILON;
DRAG = phylib.PHYLIB_DRAG;
MAX_TIME = phylib.PHYLIB_MAX_TIME;
MAX_OBJECTS = phylib.PHYLIB_MAX_OBJECTS;
FRAME_INTERVAL = 0.01;

HEADER = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN"
                       "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg width="700" height="1375" viewBox="-25 -25 1400 2750"
        xmlns="http://www.w3.org/2000/svg"
        xmlns:xlink="http://www.w3.org/1999/xlink">
    <rect width="1350" height="2700" x="0" y="0" fill="#C0D0C0" />""";

FOOTER = """</svg>\n""";

################################################################################
# the standard colours of pool balls
# if you are curious check this out:  
# https://billiards.colostate.edu/faq/ball/colors/

BALL_COLOURS = [ 
    "WHITE",
    "YELLOW",
    "BLUE",
    "RED",
    "PURPLE",
    "ORANGE",
    "GREEN",
    "BROWN",
    "BLACK",
    "LIGHTYELLOW",
    "LIGHTBLUE",
    "PINK",             # no LIGHTRED
    "MEDIUMPURPLE",     # no LIGHTPURPLE
    "LIGHTSALMON",      # no LIGHTORANGE
    "LIGHTGREEN",
    "SANDYBROWN",       # no LIGHTBROWN 
    ];

################################################################################

class Coordinate( phylib.phylib_coord ):
    """
    This creates a Coordinate subclass, that adds nothing new, but looks
    more like a nice Python class.
    """
    pass;


################################################################################

class StillBall( phylib.phylib_object ):
    """
    Python StillBall class.
    """

    def __init__( self, number, pos ):
        """
        Constructor function. Requires ball number and position (x,y) as
        arguments.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__( self, 
                                       phylib.PHYLIB_STILL_BALL, 
                                       number, 
                                       pos, None, None, 
                                       0.0, 0.0 );
      
        # this converts the phylib_object into a StillBall class
        self.__class__ = StillBall;


    # add an svg method here
    #svg method 
    def svg(self):
        """
        Returns an SVG representation of the StillBall.
        """
        return """ <circle cx="%d" cy="%d" r="%d" fill="%s" />\n""" % (self.obj.still_ball.pos.x, self.obj.still_ball.pos.y, BALL_RADIUS, BALL_COLOURS[self.obj.still_ball.number]);

################################################################################

class RollingBall( phylib.phylib_object ):
    """
    Python RollingBall class.
    """

    def __init__(self, number, pos, vel, acc):
        """
        Constructor function. Requires ball number and position (x,y) as
        arguments.
        """

        # this creates a generic phylib_object
        phylib.phylib_object.__init__(self, 
                                       phylib.PHYLIB_ROLLING_BALL, 
                                       number, 
                                       pos, vel, acc, 
                                       0.0, 0.0);
            
        # this converts the phylib_object into a RollingBall class
        self.__class__ = RollingBall;


    # add an svg method here
    def svg(self):
        """
        Returns an SVG representation of the RollingBall.
        """
        return """ <circle cx="%d" cy="%d" r="%d" fill="%s" />\n""" % (self.obj.rolling_ball.pos.x, self.obj.rolling_ball.pos.y, BALL_RADIUS, BALL_COLOURS[self.obj.rolling_ball.number]);

################################################################################

class Hole( phylib.phylib_object ):
    """
    Python Hole class.
    """

    def __init__(self, pos):
        """
        Constructor function. Requires position (x,y) as argument.
        """

        phylib.phylib_object.__init__(self, 
                                       phylib.PHYLIB_HOLE,
                                       None,  
                                       pos, None, None, 
                                       0.0, 0.0);

        self.__class__ = Hole;


    # add an svg method here
    def svg(self):
        """
        Returns an SVG representation of the Hole.
        """
        return """<circle cx="%d" cy="%d" r="%d" fill="black" />\n""" % (self.obj.hole.pos.x, self.obj.hole.pos.y, HOLE_RADIUS);

################################################################################

class HCushion( phylib.phylib_object ):
    """
    Python HCushion class.
    """

    def __init__(self, y):
        """
        Constructor function. Requires y-coordinate as argument.
        """
        pos = phylib.phylib_coord(0, y);
        phylib.phylib_object.__init__(self, 
                                       phylib.PHYLIB_HCUSHION,  
                                       y, 
                                       None, None, None, 
                                       0.0, 0.0);

        self.__class__ = HCushion;


    # add an svg method here
    def svg(self):
        """
        Returns an SVG representation of the HCushion.
        """
        if self.obj.hcushion.y == 0:
            y = -25;
        else:
            y = 2700;
        return """ <rect width="1400" height="25" x="-25" y="%d" fill="darkgreen" />\n""" % (y);

################################################################################

class VCushion( phylib.phylib_object ):
    """
    Python VCushion class.
    """

    def __init__(self, x):
        """
        Constructor function. Requires x-coordinate as argument.
        """
        pos = phylib.phylib_coord(x, 0);
        phylib.phylib_object.__init__(self, 
                                       phylib.PHYLIB_VCUSHION,  
                                       x, 
                                       None, None, None, 
                                       0.0, 0.0);

        self.__class__ = VCushion;


    # add an svg method here
    def svg(self):
        """
        Returns an SVG representation of the VCushion.
        """
        
        if self.obj.vcushion.x == 0:
            x = -25;
        else:
            x = 1350;
        return """<rect width="25" height="2750" x="%d" y="-25" fill="darkgreen" />\n""" % (x);

################################################################################

class Table( phylib.phylib_table ):
    """
    Pool table class.
    """

    def __init__( self ):
        """
        Table constructor method.
        This method call the phylib_table constructor and sets the current
        object index to -1.
        """
        phylib.phylib_table.__init__( self );
        self.current = -1;

    def __iadd__( self, other ):
        """
        += operator overloading method.
        This method allows you to write "table+=object" to add another object
        to the table.
        """
        self.add_object( other );
        return self;

    def __iter__( self ):
        """
        This method adds iterator support for the table.
        This allows you to write "for object in table:" to loop over all
        the objects in the table.
        """
        return self;

    def __next__( self ):
        """
        This provides the next object from the table in a loop.
        """
        self.current += 1;  # increment the index to the next object
        if self.current < MAX_OBJECTS:   # check if there are no more objects
            return self[ self.current ]; # return the latest object

        # if we get there then we have gone through all the objects
        self.current = -1;    # reset the index counter
        raise StopIteration;  # raise StopIteration to tell for loop to stop

    def __getitem__( self, index ):
        """
        This method adds item retreivel support using square brackets [ ] .
        It calls get_object (see phylib.i) to retreive a generic phylib_object
        and then sets the __class__ attribute to make the class match
        the object type.
        """
        result = self.get_object( index ); 
        if result==None:
            return None;
        if result.type == phylib.PHYLIB_STILL_BALL:
            result.__class__ = StillBall;
        if result.type == phylib.PHYLIB_ROLLING_BALL:
            result.__class__ = RollingBall;
        if result.type == phylib.PHYLIB_HOLE:
            result.__class__ = Hole;
        if result.type == phylib.PHYLIB_HCUSHION:
            result.__class__ = HCushion;
        if result.type == phylib.PHYLIB_VCUSHION:
            result.__class__ = VCushion;
        return result;

    def __str__( self ):
        """
        Returns a string representation of the table that matches
        the phylib_print_table function from A1Test1.c.
        """
        result = "";    # create empty string
        result += "time = %6.1f;\n" % self.time;    # append time
        for i,obj in enumerate(self): # loop over all objects and number them
            result += "  [%02d] = %s\n" % (i,obj);  # append object description
        return result;  # return the string

    def segment( self ):
        """
        Calls the segment method from phylib.i (which calls the phylib_segment
        functions in phylib.c.
        Sets the __class__ of the returned phylib_table object to Table
        to make it a Table object.
        """

        result = phylib.phylib_table.segment( self );
        if result:
            result.__class__ = Table;
            result.current = -1;
        return result;

    # add svg method here
    def svg(self):
        """
        Generates an SVG representation of the table.
        """

        svg_str = HEADER;

        for obj in self:
            if obj is not None:
                svg_str += obj.svg();

        svg_str += FOOTER;

        return svg_str;

    def roll( self, t ):
        new = Table();
        for ball in self:
            if isinstance( ball, RollingBall ):
                # create a new ball with the same number as the old ball
                new_ball = RollingBall( ball.obj.rolling_ball.number,
                                        Coordinate(0,0),
                                        Coordinate(0,0),
                                        Coordinate(0,0) );
                # compute where it rolls to
                phylib.phylib_roll( new_ball, ball, t );
                # add ball to table
                new += new_ball;
            if isinstance( ball, StillBall ):
                # create a new ball with the same number and pos as the old ball
                new_ball = StillBall( ball.obj.still_ball.number,
                                        Coordinate( ball.obj.still_ball.pos.x,
                                                    ball.obj.still_ball.pos.y ) );
                # add ball to table
                new += new_ball;
        # return table
        return new;

    def cueBall(self):
        """
        Helper method to find the cue ball (number 0) in the table.
        Returns the cue ball object if found, None otherwise.
        """
        for ball in self:
            if isinstance(ball, StillBall):
                if ball.obj.still_ball.number == 0:
                    return ball;
        return None;

################################################################################

class Database:
    """
    Database class.
    """
    def __init__( self, reset=False ):
        """
        Database constructor method.
        This method create/open a database connection “phylib.db”,
        if reset is set to True, it should first delete the
        file “phylib.db” so that a fresh database is created upon connection.
        """
        # Database file name
        db_filename = "phylib.db";

        # Check if reset is True and the file exists
        if reset and os.path.exists(db_filename):
            os.remove(db_filename);

        # Connection to the database
        self.conn = sqlite3.connect(db_filename);

    def createDB( self ):
        """
        Creates database tables.
        """
        self.cur = self.conn.cursor();

        # Create Ball table
        self.cur.execute("""CREATE TABLE IF NOT EXISTS Ball 
                              ( BALLID  INTEGER  PRIMARY KEY  AUTOINCREMENT  NOT NULL,
                                BALLNO  INTEGER  NOT NULL,
                                XPOS    FLOAT    NOT NULL,
                                YPOS    FLOAT    NOT NULL,
                                XVEL    FLOAT,
                                YVEL    FLOAT );""");
        
        # Create TTable table
        self.cur.execute("""CREATE TABLE IF NOT EXISTS TTable 
                              ( TABLEID  INTEGER  PRIMARY KEY  AUTOINCREMENT  NOT NULL,
                                TIME     FLOAT    NOT NULL );""");
        
        # Create BallTable table
        self.cur.execute("""CREATE TABLE IF NOT EXISTS BallTable 
                              ( BALLID  INTEGER  NOT NULL,
                                TABLEID INTEGER  NOT NULL,
                                FOREIGN KEY (TABLEID) REFERENCES TTable(TABLEID) 
                                FOREIGN KEY (BALLID)  REFERENCES Ball(BALLID) );""");
        
        # Create Shot table
        self.cur.execute("""CREATE TABLE IF NOT EXISTS Shot 
                              ( SHOTID   INTEGER  PRIMARY KEY  AUTOINCREMENT  NOT NULL,
                                PLAYERID INTEGER  NOT NULL,
                                GAMEID   INTEGER  NOT NULL,
                                FOREIGN KEY (PLAYERID) REFERENCES Player(PLAYERID),
                                FOREIGN KEY (GAMEID)   REFERENCES Game(GAMEID) );""");
        
        # Create TableShot table
        self.cur.execute("""CREATE TABLE IF NOT EXISTS TableShot 
                              ( TABLEID  INTEGER  NOT NULL,
                                SHOTID   INTEGER  NOT NULL,
                                FOREIGN KEY (TABLEID) REFERENCES TTable(TABLEID),
                                FOREIGN KEY (SHOTID)  REFERENCES Shot(SHOTID) );""");
        
        # Create Game table
        self.cur.execute("""CREATE TABLE IF NOT EXISTS Game 
                              ( GAMEID   INTEGER     PRIMARY KEY  AUTOINCREMENT  NOT NULL,
                                GAMENAME VARCHAR(64) NOT NULL );""");
        
        # Create Player table
        self.cur.execute("""CREATE TABLE IF NOT EXISTS Player 
                              ( PLAYERID   INTEGER     PRIMARY KEY  AUTOINCREMENT  NOT NULL,
                                GAMEID     INTEGER     NOT NULL,
                                PLAYERNAME VARCHAR(64) NOT NULL,
                                FOREIGN KEY (GAMEID) REFERENCES Game(GAMEID) );""");
        
        # Commit the changes to the database, close cursor
        self.cur.close();
        self.conn.commit();

    def readTable( self, tableID ):
        """
        This method returns a Table object.
        """
        self.cur = self.conn.cursor();

        # Query to retrieve balls for the given tableID
        query = """SELECT Ball.BALLID, BALLNO, XPOS, YPOS, XVEL, YVEL, TTable.TIME
                   FROM Ball
                   INNER JOIN BallTable ON Ball.BALLID = BallTable.BALLID
                   INNER JOIN TTable ON BallTable.TABLEID = TTable.TABLEID
                   WHERE BallTable.TABLEID = ?;""";

        # Execute the query
        self.cur.execute(query, (tableID + 1,));

        # Fetch all rows from the result
        rows = self.cur.fetchall();

        # If there are no rows, return None
        if not rows:
            self.cur.close();
            return None;

        # Create a new Table object
        table = Table();

        # Iterate through the rows and populate the table
        for row in rows:
            ballID, ballNo, xPos, yPos, xVel, yVel, time = row;

            # Check if the ball has velocity to determine ball type
            if xVel is None and yVel is None:
                ball = StillBall(ballNo, Coordinate(xPos, yPos));
            else:
                xAcc = 0;
                yAcc = 0;
                speed = phylib.phylib_length(Coordinate(xVel, yVel));

                if speed > VEL_EPSILON:
                    xAcc = (-(xVel) / speed) * DRAG;
                    yAcc = (-(yVel) / speed) * DRAG;

                ball = RollingBall(ballNo, Coordinate(xPos, yPos), Coordinate(xVel, yVel), Coordinate(xAcc, yAcc));

            # Set the time for the table
            table.time = time;

            # Add the ball to the table
            table += ball;
        
        # Commit the changes to the database, close cursor
        self.cur.close();
        self.conn.commit();

        return table;

    def writeTable( self, table ):
        """
        Stores the contents of the Table class object in the database.
        """
        self.cur = self.conn.cursor();

        # Insert the time into the TTable table
        self.cur.execute("""INSERT 
                            INTO   TTable (TIME)
                            VALUES        (?)""", (table.time,));

        # Get last autoincremented tableID value
        tableID = self.cur.lastrowid;

        # Insert each ball into the Ball and BallTable tables
        for ball in table:

            if isinstance(ball, StillBall):
                self.cur.execute("""INSERT
                                    INTO   Ball (BALLNO, XPOS, YPOS, XVEL, YVEL)
                                    VALUES      (?, ?, ?, NULL, NULL)""",
                                                (ball.obj.still_ball.number,
                                                 ball.obj.still_ball.pos.x, 
                                                 ball.obj.still_ball.pos.y));
            
                # Get last autoincremented ballID value
                ballID = self.cur.lastrowid;

                # Insert the ballID and tableID into the BallTable table
                self.cur.execute("""INSERT
                                    INTO   BallTable (BALLID, TABLEID)
                                    VALUES           (?, ?)""",
                                                     (ballID, tableID));

            elif isinstance(ball, RollingBall):
                self.cur.execute("""INSERT 
                                    INTO   Ball (BALLNO, XPOS, YPOS, XVEL, YVEL)
                                    VALUES      (?, ?, ?, ?, ?)""",
                                                (ball.obj.rolling_ball.number,
                                                 ball.obj.rolling_ball.pos.x, 
                                                 ball.obj.rolling_ball.pos.y,
                                                 ball.obj.rolling_ball.vel.x, 
                                                 ball.obj.rolling_ball.vel.y));

                # Get last autoincremented ballID value
                ballID = self.cur.lastrowid;

                # Insert the ballID and tableID into the BallTable table
                self.cur.execute("""INSERT
                                    INTO   BallTable (BALLID, TABLEID)
                                    VALUES           (?, ?)""",
                                                     (ballID, tableID));

        # Commit the changes to the database, close cursor
        self.cur.close();
        self.conn.commit();

        # Return the autoincremented TABLEID value minus 1
        return tableID - 1;

    def getGame(self, gameID):
        """
        Retrieve game data based on the provided gameID.
        """
        self.cur = self.conn.cursor();

        # Query to retrieve gameName, player1Name, and player2Name using JOIN
        query = """SELECT g.GAMENAME, p1.PLAYERNAME, p2.PLAYERNAME
                   FROM Game AS g
                   JOIN Player AS p1 ON g.GAMEID = p1.GAMEID
                   JOIN Player AS p2 ON g.GAMEID = p2.GAMEID
                   WHERE g.GAMEID = ? AND p1.PLAYERID < p2.PLAYERID;""";

        # Execute the query
        self.cur.execute(query, (gameID,));

        # Fetch the result
        game_data = self.cur.fetchone();

        # Close cursor
        self.cur.close();

        # Return the result
        return game_data if game_data else (None, None, None);

    def setGame(self, gameName, player1Name, player2Name):
        """
        Adds a new game and players to the database.
        """
        self.cur = self.conn.cursor();

        # Begin a transaction
        self.cur.execute("BEGIN TRANSACTION;");

        try:
            # Insert the game
            self.cur.execute("""INSERT 
                                INTO Game (GAMENAME) 
                                VALUES    (?)""", 
                                          (gameName,));
            game_id = self.cur.lastrowid;

            # Insert player1Name first to get lower PLAYERID
            self.cur.execute("""INSERT 
                                INTO Player (GAMEID, PLAYERNAME)
                                VALUES      ((SELECT MAX(GAMEID) FROM Game), ?)""",
                                            (player1Name,));

            # Insert player2Name
            self.cur.execute("""INSERT 
                                INTO Player (GAMEID, PLAYERNAME)
                                VALUES      ((SELECT MAX(GAMEID) FROM Game), ?)""",
                                            (player2Name,));

            # Commit the changes to the database
            self.conn.commit();

            return game_id;

        except sqlite3.Error as e:
            self.conn.rollback();
            print("Error occurred:", e);
            return None;

        finally:
            self.cur.close();

    def newShot(self, gameName, playerName):
        """
        Add a new entry to the Shot table for the current game and the given playerName.
        Return the shotID.
        """
        self.cur = self.conn.cursor();

        # Begin a transaction
        self.cur.execute("BEGIN TRANSACTION;");

        try:
            # Get the playerID and gameID based on playerName and gameName
            self.cur.execute("""SELECT Player.PLAYERID, Game.GAMEID 
                                FROM Player 
                                INNER JOIN Game ON Player.GAMEID = Game.GAMEID 
                                WHERE Player.PLAYERNAME = ? AND Game.GAMENAME = ?""", 
                                (playerName, gameName));
            result = self.cur.fetchone();
            if result:
                playerID, gameID = result;
            else:
                return None;

            # Insert a new entry into the Shot table
            self.cur.execute("INSERT INTO Shot (PLAYERID, GAMEID) VALUES (?, ?)", (playerID, gameID));

            self.conn.commit();

            # Retrieve the shotID of the newly inserted row
            shotID = self.cur.lastrowid;

            return shotID;
        
        except sqlite3.Error as e:
            self.conn.rollback();
            print("Error adding new shot:", e);
            return None;

        finally:
            # Close cursor
            self.cur.close();

    def recordTableShot(self, tableID, shotID):
        """
        Records the association between a shot and a table in the TableShot table.
        """
        self.cur = self.conn.cursor();

        try:
            # query to insert data into the TableShot table
            self.cur.execute("""INSERT 
                                INTO TableShot (TableID, ShotID) 
                                VALUES         (?, ?);""", 
                                               (tableID, shotID));
            
            # Commit the transaction
            self.conn.commit();
                        
        except Exception as e:
            # Handle any exceptions, such as database errors
            print("Error occurred while recording TableShot:", e);
            return None;

        finally:
            # Close cursor
            self.cur.close();

    def close( self ):
        """
        Commit changes and close the connection.
        """
        self.conn.commit();
        self.conn.close();

################################################################################

class Game:
    """
    Game class.
    """
    def __init__( self, gameID=None, gameName=None, player1Name=None, player2Name=None ):
        """
        Game constructor method.
        """
        # Check for valid constructor call
        if gameID is not None and any(arg is not None for arg in [gameName, player1Name, player2Name]):
            raise TypeError("Invalid constructor call. Use either gameID with other arguments as None or string values for all three Name arguments with gameID=None.");
        elif gameID is None and any(arg is None for arg in [gameName, player1Name, player2Name]):
            raise TypeError("Invalid constructor call. Use either gameID with other arguments as None or string values for all three Name arguments with gameID=None.");

        self.gameID = gameID;
        self.gameName = gameName;
        self.player1Name = player1Name;
        self.player2Name = player2Name;

        # Initialize other attributes if gameID is provided
        if self.gameID is not None:
            # Increment gameID by 1 to match SQL numbering
            self.gameID += 1;
            # Retrieve gameName, player1Name, and player2Name from the Database
            db = Database();
            game_data = db.getGame(self.gameID);
            db.close();
            if game_data:
                self.gameName, self.player1Name, self.player2Name = game_data;

        elif self.gameID is None:
            # Store gameName, player1Name, and player2Name in the Database
            db = Database();
            self.gameID = db.setGame(gameName, player1Name, player2Name);
            db.close();

    def shoot( self, gameName, playerName, table, xvel, yvel ):
        """
        Represents a shot made in Pool game.
        """
        # Add new entry to Shot table
        db = Database();
        shotID = db.newShot(gameName, playerName);

        # Find cue ball object
        cue_ball = table.cueBall();

        # Check if cue ball exists
        if cue_ball is not None:
            # Retrieve the x and y values of the cue ball's position
            xpos = cue_ball.obj.still_ball.pos.x;
            ypos = cue_ball.obj.still_ball.pos.y;
        else:
            print("No cue ball found on table.");
            return None;

        # set type to ROLLING_BALL
        cue_ball.type = phylib.PHYLIB_ROLLING_BALL;

        # Set cue ball attributes
        cue_ball.obj.rolling_ball.number = 0;

        cue_ball.obj.rolling_ball.pos.x = xpos;
        cue_ball.obj.rolling_ball.pos.y = ypos;

        cue_ball.obj.rolling_ball.vel.x = xvel;
        cue_ball.obj.rolling_ball.vel.y = yvel;

        xacc = 0;
        yacc = 0;
        speed = phylib.phylib_length(Coordinate(xvel, yvel));
        if speed > VEL_EPSILON:
            xacc = (-(xvel) / speed) * DRAG;
            yacc = (-(yvel) / speed) * DRAG;

        cue_ball.obj.rolling_ball.acc.x = xacc;
        cue_ball.obj.rolling_ball.acc.y = yacc;
        
        segment = table;

        # Loop through segments
        while segment is not None:

            time = table.time;
            segment = table.segment();

            if (segment is not None): 

                seconds = segment.time - time;
                frames = int(seconds / FRAME_INTERVAL);

                for i in range(frames):

                    rollTime = i * FRAME_INTERVAL;
                    newTable = table.roll(rollTime);
                    newTable.time = table.time + rollTime;

                    tableID = db.writeTable(newTable) + 1;
                    db.recordTableShot(tableID, shotID);

            else:
                break;

            table = segment;
        
        db.close();
        return shotID;

