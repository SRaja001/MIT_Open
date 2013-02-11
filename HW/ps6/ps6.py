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
        #print "Position", [new_x, new_y]
        #k = raw_input("")
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
        self.tile[int(pos[1])][int(pos[0])] = 1
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
        if self.tile[n][m] == 1:
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
            self.tile[int(pos[1])][int(pos[0])]
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
        self.position = self.room.getRandomPosition()
        

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
##        self.setRobotPosition(self.position)
##        x = self.position.getX()
##        y = self.position.getY()
##        #print "Robot UPAC", [x, y]
##        self.room.cleanTileAtPosition([x, y])
##       
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
        candidatePosition = self.position.getNewPosition(self.d, self.speed)
        if self.room.isPositionInRoom(candidatePosition):
            self.setRobotPosition(candidatePosition)
            self.room.cleanTileAtPosition(self.position)
        else:
            self.direction = random.randrange(360)
##        #print self.d
##        self.setRobotDirection(int(random.random() * 360))
##        #print self.d
##        self.position = self.position.getNewPosition(self.d, self.speed)
##        x = self.position.getX()
##        y = self.position.getY()
##        #print "after", [x * y]
##        while not self.room.isPositionInRoom([x, y]):
##            #print "Changing position..."
##            self.setRobotDirection(int(random.random() * 360))
##            #print self.d
##            old_position = self.position
##            self.position = self.position.getNewPosition(self.d, self.speed)
##            old_pos_dis = math.sqrt((old_position.getX()**2) + (old_position.getY()**2))
##            new_pos_dis = math.sqrt((self.position.getX()**2) + (self.position.getY()**2))
##            if new_pos_dis > old_pos_dis:
##                self.position = old_position
##            
##            x = self.position.getX()
##            y = self.position.getY()
##            #print "new", [x, y]
##        Robot.updatePositionAndClean(self)
            
        

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
    avg = 0
    for i in range(num_trials):
        #print "trial",i,"..."
        anim = ps6_visualize.RobotVisualization(num_robots, width, height) 
        room = RectangularRoom(width, height)
        robots = [robot_type(room, speed) for _ in range(num_robots)]
        steps = 0
        while room.frac < min_coverage :
            #robot = robot_type(room, speed)
            for robot in robots: 
                robot.updatePositionAndClean()
                #print (robot.position.getX(), robot.position.getY())
                #keep_going = raw_input('')
                if room.frac >= min_coverage:
                    break
                steps += 1
                anim.update(room, robots)
                #print steps
        #print "steps", steps
        avg += steps
        anim.done()
    #print avg
    avg = avg/float(num_trials)
            

    return avg
             
##        #std_robot = StandardRobot(room, speed)
##        robot.updatePositionAndClean()
##        clean_tiles = std_robot.room.getNumCleanedTiles()
##        tiles = std_robot.room.getNumTiles()
##        frac = clean_tiles/float(tiles)
       

    



runSimulation(1, 2.0, 5, 5, 1, 1, StandardRobot)
            

# === Problem 4
#
# 1) How long does it take to clean 80% of a 20×20 room with each of 1-10 robots?
#
# 2) How long does it take two robots to clean 80% of rooms with dimensions 
#	 20×20, 25×16, 40×10, 50×8, 80×5, and 100×4?

def showPlot1():
    """
    Produces a plot showing dependence of cleaning time on number of robots.
    """
    avg = []
    for i in range(1,11):
        avg.append(runSimulation(i, 1.0, 20, 20, .8, 100, StandardRobot))

    print avg
    pylab.figure(1)
    pylab.plot(range(1,11), avg)
    pylab.title('Cleaning 80% of 20x20 Room, Speed = 1.0')
    pylab.xlabel('Robots')
    pylab.ylabel('Time (s)')
    pylab.show()
    
#showPlot1()

def showPlot2():
    """
    Produces a plot showing dependence of cleaning time on room shape.
    """
    rooms = ((20, 20), (25, 16), (40, 10), (50, 8), (80, 5), (100, 4))
    avg = []
    for dim in rooms:
        print "current dim", dim
        avg.append(runSimulation(2, 1.0, dim[0], dim[1], .8, 2, StandardRobot))
        print avg
    pylab.figure(1)
    pylab.plot(avg)
    pylab.title('Cleaning 80% of 20x20 Room, Speed = 1.0')
    #pylab.xlabel('Robots')
    pylab.ylabel('Time (s)')
    pylab.show()
    
    
#showPlot2()
# === Problem 5

class RandomWalkRobot(Robot):
    """
    A RandomWalkRobot is a robot with the "random walk" movement strategy: it
    chooses a new direction at random after each time-step.
    """
    def updatePositionAndClean(self):
        d = self.getRobotDirection()
        x = self.position.getX()
        y = self.position.getY()
        print "before change", [x, y]
        old_position = self.position
        position = self.position.getNewPosition(self.d, self.speed)
        self.setRobotPosition(position)
        x = self.position.getX()
        y = self.position.getY()
        print "New position without changing direction", [x, y]
        while ((not self.room.isPositionInRoom([x, y])) or (x * y < 0)):
            #print (x * y < 0)
            print "Changing direction"
            old_position = self.position
            self.setRobotDirection(int(random.random() * 360))
            old_pos_dis = math.sqrt((old_position.getX()**2) + (old_position.getY()**2))
            new_pos_dis = math.sqrt((self.position.getX()**2) + (self.position.getY()**2))
            if new_pos_dis > old_pos_dis:
                position = old_position
                print "Old Positino was better"
            position = self.position.getNewPosition(self.getRobotDirection(), self.speed)
            self.setRobotPosition(position)
            x = self.position.getX()
            y = self.position.getY()
            print "Trying", [x, y]
        Robot.updatePositionAndClean(self)
        position = self.getRobotPosition()
        x = self.position.getX()
        y = self.position.getY()
        print
        print "After set", [x, y]
               
#runSimulation(1, 2.0, 5, 5, 1, 1, RandomWalkRobot)
# === Problem 6

# For the parameters tested below (cleaning 80% of a 20x20 square room),
# RandomWalkRobots take approximately twice as long to clean the same room as
# StandardRobots do.
def showPlot3():
    """
    Produces a plot comparing the two robot strategies.
    """
    raise NotImplementedError
