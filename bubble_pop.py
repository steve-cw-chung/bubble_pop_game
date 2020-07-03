import pygame
import os
###############################################################################
pygame.init() # initialize ( MUST DO )

# secreen resolution setup
screen_width = 640 # horizontal 
screen_height = 480 # vertical
screen = pygame.display.set_mode((screen_width, screen_height))

# screen title setup
pygame.display.set_caption("Catharziz Games") # Game name

# FPS
clock = pygame.time.Clock()
############################################################################################

# 1. User game initialization ( resolution, game image, coordinates, speed, font, etc)
current_path = os.path.dirname(__file__) # get file directory
image_path = os.path.join(current_path, "images")  # get images folder 

# background
background = pygame.image.load(os.path.join(image_path, "background.png"))

# stage
stage = pygame.image.load(os.path.join(image_path, "stage.png"))
stage_size = stage.get_rect().size
stage_height = stage_size[1]

#character
character = pygame.image.load(os.path.join(image_path, "character.png"))
character_size = character.get_rect().size
character_width = character_size[0]
character_height = character_size[1]
character_x_pos = (screen_width / 2) - (character_width / 2)
character_y_pos = screen_height - character_height - stage_height

# character movement direction
character_to_x = 0

#character speed
character_speed = 5

# weapon
weapon = pygame.image.load(os.path.join(image_path, "weapon.png"))
weapon_size = weapon.get_rect().size
weapon_width = weapon_size[0]

# weapon can be shot more than once at a time
weapons = []

# weapon speed
weapon_speed = 10

# bubble 

bubble_images = [
    pygame.image.load(os.path.join(image_path, "bubble1.png")),
    pygame.image.load(os.path.join(image_path, "bubble2.png")),       
    pygame.image.load(os.path.join(image_path, "bubble3.png")),
    pygame.image.load(os.path.join(image_path, "bubble4.png"))]

# bubble speeds
bubble_speed_y = [-18,-15,-12,-9] # index 0,1,2,3 

# bubbles
bubbles = []

bubbles.append({
    "pos_x" : 50, # bubble x position
    "pos_y" : 50, # bubble y position
    "img_idx" : 0, # bubble image
    "to_x" : 3, # x movement 
    "to_y" : -6, # y movement
    "init_spd_y" : bubble_speed_y[0]})# y speed

weapon_to_remove = -1
bubble_to_remove = -1

# Font definition
game_font = pygame.font.Font(None, 40)
total_time = 100
start_ticks = pygame.time.get_ticks() # game time

# Game end message ( Timeout, Mission Complete, Gave Over )

game_result = "Game Over"


