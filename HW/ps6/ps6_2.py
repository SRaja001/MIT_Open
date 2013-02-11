# Problem Set 6: Simulating robots
# Name:
# Collaborators:
# Time:

import math
import random

import ps6_visualize
import pylab

# === Provided classes

class Position(object):
    """
    A Position represents a location in a two-dimensional room.
    """
    def __init__(self, x, y):
        """
        Initializes a position with coordinates (x, y).
        """
        self.x = x
        self.y = y
    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def getNewPosition(self, angle, speed):
        """
        Computes and returns the new Position after a single clock-tick has
        passed, with this object as the current position, and with the
        specified angle and speed.

        Does NOT test whether the returned position fits inside the room.

        angle: float representing angle in degrees, 0 <= angle < 360
        speed: positive float representing speed

        Returns: a Position object representing the new position.
        """
        old_x, old_y = self.getX(), self.getY()
        # Compute the change in position
        delta_y = speed * math.cos(math.radians(angle))
        delta_x = speed * math.sin(math.radians(angle))
        # Add that to the existing position
        new_x = old_x + delta_x
        new_y = old_y + delta_y
        return Position(abs(new_x), abs(new_y))

# === Problems 1

class RectangularRoom(object):
    """
    A RectangularRoom represents a rectangular region containing clean or dirty
    tiles.

    A room has a width and a height and contains (width * height) tiles. At any
    particular time, each of these tiles is either clean or dirty.
    """
    def __init__(self, width, height):
        """
        Initializes a rectangular room with the specified width and height.

        Initially, no tiles in the room have been cleaned.

        width: an integer > 0
        height: an integer > 0
        """
        self.width = width
        self.height = height
        self.tile = [[0]*width for i in xrange(height)]
        self.frac = 0
        
        #raise NotImplementedError
    
    def cleanTileAtPosition(self, pos):
        """
        Mark the tile under the position POS as cleaned.

        Assumes that POS represents a valid position inside this room.

        pos: a Position.  [x, y]
        """
        self.tile[pos[0]][pos[1]] = 1
        clean_tiles = self.getNumCleanedTiles()
        tiles = self.getNumTiles()
        self.frac = clean_tiles/float(tiles)


    def isTileCleaned(self, m, n):
        """
        Return True if the tile (m, n) has been cleaned.

        Assumes that (m, n) represents a valid tile inside the room.

        m: an integer
        n: an integer
        returns: True if (m, n) is cleaned, False otherwise
        """
        if self.tile[m][n] == 1:
            return True
        else:
            return False
    
    def getNumTiles(self):
        """
        Return the total number of tiles in the room.

        returns: an integer
        """
        return self.width * self.height

    def getNumCleanedTiles(self):
        """
        Return the total number of clean tiles in the room.

        returns: an integer
        """
        return sum([sum(i) for i in self.tile])

    def getRandomPosition(self):
        """
        Return a random position inside the room.

        returns: a Position object.
        """
        x = random.choice(range(self.width))
        y = random.choice(range(self.height))
        return Position(x, y)

    def isPositionInRoom(self, pos):
        """
        Return True if pos is inside the room.

        pos: a Position object. pos = [x, y]
        returns: True if pos is in the room, False otherwise.
        """
        #print "Checking Position..."
        #print self.tile[pos[0]][pos[1]]
        try:
            self.tile[pos[0]][pos[1]]
        except IndexError:
            return False

        return True


