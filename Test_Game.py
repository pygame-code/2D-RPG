'''
Test_Game using pygame module. Use idle under D:\Anaconda\Scripts\idle
'''

import pygame
pygame.init()

screenWidth = 1600 # Full screen dimensions.
screenHeight = 896 # Make sure these are divisible by player width and height.

win = pygame.display.set_mode((screenWidth,screenHeight), pygame.FULLSCREEN)

pygame.display.set_caption("My First Game")

walkRight = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png'), pygame.image.load('R4.png')]
walkLeft = [pygame.image.load('L1.png'), pygame.image.load('L2.png'), pygame.image.load('L3.png'), pygame.image.load('L4.png')] 
walkUp = [pygame.image.load('B1.png'), pygame.image.load('B2.png'), pygame.image.load('B3.png'), pygame.image.load('B4.png')]
walkDown = [pygame.image.load('F1.png'), pygame.image.load('F2.png'), pygame.image.load('F3.png'), pygame.image.load('F4.png')]
logSurface = pygame.image.load('logSurface.png') # 800 x 750

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
    
    def __init__(self, x, y, width, height, class_index, player_class, health, stamina, mana, abilities):
        
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

        #self.hitbox = (self.x + 17, self.y + 2, 31, 57) # Have to update hitbox location. Also, needs to be better.
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

############################################################

class logDisplay(object):

    def __init__(self):

        self.logCount = 0
        self.logDisplayList = []

    def logStore(self, string_list):

        for string in string_list:
            self.logDisplayList.insert(0, string) # insert at beginning instead of the end
        self.logCount += len(string_list)

        while self.logCount > 7:
            del self.logDisplayList[-1]
            self.logCount -= 1

    def logClear(self):
    
        self.logCount = 0
        self.logDisplayList = []
       
    def updateLogDisplay(self, string_list): # log book displays items picked up and gold obtained, levels up etc.

        text_x = 30 # bottomleft coords of the first line
        text_y = screenHeight - 35 
        text_sep = 30 # seperation between lines
        mult = 0
        for string in string_list: # Up to 7 lines fit on the log
            logText = logFont.render(string, 1, (255, 255, 255))
            logText_rect = logText.get_rect(bottomleft=(text_x, text_y - (mult * text_sep)))
            win.blit(logText, logText_rect)
            mult += 1    

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

############################################################

def redrawGameWindow(logLoop):

    bg.updateBackground(map_list)
    man.draw(win)
    if logLoop:
        win.blit(logSurface, (-140, screenHeight - 510)) # log not transparent, saves fps
        log.updateLogDisplay(log.logDisplayList)
    pygame.display.update()

############################################################

bg = background()
log = logDisplay()

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
        classRun = False
        abilities = ['Health Regeneration', 'Stamina Regeneration', 'Teleport', 'Base Attack', 'Harden']
        man = player(screenWidth//2, screenHeight//2, 64, 64, 1, 'Warrior', 100, 30, -1, abilities) 

    if class_keys[pygame.K_2]:
        classRun = False
        abilities = ['Health Regeneration', 'Stamina Regeneration', 'Teleport', 'Base Attack', 'Puncture']
        man = player(screenWidth//2, screenHeight//2, 64, 64, 2, 'Rogue', 80, 50, -1, abilities)

    if class_keys[pygame.K_3]:
        classRun = False
        abilities = ['Health Regeneration', 'Stamina Regeneration', 'Teleport', 'Base Attack', 'Kick']
        man = player(screenWidth//2, screenHeight//2, 64, 64, 3, 'Predator', 85, 40, -1, abilities)
        
    if class_keys[pygame.K_4]:
        classRun = False
        abilities = ['Health Regeneration', 'Mana Regeneration', 'Teleport', 'Base Attack', 'Elemental Call']
        man = player(screenWidth//2, screenHeight//2, 64, 64, 4, 'Mystic', 70, -1, 90, abilities)
        
    if class_keys[pygame.K_5]:
        classRun = False
        abilities = ['Health Regeneration', 'Mana Regeneration', 'Teleport', 'Base Attack', 'Curse']
        man = player(screenWidth//2, screenHeight//2, 64, 64, 5, 'Cultist', 70, -1, 90, abilities)
        
    if class_keys[pygame.K_6]:
        classRun = False
        abilities = ['Health Regeneration', 'Mana Regeneration', 'Teleport', 'Base Attack', 'Flash of Light']
        man = player(screenWidth//2, screenHeight//2, 64, 64, 6, 'Priest', 65, -1, 100, abilities)
        
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

    keys = pygame.key.get_pressed()

    '''
    To simulate the player moving, the background moves behind them.
    If the player walks left, the background actually moves right, etc.
    '''
    if keys[pygame.K_a] and man.x > bg.chunkCoords[0][0] + man.width: #left
        bg.x += man.vel     
        man.left = True
        man.right = False
        man.up = False
        man.down = False
        man.stand = False
        
    elif keys[pygame.K_d] and man.x < bg.chunkCoords[8-1][0] + screenWidth - (2 * man.width): #right
        bg.x -= man.vel
        man.left = False
        man.right = True
        man.up = False
        man.down = False
        man.stand = False
        
    elif keys[pygame.K_w] and man.y > bg.chunkCoords[8-1][1]: #up
        bg.y += man.vel
        man.left = False
        man.right = False
        man.up = True
        man.down = False
        man.stand = False
        
    elif keys[pygame.K_s] and man.y < bg.chunkCoords[64-1][1] + screenHeight - (int(man.height * 1.5)): #down
        bg.y -= man.vel
        man.left = False
        man.right = False
        man.up = False
        man.down = True
        man.stand = False

    else:
        man.stand = True     
        man.walkCount = 0

    if keys[pygame.K_ESCAPE]:
        run = False

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
