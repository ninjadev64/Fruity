# Fruity
Contributing guide


## Getting Started
The Getting Started guide is in the main README.md.


## Style guide
- Please follow the indentation style used in the rest of the project (well, you have to, otherwise Python will scream at you).
- Please make sure to use perfect spelling and grammar everywhere (not just in messages that the end user will see!).
- If you've added a piece of code that is large or hard to understand, please leave a comment or two explaining what it does.
- I may ask you to change some formatting after reviewing your pull request.


## Creating pull requests
- Thouroughly explain the changes contained in your pull request
- State any changes other developers need to make to their setup after pulling your changes
- Make sure you have followed these contributing guidelines and the license diligently


## Notes
### HTTP GET requests
Please use the `aiohttp` module for making HTTP requests, instead of the builtin Python `requests` module.
### Adding commands
Please add the command to it's relevant cog, rather than dumping it somewhere else (e.g. in the main script).
### Changes to the website
Please make sure the website renders properly on different screen sizes (just test a desktop, tablet, and smartphone).
### Custom emojis
It would be appreciated if you can upload any custom emoji files to the `emojis` directory, so I can upload them to the CitrusDev server once your PR is merged.
### Top.gg
Please do not touch *any* Top.gg-related code. Don't worry about warnings along the lines of `topgg.errors.UnauthorizedDetected: Top.gg API token not provided`.
### Login status
A list of guilds the bot is in will print to the console once the bot logs in.
### Firestore usage
Make sure to minimise reads and writes to the Firestore database. If data doesn't need to be permanent, consider a user-keyed dictionary.