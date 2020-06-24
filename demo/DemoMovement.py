# Component class
from Core.Component import Component

# Used for debugging messaged
from Core.Debug import Debug

# Input class
from Core.Input import Input

# Timing class
from Core.Time import Time

# 2 dimensional vectors
from Core.math.Vector2D import Vector2D

# We import the Transform component, which we'll use to move our player
from Core.components.Transform import Transform

# Used for key codes
import pygame


# Any component must inherit from Component
class DemoMovement(Component):
    # Init runs when the component is created
    def __init__(self, game_object):  # GameObject is required
        Component.__init__(self, game_object)

        # Transform we will move to move our player
        # We still don't get the Transform because it might not be initiated
        self.transform = None

        # Input is a singleton, any instance will be the same as the others and will share the same memory
        self.input_manager = Input()

        # Units we will move per second
        self.move_speed = 200

    # Start when all components and game objects have been created
    # In start we setup the required "connections" with other components or game objects
    def start(self):

        # To move the player we need a Transform component
        # We can get it using the GameObject.get_component method
        self.transform = self.game_object.get_component(Transform)

        # The GameObject.get_component method returns None if the component wasn't found, so we can check that
        if not self.transform:
            # If the Transform component wasn't found, we'll debug an error and disable this component
            # The first parameter is the message
            # The second parameter is the origin, which we'll put self
            # Note: The origin can be a Component object or a string. If the origin is a Component,
            # the Debug class will format it so that it contains the game object name and the component
            # were the log came from
            Debug.log_error("Transform component not found, disabling", self)

            # We disable this component so that it isn't run
            self.enabled = False

        # We debug that start is complete
        Debug.log("Start complete", self)

    # Update is called on every frame
    def update(self):
        # This demo movement will move the player using WASD, without ever rotating nor scaling the object.

        # We create an empty movement vector, which will be the vector we will move towards after taking player input
        movement_vector = Vector2D(0, 0)

        # We check if we have W pressed
        # Up movement means subtracting from the y direction
        if self.input_manager.get_key(pygame.K_w):
            movement_vector.y -= 1

        # We check if we have A pressed
        # Left movement means subtracting from the x direction
        if self.input_manager.get_key(pygame.K_a):
            movement_vector.x -= 1

        # We check if we have S pressed
        # Down movement means adding to the y direction
        if self.input_manager.get_key(pygame.K_s):
            movement_vector.y += 1

        # We check if we have D pressed
        # Right movement means adding from the x direction
        if self.input_manager.get_key(pygame.K_d):
            movement_vector.x += 1

        # The movement vector right now would be larger if we went in a straight line
        # than if we went in a diagonal
        # Going in a straight line (directly upwards, for example) would result of a length of 1.
        # However going diagonally would result in a length of sqrt(1^2 + 1^2) because of the
        # pythagorean theorem
        # We fix this by normalizing the vector. This way it ends up being an unit vector.
        movement_vector.normalize()

        # Now we will multiply the movement vector by the speed we had to make the length of out unit vector the
        # same as the length we want, our speed.
        movement_vector *= self.move_speed

        # Frame rate can vary depending on the number of components and game objects in the scene,
        # so we cannot assume the timing between frames will be constant
        # The Time.delta_time method returns the time passed from the previous frame to the current one, this way,
        # regardless of the frame rate, we will move at the same speed per second
        # To use Time.delta_time we multiply the movement_vector by Time.delta_time
        movement_vector *= Time.delta_time()

        # To end the movement, we add the movement_vector to our current local position
        self.transform.position = self.transform.position + movement_vector

