"""
Sample Python/Pygame Programs
Simpson College Computer Science
http://programarcadegames.com/
http://simpson.edu/computer-science/
 
Explanation video: http://youtu.be/qbEEcQXw8aw
"""
 
import pygame
import random
import math 
 
# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
 
def get_distance(origin, destination):
    x = origin[0] - destination[0]
    y = origin[1] - destination[1]
    return math.sqrt(x*x + y*y)

def get_angle(origin, destination):
    """Returns angle in radians from origin to destination.
    This is the angle that you would get if the points were
    on a cartesian grid. Arguments of (0,0), (1, -1)
    return .25pi(45 deg) rather than 1.75pi(315 deg).
    """
    x_dist = destination[0] - origin[0]
    y_dist = destination[1] - origin[1]
    # print math.atan2(-y_dist, x_dist) % (2 * math.pi)
    return math.atan2(-y_dist, x_dist) % (2 * math.pi)

def project(pos, angle, distance):
    """Returns tuple of pos projected distance at angle
    adjusted for pygame's y-axis.
    """
    return (pos[0] + (math.cos(angle) * distance),
            pos[1] - (math.sin(angle) * distance))
class Block(pygame.sprite.Sprite):
    """
    This class represents the ball
    It derives from the "Sprite" class in Pygame
    """
    def __init__(self, color, width, height):
        """ Constructor. Pass in the color of the block,
        and its x and y position. """
        # Call the parent class (Sprite) constructor
        super(Block, self).__init__()
        self.image = pygame.image.load("Images/mine_enemy.png").convert()
        self.image.set_colorkey(WHITE)
 
        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        # self.image = pygame.Surface([width, height])
        # self.image.fill(color)
 
        # Fetch the rectangle object that has the dimensions of the image
        # image.
        # Update the position of this object by setting the values
        # of rect.x and rect.y
        self.rect = self.image.get_rect()
 
 
    def update(self):
        """ Called each frame. """
        # Do nothing
class Bullet(pygame.sprite.Sprite):

    def __init__(self, angle, origin):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Images/bullet.png").convert_alpha()

        self.rect = self.image.get_rect()
        self.rect.center = origin
        self.angle = angle        
        self.speed = 3


    def update(self):

        self.rect.x += math.sin(self.angle) * self.speed
        self.rect.y -= math.cos(self.angle) * self.speed


class Player(Block):
    """ The player class derives from Block, but overrides the 'update'
    functionality with new a movement function that will move the block
    with the mouse. """
    projectile_ammo = 3
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Images/player.png").convert_alpha()

        self.rect = self.image.get_rect()
    def has_ammo(self):
    	return self.projectile_ammo > 0

    def launch_projectile(self):
        self.projectile_ammo -= 1
        self.pos = pygame.mouse.get_pos()
        self.angle = get_angle((self.rect.x, self.rect.y), (self.pos[0], self.pos[1]))
        print math.degrees(self.angle)
        return Bullet(self.angle, self.rect.center)
    def update(self):
        # Get the current mouse position. This returns the position
        # as a list of two numbers.
        pass
        # Fetch the x and y out of the list,
        # just like we'd fetch letters out of a string.
        # Set the player object to the mouse location
        # self.rect.x = pos[0]
        # self.rect.y = pos[1]
 
# Initialize Pygame
pygame.init()
 
# Set the height and width of the screen
screen_width = 700
screen_height = 400
screen = pygame.display.set_mode([screen_width, screen_height])
 
# This is a list of 'sprites.' Each block in the program is
# added to this list. The list is managed by a class called 'Group.'
block_list = pygame.sprite.Group()
bullet_list = pygame.sprite.Group()
blocks_hit_list = pygame.sprite.Group() 
# This is a list of every sprite. All blocks and the player block as well.
all_sprites_list = pygame.sprite.Group()
 
for i in range(50):
    # This represents a block
    block = Block(BLACK, 20, 15)
 
    # Set a random location for the block
    block.rect.x = random.randrange(screen_width)
    block.rect.y = random.randrange(screen_height)
 
    # Add the block to the list of objects
    block_list.add(block)
    all_sprites_list.add(block)
 
# Create a red player block
player = Player()
all_sprites_list.add(player)
player.rect.center = (50,screen_height)
# Loop until the user clicks the close button.
done = False
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()
 
score = 0
 
# -------- Main Program Loop -----------
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
               
                    # Spawn player bullet
                if player.has_ammo():
	                bullet = player.launch_projectile()

	                # Make bullet visible by adding it into sprite lists
	                all_sprites_list.add(bullet)
	                bullet_list.add(bullet)                
    # Clear the screen
    screen.fill(WHITE)
 
    # Calls update() method on every sprite in the list
    all_sprites_list.update()
 
    # See if the player block has collided with anything.


    for bullet in bullet_list:
        blocks_hit_list = pygame.sprite.spritecollide(bullet, block_list, True)

    # # Check the list of collisions.
    for block in blocks_hit_list:
        score += 1
        print(score)
 
 
    # Draw all the spites
    all_sprites_list.draw(screen)
 
    # Limit to 20 frames per second
    clock.tick(20)
 
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
 
pygame.quit()