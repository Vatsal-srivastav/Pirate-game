import zipfile
import math
import pygame
import io
SCREEN_WIDTH = 1800
SCREEN_HEIGHT = 800
BUTTON_WIDTH = 150
BUTTON_HEIGHT = 50+50//3
BUTTON_PADDING = 10
NUM_ROWS = 3
NUM_COLS = 5
BUTTON_COLOR = (255, 255, 0)
FONT_COLOR = (0,0,0)
FONT_SIZE = 65
SEA_COLOR = (0, 158, 255)
IS_DRAWING=False
IS_DRAWN=False
delay=0
deadboats=[]       

def check_collisions(pirates):
     for i in pirates:
           for pirate in pirates:       
            overlapx=0
            overlapy=0
            if i.rect.colliderect(pirate.rect):
                if (i.rect.right>pirate.rect.left ) and (i.rect.right<pirate.rect.right):
                    overlapx=-(i.rect.right-pirate.rect.left)
                if (i.rect.left<pirate.rect.right ) and (i.rect.left>pirate.rect.right):
                    overlapx=i.rect.left-pirate.rect.right
                if (i.rect.top<pirate.rect.bottom ) and (i.rect.top>pirate.rect.top):
                    overlapy=pirate.rect.bottom-i.rect.top
                if (i.rect.bottom>pirate.rect.top ) and (i.rect.top>pirate.rect.bottom):
                    overlapx=-(i.rect.bottom-pirate.rect.top)
                i.rect.move_ip(overlapx,overlapy)
                i.x+=overlapx
                i.y+=overlapy

     
def checkboatcollisions(i,pirates,screen,lvl):
           dead=[]
           for pirate in pirates:
               x=pirate.rect.centerx-pirate.rect.width//2
               y=pirate.rect.centery-pirate.rect.height//2
               pirate.rect=pygame.Rect(x+38, y+63,pirate.rect.width-75,pirate.rect.height-125)
               if pirate.rect.colliderect(i.rect):
                     dead.append(pirate)
                     if pirate.grade==1: 
                       if 3>=lvl:  
                         i.health-=35
                       else:  
                         i.health-=50
                     if pirate.grade==2: 
                       if 3>=lvl:  
                         i.health-=50
                       else:  
                         i.health-=75                             
                     if i.health<=0:
                         return False
                            
           for pirate in dead:
               pirate.timer=60
               pirates.remove(pirate)
               
           drawdeatheffect(dead,screen)
                 
           return True      
           
def check_islandcollision(i,pirates):
         for pirate in pirates:              
            if i.rect.colliderect(pirate.rect):
                return False
            return True    

def checkwinner(i,b):
      if b.rect.colliderect(i.rect):
                return False
      return True     
                   

def drawdeatheffect(dead,screen):
    deadboats.extend(dead)
    for pirate in deadboats:
        pirate.image=pirate.image.convert_alpha()
        pirate.image.set_colorkey(pirate.colorkey)
        pirate.image.fill((255, 0, 0),special_flags=pygame.BLEND_RGBA_MULT)         
        pirate.rect=pirate.image.get_bounding_rect() 
        pirate.rect.center=(pirate.x,pirate.y)
        screen.blit(pirate.image,pirate.rect)
        pirate.timer-=1
        if pirate.timer<=0:
            deadboats.remove(pirate)

