import pygame, sys, random
from pygame.locals import *
from random import shuffle
from time import sleep
# Set up pygame.



class Text:
    """Create a text object."""

    def __init__(self, text, pos,center, **options):
        self.text = text
        self.pos = pos
        self.center = center
        self.fontname = 'gabriola'
        self.fontsize = 45
        self.fontcolor = (25, 94, 131)
        self.set_font()
        self.render()

    def set_font(self):
        """Set the Font object from name and size."""
        self.font = pygame.font.SysFont(self.fontname, self.fontsize)

    def render(self):
        """Render the text into an image."""
        self.img = self.font.render(self.text, True, self.fontcolor)
        self.rect = self.img.get_rect()
        if self.center:
        	self.rect.centerx = App.screen.get_rect().centerx
        	self.rect.top = self.pos
        else:
        	self.rect.topleft = self.pos

    def draw(self):
        """Draw the text image to the screen."""
        App.screen.blit(self.img, self.rect)


class Image:
	"""docstring for Image"""
	def __init__(self,name,position,status):
		self.name = name
		self.position = position
		self.status = status
		self.load()
	def load(self):
		picture = pygame.image.load('images/'+self.name)
		pic = pygame.transform.scale(picture, (150, 150))
		self.surface = pic
		self.rect = pic.get_rect()
		self.rect.topleft = self.position 

		


class App:
    """Create a single-window app with multiple scenes."""

    def __init__(self):
        """Initialize pygame and the application."""
        pygame.init()
        flags = RESIZABLE
        self.length = 150
        self.margin = 30
        self.width= 600
        self.height = 800
        App.screen = pygame.display.set_mode((self.width, self.height), flags)
        self.running = True
        self.t = Text('Welcome',100,True)
        self.colors = {'BLUE' : (25, 94, 131),'BEJ' : (237, 184, 121)}
        self.images = ['orange.jpg','mashrooms.jpg','headphones.jpg','donut.jpg','rocks.jpg','unknown.jpg']*2
        self.positions = self.setup_positions()
        self.grid = self.grid_list(self.images,self.positions)
        self.state = 'intro'
    def setup_positions(self):
    	l = []
    	margin = self.margin
    	length = self.length
    	for y in range(50,self.height-50,length+margin):
    		for x in range(50,self.width-50,length+margin):
    			l.append((x,y))
    	return l
    def grid_list(self,imgs,pos):
    	l = []
    	shuffle(imgs)
    	for i in range(0,len(imgs)):
    		l.append(Image(imgs[i],pos[i],'show'))
    	return l	
    def draw_grid(self,grid):
    	grid = [grid[:3],grid[3:6],grid[6:9],grid[9:]]
    	for raw in grid:
    		for img in raw:
    			if img.status =='show':
    				App.screen.blit(img.surface,img.rect)
    			if img.status =='hide':
    				pygame.draw.rect(App.screen,self.colors['BLUE'],img.rect)	
    def run(self):
        """Run the main event loop."""
        mainClock = pygame.time.Clock()
        countdown = 4
        first = None
        while True:
        	if self.state == 'intro':
        		self.intro()
        	if self.state == 'main':
        		self.main(countdown)
        		countdown -= 1
        		if countdown<0:
        			for img in self.grid:
        				img.status = 'hide'
        			self.state = 'play'
        		mainClock.tick(1)
        	if self.state == 'play':
        		first = self.play(first)
        		print(f'the return val: {first.name if first else None}')
        		mainClock.tick(10)
        	if self.state == 'end':
        		self.end()
        		mainClock.tick(10)
		
    	
    def intro(self):
	    for event in pygame.event.get():
	        if event.type == QUIT:
	            pygame.quit()
	            sys.exit()
	        if event.type == KEYDOWN:
	        	if event.key == K_RETURN:
	        		self.state = 'main'

	    App.screen.fill(self.colors['BEJ'])
	    Text('Welcome to memory puzzle game!',10,True).draw()
	    Text("I'm gonna show you the images for 3secs",300,True).draw()
	    Text("press Enter to start palying ^^",400,True).draw()
	    Text("Have fun!",500,True).draw()
	    pygame.display.update()
    def main(self,countdown):
    	for event in pygame.event.get():
    		if event.type == QUIT:
    			pygame.quit()
    			sys.exit()
    	App.screen.fill(self.colors['BEJ'])
    	Text(f'{countdown}',0,True).draw()
    	self.draw_grid(self.grid)
    	pygame.display.update()

    def play(self,first):
    	self.draw_grid(self.grid)
    	pygame.display.update()
    	for event in pygame.event.get():
    		if event.type == QUIT:
    			pygame.quit()
    			sys.exit()
    		if event.type == MOUSEBUTTONDOWN :
    			for item in self.grid:
    				if event.pos[0] > item.rect.left and event.pos[0] <item.rect.left+self.length and event.pos[1] > item.rect.top and event.pos[1] <item.rect.top+self.length:
    					item.status = 'show'
    					self.draw_grid(self.grid)
    					pygame.display.update()
	    				if first is None:
	    					first = item
	    					return first
	    				if first.name == item.name and first != item:
	    					first = None
	    					return first
	    				if (first is not None) and item.name != first.name:
	    					item.status = 'hide'
	    					self.grid[self.grid.index(first)].status = 'hide'
	    					first = None
	    					return first
    	if len([item for item in self.grid if item.status == 'show']) == len(self.grid):
    		self.state = 'end'
    	return first
    def end(self):
    	for event in pygame.event.get():
    		if event.type == QUIT:
    			pygame.quit()
    			sys.exit()
    	App.screen.fill(self.colors['BEJ'])
    	Text('good job!',300,True).draw()
    	pygame.display.update()

if __name__ == '__main__':
    App().run()

