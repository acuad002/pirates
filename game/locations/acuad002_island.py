
from game import location
import game.config as config
from game.display import announce
from game.events import *
import game.items as items
import random

class MysteriousIsland (location.Location):
    def __init__ (self, x, y, w):
        super().__init__(x, y, w)
        self.name = "mysterious island"
        self.symbol = 'M'
        self.visitable = True
        self.starting_location = SouthBeach (self)
        self.locations = {}
        self.locations["south beach"] = self.starting_location
        self.locations["forest"] = DenseForest (self)
        self.locations["cliff"] = CliffCavern (self)
        self.locations["campfire"] = Campfire (self)
        self.locations["clearing"] = Clearing (self)
        self.locations["glade"] = FireflyGlade (self)
        self.locations["entrance"] = CaveEntrance (self)
        self.locations["danger"] = DeathlyCavern (self)
        self.locations["ravine"] = Ravine (self)
        self.locations["treasure"] = TreasureRoom (self)
        self.ghost = False

    def enter (self, ship):
        print ("arrived at a mysterious island")

    def visit (self):
        config.the_player.location = self.starting_location
        config.the_player.location.enter()
        super().visit()

class SouthBeach (location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "south beach"
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self
        self.event_chance = 0
        self.first_visit = True

    def enter (self):
        if self.first_visit == True:
            announce ("arrive at a beach on the southernmost tip of the island and anchor your ship.")
            self.first_visit = False
        else:
            announce ("You've arrived at the southernmost beach. To the south, you see your achored ship.")

    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "south"):
            announce ("You return to your ship.")
            config.the_player.next_loc = config.the_player.ship
            config.the_player.visiting = False
        elif (verb == "north"):
            config.the_player.next_loc = self.main_location.locations["forest"]
        elif (verb == "east" or verb == "west"):
            announce ("You walk along the beach in search for treasure. Sadly, you do not find anything of interest and return to the south beach.")

class DenseForest (location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "forest"
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self
        self.event_chance = 0
        self.first_visit = True

    def enter (self):
        if self.first_visit == True:
            announce ("you enter into the dense forest to the north. The leaves on the trees block out most of the sunlight as you progress further.")
            self.first_visit = False
        else:
            announce ("You arrive in the dense forest.")

    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "south"):
            announce ("Perhaps in fear or utter confusion, you decide to retrace your steps and return to the southern beach.")
            config.the_player.next_loc = self.main_location.locations["south beach"]
        elif (verb == "north"):
            config.the_player.next_loc = self.main_location.locations["cliff"] 
        elif (verb == "east"):
            config.the_player.next_loc = self.main_location.locations["campfire"]
        elif (verb == "west"):
            announce ("The forest appears too dense to proceed to the west. Maybe another direction would be a better choice.")

class CliffCavern (location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "cliff"
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self
        self.event_chance = 0
        self.first_visit = True
        self.first_solve = True

    def enter (self):
        if self.first_visit == True:
            announce ("The trees part to reveal the base of a large cliff. There is a mysterious aura about it.")
            self.first_visit = False
        else:
            announce ("You return to the base of the mysterious cliff.")
        if self.main_location.ghost == True:
            if self.first_solve == True:
                announce ("BLACKEYE: Blimey! Something is off about that cliff lad... I think it was a key piece to finding the treasure, but I don't remember how... Something about enchantments, perhaps.")
        

    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "south"):
            announce ("You decide to do a u-turn and reenter the dense forest.")
            config.the_player.next_loc = self.main_location.locations["forest"]
        elif (verb == "north"):
            spyglass_in_inv = spyglass_in_inventory()
            if spyglass_in_inv == True:
                if self.main_location.ghost == True:
                    if self.first_solve == True:
                        announce ("BLACKEYE: Arrrr! Well done matey! Ye solved the puzzle! But something tells me there's still more to this place...")
                        self.first_solve = False
                config.the_player.next_loc = self.main_location.locations["entrance"]
            else:
                announce ("You examine the cliff wall closely. Yup, definitely a cliff. You determine, rather astutely, that there is no way forward.") 
        elif (verb == "west"):
            config.the_player.next_loc = self.main_location.locations["clearing"]
        elif (verb == "east"):
            announce ("You proceed to the east, get lost, and wind up back at the cliff.")

