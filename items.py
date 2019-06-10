
# coding: utf-8

# In[1]:


class Item():
    def __init__(self, name, value):
        self.name = name
        self.value = value
    
    def sell(self):
        return value
    
    def print(self):
        raise NotImplementedError("This method has not been implemented.")
    
class Etc(Item):
    def __init__(self, name="trash", value=0):
        super().__init__(name, value)
    
    def print(self):
        print("\t" + self.name)
        print("\t\t| value: " + str(self.value))
        
class Sword(Item):
    def __init__(self, name="sword", value=5, strength=5):
        super().__init__(name, value)
        self.strength = strength
        
    def print(self):
        print("\t" + self.name)
        print("\t\t| value: " + str(self.value))
        print("\t\t| strength: " + str(self.strength))
        
class Potion(Item):
    def __init__(self, name="potion", value=1, strength=5):
        super().__init__(name, value)
        self.strength = strength
    
    def print(self):
        print("\t" + self.name)
        print("\t\t| value: " + str(self.value))
        print("\t\t| strength: " + str(self.strength))
        
class Armor(Item):
    def __init__(self, name="armor", value=3, strength=15, weight=0.5):
        super().__init__(name, value)
        self.strength = strength
        self.weight = weight
    
    def print(self):
        print("\t" + self.name)
        print("\t\t| value: "+ str(self.value))
        print("\t\t| strength: "+ str(self.strength))
        print("\t\t| weight (encumberment): "+ str(self.weight))

