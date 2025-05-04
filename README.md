# Fixed That For You!
Because social media links are stupid.

# Development
1. Clone the repo
2. Create a new feature/fix branch
3. Copy `env.template` to `.env` in the root directory and fill it out
    ```ini
    DEV_GUILD=YOUR_PERSONAL_DISCORD_SERVER_ID_HERE # Your test Discord server's ID
    TOKEN=YOUR_DISCORD_DEV_TOKEN_HERE # Your test bot's token
    ENVIRONMENT=development
    ```
4. Build the Docker image
    ```bash
    docker compose build
    ```
5. Run the container
    ```bash
    docker compose up --watch
    ```
6. Go to the [Discord developer portal](https://discord.com/developers/applications) and use the URL Generator with the `bot` scope and the `Send Messages` and `Send Messages in Threads` permissions to generate a URL for you to add the bot to your test server
7. Start developing! As you make changes to the application files, the bot will automatically reload with the new code
7. Once you're ready to submit your changes, open a PR against the main branch