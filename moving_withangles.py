import pygame
import random
import math

background_colour = (255,255,255)
(width, height) = (1080 , 500)

clock = pygame.time.Clock()

drag = 0.999
elasticity = 0.75
gravity = (math.pi, 0.002)

def addVectors((angle1, length1), (angle2, length2)):
    x  = math.sin(angle1) * length1 + math.sin(angle2) * length2
    y  = math.cos(angle1) * length1 + math.cos(angle2) * length2
    
    angle = 0.5 * math.pi - math.atan2(y, x)
    length  = math.hypot(x, y)

    return (angle, length)

class Particle():
    def __init__(self, (x, y), size):
        self.x = x
        self.y = y
        self.size = size
        self.colour = (0, 0, 255)
        self.thickness = 1
        self.speed = 0
        self.angle = 0

    def display(self):
        pygame.draw.circle(screen, self.colour, (int(self.x), int(self.y)), self.size, self.thickness)

    def move(self):
        (self.angle, self.speed) = addVectors((self.angle, self.speed), gravity)

        self.x += math.sin(self.angle) * self.speed
        self.y -= math.cos(self.angle) * self.speed
        self.speed *= drag

    def bounce(self):
        if self.x > width - self.size:
            self.x = 2*(width - self.size) - self.x
            self.angle = - self.angle
            self.speed *= elasticity

        elif self.x < self.size:
            self.x = 2*self.size - self.x
            self.angle = - self.angle
            self.speed *= elasticity

        if self.y > height - self.size:
            self.y = 2*(height - self.size) - self.y
            self.angle = math.pi - self.angle
            self.speed *= elasticity

        elif self.y < self.size:
            self.y = 2*self.size - self.y
            self.angle = math.pi - self.angle
            self.speed *= elasticity

    def in_view(self, screen_x, screen_y):
        if self.x > screen_x:
            return False
        elif self.y > screen_y:
            return False
        else:
            return True

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Tutorial 4')

number_of_particles = 10
my_particles = []

def generate():
    
    size = random.randint(10, 20)
    x = random.randint(size, width-size)
    y = random.randint(size, height-size)
    pygame.mouse.get_pos()
    # particle = Particle((x, y), size)
    particle = Particle((pygame.mouse.get_pos()), size)
    particle.speed = random.randint(1,10) * .25
    particle.angle = random.uniform(0, math.pi*2)
    particle.angle = 45

    return particle
        # my_particles.append(particle)

def launch(power):
    particle = Particle((pygame.mouse.get_pos()), 20)
    particle.speed = 5 * power
    particle.angle = 45

    return particle

running = True
channelpower = False
power = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # if event.type == pygame.MOUSEMOTION:
        #         my_particles.append(generate())


        if event.type == pygame.MOUSEBUTTONDOWN:
            (mouseX, mouseY) = pygame.mouse.get_pos()
            print mouseX, mouseY
            print pygame.mouse.get_pressed()

            if pygame.mouse.get_pressed()[0] == 1:
                channelpower = True                

            if pygame.mouse.get_pressed()[2] == 1:
                my_particles.append(launch(power))
                power = 0

    if pygame.mouse.get_pressed()[0] != 1:
        channelpower = False
    if channelpower:
        power += .01
        print power

    screen.fill(background_colour)

    saved = []
    for particle in my_particles[:]:
        particle.move()
        particle.bounce()
        particle.display()
        if particle.in_view(width,height):
            saved.append(particle)

    my_particles = saved

    # print len(my_particles)
    # print addVectors((100,5),(20,5))


    clock.tick(200)
    pygame.display.flip()