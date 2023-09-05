"""
Fix message links
"""
from interactions import (
    BrandColors,
    Button,
    ButtonStyle,
    check,
    ContextMenuContext,
    Embed,
    Extension,
    Message,
    message_context_menu,
    slash_command
)

from src import logutil, linkparser

logger = logutil.init_logger(__name__)

class FixLink(Extension):
  close_button = Button(
                  label="Close",
                  custom_id="close_msg",
                  style=ButtonStyle.GREY
                )

  async def get_new_links(self, ctx:ContextMenuContext):
    url_list = []
    message: Message = ctx.target

    # Iterate through embeds in the original message and try to fix the links
    for embed in message.embeds:
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

  async def not_a_bot(ctx: ContextMenuContext):
    not_a_bot = not ctx.target.author.bot
    return not_a_bot

  @check(check=not_a_bot)
  @message_context_menu(name="View Fixed Links")
  async def fix_links(self, ctx: ContextMenuContext):
      message: Message = ctx.target
      # If there are embeds in the original message try to fix the links
      if len(message.embeds) > 0:
        new_links = await self.get_new_links(ctx)
        new_links_list = "\n".join([i for i in new_links])

        # If any links were fixed, return them in a new message
        if len(new_links_list) > 0:
          await ctx.send(
            content=new_links_list,
            components=[self.close_button],
            silent=True,
            ephemeral=True
          )
          return
      # Else, fallback to "no valid link found" message
      await self.no_link_found(ctx)

  @slash_command(name="help")
  async def help(self, ctx: ContextMenuContext):
      await ctx.send(
          content='Right-click/long-press a message with a social media or news link,\
go to "Apps", then click "View Fixed Links".',
          ephemeral=True,
      )