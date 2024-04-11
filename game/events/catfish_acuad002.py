from game import event
from game.player import Player
from game.context import Context
import game.config as config
import random

class Catfish (Context, event.Event):
    '''Encounter with a harmless catfish. Uses the parser to decide what to do about it.'''
    def __init__ (self):
        super().__init__()
        self.name = "catfish visitor"
        self.catfish = 1
        self.verbs['catch'] = self
        self.verbs['feed'] = self
        self.verbs['ignore'] = self
        self.result = {}
        self.go = False

    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "catch"):
            self.go = True
            r = random.randint(1,10)
            if (r < 5):
                self.result["message"] = "The catfish was caught."
                if (self.catfish > 1):
                    self.catfish = self.catfish - 1
                    config.the_player.ship.food += 3 #when catching a fish, it adds 3 food to reserves
                    
            else:
                c = random.choice(config.the_player.get_pirates())
                if (c.isLucky() == True):
                    self.result["message"] = "Luckly, the catfish was caught."
                    config.the_player.ship.food += 3
                    #add food to inventory
                else:
                    self.result["message"] = "Oh no! The catfish got away."

        elif (verb == "feed"):
            self.result["newevents"].append (Catfish())
            self.result["message"] = "the catfish are happy and swim away."
            self.go = True
        elif (verb == "help"):
            print ("catfish are harmless, but definitely look tasy... Feeding them may also come in useful later.")
            self.go = False
        else:
            print ("it seems the only options here are to catch, feed, or ignore")
            self.go = False



    def process (self, world):

        self.go = False
        self.result = {}
        if self.catfish == 0:
            self.result["newevents"] = [ self, Catfish()]
        else:
             self.result["newevents"] = [ self ]
        self.result["message"] = "default message"

        while (self.go == False):
            print (str (self.catfish) + " a catfish has appeared what do you want to do?")
            Player.get_interaction ([self])

        return self.result