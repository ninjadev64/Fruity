# Fruity

Fruity is a Discord bot that provides commands for fun and utility.

Cat pics, song lyrics, coin flip, Unicode characters, anagrams, and more! 

[![Discord](https://img.shields.io/discord/874266744456376370?color=%235865F2&label=Discord&style=for-the-badge)](https://discord.gg/jyJJWjqbFP)


## Contributing
As you can see, Fruity is open source. I'd love to see your contributions, so, here's how to get started.

1. Read the license in LICENSE.md.
2. Fork this repository and clone your fork.
3. Configure Poetry and install all required packages:
    ```bash
    poetry config virtualenvs.in-project true --local
    poetry install
    ```
4. Create a Discord Developer Application and set it up for a bot.
5. Create a tokens.env file, and edit respectively with your Discord bot token:
    ```
    TOKEN=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    ```
6. 
    1. Create a Firebase project on the [Firebase Console](https://console.firebase.google.com/).
    2. Initialise the Firestore Database with your preferred region. You do not need to enable test mode.
    3. Project Settings > Service Accounts > Firebase Admin SDK > Generate new private key.
        1. Save this file as `firebaseKey.json`.
7. Run the main.py file with Poetry to start the bot (VSCode users: F5)
8. Join the CitrusDev Discord server [here](https://discord.gg/jyJJWjqbFP).

As stated in the license, please read the contributing guidelines in CONTRIBUTING.md before contributing to this project.