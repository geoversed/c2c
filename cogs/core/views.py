import discord

from .helpers import economy_check, respond, membed


def format_timeout(embed: discord.Embed, children: list):
    embed.colour = discord.Colour.brand_red()
    embed.description = f"~~{embed.description}~~"
    embed.title = "Timed Out"
    
    for item in children:
        item.disabled = True


class BaseInteractionView(discord.ui.View):
    """
    A view that ensures that only the interaction creator can make use of this view.
    
    This view also deletes itself when timing out.
    
    This view has no items, you'll need to add them in manually.
    """
    def __init__(
        self, 
        interaction: discord.Interaction, 
        controlling_user: discord.User | None = None, 
        timeout: float | None = 60.0
    ) -> None:
        self.interaction = interaction
        self.controlling_user = controlling_user or interaction.user
        super().__init__(timeout=timeout)

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        return await economy_check(interaction, original=self.controlling_user)


class BaseContextView(discord.ui.View):
    """
    A view that ensures that only the command author can make use of this view.
    
    This view should delete itself when timing out. `View.wait()` should be used to do this yourself.
    
    This view has no items, you'll need to add them in manually.
    """
    def __init__(
        self,
        ctx, 
        controlling_user: discord.User | None = None, 
        timeout: float | None = 60.0
    ) -> None:
        self.ctx = ctx
        self.controlling_user = controlling_user or ctx.author
        super().__init__(timeout=timeout)

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        return await economy_check(interaction, original=self.controlling_user)


class ConfirmationButton(discord.ui.Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    async def callback(self, interaction: discord.Interaction) -> None:
        self.view.value = self.style == discord.ButtonStyle.success
        self.view.stop()

        embed = interaction.message.embeds[0]
        embed.title = f"Action {self.custom_id}"
        embed.colour = discord.Colour.brand_green() if self.view.value else discord.Colour.brand_red()

        for item in self.view.children:
            item.disabled = True
            if item.label == self.label:
                item.style = discord.ButtonStyle.success
                continue
            item.style = discord.ButtonStyle.secondary

        await interaction.response.edit_message(embed=embed, view=self.view)


async def process_confirmation(
    interaction: discord.Interaction, 
    prompt: str, 
    view_owner: discord.Member | None = None, 
    **kwargs
) -> bool:
    """
    Process a confirmation. This only updates the view.
    
    The actual action is done in the command itself.

    This returns a boolean indicating whether the user confirmed the action or not, or None if the user timed out.
    """

    confirm_view = (
        BaseInteractionView(interaction=interaction, controlling_user=view_owner, timeout=30.0)
        .add_item(ConfirmationButton(label="Cancel", style=discord.ButtonStyle.danger, custom_id="Cancelled"))
        .add_item(ConfirmationButton(label="Confirm", style=discord.ButtonStyle.success, custom_id="Confirmed"))
    )
    confirm_view.value = None
    confirm_embed = membed(prompt)
    confirm_embed.title = "Pending Confirmation"

    msg = await respond(interaction, embed=confirm_embed, view=confirm_view, **kwargs)
    await confirm_view.wait()
    if confirm_view.value is None:
        confirm_view.value = False
        format_timeout(embed=confirm_embed, children=confirm_view.children)
        try:
            if msg:
                await msg.edit(embed=confirm_embed, view=confirm_view)
            else:
                await confirm_view.interaction.edit_original_response(embed=confirm_embed, view=confirm_view)
        except discord.HTTPException:
            pass
    return confirm_view.value


async def send_boilerplate_confirm(ctx, prompt: str) -> bool:
    confirm_view = (
        BaseContextView(ctx, timeout=30.0)
        .add_item(ConfirmationButton(label="Cancel", style=discord.ButtonStyle.danger, custom_id="Cancelled"))
        .add_item(ConfirmationButton(label="Confirm", style=discord.ButtonStyle.success, custom_id="Confirmed"))
    )
    confirm_view.value = None
    confirm_embed = membed(prompt)
    confirm_embed.title = "Pending Confirmation"

    msg: discord.Message = await ctx.send(embed=confirm_embed, view=confirm_view)
    
    await confirm_view.wait()
    if confirm_view.value is None:
        confirm_view.value = False
        format_timeout(embed=confirm_embed, children=confirm_view.children)
        try:
            await msg.edit(embed=confirm_embed, view=confirm_view)
        except discord.HTTPException:
            pass
    return confirm_view.value


class MessageDevelopers(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=60.0)

        self.add_item(
            discord.ui.Button(
                label="Contact a developer", 
                url="https://www.discordapp.com/users/546086191414509599"
            )
        )


class GenericModal(discord.ui.Modal):
    def __init__(self, title: str, **kwargs) -> None:

        self.interaction = None

        for keyword, arguments in kwargs.items():
            setattr(self.data, keyword, arguments)

        super().__init__(title=title, timeout=180.0)

    data = discord.ui.TextInput(label="\u2800")

    async def on_submit(self, interaction: discord.Interaction) -> None:
        self.interaction = interaction
        self.stop()
