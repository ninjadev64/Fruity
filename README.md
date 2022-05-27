# Fruity
Before continuing, please read the license in LICENSE.md.


Fruity is a Discord bot, which sets out to spark interest and create a fun minigame experience in your server. Please see the website at [https://fruity.amansprojects.com/](https://fruity.amansprojects.com/) for more details.

## Setup for development
As you can see, Fruity is open source. We'd love to see your contributions, so, here's how to get started.

1. Read the license in LICENSE.md
2. Fork and clone this repository locally
3. Create a Discord Developer Application and set it up for a bot
4. Create a tokens.env file, following the below template, and edit respectively:
    ```
    TOKEN=discordBotToken1234
    GUILDS=874266744456376370, 856954305214545960
    ```
    Note: the GUILDS value is a list of guild IDs in which to activate slash commands.
5. Run the main.py file with Python 3 to start the bot
6. Familiarise yourself with discord.py and [dislash.py](https://github.com/EQUENOS/dislash.py)
7. Join the CitrusDev Discord [here](https://dsc.gg/CitrusDev)
8. be happy :)

As stated in the license, you must thoroughly read the contributing guidelines laid out in CONTRIBUTING.md before contributing to this project.

I recommend using Visual Studio Code as your IDE for this project as it's what I use and there are launch profiles, extension recommendations, and more set up for using it.

Note: in order to work on Fruity you need to have the below libraries / modules installed:
* python-dotenv
* discord.py
* dislash.py
* [art](https://pypi.org/project/art/)
* [geopy](https://pypi.org/project/geopy/) - for `/weather city`