'''
Test_Game using pygame module. Use idle under D:\Anaconda\Scripts\idle
'''

import pygame
import numpy as np
from threading import Timer
pygame.init()

screenWidth = 1600 # Full screen dimensions.
screenHeight = 896 # Make sure these are divisible by player width and height.

win = pygame.display.set_mode((screenWidth,screenHeight), pygame.FULLSCREEN)

pygame.display.set_caption("My First Game")

walkRight = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png'), pygame.image.load('R4.png')]
walkLeft = [pygame.image.load('L1.png'), pygame.image.load('L2.png'), pygame.image.load('L3.png'), pygame.image.load('L4.png')] 
walkUp = [pygame.image.load('B1.png'), pygame.image.load('B2.png'), pygame.image.load('B3.png'), pygame.image.load('B4.png')]
#walkDown = [pygame.image.load('F1.png'), pygame.image.load('F2.png'), pygame.image.load('F3.png'), pygame.image.load('F4.png')]
walkDown = [pygame.image.load('F1_dagger.png'), pygame.image.load('F2_dagger.png'), pygame.image.load('F3_dagger.png'), pygame.image.load('F4_dagger.png')]
#logSurface = pygame.image.load('logSurface.png') # 800 x 750
logSurface = pygame.image.load('logSurface.png') # 475 x 214

'''
HOW TO IMPLEMENT DIFFERENT SPRITES INTO THE GAME...

- For TONS of animal/enemy sprites, go to this website and look at the original post at the top of the forum:
https://forums.rpgmakerweb.com/index.php?threads/whtdragons-animals-and-running-horses-now-with-more-dragons.53552/

- For weapon sprites (under BATTLE WEAPONS), crops, chests, old water pumps, cauldrons, and much more (under OBJECTS at the bottom), go to:
https://forums.rpgmakerweb.com/index.php?threads/avys-mv-stuff.53317/

- For villager sprites, LOTS of fighting enemies like spiders, weapons and much more go to:
https://forums.rpgmakerweb.com/index.php?threads/hiddenones-mv-resource-warehouse.47255/

- Some cool 16-bit images, including potions, swords, coins etc.

NOTE: Dagger sprites are added onto character sprites. For down (and up?), rotate dagger 20 deg toward player in Paint 3D. Then make it a 3D object. Then
rotate 60 deg towards player about y axis (button on bottom). Position consistent between dagger and dagger swings. Take into account raised hand when walking.

###########################################################################################################################################
Save the picture you want into the game folder. This will give you many different versions of the animal/enemy etc.
Using the default Photos app on Windows, you can crop the image to get the version you like best, resulting in 12 sprites.
You generally cannot crop any further with Photos, so you will need to use another method to split the sprite sheet into 12 images.

1.) To crop images that contain only a few pixels, you can right click on the image and choose "Edit with Paint 3D".  Make sure you first
turn Transparent canvas OFF by first clicking on Canvas at the top. This takes away the gray background, Crop the image to get a
single sprite. Then save the cropped image as a new image in the game folder with a fitting name (e.g. bunny_1).

2.) [This method takes longer and is obsolete, but works if you want the cropping done fast, you want to split the image into many pieces,
and you don't care if it's not a pixel perfect crop... e.g. this method is more useful for a background image broken into chunks.]
To split large images into smaller images automatically (it will not crop them perfectly), go to this website:
https://www.imgonline.com.ua/eng/cut-photo-into-pieces.php
Here, you need to specify how you are splitting it. For these animal/enemy sprites, it is generally 3x4. Download the zip file that the
website outputs into your game folder. Then you can crop them perfectly by right clicking on each image and choosing "Edit with
Paint 3D". Once cropped, save and rename the images to something fitting.

'''

map_string_list = [] # 12800 x 7168 map, but broken into 64 chunks, each 1600 x 896.
for i in range(1, 65):
    if i < 10:
        map_string_list.append("image_part_00" + str(i) + ".jpg")
    else:
        map_string_list.append("image_part_0" + str(i) + ".jpg")
map_list = []
for pic in map_string_list:
    map_list.append(pygame.image.load(pic))

clock = pygame.time.Clock()
numSprites = 4 # sprites per direction
fps = 32 # divisible by numSprites

############################################################

