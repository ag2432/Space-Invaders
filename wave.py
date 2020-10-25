"""
Subcontroller module for Alien Invaders

This module contains the subcontroller to manage a single level or wave in
the Alien Invaders game.  Instances of Wave represent a single wave. Whenever
you move to a new level, you are expected to make a new instance of the class.

The subcontroller Wave manages the ship, the aliens and any laser bolts on
screen. These are model objects.  Their classes are defined in models.py.

Most of your work on this assignment will be in either this module or
models.py. Whether a helper method belongs in this module or models.py is
often a complicated issue.  If you do not know, ask on Piazza and we will
answer.

# YOUR NAME(S) AND NETID(S) HERE
# DATE COMPLETED HERE
"""
from game2d import *
from consts import *
from models import *
from Sounds import *
import random

# PRIMARY RULE: Wave can only access attributes in models.py via getters/setters
# Wave is NOT allowed to access anything in app.py (Subcontrollers are not
# permitted to access anything in their parent. To see why, take CS 3152)


class Wave(object):
    """
    This class controls a single level or wave of Alien Invaders.

    This subcontroller has a reference to the ship, aliens, and any laser bolts
    on screen. It animates the laser bolts, removing any aliens as necessary.
    It also marches the aliens back and forth across the screen until they are
    all destroyed or they reach the defense line (at which point the player
    loses). When the wave is complete, you  should create a NEW instance of
    Wave (in Invaders) if you want to make a new wave of aliens.

    If you want to pause the game, tell this controller to draw, but do not
    update.  See subcontrollers.py from Lecture 24 for an example.  This
    class will be similar to than one in how it interacts with the main class
    Invaders.

    All of the attributes of this class ar to be hidden. You may find that
    you want to access an attribute in class Invaders. It is okay if you do,
    but you MAY NOT ACCESS THE ATTRIBUTES DIRECTLY. You must use a getter
    and/or setter for any attribute that you need to access in Invaders.
    Only add the getters and setters that you need for Invaders. You can keep
    everything else hidden.

    """
    # HIDDEN ATTRIBUTES:
    # Attribute _ship: the player ship to control
    # Invariant: _ship is a Ship object or None
    #
    # Attribute _aliens: the 2d list of aliens in the wave
    # Invariant: _aliens is a rectangular 2d list containing Alien objects or None
    #
    # Attribute _bolts: the laser bolts currently on screen
    # Invariant: _bolts is a list of Bolt objects, possibly empty
    #
    # Attribute _dline: the defensive line being protected
    # Invariant : _dline is a GPath object
    #
    # Attribute _lives: the number of lives left
    # Invariant: _lives is an int >= 0
    #
    # Attribute _time: the amount of time since the last Alien "step"
    # Invariant: _time is a float >= 0s
    #
    # Atrribute _aliendirection: the direction that the alien is moving
    # Invariant: _aliendirection must be string right or left
    #
    # LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    #
    # Attribute _stepstilfire: the number of steps Aliens will take before they next fire
    # Invariant: _stepstilfire is an int between 1 and BOLT_RATE inclusive
    #
    # Attribute _stepssincefire: the number of Alien steps since they last fired
    # Invariant: _stepssincefire is an int >= 0
    #
    # Attribute _aliensalive: the number of Aliens visible on the screen
    #Invariant: _aliensalive is an an int >= 0
    #
    # Attribute _aliencollisionSound: the sound that is made when the alien
    # collides with one of the ship bolts.
    #Invariant: It is a sound object.
    #
    # Attribute _alienfireSound: the sound that is made when the alien bolt is
    #fired
    #Invariant: It is a sound object.
    #
    # Attribute _shipfireSound: the sound that is made when the ship bolt is
    # fired
    #Invariant: It is a sound object.
    #
    # Attribute _shipcollisionSound: the sound that is made when ship object
    # collides  with one of the alien bolts.
    # Invariant: It is a sound object.

    # You may change any attribute above, as long as you update the invariant
    # You may also add any new attributes as long as you document them.

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getcolumn(self):
        """
        RETURNS the column that exists.

        It calls the helper method random_column_number to get a random column,
        checks to see if it exists and returns only if the column exists.
        """
        i= self.random_column_number()
        if self._aliensalive != 0:
            while self.does_column_exist(i) == False:
                i= self.random_column_number()
        return i

    def getNumaliensalive(self):
        """
        Getter that RETURNS the number of aliens that are visible on the screen.
        """
        return self._aliensalive

    def getLives(self):
        """
        Getter that RETURNS the number of lives that the player has left.

        """
        return self._lives

    def getShip(self):
        """
        Getter that RETURNS the ship object.

        """
        return self._ship

    def setShip(self):
        """
        Setter that creates a new ship object.

        """
        self._ship = Ship()

    def getAlienfireSound(self):
        """
        getter that RETURNS the whether the volume attribute is 1 or 0
        """
        return self._alienfireSound.volume

    def setAlienfireSound(self,value):
        """
        Setter that sets the volume attribute to 0 or 1 according to the
        userinput
        """
        self._alienfireSound.volume= value

    def getAliencollisionSound(self):
        """
        getter that RETURNS the whether the volume attribute is 1 or 0
        """
        return self._aliencollisionSound.volume

    def setAliencollisionSound(self,value):
        """
        Setter that sets the volume attribute to 0 or 1 according to the
        userinput
        """
        self._aliencollisionSound.volume= value

    def getShipfireSound(self):
        """
        getter that RETURNS the whether the volume attribute is 1 or 0
        """
        return self._shipfireSound.volume

    def setShipfireSound(self,value):
        """
        Setter that sets the volume attribute to 0 or 1 according to the
        userinput
        """
        self._shipfireSound.volume= value

    def getShipcollisionSound(self):
        """
        getter that RETURNS the whether the volume attribute is 1 or 0
        """
        return self._shipcollisionSound.volume

    def setShipcollisionSound(self,value):
        """
        Setter that sets the volume attribute to 0 or 1 according to the
        userinput
        """
        self._shipcollisionSound.volume= value

    # INITIALIZER (standard form) TO CREATE SHIP AND ALIENS
    def __init__(self):
        """
        Initializes the application.
        """
        self._ship = Ship()
        self._bolts = []
        self._dline = GPath(points=[0,DEFENSE_LINE,GAME_WIDTH,DEFENSE_LINE],\
        linewidth=2, linecolor='black')
        self._lives= 3
        self._time = 0
        self._aliendirection = 'right'
        self._stepstilfire = random.randint(1,BOLT_RATE)
        self._stepssincefire = 0
        self._aliens = self.inithelper()
        self._aliensalive = ALIEN_ROWS * ALIENS_IN_ROW
        self._alienfireSound= Sound('pew1.wav')
        self._aliencollisionSound= Sound('blast2.wav')
        self._shipfireSound= Sound('pew2.wav')
        self._shipcollisionSound= Sound('blast1.wav')

    # UPDATE METHOD TO MOVE THE SHIP, ALIENS, AND LASER BOLTS
    def update(self, dt, userinput):
        """
        Animates a single frame in the game.

        It is in charge of playing the game.

        It is responsible for taking userinput and moving the ship or making it
        fire bolts according to the userinput.

        It is responsible for making the alien waves move and to remove the
        ship or aliens from the screen if there is any bolt collisions.

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)

        Parameter Userinput: It takes input from the user.
        Precondition: 'right', 'left' or 'up'
        """
        if self._ship is not None:
            if userinput.is_key_down('left') and \
            (self._ship.x - (SHIP_WIDTH/2))> 0:
                self._ship.x = self._ship.x - SHIP_MOVEMENT
            # moves ship right while user holds right key
            if userinput.is_key_down('right') and (self._ship.x + \
            (SHIP_WIDTH/2) < GAME_WIDTH):
                self._ship.x = self._ship.x + SHIP_MOVEMENT
            # update time increases during each frame
            self._time = self._time + dt
            self.movealiens()
        self.bolt_collisions()
        # fires a ship bolt if there is not one on screen
        if userinput.is_key_down('up') and self.is_ship_bolt() == False:
            self._shipfireSound.play()
            self._bolts.append(Bolt(self._ship.x, self._ship.y + \
            SHIP_HEIGHT/2 + BOLT_HEIGHT/2, BOLT_SPEED, bolttype = 'ship'))
        self.movebolts()
        self.deletebolt()
        # fires an alien bolt of there is not one and correct steps have passed
        if self.alien_bolt_on_the_screen() == False \
        and self._stepssincefire >= self._stepstilfire:
            self.makingalienbolts()
        self.losealife()
        self.aliensatdline()

    # DRAW METHOD TO DRAW THE SHIP, ALIENS, DEFENSIVE LINE AND BOLTS
    def draw(self, view):
        """
        Draws the game objects to the view.

        Every single thing you want to draw in this game is a GObject.  To
        draw a GObject g, simply use the method g.draw(self.view).  It is
        that easy!

        Many of the GObjects (such as the ships, aliens, and bolts) are
        attributes in Wave. In order to draw them, you either need to add
        getters for these attributes or you need to add a draw method to
        class Wave.  We suggest the latter.  See the example subcontroller.py
        from class.
        """
        for i in self._aliens:
            for alien in i:
                if alien is not None:
                    alien.draw(view)

        if self._ship is not None:
            self._ship.draw(view)

        if len(self._bolts) != 0:
            for bolts in self._bolts:
                bolts.draw(view)

        self._dline.draw(view)

    # HELPER METHODS
    def inithelper(self):
        """
        Helper method that initializes the new alien wave.
        """
        list = []
        b = GAME_HEIGHT - (ALIEN_CEILING + ALIEN_HEIGHT/2)
        imagenumber = 0

        for row in range(ALIEN_ROWS):
            r = []
            a = ALIEN_H_SEP + (ALIEN_WIDTH/2)
            imagenumber = (ALIEN_ROWS - 1 - row)// 2 % len(ALIEN_IMAGES)

            for col in range(ALIENS_IN_ROW):
                r.append(Alien(x=a,y=b,source=ALIEN_IMAGES[imagenumber]))
                a = a + ALIEN_H_SEP + ALIEN_WIDTH
            b = b - (ALIEN_V_SEP + ALIEN_HEIGHT)
            list.append(r)
        return list

    def movealiens(self):
        """
        Moves the alien waves according to the direction.

        Moves the alien to the right if the direction is right and does not
        hit the rightmost wall.

        Moves the alien to the left if the direction is left and does not hit
        the leftmost wall.

        """
        # move the aliens down after they hit the right wall
        if self._aliendirection == 'right' and self.rightedge() == False and \
        self._time > ALIEN_SPEED:
            self.movedown()
            self.changedirection()
            self._stepssincefire = self._stepssincefire + 1

        # move the aliens down after they hit the left wall
        if self._aliendirection == 'left' and self.leftedge() == False and \
        self._time > ALIEN_SPEED:
            self.movedown()
            self.changedirection()
            self._stepssincefire = self._stepssincefire + 1

        self.movealright()
        self.movealleft()

    def movealright(self):
        """
        Moves the alien wave right before hitting rightmost wall.
        """
        if self._aliendirection == 'right' and self.rightedge() and \
        self._time > ALIEN_SPEED:
            for row in self._aliens:
                for alien in row:
                    if alien is not None:
                        alien.x = alien.x + ALIEN_H_WALK
            self._time = 0

            self._stepssincefire = self._stepssincefire + 1

    def movealleft(self):
        """
        Moves the alien wave left before hitting leftmost wall.
        """
        if self._aliendirection == 'left' and self.leftedge() and \
        self._time > ALIEN_SPEED:
            for row in self._aliens:
                for alien in row:
                    if alien is not None:
                        alien.x = alien.x - ALIEN_H_WALK
            self._time = 0
            self._stepssincefire = self._stepssincefire + 1

    def leftedge(self):
        """
        RETURNS True if Alien is not touching the left edge and False if
        Alien is touching the left edge.
        """
        return self.leftmostalienx() - (ALIEN_WIDTH/2) > ALIEN_H_SEP

    def rightedge(self):
        """
        RETURNS True if Alien is not touching the right edge and False if
        Alien is touching the right edge.
        """
        return GAME_WIDTH - ALIEN_H_SEP > self.rightmostalienx() + \
        (ALIEN_WIDTH/2)

    def rightmostalienx(self):
        """
        RETURNS the x-coordinate of the rightmost alien in the wave.
        """
        rightmostx = 0
        for row in self._aliens:
            for alien in row:
                if alien is not None:
                    if alien.x > rightmostx:
                        rightmostx = alien.x

        return rightmostx

    def leftmostalienx(self):
        """
        RETURNS the x-coordinate of the leftmost alien in the wave.
        """
        leftmostx = GAME_WIDTH
        for row in self._aliens:
            for alien in row:
                if alien is not None:
                    if alien.x < leftmostx:
                        leftmostx = alien.x
        return leftmostx

    def changedirection(self):
        """
        MODIFIES the aliendirection to be the opposite of the current
        aliendirection.
        """
        if self._aliendirection == 'right':
            self._aliendirection = 'left'
        else:
            self._aliendirection = 'right'

    def movedown(self):
        """
        Moves the aliens down one vertical distance.
        """
        for row in self._aliens:
            for alien in row:
                if alien is not None:
                    alien.y = alien.y - ALIEN_V_WALK
        self._time = 0

    def movebolts(self):
        """
        Moves the bolts with the velocity.

        If it is a ship bolt, the velocity is positive so method moves the
        bolts up.

        If it is a alien bolt, the velocity is negative so method moves the
        bolts down.
        """
        for bolt in self._bolts:
            bolt.y = bolt.y + bolt.getVelocity()

    def deletebolt(self):
        """
        Deletes a bolt from the list of bolts after it leaves the game screen.
        """
        for bolt in self._bolts:
            if bolt.getBolttype() == 'ship':
                if (bolt.y - (BOLT_HEIGHT/2)) > GAME_HEIGHT:
                    self._bolts.remove(bolt)
            else:
                if (bolt.y + (BOLT_HEIGHT/2)) < 0:
                    self._bolts.remove(bolt)

    def is_ship_bolt(self):
        """
        RETURNS True if there is a ship bolt on the screen, False otherwise.
        """
        if len(self._bolts) < 1:
            return False
        for bolt in self._bolts:
            if bolt.getBolttype() == 'ship':
                return True
        return False

    def alien_bolt_on_the_screen(self):
        """
        RETURNS True if there is an alien bolt on the screen, False otherwise.
        """
        if len(self._bolts) < 1:
            return False
        for bolt in self._bolts:
            if bolt.getBolttype() == 'alien':
                return True
        return False

    def makingalienbolts(self):
        """
        Creates an alien bolt and resets the steps since last alien bolt was
        fired to 0.
        """
        lowestalien= self.lowest_alien()
        xe= lowestalien.x
        ye= lowestalien.y - (ALIEN_HEIGHT/2)
        self._bolts.append(Bolt(xe, ye, -BOLT_SPEED, bolttype = 'alien'))
        self._stepssincefire = 0
        self._alienfireSound.play()

    def lowest_alien(self):
        """
        RETURNS the lowest alien in the selected column of aliens.
        """
        col= self.getcolumn()
        for row in range(len(self._aliens)):
            if self._aliens[row][col] is not None:
                lowest= self._aliens[row][col]
        return lowest

    def random_column_number(self):
        """
        RETURNS an int representing a random alien column number.
        """
        column = random.randint(0, ALIENS_IN_ROW - 1)
        return column

    # HELPER METHOD FOR COLLISION DETECTION
    def bolt_collisions(self):
        """
        Checks if the ship bolt is colliding with any aliens and changes
        the hit alien to None if it collides. Decreases number of aliens alive
        if the alien was hit.

        Checks if the alien bolt collides with the ship and changes the ship to
        None if there was a collision.

        Removes bolt if there was a collision.

        Plays corresponding colliding sounds if necessary.
        """
        for i in self._bolts:
            if self._ship is not None:
                if self._ship.collides(i):
                    self._bolts.remove(i)
                    self._ship= None
                    self._shipcollisionSound.play()

        for row in range(len(self._aliens)):
            for alien in range(len(self._aliens[row])):
                for i in self._bolts:
                    if self._aliens[row][alien] is not None:
                        if i._bolttype== 'ship':
                            if self._aliens[row][alien].collides(i):
                                self._aliens[row][alien] = None
                                self._bolts.remove(i)
                                self._aliensalive = self._aliensalive - 1
                                self._aliencollisionSound.play()

    def does_column_exist(self, value):
        """
        RETURNS True if the column exists and False if the column does not
        exist.
        """
        for row in range(len(self._aliens)):
            if self._aliens[row][value] is not None:
                return True
        return False

    def losealife(self):
        """
        Removes a player life when the ship is hit.
        """
        if self._ship is None:
            self._lives = self._lives - 1

    def aliensatdline(self):
        """
        RETURNS True if the lowest alien touches the defense line and RETURNS
        False otherwise.
        """
        if self._aliensalive != 0:
            if float(self.lowest_alien().y) <= DEFENSE_LINE + ALIEN_HEIGHT/2:
                return True
            else:
                return False