class Pirate:
    def __init__(self, x, y,path,speed=4):
        self.grade=1
        self.path=path
        self.nextpos=0
        self.angle=0
        self.x=x
        self.y=y
        with zipfile.ZipFile('images.zip') as zf:
            with zf.open('pirate_ship.png') as file:
                pirate_ship = file.read()
        self.image = pygame.image.load(io.BytesIO(pirate_ship)).convert_alpha()
        self.image= pygame.transform.scale(self.image,(90,150))
        self.og_image=pygame.transform.rotate(self.image,self.angle)
        self.colorkey = self.og_image.get_at((0, 0))
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = speed     
                      
    
    def update_position(self):
        dx = self.path[self.nextpos][0]- self.rect.centerx
        dy = self.path[self.nextpos][1] - self.rect.centery
        if dx==0 and dy==0:
          if self.nextpos<len(self.path)-1:
            self.nextpos+=1
          else:
            self.nextpos=0
          self.update_position
        if dx==0 and dy<0:
            self.angle=0
        if dx>0 and dy<0:
            self.angle=-45
        if dx>0 and dy==0:
            self.angle=-90
        if dx>0 and dy>0:
            self.angle=225
        if dx==0 and dy>0:
            self.angle=180
        if dx<0 and dy>0:
            self.angle=135           
        if dx<0 and dy==0:
            self.angle=90
        if dx<0 and dy<0:
            self.angle=45
        self.velocity=[0,0]    
        if dx >0:
            if dx <4:
                self.speed=dx
            self.rect.move_ip(self.speed,0)
            self.x=self.rect.centerx
            self.y=self.rect.centery
            self.velocity[0]=self.speed
            self.speed=4
        if dy >0:
            if dy <4:
                self.speed=dy
            self.rect.move_ip(0,self.speed)
            self.x=self.rect.centerx
            self.y=self.rect.centery 
            self. velocity[1]=self.speed
            self.speed=4   
        if dy <0:
            if dy >(-4):
                self.speed=dy
            self.rect.move_ip(0,-self.speed) 
            self.x=self.rect.centerx
            self.y=self.rect.centery
            self. velocity[1]=-self.speed
            self.speed=4 
        if dx <0:
            if dx >(-4):
                self.speed=dx
            self.rect.move_ip(-self.speed,0)
            self.x=self.rect.centerx
            self.y=self.rect.centery
            self. velocity[0]=-self.speed
            self.speed=4
                    
    def draw(self, screen):
        self.image = pygame.transform.rotate(self.og_image, self.angle)
        self.image.set_colorkey(self.colorkey)
        self.rect=self.image.get_bounding_rect()
        self.rect.center=(self.x,self.y)
        screen.blit(self.image, self.rect)
        
class ElitePirate:
    def __init__(self, x, y, speed=3):
        self.grade=2
        self.angle=0
        self.x=x
        self.y=y
        with zipfile.ZipFile('images.zip') as zf:
            with zf.open('elitepirate_ship.png') as file:
                elitepirate_ship= file.read()
        self.image = pygame.image.load(io.BytesIO(elitepirate_ship)).convert_alpha()
        self.image= pygame.transform.scale(self.image,(90,150))
        self.og_image=pygame.transform.rotate(self.image,self.angle)
        self.colorkey = self.og_image.get_at((0, 0))
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = speed     
                      
    
    def update_position(self, player_pos,pirates):
        # Move towards player
        dx = player_pos.centerx- self.rect.centerx
        dy = player_pos.centery - self.rect.centery
        if dx==0 and dy<0:
            self.angle=0
        if dx>0 and dy<0:
            self.angle=-45
        if dx>0 and dy==0:
            self.angle=-90
        if dx>0 and dy>0:
            self.angle=225
        if dx==0 and dy>0:
            self.angle=180
        if dx<0 and dy>0:
            self.angle=135         
        if dx<0 and dy==0:
            self.angle=-270
        if dx<0 and dy<0:
            self.angle=45
        self.velocity=[0,0]            
        if dx >0:
            if dx <3:
                self.speed=dx
            self.rect.move_ip(self.speed,0)
            self.x=self.rect.centerx
            self.y=self.rect.centery
            self.velocity[0]=self.speed
            self.speed=3
        if dy >0:
            if dy <3:
                self.speed=dy
            self.rect.move_ip(0,self.speed)
            self.x=self.rect.centerx
            self.y=self.rect.centery 
            self. velocity[1]=self.speed
            self.speed=3   
        if dy <0:
            if dy >(-3):
                self.speed=dy
            self.rect.move_ip(0,-self.speed) 
            self.x=self.rect.centerx
            self.y=self.rect.centery
            self. velocity[1]=-self.speed
            self.speed=3 
        if dx <0:
            if dx >(-3):
                self.speed=dx
            self.rect.move_ip(-self.speed,0)
            self.x=self.rect.centerx
            self.y=self.rect.centery
            self. velocity[0]=-self.speed
            self.speed=3
                    
    def draw(self, screen):
        self.image = pygame.transform.rotate(self.og_image, self.angle)
        self.image.set_colorkey(self.colorkey)
        self.rect=self.image.get_bounding_rect()
        self.rect.center=(self.x,self.y)
        screen.blit(self.image, self.rect)         