class Campfire (location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "campfire"
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self
        self.verbs['yes'] = self
        self.verbs['no'] = self
        self.event_chance = 0
        self.merch_item = Orb()

    def enter (self):
        if self.merch_item == None:
            announce ("You find yourself by the abandonned campfire previously occupied by the merchant. Despite the fire being out, a faint smoke continues to elevate from the tinder. It doesn't appear like there's anything to do here.")
        else:
            announce ("You encounter a small campfire, and much to your surprise, you are not alone. A travelling merchant has set up shop by the fire.")
            announce ("MERCHANT: Hello there, welcome, welcome! Yes, please feel free to sit by the fire! Tell me, since we're friends now, what would you say if we did a little trade? This shiny orb for one of your items? I'll pick a random one, no taking back if you agree!")

    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "west"):
            announce ("You leave the merchant and return to the dense forest you came from.")
            config.the_player.next_loc = self.main_location.locations["forest"]
        elif (verb == "north" or verb == "south" or verb == "east"):
            announce ("The forest is too dense to proceed and you return to the travelling merchant's fire.")
        elif (verb == "yes"):
            if self.merch_item == None:
                description = "What exactly are you saying yes to? There is nobody around."
                if self.main_location.ghost == True:
                    announce("BLACKEYE: "+description)
                else:
                    announce(description)
            item = self.merch_item
            c = random.choice(config.the_player.inventory)
            while type(c) == Spyglass:
                c = random.choice(config.the_player.inventory)
            config.the_player.inventory.remove(c)
            config.the_player.add_to_inventory([item])
            self.merch_item = None
            config.the_player.go = True
            announce("MERCHANT: Splendid, I'll take that! Enjoy your new shiny, useless orb! See ya!")
            announce("The merchant gathers his belongings and speeds off into the dense forest, bringing one of your items with him.")

class Clearing (location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "clearing"
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self
        self.verbs['yes'] = self
        self.verbs['no'] = self
        self.event_chance = 0
        self.first_visit = True

    def enter (self):
        announce ("You enter a small clearing where the sun beams down.") 
        if self.first_visit == True:
            if self.main_location.ghost == False:
                announce ("In the distance, you see a strange whispy figure. You advance towards it.")
                announce ("GHOST: Arrrr! Oh! Ahoy, Matey! Ye startled me, I almost lost me boots! Who am I, you ask?")
                announce ("BLACKEYE: Why, I am Captain Blackeye, although me eyes are much paler these days. Long ago, I failed to find the treasure of this island... But if ye were to take me along with ye, I will make it worth yerr while! Whadya say, matey, will you take me along with ye?")
            self.first_visit = False
        else:
            if self.main_location.ghost == False:
                announce ("BLACKEYE: Arrr, ye return eh? Well, have ye changed yer minds? Will ye take me along on yer quest?")

    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "south"):
            config.the_player.next_loc = self.main_location.locations["glade"] 
        elif (verb == "north"):
            announce ("Somehow, you find yourself in front of the cliff again.")
            config.the_player.next_loc = self.main_location.locations["cliff"]
        elif (verb == "east"):
            config.the_player.next_loc = self.main_location.locations["cliff"]
        elif (verb == "west"):
            announce ("Something tells you that you should seek another direction.")
        elif (verb == "yes"):
            self.main_location.ghost = True
            announce ("BLACKEYE: Arrrr, I promise ye made the right choice lad!")
        elif (verb == "no"):
            announce ("BLACKEYE: Arrr, ye shall regret ye choice matey.")

class FireflyGlade (location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "glade"
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self
        self.event_chance = 0
        self.verbs['take'] = self
        self.item_in_grass = Spyglass()
        self.first_visit = True

    def enter (self):
        if self.first_visit == True:
            announce ("You enter another set of dense trees until they once again part to a small glade. Despite you knowing it should still be daytime, the night sky is lit above your head. A multitude of fireflies flicker across the grass.")
            self.first_visit = False
        else:
            announce ("You once again find yourself in the enchanted firefly glade.")
        if self.item_in_grass != None:
            announce (" In the distance, you see a different glimmer that attracts your attention.")
        

    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "north"):
            config.the_player.next_loc = self.main_location.locations["clearing"] 
        elif (verb == "north" or verb == "east" or verb == "west"):
            announce ("You proceed to the edge of the glade, but some bizarre, invisible force prevents you from going any further.")
        if (verb == "take"):
            if self.item_in_grass == None:
                announce ("You don't see anything to take.")
            item = self.item_in_grass
            if item != None:
                announce ("You pick up the "+item.name+" from the grass.")
                config.the_player.add_to_inventory([item])
                self.item_in_grass = None
                if self.main_location.ghost == True:
                    announce("BLACKEYE: Shiver me timbers! Ye found me ol' enchanted spyglass! I pillaged it from an old wench long ago. She was feared by many, but not by ol' Blackeye! Oh, no! See, it is enchanted to reveal truths hidden to the naked eye. One of me most prized possessions! Take care of it, will ye?")
                config.the_player.go = True


