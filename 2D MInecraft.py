import sys

import math
import pygame

pygame.init()

clock = pygame.time.Clock()
fps = 60

# Set screen width and height and name.
screen_width = 1000
screen_height = 1000

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('2D Minecraft')

# Define game variables
tile_size = 50
game_over = 0
main_menu = True
timer = 0

# Set player health and hunger
player_health = 10.5
player_hunger = 10
#player_health_list = [2, 2, 2, 2, 2, 2, 2, 2, 2, 2]


# Load images.
#sun_img = pygame.image.load('img/sun.png')
bg_img = pygame.image.load('img/bg_sky.png')
grass_img = pygame.image.load('img/grass_block.png') # Grass Block
stone_img = pygame.image.load('img/stone_block.png') # Stone Block
coal_ore_img = pygame.image.load('img/coal_ore_block.png') # Coal Ore Block
restart_img = pygame.image.load('img/restart_btn.png')
start_img = pygame.image.load('img/start_btn.png')
exit_img = pygame.image.load('img/exit_btn.png')
health_full_img = pygame.image.load('img/full_heart.png')  # Full heart health
health_half_img = pygame.image.load('img/half_heart.png')  # Half heart health
health_empty_img = pygame.image.load('img/empty_heart.png')  # Empty heart health
hunger_full_img = pygame.image.load('img/full_hunger.png')  # Full hunger
hunger_half_img = pygame.image.load('img/half_hunger.png')  # Half hunger
hunger_empty_img = pygame.image.load('img/empty_hunger.png')  # Empty hunger

# Scale images as needed by replacing image name with new scaled image.
health_full_img = pygame.transform.scale(health_full_img, (20, 20))  # Full health bar scaled down
health_half_img = pygame.transform.scale(health_half_img, (20, 20))  # Half health bar scaled down
health_empty_img = pygame.transform.scale(health_empty_img, (20, 20))  # Empty health bar scaled down
hunger_full_img = pygame.transform.scale(hunger_full_img, (20, 20))  # Full hunger bar scaled down
hunger_half_img = pygame.transform.scale(hunger_half_img, (20, 20))  # Half hunger bar scaled down
hunger_empty_img = pygame.transform.scale(hunger_empty_img, (20, 20))  # Empty hunger bar scaled down




class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False


    def draw(self):
        action = False

        # Get mouse position
        pos = pygame.mouse.get_pos()

        # Check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        # Draw button
        screen.blit(self.image, self.rect)

        return action


