from cmu_graphics import *
from PIL import Image 
import random, time
## sprite gif from 
# #https://tenor.com/view/omori-kel-hector-dream-world-headspace-gif-22277361
# icon from: https://www.deviantart.com/envelopedheart/art/PIXEL-You-Died-Screen-420922059
# background from 
# https://www.wallpaperflare.com/green-tall-trees-over-clear-calm-sky-illustration-wallpaper-180284

# all other text is from https://www.fonttopng.com/en/font-generator/arcade-font/index.php
#PIL and image methods are from lecture 

#Spring icon is from https://www.123rf.com/photo_132760301_vector-pixel-art-spring-isolated-cartoon.html
# bomb icon is from https://www.vectorstock.com/royalty-free-vector/pixel-art-style-isolated-bomb-for-retro-vector-33228541
#Coin icon is from https://www.freepik.com/premium-vector/gold-coin-pixel-art_22989326.htm
# explosion icon is from https://www.vecteezy.com/vector-art/8202209-explosion-with-pixel-art-vector-illustration
class Sprite:
    def __init__(self):
        self.started= False 

        myGif = Image.open('/Users/julialiu/Desktop/images/sprite.gif')
        self.spriteList = []
        for frame in range(myGif.n_frames):  #For every frame index...
            #Seek to the frame, convert it, add it to our sprite list
            myGif.seek(frame)
            fr = myGif.resize((myGif.size[0]//2, myGif.size[1]//2))
            fr = fr.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
            fr = CMUImage(fr)
            self.spriteList.append(fr)

        ##Fix for broken transparency on frame 0
        self.spriteList.pop(0)

        #Set sprite counters
        self.stepCounter = 0
        self.spriteCounter = 0

        #Set initial position, velocity, acceleration
        self.x, self.y = 100, 700

        self.width= 40
        self.height= 50

        self.dy = 0
        self.ddy = .4

    def draw(self):
        drawImage(self.spriteList[self.spriteCounter], 
                  self.x, self.y, align = 'center')
        
    def doStep(self):
        self.stepCounter += 1
        if self.stepCounter >= 1: #Update the sprite every 10th call
            self.spriteCounter = (self.spriteCounter + 1) % len(self.spriteList)
            self.stepCounter = 0

        #Update position and velocity
        self.y += self.dy
        self.dy += self.ddy

        if self.started != True: 
            if self.y > 700:
                self.y = 700
                self.dy = 0
        if self.x <=10:
            self.x=980
        elif self.x>=990:
            self.x= 15

    def flap(self):
        self.dy = -8
    def hugeFlap(self):
        self.dy= -13
    def moveLeft(self):
        self.x -= 14
    def moveRight(self):
        self.x+= 14

#-------------------------------------------------------------------
class Coin:
    def __init__(self, app):
        self.coin= Image.open('/Users/julialiu/Desktop/images/coin.png')
        self.coin= CMUImage(self.coin)
        self.x= random.randrange(100, 900)
        self.y= -50
        self.dy= 5 
        
    def doStep(self):
        self.y += self.dy 

    def draw(self):
        drawImage(self.coin, self.x, self.y)
    
#-------------------------------------------------------------------
class BoostBlocks:
    def __init__(self, app):
        self.block= Image.open('/Users/julialiu/Desktop/images/spring.png')
        self.block= CMUImage(self.block)
        self.width=153
        self.height=64
        self.x = random.randrange(self.width, 1000-self.width)
        self.dy= 3
        self.y=Blocks.y

        if Blocks.y>=125:
            Blocks.y-=125
        else:
            Blocks.y= -100

    def doStep(self):
        self.y += self.dy
        
    def draw(self):
        drawImage(self.block, self.x, self.y)

class MovingBlocks:
    def __init__(self, app):
        self.block= Image.open('/Users/julialiu/Desktop/images/block.png')
        self.block= CMUImage(self.block)
        self.width=153
        self.height=64
        self.x = random.randrange(self.width, 1000-self.width)
        self.dy= 3
        self.y=Blocks.y
        self.dx= 3

        if Blocks.y>=125:
            Blocks.y-=125
        else:
            Blocks.y= -100
        
        

    def doStep(self):
        self.y += self.dy
        if (self.x <= 0 )or (self.x >= 1000-self.width):
            self.dx= -self.dx
        self.x += self.dx
        
    def draw(self):
        drawImage(self.block, self.x, self.y)
        
class Blocks:
    y=665
    def __init__(self, app):
        self.block= Image.open('/Users/julialiu/Desktop/images/block.png')
        self.block= CMUImage(self.block)
        self.width=153
        self.height=64
        self.x = random.randrange(self.width, 1000-self.width)
        self.dy= 3
        self.y=Blocks.y

        if Blocks.y>=125:
            Blocks.y-=125
        else:
            Blocks.y= -100

    def doStep(self):
        self.y += self.dy
        

    def draw(self):
        drawImage(self.block, self.x, self.y)

#-------------------------------------------------------------------
class Bomb:
    def __init__(self, app):
        self.bomb= Image.open('/Users/julialiu/Desktop/images/bomb.png')
        self.bomb= CMUImage(self.bomb)
        self.x= random.randrange(50, 1000-50)
        self.y= -50
        self.dy= 5
        
    
    def doStep(self):
        self.y+= self.dy 
    
    def draw(self):
        drawImage(self.bomb, self.x, self.y)

#-------------------------------------------------------------------
def onAppStart(app):
    restartApp(app)

def restartApp(app):
    app.died=None 
    app.bombDeath= False

    app.backMove= 0.2
    app.back= Image.open('/Users/julialiu/Desktop/images/background.png')
    app.backX= -200
    app.backY= -307

    app.bombs=[]
    app.coins= []


    app.backWidth,app.backHeight = app.back.width,app.back.height

    app.back= CMUImage(app.back)
    app.stepsPerSecond = 30        #Adjust the onStep frequency
    app.sprite = Sprite()               
    app.blocks = []          
    app.lastBlockTime = time.time() 
    app.lastJumpTime= time.time()
    if app.died==None: 
        startScreen(app)

    deathScreen(app)

    app.score= 0  

def startScreen(app):
    #temporary background
    app.tback= Image.open('/Users/julialiu/Desktop/images/background.png')
    app.tbackX= -200
    app.tbackY= -307
    app.tbackWidth,app.tbackHeight = app.tback.width,app.tback.height
    app.tback= CMUImage(app.tback)

    #start sign
    app.start= Image.open('/Users/julialiu/Desktop/images/start.png')
    app.startWidth,app.startHeight = app.start.width,app.start.height
    app.startX= 500-app.startWidth//2
    app.startY= 200+app.startHeight
    app.start= CMUImage(app.start)
    #title screen
    app.name= Image.open('/Users/julialiu/Desktop/images/title.png')
    app.nameWidth,app.nameHeight = app.name.width,app.name.height
    app.nameX= 500-app.nameWidth//2
    app.nameY= app.nameHeight
    app.name= CMUImage(app.name)

    for i in range(6):
        app.blocks.append(Blocks(app))

def deathScreen(app):
    app.gone= Image.open('/Users/julialiu/Desktop/images/death.png')
   
    app.goneWidth,app.goneHeight = app.gone.width,app.gone.height
    app.goneX= 500-app.goneWidth//2
    app.goneY= app.goneHeight

    app.gone= CMUImage(app.gone)

    app.restart= Image.open('/Users/julialiu/Desktop/images/restart.png')
    app.restart= CMUImage(app.restart)

    app.explode = Image.open('/Users/julialiu/Desktop/images/bombed.png')
    app.explode= CMUImage(app.explode)

    
def onStep(app):
    # flap logic. determines how high a jump should be. 
    if app.died==False:
        for block in app.blocks:
            if -10<=(app.sprite.y+app.sprite.height)-(block.y)<=10:     
                if block.x<=app.sprite.x<=(block.x+block.width):
                    if type(block)== BoostBlocks:
                        app.sprite.hugeFlap()
                    else:
                        app.sprite.flap()
                
                    app.sprite.started=True 
                    app.death= False
                    break 
        
        if app.backY<=0 and app.sprite.started:
            app.backY+=app.backMove

        app.sprite.doStep()
        

        if (time.time() - app.lastJumpTime > 1) and app.sprite.started==False:
            if app.sprite.started==False:
                app.sprite.flap()
                app.lastJumpTime = time.time()

#pseudorandomization of block generation and bombs
        if app.sprite.started:
            for block in app.blocks:
                block.doStep()
            if (time.time() - app.lastBlockTime > 1):
                app.score+=10 #survival points. 
                digit= random.randrange(0, 10)
                if 0<= digit<= 7:
                    app.blocks.append(Blocks(app))
                elif digit==8:
                    app.blocks.append(MovingBlocks(app))
                else:
                    app.blocks.append(BoostBlocks(app))
                app.lastBlockTime = time.time()

            ##randomization for bombs 
            for bomb in app.bombs:
                if app.sprite.y-130<= bomb.y <=app.sprite.y+60:     
                    if bomb.x-70<=app.sprite.x<=(bomb.x+70):
                        app.bombDeath= True 
                        app.died =True 
                        
                         

            randomDigit = random.randrange(1, 1000)

            if randomDigit==2:
                app.bombs.append(Bomb(app))

            for bomb in app.bombs:
                bomb.doStep()

            ## collision check for bombs:

        for i in range(len(app.blocks)):
            if app.blocks[i].y>=1500:
                app.blocks.pop(i)
                break

        if app.sprite.y>1000:
            app.died= True 
        
        randomDigit= random.randrange(1, 100)

        ## randomization for coins
        if randomDigit== 3:
            app.coins.append(Coin(app))
        for coin in app.coins:
            coin.doStep()
        
        # collision check for coins
        for i in range(len(app.coins)):
                if app.sprite.y-200<= app.coins[i].y <=app.sprite.y+60:     
                    if app.coins[i].x-70<=app.sprite.x<=(app.coins[i].x+70):
                        app.coins.pop(i)
                        app.score+=100
                        break #gotta break otherwise list index outta range. 
                        

def onKeyPress(app, key):
    if key== 's':
        app.died=False
    if key=='r' and app.died==True:
        restartApp(app)

def onKeyHold(app, keys):
    if 'left' in keys:
        app.sprite.moveLeft()
    elif 'right' in keys:
        app.sprite.moveRight()

def redrawAll(app):
    #Background
    if app.died==False: #sliving 
        drawImage(app.back,app.backX,app.backY)
        
        for block in app.blocks:
            block.draw()

        for bomb in app.bombs:
            bomb.draw()
        for coin in app.coins:
            coin.draw()
        
        drawLabel(f'Score: {app.score}', 100, 670, bold= True, border= 'white', font='grenze', size= 30)

        app.sprite.draw()
        

    elif app.died==True: #killed
        
        drawImage(app.tback,app.tbackX,app.tbackY)
        
        if app.bombDeath==True: 
            drawImage(app.explode, 320, 130)
        drawImage(app.gone, app.goneX, app.goneY)
        drawImage(app.restart, app.startX, app.startY)
        drawLabel(f'You died with a score of: {app.score}', 500, app.startY+150, bold= True, border= 'white', font='grenze', size= 30)
        

    elif app.died==None: #not started 
        drawImage(app.tback,app.tbackX,app.tbackY)
        drawImage(app.start, app.startX, app.startY)
        drawImage(app.name, app.nameX, app.nameY)

#width and height   
runApp(width=1000, height=1000)