class CaveEntrance (location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "entrance"
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self
        self.event_chance = 0
        self.first_visit = True

    def enter (self):
        if self.first_visit == True:
            announce ("You enter the hidden cavern. Two paths are ahead, one to the east and one to the west. In the darkness, they both appear to be the same.")
            if self.main_location.ghost == True:
                announce ("BLACKEYE: Avast, matey! This cavern is dangerous! One of these lead to a trap, and one moves forward, but me ol' mind can't recall which way is which. Make the right choice, matey, or one of ye may feed the fish.")
            self.first_visit = False
        else:
            announce ("You enter into the cavern and encounter the same branching road. The two paths are to the east and the west.")

    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "south"):
            announce ("You decide not to proceed any furhter, perhaps by fear of the dark, and return to the cliffside.")
            config.the_player.next_loc = self.main_location.locations["cliff"]
        elif (verb == "west"):
            config.the_player.next_loc = self.main_location.locations["danger"] 
        elif (verb == "east"):
            config.the_player.next_loc = self.main_location.locations["ravine"] 
        elif (verb == "north"):
            announce ("There is no way north from here.")

class DeathlyCavern (location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "danger"
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self
        self.event_chance = 0
        self.first_visit = True

    def enter (self):
        if self.first_visit == True:
            announce("You hear a click and a poisonous dart shoots across the chamber towards one of your crewmates.")
            c = random.choice(config.the_player.get_pirates())
            result = {}
            if (c.isLucky() == True):
                announce("That was a close one! " + c.get_name() + " managed to avoid the poison dart!")
            else:
                damage = 20
                deathcause = "died to the poison dart."
            died = c.inflict_damage (damage, deathcause)
            if (died == True):
                result = c.get_name() + " died to the poison dart."
            else:
                result = c.get_name() + " got hit with the poison dart."
            announce(result)
            if self.main_location.ghost == True:
                announce("BLACKEYE: I warned ye matey... If only me mind weren't in the clouds. Let's return back to the entrance and enter the other chamber.") 
            self.first_visit = False
        else: 
            announce ("You enter the cavern where the poison dart shot from. Thankfully, the trap is now disarmed and poses no further danger to your crew.")


    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "east"):
            announce ("You return to the cave entrance.")
            config.the_player.next_loc = self.main_location.locations["entrance"]
        elif (verb == "north" or verb == "west" or verb == "south"):
            announce ("There is no way forward here.")

