# TwitchMMLevelPickerGUI
Twitch bot which semi-randomly picks Mario Maker 2 Levels from chat

---

# Explanation
When the bot has started, it will open up this GUI:

![image](https://user-images.githubusercontent.com/37621491/60506964-55989a00-9cc7-11e9-8381-dec8f24be42a.png)

The bot connected to this GUI will, when "Run" is pressed, allow chat members to add their levels to the drawing. When the streamer wishes to play a level, they can semi-randomly generate a level to play from the list of levels. It's possible to give subscribers a higher chance of winning this drawing, based on how many months they have been subscribed.  
In short, this bot allows streamers to fairly pick chat levels with just one click.

--- 

# Commands

<pre>
<b>!addlevel XXX-XXX-XXX</b>
</pre>
- Adds the level with code XXX-XXX-XXX to the list.<br>
- Anyone can use this.
---
<pre>
<b>!nextlevel</b>
</pre>
- Semi-randomly generates the next level to be played.<br>
- Anyone with the allowed rank can use this. (See [Settings](https://github.com/CubieDev/TwitchMMLevelPicker/blob/master/README.md#Settings) for more information)
---
<pre>
<b>!level/!current/!currentlevel</b>
</pre>
- Shows the creator and code of the current level in the chat.
- Anyone can use this.
---
<pre>
<b>!clearlevel</b>
</pre>
- Clears the list of levels
- Anyone with the allowed rank can use this. (See [Settings](https://github.com/CubieDev/TwitchMMLevelPicker/blob/master/README.md#Settings) for more information)
---
<pre>
<b>!levelhelp/!helplevel</b>
</pre>
- Shows information about the commands everyone can use.
- Anyone can use this.

---

# Settings
This bot is controlled by a settings.txt file, which looks like:
```
{
    "Host": "irc.chat.twitch.tv",
    "Port": 6667,
    "Channel": "#<channel>",
    "Nickname": "<name>",
    "Authentication": "oauth:<auth>",
    "AllowedRanks": [
        "broadcaster",
        "moderator"
    ],
    "AllowedPeople": [],
    "MonthsPerChance": 6
}
```

| **Parameter**        | **Meaning** | **Example** |
| -------------------- | ----------- | ----------- |
| Host                 | The URL that will be used. Do not change.                         | "irc.chat.twitch.tv" |
| Port                 | The Port that will be used. Do not change.                        | 6667 |
| Channel              | The Channel that will be connected to.                            | "#CubieDev" |
| Nickname             | The Username of the bot account.                                  | "CubieB0T" |
| Authentication       | The OAuth token for the bot account.                              | "oauth:pivogip8ybletucqdz4pkhag6itbax" |
| AllowedRanks  | List of ranks required to be able to perform the commands. | ["broadcaster", "moderator"] |
| AllowedPeople | List of users who, even if they don't have the right ranks, will be allowed to perform the commands. | ["cubiedev"] |
| MonthsPerChance | How many months of total subscriptions on the current channel should count for 1 extra chance in the drawing. If set to 6, someone with 11 months of subscriptions will have `11 / 6 = 1.8333...` additional chances per roll. This would mean they have `1 + 1.8333... = 2.8333...`, while someone who is not subscribed has the standard `1`. | 6 |

*Note that the example OAuth token is not an actual token, but merely a generated string to give an indication what it might look like.*

I got my real OAuth token from https://twitchapps.com/tmi/.

---

# GUI
For reference, this is the GUI:

![image](https://user-images.githubusercontent.com/37621491/60506964-55989a00-9cc7-11e9-8381-dec8f24be42a.png)

Let's clarify the functionality from the GUI:

| **Button** | **Action** |
| ---------- | ----------- |
| Auth | This button will hide or unhide your Authentication token. This way you can hide it when you aren't changing it, so that it will not leak. |
| Run | This button is both "Stop" and "Run" at the same time. When the bot is running, the button will say Stop. While it is not, it will display "Run". Pressing this button will either stop the bot from running, or start the bot using the information filled in above. | 
| Pick Next Level | Equivalent to typing `!nextlevel` in chat. Picks the next level. |
| Clear: <date> | Clears the list of levels. The date shows when the list of levels was last cleared. |


---

# Requirements
* Python 3+ (Only tested on 3.6)

Download Python online.

* TwitchWebsocket

Install this using `pip install git+https://github.com/CubieDev/TwitchWebsocket.git`

This last library is my own [TwitchWebsocket](https://github.com/CubieDev/TwitchWebsocket) wrapper, which makes making a Twitch chat bot a lot easier.
This repository can be seen as an implementation using this wrapper.

---

# Other Twitch Bots

* [TwitchGoogleTranslate](https://github.com/CubieDev/TwitchGoogleTranslate)
* [TwitchMarkovChain](https://github.com/CubieDev/TwitchMarkovChain)
* [TwitchRhymeBot](https://github.com/CubieDev/TwitchRhymeBot)
* [TwitchCubieBotGUI](https://github.com/CubieDev/TwitchCubieBotGUI)
* [TwitchCubieBot](https://github.com/CubieDev/TwitchCubieBot)
* [TwitchDeathCounter](https://github.com/CubieDev/TwitchDeathCounter)
* [TwitchSuggestDinner](https://github.com/CubieDev/TwitchSuggestDinner)
* [TwitchPickUser](https://github.com/CubieDev/TwitchPickUser)
* [TwitchSaveMessages](https://github.com/CubieDev/TwitchSaveMessages)
* [TwitchPackCounter](https://github.com/CubieDev/TwitchPackCounter) (Streamer specific bot)
* [TwitchDialCheck](https://github.com/CubieDev/TwitchDialCheck) (Streamer specific bot)
* [TwitchSendMessage](https://github.com/CubieDev/TwitchSendMessage) (Not designed for non-programmers)
