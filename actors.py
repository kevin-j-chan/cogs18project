
# coding: utf-8

# In[4]:


import random
from items import *
from math import floor
# In[5]:


class Player():
    def __init__(self, level=1, health=50, strength=5, speed=5):    
        self.is_alive = True
        
        # Player inventory
        self.e_sword = Sword(name="none", value=0, strength=0)
        self.e_armor = Armor(name="none", value=0, strength=0, weight=1)
        self.backpack = dict()
        self.wealth = 0
        
        # Player level values
        self.level = level
        self.exp_value = 0
        
        # Player stat values
        self.max_health = health
        self.curr_health = health
        self.strength = strength
        self.speed = speed

        
    def gain_experience(self, value):
        """ Calculate experience value. """
        stat_points = 0
        self.exp_value = self.exp_value + value
        exp_requirement = 25 * self.level
        while self.exp_value >= exp_requirement:
            print("You leveled up!")
            self.level = self.level + 1
            self.exp_value = self.exp_value - exp_requirement
            exp_requirement = 25 * self.level
            stat_points = stat_points + 10
        if stat_points > 0:
            self.allocate_stats(stat_points)
        print("Current experience:\t" + str(self.exp_value))
        print("Experience required for the next level:\t" + str(exp_requirement))
        
        
    def show_stats(self):
        """ Print out the stats for a player. """
        print("Your current stats are (+equipment): " +
              "\n\t Health: " + "\t" + str(self.max_health) + "(+" + str(self.e_armor.strength) + ")"
              "\n\t Strength: " + "\t" + str(self.strength) + "(+" + str(self.e_sword.strength) + ")"
              "\n\t Speed: " + "\t" + str(self.speed) + "(*" + str(self.e_armor.weight) + ")")
        
    def allocate_stats(self, points):
        self.show_stats()
        print()
        while points != 0:
            print("You have " + str(points) + " points to put into your stats.")
            stat_name = input("Which stat would you like to increase? \t")
            if stat_name.lower() == "health":
                stat_value = int(input("How much would you like to add?\t"))
                if stat_value > points:
                    print("Invalid amount.")
                else:
                    points = points - stat_value
                    self.max_health = self.max_health + stat_value
            elif stat_name.lower() == "strength":
                stat_value = int(input("How much would you like to add?\t"))
                if stat_value > points:
                    print("Invalid amount.")
                else:
                    points = points - stat_value
                    self.strength = self.strength + stat_value
            elif stat_name.lower() == "speed":
                stat_value = int(input("How much would you like to add?\t"))
                if stat_value > points:
                    print("Invalid amount.")
                else:
                    points = points - stat_value
                    self.speed = self.speed + stat_value
            else:
                print("Stat name entered incorrectly, try again.")
            print()
        self.show_stats()
    
    def calculated_health(self):
        return self.max_health + self.e_armor.strength
    
    def calculated_strength(self):
        return self.strength + self.e_sword.strength
    
    def calculated_speed(self):
        return self.speed * self.e_armor.weight
    
    def display_items(self):
        if self.backpack:
            print("Contents of your backpack: ")
            for item in self.backpack.values():
                item.print()
            
    def add_item(self, item):
        if item.name in self.backpack.keys():
            item_in_backpack = self.backpack[item.name]
            item.value += item_in_backpack.value
            if(type(item) != Etc):
                item.strength += item_in_backpack.strength
        self.backpack.update({ item.name : item})
    
    def remove_item(self, item_name):
        if item_name.lower() in self.backpack.keys():
            del self.backpack[item_name]
    
    def equip_item(self, item_name):
        if item_name.lower() in self.backpack.keys():
            item_name = item_name.lower()
            item = self.backpack[item_name]
            
            if type(item) == Sword:
                if self.e_sword.name == "none":
                    self.e_sword = item
                    self.remove_item(item_name)
                else:
                    self.add_item(self.e_sword)
                    self.e_sword = item
                    self.remove_item(item_name)
            elif type(item) == Armor:
                if self.e_armor.name == "none":
                    self.e_armor = item
                    self.remove_item(item_name)
                else:
                    self.add_item(self.e_armor)
                    self.e_armor = item
                    self.remove_item(item_name)
            else:
                print(item.name + " is not equippable.")
        else:
            print("You do not have " + item_name)
    
    def use_item(self, item_name):
        if item_name.lower() in self.backpack.keys():
            item_name = item_name.lower()
            item = self.backpack[item_name]
            
            if type(item) == Potion:
                self.curr_health = self.curr_health + item.strength
                if self.curr_health > self.calculated_health():
                    self.curr_health = self.calculated_health()
                self.remove_item(item_name)
                
            elif type(item) == Sword or type(item) == Armor:
                self.equip_item(item_name)
                
            else:
                print("You cannot use this item!")
        else:
            print("You do not have " + item_name)
    
    def attack(self, mob):
        damage = random.randint(self.calculated_strength() - 2,self.calculated_strength() + 2)
        if random.random() < 0.05:
            damage = damage ** 2
            print("\tCRITICAL STRIKE - You dealt " + str(damage) + " damage.")
        else:
            print("\tYou attacked the monster and dealt " + str(damage) + " damage.")
        mob.health = mob.health - damage
        
    def fight(self, mob):
            if self.calculated_speed() > mob.speed:
                self.attack(mob)
                if(mob.status()):
                    mob.attack(self)
            elif self.calculated_speed() < mob.speed:
                mob.attack(self)
                if(self.status()):
                    self.attack(mob)
            else:
                if random.random() < .5:
                    self.attack(mob)
                    if(mob.status()):
                        mob.attack(self)
                else:
                    mob.attack(self)
                    if(self.status()):
                        self.attack(mob)                
            
        
    def run_from(self, mob):
        run_away_chance = 0.75
        if self.calculated_speed() < mob.speed:
            run_away_chance = 0.50
        return random.random() <= run_away_chance
    
    def status(self):
        return self.curr_health > 0
    
    