running = True 
while running:
    dt = clock.tick(30) 

    # 2. Event Handler ( Keyboard, Mouse, etc )
    for event in pygame.event.get(): # check events
        if event.type == pygame.QUIT: # X clicked
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                character_to_x -= character_speed
            elif event.key == pygame.K_RIGHT:
                character_to_x += character_speed
            elif event.key == pygame.K_SPACE:
                weapon_x_pos = character_x_pos + character_width/2 - weapon_width/2
                weapon_y_pos = character_y_pos
                weapons.append([weapon_x_pos,weapon_y_pos])
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                character_to_x = 0
    # 3. Definition for game character location 
    character_x_pos += character_to_x

    if character_x_pos < 0:
        character_x_pos = 0
    elif character_x_pos > screen_width - character_width:
        character_x_pos = screen_width - character_width
    
    # weapon location
    weapons = [ [w[0], w[1] - weapon_speed] for w in weapons] # move weapon up
    
    # on weapon and roof contact
    weapons = [ [w[0], w[1]] for w in weapons if w[1] >= 0]

    # bubble location
    for bubble_idx, bubble_val in enumerate(bubbles):
        bubble_pos_x = bubble_val["pos_x"]
        bubble_pos_y = bubble_val["pos_y"]
        bubble_img_idx = bubble_val["img_idx"]

        bubble_size = bubble_images[bubble_img_idx].get_rect().size
        bubble_width = bubble_size[0]
        bubble_height = bubble_size[1]
        
        # bounced to verital walls 
        if bubble_pos_x < 0 or bubble_pos_x > screen_width - bubble_width:
            bubble_val["to_x"] = bubble_val["to_x"] * -1

        # horizontal position
        if bubble_pos_y >= screen_height - stage_height - bubble_height:
            bubble_val["to_y"] = bubble_val["init_spd_y"]
        else:
            bubble_val["to_y"] += 0.5

        bubble_val["pos_x"] += bubble_val["to_x"]
        bubble_val["pos_y"] += bubble_val["to_y"]
    # 4. Collision 
    
    # character rect info update
    character_rect = character.get_rect()
    character_rect.left = character_x_pos
    character_rect.top = character_y_pos

    for bubble_idx, bubble_val in enumerate(bubbles):
        bubble_pos_x = bubble_val["pos_x"]
        bubble_pos_y = bubble_val["pos_y"]
        bubble_img_idx = bubble_val["img_idx"]

        # update bubble rect info
        bubble_rect = bubble_images[bubble_img_idx].get_rect()
        bubble_rect.left = bubble_pos_x
        bubble_rect.top = bubble_pos_y
        
        # collision check
        if character_rect.colliderect(bubble_rect):
            running = False
            break

        # bubble and weapon collision
        for weapon_idx, weapon_val in enumerate(weapons):
            weapon_pos_x = weapon_val[0]
            weapon_pos_y = weapon_val[1]

            # update weapon rect info
            weapon_rect = weapon.get_rect()
            weapon_rect.left = weapon_pos_x
            weapon_rect.top = weapon_pos_y 

            # collision check
            if weapon_rect.colliderect(bubble_rect):
                weapon_to_remove = weapon_idx 
                bubble_to_remove = bubble_idx 
                
                if bubble_img_idx < 3:
                    # current bubble size info
                        bubble_width = bubble_rect.size[0]
                        bubble_height = bubble_rect.size[1]

                        # divided bubble info 
                        small_bubble_rect = bubble_images[bubble_img_idx + 1].get_rect()
                        small_bubble_width = small_bubble_rect.size[0]
                        small_bubble_height = small_bubble_rect.size[1]
                        # left bubble
                        bubbles.append({
                            "pos_x" : bubble_pos_x + bubble_width /2 - small_bubble_width,
                            "pos_y" : bubble_pos_y + bubble_height /2 - small_bubble_height,
                            "img_idx" : bubble_img_idx +1,
                            "to_x" : -3,
                            "to_y" : -6,
                            "init_spd_y" : bubble_speed_y[bubble_img_idx +1]})
                        # right bubble
                        bubbles.append({
                            "pos_x" : bubble_pos_x + bubble_width /2 - small_bubble_width,
                            "pos_y" : bubble_pos_y + bubble_height /2 - small_bubble_height,
                            "img_idx" : bubble_img_idx +1,
                            "to_x" : 3,
                            "to_y" : -6,
                            "init_spd_y" : bubble_speed_y[bubble_img_idx +1]})
                break
        else:   # this is added to fix the bug
            continue
        break
    # delete weapon or bubble
    if bubble_to_remove > -1:
        del bubbles[bubble_to_remove]
        bubble_to_remove = -1
    if weapon_to_remove > -1:
        del weapons[weapon_to_remove]
        weapon_to_remove = -1

    # exit when all bubbles gone
    if len(bubbles) == 0:
        game_result = "Mission Complete"
        running = False

    # 5. Draw on Screen
    screen.blit(background, (0,0))
    for weapon_x_pos, weapon_y_pos in weapons:
        screen.blit(weapon, (weapon_x_pos, weapon_y_pos))

    for idx, val in enumerate(bubbles):
        bubble_pos_x = val["pos_x"]
        bubble_pos_y = val["pos_y"]
        bubble_img_idx = val["img_idx"]
        screen.blit(bubble_images[bubble_img_idx], (bubble_pos_x,bubble_pos_y))
    screen.blit(stage, (0,screen_height - stage_height))
    screen.blit(character,(character_x_pos,character_y_pos))
 

    elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000 # ms -> s
    timer = game_font.render("Time : {}".format(int(total_time - elapsed_time)),True, (255,255,255))
    screen.blit(timer,(10,10))

    # Timeout
    if total_time - elapsed_time <= 0:
        game_result = "Time Over"
        running = False
    pygame.display.update() # redrawing game screen




# game over message 
msg = game_font.render(game_result, True, (255, 0, 0)) # yellow
msg_rect = msg.get_rect(center=(int(screen_width / 2) , int(screen_height / 2 )))
screen.blit(msg, msg_rect)
pygame.display.update()

# delay before ending
pygame.time.delay(2000) # wait 2 seconds before ending (ms)
#pygame exit

pygame.quit()

