import contextlib
from typing import Any, Literal, Optional

import discord
from asqlite import Connection


async def declare_transaction(conn: Connection, user_id: int, /) -> bool:
    await conn.execute(
        """
        INSERT INTO transactions VALUES ($0)
        ON CONFLICT DO NOTHING
        """, user_id
    )


async def end_transaction(conn: Connection, user_id: int, /) -> bool:
    await conn.execute("DELETE FROM transactions WHERE userID = $0", user_id)


async def commands_used_by(user_id: int, conn: Connection) -> int:
    total, = await conn.fetchone(
        """
        SELECT CAST(TOTAL(cmd_count) AS INTEGER)
        FROM command_uses
        WHERE userID = $0
        """, user_id
    )

    return total


async def add_multiplier(
    conn: Connection,
    *,
    user_id: int,
    multi_amount: int,
    multi_type: Literal["xp", "luck", "robux"],
    cause: str,
    description: str,
    expiry: Optional[float] = None,
    on_conflict: str = "UPDATE SET amount = amount + $1, description = $4"
) -> None:
    """
    Add a multiplier to the database.

    Parameters
    ------------
    conn
        The connection to the database.
    user_id
        The user's ID to add the multiplier to.
    multi_amount
        The amount of the multiplier.
    multi_type
        The type of the multiplier.
        Can be either 'xp', 'luck', or 'robux'.
    cause
        Why the multiplier was added.
        Must be consistent in order to find it later.
    description
        A description of the multiplier.
        This will show up on the user multiplier list.
    expiry
        The expiry timestamp of the multiplier.
        Can be None if the multiplier is permanent.
    on_conflict
        The action to take when a conflict occurs.
        Defaults to updating the amount and description.

    Returns
    ------------
    A boolean to indicate if the multiplier was updated/inserted.

    ## Values of `on_conflict` explained
    ### `on_conflict` set to "DO NOTHING"
    - Return `False` if the `on_conflict` clause was triggered.
    - Row insertion occurs otherwise, returning `True`.
    - Useful for apply temporary multipliers.

    ### `on_conflict` set to "DO UPDATE" (default)
    - Always return `True` because in either case an operation took place.
    - Useful for applying permanent multipliers updated incrementally.
    """

    result = await conn.fetchone(
        f"""
        INSERT INTO multipliers VALUES ($0, $1, $2, $3, $4, $5)
        ON CONFLICT(userID, cause) DO {on_conflict}
        RETURNING rowid
        """, user_id, multi_amount, multi_type, cause, description, expiry
    )
    return result is not None


async def remove_multiplier_from_cause(
    conn: Connection,
    *,
    user_id: int,
    cause: str
) -> None:
    """Remove a multiplier from a user based on the cause."""

    query = "DELETE FROM multipliers WHERE userID = $0 AND cause = $1"
    await conn.execute(query, user_id, cause)


async def get_multi_of(
    user_id: int,
    multi_type: Literal["xp", "luck", "robux"],
    conn: Connection
) -> int:
    """Get the amount of a multiplier of a specific type for a user."""

    multiplier, = await conn.fetchone(
        """
        SELECT CAST(TOTAL(amount) AS INTEGER)
        FROM multipliers
        WHERE (userID IS NULL OR userID = $0)
        AND multi_type = $1
        """, user_id, multi_type
    )
    return multiplier


def membed(description: Optional[str] = None) -> discord.Embed:
    """Quickly construct an embed with an optional description."""
    return discord.Embed(colour=0x2B2D31, description=description)


async def economy_check(
    itx: discord.Interaction,
    original_id: int,
    /
) -> bool:
    """Shared interaction check common amongst most interactions."""
    if original_id == itx.user.id:
        return True
    await itx.response.send_message(
        "This menu is not for you",
        ephemeral=True,
        delete_after=5.0,
    )
    return False


class BaseInteractionView(discord.ui.View):
    """
    A view ensuring only the interaction creator can interact.

    It also destroys the view if an exception is raised.

    This view has no items, you'll need to add them in manually.
    """
    def __init__(
        self,
        itx: discord.Interaction,
        controlling_user: Optional[discord.User] = None
    ) -> None:
        self.itx = itx
        self.controlling_user = controlling_user or itx.user
        super().__init__(timeout=45.0)

    async def interaction_check(self, itx: discord.Interaction) -> bool:
        return await economy_check(itx, self.controlling_user.id)

    async def on_error(
        self,
        itx: discord.Interaction,
        error: Exception,
        item: discord.ui.Item[Any],
        /
    ) -> None:
        with contextlib.suppress(discord.NotFound):
            await self.itx.edit_original_response(view=None)

        if not self.is_finished():
            self.stop()

        await super().on_error(itx, error, item)


class ConfirmButton(discord.ui.Button):
    def __init__(self) -> None:
        super().__init__(style=discord.ButtonStyle.success, label="Confirm")

    async def callback(self, itx: discord.Interaction) -> None:
        self.view.value = True
        self.view.stop()

        embed = itx.message.embeds[0]
        embed.title = "Action Confirmed"
        embed.colour = discord.Colour.brand_green()

        cancel_btn, confirm_btn = self.view.children[0], self
        confirm_btn.disabled, cancel_btn.disabled = True, True
        confirm_btn.style, cancel_btn.style = (
            discord.ButtonStyle.success,
            discord.ButtonStyle.secondary
        )

        await itx.response.edit_message(embed=embed, view=self.view)


