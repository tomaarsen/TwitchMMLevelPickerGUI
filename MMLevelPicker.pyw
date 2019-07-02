
from TwitchWebsocket import TwitchWebsocket
import random, time, json, logging, re

from Log import Log
Log(__file__)

from Settings import Settings
from Database import Database
from App import App
from View import View
from View import MessageSource

class Level:
    # Simple data structure to store weight and time of a user who chatted.
    def __init__(self, user, code, weight):
        self.user = user
        self.code = code
        self.weight = weight

class MMLevelPicker:
    def __init__(self, db):
        self.host = None
        self.port = None
        self.chan = None
        self.nick = None
        self.auth = None
        self.months_per_chance = None
        self.capability = "tags"
        self.db = db
        self.app = None
        self.view = View(self)
        
        # Fill previously initialised variables with data from the settings.txt file
        Settings(self)

    def start(self):
        self.ws = TwitchWebsocket(host=self.host, 
                                  port=self.port,
                                  chan=self.chan,
                                  nick=self.nick,
                                  auth=self.auth,
                                  callback=self.message_handler,
                                  capability=self.capability,
                                  live=True)
        self.ws.start_nonblocking()

    def stop(self):
        try:
            self.ws.join()
        except AttributeError:
            # If self.ws has not yet been instantiated. 
            # In this case we have essentially already stopped
            pass

    # Used from GUI
    def set_login_settings(self, host, port, chan, nick, auth):
        self.host = host
        self.port = port
        self.chan = chan
        self.nick = nick
        self.auth = auth
    
    def set_settings(self, host, port, chan, nick, auth, allowed_ranks, allowed_people, months_per_chance):
        self.set_login_settings(host, port, chan, nick, auth)
        self.allowed_ranks = allowed_ranks
        self.allowed_people = allowed_people
        self.months_per_chance = months_per_chance

    def message_handler(self, m):
        try:
            if m.type == "366":
                self.app.now_running()
            
            if m.type == "PRIVMSG":
                if m.message.startswith("!addlevel"):
                    self.handle_add_level(m)
                elif m.message.startswith("!nextlevel") and self.check_permissions(m):
                    self.handle_next_level()
                elif m.message.startswith(("!level", "!current")):
                    self.handle_current_level()
                elif m.message.startswith("!clearlevel") and self.check_permissions(m):
                    self.handle_clear_level()
                elif m.message.startswith(("!levelhelp", "!helplevel")):
                    self.handle_help()

        except Exception as e:
            logging.exception(e)

    def check_permissions(self, m):
        for rank in self.allowed_ranks:
            if rank in m.tags["badges"]:
                return True
        for name in self.allowed_people:
            if m.user.lower() == name.lower():
                return True
        return False
    
    def get_weight(self, m):
        # Get badges
        badges = m.tags["badge-info"]
        # I assume that badge-info would be split by commas. I can only find instances where badge-info contains "subscriber/...", however.
        badges_list = badges.split(",")
        # Set the standard weight, 1
        weight = 1
        # Get the bonus from the badge
        for badge in badges_list:
            badge_data = badge.split("/")
            if badge_data[0] == "subscriber":
                months = int(badge_data[1])
                # The bonus weight is: months / 6
                weight += months / 6
                break
        return weight

    def handle_add_level(self, m):
        # Get the full message
        message = m.message
        # Split by space
        message_list = message.split()
        if len(message_list) != 2:
            self.view.output("The command is !addlevel XXX-XXX-XXX.", MessageSource.ADD_LEVEL_ERROR)
        else:
            # Get the code
            code = message_list[-1].upper()
            # Check if the code matches the correct format of XXX-XXX-XXX
            if re.match("[A-Z|0-9]{3}-[A-Z|0-9]{3}-[A-Z|0-9]{3}", code):
                # Add the level. It might return a warning
                source = self.db.add_level(m.tags["display-name"], code, self.get_weight(m))
                if source == MessageSource.ADD_LEVEL_WARNING:
                    self.view.output("Your previous code has been overridden.", MessageSource.ADD_LEVEL_WARNING)
                elif source == MessageSource.ADD_LEVEL_ERROR:
                    self.view.output("Your level is already the current level.", MessageSource.ADD_LEVEL_ERROR)
                elif source == MessageSource.ADD_LEVEL_SUCCESS:
                    self.view.output("Your code has been added.", MessageSource.ADD_LEVEL_SUCCESS)
                self.app.update_levels()
            else:
                self.view.output("The format for the code is: XXX-XXX-XXX.", MessageSource.ADD_LEVEL_ERROR)
    
    def handle_next_level(self):

        # Get all the data from the levels, including weight
        data = self.db.get_levels_weight()

        # Randomly choose r as an int between 0 and the total amount of weight total
        total = sum(tup[2] for tup in data)
        if total == 0:
            self.view.output("No levels currently in queue.", MessageSource.NEXT_LEVEL_ERROR)
            return
        r = random.uniform(1, total)
        
        # Continuously reduce r by the weight while looping through all levels, 
        # until it would have resulted in a negative (or zero) r.
        # When this happens, return the name of the user that won.
        for tup in data:
            if tup[2] >= r:
                winner = tup
                break
            r -= tup[2]

        user = winner[0]
        code = winner[1]
        self.db.set_new_current(user, code)
        self.app.update_levels()
        self.view.output(f"{user}'s level with code {code} has been picked as the next level!", MessageSource.NEXT_LEVEL_SUCCESS)

    def handle_current_level(self):
        # Get the current level
        current = self.db.get_current_level()
        if len(current) == 0:
            self.view.output("There is no current level.", MessageSource.CURRENT_LEVEL_ERROR)
            return

        self.view.output(f"Creator: {current[0][0]}, Code: {current[0][1]}", MessageSource.CURRENT_LEVEL_SUCCESS)

    def handle_clear_level(self):
        # Clear the database of levels
        self.db.clear()

        self.view.output(f"The levels have been cleared.", MessageSource.CLEAR_LEVEL_SUCCESS)

        self.app.update_levels()
    
    def handle_help(self):
        
        self.view.output(f"Commands: !addlevel XXX-XXX-XXX to add your level, !current/!level to get the code of the current level. This is not a queue, it's a semi-random drawing between all added levels!", MessageSource.HELP)

if __name__ == "__main__":
    db = Database()
    bot = MMLevelPicker(db)
    app = App(bot, db)
    bot.app = app