class SpecialPirate:
    def __init__(self, x, y, speed=6):
        self.grade=2
        self.angle=0
        self.x=x
        self.y=y
        with zipfile.ZipFile('images.zip') as zf:
            with zf.open('specialpirate_ship.png') as file:
                elitepirate_ship= file.read()
        self.image = pygame.image.load(io.BytesIO(elitepirate_ship)).convert_alpha()
        self.image= pygame.transform.scale(self.image,(60,150))
        self.og_image=pygame.transform.rotate(self.image,self.angle)
        self.colorkey = self.og_image.get_at((0, 0))
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = speed     
                      
    
    def update_position(self, player_pos,pirates):
        # Move towards player
        dx = player_pos.centerx- self.rect.centerx
        dy = player_pos.centery - self.rect.centery
        if dx==0 and dy<0:
            self.angle=0
        if dx>0 and dy<0:
            self.angle=-45
        if dx>0 and dy==0:
            self.angle=-90
        if dx>0 and dy>0:
            self.angle=225
        if dx==0 and dy>0:
            self.angle=180
        if dx<0 and dy>0:
            self.angle=135         
        if dx<0 and dy==0:
            self.angle=-270
        if dx<0 and dy<0:
            self.angle=45
        self.velocity=[0,0]            
        if dx >0:
            if dx <6:
                self.speed=dx
            self.rect.move_ip(self.speed,0)
            self.x=self.rect.centerx
            self.y=self.rect.centery
            self.velocity[0]=self.speed
            self.speed=6
        if dy >0:
            if dy <6:
                self.speed=dy
            self.rect.move_ip(0,self.speed)
            self.x=self.rect.centerx
            self.y=self.rect.centery 
            self. velocity[1]=self.speed
            self.speed=6   
        if dy <0:
            if dy >(-6):
                self.speed=dy
            self.rect.move_ip(0,-self.speed) 
            self.x=self.rect.centerx
            self.y=self.rect.centery
            self. velocity[1]=-self.speed
            self.speed=6 
        if dx <0:
            if dx >(-6):
                self.speed=dx
            self.rect.move_ip(-self.speed,0)
            self.x=self.rect.centerx
            self.y=self.rect.centery
            self. velocity[0]=-self.speed
            self.speed=6
                    
    def draw(self, screen):
        self.image = pygame.transform.rotate(self.og_image, self.angle)
        self.image.set_colorkey(self.colorkey)
        self.rect=self.image.get_bounding_rect()
        self.rect.center=(self.x,self.y)
        screen.blit(self.image, self.rect) 
   
