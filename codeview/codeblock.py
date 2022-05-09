from pydoc import visiblename
import pygame
#set constant for the inivisible color(done bycolorkey later)
INVISIBLE_COLOR = (255,1,1)

class CodeBlock(pygame.sprite.Sprite):
    id = "classic"
    def __init__(self, background_color = (130,130,130)):
        super().__init__()
        self.background_color = background_color

        self.size = pygame.Vector2(300,80)
        self.scale_factor = 1
        self.position = pygame.Vector2(10,10)

        self.in_focus = False

        #the nex block in the list(under self)
        self.next_block = None
        #first build of the image with the start size.
        self.build_image(self.size)

    def update_scale_factor(self, scalefactor):
        last_scale_factor = self.scale_factor
        self.scale_factor = scalefactor

        #rebuild the image with the new scalefactor and size
        self.build_image(self.size * scalefactor)

        #get the current mouseposition for moving the images in the right way(center of movemet is the mouseposition).
        center_of_scrollment = pygame.mouse.get_pos()
        distance = (self.position - center_of_scrollment) / last_scale_factor
        distance *= scalefactor
        self.position = center_of_scrollment + distance

        #pass on the new scalefactor to the nex block in the list
        if self.next_block:
            self.next_block.update_scale_factor(scalefactor)
            self.adjust_blocks()

    def build_image(self, size):
        """creates the self.image Surface for the block"""

        self.image = pygame.Surface(size)
        self.rect = self.image.get_rect()

        #set the right color as invisble
        self.image.set_colorkey(INVISIBLE_COLOR)
        #fill the background with the invisible color
        self.image.fill(INVISIBLE_COLOR)

        #set the size of the visible part (it is 85% from the height)
        self.visible_size = size - pygame.Vector2(0, 0.15 * size.y)

        #the normal collision box should be on the visible part of the surface
        self.rect.size = self.visible_size.copy()
        rect = pygame.Rect((0,0), self.visible_size)

        #draw the normal rect with border
        pygame.draw.rect(self.image,self.background_color,rect)
        pygame.draw.rect(self.image,(0,0,0),rect,width=2)

        #draw the bottom circle width border
        self.circle_overlap = 10 * self.scale_factor
        self.circle_radius = (size.y - self.visible_size.y) + self.circle_overlap #create the circle radius from height of the invisible part
        self.circle_x = size.x / 2
        circle_position = pygame.Vector2(self.circle_x, self.visible_size.y - self.circle_overlap)
        pygame.draw.circle(self.image,self.background_color, circle_position, self.circle_radius)
        pygame.draw.circle(self.image, (0,0,0), (self.circle_x ,self.visible_size.y - self.circle_overlap), self.circle_radius, width = 2)

        #rect for covering the circlelines inside the rect
        rect =pygame.rect.Rect((0,0),(self.circle_radius * 2, self.circle_radius+self.circle_overlap))
        rect.centerx = self.circle_x
        rect.bottom = self.visible_size.y - 2
        pygame.draw.rect(self.image, self.background_color, rect)

    def append(self, code_block):
        """Append the given block"""
        if self.next_block: #if this block already has one next_block pass it on to it
            self.next_block.append(code_block)
        else: # found the right place to append
            self.next_block = code_block
            #adjust the position to each other
            self.adjust_blocks() 
          
    def get_last_invisible_rect(self):  
        """Returns the invisible rect of the last element in the line(bottom)"""
        if self.next_block: #if this block has one next_block pass it on to it
            return self.next_block.get_last_invisible_rect()
        else:
            #create the invisible rect from visible size(its 85%)
            invisible_size = (self.visible_size.x, (self.visible_size.y/0.85)*0.15)
            invisible_position = self.position + (0,self.visible_size.y)
            invisible_rect = pygame.rect.Rect(invisible_position, invisible_size)
            return invisible_rect

    def try_to_connect(self, block):
        """Checks if the two blocks can connect. Connect them if possible 
        and return the one that is beneath the other."""
        #get the last invisible rects from self and the given block
        own_invisible_rect = self.get_last_invisible_rect()
        other_invisible_rect = block.get_last_invisible_rect()

        #if the blocks(and its appendix) collide with visible part on invisble part connect them,
        #the start block should not be appended on another block(is everytime the start)
        if block.id != "start" and own_invisible_rect.colliderect(block.rect):
            self.append(block)
            return block
        elif self.id != "start" and other_invisible_rect.colliderect(self.rect):
            block.append(self)
            return self


    def adjust_blocks(self):
        """Adjust the next block(if existing) to the right position beneath self."""
        if self.next_block:
            half_size_difference_x = (self.next_block.visible_size.x - self.visible_size.x)/2
            self.next_block.position = self.position + (-half_size_difference_x,self.visible_size.y - 1)
            self.next_block.adjust_blocks()

    def mouse_button_up(self):
        #reset the focus
        self.in_focus = False
        if self.next_block :#if this block has one next_block pass it on to it
            self.next_block.mouse_button_up()

    def get_collider(self, mouse_position : pygame.Vector2):
        """check own and child block collision with given (mouse-)position"""
        if self.rect.collidepoint(mouse_position):
            self.in_focus = True
            return self
        else: 
            if self.next_block:
                #delete the selected block frm line and return it for adding into the blockview blocklist
                collider = self.next_block.get_collider(mouse_position)
                if collider == self.next_block:
                    self.next_block = None
                return collider

    def move(self, movement : pygame.Vector2):
        self.position += movement
        if self.next_block:#if this block has one next_block pass it on to it
            self.next_block.move(movement)

    def update(self):
        self.rect.topleft = self.position
        if self.next_block:#if this block has one next_block pass it on to it
            self.next_block.update()

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        if self.next_block:#if this block has one next_block pass it on to it
            self.next_block.draw(screen)