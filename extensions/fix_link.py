"""
Fix message links
"""
import asyncio
from typing import Union
from interactions import (
    BrandColors,
    Button,
    ButtonStyle,
    ContextMenuContext,
    Embed,
    Extension,
    check,
    listen,
    Member,
    Message,
    message_context_menu,
    slash_command,
    User
)
from interactions.api.events import MessageCreate
from src import logutil, linkparser

logger = logutil.init_logger(__name__)

class FixLink(Extension):
  async def is_a_bot(self, author: Union[Member, User]) -> bool:
    return author.bot

  async def not_a_bot(ctx: ContextMenuContext) -> bool:
    result = not ctx.target.author.bot
    return result

  close_button = Button(
                  label="Close",
                  custom_id="close_msg",
                  style=ButtonStyle.GREY
                )

  async def get_new_links(self, embeds: list[Embed]):
    url_list = []

    # Iterate through embeds in the original message and try to fix the links
    for embed in embeds:
      new_url = linkparser.LinkParser(embed.url).fix()
      if new_url is not None:
        url_list.append(new_url)
    return url_list
  
  async def no_link_found(self, ctx:ContextMenuContext):
      await ctx.send(
          content="",
          ephemeral=True,
          embed=Embed(
              description="No valid link was found in the selected message!",
              color=BrandColors.YELLOW
          ),
          components=[
            self.close_button
          ]
      )

  @listen(MessageCreate)
  async def on_message_create(self, event: MessageCreate):
    not_a_bot = not await self.is_a_bot(event.message.author)
    if (not_a_bot):
      await asyncio.sleep(2) # This is required because the original embed isn't always instantly available
      message: Message = event.message
      # If there are embeds in the original message try to fix the links
      if len(message.embeds) > 0:
        new_links = await self.get_new_links(message.embeds)
        new_links_list = "\n".join([i for i in new_links])

        # If any links were fixed, return them in a new message
        if len(new_links_list) > 0:
          await message.reply(
            content=new_links_list,
            silent=True
          )
          return

  @check(check=not_a_bot)
  @message_context_menu(name="View Fixed Links")
  async def fix_links(self, ctx: ContextMenuContext):
      message: Message = ctx.target
      # If there are embeds in the original message try to fix the links
      if len(message.embeds) > 0:
        new_links = await self.get_new_links(message.embeds)
        new_links_list = "\n".join([i for i in new_links])

        # If any links were fixed, return them in a new message
        if len(new_links_list) > 0:
          await ctx.send(
            content=new_links_list,
            silent=True,
          )
          return
      # Else, fallback to "no valid link found" message
      await self.no_link_found(ctx)

  @slash_command(name="help")
  async def help(self, ctx: ContextMenuContext):
      await ctx.send(
          content='Right-click/long-press a message with a social media or news link, \
go to "Apps", then click "View Fixed Links".',
          ephemeral=True,
          components=[
            self.close_button
          ]
      )