class player(object):
    
    def __init__(self, x, y, width, height, class_index, player_class, health, stamina, mana, abilities, base_dmg):
        
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        
        self.vel = 8
        self.left = False
        self.right = False
        self.up = False
        self.down = False
        self.stand = True
        self.walkCount = 0

        self.hitbox = (self.x, self.y, 64, 64) # Can I make better?
        
        self.bar_width = 200
        self.bar_height = 20

        self.class_index = class_index
        self.player_class = player_class
        self.health = health
        self.max_health = health
        self.stamina = stamina
        self.max_stamina = stamina
        self.mana = mana
        self.max_mana = mana
        self.abilities = abilities

        self.max_inventory = 20
        self.inventory = []
        self.tele_home = []
        self.exp = 0
        self.level = 1
        self.gold = 0
        self.max_level = 50
        self.max_level_status = False
        self.max_skill_level = 50

        self.blacksmithing_level = 1
        self.armoring_level = 1
        self.smelting_level = 1
        self.mining_level = 1
        self.gardening_level = 1
        self.herbGathering_level = 1
        self.alchemy_level = 1
        self.fishing_level = 1
        self.enchanting_level = 1
        self.fabricWeaving_level = 1
        self.cooking_level = 1

        self.blacksmithing_exp = 0
        self.armoring_exp = 0
        self.smelting_exp = 0
        self.mining_exp = 0
        self.gardening_exp = 0
        self.herbGathering_exp = 0
        self.alchemy_exp = 0
        self.fishing_exp = 0
        self.enchanting_exp = 0
        self.fabricWeaving_exp = 0
        self.cooking_exp = 0

        self.max_blacksmithing_status = False
        self.max_armoring_status = False
        self.max_smelting_status = False
        self.max_mining_status = False
        self.max_gardening_status = False
        self.max_herbGathering_status = False
        self.max_alchemy_status = False
        self.max_fishing_status = False
        self.max_enchanting_status = False
        self.max_fabricWeaving_status = False
        self.max_cooking_status = False

        self.base_dmg = base_dmg

    def draw(self, win):

        #############################################
        # Player Sprites

        if self.walkCount + 1 >= fps: # walk lists have 4 sprites, display each for 8 frames
            self.walkCount = 0
        if self.left:
            if self.stand:
                win.blit(walkLeft[0], (self.x,self.y))
            else:
                win.blit(walkLeft[self.walkCount//(fps//numSprites)], (self.x,self.y))
                self.walkCount += 1
        elif self.right:
            if self.stand:
                win.blit(walkRight[1], (self.x,self.y))
            else:
                win.blit(walkRight[self.walkCount//(fps//numSprites)], (self.x,self.y))
                self.walkCount += 1        
        elif self.up:
            if self.stand:
                win.blit(walkUp[1], (self.x,self.y))
            else:
                win.blit(walkUp[self.walkCount//(fps//numSprites)], (self.x,self.y))
                self.walkCount += 1
        elif self.down:
            if self.stand:
                win.blit(walkDown[1], (self.x,self.y))
            else:
                win.blit(walkDown[self.walkCount//(fps//numSprites)], (self.x,self.y))
                self.walkCount += 1   
        elif self.stand:
            win.blit(walkDown[1], (self.x,self.y))

        #############################################
        # Hitbox

        self.hitbox = (self.x, self.y, 64, 64)
        pygame.draw.rect(win, (255,0,0), self.hitbox, 2)

        #############################################
        # Health, Stamina, and Mana Bars
        
        pygame.draw.rect(win, (200, 0, 0), (30, 30, self.bar_width, self.bar_height))
        if self.health > 0:
            pygame.draw.rect(win, (0,200,0), (30, 30, int(self.bar_width * (self.health / self.max_health)), self.bar_height))
            
        healthText = logFont.render(str(int(100* self.health / self.max_health)) + '%', 1, (0, 0, 0))
        healthText_rect = healthText.get_rect(center=((30 + 30 + self.bar_width)/2, (30 + 30 + self.bar_height)/2))
        win.blit(healthText, healthText_rect)
        
        if self.class_index == 1 or self.class_index == 2 or self.class_index == 3:
            pygame.draw.rect(win, (105, 105, 105), (30, 50, self.bar_width, self.bar_height))
            if self.stamina > 0:
                pygame.draw.rect(win, (200, 200, 0), (30, 50, int(self.bar_width * (self.stamina / self.max_stamina)), self.bar_height))
                
            staminaText = logFont.render(str(int(100 * self.stamina / self.max_stamina)) + '%', 1, (0, 0, 0))
            staminaText_rect = staminaText.get_rect(center=((30 + 30 + self.bar_width)/2, (50 + 50 + self.bar_height)/2))
            win.blit(staminaText, staminaText_rect)
        else:
            pygame.draw.rect(win, (105, 105, 105), (30, 50, self.bar_width, self.bar_height))
            if self.mana > 0:
                pygame.draw.rect(win, (0, 80, 200), (30, 50, int(self.bar_width * (self.mana / self.max_mana)), self.bar_height))

            manaText = logFont.render(str(int(100 * self.mana / self.max_mana)) + '%', 1, (0, 0, 0))
            manaText_rect = manaText.get_rect(center=((30 + 30 + self.bar_width)/2, (50 + 50 + self.bar_height)/2))
            win.blit(manaText, manaText_rect)

    def gainExp(self, gainedExp, expThreshold):

        if not self.max_level_status:
            self.exp += gainedExp
            log.logStore(['Gained ' + str(gainedExp) + ' experience.'])
            t = 0
            for i in range(min(self.level, self.max_level - 2), self.max_level - 1):
                if self.exp >= expThreshold[min(i, self.max_level - 2)] and self.exp <= expThreshold[min(i + 1, self.max_level - 1)]:
                    if self.level != self.max_level - 1:
                        self.level += 1 + t 
                        self.level = min(self.level, self.max_level)
                        log.logStore(['Congratulations! You\'ve leveled up!', 'You are now level ' + str(self.level) + '.'])
                t += 1
            if self.exp >= expThreshold[self.max_level - 1]:
                log.logStore(['Congratulations! You\'ve reached the max level, ' + str(self.max_level) + '!'])
                self.max_level_status = True

    def gainSkillExp(self, gainedSkillExp, skill, skillExpThreshold):
        
        if skill == 'Blacksmithing':
            skill_exp = self.blacksmithing_exp
            skill_level = self.blacksmithing_level
            max_skill_status = self.max_blacksmithing_status
        elif skill == 'Armoring':
            skill_exp = self.armoring_exp
            skill_level = self.armoring_level
            max_skill_status = self.max_armoring_status
        elif skill == 'Smelting':
            skill_exp = self.smelting_exp
            skill_level = self.smelting_level
            max_skill_status = self.max_smelting_status
        elif skill == 'Mining':
            skill_exp = self.mining_exp
            skill_level = self.mining_level
            max_skill_status = self.max_mining_status
        elif skill == 'Gardening':
            skill_exp = self.gardening_exp
            skill_level = self.gardening_level
            max_skill_status = self.max_gardening_status
        elif skill == 'Herb Gathering':
            skill_exp = self.herbGathering_exp
            skill_level = self.herbGathering_level
            max_skill_status = self.max_herbGathering_status
        elif skill == 'Alchemy':
            skill_exp = self.alchemy_exp
            skill_level = self.alchemy_level
            max_skill_status = self.max_alchemy_status
        elif skill == 'Fishing':
            skill_exp = self.fishing_exp
            skill_level = self.fishing_level
            max_skill_status = self.max_fishing_status
        elif skill == 'Enchanting':
            skill_exp = self.enchanting_exp
            skill_level = self.enchanting_level
            max_skill_status = self.max_enchanting_status
        elif skill == 'Fabric Weaving':
            skill_exp = self.fabricWeaving_exp
            skill_level = self.fabricWeaving_level
            max_skill_status = self.max_fabricWeaving_status
        elif skill == 'Cooking':
            skill_exp = self.cooking_exp
            skill_level = self.cooking_level
            max_skill_status = self.max_cooking_status

        if not max_skill_status:            
            skill_exp += gainedSkillExp
            log.logStore(['Gained ' + str(gainedSkillExp) + ' ' + skill + ' experience.'])
            t = 0
            for i in range(min(skill_level, self.max_skill_level - 2), self.max_skill_level - 1):
                if skill_exp >= skillExpThreshold[min(i, self.max_skill_level - 2)] and skill_exp <= skillExpThreshold[min(i + 1, self.max_skill_level - 1)]:
                    if skill_level != self.max_skill_level - 1:
                        skill_level += 1 + t 
                        skill_level = min(skill_level, self.max_skill_level)
                        log.logStore(['Congratulations! You are now level ' + str(skill_level) + ' in ' + skill + '!'])
                t += 1
            if skill_exp >= skillExpThreshold[self.max_skill_level - 1]:
                log.logStore(['Congratulations! You\'ve reached the max level, ' + str(self.max_skill_level) + ', in ' + skill + '!'])
                max_skill_status = True

            return skill_exp, skill_level, max_skill_status

        else:
            return skill_exp, skill_level, max_skill_status

    def gainItem(self, item):
    
        if len(self.inventory) >= self.max_inventory:
            log.logStore(['Inventory is full.'])
        else:
            self.inventory.append(item)
            log.logStore(['Picked up ' + item + '.'])

    def gainGold(self, gainedGold):
        
        self.gold += gainedGold
        log.logStore(['Gained ' + str(gainedGold) + ' gold.'])

    def pressed(self, key): # Let the player hotkey their abilities to different buttons

        if key == 1:
            self.attack(self.abilities[3]) # Base Attack

        if key == 2:
            self.attack(self.abilities[4]) # Starting class-specific move

    def attack(self, ability):

        if enemy.any_highlighted:

            rel_enemy = enemy.whichHighlighted()

            if ability == 'Base Attack':
                
                if self.class_index == 1 or self.class_index == 2: # melee
                    if dist <= np.sqrt(((self.width/2) + (rel_enemy.widths[0]/2) + 20)**2 + ((self.height/2) + (rel_enemy.heights[0]/2) + 20)**2):
                        
                        if rel_enemy.health > 0:
                            rel_enemy.health -= self.base_dmg
                            rel_enemy.health = max(0, rel_enemy.health)

                elif self.class_index == 3: # arrow
                    if dist <= 250:

                        if rel_enemy.health > 0:
                            rel_enemy.health -= self.base_dmg
                            rel_enemy.health = max(0, rel_enemy.health)

                elif self.class_index == 4 or self.class_index == 5 or self.class_index == 6: # ranged magic
                    if dist <= 300:

                        if rel_enemy.health > 0:
                            rel_enemy.health -= self.base_dmg
                            rel_enemy.health = max(0, rel_enemy.health)

            elif ability == 'Harden':
                pass
            elif ability == 'Puncture':
                pass
            elif ability == 'Kick':
                pass
            elif ability == 'Elemental Call':
                pass
            elif ability == 'Curse':
                pass
            elif ability == 'Flash of Light':
                pass
        
############################################################

class enemy(object):

    '''
    I want to create enemies that move randomly in a given area. Thus, I need to specify the width and height
    of the area they can roam in and give their path a randomness to it, but make sure the boundaries are upheld.
    The randomness I'm thinking of for now can be 1/5 chance of either moving left, right, up, down or stand still.
    Whichever is choosen, the enemy will go in that direction or stand still for a certain amount of time. Then it resets.
    '''

    objs = [] # Registrar
    any_highlighted = False # True if any attacking enemy is already highlighted.

    def __init__(self, x, y, widths, heights, vel, containmentArea, health, convert12to16, threat):

        enemy.objs.append(self) # Each object instance is added to the list "objs". Used for @classmethods

        self.x = x
        self.y = y
        self.widths = widths # list of widths and heights of the sprites facing different directions (x4) in the order below.
        self.heights = heights
        
        ''' The order of widths and heights lists are left (0), right (1), up (2), down (3). '''
        
        self.hitbox = (self.x, self.y, self.widths[3], self.heights[3])
        self.containmentArea = containmentArea # area the enemy can move around in. (left, top, width, height)

        self.convert12to16 = convert12to16
        if self.convert12to16:
            self.numEnemySprites = 4 # per direction
        else:
            self.numEnemySprites = 3
        self.enemy_fps = self.numEnemySprites * 8 # 24 or 32 depending on whether numEnemySprites is 3 or 4
        
        self.walkCount = 0
        self.vel = vel
        self.left = False
        self.right = False
        self.up = False
        self.down = False
        self.stand = True
        
        self.direction = np.random.rand()
        self.loopCount = 0
        self.loopReset = 25

        self.walkRight_sprites = []
        self.walkLeft_sprites = []
        self.walkUp_sprites = []
        self.walkDown_sprites = []

        self.highlighted = False
        self.threat = threat
        self.aggro_dist = 300
        self.attackLoop = False
        self.path = ' '
        
        self.offset1 = 6
        self.offset2 = 24 # 24
        self.offset3 = 0 # If player is above and enemies are looking left or right, it looks like they are too far away. So need this to be big!
        self.offset4 = 20

        self.level = np.random.randint(1, 4) # Level can be anything from 1 to 3.
        self.base_dmg = 5 * self.level
        self.health = health
        self.max_health = health
        self.damageLoop = False
        self.initialAttack = True
        self.initSwitch = True

        self.health_bar_width = 100
        self.health_bar_height = 20

    def loadSprites_12(self, baseImageName, png = True, jpg = False): # convert12to16 makes 4 sprites per direction from a sprite sheet with 3 sprites per direction.

        if png:
            ext = '.png'
        elif jpg:
            ext = '.jpg'
        
        for i in range(1, 12 + 1): # 12 sprites total in the sprite sheet (3 per direction, 4 directions)
            if i <= 3:
                self.walkDown_sprites.append(pygame.image.load(baseImageName + '_' + str(i) + ext))
                if i == 3:
                    if self.convert12to16:
                        self.walkDown_sprites.append(pygame.image.load(baseImageName + '_' + str(i-1) + ext)) # Adding extra sprite to keep consistent with 4 sprites per direction.
            if i > 3 and i <= 6:
                self.walkLeft_sprites.append(pygame.image.load(baseImageName + '_' + str(i) + ext))
                if i == 6:
                    if self.convert12to16:
                        self.walkLeft_sprites.append(pygame.image.load(baseImageName + '_' + str(i-1) + ext))
            if i > 6 and i <= 9:
                self.walkRight_sprites.append(pygame.image.load(baseImageName + '_' + str(i) + ext))
                if i == 9:
                    if self.convert12to16:
                        self.walkRight_sprites.append(pygame.image.load(baseImageName + '_' + str(i-1) + ext))
            if i > 9:
                self.walkUp_sprites.append(pygame.image.load(baseImageName + '_' + str(i) + ext))
                if i == 12:
                    if self.convert12to16:
                        self.walkUp_sprites.append(pygame.image.load(baseImageName + '_' + str(i-1) + ext))

    def chase(self, prevPath): # threat - 0: No aggro, and will not fight back (small critters) 1: Will aggro. 2: No aggro, but will fight back
        '''
        If this is called, instead of the enemy doing their normal enemy.move() random behavior, I want them to move towards the player
        and attack them once close enough. I need to make sure they "chase" the player if he/she decides to run away (i.e. mirror the players movements?).
        I'm thinking the enemy moving toward the player can be done by first calculating the distance between them (by calling the distanceFromPlayer function).
        Since the game has only 4 directions, the enemy cannot travel along the line between it and the player. They have to travel in 2 directions to get there.
        Now consider the triangle that is made up of x and y components of the distance between enemy and player (really, 2 possible triangles). The sides of this
        triangle are what the enemy must travel along to get there. Keep in mind that either direction that is chosen initially will result in the same distance
        traveled in the end, so there is no one preferred direction to start in (thinking about things statically). However, when the player is moving, it makes
        more sense for the enemy to travel along the longer of the triangle sides. This will result in looking more like the enemy is chasing the player.

          Update: This method was causing the enemies to rapidly switch directions when the side lengths were about the same, since the larger side
                  would flip every step. I fixed this by adding a condition where if the difference between the side lengths is less than a certain
                  number, the enemy will continue moving in the same direction they previously were. This looks much cleaner for a difference of at least 24.

          Update: Getting the enemies to stop at the player in a realistic looking way was challenging. They would experience the same glitchy rapid movement
                  when I made them follow me a certain way (having them be in the corner of my hitbox and going in some direction). I finally was able to add
                  an offset to the distance at which the movement method changed. This fixed the glitchy behavior for large enough offsets, but I still need
                  to optimize their values to make it look like the enemy is close enough to actually attack the player (no large spaces which make it look
                  unrealistic).
        '''
        
        dist, Dx, Dy = self.distanceFromPlayer() # Dx, Dy are vectors from player to enemy (i.e. enemy pos - player pos)

        if max(abs(Dx), abs(Dy)) == abs(Dx):
            path = 'horizontal'
        else:
            path = 'vertical'
        
        if abs(abs(Dx) - abs(Dy)) < 24: #or dist < np.sqrt((man.width/2 + self.widths[0]/2 + 20)**2 + (man.height/2 + self.heights[2] + 20)**2):
            path = prevPath

        if path == 'horizontal':

            if Dx > (man.width/2) + (self.widths[0]/2) - self.offset1: # Player to the left, so enemy moves left
                if self.x > self.containmentArea[0]:
                    '''
                    Add here if statement about whether the hitboxes are colliding.
                    '''
                    self.x -= self.vel
                    self.left = True
                    self.right = False
                    self.up = False
                    self.down = False
                    self.stand = False
                else:
                    self.stand = True
                    self.walkCount = 0
                    self.attackLoop = False

            elif Dx < -((man.width/2) + (self.widths[1]/2) - self.offset1): # Player to the right, so enemy moves right
                if self.x + self.widths[1] < self.containmentArea[0] + self.containmentArea[2]:
                    '''
                    Add here if statement about whether the hitboxes are colliding.
                    '''
                    self.x += self.vel
                    self.left = False
                    self.right = True
                    self.up = False
                    self.down = False
                    self.stand = False
                else:
                    self.stand = True
                    self.walkCount = 0
                    self.attackLoop = False

            elif Dx >= 0 and Dx <= (man.width/2) + (self.widths[0]/2): # Player to the left, but close. Attack once this close

                if Dy > (man.height/2) + (self.heights[0]/2) + self.offset2 or Dy < -((man.height/2) + (self.heights[0]/2) - self.offset3):
                    path = 'vertical'
                else:
                    self.left = True
                    self.right = False
                    self.up = False
                    self.down = False
                    self.stand = True
                    self.walkCount = 0
                
            elif Dx < 0 and Dx >= -((man.width/2) + (self.widths[1]/2)): # Player to the right, but close. Attack once this close

                if Dy > (man.height/2) + (self.heights[1]/2) + self.offset2 or Dy < -((man.height/2) + (self.heights[1]/2) - self.offset3):
                    path = 'vertical'
                else:
                    self.left = False
                    self.right = True
                    self.up = False
                    self.down = False
                    self.stand = True
                    self.walkCount = 0

        else: # if path = 'vertical':

            if Dy > (man.height/2) + (self.heights[2]/2) - self.offset1: # Player above, so enemy moves up
                if self.y > self.containmentArea[1]:
                    '''
                    Add here if statement about whether the hitboxes are colliding.
                    '''
                    self.y -= self.vel
                    self.left = False
                    self.right = False
                    self.up = True
                    self.down = False
                    self.stand = False

                else:
                    self.stand = True
                    self.walkCount = 0
                    self.attackLoop = False

            elif Dy < -((man.height/2) + (self.heights[3]/2) - self.offset1): # Player below, so enemy moves down
                if self.y + self.heights[3] < self.containmentArea[1] + self.containmentArea[3]:
                    '''
                    Add here if statement about whether the hitboxes are colliding.
                    '''
                    self.y += self.vel
                    self.left = False
                    self.right = False
                    self.up = False
                    self.down = True
                    self.stand = False

                else:
                    self.stand = True
                    self.walkCount = 0
                    self.attackLoop = False

            elif Dy >= 0 and Dy <= (man.height/2) + (self.heights[2]/2): # Player above, but close. Attack once this close

                if Dx >= (man.width/2) + (self.widths[2]/2) + self.offset2 or Dx <= -((man.width/2) + (self.widths[2]/2) + self.offset2):
                    path = 'horizontal'
                else:
                    self.left = False
                    self.right = False
                    self.up = True
                    self.down = False
                    self.stand = True
                    self.walkCount = 0

            elif Dy < 0 and Dy >= -((man.height/2) + (self.heights[3]/2)): # Player below, but close. Attack once this close

                if Dx >= (man.width/2) + (self.widths[3]/2) + self.offset2 or Dx <= -((man.width/2) + (self.widths[3]/2) + self.offset2):
                    path = 'horizontal'
                else:
                    self.left = False
                    self.right = False
                    self.up = False
                    self.down = True
                    self.stand = True
                    self.walkCount = 0

        '''
        I want the enemy to attack the player immediately when it is within distance the first time. Then as they are close together, there should be
        a delay between subsequent attacks (2 seconds for example). But if the player chooses to run away, then come back and fight, the attack should
        be immediate again. This needs to have its own delay though, since the player could just inch away slowly and the enemy would immediately attack
        each time causing health to drop too fast.

        Update: Right now there is an initial attack and then an inevitable attack after 2 seconds, no matter how far away the player is at that time.
                It works very well otherwise. I'd like there to be a condition where if the player is far enough away at the end of the 2 seconds,
                there is no attack. (FIXED with dist < np.sqrt(....))

        Update: There is a bug where if the enemy attacks the player initially, then the player runs away but comes back in exactly 2 seconds, the
                initialAttack value will fluctuate between True and False every game loop, and the enemy attacks every loop. This happens because the
                initAttackCoolDown method is called on a delay multiple times at once. When 2 seconds have passed and those multiple calls are being executed,
                the loop that makes initialAttack False competes with the method that makes it True. (FIXED with self.initSwitch)
        '''

        if self.stand: # If close enough to no longer chase the player, the enemy can attack
            if not self.damageLoop:
                
                if self.initialAttack: # Attack initially the instant the enemy gets close enough.
                    self.attack()
                    self.initialAttack = False
                else:
                    Timer(2, self.attack).start() # Calls the function in 2 seconds.
                    
                self.damageLoop = not self.damageLoop # Acts as a switch to turn off calling the attack function until 2 seconds have passed.
        else:
            if not self.initialAttack:
                if self.initSwitch:
                    Timer(2, self.initAttackCoolDown).start()
                    self.initSwitch = False # Prevents repeated calling of initAttackCoolDown

        return path

    def initAttackCoolDown(self):
        
        self.initialAttack = True
        self.initSwitch = True

    def attack(self):

        dist, Dx, Dy = self.distanceFromPlayer()
        if dist < np.sqrt(((man.width/2) + (self.widths[0]/2) + 50)**2 + ((man.height/2) + (self.heights[0]/2) + 50)**2):

            if man.health > 0:
                man.health -= self.base_dmg
                man.health = max(0, man.health)

        self.damageLoop = not self.damageLoop

    def move(self):
  
        if self.loopCount == 0:
            self.direction = np.random.rand() # random number between 0 and 1
        if self.loopCount < self.loopReset:
        
            if self.direction <= 0.2:
                self.stand = True
                self.walkCount = 0

            elif self.direction > 0.2 and self.direction <= 0.4: # left
                if self.x > self.containmentArea[0]:
                    self.x -= self.vel
                    self.left = True
                    self.right = False
                    self.up = False
                    self.down = False
                    self.stand = False
                else:
                    self.stand = True
                    self.walkCount = 0

            elif self.direction > 0.4 and self.direction <= 0.6: # right
                if self.x + self.widths[1] < self.containmentArea[0] + self.containmentArea[2]:
                    self.x += self.vel
                    self.left = False
                    self.right = True
                    self.up = False
                    self.down = False
                    self.stand = False
                else:
                    self.stand = True
                    self.walkCount = 0

            elif self.direction > 0.6 and self.direction <= 0.8: # up
                if self.y > self.containmentArea[1]:
                    self.y -= self.vel
                    self.left = False
                    self.right = False
                    self.up = True
                    self.down = False
                    self.stand = False
                else:
                    self.stand = True
                    self.walkCount = 0

            elif self.direction > 0.8: # down
                if self.y + self.heights[3] < self.containmentArea[1] + self.containmentArea[3]:
                    self.y += self.vel
                    self.left = False
                    self.right = False
                    self.up = False
                    self.down = True
                    self.stand = False
                else:
                    self.stand = True
                    self.walkCount = 0

        self.loopCount += 1
                    
        if self.loopCount >= self.loopReset:
            self.loopCount = 0

    def draw(self, win):

        if not self.attackLoop:
            self.move()
        else:
            self.path = self.chase(self.path)
        
        if self.walkCount + 1 >= self.enemy_fps:
            self.walkCount = 0

        if self.left:
            if self.stand:
                win.blit(self.walkLeft_sprites[1], (self.x,self.y))
            else:
                win.blit(self.walkLeft_sprites[self.walkCount//(self.enemy_fps//self.numEnemySprites)], (self.x,self.y))
                self.walkCount += 1
        elif self.right:
            if self.stand:
                win.blit(self.walkRight_sprites[1], (self.x,self.y))
            else:
                win.blit(self.walkRight_sprites[self.walkCount//(self.enemy_fps//self.numEnemySprites)], (self.x,self.y))
                self.walkCount += 1        
        elif self.up:
            if self.stand:
                win.blit(self.walkUp_sprites[1], (self.x,self.y))
            else:
                win.blit(self.walkUp_sprites[self.walkCount//(self.enemy_fps//self.numEnemySprites)], (self.x,self.y))
                self.walkCount += 1
        elif self.down:
            if self.stand:
                win.blit(self.walkDown_sprites[1], (self.x,self.y))
            else:
                win.blit(self.walkDown_sprites[self.walkCount//(self.enemy_fps//self.numEnemySprites)], (self.x,self.y))
                self.walkCount += 1   
        elif self.stand:
            win.blit(self.walkDown_sprites[1], (self.x,self.y))

        #############################################
        # Hitbox
        
        if self.left:
            self.hitbox = (self.x, self.y, self.widths[0], self.heights[0])
        elif self.right:
            self.hitbox = (self.x, self.y, self.widths[1], self.heights[1])
        elif self.up:
            self.hitbox = (self.x, self.y, self.widths[2], self.heights[2])
        elif self.down:
            self.hitbox = (self.x, self.y, self.widths[3], self.heights[3])
        else:
            self.hitbox = (self.x, self.y, self.widths[3], self.heights[3])

        if not self.highlighted:
            pygame.draw.rect(win, (255,0,0), self.hitbox, 2)
        else:
            pygame.draw.rect(win, (0,0,255), self.hitbox, 2) # Blue if highlighted

        #############################################
        # Containment Area Box

        pygame.draw.rect(win, (255,0,0), self.containmentArea, 2)

        #############################################
        # Health Bar

        if self.highlighted:
            
            pygame.draw.rect(win, (200, 0, 0), (self.x - 30, self.y - 30, self.health_bar_width, self.health_bar_height))
            if self.health > 0:
                pygame.draw.rect(win, (0,200,0), (self.x - 30, self.y - 30, int(self.health_bar_width * (self.health / self.max_health)), self.health_bar_height))
                
            healthText = smallFont.render(str(int(100 * self.health / self.max_health)) + '%', 1, (0, 0, 0))
            healthText_rect = healthText.get_rect(center=(self.x - 30 + (self.health_bar_width)/2, self.y - 30 + (self.health_bar_height)/2))
            win.blit(healthText, healthText_rect)

    @classmethod
    def moveWithBackground(cls):

        for obj in cls.objs: # For each instance of the enemy class object...
            if man.left:
                obj.x += man.vel
                obj.containmentArea[0] += man.vel
            elif man.right:
                obj.x -= man.vel
                obj.containmentArea[0] -= man.vel
            elif man.up:
                obj.y += man.vel
                obj.containmentArea[1] += man.vel
            elif man.down:
                obj.y -= man.vel
                obj.containmentArea[1] -= man.vel

    @classmethod
    def drawAll(cls):

        for obj in cls.objs: # For each instance of the enemy class object...
            obj.draw(win)

    @classmethod
    def getHitboxes(cls): # Gets a list of all the enemy hitboxes [(10, 10 10, 10), (20, 20, 20, 20), etc.]

        hitboxes = []
        for obj in cls.objs: # For each instance of the enemy class object...
            hitboxes.append(obj.hitbox)

        return hitboxes

    @classmethod
    def highlightEnemy(cls, index): #If enemy is highlighted, it is represented on-screen. For now the hitbox just turns blue from enemy.draw()

        #if not cls.any_highlighted:
        
        enemy.unHighlightAll()

        rel_obj = cls.objs[index]
        rel_obj.highlighted = True # Highlight the relevant enemy (clicked on or closest to player after pressing tab)

    @classmethod
    def unHighlightAll(cls):

        for obj in cls.objs:
            obj.highlighted = False

    @classmethod
    def whichHighlighted(cls):

        for obj in cls.objs:
            if obj.highlighted == True:
                rel_obj = obj
                return rel_obj

            else:
                pass

    @classmethod
    def distancesFromPlayer(cls):

        distances = []
        for obj in cls.objs:
            center_x_enemy = obj.x + (obj.hitbox[2]/2)
            center_y_enemy = obj.y + (obj.hitbox[3]/2)
            center_x_player = man.x + (man.width/2)
            center_y_player = man.y + (man.height/2)

            dist = np.sqrt((center_x_enemy - center_x_player)**2 + (center_y_enemy - center_y_player)**2)
            distances.append(dist)

        return distances

    def distanceFromPlayer(self):

        center_x_enemy = self.x + (self.hitbox[2]/2)
        center_y_enemy = self.y + (self.hitbox[3]/2)
        center_x_player = man.x + (man.width/2)
        center_y_player = man.y + (man.height/2)

        x_PlayerToEnemy = center_x_enemy - center_x_player
        y_PlayerToEnemy = center_y_enemy - center_y_player
        dist = np.sqrt(x_PlayerToEnemy**2 + y_PlayerToEnemy**2)

        return dist, x_PlayerToEnemy, y_PlayerToEnemy
            
############################################################

class logDisplay(object):

    def __init__(self):

        self.lineCount = 0
        self.upCount = 0
        self.logHistoryList = []
        self.logDisplayList = []
        self.log_rect = pygame.Rect((22, screenHeight - 242, 475, 214))

    def logStore(self, string_list):

        for string in string_list:
            if self.upCount == 0:
                self.logDisplayList.insert(0, string) # insert at beginning instead of the end
            elif self.upCount > 0:
                self.upCount += 1
            self.logHistoryList.insert(0, string)
                
        self.lineCount += len(string_list)

        while self.lineCount > 7:
            if self.upCount == 0:
                del self.logDisplayList[-1] # Delete the oldest line in the log. It can only hold 7 lines.
            self.lineCount -= 1

    def logClear(self):
    
        self.lineCount = 0
        self.upCount = 0
        self.logDisplayList = []
        self.logHistoryList = []
       
    def updateLogDisplay(self, string_list): # log book displays items picked up and gold obtained, levels up etc.

        text_x = 30 # bottomleft coords of the first line
        text_y = screenHeight - 35 
        text_sep = 30 # seperation between lines
        mult = 0
        for string in string_list:
            logText = logFont.render(string, 1, (255, 255, 255))
            logText_rect = logText.get_rect(bottomleft=(text_x, text_y - (mult * text_sep)))
            win.blit(logText, logText_rect)
            mult += 1

        if self.upCount > 0:
            pygame.draw.polygon(win, (255, 255, 255), ((479, 845), (479, 855), (474, 855), (481.5, 860), (489, 855), (484, 855), (484, 845))) # Down arrow

    def logScroll(self, wheel_up):

        if self.lineCount == 7:
            if wheel_up and self.logDisplayList != self.logHistoryList[-7:]: # Top of history boundary condition
                self.upCount += 1 # How many lines we are above most recent line.
                self.logDisplayList = self.logHistoryList[self.upCount:self.upCount + 7]
                
            elif not wheel_up and self.logDisplayList != self.logHistoryList[0:7]: # Bottom of log boundary condition
                self.upCount -= 1
                self.logDisplayList = self.logHistoryList[self.upCount:self.upCount + 7]

############################################################

class background(object):

    def __init__(self):

        self.x = -7200 # Coords of topleft part of 1st chunk relative to topleft of initial screen location.
        self.y = -2240 # These are updated based on player movement.
        self.chunkCoords = []

    def locateChunks(self, image_list):

        width = 1600
        height = 896
        x_step = 0
        y_step = 0
        t = 0
        self.chunkCoords = [] # Coords of topleft points for all 64 chunks
        for image in range(len(image_list)):
            self.chunkCoords.append((self.x + (x_step * width), self.y + (y_step * height)))
            x_step += 1
            if t==8-1 or t==16-1 or t==24-1 or t==32-1 or t==40-1 or t==48-1 or t==56-1 or t==64-1:
                x_step = 0
                y_step += 1
            t += 1

    def updateBackground(self, image_list):

        self.locateChunks(image_list)
        t = 0
        for chunk in image_list:
            win.blit(chunk, self.chunkCoords[t])
            t += 1

    def moveBackground(self):

        if man.left:
            self.x += man.vel
        elif man.right:
            self.x -= man.vel
        elif man.up:
            self.y += man.vel
        elif man.down:
            self.y -= man.vel 

############################################################

def redrawGameWindow(logLoop):

    bg.updateBackground(map_list)
    enemy.drawAll()
    man.draw(win)
    if logLoop:
        win.blit(logSurface, (22, screenHeight - 242)) # 475 x 214. Bottomright corner is 497, 868.
        log.updateLogDisplay(log.logDisplayList)
    pygame.display.update()

############################################################

bg = background()
log = logDisplay()

bunny = enemy((screenWidth//2) + 200, (screenHeight//2) + 200, [29, 29, 19, 19], [24, 24, 32, 25], 4, [screenWidth//2, screenHeight//2, 400, 400], 5, True, 0)
bunny.loadSprites_12('bunny')

bear = enemy((screenWidth//2) + 400, (screenHeight//2) + 400, [80, 80, 50, 53], [55, 55, 80, 80], 4, [0, 0, screenWidth, screenHeight], 100, True, 1)
bear.loadSprites_12('bear')

boar = enemy((screenWidth//2) + 400, (screenHeight//2) + 400, [60, 60, 32, 37], [41, 41, 60, 60], 4, [0, 0, screenWidth, screenHeight], 50, True, 1)
boar.loadSprites_12('boar')

wolf = enemy((screenWidth//2) + 400, (screenHeight//2) + 400, [64, 64, 31, 34], [42, 42, 64, 64], 4, [0, 0, screenWidth, screenHeight], 75, True, 1)
wolf.loadSprites_12('wolf')

turtle = enemy((screenWidth//2) + 200, (screenHeight//2) + 200, [50, 50, 36, 41], [32, 32, 50, 50], 4, [screenWidth//2, screenHeight//2, 400, 400], 50, True, 2)
turtle.loadSprites_12('turtle')

crab = enemy((screenWidth//2) + 200, (screenHeight//2) + 200, [36, 36, 41, 41], [27, 27, 20, 31], 4, [screenWidth//2, screenHeight//2, 400, 400], 50, True, 2)
crab.loadSprites_12('crab')

expThreshold = []
for i in range(50):
    expThreshold.append((i*10)**2)

skillExpThreshold = []
for i in range(50):
    skillExpThreshold.append((i*5)**2)

menuRun = True
classRun = True
run = True
logLoop = False

############################################################
# MAIN MENU

win.fill((0,0,0))

titleFont = pygame.font.SysFont('arial', 64, bold=True)
menuFont = pygame.font.SysFont('arial', 28)
classFont = pygame.font.SysFont('arial', 32, bold=True)
logFont = pygame.font.SysFont('arial', 16)
smallFont = pygame.font.SysFont('arial', 8)

titleText = titleFont.render('My First Game', 1, (255, 255, 255))
titleText_rect = titleText.get_rect(center=(screenWidth/2, screenHeight//6))
enterText = menuFont.render('Press Enter', 1, (255, 255, 255))
enterText_rect = enterText.get_rect(center=(screenWidth/2, screenHeight//1.1))
win.blit(titleText, titleText_rect)
win.blit(enterText, enterText_rect)

pygame.display.update()

while menuRun:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            menuRun = False
            classRun = False
            run = False
              
    menu_keys = pygame.key.get_pressed()

    if menu_keys[pygame.K_RETURN]:
        menuRun = False

    if menu_keys[pygame.K_ESCAPE]:
        menuRun = False
        classRun = False
        run = False

############################################################
# CREATE CLASS MENU

win.fill((0,0,0))
classText = titleFont.render('Choose a Class:', 1, (255, 255, 255))
classText_rect = classText.get_rect(center=(screenWidth//6, screenHeight//8))
win.blit(classText, classText_rect)
warrText = classFont.render('1.)   Warrior', 1, (255, 255, 255))
warrText2 = menuFont.render('Tank specialist and melee combat.', 1, (255, 255, 255))
win.blit(warrText, (screenWidth//6, (screenHeight//8) + 100))
win.blit(warrText2, ((screenWidth//6) + 200, (screenHeight//8) + 100))
rogueText = classFont.render('2.)   Rogue', 1, (255, 255, 255))
rogueText2 = menuFont.render('Stealth specialist and melee combat.', 1, (255, 255, 255))
win.blit(rogueText, (screenWidth//6, (screenHeight//8) + 220))
win.blit(rogueText2, ((screenWidth//6) + 200, (screenHeight//8) + 220))
predText = classFont.render('3.)   Predator', 1, (255, 255, 255))
predText2 = menuFont.render('Ranged bow specialist. Can tame beasts.', 1, (255, 255, 255))
win.blit(predText, (screenWidth//6, (screenHeight//8) + 340))
win.blit(predText2, ((screenWidth//6) + 200, (screenHeight//8) + 340))
mystText = classFont.render('4.)   Mystic', 1, (255, 255, 255))
mystText2 = menuFont.render('Elemental magic damage specialist. Casts spells dealing instant damage.', 1, (255, 255, 255))
win.blit(mystText, (screenWidth//6, (screenHeight//8) + 460))
win.blit(mystText2, ((screenWidth//6) + 200, (screenHeight//8) + 460))
cultText = classFont.render('5.)   Cultist', 1, (255, 255, 255))
cultText2 = menuFont.render('Dark magic damage specialist. Casts damage over time spells.', 1, (255, 255, 255))
win.blit(cultText, (screenWidth//6, (screenHeight//8) + 580))
win.blit(cultText2, ((screenWidth//6) + 200, (screenHeight//8) + 580))
priestText = classFont.render('6.)   Priest', 1, (255, 255, 255))
priestText2 = menuFont.render('Divine magic damage and healing specialist.', 1, (255, 255, 255))
win.blit(priestText, (screenWidth//6, (screenHeight//8) + 700))
win.blit(priestText2, ((screenWidth//6) + 200, (screenHeight//8) + 700))
pygame.display.update()

while classRun:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            classRun = False
            run = False

    class_keys = pygame.key.get_pressed()

    if class_keys[pygame.K_1]:
        pygame.time.delay(60)
        classRun = False
        abilities = ['Health Regeneration', 'Stamina Regeneration', 'Teleport', 'Base Attack', 'Harden']
        man = player(screenWidth//2, screenHeight//2, 64, 64, 1, 'Warrior', 100, 30, -1, abilities, 10) 

    if class_keys[pygame.K_2]:
        pygame.time.delay(60)
        classRun = False
        abilities = ['Health Regeneration', 'Stamina Regeneration', 'Teleport', 'Base Attack', 'Puncture']
        man = player(screenWidth//2, screenHeight//2, 64, 64, 2, 'Rogue', 80, 50, -1, abilities, 14)

    if class_keys[pygame.K_3]:
        pygame.time.delay(60)
        classRun = False
        abilities = ['Health Regeneration', 'Stamina Regeneration', 'Teleport', 'Base Attack', 'Kick']
        man = player(screenWidth//2, screenHeight//2, 64, 64, 3, 'Predator', 85, 40, -1, abilities, 12)
        
    if class_keys[pygame.K_4]:
        pygame.time.delay(60)
        classRun = False
        abilities = ['Health Regeneration', 'Mana Regeneration', 'Teleport', 'Base Attack', 'Elemental Call']
        man = player(screenWidth//2, screenHeight//2, 64, 64, 4, 'Mystic', 70, -1, 90, abilities, 12)
        
    if class_keys[pygame.K_5]:
        pygame.time.delay(60)
        classRun = False
        abilities = ['Health Regeneration', 'Mana Regeneration', 'Teleport', 'Base Attack', 'Curse']
        man = player(screenWidth//2, screenHeight//2, 64, 64, 5, 'Cultist', 70, -1, 90, abilities, 8)
        
    if class_keys[pygame.K_6]:
        pygame.time.delay(60)
        classRun = False
        abilities = ['Health Regeneration', 'Mana Regeneration', 'Teleport', 'Base Attack', 'Flash of Light']
        man = player(screenWidth//2, screenHeight//2, 64, 64, 6, 'Priest', 65, -1, 100, abilities, 8)
        
    if class_keys[pygame.K_ESCAPE]:
        classRun = False
        run = False    

############################################################
# MAIN CODE

while run:

    clock.tick(fps)

    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            
            mouse_pos = pygame.mouse.get_pos()
            
            if event.button == 4: # Mouse wheel up
                if logLoop and log.log_rect.collidepoint(mouse_pos):
                    log.logScroll(wheel_up = True)
            elif event.button == 5: # Mouse wheel down
                if logLoop and log.log_rect.collidepoint(mouse_pos):
                    log.logScroll(wheel_up = False)
                    
            else:
                hitboxes = enemy.getHitboxes()
                for hitbox in hitboxes:

                    hitbox_rect = pygame.Rect(hitbox)
                    if hitbox_rect.collidepoint(mouse_pos):
                        
                        enemy.highlightEnemy(hitboxes.index(hitbox))
                        enemy.any_highlighted = True

                    else:
                        enemy.unHighlightAll()
                        enemy.any_hightlighted = False
                    
    keys = pygame.key.get_pressed()

    '''
    To simulate the player moving, the background moves behind them.
    If the player walks left, the background actually moves right, etc.
    '''
    if keys[pygame.K_a] and man.x > bg.chunkCoords[0][0] + man.width: #left
        man.left = True
        man.right = False
        man.up = False
        man.down = False
        man.stand = False
        
    elif keys[pygame.K_d] and man.x < bg.chunkCoords[8-1][0] + screenWidth - (2 * man.width): #right
        man.left = False
        man.right = True
        man.up = False
        man.down = False
        man.stand = False
        
    elif keys[pygame.K_w] and man.y > bg.chunkCoords[8-1][1]: #up
        man.left = False
        man.right = False
        man.up = True
        man.down = False
        man.stand = False
        
    elif keys[pygame.K_s] and man.y < bg.chunkCoords[64-1][1] + screenHeight - (int(man.height * 1.5)): #down
        man.left = False
        man.right = False
        man.up = False
        man.down = True
        man.stand = False

    else:
        man.stand = True
        man.walkCount = 0

    if not man.stand:
        bg.moveBackground()
        enemy.moveWithBackground()
    
    distances = enemy.distancesFromPlayer()
    for dist in distances:
        obj = enemy.objs[distances.index(dist)]
        if dist <= obj.aggro_dist and obj.threat == 1 and not obj.attackLoop:
            obj.attackLoop = True
            if not enemy.any_highlighted:
                obj.highlightEnemy(distances.index(dist))
                enemy.any_highlighted = True
    
    if keys[pygame.K_TAB]: # If it is on-screen, determine which enemy is closest and highlight the enemy (e.g. make hitbox blue)

        min_obj = enemy.objs[distances.index(min(distances))]

        if min_obj.x <= screenWidth and min_obj.x >= 0 and min_obj.y <= screenHeight and min_obj.y >= 0:
            pygame.time.delay(5)
            enemy.highlightEnemy(distances.index(min(distances)))
            enemy.any_highlighted = True
        
    if keys[pygame.K_ESCAPE]:
        run = False

    #################### Hotkeys 1,2,3,4,5,6,7,8,9,0 ########################

    if keys[pygame.K_1]:
        pygame.time.delay(5)
        man.pressed(1)

    if keys[pygame.K_2]:
        pygame.time.delay(5)
        man.pressed(2)

    if keys[pygame.K_3]:
        pygame.time.delay(5)
        man.pressed(3)

    if keys[pygame.K_4]:
        pygame.time.delay(5)
        man.pressed(4)

    if keys[pygame.K_5]:
        pygame.time.delay(5)
        man.pressed(5)

    if keys[pygame.K_6]:
        pygame.time.delay(5)
        man.pressed(6)

    if keys[pygame.K_7]:
        pygame.time.delay(5)
        man.pressed(7)

    if keys[pygame.K_8]:
        pygame.time.delay(5)
        man.pressed(8)

    if keys[pygame.K_9]:
        pygame.time.delay(5)
        man.pressed(9)

    if keys[pygame.K_0]:
        pygame.time.delay(5)
        man.pressed(0)

    if keys[pygame.K_g]: # g = get gold
        pygame.time.delay(60)
        man.gainGold(10)

    if keys[pygame.K_i]: # i = pick up item
        pygame.time.delay(60)
        man.gainItem('Iron Short Sword')

    if keys[pygame.K_e]: # e = get exp
        pygame.time.delay(60)
        man.gainExp(40, expThreshold)

    if keys[pygame.K_f]:
        pygame.time.delay(60)
        man.fishing_exp, man.fishing_level, man.max_fishing_status = man.gainSkillExp(1000, 'Fishing', skillExpThreshold)

    if keys[pygame.K_t]:
        pygame.time.delay(60)
        if man.health > 0:
            man.health -= 5
            man.health = max(0, man.health)

    if keys[pygame.K_y]:
        pygame.time.delay(60)
        if man.class_index == 1 or man.class_index == 2 or man.class_index == 3:
            if man.stamina > 0:
                man.stamina -= 5
                man.stamina = max(0, man.stamina)
        else:
            if man.mana > 0:
                man.mana -= 5
                man.mana = max(0, man.mana)

    if keys[pygame.K_l]: # l = open log book
        pygame.time.delay(60)
        if not logLoop:
            logLoop = True
        else:
            logLoop = False

    if keys[pygame.K_c]:
        if logLoop:
            pygame.time.delay(60)
            log.logClear()

    redrawGameWindow(logLoop)
    
pygame.quit()