# In[7]:


class Mob():
    common_loot = [ Sword(),
                    Potion(strength=5),
                    Armor(strength=5, weight=0.75)]
    rare_loot = [ Sword(name="scimitar",value=10,strength=7),
                  Sword(name="two-handed sword",value=5,strength=10),
                  Potion(name="poison",value=5,strength=-15),
                  Potion(name="elixir",value=10, strength=20),
                  Armor(name="chainmail", value=7)]
    super_loot = [ Sword(name="slayer",value=99,strength=99),
                   Armor(name="impenetrable defense",value=99,strength=99,weight=0.10),
                   Armor(name="ungodly boots", value=99, strength=-5, weight=2)]
    
    def __init__(self, name, health, strength, speed, d):
        self.name = name
        self.health = floor(health * d)
        self.strength = floor(strength * d)
        self.speed = floor(speed * d)
        self.difficulty = d
        
    def drop_loot(self, base_rate=0.25):
        num = random.random()
        item = None
        if num < base_rate:
            num = random.random()
            if num < 0.05:
                item = random.choice(self.super_loot)
            elif num < 0.25:
                item = random.choice(self.rare_loot)
            elif num < 0.75:
                item = random.choice(self.common_loot)
            else:
                item = Etc(value=random.randint(0,5))
        return item
    
    def attack(self, player):
        upper_bound = self.strength + 2
        lower_bound = self.strength - 2
        if lower_bound < 0:
            lower_bound = 0
        damage = random.randint(lower_bound, upper_bound)
        
        if random.random() < 0.05:
            damage = damage ** 2
            print("\tCRITICAL STRIKE - It dealt " + str(damage) + " damage.")
        else:
            print("\tIt attacked you and dealt " + str(damage) + " damage.")
        player.curr_health = player.curr_health - damage
            
    def print_undiscovered(self):
        print("\t"+self.name + " can be heard somewhere in the distance...")
        print("\t\t| health\t?")
        print("\t\t| strength\t?")
        print("\t\t| speed \t?")
        
    def print_encountered(self):
        print("\t"+self.name + " has appeared.")
        print("\t\t| health\t" + str(self.health))
        print("\t\t| strength\t" + str(self.strength))
        print("\t\t| speed \t" + str(self.speed))
        
class Heavy(Mob):
    def __init__(self, health=50, strength=5, speed=1, d = 1):
        super().__init__("a large beast", health, strength, speed, d)
        self.exp_value = floor(20 * d)
        
    def status(self):
        if self.health <= 0:
            return False
        else:
            return True
        
class Normal(Mob):
    def __init__(self, health=20, strength=3, speed=5, d = 1):
        super().__init__("an animal", health, strength, speed, d)
        self.exp_value = floor(15 * d)
        
    def status(self):
        if self.health <= 0:
            return False
        else:
            return True
        
        
class Quick(Mob):
    def __init__(self, health=5, strength=1, speed=10, d = 1):
        super().__init__("many small creatures", health, strength, speed, d)
        self.base_health = health
        self.exp_value = floor(10 * d)
        self.lives = 5

    def status(self):
        if self.health <= 0:
            if self.lives == 0:
                return False
            else:
                print("\tOne has died, but many more fill its place")
                self.lives = self.lives - 1
                self.health = self.base_health
                return True
    
    def print_encountered(self):
        print("\t"+self.name + " have appeared.")
        print("\t\t| health\t" + str(self.health))
        print("\t\t| strength\t" + str(self.strength))
        print("\t\t| speed \t" + str(self.speed))
        
class Aberrant(Mob):
    def __init__(self, d = 1):
        r = random
        health = r.randint(10,30)
        strength = r.randint(8, 15)
        speed = r.randint(1, 10)
        super().__init__("an abberant", health, strength, speed, d)
        self.exp_value = floor(99 * d)
      
    def status(self):
        if self.health <= 0:
            return False
        else:
            return True