class Boat:
    def __init__(self, x, y, image_path='player_ship.png'):
        self.angle=0
        self.x = x
        self.y = y
        self.health=100
        with zipfile.ZipFile('images.zip') as zf:
            with zf.open('player_ship.png') as file:
                player_ship = file.read()
        self.image = pygame.image.load(io.BytesIO(player_ship)).convert_alpha()
        self.og_image= pygame.transform.scale(self.image,(90,150))
        self.colorkey = self.og_image.get_at((0, 0))
        self.og_image.set_colorkey(self.colorkey)
       

    def render(self,screen):
            self.image = pygame.transform.rotate(self.og_image, self.angle)
            self.rect=self.image.get_bounding_rect()
            self.image.set_colorkey(self.colorkey)    
            self.rect.center=(self.x+45,self.y+75)
            screen.blit(self.image, self.rect)
            health_bar_rect = pygame.Rect(self.x+25, self.y, (self.health*6)//10, 4)
            health_bar_surface = pygame.Surface(((self.health*6//10), 4))
            health_bar_surface.fill((0, 255, 0))
            screen.blit(health_bar_surface, health_bar_rect)
    
    def getpos(self):
        return self.x,self.y
    
    def update_position(self,positions,path):
        dx=positions[0][0]
        dy=positions[0][1]
        if path.index//7 < len(path.direc):
            self.angle = path.direc[path.index//7]
        self.x = dx-45
        self.y = dy-75
        self.rect.centerx=dx
        self.rect.centery=dy
        path.index+=1
        positions=positions[1:len(positions)]
        return positions
    
    
class Path:
    def __init__(self):
        self.direc=[]
        self.points = []
        self.index=1

    def add(self, pos):
        self.points.append(pos)
        
    def update(self, pos):
        self.points=pos
    
    def reset(self):
        self.points=[]
        self.index=0
        self.direc=[]
    
    def getpath(self):
        return self.points

    def draw(self, surface):
        if len(self.points) < 2:
            return
        pygame.draw.lines(surface, (0, 0, 255), False, self.points, 10)
        
    def smooth(self, points):
        for i in range(7,len(points),7):
            dx=points[i][0]
            dy=points[i][1]
            direcx=dx-points[i-7][0]
            direcy=dy-points[i-7][1]
            if direcx==0 and direcy<0:
                self.direc.append(0)
            if direcx>0 and direcy<0:
                self.direc.append(-45)
            if direcx>0 and direcy==0:
                self.direc.append(270)
            if direcx>0 and direcy>0:
                self.direc.append(225)
            if direcx==0 and direcy>0:
                self.direc.append(180)
            if direcx<0 and direcy>0:
                self.direc.append(225-90)          
            if direcx<0 and direcy==0:
                self.direc.append(270+180)
            if direcx<0 and direcy<0:
                self.direc.append(45)         

class Island:
    def __init__(self, position):
        with zipfile.ZipFile('images.zip') as zf:
            with zf.open('island.png') as file:
                island = file.read()
        self.image = pygame.image.load(io.BytesIO(island)).convert_alpha()        
        self.image= pygame.transform.scale(self.image,(180,180))
        self.rect=self.image.get_bounding_rect()
        self.position=position
        self.rect=self.image.get_bounding_rect()
        self.rect.center=((self.position[0]+90,self.position[1]+90))
    def render(self, screen):
        screen.blit(self.image, self.rect)

def levels(selected):
    if selected == 1:
        boat = Boat(1010, 625)
        island = Island((90, 90))
        pirates = [Pirate(150, 400, ((500, 150), (150, 400)))]
        elitepirates = []
        specialpirates=[]
        return boat, island, pirates, elitepirates,specialpirates

    elif selected == 2:
        boat = Boat(600, 625)
        island = Island((600, 90))
        pirates = [Pirate(500, 400, ((1100, 400), (500, 400))),
                   Pirate(800, 600, ((500, 600), (1100, 600)))]
        elitepirates = []
        specialpirates=[]
        return boat, island, pirates, elitepirates,specialpirates

    elif selected == 3:
        boat = Boat(600, 625)
        island = Island((600, 90))
        pirates = [Pirate(500, 400, ((1100, 400), (500, 400))),
                   Pirate(800, 600, ((500, 600), (1100, 600)))]
        elitepirates = [ElitePirate(90,90)]
        specialpirates=[]
        return boat, island, pirates, elitepirates,specialpirates

    elif selected == 4:
        boat = Boat(1010,325)
        island = Island((0, 310))
        pirates = [Pirate(300,75, ((300,725), (300,75))),
                   Pirate(900,75, ((900,725), (900,75)))]
        elitepirates = [ElitePirate(600,400)]
        specialpirates=[]
        return boat, island, pirates, elitepirates,specialpirates

    elif selected == 5:
        boat = Boat(1010,625)
        island = Island((0, 310))
        pirates = [Pirate(300,625, ((300,75), (300,625))),
                   Pirate(900,625, ((900,75), (900,625)))]
        elitepirates = [ElitePirate(1010,75)]
        specialpirates=[]
        return boat, island, pirates, elitepirates,specialpirates

    elif selected == 6:
        boat = Boat(75,625)
        island = Island((600, 310))
        pirates = [Pirate(600, 220, ((800, 220), (800, 550), (400, 550), (400, 220)),speed=6),
        Pirate(600, 550, ((400, 550), (400, 220),(800, 220), (800, 550)),speed=6)]
        elitepirates = [ElitePirate(1010,75)]
        specialpirates=[]
        return boat, island, pirates, elitepirates,specialpirates

    elif selected == 7:
        boat = Boat(75,250)
        island = Island((1000, 400))
        pirates = [Pirate(400,75, ((800,625), (400, 625),(400,75)),speed=5),
                   Pirate(400, 625, ((400,75),(800,625), (400, 625)),speed=5),
                   Pirate(600,310, ((800,625), (400, 625),(400,75)),speed=5),
                   Pirate(400,400, ((400,75),(800,625), (400, 625)),speed=5),
                   Pirate(800, 625, ((400,625),(400, 75),(800,625)),speed=5) ]
        elitepirates = [] 
        specialpirates=[]
        return boat, island, pirates, elitepirates,specialpirates

    elif selected == 8:
        boat = Boat(75,325)
        island = Island((1000,400))
        pirates = []
        elitepirates = []
        specialpirates=[SpecialPirate(400,400),SpecialPirate(400,200),SpecialPirate(400,600)]
        return boat, island, pirates, elitepirates,specialpirates
    
    elif selected == 9:
        boat = Boat(550, 600)
        island = Island((1000, 100))
        pirates = [Pirate(700, 300, ((400,300), (400,600), (900,600))),
                   Pirate(200, 700, ((800,700), (800,400), (100,400)))]
        elitepirates = []
        specialpirates=[SpecialPirate(400,400)]
        return boat, island, pirates, elitepirates,specialpirates
             
    elif selected == 10:
        boat = Boat(75, 600)
        island = Island((1000,90))
        pirates = [Pirate(600, 220, ((800, 220), (800, 550), (400, 550), (400, 220)),speed=6),
        Pirate(600, 550, ((400, 550), (400, 220),(800, 220), (800, 550)),speed=6)]
        elitepirates = [ElitePirate(1000,650)]
        specialpirates=[SpecialPirate(400,400)]
        return boat, island, pirates, elitepirates,specialpirates
        
    elif selected == 11:
        boat = Boat(75,75)
        island = Island((1000,600))
        pirates = [Pirate(400,600, ((1000,200), (400,600)),speed=6),
                   Pirate(75, 400, ((400,75), (75, 400)),speed=6)]
        elitepirates = [ElitePirate(1000,75)]
        specialpirates=[SpecialPirate(75,600)]
        return boat, island, pirates, elitepirates,specialpirates

    elif selected == 12:
        boat = Boat(310, 625)
        island = Island((400, 90))
        pirates = [Pirate(500, 400, ((1100, 400), (500, 400))),
                   Pirate(800, 600, ((500, 600), (1100, 600)))]
        elitepirates = [ElitePirate(90,90),ElitePirate(1000,90)]
        specialpirates=[SpecialPirate(90,625),SpecialPirate(1000,625)]
        return boat, island, pirates, elitepirates,specialpirates
    
    elif selected == 13:
        boat = Boat(75, 600)
        island = Island((1000,240))
        pirates = [Pirate(75,75, ((1000,600), (75,75)),speed=8)]
        elitepirates = []
        specialpirates=[SpecialPirate(400,400),SpecialPirate(800,400)]
        return boat, island, pirates, elitepirates,specialpirates
        
    elif selected == 14:
        boat = Boat(75, 600)
        island = Island((850,160))
        pirates = [Pirate(950,75, ((1065,75), (1065,405), (730,405),(730,75)),speed=10)
               ,Pirate(950,405, ((730,405),(730,75),(1065,75), (1065,405)),speed=10)
               ,Pirate(600,75, ((600,600),(600,75)))  ]
        elitepirates = [ElitePirate(75,75)]
        specialpirates=[SpecialPirate(75,400),SpecialPirate(600,600)]
        return boat, island, pirates, elitepirates,specialpirates
     
    elif selected == 15:
        boat = Boat(550, 600)
        island = Island((100, 700))
        pirates = [Pirate(800, 200, ((400,200), (400,600), (900,600))),
                   Pirate(1100, 500, ((800,500), (800,200), (500,200)))]
        elitepirates = []
        specialpirates=[]
        return boat, island, pirates, elitepirates,specialpirates        

def game_over(screen):
    
    with zipfile.ZipFile('images.zip') as zf:
            with zf.open('background2.jpg') as file:
                background = file.read()    
    background = pygame.image.load(io.BytesIO(background)).convert_alpha()
    background= pygame.transform.scale(background,(SCREEN_WIDTH,SCREEN_HEIGHT))
    with zipfile.ZipFile('images.zip') as zf:
            with zf.open('button.png') as file:
                button = file.read()
    image = pygame.image.load(io.BytesIO(button)).convert_alpha()    
    font = pygame.font.SysFont("Impact", 72)
    game_over_text = font.render("Defeat", True, (0, 0, 0))
    text_rect = game_over_text.get_rect(center=(600,800//3))
    text = font.render(' menu', True, (0, 0, 0))
    rect=text.get_rect()  
    rect.center=((600,400))
    image1= pygame.transform.scale(image,(rect.width, rect.height))
    image2= pygame.transform.scale(image,(text_rect.width, text_rect.height))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if rect.collidepoint(event.pos):
                    game(screen,False,False,0)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_SPACE:
                    return True
        screen.blit(background,(0,0))        
        screen.blit(image1,rect)       
        screen.blit(image2,text_rect)
        screen.blit(text,rect)
        screen.blit(game_over_text, text_rect)
        pygame.display.flip()

def you_won(screen):
    with zipfile.ZipFile('images.zip') as zf:
            with zf.open('background2.jpg') as file:
                background = file.read()    
    background = pygame.image.load(io.BytesIO(background)).convert_alpha()
    background= pygame.transform.scale(background,(SCREEN_WIDTH,SCREEN_HEIGHT))
    with zipfile.ZipFile('images.zip') as zf:
            with zf.open('button.png') as file:
                button = file.read()
    image = pygame.image.load(io.BytesIO(button)).convert_alpha()    
    font = pygame.font.SysFont("Impact", 72)
    game_over_text = font.render("You won", True, (0, 0, 0))
    text_rect = game_over_text.get_rect(center=(600,800//3))
    text = font.render(' menu', True, (0, 0, 0))
    rect=text.get_rect()  
    rect.center=((600,400))
    image1= pygame.transform.scale(image,(rect.width, rect.height))
    image2= pygame.transform.scale(image,(text_rect.width, text_rect.height))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if rect.collidepoint(event.pos):
                    game(screen,False,False,0)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_SPACE:
                    return True
        screen.blit(background,(0,0))        
        screen.blit(image1,rect)       
        screen.blit(image2,text_rect)
        screen.blit(text,rect)
        screen.blit(game_over_text, text_rect)
        pygame.display.flip()

def create_menu(surface):
    # Initialize Pygame
    pygame.init()
    with zipfile.ZipFile('images.zip') as zf:
            with zf.open('background.jpg') as file:
                background = file.read()    
    background = pygame.image.load(io.BytesIO(background)).convert_alpha()
    background= pygame.transform.scale(background,(SCREEN_WIDTH,SCREEN_HEIGHT))
    with zipfile.ZipFile('images.zip') as zf:
            with zf.open('button.png') as file:
                button = file.read()
    image = pygame.image.load(io.BytesIO(button)).convert_alpha()
    image= pygame.transform.scale(image,(BUTTON_WIDTH, BUTTON_HEIGHT))
    
    font = pygame.font.SysFont("Impact", 72)
    title = font.render('Levels', True, (0, 0, 0))
    image2= pygame.transform.scale(image,(250, 90)) 
    font = pygame.font.Font(None, FONT_SIZE)

    # Create buttons
    buttons = []
    for row in range(NUM_ROWS):
        for col in range(NUM_COLS):
            # Calculate button position and rect
            x = (col * (BUTTON_WIDTH + BUTTON_PADDING)) + (SCREEN_WIDTH - (BUTTON_WIDTH + BUTTON_PADDING) * NUM_COLS) // 2
            y = (row * (BUTTON_HEIGHT + BUTTON_PADDING)) + (SCREEN_HEIGHT - (BUTTON_HEIGHT + BUTTON_PADDING) * NUM_ROWS) // 2
            rect = pygame.Rect(x, y, BUTTON_WIDTH, BUTTON_HEIGHT)
            # Create button text
            text = font.render(str(row * NUM_COLS + col + 1), True, FONT_COLOR)
            text_rect = text.get_rect(center=rect.center)
            # Append button and text to buttons list
            buttons.append((rect, text))

    # Main loop
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Check if a button was clicked
                for i, (rect, _) in enumerate(buttons):
                    if rect.collidepoint(event.pos):
                        return i + 1

        # Draw buttons and text on surface
        surface.fill(SEA_COLOR)
        surface.blit(background, (0,0))
        surface.blit(image2, (450,90))
        surface.blit(title, (500,100))
        for rect, text in buttons:
            surface.blit(image,rect)
            surface.blit(text, text.get_rect(center=rect.center))

        # Update display
        pygame.display.update()

    # Quit Pygame
    pygame.quit()

def game(screen,IS_DRAWN,IS_DRAWING,delay):

    pygame.display.set_caption("Pirate Hunter: The Quest for Treasure")
    
    selected_level = create_menu(screen)
    
    path = Path()
    
    entities=levels(selected_level)
    boat=entities[0]
    island=entities[1]
    pirates=entities[2]
    elitepirates=entities[3]
    specialpirates=entities[4]
    
    pygame.init()
    
    boat.render(screen)
    
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                b=boat.getpos()
                e=event.pos
                if e[0]>=b[0] and e[1]>=b[1] and (e[0]<=b[0]+150) and (e[1]<=b[1]+250):
                    if IS_DRAWN==False:
                        IS_DRAWING = True
            elif event.type == pygame.MOUSEMOTION:
                if IS_DRAWING:
                        path.add(event.pos)
            elif event.type == pygame.MOUSEBUTTONUP:       
                if IS_DRAWING==True:
                     IS_DRAWN= True
                     IS_DRAWING=False
                     path.smooth(path.getpath())     
                                                                
        screen.fill(SEA_COLOR)
        
        if (delay%4==0):            
            for pirate in elitepirates:
                pirate.update_position(island.rect,pirates)
                r=check_islandcollision(island,elitepirates)
                if r==False:
                    game_over(screen)
                
            for pirate in specialpirates:
                pirate.update_position(boat.rect,pirates)                
            
            for pirate in pirates:
                pirate.update_position()
                check_collisions(pirates+elitepirates+specialpirates)
        
        if (IS_DRAWN==True) and (delay%6==0):
            if delay==299:
                delay=0            
            p=boat.update_position(path.points,path)
            if p==[]:
                path.reset()    
                IS_DRAWN=False
            else:
                path.update(p)    
        delay+=1
        
        running=checkboatcollisions(boat,pirates,screen,selected_level)
        if running==False:
            dead=[]
            game_over(screen)
         
        running=checkboatcollisions(boat,specialpirates,screen,selected_level)
        if running==False:
            dead=[]
            game_over(screen)
                   
        running=checkboatcollisions(boat,elitepirates,screen,selected_level)
        if running==False:
            dead=[]
            game_over(screen)
        
        running=checkwinner(boat,island)
        if running==False:
            dead=[]
            you_won(screen)  
          
        boat.render(screen)  
        
        island.render(screen) 
        
        path.draw(screen)        
        
        for pirate in pirates:
            pirate.draw(screen)
            
        for pirate in specialpirates:
            pirate.draw(screen)
        
        for pirate in elitepirates:
            pirate.draw(screen)
            
        pygame.display.update()
    
    # Quit Pygame
    pygame.quit()

    
pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

game(screen,IS_DRAWN,IS_DRAWING,delay)  