class Ravine (location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "ravine"
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self
        self.verbs['jump'] = self
        self.verbs['place'] = self
        self.event_chance = 0
        self.first_visit = True
        self.first_solve = True

    def enter (self):
        if self.first_visit == True:
            announce ("You encounter a ravine. Across from it, you see a tunnel shining with light. Is that where the treasure is? Only one way to find out.")
            announce ("It appears that the ravine is short enough to jump across, if you dare. To your right, you notice a pedestal with a perfectly spherical indent. Wonder what that's for.")
            if self.main_location.ghost == True:
                announce ("BLACKEYE: Arrrr, I remember this chamber! T'is where I lost me life! I wish I could help, but I don't know what to do here.")
            self.first_visit = False
        else:
            if self.first_solve == True:
                announce ("You once again enter the cavern containing the ravine. The path across is still uncertain, and the mysterious pedestal with a spherical indent remains untouched.")
            else:
                announce ("You enter the cavern with the ravine. The enchanted bridge is still there, allowing safe passage across the bottomless trap.")
        if self.first_solve == True:
            orb_in_inv = orb_in_inventory()
            if orb_in_inv == True:
                announce ("Maybe that orb the merchant gave you would be useful here. Try placing it on the pedestal.") 

    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "west"):
            announce ("You return to the cave entrance.")
            config.the_player.next_loc = self.main_location.locations["entrance"] 
        elif (verb == "south" or verb == "east"):
            announce ("There is no way forward.")
        elif (verb == "north"):
            if self.first_solve == True:
                announce ("The ravine is north. Maybe you can try jumping?")
            else:
                config.the_player.next_loc = self.main_location.locations["treasure"]
                announce ("You cross the enchanted bridge towards the shinning cavern.")

        elif (verb == "jump"):
            c = random.choice(config.the_player.get_pirates())
            result = {}
            announce(c.get_name() + " ran and attempted to jump across the ravine. As they were in midair, the ravine grew magically larger. There's no way they'll make it that far across!")
            if (c.isLucky() == True):
                announce("You managed to catch " + c.get_name() + "'s hand just in time to stop them from falling. How lucky!")
            else:
                damage = 50
                deathcause = "died from jumping into the ravine."
            died = c.inflict_damage (damage, deathcause)
            if (died == True):
                result = c.get_name() + " died from jumping into the ravine."
            else:
                result = c.get_name() + " fell into the ravine. Thankfully, they survived and are able to make their way back up."
            announce(result)
            config.the_player.go = True
        elif (verb == "place"):
            orb_in_inv = orb_in_inventory()
            if orb_in_inv == True:
                announce ("You decide to place the orb on the pedestal. A bright light shines around it as the earth shakes and the pedestal slowly lowers into the cave ground and disappears. As the ground continues to shake, a bridge materializes from the stone at the bottom of the ravine. There's now a way across!")
                announce ("You feel something in your pocket and realize the orb has returned to you. How is the bridge still there? That's really strange...")
                if self.main_location.ghost == True:
                    announce ("BLACKEYE: Shiver me timbers! Ye solved the puzzle me crew and I could not figure out! Well done! Let's move forward, me ol' nose can smell treasure!")
                self.first_solve = False

class TreasureRoom (location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "treasure"
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self
        self.verbs['take'] = self
        self.event_chance = 0
        self.treasure = Gemstones()

    def enter (self):
        if self.treasure != None:
            announce ("You enter the cavern where the glowing light is eminating from. Once your eyes have adjusted to the blinding light, you see a large chamber filled with precious gemstones from floor to ceiling.")
            announce ("BLACKEYE: Blimey! Look at all the treasure lads! Hurry, gather it before some scallywag claims our well-deserved loot!")
        else:
            announce ("You stand in the middle of the barren cavern that was once covered in the gemstones your crew gathered.")

    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "south"):
            announce ("You return to the ravine.")
            config.the_player.next_loc = self.main_location.locations["ravine"]
        elif (verb == "north" or verb == "east" or verb == "west"):
            announce ("There is no way forward.")
        elif (verb == "take"):
            if self.treasure == None:
                if self.main_location.ghost == True:
                    announce ("BLACKEYE: Ye already gathered it all, lads! Someone got themself into the grog early!")
                else:
                    announce ("You've already gathered all the treasure!")
            item = self.treasure
            if item != None:
                announce ("BLACKEYE: Heave Ho, lads! Ol' Blackeye would help ye, but me spectral form confines me to the role of lookout!")
                announce ("The crew disperses to gather all the "+item.name+" in the chamber. It takes hours for them to gather it all, but the sheer thought of their newly acquired riches is enough to push them forward.")
                config.the_player.add_to_inventory([item])
                self.treasure = None
                if self.main_location.ghost == True:
                    announce("BLACKEYE: Ha HA! Ye did it lads! Ye made ol' Blackeye proud. May ye calabrate yer plunder o'er a well-earned grog!")
                    announce ("Congratulations, you have collected this island's treasure!")
                config.the_player.go = True


class Spyglass (items.Item):
    def __init__(self):
        super().__init__("enchanted spyglass", 1000)

class Orb (items.Item):
    def __init__(self):
        super().__init__("shiny orb", 500)

class Gemstones (items.Item):
    def __init__(self):
        super().__init__("gemstones", 5000)

def spyglass_in_inventory():
    for i in config.the_player.inventory:
        if type (i) == Spyglass:
            return True

def orb_in_inventory():
    for i in config.the_player.inventory:
        if type(i) == Orb:
            return True
        