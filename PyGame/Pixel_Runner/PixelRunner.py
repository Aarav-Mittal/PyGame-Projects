import pygame
from sys import exit
from random import randint,choice

class Player(pygame.sprite.Sprite):
    def __init__(self) :
        super().__init__()
        player_walk_1 = pygame.image.load("Pixel_Runner/Graphics/Player/player_walk_1.png").convert_alpha()
        player_walk_2 = pygame.image.load("Pixel_Runner/Graphics/Player/player_walk_2.png").convert_alpha()
        self.player_walk = [player_walk_1,player_walk_2]
        self.player_index = 0
        self.player_jump = pygame.image.load("Pixel_Runner/Graphics/Player/jump.png").convert_alpha()
        
        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (80,300))
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound('Pixel_Runner/audio/jump.mp3')
        self.jump_sound.set_volume(0.2)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
            self.jump_sound.play()

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def animation_state(self):
        if self.rect.bottom<300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()
        #return super().update()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self,type):
        super().__init__()
        if type == 'fly':
            fly_1 = pygame.image.load('Pixel_Runner/Graphics/Fly/Fly1.png').convert_alpha()
            fly_2 = pygame.image.load('Pixel_Runner/Graphics/Fly/Fly2.png').convert_alpha()
            self.frames = [fly_1,fly_2]
            y_pos = 210
        else:
            snail_1 = pygame.image.load('Pixel_Runner/Graphics/snail/snail1.png').convert_alpha()
            snail_2 = pygame.image.load('Pixel_Runner/Graphics/snail/snail2.png').convert_alpha()
            self.frames = [snail_1,snail_2]
            y_pos = 300

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (randint(900,1100),y_pos))

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation_state()
        if final_score <= 30:
            self.rect.x -= 5
        elif final_score <= 60:
            self.rect.x -= 7
        else:
            self.rect.x -= 10

        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

def score():
    time = (pygame.time.get_ticks() - start_time)//1000
    score_surface = test_font.render(f'Score: {time}',False,(64,64,64))
    score_rectangle = score_surface.get_rect(center = (400,50))
    screen.blit(score_surface,score_rectangle)
    return time

def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite,obstacle_group,False):
        obstacle_group.empty()
        return False
    else:
        return True

pygame.init()   # very important as it starts pygame
screen = pygame.display.set_mode((800,400)) # brackets contains width and hight of the dispaly widow
pygame.display.set_caption('Pixel Runner')  # sets a title for display window
clock = pygame.time.Clock()
test_font = pygame.font.Font("Pixel_Runner/font/Pixeltype.ttf",50)  # creates a font. takes 2 arguments, font type and size
game_active = False
start_time = 0
final_score = 0
all_scores = []

bg_music = pygame.mixer.Sound('Pixel_Runner/audio/music.wav')
bg_music.set_volume(0.5)
bg_music.play(loops=-1)

player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

# making a solid color surface
'''test_surface1 = pygame.Surface((100,200))
test_surface1.fill('Red')
'''
# making a image surface
Sky_surface = pygame.image.load('Pixel_Runner/Graphics/sky2.png').convert_alpha()   # convert_alpha() converts the file type to a type that pygame easily understands.
Sky_surface_rect = Sky_surface.get_rect(topleft = (0,0))
ground_surface = pygame.image.load('Pixel_Runner/Graphics/ground.png').convert_alpha()
ground_surface_rect = ground_surface.get_rect(topleft = (0,300))

# rectangles
player_stand = pygame.image.load('Pixel_Runner/Graphics/Player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand,0,2)
player_stand_rectangle = player_stand.get_rect(center=(400,200))

# creating text surface
line1 = test_font.render('Pixel Runner',False,(111,196,169))
line1_rectangle = line1.get_rect(center=(400,80))
line2 = test_font.render("Game Over",False,(111,196,169))
line2_rectangle = line2.get_rect(center = (400,80))

game_message = test_font.render("Press space to run",False,(111,196,169))
game_message_rectangle = game_message.get_rect(center = (400,330))

# Timers
obstacle_timer = pygame.USEREVENT+1
pygame.time.set_timer(obstacle_timer,1500)

'''snail_animation_timer = pygame.USEREVENT+2
pygame.time.set_timer(snail_animation_timer,500)

fly_animation_timer = pygame.USEREVENT+3
pygame.time.set_timer(fly_animation_timer,200)'''

while True:
    """This while loops makes sure that the display window is displayed on the screen countinously and 
    in this loop, 
    1) we will draw all our elements
    2) update everything
    """
    for event in pygame.event.get():   # this loop checks all possible player inputs that are happening at the moment
        if event.type == pygame.QUIT:
            pygame.quit()  # closes the display window
            exit()
        
        if game_active:
            '''if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rectangle.bottom >= 300:
                    player_gravity = -20'''
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(['fly','snail','snail','snail'])))
            '''if event.type == snail_animation_timer:
                if snail_index == 0:
                    snail_index = 1
                else:
                    snail_index=0
                snail_surface = snail_frame[snail_index]
            if event.type == fly_animation_timer:
                if fly_index == 0:
                    fly_index = 1
                else:
                    fly_index=0
                fly_surface = fly_frame[fly_index]
'''

        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_active=True 
                    start_time = pygame.time.get_ticks()
                
    if game_active:
        # origin(0,0) is at top left corner of the window unlike the bottom left is cartesian plane
        # blit is short for block image transfer and it puts one surface on top of another. "screen.blit" takes two arguments... 1st is the surface to be placed and second is its position
        screen.blit(Sky_surface,Sky_surface_rect)
        screen.blit(ground_surface,ground_surface_rect)
        final_score = score()
        
        '''        
        pygame.draw.rect(screen,'#c0e8ec',score_rectangle)  # draws a rectangle. we can draw any shape like a line or circle(elipse),etc
        pygame.draw.rect(screen,'#c0e8ec',score_rectangle,10)
        screen.blit(score_surface,score_rectangle)
        '''

        player.draw(screen)
        player.update()

        obstacle_group.draw(screen)
        obstacle_group.update()
        
        game_active = collision_sprite()

    else:
        screen.fill((94,129,210))
        screen.blit(player_stand,player_stand_rectangle)

        all_scores.append(int(final_score))
        highest_score = max(all_scores)
        highest_score_message = test_font.render(f'Highest Score: {highest_score}',False,(111,196,169))
        highest_score_message_rect = highest_score_message.get_rect(center = (400,370))

        score_message = test_font.render(f"Your Score: {final_score}",False,(111,196,169))
        score_message_rectangle = score_message.get_rect(center=(400,330)) 
        
        if final_score == 0:
            screen.blit(line1,line1_rectangle)
            screen.blit(game_message,game_message_rectangle)
        else:
            screen.blit(line2,line2_rectangle)
            screen.blit(score_message,score_message_rectangle)
            screen.blit(highest_score_message,highest_score_message_rect)


    
    
    pygame.display.update() # this line updates the display window
    clock.tick(60)     #  sets maximum framerate 
