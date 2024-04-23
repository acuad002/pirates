
from game import location
import game.config as config
from game.display import announce
from game.events import *
import game.items as items

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

    def enter (self):
        announce ("arrive at a beach on the southernmost tip of the island and anchor your ship.")

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

    def enter (self):
        announce ("you enter into the dense forest to the north. The leaves on the trees block out most of the sunlight as you progress further.")

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

    def enter (self):
        announce ("The trees part to reveal the base of a large cliff. There is a mysterious aura about it.")

    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "south"):
            announce ("You decide to do a u-turn and reenter the dense forest.")
            config.the_player.next_loc = self.main_location.locations["forest"]
        elif (verb == "north"):
            config.the_player.next_loc = self.main_location.locations["entrance"] 
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
        self.event_chance = 0

    def enter (self):
        announce ("You encounter a small campfire, and much to your surpise, you are not alone. A travelling merchant has set up shop by the fire.")

    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "west"):
            announce ("You leave the merchant and return to the dense forest you came from.")
            config.the_player.next_loc = self.main_location.locations["forest"]
        elif (verb == "north" or verb == "south" or verb == "east"):
            announce ("The forest is too dense to proceed and you return to the travelling merchant's fire.")

class Clearing (location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "clearing"
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self
        self.event_chance = 0

    def enter (self):
        announce ("You enter a small clearing where the sun beams down. In the distance, you see a strange whispy figure. You advance towards it.")

    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "south"):
            config.the_player.next_loc = self.main_location.locations["glade"] #firefly glade
        elif (verb == "north"):
            announce ("Somehow, you find yourself in front of the cliff again.")
            config.the_player.next_loc = self.main_location.locations["cliff"]
        elif (verb == "east"):
            config.the_player.next_loc = self.main_location.locations["cliff"]
        elif (verb == "west"):
            announce ("Something tells you that you should seek another direction.")

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

    def enter (self):
        description = "You enter another set of dense trees until they once again part to a small glade. Despite you knowing it should still be daytime, the night sky is lit above your head. A multitude of fireflies flicker across the grass."
        if self.item_in_grass != None:
            description = description + " In the distance, you see a different glimmer that attracts your attention."
        announce (description)

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

    def enter (self):
        announce ("You enter the hidden cavern. Two paths are ahead, one to the east and one to the west. In the darkness, they both appear to be the same.")

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

    def enter (self):
        announce ("Something happens.")

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
        self.event_chance = 0

    def enter (self):
        announce ("You encounter a large ravine.")

    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "west"):
            announce ("You return to the cave entrance.")
            config.the_player.next_loc = self.main_location.locations["entrance"]
        elif (verb == "north"):
            config.the_player.next_loc = self.main_location.locations["treasure"] 
        elif (verb == "south" or verb == "east"):
            announce ("There is no way forward.")

class TreasureRoom (location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "treasure"
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self
        self.event_chance = 0

    def enter (self):
        announce ("You found treasure!")

    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "south"):
            announce ("You return to the ravine.")
            config.the_player.next_loc = self.main_location.locations["ravine"]
        elif (verb == "north" or verb == "east" or verb == "west"):
            announce ("There is no way forward.")

class Spyglass (items.Item):
    def __init__(self):
        super().__init__("enchanted spyglass", 1000)