class CancelButton(discord.ui.Button):
    def __init__(self) -> None:
        super().__init__(label="Cancel", style=discord.ButtonStyle.danger)

    async def callback(self, itx: discord.Interaction) -> None:
        self.view.value = False
        self.view.stop()

        embed = itx.message.embeds[0]
        embed.title = "Action Cancelled"
        embed.colour = discord.Colour.brand_red()

        confirm_btn = self.view.children[-1]

        self.disabled, confirm_btn.disabled = True, True
        self.style, confirm_btn.style = (
            discord.ButtonStyle.success,
            discord.ButtonStyle.secondary
        )

        await itx.response.edit_message(embed=embed, view=self.view)


async def format_timeout_view(
    embed: discord.Embed,
    view: BaseInteractionView
) -> bool:

    embed.colour = discord.Colour.brand_red()
    embed.description = f"~~{embed.description}~~"
    embed.title = "Timed Out"
    view.value = False

    for item in view.children:
        item.disabled = True

    with contextlib.suppress(discord.NotFound):
        await view.itx.edit_original_response(embed=embed, view=view)
    return False


def to_ord(n: int) -> str:
    """Convert 01 to 1st, 02 to 2nd etc."""
    if 10 <= n % 100 <= 20:
        return f"{n}th"

    suffix = {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return f"{n}{suffix}"


async def respond(
    itx: discord.Interaction,
    content: Optional[str] = None,
    /,
    **kwargs
) -> Optional[discord.WebhookMessage]:
    """
    Responds to the interaction by sending a message.

    Considers whether or not this interaction was already responded to before.
    """
    if itx.response.is_done():
        return await itx.followup.send(content, **kwargs)
    await itx.response.send_message(content, **kwargs)


async def edit_response(
    itx: discord.Interaction,
    /,
    **kwargs
) -> Optional[discord.InteractionMessage]:
    """
    Edit an interaction's original response message, which may be a response.

    Considers whether or not this interaction was already responded to before.
    """
    if itx.response.is_done():
        return await itx.edit_original_response(**kwargs)
    await itx.response.edit_message(**kwargs)


async def process_confirmation(
    itx: discord.Interaction,
    /,
    prompt: str,
    view_owner: Optional[discord.User] = None,
    **kwargs
) -> bool:
    """
    Process a confirmation. This only updates the view.

    The actual action is done in the command itself.

    This returns a boolean indicating whether the user confirmed the action.
    Can be None if the user timed out.
    """

    view = BaseInteractionView(itx, view_owner)
    view.add_item(CancelButton()).add_item(ConfirmButton())

    view.value = None
    emb = membed(prompt)
    emb.title = "Pending Confirmation"

    await respond(itx, embed=emb, view=view, **kwargs)

    await view.wait()
    if view.value is None:
        await format_timeout_view(emb, view)
    return view.value


async def is_setting_enabled(
    conn: Connection,
    user_id: int,
    setting: str
) -> int:
    """Check if a user has a setting enabled."""

    query = "SELECT value FROM settings WHERE userID = $0 AND setting = $1"
    result, = await conn.fetchone(query, user_id, setting) or (0,)
    return result


async def handle_confirm_outcome(
    itx: discord.Interaction,
    prompt: str,
    view_owner: Optional[discord.User] = None,
    setting: Optional[str] = None,
    conn: Optional[Connection] = None,
    **kwargs
) -> Optional[bool]:
    """
    Handle a confirmation outcome correctly,
    considering whether or not a specific confirmation is enabled.

    Setting names should be lowercase.

    ## Returns
    ### `None`
    - When the user doesn't have the specified confirmation enabled.

    ### `True`
    - When the user has confirmed, by confirming on a specific confirmation
    - When enabled setting, or through a generic confirmation confirmed on.

    ### `False`
    - When user has not confirmed explicity or via timeout
    - Applicable for both specific and generic confirmations

    ## Notes

    Transactions will now be created if a passed in
    confirmation is enabled or no confirmation is passed in.

    Only for use in the economy system on a user who is registered.

    Foreign key constraints require you to
    pass in a valid row of the accounts table.

    All connections acquired by or in the function
    will also be released in this function. Do not handle it yourself.
    """

    can_proceed = None
    view_owner = view_owner or itx.user

    # always hold a connection
    conn = conn or await itx.client.pool.acquire()
    try:
        disabled_confirms = (
            setting and not(
                await is_setting_enabled(conn, view_owner.id, setting)
            )
        )
        if disabled_confirms:
            return

        await declare_transaction(conn, view_owner.id)
        await conn.commit()
        await itx.client.pool.release(conn)
        conn = None

        can_proceed = await process_confirmation(
            itx, prompt, view_owner, **kwargs
        )
    finally:
        if conn:
            await itx.client.pool.release(conn)
    return can_proceed