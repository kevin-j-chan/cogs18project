
# coding: utf-8

# In[13]:


# FILE SETUP
import random
from IPython.display import clear_output
from time import sleep
from actors import *


# In[14]:


class Location():
    def __init__(self, name):
        self.name = name
    
    def interact(self, player):
        raise NotImplementedError("Please implement this method.")


# In[15]:


class Shop(Location):
    
    def __init__(self, name="Shop"):
        super().__init__(name)
        self.inventory = dict()
        self.add_item(Potion(value = 5))
        self.add_item(Potion(name = "elixir", value = 10, strength = 10))
        

    def display_items(self):
        """ Print out the items in the inventory. """
        if not self.inventory:
            print("This shop has no inventory.")
        else:
            print("This shop currently has:")
            for item in self.inventory.values():
                item.print()
    
    def add_item(self, item):
        """ Add an item to shop inventory. """
        self.inventory.update({item.name : item})
        
    def remove_item(self, item_name):
        """ Remove an item from shop inventory."""
        del self.inventory[item_name]
    
    def interact(self, player):
        self.display_items()
        print()
        player.display_items()
        print("You currently have " + str(player.wealth) + " gold.")
        print("What would you like to do?")
        response = input("\t purchase | sell | exit \t")
        if response.lower() == 'purchase':
            self.purchase(player)
        elif response.lower() == 'sell':
            self.sell(player)
        else:
            print("Okay, have a nice day.")
            
    def purchase(self, player):
        """ Gives the player an item and removes it from inventory. """
        interacting_with_shop = True
        shop_prompt = "What would you like to buy? (Type 'exit' to leave the shop.) \t"
        while interacting_with_shop:
            item_name = input(shop_prompt)
            item_name = item_name.lower()
            # If the shop does not have the item in inventory
            while item_name not in self.inventory.keys():
                if item_name == 'exit':
                    interacting_with_shop = False
                    break
                print("\tThis shop does not have " + item)
                item_name = input(shop_prompt)
                item_name = item_name.lower()
            # If the shop has the item in inventory, take the money from player and give them the item
            if item_name in self.inventory.keys():
                curr_item = self.inventory[item_name]
                cost = curr_item.value
                if player.wealth >= cost:
                    player.wealth = player.wealth - cost
                    player.add_item(curr_item)
                    self.remove_item(curr_item.name)
                    print("\t" + item_name + " has been added to your inventory")
                    self.display_items()
                else:
                    print("You cannot afford this item!")
    
    def sell(self, player):
        """ The player sells an item to the shop, adding wealth to the player and adding the item to the shop. """
        interacting_with_shop = True
        shop_prompt = "What would you like to sell? (Type 'exit' to leave the shop.) \t"
        while interacting_with_shop:
            item_name = input(shop_prompt)
            item_name = item_name.lower()
            # If the player does not have the item in invetory
            while item_name not in player.backpack.keys():
                if item_name == 'exit':
                    interacting_with_shop = False
                    break
                print("\tYou do not have this item.")
                item_name = input(shop_prompt)
                item_name = item_name.lower()
            if item_name in player.backpack.keys():
                curr_item = player.backpack[item_name]
                self.add_item(curr_item)
                player.remove_item(curr_item.name)
                player.wealth = player.wealth + curr_item.value
                print("\tYou have sold " + curr_item.name +" for " + str(curr_item.value) +" gold.")


# In[16]:


class Home(Location):
    def __init__(self, name="Home"):
        super().__init__(name)
    
    def interact(self, player):
        print("Welcome home - enjoy your rest.")
        
        response = input("Would you like to change your equipment? (Y/N)\t")
        while(response.lower() == 'y'):
            if(len(player.backpack) == 0):
                print("\tYou do not have any items.")
                break
            player.display_items()
            item_name = input("What would you like to equip?\t")
            item_name = item_name.lower()
            player.equip_item(item_name)
            response = input("Would you like to equip anything else? (Y/N)\t")
                
        player.curr_health = player.calculated_health()
        print("Your health has been restored.")

# In[17]:


class Map(Location):
    def __init__(self, name="Dungeon", size=5):
        super().__init__(name + " - level " + str(size))
        self.size = size
        self.map = []
        self.initialize_map()
    
    def initialize_map(self):
        r = random
        difficulty_mult = 1 + self.size * 0.25
        while len(self.map) < self.size:
            num = r.random()
            if num < .05:
                self.map.append(Aberrant(d = difficulty_mult))
            elif num < .15:
                self.map.append(Heavy(d = difficulty_mult))
            elif num < .60:
                self.map.append(Normal(d = difficulty_mult))
            elif num < .90:
                self.map.append(Quick(d = difficulty_mult))
            else:
                self.size = self.size - 1
                
    def print_contents(self):
        for i in self.map:
            i.print_undiscovered()
    
    def interact(self, player):
        self.print_contents()
        sleep(3)
        self.combat(player)
    
    def combat(self, player):
        actions = ['fight', 'item', 'run', 'f', 'i', 'r']
        combat_prompt = "\t[f]ight | [i]tem | [r]un\t"
        for mob in self.map:
            clear_output(True)
            print("---------------------------------------------------")
            mob.print_encountered()
            print("---------------------------------------------------")
            while player.status() and mob in self.map:
                print("Current health:\t" + str(player.curr_health))
                print(mob.name +":\t" + str(mob.health))
                action = input(combat_prompt)
                action = action.lower()
                while action not in actions:
                    print("Please enter a valid action.")
                    action = input(combat_prompt)
                if action == 'fight' or action == 'f':
                    player.fight(mob)
                    if not player.status():
                        print("You have died.")
                        break;
                    if not mob.status():
                        player.gain_experience(mob.exp_value)
                        self.map.remove(mob)
                        drop = mob.drop_loot(base_rate = 1)
                        if drop is not None:
                            player.add_item(drop)
                            print("\tYou found " + drop.name + ".")
                            sleep(3)
                elif action == 'item' or action == 'i':
                    player.display_items()
                    item_name = input("What would you like to use? Type '[e]xit' to use nothing.\t")
                    if item_name.lower() != 'e' or item_name.lower() != 'exit':
                        player.use_item(item_name)
                        mob.attack(player)
                elif action == 'run' or action == 'r':
                    if player.run_from(mob):
                        print("\tYou have successfully fled.")
                        self.map.remove(mob)
                    else:
                        print("\tYou have failed to get away and took " + str(mob.strength) + " damage.")
                        player.curr_health = player.curr_health - mob.strength
            
            