class Robot(object):
    """
    Represents a robot cleaning a particular room.

    At all times the robot has a particular position and direction in the room.
    The robot also has a fixed speed.

    Subclasses of Robot should provide movement strategies by implementing
    updatePositionAndClean(), which simulates a single time-step.
    """
    def __init__(self, room, speed):
        """
        Initializes a Robot with the given speed in the specified room. The
        robot initially has a random direction and a random position in the
        room. The robot cleans the tile it is on.

        room:  a RectangularRoom object.
        speed: a float (speed > 0)
        """
        self.d = int(random.random() * 360)
        self.room = room
        self.speed = speed
        self.position = room.getRandomPosition()
        

    def getRobotPosition(self):
        """
        Return the position of the robot.

        returns: a Position object giving the robot's position.
        """
        return self.position
    
    def getRobotDirection(self):
        """
        Return the direction of the robot.

        returns: an integer d giving the direction of the robot as an angle in
        degrees, 0 <= d < 360.
        """
        return self.d

    def setRobotPosition(self, position):
        """
        Set the position of the robot to POSITION.

        position: a Position object.
        """
        self.position = position

    def setRobotDirection(self, direction):
        """
        Set the direction of the robot to DIRECTION.

        direction: integer representing an angle in degrees
        """
        self.d = direction


    def updatePositionAndClean(self):
        """
        Simulate the raise passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        self.setRobotPosition(self.position)
        x = self.position.getX()
        y = self.position.getY()
        #print "Robot UPAC", [x, y]
        self.room.cleanTileAtPosition([x, y])
       
# === Problem 2
class StandardRobot(Robot):
    """
    A StandardRobot is a Robot with the standard movement strategy.

    At each time-step, a StandardRobot attempts to move in its current direction; when
    it hits a wall, it chooses a new direction randomly.
    """
    def updatePositionAndClean(self):
        """
        Simulate the passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        print self.d
        self.setRobotDirection(int(random.random() * 360))
        print self.d
        self.position = self.position.getNewPosition(self.d, self.speed)
        x = self.position.getX()
        y = self.position.getY()
        #print "after", [x, y]
        while not self.room.isPositionInRoom([x, y]):
            #print "Changing position..."
            self.setRobotDirection(int(random.random() * 360))
            #print self.d
            self.position = self.position.getNewPosition(self.d, self.speed)
            x = self.position.getX()
            y = self.position.getY()
            #print "new", [x, y]
        Robot.updatePositionAndClean(self)
            
        

##room = RectangularRoom(3, 3)
##st_robot = StandardRobot(room, 2.0)
##x = st_robot.position.getX()
##y = st_robot.position.getY()
##st_robot.updatePositionAndClean()
##x = st_robot.position.getX()
##y = st_robot.position.getY()

        
# === Problem 3

def runSimulation(num_robots, speed, width, height, min_coverage, num_trials,
                  robot_type):
    """
    Runs NUM_TRIALS trials of the simulation and returns the mean number of
    time-steps needed to clean the fraction MIN_COVERAGE of the room.

    The simulation is run with NUM_ROBOTS robots of type ROBOT_TYPE, each with
    speed SPEED, in a room of dimensions WIDTH x HEIGHT.

    num_robots: an int (num_robots > 0)
    speed: a float (speed > 0)
    width: an int (width > 0)
    height: an int (height > 0)
    min_coverage: a float (0 <= min_coverage <= 1.0)
    num_trials: an int (num_trials > 0)
    robot_type: class of robot to be instantiated (e.g. Robot or
                RandomWalkRobot)
    """
    room = RectangularRoom(width, height)
    robot = robot_type(room, speed)

    keep_going = 'y'
    while room.frac < 1 and (not keep_going == 'n'):
        #robot = robot_type(room, speed)
        robot.updatePositionAndClean()
        print room.getNumCleanedTiles(), (robot.position.getX(), robot.position.getY())
        #keep_going = raw_input('')
             
##        #std_robot = StandardRobot(room, speed)
##        robot.updatePositionAndClean()
##        clean_tiles = std_robot.room.getNumCleanedTiles()
##        tiles = std_robot.room.getNumTiles()
##        frac = clean_tiles/float(tiles)
       

    



runSimulation(1, 1.0, 3, 3, .5, 2, StandardRobot)
            

### === Problem 4
###
### 1) How long does it take to clean 80% of a 20×20 room with each of 1-10 robots?
###
### 2) How long does it take two robots to clean 80% of rooms with dimensions 
###	 20×20, 25×16, 40×10, 50×8, 80×5, and 100×4?
##
##def showPlot1():
##    """
##    Produces a plot showing dependence of cleaning time on number of robots.
##    """ 
##    raise NotImplementedError
##
##def showPlot2():
##    """
##    Produces a plot showing dependence of cleaning time on room shape.
##    """
##    raise NotImplementedError
##
### === Problem 5
##
##class RandomWalkRobot(Robot):
##    """
##    A RandomWalkRobot is a robot with the "random walk" movement strategy: it
##    chooses a new direction at random after each time-step.
##    """
##    raise NotImplementedError
##
##
### === Problem 6
##
### For the parameters tested below (cleaning 80% of a 20x20 square room),
### RandomWalkRobots take approximately twice as long to clean the same room as
### StandardRobots do.
##def showPlot3():
##    """
##    Produces a plot comparing the two robot strategies.
##    """
##    raise NotImplementedError
