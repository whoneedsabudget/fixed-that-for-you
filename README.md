# Fixed That For You!
Because social media links are stupid.

# Development
1. Clone the repo
2. Create a new feature/fix branch
3. Run `script/bootstrap`
4. Fill out the `.env` file:
    ```ini
    DEV_GUILD = 1000000000000000000 # Your test Discord server's ID
    TOKEN = "BOT_TOKEN_STRING" # Your test bot's token
    ```
5. Run `script/server` to start the bot
6. Go to the [Discord developer portal](https://discord.com/developers/applications) and use the URL Generator with the `bot` scope and the `Send Messages` and `Send Messages in Threads` permissions to generate a URL for you to add the bot to your test server
7. Once you're ready to submit your changes, open a PR against the main branch