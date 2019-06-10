
# coding: utf-8

# In[14]:


from actors import *
from places import *
import random
from time import sleep
from IPython.display import clear_output


# In[15]:


def print_line():
    print("---------------------------------------------------")

def text_loading(string):
    for i in range(8):
        print_line()
        print(string + "."*(i%4))
        print_line()
        clear_output(True)
        sleep(0.3)
        
def text_header(string):
    print_line()
    print(string)
    print_line()


# In[16]:


class World():
    def __init__(self):
        self.levels = []
        self.levels.append(Home())
        self.curr_level_ind = 0
        self.player = None
                
    def play(self):
        self = World()
        self.player = Player()
        self.player.wealth = 10
        text_loading("Generating world")
        clear_output(True)
        
        while(self.player.status()):
            curr_level = self.levels[self.curr_level_ind]
            text_header("Entering Location: " + curr_level.name)
            curr_level.interact(self.player)
            while True:
                if(self.player.status() == False):
                    print("Your story ends here. You went through " + str(len(self.levels)) + " level(s).")
                    break;
                response = input("Would you like to continue your journey? (Y/N)\t")
                if response.lower() == 'y':
                    self.enter_next_location()
                    break
                elif response.lower() == 'n':
                    if self.curr_level_ind == 0:
                        print("Your story ends here. You went through " + str(len(self.levels)) + " level(s).")
                        self.player.curr_health = 0
                    self.curr_level_ind = 0
                    break
                elif response.lower() == 'p':
                    self.print_world()
                elif response.lower() == 's':
                    self.player.show_stats()
                else:
                    print("Please enter a valid response.")
            clear_output(True)
            
    def enter_next_location(self):
        self.curr_level_ind = self.curr_level_ind + 1
        if self.curr_level_ind >= len(self.levels):
            r = random.random()
            if r < 0.10:
                self.levels.append(Shop())
                text_loading("Generating a shop")
            else:
                self.levels.append(Map(size=self.curr_level_ind + 1))
                text_loading("Generating a dungeon")

    def print_world(self):
        out = ""
        curr_level = self.levels[self.curr_level_ind]
        for level in self.levels:
            if level == curr_level:
                out = out + '*['
            else:
                out = out + '|'
            if type(level) is Home:
                out = out + "H"
            elif type(level) == Shop:
                out = out + "S"
            elif type(level) == Map:
                out = out + "D"
            if level == curr_level:
                out = out + ']*'
            else:
                out = out + '|'
            out = out + " > "
        print(out)

