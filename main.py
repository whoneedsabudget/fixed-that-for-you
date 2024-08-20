"""
Main script to run

This script initializes extensions and starts the bot
"""
import os
import sys

from interactions import (
    Activity,
    ActivityType,
    BrandColors,
    Button,
    ButtonStyle,
    Client,
    component_callback,
    ComponentContext,
    Embed,
    errors,
    Intents,
    listen,
    MISSING
)
from interactions.api.events import CommandError
from config import config
from src import logutil

logger = logutil.init_logger(__name__)
logger.debug(
    "Debug mode is %s; This is not a warning, \
just an indicator. You may safely ignore",
    config.DEBUG,
)

if not os.environ.get("TOKEN"):
    logger.critical("TOKEN variable not set. Cannot continue")
    sys.exit(1)

client = Client(
    token=os.environ.get("TOKEN"),
    activity=Activity(
        name="with social media links", type=ActivityType.PLAYING
    ),
    intents=Intents.DEFAULT | Intents.GUILDS | Intents.GUILD_MESSAGES | Intents.MESSAGE_CONTENT,
    sync_interactions=True,
    debug_scope=MISSING,
    send_command_tracebacks=False,
    logger=logger
)

# Enable hot-reload and traceback printing if debug is enabled
if config.DEBUG:
    client.send_command_tracebacks=True
    client.load_extension("interactions.ext.jurigged")

@listen()
async def on_startup():
    """Called when the bot starts"""
    logger.info(f"Logged in as {client.user}")

@component_callback("close_msg")
async def close_msg(ctx: ComponentContext):
    """Close the message"""
    message = await ctx.edit_origin()
    await ctx.delete(message)

@listen(CommandError, disable_default_listeners=False)
async def on_command_error(event: CommandError):
    if isinstance(event.error, errors.CommandCheckFailure):
      if event.error.check.__name__ == 'not_a_bot':
        await event.ctx.send(
            embeds=Embed(
                description="This command can't be run against bot messages!",
                color=BrandColors.YELLOW,
            ),
            components=Button(
              label="Close",
              custom_id="close_msg",
              style=ButtonStyle.GREY
            ),
            ephemeral=True
        )
    if not event.ctx.responded:
        await event.ctx.send(
            embeds=Embed(
                description="Something went wrong! Please try again later.",
                color=BrandColors.RED,
            ),
            components=Button(
              label="Close",
              custom_id="close_msg",
              style=ButtonStyle.GREY
            ),
            ephemeral=True
        )

# get all python files in "extensions" folder
extensions = [
    f"extensions.{f[:-3]}"
    for f in os.listdir("extensions")
    if f.endswith(".py") and not f.startswith("_")
]
for extension in extensions:
    try:
        client.load_extension(extension)
        logger.info(f"Loaded extension {extension}")
    except errors.ExtensionLoadException as e:
        logger.exception(f"Failed to load extension {extension}.", exc_info=e)

client.start()