class Player():

    def __init__(self, x, y):
        self.reset(x, y)

    def update(self, player_health):
        dx = 0
        dy = 0
        # Character walk speed
        walk_cooldown = 10

        if game_over == 0:

            # Get key presses
            key = pygame.key.get_pressed()
            if (key[pygame.K_SPACE] or key[pygame.K_w] or key[pygame.K_UP]) and self.jumped == False and self.in_air == False:
                self.vel_y = -15  # Negative moves player up
                self.jumped = True
            if key[pygame.K_SPACE] or key[pygame.K_w] or key[pygame.K_UP] == False:
                self.jumped = False
            if key[pygame.K_LEFT] or key[pygame.K_a]:
                dx -= 5
                self.counter += 1
                self.direction = -1
            if key[pygame.K_RIGHT] or key[pygame.K_d]:
                dx += 5
                self.counter += 1
                self.direction = 1
            # Closes the program
            if key[pygame.K_ESCAPE]:
                sys.exit()
            if ((key[pygame.K_LEFT] or key[pygame.K_a]) == False) and (key[pygame.K_RIGHT] or key[pygame.K_d]) == False:
                self.counter = 0
                self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                if self.direction == -1:
                    self.image = self.images_left[self.index]
            # Handle animation
            if self.counter > walk_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images_right):
                    self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                if self.direction == -1:
                    self.image = self.images_left[self.index]

            # Add gravity
            self.vel_y += 1
            if self.vel_y > 10:
                self.vel_y = 10
            dy += self.vel_y

            # Check for collision
            self.in_air = True
            for tile in world.tile_list:
                # Check for collision in x direction
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0
                # Check for collision in y direction
                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    # Check if below the ground i.e. jumping
                    if self.vel_y < 0:
                        dy = tile[1].bottom - self.rect.top
                    # Check if above the ground i.e. falling
                    elif self.vel_y >= 0:
                        dy = tile[1].top - self.rect.bottom
                        self.vel_y = 0
                        self.in_air = False

            # Check for collision with enemies
            if pygame.sprite.spritecollide(self, blob_group, False):
                player_health -= 0.1  # If player collides with sprite, take 0.1 health
            # Check for collision with lava
            if pygame.sprite.spritecollide(self, lava_group, False):
                player_health -= 0.01  # If player collides with lava, take 0.01 health
            print(player_health)

            # Update player coordinates
            self.rect.x += dx
            self.rect.y += dy

            if self.rect.bottom > screen_height:
                self.rect.bottom = screen_height
                dy = 0

        elif game_over == -1:
            key = pygame.key.get_pressed()
            # Still allow player to exit with ESCAPE key even after they die
            if key[pygame.K_ESCAPE]:
                sys.exit()

            self.image =  self.dead_image
            if self.rect.y >= 200:
                self.rect.y -= 5

        # Draw player onto screen.
        screen.blit(self.image, self.rect)


        return player_health

    def reset(self, x, y):
        self.images_right = []
        self.images_left = []
        self.index = 0
        self.counter = 0
        for num in range(1, 5):
            img_right = pygame.image.load(f'img/steve{num}.png')
            img_right = pygame.transform.scale(img_right, (48, 84))
            img_left = pygame.transform.flip(img_right, True, False)
            self.images_right.append(img_right)
            self.images_left.append(img_left)
        self.dead_image = pygame.image.load('img/ghost.png')
        self.image = self.images_right[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0
        self.jumped = False
        self.direction = 0
        self.in_air = True


class World():
    def __init__(self, data):
        self.tile_list = []

        # Load images
        dirt_img = pygame.image.load('img/dirt_block.png')

        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:  # dirt Blocks added to game
                    img = pygame.transform.scale(dirt_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 2:  # Grass Blocks added to game
                    img = pygame.transform.scale(grass_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 3:  # Enemy added to game
                    blob = Enemy(col_count * tile_size, row_count * tile_size - 50)
                    blob_group.add(blob)
                if tile == 4:  # Stone Blocks added to game
                    img = pygame.transform.scale(stone_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 5:  # Coal Ore Blocks added to game
                    img = pygame.transform.scale(coal_ore_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 6:
                    lava = Lava(col_count * tile_size, row_count * tile_size + (tile_size // 2))
                    lava_group.add(lava)
                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])
            #pygame.draw.rect(screen, (255, 255, 255), tile[1], 2)


# Enemy sprite class
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('img/zombie_front.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        self.move_counter = 0
        self.vel_y = 0
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def update(self):
        # Find direction vector (dx, dy) between enemy and player.
        dx = player.rect.x - self.rect.x
        dy = player.rect.y - self.rect.y
        dist = math.hypot(dx, dy)
        dx, dy = dx / dist, dy / dist  # Normalize.

        # Move along this normalized vector towards the player at current speed.
        self.rect.x += dx * 3

        # Change sprite images based on which direction they are moving
        if self.rect.x < player.rect.x: # If moving right, use right facing sprite image
            self.image = pygame.image.load('img/zombie_side.png')
        elif self.rect.x > player.rect.x:  # If moving left, flip right facing sprite image so it is facing leftward
            self.image = pygame.image.load('img/zombie_side.png')
            self.image = pygame.transform.flip(self.image, True, False)
        else:  # Otherwise have sprite facing forward while still
            self.image = pygame.image.load('img/zombie_front.png')

        # Add gravity
        self.vel_y += 1
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y

        self.in_air = True
        for tile in world.tile_list:
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                # Check if below the ground i.e. jumping
                if self.vel_y < 0:
                    dy = tile[1].bottom - self.rect.top
                # Check if above the ground i.e. falling
                elif self.vel_y >= 0:
                    dy = tile[1].top - self.rect.bottom
                    self.vel_y = 0
                    self.in_air = False

        self.rect.x += dx
        self.rect.y += dy

        if self.rect.bottom > screen_height:
            self.rect.bottom = screen_height
            dy = 0


class Lava(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('img/lava.png')
        self.image = pygame.transform.scale(img, (tile_size, tile_size // 2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


world_data = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 1],
    [1, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 2, 2, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 7, 0, 5, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 1],
    [1, 7, 0, 0, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 7, 0, 0, 0, 0, 1],
    [1, 0, 2, 0, 0, 7, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 2, 0, 0, 2, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 7, 0, 0, 0, 0, 2, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 2, 0, 2, 2, 2, 2, 2, 1],
    [1, 0, 0, 0, 0, 0, 2, 2, 2, 6, 6, 6, 6, 6, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 4, 4, 4, 4, 1, 1],
    [1, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 4, 1, 4, 4, 5, 4, 4, 4, 4],
    [1, 2, 2, 2, 1, 1, 1, 1, 1, 1, 4, 4, 4, 4, 5, 5, 4, 5, 4, 4]
]

player = Player(100, screen_height - 130)

blob_group = pygame.sprite.Group()
lava_group = pygame.sprite.Group()

world = World(world_data)

# Create buttons
restart_button = Button(screen_width // 2 - 50, screen_height // 2 + 100, restart_img)
start_button = Button(screen_width // 2 - 350, screen_height // 2, start_img)
exit_button = Button(screen_width // 2 + 150, screen_height // 2, exit_img)

# Set the game to be running.
run = True
while run:

    # Fix frame rate
    clock.tick(fps)

    # Put sun and background on screen
    screen.blit(bg_img, (0, 0))
    #screen.blit(sun_img, (100, 100))

    # Draw start menu
    if main_menu == True:
        if exit_button.draw():
            run = False
        if start_button.draw():
            main_menu = False

    else:
        world.draw()

        if game_over == 0:
            blob_group.update()

        blob_group.draw(screen)
        lava_group.draw(screen)

        # Update player health from player update function
        player_health = player.update(player_health)

        # draw_grid()
        player_hunger_list = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

        # Determine player health and hunger
        if 10 < player_health <= 11:
            # Draw health and hunger bars to the screen with for loop
            i = 0  # Set i to zero before iteration begins
            x = 0  # Set starting x value for health
            screen.blit(health_full_img, (0, 960))
            screen.blit(health_full_img, (30, 960))
            screen.blit(health_full_img, (60, 960))
            screen.blit(health_full_img, (90, 960))
            screen.blit(health_full_img, (120, 960))
            screen.blit(health_full_img, (150, 960))
            screen.blit(health_full_img, (180, 960))
            screen.blit(health_full_img, (210, 960))
            screen.blit(health_full_img, (240, 960))
            screen.blit(health_full_img, (270, 960))
        elif 9.51 <= player_health <= 10:
            # Draw health and hunger bars to the screen with for loop
            i = 0  # Set i to zero before iteration begins
            x = 0  # Set starting x value for health
            screen.blit(health_full_img, (0, 960))
            screen.blit(health_full_img, (30, 960))
            screen.blit(health_full_img, (60, 960))
            screen.blit(health_full_img, (90, 960))
            screen.blit(health_full_img, (120, 960))
            screen.blit(health_full_img, (150, 960))
            screen.blit(health_full_img, (180, 960))
            screen.blit(health_full_img, (210, 960))
            screen.blit(health_full_img, (240, 960))
            screen.blit(health_half_img, (270, 960))
        elif 9 <= player_health < 9.5:
            # Draw health and hunger bars to the screen with for loop
            i = 0  # Set i to zero before iteration begins
            x = 0  # Set starting x value for health
            screen.blit(health_full_img, (0, 960))
            screen.blit(health_full_img, (30, 960))
            screen.blit(health_full_img, (60, 960))
            screen.blit(health_full_img, (90, 960))
            screen.blit(health_full_img, (120, 960))
            screen.blit(health_full_img, (150, 960))
            screen.blit(health_full_img, (180, 960))
            screen.blit(health_full_img, (210, 960))
            screen.blit(health_full_img, (240, 960))
            screen.blit(health_empty_img, (270, 960))
        elif 8.51 <= player_health < 9:
            # Draw health and hunger bars to the screen with for loop
            i = 0  # Set i to zero before iteration begins
            x = 0  # Set starting x value for health
            screen.blit(health_full_img, (0, 960))
            screen.blit(health_full_img, (30, 960))
            screen.blit(health_full_img, (60, 960))
            screen.blit(health_full_img, (90, 960))
            screen.blit(health_full_img, (120, 960))
            screen.blit(health_full_img, (150, 960))
            screen.blit(health_full_img, (180, 960))
            screen.blit(health_full_img, (210, 960))
            screen.blit(health_half_img, (240, 960))
            screen.blit(health_empty_img, (270, 960))
        elif 8 <= player_health < 8.5:
            # Draw health and hunger bars to the screen with for loop
            i = 0  # Set i to zero before iteration begins
            x = 0  # Set starting x value for health
            screen.blit(health_full_img, (0, 960))
            screen.blit(health_full_img, (30, 960))
            screen.blit(health_full_img, (60, 960))
            screen.blit(health_full_img, (90, 960))
            screen.blit(health_full_img, (120, 960))
            screen.blit(health_full_img, (150, 960))
            screen.blit(health_full_img, (180, 960))
            screen.blit(health_full_img, (210, 960))
            screen.blit(health_empty_img, (240, 960))
            screen.blit(health_empty_img, (270, 960))
        elif 7.51 <= player_health < 8:
            # Draw health and hunger bars to the screen with for loop
            i = 0  # Set i to zero before iteration begins
            x = 0  # Set starting x value for health
            screen.blit(health_full_img, (0, 960))
            screen.blit(health_full_img, (30, 960))
            screen.blit(health_full_img, (60, 960))
            screen.blit(health_full_img, (90, 960))
            screen.blit(health_full_img, (120, 960))
            screen.blit(health_full_img, (150, 960))
            screen.blit(health_full_img, (180, 960))
            screen.blit(health_half_img, (210, 960))
            screen.blit(health_empty_img, (240, 960))
            screen.blit(health_empty_img, (270, 960))
        elif 7 <= player_health < 7.5:
            # Draw health and hunger bars to the screen with for loop
            i = 0  # Set i to zero before iteration begins
            x = 0  # Set starting x value for health
            screen.blit(health_full_img, (0, 960))
            screen.blit(health_full_img, (30, 960))
            screen.blit(health_full_img, (60, 960))
            screen.blit(health_full_img, (90, 960))
            screen.blit(health_full_img, (120, 960))
            screen.blit(health_full_img, (150, 960))
            screen.blit(health_full_img, (180, 960))
            screen.blit(health_empty_img, (210, 960))
            screen.blit(health_empty_img, (240, 960))
            screen.blit(health_empty_img, (270, 960))
        elif 6.51 <= player_health < 7:
            # Draw health and hunger bars to the screen with for loop
            i = 0  # Set i to zero before iteration begins
            x = 0  # Set starting x value for health
            screen.blit(health_full_img, (0, 960))
            screen.blit(health_full_img, (30, 960))
            screen.blit(health_full_img, (60, 960))
            screen.blit(health_full_img, (90, 960))
            screen.blit(health_full_img, (120, 960))
            screen.blit(health_full_img, (150, 960))
            screen.blit(health_half_img, (180, 960))
            screen.blit(health_empty_img, (210, 960))
            screen.blit(health_empty_img, (240, 960))
            screen.blit(health_empty_img, (270, 960))
        elif 6 <= player_health < 6.5:
            # Draw health and hunger bars to the screen with for loop
            i = 0  # Set i to zero before iteration begins
            x = 0  # Set starting x value for health
            screen.blit(health_full_img, (0, 960))
            screen.blit(health_full_img, (30, 960))
            screen.blit(health_full_img, (60, 960))
            screen.blit(health_full_img, (90, 960))
            screen.blit(health_full_img, (120, 960))
            screen.blit(health_full_img, (150, 960))
            screen.blit(health_empty_img, (180, 960))
            screen.blit(health_empty_img, (210, 960))
            screen.blit(health_empty_img, (240, 960))
            screen.blit(health_empty_img, (270, 960))
        elif 5.51 <= player_health < 6:
            # Draw health and hunger bars to the screen with for loop
            i = 0  # Set i to zero before iteration begins
            x = 0  # Set starting x value for health
            screen.blit(health_full_img, (0, 960))
            screen.blit(health_full_img, (30, 960))
            screen.blit(health_full_img, (60, 960))
            screen.blit(health_full_img, (90, 960))
            screen.blit(health_full_img, (120, 960))
            screen.blit(health_half_img, (150, 960))
            screen.blit(health_empty_img, (180, 960))
            screen.blit(health_empty_img, (210, 960))
            screen.blit(health_empty_img, (240, 960))
            screen.blit(health_empty_img, (270, 960))
        elif 5 <= player_health < 5.5:
            # Draw health and hunger bars to the screen with for loop
            i = 0  # Set i to zero before iteration begins
            x = 0  # Set starting x value for health
            screen.blit(health_full_img, (0, 960))
            screen.blit(health_full_img, (30, 960))
            screen.blit(health_full_img, (60, 960))
            screen.blit(health_full_img, (90, 960))
            screen.blit(health_full_img, (120, 960))
            screen.blit(health_empty_img, (150, 960))
            screen.blit(health_empty_img, (180, 960))
            screen.blit(health_empty_img, (210, 960))
            screen.blit(health_empty_img, (240, 960))
            screen.blit(health_empty_img, (270, 960))
        elif 4.51 <= player_health < 5:
            # Draw health and hunger bars to the screen with for loop
            i = 0  # Set i to zero before iteration begins
            x = 0  # Set starting x value for health
            screen.blit(health_full_img, (0, 960))
            screen.blit(health_full_img, (30, 960))
            screen.blit(health_full_img, (60, 960))
            screen.blit(health_full_img, (90, 960))
            screen.blit(health_half_img, (120, 960))
            screen.blit(health_empty_img, (150, 960))
            screen.blit(health_empty_img, (180, 960))
            screen.blit(health_empty_img, (210, 960))
            screen.blit(health_empty_img, (240, 960))
            screen.blit(health_empty_img, (270, 960))
        elif 4 <= player_health < 4.5:
            # Draw health and hunger bars to the screen with for loop
            i = 0  # Set i to zero before iteration begins
            x = 0  # Set starting x value for health
            screen.blit(health_full_img, (0, 960))
            screen.blit(health_full_img, (30, 960))
            screen.blit(health_full_img, (60, 960))
            screen.blit(health_full_img, (90, 960))
            screen.blit(health_empty_img, (120, 960))
            screen.blit(health_empty_img, (150, 960))
            screen.blit(health_empty_img, (180, 960))
            screen.blit(health_empty_img, (210, 960))
            screen.blit(health_empty_img, (240, 960))
            screen.blit(health_empty_img, (270, 960))
        elif 3.51 <= player_health < 4:
            # Draw health and hunger bars to the screen with for loop
            i = 0  # Set i to zero before iteration begins
            x = 0  # Set starting x value for health
            screen.blit(health_full_img, (0, 960))
            screen.blit(health_full_img, (30, 960))
            screen.blit(health_full_img, (60, 960))
            screen.blit(health_half_img, (90, 960))
            screen.blit(health_empty_img, (120, 960))
            screen.blit(health_empty_img, (150, 960))
            screen.blit(health_empty_img, (180, 960))
            screen.blit(health_empty_img, (210, 960))
            screen.blit(health_empty_img, (240, 960))
            screen.blit(health_empty_img, (270, 960))
        elif 3 <= player_health < 3.5:
            # Draw health and hunger bars to the screen with for loop
            i = 0  # Set i to zero before iteration begins
            x = 0  # Set starting x value for health
            screen.blit(health_full_img, (0, 960))
            screen.blit(health_full_img, (30, 960))
            screen.blit(health_full_img, (60, 960))
            screen.blit(health_empty_img, (90, 960))
            screen.blit(health_empty_img, (120, 960))
            screen.blit(health_empty_img, (150, 960))
            screen.blit(health_empty_img, (180, 960))
            screen.blit(health_empty_img, (210, 960))
            screen.blit(health_empty_img, (240, 960))
            screen.blit(health_empty_img, (270, 960))
        elif 2.51 <= player_health < 3:
            # Draw health and hunger bars to the screen with for loop
            i = 0  # Set i to zero before iteration begins
            x = 0  # Set starting x value for health
            screen.blit(health_full_img, (0, 960))
            screen.blit(health_full_img, (30, 960))
            screen.blit(health_half_img, (60, 960))
            screen.blit(health_empty_img, (90, 960))
            screen.blit(health_empty_img, (120, 960))
            screen.blit(health_empty_img, (150, 960))
            screen.blit(health_empty_img, (180, 960))
            screen.blit(health_empty_img, (210, 960))
            screen.blit(health_empty_img, (240, 960))
            screen.blit(health_empty_img, (270, 960))
        elif 2 <= player_health < 2.5:
            # Draw health and hunger bars to the screen with for loop
            i = 0  # Set i to zero before iteration begins
            x = 0  # Set starting x value for health
            screen.blit(health_full_img, (0, 960))
            screen.blit(health_full_img, (30, 960))
            screen.blit(health_empty_img, (60, 960))
            screen.blit(health_empty_img, (90, 960))
            screen.blit(health_empty_img, (120, 960))
            screen.blit(health_empty_img, (150, 960))
            screen.blit(health_empty_img, (180, 960))
            screen.blit(health_empty_img, (210, 960))
            screen.blit(health_empty_img, (240, 960))
            screen.blit(health_empty_img, (270, 960))
        elif 1.51 <= player_health < 2:
            # Draw health and hunger bars to the screen with for loop
            i = 0  # Set i to zero before iteration begins
            x = 0  # Set starting x value for health
            screen.blit(health_full_img, (0, 960))
            screen.blit(health_half_img, (30, 960))
            screen.blit(health_empty_img, (60, 960))
            screen.blit(health_empty_img, (90, 960))
            screen.blit(health_empty_img, (120, 960))
            screen.blit(health_empty_img, (150, 960))
            screen.blit(health_empty_img, (180, 960))
            screen.blit(health_empty_img, (210, 960))
            screen.blit(health_empty_img, (240, 960))
            screen.blit(health_empty_img, (270, 960))
        elif 1 <= player_health < 1.5:
            # Draw health and hunger bars to the screen with for loop
            i = 0  # Set i to zero before iteration begins
            x = 0  # Set starting x value for health
            screen.blit(health_full_img, (0, 960))
            screen.blit(health_empty_img, (30, 960))
            screen.blit(health_empty_img, (60, 960))
            screen.blit(health_empty_img, (90, 960))
            screen.blit(health_empty_img, (120, 960))
            screen.blit(health_empty_img, (150, 960))
            screen.blit(health_empty_img, (180, 960))
            screen.blit(health_empty_img, (210, 960))
            screen.blit(health_empty_img, (240, 960))
            screen.blit(health_empty_img, (270, 960))
        elif 0.51 <= player_health < 1:
            # Draw health and hunger bars to the screen with for loop
            i = 0  # Set i to zero before iteration begins
            x = 0  # Set starting x value for health
            screen.blit(health_half_img, (0, 960))
            screen.blit(health_empty_img, (30, 960))
            screen.blit(health_empty_img, (60, 960))
            screen.blit(health_empty_img, (90, 960))
            screen.blit(health_empty_img, (120, 960))
            screen.blit(health_empty_img, (150, 960))
            screen.blit(health_empty_img, (180, 960))
            screen.blit(health_empty_img, (210, 960))
            screen.blit(health_empty_img, (240, 960))
            screen.blit(health_empty_img, (270, 960))
        elif 0.01 <= player_health < 0.5:
            # Draw health and hunger bars to the screen with for loop
            i = 0  # Set i to zero before iteration begins
            x = 0  # Set starting x value for health
            screen.blit(health_half_img, (0, 960))
            screen.blit(health_empty_img, (30, 960))
            screen.blit(health_empty_img, (60, 960))
            screen.blit(health_empty_img, (90, 960))
            screen.blit(health_empty_img, (120, 960))
            screen.blit(health_empty_img, (150, 960))
            screen.blit(health_empty_img, (180, 960))
            screen.blit(health_empty_img, (210, 960))
            screen.blit(health_empty_img, (240, 960))
            screen.blit(health_empty_img, (270, 960))
        elif player_health < 0:
            # Draw health and hunger bars to the screen with for loop
            i = 0  # Set i to zero before iteration begins
            x = 0  # Set starting x value for health
            screen.blit(health_empty_img, (0, 960))
            screen.blit(health_empty_img, (30, 960))
            screen.blit(health_empty_img, (60, 960))
            screen.blit(health_empty_img, (90, 960))
            screen.blit(health_empty_img, (120, 960))
            screen.blit(health_empty_img, (150, 960))
            screen.blit(health_empty_img, (180, 960))
            screen.blit(health_empty_img, (210, 960))
            screen.blit(health_empty_img, (240, 960))
            screen.blit(health_empty_img, (270, 960))
            game_over = -1
        else:
            print("Health bar value out of bounds")
        # If player dies
        key = pygame.key.get_pressed()
        if game_over == -1:
            if restart_button.draw():
                player.reset(100, screen_height - 130)
                game_over = 0
                player_health = 10.5
            if key[pygame.K_r]:
                player.reset(100, screen_height - 130)
                game_over = 0
                player_health = 10.5

    for event in pygame.event.get():
        # If user quits then the program stops running.
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()  # Update window
