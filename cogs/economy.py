from other.utilities import *
from asyncio import sleep, TimeoutError as asyncTE
from string import ascii_letters, digits
from shelve import open as open_shelve
import datetime
import discord
from other.pagination import Pagination
from discord.ext import commands
from math import floor
from random import randint, choices, choice, sample, shuffle
from pluralizer import Pluralizer
from discord import app_commands
import json
from asqlite import Connection as asqlite_Connection
from typing import Optional, Literal, Any, Union
from tatsu.wrapper import ApiWrapper


def membed(custom_description: str) -> discord.Embed:
    """Quickly create an embed with a custom description using the preset."""
    membedder = discord.Embed(colour=0x2F3136,
                              description=custom_description)
    return membedder


def number_to_ordinal(n):
    """Convert 01 to 1st, 02 to 2nd etc."""
    if 10 <= n % 100 <= 20:
        suffix = 'th'
    else:
        suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')

    return str(n) + suffix


"""ALL VARIABLES AND CONSTANTS FOR THE ECONOMY ENVIRONMENT"""

BANK_TABLE_NAME = 'bank'
SLAY_TABLE_NAME = "slay"
COOLDOWN_TABLE_NAME = "cooldowns"
BANK_COLUMNS = ["wallet", "bank", "slotw", "slotl", "betw", "betl", "bjw", "bjl", "pmulti", "job", "bounty" "prestige"]
invoker_ch = int()
participants = set()
DOWN = True

SERVER_MULTIPLIERS = {
    829053898333225010: 120,
    780397076273954886: 160,
    1144923657064419398: 6969}
INV_TABLE_NAME = "inventory"
FEEDBACK_GLOBAL = 'Have complaints or suggestions? **Let us know:** </feedback:1172898645058785334>.'
ARROW = "<:arrowe:1180428600625877054>"
CURRENCY = '<:robux:1146394968882151434>'
PREMIUM_CURRENCY = '<:robuxpremium:1174417815327998012>'
ERR_UNREASON = membed('You are unqualified to use this command. Possible reasons include '
                      'insufficient balance and/or unreasonable input.')
DOWNM = membed('This command is currently outdated and will be made available at a later date.')
NOT_REGISTERED = membed('Could not find account associated with the user provided.')
extraneous_data = []

BONUS_MULTIPLIERS = {
    "🍕🍕": 55,
    "🤡🤡": 56.5,
    "💔💔": 66.6,
    "🍑🍑": 66.69,
    "🖕🖕": 196.6699,
    "🍆🍆": 129.979,
    "😳😳": 329.999,
    "🌟🌟": 300.53,
    "🔥🔥": 350.5,
    "💔💔💔": 451.11,
    "🖕🖕🖕": 533.761,
    "🤡🤡🤡": 622.227,
    "🍕🍕🍕": 654.555,
    "🍆🍆🍆": 655.521,
    "🍑🍑🍑": 766.667,
    "😳😳😳": 669,
    "🌟🌟🌟": 600,
    "🔥🔥🔥": 850

}

PRESTIGE_EMOTES = {
    1: "<:irn:1164932765674897499>",
    2: "<:iirn:1164932794506559568>",
    3: "<:iiirn:1164932820452524033>",
    4: "<:ivrn:1164932851490365561>",
    5: "<:vrn:1164932886370209833>",
    6: "<:virn:1164932961200783430>",
    7: "<:viirn:1164933271268900874>",
    8: "<:viiirn:1164933309902639194>",
    9: "<:ixrn:1164933376000663562>",
    10: "<:xrn:1164933414156247191>",
    11: "<:Xrne:1164937391514062848>"
}

SHOP_ITEMS = [
    {"name": "Keycard", "cost": 8269069420, "id": 1, "info": "Allows you to bypass certain restrictions.",
     "emoji": "<:lanyard:1165935243140796487>", "rarity": "**Common** <:common:1166316338571132928>"},

    {"name": "Trophy", "cost": 5085779847, "id": 2, "info": "Flex on your friends with this trophy!",
     "emoji": "<:tr1:1165936712468418591>", "rarity": "**Luxurious** <:luxurious:1166316420125163560>"},

    {"name": "Dynamic_Item", "cost": 55556587196, "id": 3,
     "info": "An item that changes use often. Its transformative functions change to match the seasonality of the year.",
     "emoji": "<:dynamic:1166082288069648394>", "rarity": "**Rare** <:rare:1166316365892825138>", "qn": "dynamic_item"},

    {"name": "Resistor", "cost": 18102892402, "id": 4,
     "info": "Creates an embedded system... No one knows how it works because no one has ever purchased this item.",
     "emoji": "<:resistor:1165934607447887973>", "rarity": "**Luxurious** <:luxurious:1166316420125163560>"},

    {"name": "Clan_License", "cost": 20876994182, "id": 5,
     "info": "Create your own clan! It costs a fortune, but with it brings a lot of privileges exclusive to clan members.",
     "emoji": "<:clan_license:1165936231922806804>", "rarity": "**Rare** <:rare:1166316365892825138>", "qn": "clan_license"},

    {"name": "Hyperion", "cost": 49510771984, "id": 6,
     "info": "The `passive` drone that actively helps in increasing the returns in almost everything.",
     "emoji": "<:DroneHyperion:1171491601726574613>", "rarity": "**Rare** <:rare:1166316365892825138>", "qn": "hyperion_drone"},

    {"name": "Crisis", "cost": 765191412472, "id": 7,
     "info": "The `support` drone that can bring status effects into the game, wreaking havoc onto other users!",
     "emoji": "<:DroneCrisis:1171491564258852894>", "rarity": "**Rare** <:rare:1166316365892825138>", "qn": "crisis_drone"},

    {"name": "Odd_Eye", "cost": 33206481258, "id": 8,
     "info": "An eye that may prove advantageous during certain events.",
     "emoji": "<a:eyeOdd:1166465357142298676>", "rarity": "**Luxurious** <:luxurious:1166316420125163560>",
     "qn": "odd_eye"},

    {"name": "Amulet", "cost": 159961918315, "id": 9,
     "info": "Found from a black market, those who wear it are practically invincible in all situations.",
     "emoji": "<a:amuletrc:1175393496799137842>", "rarity": "**Luxurious** <:luxurious:1166316420125163560>"},
]


with open('C:\\Users\\georg\\PycharmProjects\\c2c\\cogs\\times.json') as file_name_thi:
    times = json.load(file_name_thi)

with open('C:\\Users\\georg\\PycharmProjects\\c2c\\cogs\\claimed.json') as file_name_four:
    claims = json.load(file_name_four)


def save_times():  # Note that this used to be called save_amount_job_times, just in case anything breaks
    with open('C:\\Users\\georg\\PycharmProjects\\c2c\\cogs\\times.json', 'w') as file_name_seven:
        json.dump(times, file_name_seven, indent=4)

def acknowledge_claim():
    with open('C:\\Users\\georg\\PycharmProjects\\c2c\\cogs\\claimed.json', 'w') as file_name_nine:
        json.dump(claims, file_name_nine, indent=4)


def make_plural(word, count):
    mp = Pluralizer()
    return mp.pluralize(word=word, count=count)

def plural_for_own(count: int) -> str:
    """Only use this pluralizer if the term is 'own'. Nothing else."""
    # Check if count is not equal to 1
    if count != 1:
        # Add 's' to the word to make it plural
        return "own"
    else:
        # Return the singular form of the word
        return "owns"

def return_rand_str():
    all_char = ascii_letters + digits
    password = "".join(choice(all_char) for _ in range(randint(10, 11)))
    return password


def format_number_short(number):
    if abs(number) < 1e3:
        return str(number)
    elif abs(number) < 1e6:
        return '{:.1f}K'.format(number / 1e3)
    elif abs(number) < 1e9:
        return '{:.1f}M'.format(number / 1e6)
    elif abs(number) < 1e12:
        return '{:.1f}B'.format(number / 1e9)
    else:
        return '{:.1f}T'.format(number / 1e12)


def owners_nolimit(interaction: discord.Interaction) -> Optional[app_commands.Cooldown]:
    """Any of the owners of the client bypass all cooldown restrictions (i.e. Splint + inter_geo)."""
    if interaction.user.id in {546086191414509599, 992152414566232139}:
        return None
    return app_commands.Cooldown(1, randint(6, 8))


def determine_exponent(rinput: str) -> str | int:
    """Finds out what the exponential value entered is equivalent to in numerical form.

    Can handle normal integers and "max"/"all" is always returned 'as-is', not converted to numerical form."""

    def is_exponential(val: str) -> bool:
        """Is the input an exponential input?"""
        return 'e' in val

    rinput = rinput.lower()

    if rinput in {"max", "all"}:
        return rinput

    if is_exponential(rinput):
        before_e_str, after_e_str = map(str, rinput.split('e'))
        before_e = float(before_e_str)
        ten_exponent = int(after_e_str)
        actual_value = before_e * (10 ** ten_exponent)
    else:
        # Handle cases where 'e' is not present
        try:
            actual_value = int(rinput)
        except ValueError:
            # Handle invalid input
            return rinput

    return floor(abs(actual_value))


def generate_slot_combination():
    """A slot machine that generates and returns one row of slots."""
    slot = ['🔥', '😳', '🌟', '💔', '🖕', '🤡', '🍕', '🍆', '🍑']

    weights = [
        (800, 1000, 800, 100, 900, 800, 1000, 800, 800),
        (800, 1000, 800, 100, 900, 800, 1000, 800, 800),
        (800, 1000, 800, 100, 900, 800, 1000, 800, 800)]

    slot_combination = ''.join(choices(slot, weights=w, k=1)[0] for w in weights)
    return slot_combination


def fmt_timestamp(year_inp: int, month_inp: int, day_inp: int, hour_inp: int, min_inp: Optional[int]
                  , fmt_style: Literal['f', 'F', 'd', 'D', 't', 'T', 'R']):
    """A helper function to format a :class:`datetime.datetime` for presentation within Discord.

        This allows for a locale-independent way of presenting data using Discord specific Markdown.

        +-------------+----------------------------+-----------------+
        |    Style    |       Example Output       |   Description   |
        +=============+============================+=================+
        | t           | 22:57                      | Short Time      |
        +-------------+----------------------------+-----------------+
        | T           | 22:57:58                   | Long Time       |
        +-------------+----------------------------+-----------------+
        | d           | 17/05/2016                 | Short Date      |
        +-------------+----------------------------+-----------------+
        | D           | 17 May 2016                | Long Date       |
        +-------------+----------------------------+-----------------+
        | f (default) | 17 May 2016 22:57          | Short Date Time |
        +-------------+----------------------------+-----------------+
        | F           | Tuesday, 17 May 2016 22:57 | Long Date Time  |
        +-------------+----------------------------+-----------------+
        | R           | 5 years ago                | Relative Time   |
        +-------------+----------------------------+-----------------+

        Note that the exact output depends on the user's locale setting in the client. The example output
        presented is using the ``en-GB`` locale.

        -----------

        Returns
        --------
        :class:`str`
            The formatted string.
        """

    if min_inp is None:
        min_inp = 0
    period = datetime.datetime(year=year_inp, month=month_inp, day=day_inp, hour=hour_inp, minute=min_inp)

    period_fmt = discord.utils.format_dt(period, fmt_style)
    return period_fmt


def get_profile_key_value(key: str) -> Any:
    """Fetch a profile key (attribute) from the database. Returns None if no key is found."""
    with open_shelve("C:\\Users\\georg\\PycharmProjects\\c2c\\db-shit\\profile_mods") as dbmr:
        return dbmr.setdefault(key, None)


def display_user_friendly_deck_format(deck: list, /):
    """Convert a deck view into a more user-friendly view of the deck."""
    remade = list()
    suits = ["♥", "♦", "♣", "♠"]  # hearts diamonds, clubs, spades
    ranks = {10: ["K", "Q", "J"], 1: "A"}
    chosen_suit = choice(suits)
    for number in deck:
        conversion_letter = ranks.setdefault(number, None)
        if conversion_letter:
            unfmt = choice(conversion_letter)
            fmt = f"[`{chosen_suit} {unfmt}`](https://www.youtube.com)"
            remade.append(fmt)
            continue
        unfmt = number
        fmt = f"[`{chosen_suit} {unfmt}`](https://www.youtube.com)"
        remade.append(fmt)
        continue
    remade = ' '.join(remade)
    return remade


def display_user_friendly_card_format(number: int, /):
    """Convert a single card into the user-friendly card version linked and ranked."""
    suits = ["♥", "♦", "♣", "♠"]  # hearts diamonds, clubs, spades
    ranks = {10: ["K", "Q", "J"]}
    chosen_suit = choice(suits)
    conversion_letter = ranks.setdefault(number, None)
    if conversion_letter:
        unfmt = choice(conversion_letter)
        fmt = f"[`{chosen_suit} {unfmt}`](https://www.youtube.com)"
        return fmt
    unfmt = number
    fmt = f"[`{chosen_suit} {unfmt}`](https://www.youtube.com)"
    return fmt


def modify_profile(typemod: Literal["update", "create", "delete"], key: str, new_value: Any):
    """Modify custom profile attributes (or keys) of any given discord user. If "delete" is used on a key that does not exist, returns ``0``
    :param typemod: type of modification to the profile. could be ``update`` to update an already existing key, or ``create`` to create a new key or ``delete`` to delete a key
    :param key: The key to modify/delete.
    :param new_value: The new value to replace the old value with. For a typemod of ``delete``, this argument will not matter at all, since only the key name is required to delete a key."""
    with open_shelve("C:\\Users\\georg\\PycharmProjects\\c2c\\db-shit\\profile_mods") as dbm:
        match typemod:
            case "update" | "create":
                dbm.update({f'{key}': new_value})
                return dict(dbm)
            case "delete":
                try:
                    del dbm[f"{key}"]
                except KeyError:
                    return 0
            case _:
                return "invalid type of modification value entered"


def get_stock(item: str) -> int:
    """Find out how much of an item is available."""
    with open_shelve("C:\\Users\\georg\\PycharmProjects\\c2c\\db-shit\\stock") as dbm:
        a = dbm.get(f"{item}")
        if a is None:
            a = 0
        return int(a)


def modify_stock(item: str, modify_type: Literal["+", "-"], amount: int) -> int:
    """Directly modify the amount of stocks available for an item, returns the new amount that is available."""
    with open_shelve("C:\\Users\\georg\\PycharmProjects\\c2c\\db-shit\\stock") as dbm:
        match modify_type:
            case "+":
                a = dbm.get(f"{item}")
                if a is None:
                    a = 0
                new_count = int(a) + amount
                dbm.update({f'{item}': new_count})
                dbm.close()
                return new_count
            case "-":
                a = dbm.get(f"{item}")
                if a is None:
                    a = 0
                new_count = int(a) - amount
                dbm.update({f'{item}': new_count})
                return new_count


class ConfirmDeny(discord.ui.View):
    def __init__(self, interaction: discord.Interaction):
        super().__init__(timeout=20.0)
        self.interaction = interaction
        self.timed_out: bool = True

    async def on_timeout(self) -> None:
        if self.timed_out:
            for item in self.children:
                item.disabled = True
            await self.msg.edit(content="Timed out waiting for a response.", view=None) # type: ignore
        else:
            for item in self.children:
                item.disabled = True

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        """Make sure the original user that called the interaction is only in control, no one else."""
        if interaction.user == self.interaction.user:
            return True
        else:
            emb = membed(
                f"A good attempt, but only {self.interaction.user.mention} can perform this action.")
            await interaction.response.send_message(embed=emb, ephemeral=True) # type: ignore
            return False

    @discord.ui.button(label='Confirm', style=discord.ButtonStyle.green)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        button.disabled = True
        # await interaction.response.send_message("Request accepted.", ephemeral=True)
        self.timed_out = False
        for item in self.children:
            item.disabled = True
        await interaction.message.edit(content="Request accepted.", view=None)

    @discord.ui.button(label='Deny', style=discord.ButtonStyle.red)
    async def deny(self, interaction: discord.Interaction, button: discord.ui.Button):
        button.disabled = True
        # await interaction.response.send_message("Request denied.", ephemeral=True)
        self.timed_out = False
        for item in self.children:
            item.disabled = True
        await interaction.message.edit(content="Request denied.", view=None)


# class GroupModal(discord.ui.Modal, title='Create your clan'):
#     # Our modal classes MUST subclass `discord.ui.Modal`,
#     # but the title can be whatever you want.
#
#     # This will be a short input, where the user can enter their name
#     # It will also have a placeholder, as denoted by the `placeholder` kwarg.
#     # By default, it is required and is a short-style input which is exactly
#     # what we want.
#     name = discord.ui.TextInput(
#         label='Clan Name',
#         placeholder='The name of your clan e.g, One Love 2 Killers',
#         min_length=3, max_length=20
#     )
#
#     tag = discord.ui.TextInput(
#         label='Clan Tag',
#         placeholder='A brief sequence of letters to represent your clan e.g., 1K2L',
#         min_length=2, max_length=8
#     )
#
#     # This is a longer, paragraph style input, where user can submit feedback
#     # Unlike the name, it is not required. If filled out, however, it will
#     # only accept a maximum of 300 characters, as denoted by the
#     # `max_length=300` kwarg.
#     desc = discord.ui.TextInput(
#         label='Clan Description',
#         style=discord.TextStyle.long,
#         placeholder='Tell us about your clan..',
#         max_length=300,
#         min_length=10
#     )
#
#
#     async def on_submit(self, interaction: discord.Interaction):
#
#         await interaction.response.send_message(f'Thanks for your feedback, {self.name.value}!', ephemeral=True)
#
#     async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
#         await interaction.response.send_message('Oops! Something went wrong.', ephemeral=True)
#
#         # Make sure we know what the error actually is
#         traceback.print_exception(type(error), error, error.__traceback__)


class HighLow(discord.ui.View):
    """View for the High-low command and its associated functions."""
    foo: bool = None

    def __init__(self, interaction: discord.Interaction, client: commands.Bot):
        self.interaction = interaction
        self.client = client
        super().__init__(timeout=30)

    async def disable_all_items(self):
        for item in self.children:
            item.disabled = True

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user == self.interaction.user:
            return True
        else:
            emb = discord.Embed(
                description=f"# You cannot perform this action.\n"
                            f"A good attempt, but you did not make this interaction. **Start by making one yourself.**",
                color=0x2F3136
            )
            await interaction.response.send_message(embed=emb, ephemeral=True) # type: ignore
            return False

    @discord.ui.button(label='Low', style=discord.ButtonStyle.grey)
    async def low(self, interaction: discord.Interaction, button: discord.ui.Button):
        button.disabled = True
        await interaction.response.defer(thinking=True, ephemeral=True) # type: ignore

        async with self.client.pool_connection.acquire() as conn: # type: ignore
            conn: asqlite_Connection
            avatar = interaction.user.display_avatar or interaction.user.default_avatar

            if 33 >= extraneous_data[0] > 0:

                pmulti = await Economy.get_pmulti_data_only(interaction.user, conn)
                new_multi = SERVER_MULTIPLIERS.setdefault(interaction.guild.id, 0) + pmulti[0]
                bonus = floor((new_multi/100)*extraneous_data[1])
                total = bonus + extraneous_data[1]
                new_balance = await Economy.update_bank_new(interaction.user, conn, total)

                self.foo = False
                await self.disable_all_items()

                win = discord.Embed(title=f'{interaction.user.display_name}\'s winning high-low game',
                                    description=f'- You just won **\U000023e3 {total:,}**.\n'
                                                f' - {PREMIUM_CURRENCY} **{bonus:,}** won from a **{new_multi}**% multi.\n'
                                                f'- Your new `wallet` balance is **\U000023e3 {new_balance[0]:,}**.\n',
                                    colour=discord.Color.brand_green())
                win.set_thumbnail(url=avatar.url)

                await interaction.followup.send(embed=win)
                await interaction.message.edit(
                    content=f'{interaction.user.display_name}, you won. the number i was guessing '
                            f'of was **{extraneous_data[0]}**', view=None)
                extraneous_data.clear()
            else:
                new_balance = await Economy.update_bank_new(interaction.user, conn, -int(extraneous_data[1]))
                self.foo = False
                await self.disable_all_items()

                lose = discord.Embed(title=f'{interaction.user.display_name}\'s losing high-low game',
                                     description=f'- You lost **\U000023e3 {int(extraneous_data[1]):,}**.\n'
                                                 f'- No multiplier accrued due to a lost bet.\n'
                                                 f'- Your new `wallet` balance is **\U000023e3 {new_balance[0]:,}**.\n',
                                     colour=discord.Color.brand_red())
                lose.set_thumbnail(url=avatar.url)

                await interaction.followup.send(embed=lose)
                await interaction.message.edit(
                    content=f'{interaction.user.display_name}, you lost unfortunatley. the number i was guessing '
                            f'of was **{extraneous_data[0]}**', view=None)
                extraneous_data.clear()

    @discord.ui.button(label='JACKPOT!', style=discord.ButtonStyle.green)
    async def jackpot(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(thinking=True, ephemeral=True) # type: ignore
        button.disabled = True

        async with self.client.pool_connection.acquire() as conn: # type: ignore
            conn: asqlite_Connection
            avatar = interaction.user.display_avatar or interaction.user.default_avatar

            if 66 >= extraneous_data[0] > 33:

                pmulti = await Economy.get_pmulti_data_only(interaction.user, conn)
                new_multi = SERVER_MULTIPLIERS.setdefault(interaction.guild.id, 0) + pmulti[0]
                bonus = floor((new_multi / 100) * extraneous_data[1])
                total = bonus + extraneous_data[1]
                new_balance = await Economy.update_bank_new(interaction.user, conn, total)

                self.foo = False
                await self.disable_all_items()
                win = discord.Embed(title=f'{interaction.user.display_name}\'s winning high-low game',
                                    description=f'- You just won **\U000023e3 {total:,}**.\n'
                                                f' - {PREMIUM_CURRENCY} **{bonus:,}** won from a **{new_multi}**% multi.\n'
                                                f'- Your new `wallet` balance is **\U000023e3 {new_balance[0]:,}**.\n',
                                    colour=discord.Color.brand_green())

                win.set_thumbnail(url=avatar.url)
                await interaction.followup.send(embed=win)
                await interaction.message.edit(
                    content=f'{interaction.user.display_name}, you won. the number i was guessing '
                            f'of was **{extraneous_data[0]}**', view=None)
                extraneous_data.clear()
            else:
                new_balance = await Economy.update_bank_new(interaction.user, conn, -int(extraneous_data[1]))
                self.foo = False
                await self.disable_all_items()

                lose = discord.Embed(title=f'{interaction.user.display_name}\'s losing high-low game',
                                     description=f'- You lost **\U000023e3 {int(extraneous_data[1]):,}** robux.\n'
                                                 f'- No multiplier accrued due to a lost bet.\n'
                                                 f'- Your new balance is **\U000023e3 {new_balance[0]:,}**',
                                     colour=discord.Color.brand_red())
                lose.set_thumbnail(url=avatar.url)

                await interaction.followup.send(embed=lose)
                await interaction.message.edit(
                    content=f'{interaction.user.display_name}, you lost unfortunatley. the number i was guessing '
                            f'of was **{extraneous_data[0]}**', view=None)
                extraneous_data.clear()

    @discord.ui.button(label='High', style=discord.ButtonStyle.blurple)
    async def high(self, interaction: discord.Interaction, button: discord.ui.Button):
        button.disabled = True
        await interaction.response.defer(thinking=True, ephemeral=True) # type: ignore

        async with self.client.pool_connection.acquire() as conn: # type: ignore
            conn: asqlite_Connection
            avatar = interaction.user.display_avatar or interaction.user.default_avatar

            if 100 >= extraneous_data[0] > 66:

                pmulti = await Economy.get_pmulti_data_only(interaction.user, conn)
                new_multi = SERVER_MULTIPLIERS.setdefault(interaction.guild.id, 0) + pmulti[0]
                bonus = floor((new_multi / 100) * extraneous_data[1])
                total = bonus + extraneous_data[1]
                new_balance = await Economy.update_bank_new(interaction.user, conn, total)

                self.foo = False
                await self.disable_all_items()
                win = discord.Embed(title=f'{interaction.user.display_name}\'s winning high-low game',
                                    description=f'- You just won **\U000023e3 {total:,}**.\n'
                                                f' - {PREMIUM_CURRENCY} **{bonus:,}** won from a **{new_multi}**% multi.\n'
                                                f'- Your new `wallet` balance is **\U000023e3 {new_balance[0]:,}**.\n',
                                    colour=discord.Color.brand_green())
                win.set_thumbnail(url=avatar.url)

                await interaction.followup.send(embed=win)
                await interaction.message.edit(
                    content=f'{interaction.user.display_name}, you won. the number i was guessing '
                            f'of was **{extraneous_data[0]}**', view=None)
                extraneous_data.clear()
            else:
                new_balance = await Economy.update_bank_new(interaction.user, conn, -int(extraneous_data[1]))
                self.foo = False
                await self.disable_all_items()
                lose = discord.Embed(title=f'{interaction.user.display_name}\'s losing high-low game',
                                     description=f'- You lost **\U000023e3 {int(extraneous_data[1]):,}** robux.\n'
                                                 f'- No multiplier accrued due to a lost bet.\n'
                                                 f'- your new balance is **\U000023e3 {new_balance[0]:,}**',
                                     colour=discord.Color.brand_red())
                lose.set_thumbnail(url=avatar.url)

                await interaction.followup.send(embed=lose)
                await interaction.message.edit(
                    content=f'{interaction.user.display_name}, you lost unfortunatley. the number i was guessing '
                            f'of was **{extraneous_data[0]}**', view=None)
                extraneous_data.clear()


class UpdateInfo(discord.ui.Modal, title='Update your Profile'):
    bio = discord.ui.TextInput(
        style=discord.TextStyle.paragraph,
        label='Bio',
        required=True,
        placeholder="Insert your bio here.. (Type 'delete' or 'none' here to remove your existent bio)"
    )

    async def on_submit(self, interaction: discord.Interaction):
        user_id = str(interaction.user.id)
        val = get_profile_key_value(f"{user_id} bio")
        if val is None:
            phrases = "added your new"
            modify_profile("create", f"{user_id} bio", self.bio.value)
        else:
            if self.bio.value.lower() in {"delete", "none"}:
                res = modify_profile("delete", f"{user_id} bio", "placeholder")
                if res:
                    embed = discord.Embed(description=f'Your bio has been removed, {interaction.user.name}.\n**The '
                                                      f'changes have taken effect immediately.**', colour=0x2F3136)
                else:
                    embed = discord.Embed(
                        description=f'You don\'t have a bio yet. **Add one first.**', colour=0x2F3136)
                return await interaction.response.send_message(embed=embed) # type: ignore
            phrases = "updated your"
            modify_profile("update", f"{user_id} bio", self.bio.value)

        successful = discord.Embed(description=f"Successfully {phrases} bio to: \n"
                                               f"> {self.bio.value}\n"
                                               f"- The changes have taken effect immediatley.\n\n"
                                               f"{FEEDBACK_GLOBAL}", colour=0x2F3136)

        return await interaction.response.send_message(embed=successful) # type: ignore

    async def on_error(self, interaction: discord.Interaction, error):
        notsuccess = discord.Embed(description=f"An error occured.\n\n"
                                               f"> {error.__cause__}", colour=0x2F3136)

        return await interaction.response.send_message(embed=notsuccess) # type: ignore


class Economy(commands.Cog):

    def __init__(self, client: commands.Bot):
        self.client: commands.Bot = client


        self.not_registered = discord.Embed(description=f"## <:noacc:1183086855181324490> You are not registered.\n"
                                                        f"You'll need to register first before you can use this command"
                                                        f".\n"
                                                        f"### Already Registered?\n"
                                                        f"Find out what could've happened by calling the command "
                                                        f"[`>reasons`](https://www.google.com/).",
                                            colour=0x2F3136,
                                            timestamp=datetime.datetime.now(datetime.UTC))

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        role = interaction.guild.get_role(1168204249096785980)
        if (role in interaction.user.roles) or (role is None):
            return True
        return False

    async def cog_check(self, ctx: commands.Context) -> bool:
        role = ctx.guild.get_role(1168204249096785980)
        if (role in ctx.author.roles) or (role is None):
            return True
        return False

    async def fetch_tatsu_profile(self, user_id: int):
        """Get tatsu data associated with a given user."""
        wrapper = ApiWrapper(key=self.client.TATSU_API_KEY)  # type: ignore
        result = await wrapper.get_profile(user_id)
        return result

    @staticmethod
    def calculate_hand(hand):
        aces = hand.count(11)
        total = sum(hand)

        while total > 21 and aces > 0:
            total -= 10
            aces -= 1

        return total

    # ------------------ BANK FUNCS ------------------ #

    @staticmethod
    async def create_table(conn_input: asqlite_Connection) -> None:
        await conn_input.execute(f"CREATE TABLE IF NOT EXISTS `{BANK_TABLE_NAME}`(userID BIGINT)")
        for col in BANK_COLUMNS:
            await conn_input.execute(f"ALTER TABLE `{BANK_TABLE_NAME}` ADD COLUMN `{col}` BIGINT")
        await conn_input.commit()

    @staticmethod
    async def open_bank_new(user: discord.Member, conn_input: asqlite_Connection) -> None:
        """Register the user, if they don't exist. Only use in balance commands (reccommended.)"""
        users = await conn_input.execute(f"SELECT * FROM `{BANK_TABLE_NAME}` WHERE userID = ?", (user.id,))
        new_data = await users.fetchone()
        if new_data is None:
            await conn_input.execute(
                f"INSERT INTO `{BANK_TABLE_NAME}`(userID, {', '.join(BANK_COLUMNS)}) VALUES(?, {', '.join(['0'] * len(BANK_COLUMNS))})",
                (user.id,))

            ranumber = randint(10000000, 50000000)
            await conn_input.execute(f"UPDATE `{BANK_TABLE_NAME}` SET `wallet` = ? WHERE userID = ?",
                                     (ranumber, user.id))
            await conn_input.commit()

    @staticmethod
    async def can_call_out(user: discord.Member, conn_input: asqlite_Connection):
        """Check if the user is NOT in the database and therefore not registered (evaluates True if not in db).
        Example usage:
        if await self.can_call_out(interaction.user, conn):
            await interaction.response.send_message(embed=self.not_registered)

        This is what should be done all the time to check if a user IS NOT REGISTERED.
        """
        result = await conn_input.execute(f"SELECT EXISTS (SELECT 1 FROM `{BANK_TABLE_NAME}` WHERE userID = ?)",
                                          (user.id,))
        exists = await result.fetchone()

        return not exists[0]

    @staticmethod
    async def can_call_out_either(user1: discord.Member, user2: discord.Member, conn_input: asqlite_Connection):
        """Check if both users are in the database. (evaluates True if both users are in db.)
        Example usage:

        if not(await self.can_call_out_either(interaction.user, username, conn)):
            do something

        This is what should be done all the time to check if a user IS NOT REGISTERED."""
        users = await conn_input.execute(f"SELECT COUNT(*) FROM `{BANK_TABLE_NAME}` WHERE userID IN (?, ?)",
                                         (user1.id, user2.id))
        count = await users.fetchone()

        return count[0] == 2

    @staticmethod
    async def get_bank_data_new(user: discord.Member, conn_input: asqlite_Connection) -> Optional[Any]:
        """Retrieves robux data and other gambling stats from a registered user."""
        data = await conn_input.execute(f"SELECT * FROM `{BANK_TABLE_NAME}` WHERE userID = ?", (user.id,))
        data = await data.fetchone()
        return data

    @staticmethod
    async def get_wallet_data_only(user: discord.Member, conn_input: asqlite_Connection) -> Optional[Any]:
        """Retrieves the wallet amount only from a registered user's bank data."""
        data = await conn_input.execute(f"SELECT wallet FROM `{BANK_TABLE_NAME}` WHERE userID = ?", (user.id,))
        wallet_amount = await data.fetchone()
        return wallet_amount[0]

    @staticmethod
    async def get_spec_bank_data(user: discord.Member, field_name: str, conn_input: asqlite_Connection) -> Optional[
        Any]:
        """Retrieves a specific field name only from the bank table."""
        data = await conn_input.execute(f"SELECT {field_name} FROM `{BANK_TABLE_NAME}` WHERE userID = ?", (user.id,))
        field_val = await data.fetchone()
        return field_val[0]

    @staticmethod
    async def update_bank_new(user: discord.Member | discord.User, conn_input: asqlite_Connection, amount: Union[float, int] = 0,
                              mode: str = "wallet") -> Optional[Any]:
        """Modifies a user's balance in a given mode: either wallet (default) or bank.
        It also returns the new balance in the given mode, if any (defaults to wallet).
        Note that conn_input is not the last parameter, it is the second parameter to be included."""

        data = await conn_input.execute(
            f"UPDATE `{BANK_TABLE_NAME}` SET `{mode}` = `{mode}` + ? WHERE userID = ? RETURNING `{mode}`",
            (amount, user.id))
        users = await data.fetchone()
        return users

    # ------------------ INVENTORY FUNCS ------------------ #

    @staticmethod
    async def open_inv_new(user: discord.Member, conn_input: asqlite_Connection) -> None:
        """Register a new user's inventory records into the db."""

        data = await conn_input.execute(f"SELECT * FROM `{INV_TABLE_NAME}` WHERE userID = ?", (user.id,))
        data = await data.fetchone()
        if data is None:
            await conn_input.execute(f"INSERT INTO `{INV_TABLE_NAME}`(userID) VALUES(?)", (user.id,))

            for item in SHOP_ITEMS:
                item_name = item["name"]
                await conn_input.execute(f"UPDATE `{INV_TABLE_NAME}` SET `{item_name}` = ? WHERE userID = ?",
                                         (0, user.id,))
            await conn_input.commit()

    @staticmethod
    async def get_inv_data_new(user: discord.Member, conn_input: asqlite_Connection) -> Optional[Any]:
        """Fetch inventory data."""
        users = await conn_input.execute(f"SELECT * FROM `{INV_TABLE_NAME}` WHERE userID = ?", (user.id,))
        users = await users.fetchone()
        return users

    @staticmethod
    async def get_one_inv_data_new(user: discord.Member, item: str, conn_input: asqlite_Connection) -> Optional[Any]:
        """Fetch inventory data from one specific item inputted."""
        users = await conn_input.execute(f"SELECT {item} FROM `{INV_TABLE_NAME}` WHERE userID = ?", (user.id,))
        users = await users.fetchone()
        return users[0]

    @staticmethod
    async def update_inv_new(user: discord.Member, amount: Union[float, int], mode: str,
                             conn_input: asqlite_Connection) -> Optional[Any]:
        """Modify a user's inventory."""

        data = await conn_input.execute(f"SELECT * FROM `{INV_TABLE_NAME}` WHERE userID = ?", (user.id,))
        data = await data.fetchone()
        if data is not None:
            await conn_input.execute(f"UPDATE `{INV_TABLE_NAME}` SET `{mode}` = `{mode}` + ? WHERE userID = ?",
                                     (amount, user.id))
            await conn_input.commit()

        # Retrieve and return the updated value
        updated_user = await conn_input.execute(f"SELECT `{mode}` FROM `{INV_TABLE_NAME}` WHERE userID = ?", (user.id,))
        updated_user = await updated_user.fetchone()
        return updated_user

    @staticmethod
    async def change_inv_new(user: discord.Member, amount: Union[float, int, None], mode: str,
                             conn_input: asqlite_Connection) -> Optional[Any]:

        data = await conn_input.execute(f"SELECT * FROM `{INV_TABLE_NAME}` WHERE userID = ?", (user.id,))
        data = await data.fetchone()
        if data is not None:
            await conn_input.execute(f"UPDATE `{INV_TABLE_NAME}` SET `{mode}` = ? WHERE userID = ?", (amount, user.id))
            await conn_input.commit()

        # Retrieve and return the updated value
        updated_data = await conn_input.execute(f"SELECT `{mode}` FROM `{INV_TABLE_NAME}` WHERE userID = ?", (user.id,))
        updated_data = await updated_data.fetchone()
        return updated_data

    # ------------ JOB FUNCS ----------------

    @staticmethod
    async def get_job_data_only(user: discord.Member, conn_input: asqlite_Connection) -> Optional[Any]:
        """Retrieves the users current job."""
        data = await conn_input.execute(f"SELECT job FROM `{BANK_TABLE_NAME}` WHERE userID = ?", (user.id,))
        job_name = await data.fetchone()
        return job_name

    @staticmethod
    async def change_job_new(user: discord.Member, conn_input: asqlite_Connection,
                                job_name: str) -> Optional[Any]:
        """Modifies a user's job, returning the new job after changes were made."""

        data = await conn_input.execute(
            f"UPDATE `{BANK_TABLE_NAME}` SET `job` = ? WHERE userID = ? RETURNING `job`",
            (job_name, user.id))
        await conn_input.commit()
        users = await data.fetchone()
        return users

    # ------------ cooldowns ----------------

    @staticmethod
    async def open_cooldowns(user: discord.Member, conn_input: asqlite_Connection):
        cd_columns = ["slaywork", "casino"]
        users = await conn_input.execute(f"SELECT * FROM `{COOLDOWN_TABLE_NAME}` WHERE userID = ?", (user.id,))
        new_data = await users.fetchone()
        if new_data is None:
            await conn_input.execute(
                f"INSERT INTO `{COOLDOWN_TABLE_NAME}`(userID, {', '.join(cd_columns)}) VALUES(?, {', '.join(['0'] * len(cd_columns))})",
                (user.id,))
            await conn_input.commit()
            return 1

    @staticmethod
    async def fetch_cooldown(conn_input: asqlite_Connection, *, user: discord.Member, cooldown_type: str):
        """Fetch a cooldown from the cooldowns table. Requires indexing."""
        data = await conn_input.execute(f"SELECT `{cooldown_type}` FROM `{'cooldowns'}` WHERE userID = ?", (user.id,))
        data = await data.fetchone()
        return data

    @staticmethod
    async def update_cooldown(conn_input: asqlite_Connection, *, user: discord.Member, cooldown_type: str, new_cd: str):
        """Update a user's cooldown. Requires accessing the return value via the index, so [0].

        Use this func to reset and create a cooldown."""
        data = await conn_input.execute(
            f"UPDATE `{'cooldowns'}` SET `{cooldown_type}` = ? WHERE userID = ? RETURNING `{cooldown_type}`",
            (new_cd, user.id))
        await conn_input.commit()
        users = await data.fetchone()
        return users

    # ------------ PMULTI FUNCS -------------

    @staticmethod
    async def get_pmulti_data_only(user: discord.Member, conn_input: asqlite_Connection) -> Optional[Any]:
        """Retrieves the pmulti amount only from a registered user's bank data."""
        data = await conn_input.execute(f"SELECT pmulti FROM `{BANK_TABLE_NAME}` WHERE userID = ?", (user.id,))
        pmulti_amt = await data.fetchone()
        return pmulti_amt

    @staticmethod
    async def change_pmulti_new(user: discord.Member, conn_input: asqlite_Connection, amount: Union[float, int] = 0,
                                mode: str = "pmulti") -> Optional[Any]:
        """Modifies a user's personal multiplier, returning the new multiplier after changes were made."""

        data = await conn_input.execute(
            f"UPDATE `{BANK_TABLE_NAME}` SET `{mode}` = ? WHERE userID = ? RETURNING `{mode}`",
            (amount, user.id))
        await conn_input.commit()
        users = await data.fetchone()
        return users

    # ------------------- slay ----------------

    @staticmethod
    async def open_slay(conn_input: asqlite_Connection, user: discord.Member, sn: str, gd: str, pd: float, happy: int, stus: int):
        sql = "INSERT INTO slay (slay_name, userID, gender, productivity, happiness, status) VALUES (?, ?, ?, ?, ?, ?)"
        values = (sn, user.id, gd, pd, happy, stus)

        await conn_input.execute(sql, values)
        await conn_input.commit()

    @staticmethod
    async def get_slays(conn_input: asqlite_Connection, user: discord.Member):
        # Define your SQL statement with a placeholder for the test value
        sql = "SELECT * FROM slay WHERE userID = ?"

        # Execute the SQL statement with the test value as a parameter
        new_data = await conn_input.execute(sql, (user.id,))

        # Fetch all rows that match the condition
        selected_rows = await new_data.fetchall()

        return selected_rows

    @staticmethod
    async def change_slay_field(conn_input: asqlite_Connection, user: discord.Member, field: str, new_val: Any):
        # Define your SQL statement with a placeholder for the test value
        await conn_input.execute(
            f"UPDATE `{SLAY_TABLE_NAME}` SET `{field}` = ? WHERE userID = ?",
            (new_val, user.id,))
        await conn_input.commit()

    @staticmethod
    async def delete_slay(conn_input: asqlite_Connection, user: discord.Member, slay_name):
        """Remove a single slay row from the db and return 1 if the row existed, 0 otherwise."""

        # Define your SQL statement with the "IF EXISTS" clause
        sql = "DELETE FROM slay WHERE userID = ? AND slay_name = ?"

        # Execute the SQL statement with the user ID and slay name as parameters
        await conn_input.execute(sql, (user.id, slay_name))
        await conn_input.commit()

    @staticmethod
    async def count_happiness_above_threshold(conn_input: asqlite_Connection, user: discord.Member):
        """Count the number of rows for a given user ID where happiness is greater than 30."""

        # Define your SQL statement to retrieve happiness values for a specific user ID
        sql = "SELECT happiness FROM slay WHERE userID = ?"

        # Fetch all rows with the specified user ID
        rows = await conn_input.fetchall(sql, user.id)

        # Initialize a variable to count happiness values above 30
        count = 0

        # Iterate through the rows and check happiness values
        for row in rows:
            happiness_value = row['happiness']
            if happiness_value > 30:
                count += 1

        return count

    @staticmethod
    async def modify_happiness(conn_input: asqlite_Connection, slaves_for_user: discord.Member):
        """Modify every row's happiness field for a given user ID with a different random number."""

        # Define your SQL statement to update the happiness field with a random number
        sql = "UPDATE slay SET happiness = ? WHERE userID = ?"

        # Retrieve all rows with the specified user ID
        rows = await conn_input.fetchall("SELECT * FROM slay WHERE userID = ?", slaves_for_user.id)

        # Iterate through the rows and update the happiness field with a random number
        for _ in rows:
            random_happiness = randint(20, 40)  # Adjust the range as needed
            await conn_input.execute(sql, (random_happiness, slaves_for_user.id))

        await conn_input.commit()

    # ----------- END OF ECONOMY FUNCS, HERE ON IS JUST COMMANDS --------------


    pmulti = app_commands.Group(name='multi', description='[Group Command] No description.',
                                guild_only=True, guild_ids=[829053898333225010, 780397076273954886])

    @pmulti.command(name='view', description='view personal and global multipliers.')
    @app_commands.describe(user_name="whose multiplier to view")
    @app_commands.rename(user_name='user')
    @app_commands.checks.dynamic_cooldown(owners_nolimit)
    async def my_multi(self, interaction: discord.Interaction, user_name: Optional[discord.Member]):

        async with self.client.pool_connection.acquire() as conn: # type: ignore
            conn: asqlite_Connection

            if user_name is None:
                user_name = interaction.user

            if await Economy.can_call_out(user_name, conn):
                return await interaction.response.send_message(embed=NOT_REGISTERED) # type: ignore
            their_multi = await Economy.get_pmulti_data_only(user_name, conn)

            avatar = user_name.display_avatar or user_name.default_avatar
            if their_multi[0] == 0 and (user_name.id == interaction.user.id):  # only author can create their own pmulti
                rand = randint(30, 90)
                await Economy.change_pmulti_new(user_name, conn, rand)
                multi_own = discord.Embed(colour=0x2F3136,
                                          description=f'# Your new personal multiplier has been created.\n'
                                                      f'- Starting now, your new personal multiplier is **{rand}**%\n'
                                                      f' - You cannot change this multiplier, it is fixed and unique '
                                                      f'to your account.\n'
                                                      f' - Your personal multiplier will be used to determine the incre'
                                                      f'ase bonus rewards you receive when claiming rewards, gambling, '
                                                      f'and receiving robux (indicated by a <:robuxpremium:11744178153'
                                                      f'27998012>).\n'
                                                      f' - That means under these given conditions, you will receive '
                                                      f'**{rand}**% more of an asset/robux depending on the case.\n\n'
                                                      f'If you\'ve received a low roll, there is a very *small chance* '
                                                      f'you can request for a buff (in very unfortunate cases).')
            elif (their_multi[0] == 0) and (user_name.id != interaction.user.id):
                multi_own = discord.Embed(colour=0x2F3136, description=f'{user_name.name} doesn\'t have a personal '
                                                                       f'multiplier associated with their account.')
                multi_own.set_author(name=f'Viewing {user_name.name}\'s multipliers', icon_url=avatar.url)
            else:
                server_bs = SERVER_MULTIPLIERS.setdefault(interaction.guild.id, 0)
                multi_own = discord.Embed(colour=0x2F3136,
                                          description=f'Personal multiplier: **{their_multi[0]:,}**%\n'
                                                      f'*A multiplier that is unique to a user and is usually a fixed '
                                                      f'amount.*\n\n'
                                                      f'Global multiplier: **{server_bs:,}**%\n'
                                                      f'*A multiplier that changes based on the server you are calling'
                                                      f' commands in.*')
                multi_own.set_author(name=f'Viewing {user_name.name}\'s multipliers', icon_url=avatar.url)
                multi_own.set_thumbnail(url=avatar.url)

            await interaction.response.send_message(embed=multi_own) # type: ignore

    share = app_commands.Group(name='share', description='[Group Command] share different assets with others.',
                               guild_only=True, guild_ids=[829053898333225010, 780397076273954886])

    @share.command(name="robux", description="share robux with another user.")
    @app_commands.describe(other='the user to give robux to',
                           amount='the amount of robux to give them. Supports Shortcuts (max, all, exponents).')
    @app_commands.rename(other='user')
    @app_commands.checks.dynamic_cooldown(owners_nolimit)
    async def give_robux(self, interaction: discord.Interaction, other: discord.Member, amount: str):
        clr = interaction.user

        async with self.client.pool_connection.acquire() as conn: # type: ignore
            conn: asqlite_Connection

            if not (await self.can_call_out_either(interaction.user, other, conn)):
                await interaction.response.defer(thinking=True) # type: ignore
                embed = membed(f'- Either you or {other.name} does not have an account.\n'
                               f' - </balance:1179817617435926686> to register.')
                return await interaction.followup.send(embed=embed)
            else:
                real_amount = determine_exponent(amount)
                wallet_amt_host = await Economy.get_wallet_data_only(interaction.user, conn)
                avatar = interaction.user.display_avatar or interaction.user.default_avatar

                if isinstance(real_amount, str):
                    if real_amount.lower() == 'all' or real_amount.lower() == 'max':
                        real_amount = wallet_amt_host
                    else:
                        return await interaction.response.send_message(embed=ERR_UNREASON) # type: ignore
                    host_amt = await Economy.update_bank_new(interaction.user, conn, -int(real_amount))
                    recp_amt = await Economy.update_bank_new(other, conn, int(real_amount))
                else:
                    if real_amount == 0:
                        return await interaction.response.send_message(embed=ERR_UNREASON) # type: ignore
                    elif real_amount > wallet_amt_host:
                        return await interaction.response.send_message(embed=ERR_UNREASON) # type: ignore
                    else:
                        host_amt = await Economy.update_bank_new(interaction.user, conn, -int(real_amount))
                        recp_amt = await Economy.update_bank_new(other, conn, int(real_amount))

                embed = discord.Embed(title='Transaction Complete',
                                      description=f'- {clr.mention} has given {other.mention} \U000023e3 {real_amount:,}\n'
                                                  f'- {clr.mention} now has \U000023e3 {host_amt[0]:,} in their wallet.\n'
                                                  f'- {other.mention} now has \U000023e3 {recp_amt[0]:,} in their wallet.',
                                      colour=0x2F3136)
                embed.set_author(name=f'Transaction made by {interaction.user.name}', icon_url=avatar.url)
                return await interaction.response.send_message(embed=embed) # type: ignore

    @share.command(name='items', description='share items with another user.')
    @app_commands.describe(item_name='the name of the item you want to share.',
                           amount='the amount of this item to share', username='the name of the user to share it with')
    @app_commands.checks.dynamic_cooldown(owners_nolimit)
    async def give_items(self, interaction: discord.Interaction,
                         item_name: Literal['Keycard', 'Trophy', 'Clan License', 'Resistor', 'Amulet', 'Dynamic Item', 'Hyperion', 'Crisis', 'Odd Eye'],
                         amount: Literal[1, 2, 3, 4, 5], username: discord.Member):
        primm = interaction.user.mention
        otherm = username.mention

        async with self.client.pool_connection.acquire() as conn: # type: ignore
            conn: asqlite_Connection
            item_name = item_name.replace(" ", "_")
            if not(await self.can_call_out_either(interaction.user, username, conn)):
                embed = discord.Embed(description=f'Either you or {username.name} does not have an account.\n'
                                                  f'</balance:1179817617435926686> to register.',
                                      colour=0x2F3136)
                return await interaction.response.send_message(embed=embed) # type: ignore
            else:
                quantity = await self.update_inv_new(interaction.user, 0, item_name, conn)
                if amount > quantity[0]:  # if interaction user tries to give more than (s)he owns
                    return await interaction.response.send_message(embed=ERR_UNREASON) # type: ignore
                else:
                    avatar = interaction.user.display_avatar or interaction.user.default_avatar
                    receiver = await self.update_inv_new(username, +amount, item_name, conn)
                    new_after_transaction = quantity[0] - amount
                    sender = await self.change_inv_new(interaction.user, new_after_transaction, item_name, conn)
                    item_name = " ".join(item_name.split("_"))
                    send_amt = make_plural(item_name, amount)
                    send_cont = make_plural(item_name, sender[0])
                    teir_cont = make_plural(item_name, receiver[0])
                    transaction_success = discord.Embed(title="Transaction Complete",
                                                        description=f'- {primm} has given **{amount}** {send_amt}\n'
                                                                    f'- {primm} now has **{sender[0]}** {send_cont}\n'
                                                                    f'- {otherm} now has **{receiver[0]}** {teir_cont}',
                                                        colour=interaction.user.colour)
                    transaction_success.set_author(name=f'Transaction made by {interaction.user.name}',
                                                   icon_url=avatar.url)

                    await interaction.response.send_message(embed=transaction_success) # type: ignore

    shop = app_commands.Group(name='shop', description='[Group Command] view items available for purchase.', guild_only=True,
                              guild_ids=[829053898333225010, 780397076273954886])

    @shop.command(name='view', description='view items that are available for purchase.')
    @app_commands.checks.dynamic_cooldown(owners_nolimit)
    async def view_the_shop(self, interaction: discord.Interaction):

        async with self.client.pool_connection.acquire() as conn: # type: ignore
            conn: asqlite_Connection
            if await self.can_call_out(interaction.user, conn):
                return await interaction.response.send_message(embed=self.not_registered) # type: ignore
            additional_notes: set = set()
            em = discord.Embed(
                title="Shop",
                color=0x2F3136
            )

            for item in SHOP_ITEMS:
                name_beta = item["name"].split("_")
                name = " ".join(name_beta)
                item_info = item["info"]
                item_stock = get_stock(name)

                additional_notes.add(
                    f"{item['emoji']} __{name}__ \U00002014 [\U000023e3 **{item['cost']:,}**](https://youtu.be/dQw4w9WgXcQ)\n"
                    f"{ARROW}{item_info}\n"
                    f"{ARROW}ID: `{item['id']}`\n"
                    f"{ARROW}Quantity Remaining: `{item_stock}`")
                all_items = "\n\n".join(additional_notes)
                em.description = f"{all_items}"
            await interaction.response.send_message(embed=em) # type: ignore

    @shop.command(name='lookup', description='get info about a particular item.')
    @app_commands.describe(item_name='the name of the item you want to sell.')
    async def lookup_item(self, interaction: discord.Interaction,
                     item_name: Literal['Keycard', 'Trophy', 'Clan License', 'Resistor', 'Amulet', 'Dynamic Item', 'Hyperion', 'Crisis', 'Odd Eye']):

        item_stock = get_stock(item_name)
        match item_stock:
            case 0:
                stock_resp = f"*This item is currently out of stock.*"
            case 1 | 2 | 3:
                stock_resp = f"*Shortage in stocks, only **{item_stock}** remain.*"
            case _:
                stock_resp = f"*No stock shortages currently for this item ({item_stock} available).*"
        match item_name:
            case 'Keycard':
                clr = discord.Colour.from_rgb(80, 85, 252)
            case 'Trophy':
                clr = discord.Colour.from_rgb(254, 204, 78)
            case 'Clan License':
                clr = discord.Colour.from_rgb(209, 30, 54)
            case 'Resistor':
                clr = discord.Colour.from_rgb(49, 51, 56)
            case _:
                clr = discord.Colour.from_rgb(54, 123, 112)

        for item in SHOP_ITEMS:
            stored = item["name"]
            name_beta = stored.split("_")
            name = " ".join(name_beta)
            cost = item["cost"]
            item_info = item["info"]

            if name == item_name:
                async with self.client.pool_connection.acquire() as conn:  # type: ignore
                    conn: asqlite_Connection
                    data = await conn.execute(f"SELECT COUNT(*) FROM inventory WHERE {stored} > 0")
                    data = await data.fetchone()
                    owned_by_how_many = data[0]

                em = discord.Embed(
                    description=f"# About Item: {name} {item['emoji']}\n"
                                f"{ARROW}{item_info}\n"
                                f"{ARROW}**[Stock Status]**: {stock_resp}\n"
                                f"{ARROW}**{owned_by_how_many}** {make_plural("person", owned_by_how_many)} "
                                f"{plural_for_own(owned_by_how_many)} this item.",
                    colour=clr
                )

                sell_amt = int(abs(int(cost) / 4))

                em.add_field(name="Buying price", value=f"<:robux:1146394968882151434> {cost:,}")
                em.add_field(name="Selling price",
                             value=f"<:robux:1146394968882151434> {sell_amt:,}")

                return await interaction.response.send_message(embed=em) # type: ignore

        await interaction.response.send_message(f"There is no item named {item_name}.") # type: ignore

    profile = app_commands.Group(name='editprofile', description='[Group Command] custom-profile-orientated.',
                                 guild_only=True, guild_ids=[829053898333225010, 780397076273954886])

    @profile.command(name='bio', description='add a bio to your profile.')
    @app_commands.checks.dynamic_cooldown(owners_nolimit)
    async def update_bio_profile(self, interaction: discord.Interaction):
        async with self.client.pool_connection.acquire() as conn: # type: ignore
            conn: asqlite_Connection
            if await self.can_call_out(interaction.user, conn):
                embed = discord.Embed(colour=0x2F3136,
                                      description='You cannot use this command until you register.')
                return await interaction.response.send_message(embed=embed) # type: ignore
            await interaction.response.send_modal(UpdateInfo()) # type: ignore

    @profile.command(name='avatar', description='modify the avatar displayed on your profile.')
    @app_commands.describe(url='The url of the new avatar. Type "reset" to remove.')
    @app_commands.checks.dynamic_cooldown(owners_nolimit)
    async def update_avatar_profile(self, interaction: discord.Interaction, url: str):

        async with self.client.pool_connection.acquire() as conn: # type: ignore
            conn: asqlite_Connection
            if await self.can_call_out(interaction.user, conn):
                embed = discord.Embed(colour=0x2F3136,
                                      description='You cannot use this command until you register.')
                return await interaction.response.send_message(embed=embed) # type: ignore

        if url.lower() in {"reset", "default", "delete"}:
            res = modify_profile("delete", f"{interaction.user.id} avatar_url", url)
            match res:
                case 0:
                    res = "No avatar url was found under your account."
                case _:
                    res = "Your avatar url was removed."
            result = discord.Embed(colour=0x2F3136, description=res)
            return await interaction.response.send_message(embed=result) # type: ignore

        successful = discord.Embed(colour=0x2F3136,
                                   description=f"Your avatar url has been added. If it is a valid url, it will look "
                                               f"like this ----->")
        successful.set_thumbnail(url=url)
        modify_profile("update", f"{interaction.user.id} avatar_url", url)
        await interaction.response.send_message(embed=successful) # type: ignore

    @update_avatar_profile.error
    async def uap_error(self, interaction: discord.Interaction, err: discord.app_commands.AppCommandError):
        if isinstance(err, discord.app_commands.CommandInvokeError):
            successful = discord.Embed(colour=0x2F3136,
                                       description=f"The avatar url requested for could not be added:\n"
                                                   f"- The URL provided was not well formed.\n"
                                                   f"- Discord embed thumbnails have specific image requirements to "
                                                   f"ensure proper display.\n"
                                                   f" - **The recommended size for a thumbnail is 80x80 pixels.**")

            return await interaction.response.send_message(embed=successful) # type: ignore

    @profile.command(name='visibility', description='hide your profile for privacy.')
    @app_commands.describe(mode='Toggle public or private profile')
    @app_commands.checks.dynamic_cooldown(owners_nolimit)
    async def update_vis_profile(self, interaction: discord.Interaction,
                                 mode: Literal['public', 'private']):
        async with self.client.pool_connection.acquire() as conn: # type: ignore
            conn: asqlite_Connection
            if await self.can_call_out(interaction.user, conn):
                embed = discord.Embed(colour=0x2F3136,
                                      description='You cannot use this command until you register.')
                return await interaction.response.send_message(embed=embed) # type: ignore

        modify_profile("update", f"{interaction.user.id} vis", mode)
        await interaction.response.send_message(f"Your profile is now {mode}.", ephemeral=True, delete_after=7.5) # type: ignore

    slay = app_commands.Group(name='slay', description='[Group Command] manage your slay.',
                              guild_only=True,
                              guild_ids=[829053898333225010, 780397076273954886])

    @slay.command(name='hire', description='hire your own slay.')
    @app_commands.describe(user='member to make a slay. if empty, specify new_slay_name.',
                           new_slay_name='The name of your slay, if you didn\'t pick a user.',
                           gender="the gender of your slay, doesn't have to be true..",
                           investment="how much robux your willing to spend on this slay (no shortcuts)")
    async def hire_slv(self, interaction: discord.Interaction, user: Optional[discord.Member],
                       new_slay_name: Optional[str], gender: Literal["male", "female"], investment: int):
        await interaction.response.defer(thinking=True) # type: ignore
        async with self.client.pool_connection.acquire() as conn: # type: ignore
            conn: asqlite_Connection

            if await self.can_call_out(interaction.user, conn):
                return await interaction.followup.send(embed=self.not_registered)

            wallet_amt = await self.get_wallet_data_only(interaction.user, conn)

            if user and (interaction.user.id == user.id):
                return await interaction.followup.send("Why would you make yourself a slay?")
            elif (user is None) and (new_slay_name is None):
                return await interaction.followup.send("You did not input any slay.")
            elif (new_slay_name is not None) and (user is not None):
                return await interaction.followup.send("You cannot name your slay if the user has also "
                                                       "been inputted. Remove this argument if needed.")
            elif abs(investment) > wallet_amt:
                return await interaction.followup.send(
                    embed=membed("Your slay will not obey your orders if you do not "
                                 "guarantee your investment.\n"
                                 "Hook up some more robux in your investment to increase your slay's productivity."))
            else:

                investment = abs(investment)
                await self.update_bank_new(interaction.user, conn, -investment)
                prod = labour_productivity_via(investment=investment)
                slays = await self.get_slays(conn, interaction.user)
                if new_slay_name is None:
                    new_slay_name = user.display_name

                if not slays:

                    await self.open_slay(conn, interaction.user, new_slay_name, gender, prod, 100, 1)
                    slayy = discord.Embed(description=f"## Slay Summary\n"
                                                      f"- Paid **\U000023e3 {investment:,}** for the following:\n"
                                                      f" - Your brand new slay named {new_slay_name}\n"
                                                      f" - {new_slay_name} has a productivity level "
                                                      f"of `{prod}`.",
                                          colour=discord.Colour.from_rgb(0, 0, 0))
                    slayy.set_footer(text="1/6 slots consumed")
                    await interaction.followup.send(embed=slayy)

                else:
                    if len(slays) >= 6:
                        return await interaction.followup.send(
                            embed=membed("## You have reached the maximum slay quota for now.\n"
                                         "You must abandon a current slay before hiring a new one."))

                    for slay in slays:
                        name =  slay[0]
                        if new_slay_name == name:
                            return await interaction.followup.send(
                                "You already own a slay with that name."
                            )

                    await self.open_slay(conn, interaction.user, new_slay_name, gender, prod, 100, 1)

                    slayyy = discord.Embed(description=f"## Slay Summary\n"
                                                      f"- Paid **\U000023e3 {investment:,}** for the following:\n"
                                                      f" - Your brand new slay named {new_slay_name}\n"
                                                      f" - {new_slay_name} has a productivity level "
                                                      f"of `{prod}`.",
                                          color=discord.Color.from_rgb(0, 0, 0))
                    slayyy.set_footer(text=f"{len(slays)+1}/6 slay slots consumed")

                    await interaction.followup.send(embed=slayyy)

    @slay.command(name='abandon', description='abandon your slay')
    @app_commands.rename(slay_purge='slay')
    @app_commands.describe(user='member to make a slay. if empty, specify new_slay_name.',
                           slay_purge='the name of your slay, if you didn\'t pick a user.')
    async def abandon_slv(self, interaction: discord.Interaction, user: Optional[discord.Member],
                          slay_purge: Optional[str]):
        async with self.client.pool_connection.acquire() as conn: # type: ignore
            conn: asqlite_Connection

            if await self.can_call_out(interaction.user, conn):
                return await interaction.followup.send(embed=self.not_registered)

            if (user is None) and (slay_purge is None):
                return await interaction.response.send_message("You did not input any slay.") # type: ignore
            elif (slay_purge is not None) and (user is not None):
                return await interaction.response.send_message("You cannot name your slay if the user has also " # type: ignore
                                                               "been inputted. Remove this argument if needed.")
            else:
                slays = await self.get_slays(conn, interaction.user)

                if slay_purge is None:
                    slay_purge = user.display_name

                await self.delete_slay(conn, interaction.user, slay_purge)

                return await interaction.response.send_message( # type: ignore
                embed=membed(f"Attempted to remove {slay_purge} from your owned slays.\n"
                             f" - {len(slays)}/6 total slay slots consumed."))


    @slay.command(name='viewall', description='view all slays owned by a user.')
    @app_commands.describe(user='the user to view the slays of')
    async def view_all_slays(self, interaction: discord.Interaction, user: Optional[discord.Member]):

        async with self.client.pool_connection.acquire() as conn: # type: ignore
            conn: asqlite_Connection

            if await self.can_call_out(interaction.user, conn):
                return await interaction.followup.send(embed=NOT_REGISTERED)

            if user is None:
                user = interaction.user
            stats = {1: "Free", 0: "Working"}
            slays = await self.get_slays(conn, interaction.user)
            embed = discord.Embed(colour=0x2F3136)
            avatar = user.display_avatar or user.default_avatar
            embed.set_author(name=f'{user.name}\'s Slays', icon_url=avatar.url)

            if len(slays) == 0:
                embed.add_field(name="Nothingness.", value="This user has no slays yet.", inline=False)
                return await interaction.response.send_message(embed=embed) # type: ignore

            for slay in slays:
                if 66 <= slay[4] <= 100:
                    state = "\U0001f603 "
                elif 33 <= slay[4] < 66:
                    state = "\U0001f610 "
                else:
                    state = "\U0001f641 "
                embed.add_field(name=f'{state}{slay[0]}', value=f'{ARROW}{slay[2]}\n{ARROW}{slay[3]}'
                                                              f'\n{ARROW}{stats.get(slay[5])}')

            embed.set_footer(text=f"{len(slays)}/6 slay slots consumed")
            await interaction.response.send_message(embed=embed) # type: ignore

    @slay.command(name='work', description="assign your slays to do tasks for you.")
    @app_commands.describe(duration="the time spent working (e.g, 18h or 1d 3h)")
    async def make_slay_work_pay(self, interaction: discord.Interaction, duration: str):
        await interaction.response.defer(thinking=True) # type: ignore

        try:
            async with self.client.pool_connection.acquire() as conn: # type: ignore
                conn: asqlite_Connection

                if await self.can_call_out(interaction.user, conn):
                    return await interaction.followup.send(embed=NOT_REGISTERED)

                if len(await self.get_slays(conn, interaction.user)) == 0:
                    return await interaction.followup.send(
                        embed=membed("You got no slays to send to work.")
                    )

                res_duration = parse_duration(duration)  # a datetime object

                cooldown = await self.fetch_cooldown(conn, user=interaction.user, cooldown_type="slaywork")
                # If the cooldown is nothing by default
                if cooldown is not None:
                    if cooldown[0] in {"0", 0}:
                        day = number_to_ordinal(int(res_duration.strftime("%d")))
                        shallow = res_duration.strftime(f"%A the {day} of %B at %I:%M%p")
                        await self.change_slay_field(conn, interaction.user, "status", 0)

                        res_duration = datetime_to_string(res_duration)
                        await self.update_cooldown(conn, user=interaction.user, cooldown_type="slaywork", new_cd=res_duration)
                        await interaction.followup.send(f"## Your slay(s) have been sent off.\n"
                                                        f"{ARROW}As commanded, they will work until {shallow} (UTC).")
                    else:
                        cooldown = string_to_datetime(cooldown[0])
                        now = datetime.datetime.now()
                        diff = cooldown - now

                        if diff.total_seconds() <= 0:

                            slays = await self.get_slays(conn, interaction.user)
                            content = set()
                            await self.update_cooldown(conn, user=interaction.user, cooldown_type="slaywork",
                                                       new_cd="0")

                            labour_actions: dict = {
                                0: "making numerous bets at the casino",
                                1: "working at factory made for slays",
                                2: "playing with the slot machine",
                                3: "doing multiple high-low games",
                                4: "bidding at an auction",
                                5: "robbing vulnerable victims",
                                6: "robbing the central bank"
                            }

                            sad_actions: dict = {
                                0: "isolating oneself from friends and family",
                                1: "struggling with a mundane job at a soul-crushing factory",
                                2: "mindlessly hoping for a change and working for better treatment",
                                3: "seeking fleeting excitement for others to give money",
                                4: "trying to fill the emptiness in his heart",
                                5: "trying to succumb to a life of crime",
                                6: "desperately attempting to rob the central bank, a futile and dangerous endeavor"
                            }

                            happy_slays = await self.count_happiness_above_threshold(conn, interaction.user)

                            index_l = 0
                            slay_fund = randint(50000000, 325000000 * happy_slays)
                            total_fund = 0 + slay_fund
                            disproportionate_share = 0
                            dissatisfaction = 100 - randint(20, 67)
                            await self.change_slay_field(conn, interaction.user, "status", 1)
                            await self.change_slay_field(conn, interaction.user, "happiness", dissatisfaction)
                            summ = discord.Embed(colour=discord.Colour.from_rgb(66, 164, 155))
                            for slay in slays:
                                tname = slay[0]
                                happiness = slay[-2]
                                if happiness > 30:
                                    doing_what = labour_actions.get(index_l)
                                    disproportionate_share = randint(20000000, slay_fund-disproportionate_share)
                                    bonus = round((1.2 / 100) * disproportionate_share) + disproportionate_share
                                    total_fund += bonus

                                    content.add(f'- {tname} was {doing_what} and got a total '
                                                f'of **\U000023e3 {disproportionate_share:,}**\n'
                                                f' - Bonus: **\U000023e3 {bonus:,}**')
                                else:
                                    doing_what = sad_actions.get(index_l)
                                    loss = (happiness/100)*disproportionate_share
                                    disproportionate_share = randint(2000, abs(slay_fund - disproportionate_share))
                                    content.add(f'- {tname} was {doing_what} and got a total '
                                                f'of **\U000023e3 {loss:,}**\n'
                                                f' - Bonus: **\U000023e3 {bonus:,}**')
                                    def d():
                                        pass
                                    summ.add_field(name='You have an unhappy slay.',
                                                   value='Paying too little attention to your slay\'s needs will result'
                                                         ' in your slay running away.',
                                                   inline=False) if summ.fields == 0 else d()
                                index_l += 1

                            await self.modify_happiness(conn, interaction.user)
                            net_returns = await self.update_bank_new(interaction.user, conn, total_fund)
                            avatar = interaction.user.display_avatar or interaction.user.default_avatar
                            summ.set_footer(icon_url=avatar.url, text=f"For {interaction.user.name}")
                            summ.description = (f"## <a:2635serversubscriptionsanimated:1174417911344013523> Paycheck\n"
                                                f"> Your slays have made **\U000023e3 {slay_fund:,}**.\n"
                                                f"> Your new `wallet` balance now is **\U000023e3 {net_returns[0]:,}**."
                                                f"\n\nHere is a summary:\n"
                                                f"{'\n'.join(content)}\n")

                            return await interaction.followup.send(embed=summ)
                        else:
                            minutes, seconds = divmod(diff.total_seconds(), 60)
                            hours, minutes = divmod(minutes, 60)
                            days, hours = divmod(hours, 24)
                            await interaction.followup.send(f"Your slays are still working.\n"
                                                            f"They will finish working in **{int(days)}** days, "
                                                            f"**{int(hours)}** hours, **{int(minutes)}** minutes "
                                                            f"and **{int(seconds)}** seconds. ")
                else:
                    return await interaction.followup.send("## No data has been found under your name.\n"
                                                           "- This is because you've registered after the "
                                                           "cooldown system was implemented.\n"
                                                           "- A quick fix is to use the /discontinue command "
                                                           "and re-register (you can request a developer to "
                                                           "add your original items back).")
        except ValueError as veer:
            await interaction.followup.send(f"{veer}")

    @commands.command(name='reasons', description='reasons why the user not registered error is caused.')
    @commands.cooldown(1, 6)
    async def not_registered_why(self, ctx: commands.Context):
        async with ctx.typing():
            embed = discord.Embed(title="Not registered? But why?",
                                  description='This list is not exhaustive, all known causes will be displayed:\n'
                                              f'- You were removed by the c2c developers.\n'
                                              f'- You opted out of the system yourself.\n'
                                              f'- The database is currently under construction.\n'
                                              f'- The database malfunctioned due to a undelivered transaction.\n'
                                              f'- You called a command that is using an outdated database.\n'
                                              f'- The database unexpectedly closed (likely due to maintenance).\n'
                                              f'- The developers are modifying the database contents.\n'
                                              f'- The database is closed and a connection has not been yet.\n'
                                              f'- The command hasn\'t acquired a pool connection (devs know why).\n\n'
                                              f'Found an unusual bug on a command? **Report it now to prevent further '
                                              f'issues.**', colour=0x2F3136)
        await ctx.send(embed=embed)

    @app_commands.command(name="use", description="use an item you own from your inventory.")
    @app_commands.guilds(discord.Object(id=829053898333225010), discord.Object(id=780397076273954886))
    @app_commands.describe(item='the name of the item to use')
    @app_commands.checks.dynamic_cooldown(owners_nolimit)
    async def use_item(self, interaction: discord.Interaction,
                       item: Literal['Keycard', 'Trophy', 'Clan License', 'Resistor', 'Amulet', 'Dynamic Item', 'Hyperion', 'Crisis', 'Odd Eye']):

        async with self.client.pool_connection.acquire() as conn: # type: ignore
            conn: asqlite_Connection
            if await self.can_call_out(interaction.user,conn):
                return await interaction.response.send_message(embed=self.not_registered) # type: ignore

            item = item.replace(" ", "_")
            quantity = await self.get_one_inv_data_new(interaction.user, item, conn)

            if quantity < 1:
                return await interaction.response.send_message( # type: ignore
                    embed=membed(f"You don't have this item in your inventory."))

            unavailable = discord.Embed(title='We need your feedback!',
                                        colour=0x2F3136)
            unavailable.description = (
                "We have created multiple items in this release of c2c, but we have no idea what uses they should have."
                " Therefore, you must submit your ideas and suggestions for what this item should implement through "
                "the </feedback:1179817617767268353>.\n\n"
                "- Set the title of your feedback as the name of the item that you want to create a use for.\n"
                "- Briefly describe in the description header what you would like to see for that item you've chosen.\n"
                "- Your ideas will be sent to the developers and from there, it will (usually) be immediately accepted."
                "\n\nIt is not a requirement for you to submit ideas which are reflected in the bot, but you may do so "
                "if you would like to see the functionality for these items earlier on instead of years later "
                "when we figure out!"
            )
            match item:
                case 'Keycard':  # if items are collectibles, put in this branch
                    return await interaction.response.send_message(  # type: ignore
                        embed=membed("This item is a collectible and cannot be used.")
                    )
                case 'Trophy':
                    if quantity > 1:
                        content = f'\nThey have **{quantity}** of them, WHAT A BADASS'
                    else:
                        content = ''
                    return await interaction.response.send_message( # type: ignore
                        f"{interaction.user.name} is flexing on you all with their <:tr1:1165936712468418591> **~~PEPE~~ TROPHY**{content}")
                case _:
                    return await interaction.response.send_message( # type: ignore
                        embed=unavailable
                    )

    @app_commands.command(name='tester', description='test slash command.')
    @app_commands.guilds(discord.Object(id=829053898333225010), discord.Object(id=780397076273954886))
    async def test_sla_cmd(self, interaction: discord.Interaction):
        view = ConfirmDeny(interaction)
        await interaction.response.send_message("Do you confirm the changes?", view=view) # type: ignore
        view.msg = await interaction.original_response()

    @app_commands.command(name="getjob", description="earn a salary becoming employed.")
    @app_commands.guilds(discord.Object(id=829053898333225010), discord.Object(id=780397076273954886))
    @app_commands.describe(job_name='the name of the job')
    @app_commands.checks.dynamic_cooldown(owners_nolimit)
    async def get_job(self, interaction: discord.Interaction,
                      job_name: Literal['Plumber', 'Cashier', 'Fisher', 'Janitor', 'Youtuber', 'Police']):

        async with self.client.pool_connection.acquire() as conn: # type: ignore
            conn: asqlite_Connection
            if await self.can_call_out(interaction.user, conn):
                return await interaction.response.send_message(embed=self.not_registered) # type: ignore

            await self.change_job_new(interaction.user, conn, job_name=job_name)
            recruited = membed(f"Success! You are now a **{job_name}**.")
            await interaction.response.send_message(embed=recruited) # type: ignore

    @app_commands.command(name='profile', description='view information about a user and their stats.')
    @app_commands.guilds(discord.Object(id=829053898333225010), discord.Object(id=780397076273954886))
    @app_commands.describe(user='the profile of the user to find')
    @app_commands.checks.dynamic_cooldown(owners_nolimit)
    async def find_profile(self, interaction: discord.Interaction, user: Optional[discord.Member]):
        if user is None:
            user = interaction.user

        if (get_profile_key_value(f"{user.id} vis") == "private") and (interaction.user.id != user.id):
            embed = discord.Embed(
                colour=0x2F3136,
                description=f"# <:security:1153754206143000596> {user.name}'s profile is protected.\n"
                            f"- Only approved users can view {user.name}'s profile.")
            return await interaction.response.send_message(embed=embed) # type: ignore

        main_id = str(user.id)
        tatsu = await self.fetch_tatsu_profile(int(main_id))

        async with self.client.pool_connection.acquire() as conn: # type: ignore

            if await self.can_call_out(user, conn):
                return await interaction.response.send_message(embed=NOT_REGISTERED) # type: ignore

            users = await conn.execute(f"SELECT * FROM `bank` WHERE userID = ?", (user.id,))
            user_data = await users.fetchone()
            their_prest = user_data[-1]
            pr_no = their_prest + 1 if user.id == 546086191414509599 else their_prest
            corresp_preste = PRESTIGE_EMOTES.setdefault(pr_no, "")
            their_avatar = user.display_avatar or user.default_avatar
            their_badges = get_profile_key_value(f"{main_id} badges") or "No badges acquired yet"

            procfile = discord.Embed(colour=user.colour, timestamp=discord.utils.utcnow())
            inv = 0
            unique = 0
            total = 0

            for item in SHOP_ITEMS:
                name = item["name"]
                cost = item["cost"]
                data = await self.get_one_inv_data_new(user, name, conn)
                inv += int(cost) * data
                total += data
                unique += 1 if data else 0

            if main_id == "992152414566232139":
                procfile.set_image(
                    url="https://media.discordapp.net/attachments/1124672402413072446/1164912661004292136/20231010000451.png?ex=6544f075&is=65327b75&hm=dfef49bfcab2ca0f8f2d50db7733c5e3ba6cf691f5350ddf8fb8350fc2bb38d8&=&width=1246&height=701")

            match user.id:
                case 546086191414509599 | 992152414566232139:
                    note = ("> <:cprofile:1174417914183561287> *This user's custom profile contains "
                            "additional perks that will not be publicized.*\n\n")
                case _:
                    note = ""

            procfile.description = (f"### {user.name}'s Profile - [{tatsu.title or 'No title set'}](https://www.google.com)\n"
                                    f"{note}"
                                    f"{corresp_preste} Prestige Level **{their_prest}**\n"
                                    f"Bounty: \U000023e3 **{user_data[-2]:,}**\n"
                                    f"{their_badges}")

            procfile.add_field(name='Robux',
                               value=f"Wallet: `\U000023e3 {format_number_short(user_data[1])}`\n"
                                     f"Bank: `\U000023e3 {format_number_short(user_data[2])}`\n"
                                     f"Net: `\U000023e3 {format_number_short(user_data[1]+user_data[2])}`")

            procfile.add_field(name='Items',
                               value=f"Unique: `{unique:,}`\n"
                                     f"Total: `{format_number_short(total)}`\n"
                                     f"Worth: `\U000023e3 {format_number_short(inv)}`")

            procfile.add_field(name='Tatsu',
                               value=f"Credits: `{format_number_short(tatsu.credits)}`\n"
                                     f"Tokens: `{format_number_short(tatsu.tokens)}`\n"
                                     f"XP: `{format_number_short(tatsu.xp)}`")

            if get_profile_key_value(f"{main_id} bio") is not None:
                procfile.add_field(name='Bio', value=f'{get_profile_key_value(f"{main_id} bio")}', inline=False)
            if get_profile_key_value(f"{main_id} avatar_url") is None:  # if user has a custom avatar url
                procfile.set_thumbnail(url=their_avatar.url)
            else:  # if the user does not have a custom avatar url set
                try:  # try to set the custom url as the embed thumbnail
                    procfile.set_thumbnail(url=get_profile_key_value(f"{main_id} avatar_url"))
                except discord.HTTPException:  # use default avatar if doesn't work
                    procfile.set_thumbnail(url=their_avatar.url)
            return await interaction.response.send_message(embed=procfile, silent=True) # type: ignore

    @app_commands.command(name='highlow', description='Guess if a number is high, low, or jackpot!')
    @app_commands.guilds(discord.Object(id=829053898333225010), discord.Object(id=780397076273954886))
    @app_commands.checks.dynamic_cooldown(owners_nolimit)
    @app_commands.describe(robux='an integer to bet upon. Supports Shortcuts (max, all, exponents).')
    async def highlow(self, interaction: discord.Interaction, robux: str):

        def is_valid(value: int, user_balance: int) -> bool:
            """A check that defines that the amount a user inputs is valid for their account. Meets preconditions for highlow.
            :param value: amount to check,
            :param user_balance: the user's balance currenctly, which should be an integer.
            :return: A boolean indicating whether the amount is valid for the function to proceed."""
            if value <= 0:
                return False
            elif value > 50000000:
                return False
            elif value < 100000:
                return False
            elif value > user_balance:
                return False
            else:
                return True

        conn = await self.client.pool_connection.acquire() # type: ignore
        number = randint(1, 100)
        hint = f"Your hint is {abs(randint(number - randint(1, 30), number + randint(1, 15)))}"
        try:
            if await self.can_call_out(interaction.user, conn):
                return await interaction.response.send_message(embed=self.not_registered) # type: ignore

            real_amount = determine_exponent(robux)
            wallet_amt = await self.get_wallet_data_only(interaction.user, conn)
            try:
                assert isinstance(real_amount, str)
                if real_amount.lower() == 'max' or real_amount.lower() == 'all':
                    if 50000000 > wallet_amt:
                        real_amount = wallet_amt
                    else:
                        real_amount = 50000000
            except AssertionError:
                pass
            if not (is_valid(int(real_amount), wallet_amt)):
                return await interaction.response.send_message(embed=ERR_UNREASON) # type: ignore
            extraneous_data.clear()
            extraneous_data.append(number)
            extraneous_data.append(real_amount)

        finally:
            await self.client.pool_connection.release(conn) # type: ignore
            await interaction.response.send_message(f"I am thinking of a number. Guess what it is. **{hint}!**", # type: ignore
                                                    view=HighLow(interaction, self.client))

    @app_commands.command(name='slots',
                          description='take your chances and gamble on a slot machine.')
    @app_commands.guilds(discord.Object(id=829053898333225010), discord.Object(id=780397076273954886))
    @app_commands.rename(keyword='robux')
    @app_commands.checks.dynamic_cooldown(owners_nolimit)
    @app_commands.describe(keyword='an integer to bet upon. Supports Shortcuts (max, all, exponents).')
    async def slots(self, interaction: discord.Interaction, keyword: str):

        async with self.client.pool_connection.acquire() as conn: # type: ignore
            conn: asqlite_Connection
            if await self.can_call_out(interaction.user, conn):
                await interaction.response.send_message(embed=self.not_registered) # type: ignore

        # --------------- Checks before betting i.e. has keycard, meets bet constraints. -------------
        data = await self.get_one_inv_data_new(interaction.user, "Keycard", conn)  # no need to do data[0] here
        has_keycard = data and True
        expo = determine_exponent(keyword)
        try:
            assert isinstance(expo, int)
            amount = expo
        except AssertionError:
            if keyword.lower() in {'max', 'all'}:
                if has_keycard:
                    amount = 75000000
                else:
                    amount = 50000000
            else:
                return await interaction.response.send_message(embed=ERR_UNREASON) # type: ignore

        # --------------- Contains checks before betting i.e. has keycard, meets bet constraints. -------------
        wallet_amt = await self.get_wallet_data_only(interaction.user, conn)
        if has_keycard:
            # if the user has a keycard
            if (amount > 75000000) or (amount < 30000):
                err = discord.Embed(colour=0x2F3136, description=f'## You did not meet the slot machine criteria:\n'
                                                                 f'- You wanted to bet {CURRENCY}**{amount:,}**\n'
                                                                 f' - A minimum bet of {CURRENCY}**30,000** must '
                                                                 f'be made\n'
                                                                 f' - A maximum bet of {CURRENCY}**75,000,000** '
                                                                 f'can only be made.')
                return await interaction.response.send_message(embed=err) # type: ignore
            elif amount > wallet_amt:
                err = discord.Embed(colour=0x2F3136, description=f'Cannot perform this action, '
                                                                 f'you only have {CURRENCY}**{wallet_amt:,}**\n'
                                                                 f'You\'ll need {CURRENCY}**{amount - wallet_amt:,}**'
                                                                 f' more in your wallet first.')
                return await interaction.response.send_message(embed=err) # type: ignore
        else:
            if (amount > 50000000) or (amount < 50000):
                err = discord.Embed(colour=0x2F3136, description=f'## You did not meet the slot machine criteria:\n'
                                                                 f'- You wanted to bet {CURRENCY}**{amount:,}**\n'
                                                                 f' - A minimum bet of {CURRENCY}**50,000** must '
                                                                 f'be made.\n'
                                                                 f' - A maximum bet of {CURRENCY}**50,000,000** '
                                                                 f'can only be made.')
                return await interaction.response.send_message(embed=err) # type: ignore
            elif amount > wallet_amt:
                err = discord.Embed(colour=0x2F3136, description=f'Cannot perform this action, '
                                                                 f'you only have {CURRENCY}**{wallet_amt:,}**\n'
                                                                 f'You\'ll need {CURRENCY}**{amount - wallet_amt:,}**'
                                                                 f' more in your wallet first.')
                return await interaction.response.send_message(embed=err) # type: ignore

        # ------------------ THE SLOT MACHINE ITESELF ------------------------

        emoji_outcome = generate_slot_combination()  # this is a string
        freq1, freq2, freq3 = emoji_outcome[0], emoji_outcome[1], emoji_outcome[2]
        slot_stuff = await self.get_bank_data_new(interaction.user, conn)
        id_won_amount, id_lose_amount = slot_stuff[3], slot_stuff[4]
        avatar = interaction.user.display_avatar or interaction.user.default_avatar

        if emoji_outcome.count(freq1) > 1:  # WINNING SLOT MACHINE
            # most_frequent_emoji_outcome = freq1

            emulti = BONUS_MULTIPLIERS[f'{freq1 * emoji_outcome.count(freq1)}']
            serv_multi = SERVER_MULTIPLIERS.setdefault(interaction.guild.id, 0)  # Get server multiplier
            new_multi = serv_multi + emulti  # Server multiplier PLUS slot machine multiplier
            amount_after_multi = floor(((new_multi / 100) * amount) + amount)  # New amount AFTER all multipliers
            tma = amount_after_multi - amount  # The multiplier amount
            new_amount_balance = await self.update_bank_new(interaction.user, conn, amount_after_multi)
            new_id_won_amount = await self.update_bank_new(interaction.user, conn, 1, "slotw")
            new_total = id_lose_amount + new_id_won_amount[0]

            prcntw = round((new_id_won_amount[0] / new_total) * 100, 1)
            embed = discord.Embed(description=f"## {interaction.user.mention}'s winning slot machine\n"
                                              f"**\U0000003e** {emoji_outcome[0]} {emoji_outcome[1]} {emoji_outcome[2]} **\U0000003c**\n\n"
                                              f"\U0000279c You won {CURRENCY}**{amount_after_multi:,}** robux.\n"
                                              f"\U0000279c Bonus: {PREMIUM_CURRENCY} **{tma:,}** via a `{new_multi}x` multiplier.\n"
                                              f"<:linkit:1176970030961930281> **{serv_multi}**% Server Multiplier, **{emulti}**% via slots.\n"
                                              f"\U0000279c Your new `wallet` balance is {CURRENCY}"
                                              f"**{new_amount_balance[0]:,}**.",
                                  colour=discord.Color.brand_green())
            embed.set_footer(text=f"You've won {prcntw}% of all slots games. ({new_id_won_amount[0]:,}/{new_total:,})",
                             icon_url=avatar.url)
            await interaction.response.send_message(embed=embed) # type: ignore

        elif emoji_outcome.count(freq2) > 1:  # STILL A WINNING SLOT MACHINE

            emulti = BONUS_MULTIPLIERS[f'{freq2 * emoji_outcome.count(freq2)}']

            serv_multi = SERVER_MULTIPLIERS.setdefault(interaction.guild.id, 0)  # Get server multiplier
            new_multi = serv_multi + emulti  # Server multiplier PLUS slot machine multiplier
            amount_after_multi = floor(((new_multi / 100) * amount) + amount)  # New amount AFTER all multipliers
            tma = amount_after_multi - amount  # The multiplier amount
            new_amount_balance = await self.update_bank_new(interaction.user, conn, amount_after_multi)
            new_id_won_amount = await self.update_bank_new(interaction.user, conn, 1, "slotw")
            new_total = id_lose_amount + new_id_won_amount[0]
            prcntw = round((new_id_won_amount[0] / new_total) * 100, 1)

            embed = discord.Embed(description=f"## {interaction.user.mention}'s winning slot machine\n"
                                              f"**\U0000003e** {emoji_outcome[0]} {emoji_outcome[1]} {emoji_outcome[2]} **\U0000003c**\n\n"
                                              f"\U0000279c You won {CURRENCY}**{amount_after_multi:,}** robux.\n"
                                              f"\U0000279c Bonus: {PREMIUM_CURRENCY} **{tma:,}** via a `{new_multi}x` multiplier.\n"
                                              f"<:linkit:1176970030961930281> **{serv_multi}**% Server Multiplier, **{emulti}**% via slots.\n"
                                              f"\U0000279c Your new `wallet` balance is {CURRENCY}"
                                              f"**{new_amount_balance[0]:,}**.",
                                  colour=discord.Color.brand_green())
            embed.set_footer(text=f"You've won {prcntw}% of all slot games. ({new_id_won_amount[0]:,}/{new_total:,})",
                             icon_url=avatar.url)
            await interaction.response.send_message(embed=embed) # type: ignore

        else:  # A LOSING SLOT MACHINE

            new_amount_balance = await self.update_bank_new(interaction.user, conn, -amount)
            new_id_lose_amount = await self.update_bank_new(interaction.user, conn, 1, "slotl")
            new_total = new_id_lose_amount[0] + id_won_amount

            prcntl = round((new_id_lose_amount[0] / new_total) * 100, 1)

            embed = discord.Embed(description=f"## {interaction.user.mention}'s losing slot machine\n"
                                              f"**\U0000003e** {emoji_outcome[0]} {emoji_outcome[1]} {emoji_outcome[2]} **\U0000003c**\n\n"
                                              f"\U0000279c You lost {CURRENCY}**{amount:,}** robux \n"
                                              f"\U0000279c No multiplier accrued due to a lost bet.\n"
                                              f"\U0000279c Your new `wallet` balance is {CURRENCY}"
                                              f"**{new_amount_balance[0]:,}**.",
                                  colour=discord.Color.brand_red())
            embed.set_footer(text=f"You've lost {prcntl}% of all slots games. ({new_id_lose_amount[0]:,}/{new_total:,})",
                             icon_url=avatar.url)
            await interaction.response.send_message(embed=embed) # type: ignore

    @app_commands.command(name='inventory', description='view your currently owned items.')
    @app_commands.guilds(discord.Object(id=829053898333225010), discord.Object(id=780397076273954886))
    @app_commands.describe(member='the member to view the inventory of:')
    async def inventory(self, interaction: discord.Interaction, member: Optional[discord.Member]):
        user = member or interaction.user

        if user.bot and user.id != self.client.user.id:
            return await interaction.response.send_message(embed=membed("Bots do not have accounts."), delete_after=5.0) # type: ignore

        async with self.client.pool_connection.acquire() as conn: # type: ignore

            conn: asqlite_Connection
            em = discord.Embed(color=0x2F3136)
            await self.open_inv_new(user, conn)
            length = 5
            value, svalue = 0, 0
            total_items = 0
            owned_items = []

            for item in SHOP_ITEMS:
                name = item["name"]
                qualified_name = " ".join(name.split("_"))
                cost = item["cost"]
                item_id = item["id"]
                item_emoji = item["emoji"]
                item_type = item["rarity"]
                data = await self.update_inv_new(user, 0, name, conn)
                if data[0] >= 1:
                    value += int(cost) * data[0]
                    svalue += int(cost / 4) * data[0]
                    total_items += data[0]
                    owned_items.append(
                        f"{item_emoji} **{qualified_name}** ({data[0]} owned)\nID: **`{item_id}`**\nItem Type: {item_type}")

            user_av = user.display_avatar or user.default_avatar

            if len(owned_items) == 0:
                em.set_author(name=f"{user.name}'s Inventory", icon_url=user_av.url)
                em.description = (f"{user.name} currently has **no items** in their inventory.\n"
                                  f"**Net Value:** <:robux:1146394968882151434> 0\n"
                                  f"**Sell Value:** <:robux:1146394968882151434> 0")

                em.add_field(
                    name=f"Nothingness.", value=f"No items were found from this user.", inline=False)
                return await interaction.response.send_message(embed=em) # type: ignore

            async def get_page_part(page: int):

                em.set_author(name=f"{user.name}'s Inventory", icon_url=user_av.url)

                offset = (page - 1) * length

                em.description = (f"{user.name} currently has **`{total_items}`** item(s) in their inventory.\n"
                                  f"**Net Value:** <:robux:1146394968882151434> {value:,}\n"
                                  f"**Sell Value:** <:robux:1146394968882151434> {svalue:,}\n\n")

                for itemm in owned_items[offset:offset + length]:

                    em.description += f"{itemm}\n\n"

                n = Pagination.compute_total_pages(len(owned_items), length)

                em.set_footer(text=f"Owned Items \U00002500 Page {page} of {n}")
                return em, n

            await Pagination(interaction, get_page_part).navigate()

    @app_commands.command(name='buy', description='make a purchase from the shop.')
    @app_commands.guilds(discord.Object(id=829053898333225010), discord.Object(id=780397076273954886))
    @app_commands.describe(item_name='the name of the item you want to buy.',
                           quantity='the quantity of the item(s) you wish to buy')
    async def buy(self, interaction: discord.Interaction,
                  item_name: Literal['Keycard', 'Trophy', 'Clan License', 'Resistor', 'Amulet', 'Dynamic Item', 'Hyperion', 'Crisis', 'Odd Eye'],
                  quantity: Optional[Literal[1, 2, 3, 4, 5]]):

        if quantity is None:
            quantity = 1

        async with self.client.pool_connection.acquire() as conn: # type: ignore
            conn: asqlite_Connection

            if await self.can_call_out(interaction.user, conn):
                return await interaction.response.send_message(embed=self.not_registered) # type: ignore

            wallet_amt = await self.get_wallet_data_only(interaction.user, conn)

            for item in SHOP_ITEMS:
                access_name = ' '.join(item["name"].split('_'))  # Dynamic_Item becomes Dynamic Item

                if item_name == access_name:
                    ie = item['emoji']
                    proper_name = item.setdefault('qn', None) or access_name
                    stock_item = get_stock(item_name)

                    if stock_item == 0:
                        return await interaction.response.send_message( # type: ignore
                            embed=membed(f"## Unsuccessful Transaction\n"
                                         f"- The {ie} **{item_name}** is currently out of stock.\n"
                                         f" - Until a user who owns this item chooses to "
                                         f"sell it, stocks cannot be refilled."))

                    if quantity > stock_item:
                        proper_name = " ".join(proper_name.split("_"))
                        proper_name = make_plural(proper_name, stock_item)
                        their_name = make_plural(proper_name, quantity)
                        return await interaction.response.send_message( # type: ignore
                            embed=membed(f"## Unsuccessful Transaction\n"
                                         f"There are only **{stock_item}** {ie} **{proper_name.title()}** available.\n"
                                         f"{ARROW}Meaning you cannot possibly buy **{quantity}** {their_name.title()}."))

                    await self.open_inv_new(interaction.user, conn)
                    total_cost = int((item["cost"] * int(quantity)))

                    if wallet_amt < int(total_cost):
                        proper_name = " ".join(proper_name.split("_"))
                        proper_name = make_plural(proper_name, quantity)
                        return await interaction.response.send_message( # type: ignore
                            embed=membed(f"## Unsuccessful Transaction\n"
                                         f"You'll need {CURRENCY} **{total_cost - wallet_amt:,}** more to "
                                         f"purchase {quantity} {ie} **{proper_name.title()}**."))

                    await self.update_inv_new(interaction.user, +int(quantity), item["name"], conn)
                    await self.update_bank_new(interaction.user, conn, -total_cost)
                    modify_stock(item_name, "-", quantity)

                    match quantity:
                        case 1:
                            return await interaction.response.send_message( # type: ignore
                                embed=membed(f"## Success\n"
                                             f"- Purchased **1** {ie} **{item_name}** by paying "
                                             f"{CURRENCY} **{total_cost:,}**.\n"
                                             f" - The items requested have been added to your inventory."))
                        case _:
                            their_name = ' '.join(proper_name.split("_"))
                            their_name = make_plural(their_name, quantity)
                            await interaction.response.send_message( # type: ignore
                                embed=membed(f"## Success\n"
                                             f"- Purchased **{quantity}** {ie} **{their_name.title()}** by"
                                             f" paying {CURRENCY} **{total_cost:,}**.\n"
                                             f" - The items requested have been added to your inventory."))

    @app_commands.command(name='sell', description='sell an item from your inventory.')
    @app_commands.guilds(discord.Object(id=829053898333225010), discord.Object(id=780397076273954886))
    @app_commands.describe(item_name='the name of the item you want to sell.',
                           sell_quantity='the quantity you wish to sell. defaults to 1.')
    async def sell(self, interaction: discord.Interaction,
                   item_name: Literal['Keycard', 'Trophy', 'Clan License', 'Resistor', 'Amulet', 'Dynamic Item', 'Hyperion', 'Crisis', 'Odd Eye'],
                   sell_quantity: Optional[Literal[1, 2, 3, 4, 5]]):

        if sell_quantity is None:
            sell_quantity = 1
        name = item_name.replace(" ", "_")
        async with self.client.pool_connection.acquire() as conn: # type: ignore
            conn: asqlite_Connection

            if await self.can_call_out(interaction.user, conn):
                return await interaction.response.send_message(embed=self.not_registered) # type: ignore

            for item in SHOP_ITEMS:
                if name == item["name"]:
                    ie = item['emoji']
                    cost = int(round((item["cost"] / 4) * sell_quantity, ndigits=None))
                    quantity = await self.update_inv_new(interaction.user, 0, item["name"], conn)

                    if quantity[0] < 1:
                        return await interaction.response.send_message( # type: ignore
                            embed=membed(f"You don't have a {ie} **{item_name}** in your inventory."))

                    new_quantity = quantity[0] - sell_quantity
                    if new_quantity < 0:
                        return await interaction.response.send_message( # type: ignore
                            f"You are requesting to sell more than what you currently own. Not possible.")

                    await self.change_inv_new(interaction.user, new_quantity, item["name"], conn)
                    modify_stock(item_name, "+", sell_quantity)
                    await self.update_bank_new(interaction.user, conn, +cost)

                    match sell_quantity:
                        case 1:
                            proper_name = item.setdefault('qn', None) or name
                            proper_name = ' '.join(proper_name.split('_'))
                            return await interaction.response.send_message( # type: ignore
                                embed=membed(f"You just sold 1 {ie} **{proper_name.title()}** and got "
                                             f"<:robux:1146394968882151434> **{cost:,}** in return."))
                        case _:
                            proper_name = item.setdefault('qn', None) or name
                            proper_name = ' '.join(proper_name.split('_'))
                            proper_name = make_plural(proper_name, sell_quantity)
                            return await interaction.response.send_message( # type: ignore
                                embed=membed(f"You just sold {sell_quantity} {ie} **{proper_name.title()}** and got "
                                             f"<:robux:1146394968882151434> **{cost:,}** in return."))

    @app_commands.command(name="work", description="work and earn an income, if you have a job.")
    @app_commands.guilds(discord.Object(id=829053898333225010), discord.Object(id=780397076273954886))
    async def work(self, interaction: discord.Interaction):

        await interaction.response.defer(thinking=True, ephemeral=True) # type: ignore

        words = {
            "Plumber": [("TOILET", "SINK", "SEWAGE", "SANITATION", "DRAINAGE", "PIPES"), 400000000],
            "Cashier": [("ROBUX", "TILL", "ITEMS", "WORKER", "REGISTER", "CHECKOUT", "TRANSACTIONS", "RECEIPTS"),
                        500000000],
            "Fisher": [("FISHING", "NETS", "TRAWLING", "FISHERMAN", "CATCH", "VESSEL", "AQUATIC", "HARVESTING", "MARINE"),
                       550000000],
            "Janitor": [("CLEANING", "SWEEPING", "MOPING", "CUSTODIAL", "MAINTENANCE", "SANITATION", "BROOM", "VACUUMING"),
                        650000000],
            "Youtuber": [("CONTENT CREATION", "VIDEO PRODUCTION", "CHANNEL", "SUBSCRIBERS", "EDITING", "UPLOAD",
                         "VLOGGING", "MONETIZATION", "THUMBNAILS", "ENGAGEMENT"), 1000000000],
            "Police": [("LAW ENFORCEMENT", "PATROL", "CRIME PREVENTION", "INVESTIGATION", "ARREST", "UNIFORM", "BADGE",
                       "INTERROGATION"), 1200000000]
        }

        async with self.client.pool_connection.acquire() as conn: # type: ignore
            conn: asqlite_Connection

            if await self.can_call_out(interaction.user, conn):
                return await interaction.followup.send(embed=self.not_registered)

            resp = {"0": "None", 0: "None"}
            job_description = await self.get_job_data_only(user=interaction.user,
                                                           conn_input=conn)  # Ensure consistency, save to job dictionary
            job_val = resp.setdefault(job_description[0], job_description[0])

            if job_val == "None":
                return await interaction.followup.send(embed=membed("You don't have a job, get one first."))

            possible_words: tuple = words.get(job_val)[0]
            # Pick a random word from possible_words
            selected_word = choice(possible_words)

            # Determine the number of letters to hide (excluding spaces)
            letters_to_hide = max(1, len(selected_word) // 3)  # You can adjust this ratio

            # Get the indices of letters to hide (excluding spaces)
            indices_to_hide = [i for i, char in enumerate(selected_word) if char.isalpha()]
            indices_hidden = sample(indices_to_hide, min(letters_to_hide, len(indices_to_hide)))

            # Replace selected letters with '_'
            hidden_word_list = [char if i not in indices_hidden else '_' for i, char in enumerate(selected_word)]
            hidden_word = ''.join(hidden_word_list)

            # Display the hidden word to the user

            def check(m):
                return m.content.lower() == selected_word.lower() and m.channel == interaction.channel and m.author == interaction.user

            await interaction.followup.send(
                f"What is the word?\nReplace the blanks \U0000279c [`{hidden_word}`](https://www.sss.com)")

            my_msg = await interaction.channel.send("Waiting for correct input..")

            try:
                await self.client.wait_for('message', check=check, timeout=15.0)
            except asyncTE:
                await interaction.followup.send(f"`BOSS`: Too slow, you get nothing for the attitude. I expect better "
                                                f"of you next time.")
            else:
                salary = words.get(job_val)[-1]
                rangeit = randint(10000000, salary)
                await self.update_bank_new(interaction.user, conn, rangeit, "bank")
                await my_msg.edit(content=f"*BOSS*: Good work from you, got the "
                                          f"job done. You got **\U000023e3 {rangeit:,}** for your efforts. The "
                                          f"money has been sent to your bank account.")

    @app_commands.command(name="balance", description="returns a user's current balance.")
    @app_commands.guilds(discord.Object(id=829053898333225010), discord.Object(id=780397076273954886))
    @app_commands.describe(user='the user to return the balance of')
    @app_commands.checks.dynamic_cooldown(owners_nolimit)
    async def find_balance(self, interaction: discord.Interaction, user: Optional[discord.Member]):
        """Returns a user's balance."""

        await interaction.response.defer(thinking=True) # type: ignore

        if user is None:
            user = interaction.user

        async with self.client.pool_connection.acquire() as conn: # type: ignore
            conn: asqlite_Connection

            if await self.can_call_out(user, conn) and (user.id != interaction.user.id):
                return await interaction.followup.send(embed=membed(f"{user.name} isn't registered."))

            elif await self.can_call_out(user, conn) and (user.id == interaction.user.id):

                await self.open_bank_new(user, conn)
                await self.open_inv_new(user, conn)
                await self.open_cooldowns(user, conn)
                norer = membed(f"# <:successful:1183089889269530764> You are now registered.\n"
                                f"Your records have been added in our database, **{user.name}**.\n"
                                f"From now on, you may use any of the economy commands.\n"
                                f"Here are some of our top used commands:\n"
                                f"### 1. Start earning quick robux:\n"
                                f" - </bet:1172898644622585883>, "
                                f"</coinflip:1172898644622585882> </slots:1172898644287029332>, "
                                f"</step:1172898643884380166>, </highlow:1172898644287029331>\n"
                                f"### 2. Seek out employment:\n "
                                f" - </getjob:1172898643884380168>, </work:1172898644287029336>\n"
                                f"### 3. Customize your look:\n"
                                f" - </editprofile bio:1172898645532749948>, "
                                f"</editprofile avatar:1172898645532749948>\n"
                                f"### 4. Manage your Account:\n"
                                f" - </balance:1172898644287029337>, "
                                f"</withdraw:1172898644622585876>, </deposit:1172898644622585877>, "
                                f"</inventory:1172898644287029333>, </shop view:1172898645532749946>, "
                                f"</buy:1172898644287029334>")
                return await interaction.followup.send(embed=norer)
            else:
                av = user.display_avatar or user.default_avatar
                new_data = await self.get_bank_data_new(user, conn)
                bank = new_data[1] + new_data[2]
                inv = 0
                for item in SHOP_ITEMS:
                    name = item["name"]
                    cost = item["cost"]
                    data = await self.get_one_inv_data_new(user, name, conn)
                    inv += int(cost) * data

                resp = {"0": "None", 0: "None"}
                job_description = await self.get_job_data_only(user=user, conn_input=conn)  # Ensure consistency, save to job dictionary
                job_val = resp.setdefault(job_description[0], job_description[0])

                balance = discord.Embed(color=0x2F3136, timestamp=discord.utils.utcnow())
                balance.set_author(name=f"{user.name}'s balance", icon_url=av.url)

                balance.add_field(name="Wallet", value=f"\U000023e3 {new_data[1]:,}", inline=True)
                balance.add_field(name="Bank", value=f"\U000023e3 {new_data[2]:,}", inline=True)
                balance.add_field(name="Job", value=f"{job_val}", inline=True)
                balance.add_field(name="Bank Net", value=f"\U000023e3 {bank:,}", inline=True)
                balance.add_field(name="Inventory Net", value=f"\U000023e3 {inv:,}", inline=True)
                balance.add_field(name="Total Net", value=f"\U000023e3 {inv+bank:,}", inline=True)

                if user.id in {992152414566232139, 546086191414509599}:
                    balance.set_footer(icon_url='https://cdn.discordapp.com/emojis/1174417902980583435.webp?size=128&'
                                                'quality=lossless',
                                       text='mallow is dazzled')

                await interaction.followup.send(embed=balance)

    @app_commands.command(name="discontinue", description="opt out of the virtual economy system.")
    @app_commands.guilds(discord.Object(id=829053898333225010), discord.Object(id=780397076273954886))
    @app_commands.describe(member='the user to remove all of the data of')
    async def reset_user(self, interaction: discord.Interaction, member: Optional[discord.Member]):
        their_name = member or interaction.user
        if interaction.user.id not in {992152414566232139, 546086191414509599}:  # if author is not geo or splint
            if member is not None:  # if member content was written
                return await interaction.response.send_message(embed=ERR_UNREASON) # type: ignore
        else:  # if author is geo or splint
            if their_name.bot:
                return await interaction.response.send_message(embed=ERR_UNREASON) # type: ignore

        if member is None:
            member = interaction.user

        async with self.client.pool_connection.acquire() as conn: # type: ignore
            conn: asqlite_Connection
            data = await self.get_bank_data_new(member, conn)
            if data is None:
                await interaction.response.send_message( # type: ignore
                    embed=membed(f"Cannot perform this action, {member.name} is not on our database."))
            else:
                tables_to_delete = [BANK_TABLE_NAME, INV_TABLE_NAME, COOLDOWN_TABLE_NAME, SLAY_TABLE_NAME]

                # Execute DELETE queries using a loop
                for table in tables_to_delete:
                    await conn.execute(f"DELETE FROM `{table}` WHERE userID = ?", (member.id,))

                await conn.commit()
                embed = discord.Embed(colour=0x2F3136,
                                      description=f"## <:successful:1183089889269530764> {member.name}'s records have been wiped.\n"
                                                  f"- {member.name} can register again at any time"
                                                  f" if {member.name} checks their balance.")

                await interaction.response.send_message(embed=embed) # type: ignore

    @app_commands.command(name="withdraw", description="take out robux from your bank account.")
    @app_commands.guilds(discord.Object(id=829053898333225010), discord.Object(id=780397076273954886))
    @app_commands.describe(robux='the amount of robux to withdraw. Supports Shortcuts (max, all, exponents).')
    @app_commands.checks.dynamic_cooldown(owners_nolimit)
    async def withdraw(self, interaction: discord.Interaction, robux: str):

        user = interaction.user
        actual_amount = determine_exponent(robux)

        async with (self.client.pool_connection.acquire() as conn): # type: ignore
            conn: asqlite_Connection
            if await self.can_call_out(interaction.user, conn):
                await interaction.response.send_message(embed=self.not_registered) # type: ignore
            users = await self.get_bank_data_new(user, conn)

            bank_amt = users[2]
            if isinstance(actual_amount, str):
                if actual_amount.lower() == "all" or actual_amount.lower() == "max":
                    wallet_new = await self.update_bank_new(user, conn, +bank_amt)
                    bank_new = await self.update_bank_new(user, conn, -bank_amt, "bank")

                    embed = discord.Embed(colour=0x2F3136)


                    embed.add_field(name=f"Withdrawn", value=f"\U000023e3 {bank_amt:,}", inline=False)
                    embed.add_field(name=f"Current Wallet Balance", value=f"\U000023e3 {wallet_new[0]:,}")
                    embed.add_field(name=f"Current Bank Balance", value=f"\U000023e3 {bank_new[0]:,}")

                    return await interaction.response.send_message(embed=embed) # type: ignore
                return await interaction.response.send_message(embed=ERR_UNREASON) # type: ignore

            amount_conv = abs(int(actual_amount))
            if amount_conv < 5000:
                embed = discord.Embed(colour=0x2F3136,
                                      description=f"- For performance reasons, a minimum of "
                                                  f"\U000023e3 **5,000** must be withdrawn.\n"
                                                  f" - You wanted to withdraw \U000023e3 **{amount_conv:,}**.\n")
                return await interaction.response.send_message(embed=embed) # type: ignore

            elif amount_conv > bank_amt:
                embed = discord.Embed(colour=0x2F3136,
                                      description=f"- You do not have that much money in your bank.\n"
                                                  f" - You wanted to withdraw \U000023e3 **{amount_conv:,}**.\n"
                                                  f" - Currently, you only have \U000023e3 **{bank_amt:,}**.")
                return await interaction.response.send_message(embed=embed) # type: ignore

            else:
                wallet_new = await self.update_bank_new(user, conn, +amount_conv)
                bank_new = await self.update_bank_new(user, conn, -amount_conv, "bank")

                embed = discord.Embed(colour=0x2F3136)
                embed.add_field(name=f"Withdrawn", value=f"\U000023e3 {amount_conv:,}", inline=False)
                embed.add_field(name=f"Current Wallet Balance", value=f"\U000023e3 {wallet_new[0]:,}")
                embed.add_field(name=f"Current Bank Balance", value=f"\U000023e3 {bank_new[0]:,}")

                return await interaction.response.send_message(embed=embed) # type: ignore

    @app_commands.command(name='deposit', description="deposit robux to your bank account.")
    @app_commands.guilds(discord.Object(id=829053898333225010), discord.Object(id=780397076273954886))
    @app_commands.describe(robux='the amount of robux to deposit. Supports Shortcuts (max, all, exponents).')
    @app_commands.checks.dynamic_cooldown(owners_nolimit)
    async def deposit(self, interaction: discord.Interaction, robux: str):
        user = interaction.user
        actual_amount = determine_exponent(robux)

        async with self.client.pool_connection.acquire() as conn: # type: ignore
            conn: asqlite_Connection

            if await self.can_call_out(interaction.user, conn):
                return await interaction.response.send_message(embed=self.not_registered) # type: ignore
            users = await self.get_bank_data_new(user, conn)
            wallet_amt = users[1]
            if isinstance(actual_amount, str):
                if actual_amount.lower() == "all" or actual_amount.lower() == "max":
                    wallet_new = await self.update_bank_new(user, conn, -wallet_amt)
                    bank_new = await self.update_bank_new(user, conn, +wallet_amt, "bank")

                    embed = discord.Embed(colour=0x2F3136)
                    embed.add_field(name="Deposited", value=f"\U000023e3 {wallet_amt:,}", inline=False)
                    embed.add_field(name="Current Wallet Balance", value=f"\U000023e3 {wallet_new[0]:,}")
                    embed.add_field(name="Current Bank Balance:", value=f"\U000023e3 {bank_new[0]:,}")

                    return await interaction.response.send_message(embed=embed) # type: ignore
                return await interaction.response.send_message(embed=ERR_UNREASON) # type: ignore

            amount_conv = abs(int(actual_amount))
            if amount_conv < 5000:
                embed = discord.Embed(colour=0x2F3136,
                                      description=f"- For performance reasons, a minimum of "
                                                  f"\U000023e3 **5,000** must be deposited.\n"
                                                  f" - You wanted to deposit \U000023e3 **{amount_conv:,}**.\n")
                return await interaction.response.send_message(embed=embed) # type: ignore

            elif amount_conv > wallet_amt:
                embed = discord.Embed(colour=0x2F3136,
                                      description=f"- You do not have that much money in your wallet.\n"
                                                  f" - You wanted to deposit \U000023e3 **{amount_conv:,}**.\n"
                                                  f" - Currently, you only have \U000023e3 **{wallet_amt:,}**.")
                return await interaction.response.send_message(embed=embed) # type: ignore
            else:
                wallet_new = await self.update_bank_new(user, conn, -amount_conv)
                bank_new = await self.update_bank_new(user, conn, +amount_conv, "bank")  # \U000023e3

                embed = discord.Embed(colour=0x2F3136)
                embed.add_field(name="Deposited", value=f"\U000023e3 {amount_conv:,}", inline=False)
                embed.add_field(name="Current Wallet Balance", value=f"\U000023e3 {wallet_new[0]:,}")
                embed.add_field(name="Current Bank Balance", value=f"\U000023e3 {bank_new[0]:,}")

                return await interaction.response.send_message(embed=embed) # type: ignore

    @app_commands.command(name='leaderboard', description='ranks users with the most robux.')
    @app_commands.guilds(discord.Object(id=829053898333225010), discord.Object(id=780397076273954886))
    @app_commands.checks.dynamic_cooldown(owners_nolimit)
    async def get_leaderboard(self, interaction: discord.Interaction):

        async with self.client.pool_connection.acquire() as conn: # type: ignore
            conn: asqlite_Connection = conn

            data = await conn.execute(
                f"SELECT `userID`, SUM(`wallet` + `bank`) as total_balance FROM `{BANK_TABLE_NAME}` GROUP BY `userID` ORDER BY total_balance DESC",
                ())
            data = await data.fetchall()

            not_database = []
            index = 1
            unique_badges = {
                "546086191414509599": "<:in_power:1153754243220647997>",
                "992152414566232139": "<:e1_stafff:1145039666916110356>",
                "1134123734421217412": "<:e1_bughunterGold:1145053225414832199>",
                "1154092136115994687": "<:e1_bughunterGreen:1145052762351095998>",
                "713736460142116935": "<:e1_giggle:1150899657912893642>",
                "1047572530422108311": "<:cc:1146092310464049203>"
            }

            for member in data:
                # if index > 10:
                #     break
                member_name = await self.client.fetch_user(member[0])
                their_badge = unique_badges.setdefault(str(member_name.id), f"")
                member_amt = member[1]
                msg1 = f"**{index}.** {member_name.name} {their_badge}\n{CURRENCY}{member_amt:,}"
                not_database.append(msg1)
                index += 1

            msg = "\n\n".join(not_database)

            lb = discord.Embed(
                title=f"Leaderboard",
                description=f"The top `{index - 1}` users with the most amount of robux are displayed here.\n"
                            f"this is calculated based on net value of all users (wallet + bank).\n\n{msg}",
                color=0x2F3136,
                timestamp=discord.utils.utcnow()
            )
            lb.set_footer(
                text=f"all leaderboards are ranked globally",
                icon_url=self.client.user.avatar.url)

            await interaction.response.send_message(embed=lb) # type: ignore

    @commands.guild_only()
    @commands.cooldown(1, 5)
    @commands.command(name='extend_profile', description='display misc info on a user.',
                      aliases=('e_p', 'ep', 'extend'))
    async def extend_profile(self, ctx: commands.Context, username: Optional[discord.Member]):
        async with ctx.typing():
            user_stats = {}
            if username is None:
                username = ctx.author

            username = ctx.guild.get_member(username.id)

            user_stats["status"] = str(username.status)
            user_stats["is_on_mobile"] = str(username.is_on_mobile())
            user_stats["desktop"] = str(username.desktop_status)
            user_stats["web"] = str(username.web_status)
            user_stats["voice_status"] = str(username.voice)
            user_stats["is_bot"] = str(username.bot)
            user_stats["activity"] = str(username.activity)

            procfile = discord.Embed(title='Profile Summary', description=f'This mostly displays {username.display_name}\'s '
                                                                          f'prescence on Discord.',
                                     colour=0x2F3136)
            procfile.add_field(name=f'{username.display_name}\'s Extended Information',
                               value=f"\U0000279c Top role: {username.top_role.mention}\n"
                                     f"\U0000279c Is a bot: {user_stats['is_bot']}\n"
                                     f"\U0000279c Current Activity: {user_stats['activity']}\n"
                                     f"\U0000279c Status: {user_stats['status']}\n"
                                     f"\U0000279c Desktop Status: {user_stats['desktop']}\n"
                                     f"\U0000279c Web Status: {user_stats['web']}\n"
                                     f"\U0000279c Is on Mobile: {user_stats['is_on_mobile']}\n"
                                     f"\U0000279c Voice State: {user_stats['voice_status']}", )
            procfile.set_thumbnail(url=username.avatar.url) if username.avatar else procfile.set_thumbnail(
                url=username.default_avatar.url)
            procfile.set_footer(text=f"{discord.utils.utcnow().strftime('%A %d %b %Y, %I:%M%p')}")
            await ctx.send(embed=procfile)

    rob = app_commands.Group(name='rob', description='[Group Command] rob different places or people.',
                                guild_only=True, guild_ids=[829053898333225010, 780397076273954886])

    @rob.command(name="user", description="rob robux from another user.")
    @app_commands.describe(other='the user to rob from')
    @app_commands.checks.dynamic_cooldown(owners_nolimit)
    async def rob_the_user(self, interaction: discord.Interaction, other: discord.Member):
        """Rob someone else."""
        primary_id = str(interaction.user.id)
        other_id = str(other.id)

        async with self.client.pool_connection.acquire() as conn: # type: ignore
            conn: asqlite_Connection

            if other_id == primary_id:
                embed = membed('You cannot rob yourself, everyone knows that.')
                return await interaction.response.send_message(embed=embed) # type: ignore
            elif other.bot:
                embed = membed('You are not allowed to steal from bots, back off my kind')
                return await interaction.response.send_message(embed=embed) # type: ignore
            elif other_id == "992152414566232139":
                embed = membed('You are not allowed to rob the developer of this bot.')
                return await interaction.response.send_message(embed=embed) # type: ignore
            elif not (await self.can_call_out_either(interaction.user, other, conn)):  # if len of tup isnt 2, meaning one isnt registered
                embed = membed(f'- Either you or {other.name} does not have an account.\n'
                               f' - </balance:1179817617435926686> to register.')
                return await interaction.response.send_message(embed=embed) # type: ignore
            else:
                prim_bal = await self.get_bank_data_new(interaction.user, conn)
                host_bal = await self.get_bank_data_new(other, conn)

                caught = [0, 1]
                result = choices(caught, weights=(49, 51), k=1)  # more likely to successfully rob

                if not result[0]:
                    fine = randint(1, prim_bal[1])

                    prcf = round((fine/prim_bal[1])*100, ndigits=1)

                    await self.update_bank_new(interaction.user, conn, -fine)
                    await self.update_bank_new(other, conn, +fine)
                    conte = (f'- You were caught stealing now you paid {other.name} \U000023e3 **{fine:,}**.\n'
                             f'- **{prcf}**% of your money was handed over to the victim.')
                    return await interaction.response.send_message(embed=membed(conte)) # type: ignore
                else:
                    steal_amount = randint(1, host_bal[1])
                    await self.update_bank_new(interaction.user, conn, +steal_amount)
                    await self.update_bank_new(other, conn, -steal_amount)

                    prcf = round((steal_amount / host_bal[1]) * 100, ndigits=1)

                    return await interaction.response.send_message( # type: ignore
                        embed=membed(f"- You managed to steal \U000023e3 **{steal_amount:,}** from {other.name}.\n"
                                     f"- You took a dandy **{prcf}**% of {other.name}'s `wallet` balance."),
                        delete_after=10.0)

    @rob.command(name='casino', description='rob a vault deep in the heart of the casino.')
    async def get_input_user(self, interaction: discord.Interaction):

        await interaction.response.defer() # type: ignore

        async with self.client.pool_connection.acquire() as conn: # type: ignore
            conn: asqlite_Connection

            if await self.can_call_out(interaction.user, conn):
                return await interaction.followup.send(embed=self.not_registered)


            cooldown = await self.fetch_cooldown(conn, user=interaction.user, cooldown_type="casino")

            if cooldown is not None:
                if cooldown[0] in {"0", 0}:
                    channel = interaction.channel
                    ranint = randint(1000, 1999)
                    await channel.send(
                        embed=membed(f'A 4-digit PIN is required to enter the casino.\n'
                                     f'Here are the first 3 digits: {str(ranint)[:3]}'))

                    def check(m):
                        return m.content == f'{str(ranint)}' and m.channel == channel and m.author == interaction.user

                    try:
                        await self.client.wait_for('message', check=check, timeout=30.0)
                    except asyncTE:
                        await interaction.followup.send(
                            embed=membed(f"Too many seconds passed. Access denied. (The code was {ranint})"))
                    else:
                        msg = await interaction.followup.send(
                            embed=membed(f'You cracked the code and got access. Good luck escaping unscathed.'),
                            wait=True)
                        hp = 100
                        messages = await channel.send(
                            embed=membed("Passing through security forces.. (HP: 100/100)"),
                            reference=msg.to_reference(fail_if_not_exists=False))
                        hp -= randint(16, 40)
                        await sleep(0.9)
                        await messages.edit(embed=membed(f"Disabling security on security floor.. (HP {hp}/100)"))
                        hp -= randint(15, 59)
                        await sleep(0.9)
                        await messages.edit(embed=membed(f"Entering the vault.. (HP {hp}/100)"))
                        hp -= randint(1, 25)
                        await sleep(1.5)
                        if hp <= 5:
                            await self.update_bank_new(interaction.user, conn, )
                            timeout = randint(5, 12)
                            await messages.edit(
                            embed=membed(f"## <:rwarning:1165960059260518451> Critical HP Reached.\n"
                                         f"- Your items and robux will not be lost.\n"
                                         f"- Police forces were alerted and escorted you out of the building.\n"
                                         f"- You may not enter the casino for another **{timeout}** hours."))
                            ncd = datetime.datetime.now() + datetime.timedelta(hours=timeout)  # the cd
                            ncd = datetime_to_string(ncd)
                            await self.update_cooldown(conn, user=interaction.user, cooldown_type="casino", new_cd=ncd)
                        else:
                            recuperate_amt = randint(6, 21)
                            total, extra = 0, 0
                            pmulti = await self.get_pmulti_data_only(interaction.user, conn)
                            new_multi = SERVER_MULTIPLIERS.setdefault(interaction.guild.id, 0) + pmulti[0]

                            for _ in range(recuperate_amt):
                                fill_by = randint(212999999, 286999999)
                                total += fill_by
                                extra += floor(((new_multi / 100) * fill_by))
                                await messages.edit(
                                    embed=membed(f"> \U0001f4b0 **{interaction.user.name}'s "
                                                 f"Duffel Bag**: {total:,} / 3,000,000,000\n"
                                                 f"> {PREMIUM_CURRENCY} **Bonus**: {extra:,} / 5,000,000,0000"))
                                await sleep(0.9)

                            overall = total + extra
                            wllt = await self.update_bank_new(interaction.user, conn, +overall)

                            timeout = randint(18, 24)
                            ncd = datetime.datetime.now() + datetime.timedelta(hours=timeout)  # the cd
                            ncd = datetime_to_string(ncd)
                            await self.update_cooldown(conn, user=interaction.user, cooldown_type="casino", new_cd=ncd)
                            bounty = randint(12500000, 105_000_000)
                            nb = await self.update_bank_new(interaction.user, conn, +bounty, "bounty")
                            await messages.edit(
                                content=f"Your bounty has increased by \U000023e3 "
                                        f"**{bounty:,}**, to \U000023e3 **{nb[0]:,}**!",
                                embed=membed(f"> \U0001f4b0 **{interaction.user.name}'s "
                                             f"Duffel Bag**: \U000023e3 {total:,} / \U000023e3 10,000,000,000\n"
                                             f"> {PREMIUM_CURRENCY} **Bonus**: \U000023e3 {extra:,} "
                                             f"/ \U000023e3 50,000,000,0000\n"
                                             f"> [\U0001f4b0 + {PREMIUM_CURRENCY}] **Total**: \U000023e3 **{overall:,}"
                                             f"**\n\nYou escaped without a scratch.\n"
                                             f"Your new `wallet` balance is \U000023e3 {wllt[0]:,}"))
                else:
                    cooldown = string_to_datetime(cooldown[0])
                    now = datetime.datetime.now()
                    diff = cooldown - now

                    if diff.total_seconds() <= 0:
                        await self.update_cooldown(conn, user=interaction.user, cooldown_type="casino",
                                                   new_cd="0")
                        await interaction.followup.send(
                            embed=membed("The casino is now ready for use.\n"
                                         "Call this command again to start a robbery."))
                    else:
                        minutes, seconds = divmod(diff.total_seconds(), 60)
                        hours, minutes = divmod(minutes, 60)
                        days, hours = divmod(hours, 24)
                        await interaction.followup.send(f"# Not yet.\n"
                                                        f"The casino is not ready. It will be available for "
                                                        f"you in **{int(hours)}** hours, **{int(minutes)}** minutes "
                                                        f"and **{int(seconds)}** seconds.")

    @app_commands.command(name='coinflip', description='bet your robux on a coin flip')
    @app_commands.guilds(discord.Object(id=829053898333225010), discord.Object(id=780397076273954886))
    @app_commands.describe(bet_on='what side of the coin you bet it will flip on',
                           amount='the amount of robux to bet. Supports Shortcuts (exponents only)')
    @app_commands.checks.dynamic_cooldown(owners_nolimit)
    @app_commands.rename(bet_on='side', amount='robux')
    async def coin_flip(self, interaction: discord.Interaction, bet_on: str, amount: int):
        user = interaction.user

        async with self.client.pool_connection.acquire() as conn: # type: ignore

            amount = determine_exponent(str(amount))

            bet_on = "heads" if "h" in bet_on.lower() else "tails"
            if not 500 <= amount <= 200000000:
                return await interaction.response.send_message(  # type: ignore
                    embed=membed(f"*As per-policy*, the minimum bet is {CURRENCY}**500**, the maximum is "
                                 f"{CURRENCY}**200,000,000**."))
            reward = round(amount / 2)

            conn: asqlite_Connection
            if await self.can_call_out(interaction.user, conn):
                return await interaction.response.send_message(embed=self.not_registered) # type: ignore
            users = await self.get_bank_data_new(user, conn)
            if users[1] < amount:
                return await interaction.response.send_message(embed=ERR_UNREASON) # type: ignore

            coin = ["heads", "tails"]
            result = choice(coin)

            if result != bet_on:
                await self.update_bank_new(user, conn, -amount)
                return await interaction.response.send_message( # type: ignore
                    embed=membed(f"You got {result}, meaning you lost \U000023e3 **{amount:,}**."))

            await self.update_bank_new(user, conn, +reward)
            return await interaction.response.send_message(embed=membed(f"You got {result}, meaning you won \U000023e3 " # type: ignore
                                                                        f"**{reward:,}** (50% capital gains tax)."))

    @commands.command(name='blackjack', description='play a quick round of [blackjack.](https://www.youtube.com/watch?v=VB-6MvXvsKo)',
                      aliases=("bj",))
    @commands.cooldown(1, 12)
    @commands.guild_only()
    async def start_blackjack(self, ctx: commands.Context, bet_amount):

        # ------ Check the user is registered or already has an ongoing game ---------
        if len(self.client.games) >= 2: # type: ignore
            return await ctx.send(
                embed=membed(
                    "- The maximum consecutive blackjack games being held has been reached.\n"
                    "- To prevent server overload, you cannot start a game until the current games "
                    "being played has been finished.\n"
                    " - The maximum consecutive blackjack game quota has been set to `2`."
                )
            )

        if self.client.games.setdefault(ctx.author.id, None) is not None: # type: ignore
            return await ctx.send("You already have an ongoing game taking place.")

        async with self.client.pool_connection.acquire() as conn: # type: ignore
            conn: asqlite_Connection
            if await self.can_call_out(ctx.author, conn):
                return await ctx.send(embed=self.not_registered) # type: ignore

        # --------------------------------------------------------------

        # ----------------- Game setup ---------------------------------

        deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10] * 4
        shuffle(deck)

        player_hand = [deck.pop(), deck.pop()]
        dealer_hand = [deck.pop(), deck.pop()]


        keycard_amt = await self.get_one_inv_data_new(ctx.author, "Keycard", conn)
        wallet_amt = await self.get_wallet_data_only(ctx.author, conn)
        pmulti = await self.get_pmulti_data_only(ctx.author, conn)
        has_keycard = keycard_amt >= 1
        # ----------- Check what the bet amount is, converting where necessary -----------

        expo = determine_exponent(bet_amount)  # negatives and decimals removed already

        try:
            assert isinstance(expo, int)
            namount = expo
        except AssertionError:

            if bet_amount.lower() in {'max', 'all'}:
                if has_keycard and wallet_amt >= 100_000_000:
                    namount = 100_000_000
                else:
                    namount = wallet_amt
            else:
                ctx.command.reset_cooldown(ctx)
                return await ctx.send(embed=ERR_UNREASON)  # type: ignore

        # -------------------- Check to see if user has sufficient balance --------------------------

        if has_keycard:
            # if the user has a keycard
            if (namount > 100_000_000) or (namount < 500_000):
                err = discord.Embed(colour=0x2F3136, description=f'## You did not meet the blackjack criteria:\n'
                                                                 f'- You wanted to bet {CURRENCY}**{namount:,}**\n'
                                                                 f' - A minimum bet of {CURRENCY}**500,000** must '
                                                                 f'be made\n'
                                                                 f' - A maximum bet of {CURRENCY}**100,000,000** '
                                                                 f'can only be made.')
                return await ctx.send(embed=err)  # type: ignore
            if namount > wallet_amt:
                err = discord.Embed(colour=0x2F3136, description=f'Cannot perform this action, '
                                                                 f'you only have {CURRENCY}**{wallet_amt:,}**\n'
                                                                 f'You\'ll need {CURRENCY}**{namount - wallet_amt:,}**'
                                                                 f' more in your wallet first.')
                return await ctx.send(embed=err)  # type: ignore
        else:
            if (namount > 50_000_000) or (namount < 1000000):
                err = discord.Embed(colour=0x2F3136, description=f'## You did not meet the blackjack criteria:\n'
                                                                 f'- You wanted to bet {CURRENCY}**{namount:,}**\n'
                                                                 f' - A minimum bet of {CURRENCY}**1,000,000** must '
                                                                 f'be made (this can decrease when you acquire a'
                                                                 f' <:lanyard:1165935243140796487> Keycard).\n'
                                                                 f' - A maximum bet of {CURRENCY}**50,000,000** '
                                                                 f'can only be made (this can increase when you '
                                                                 f'acquire a <:lanyard:1165935243140796487> '
                                                                 f'Keycard).')
                return await ctx.send(embed=err)  # type: ignore
            if namount > wallet_amt:
                err = discord.Embed(colour=0x2F3136, description=f'Cannot perform this action, '
                                                                 f'you only have {CURRENCY}**{wallet_amt:,}**\n'
                                                                 f'You\'ll need {CURRENCY}**{namount - wallet_amt:,}**'
                                                                 f' more in your wallet first.')
                return await ctx.send(embed=err)  # type: ignore

        # ------------ In the case where the user already won --------------
        if self.calculate_hand(player_hand) == 21:

            bj_lose = await conn.execute('SELECT bjl FROM bank WHERE userID = ?', (ctx.author.id,))
            bj_lose = await bj_lose.fetchone()
            new_bj_win = await self.update_bank_new(ctx.author, conn, 1, "bjw")
            new_total = new_bj_win[0] + bj_lose[0]
            prctnw = round((new_bj_win[0]/new_total)*100)

            new_multi = SERVER_MULTIPLIERS.setdefault(ctx.guild.id, 0) + pmulti[0]
            amount_after_multi = floor(((new_multi / 100) * namount) + namount) + randint(1, 999)
            # tma = amount_after_multi - namount
            new_amount_balance = await self.update_bank_new(ctx.author, conn, amount_after_multi)

            d_fver_p = display_user_friendly_deck_format(player_hand)
            d_fver_d = display_user_friendly_deck_format(dealer_hand)


            embed = discord.Embed(colour=discord.Colour.brand_green(),
                                  description=(
                                      f"**Blackjack! You've already won with a total of {sum(player_hand)}!**\n\n"
                                      f"You won {CURRENCY}**{amount_after_multi:,}**. "
                                      f"You now have {CURRENCY}**{new_amount_balance[0]:,}**.\n"
                                      f"You won {prctnw}% of the games."))
            embed.add_field(name=f"{ctx.author.name} (Player)", value=f"**Cards** - {' '.join(d_fver_p)}\n"
                                                                      f"**Total** - `{sum(player_hand)}`")
            embed.add_field(name=f"{ctx.guild.me} (Dealer)", value=f"**Cards** - {' '.join(d_fver_d)}\n"
                                                                   f"**Total** - {sum(dealer_hand)}")
            return await ctx.send(embed=embed)

        shallow_pv = []
        shallow_dv = []

        for number in player_hand:
            remade = display_user_friendly_card_format(number)
            shallow_pv.append(remade)

        for number in dealer_hand:
            remade = display_user_friendly_card_format(number)
            shallow_dv.append(remade)

        # self.client.games[ctx.author.id] = (deck, player_hand, dealer_hand, namount)  # type: ignore  # before
        self.client.games[ctx.author.id] = (deck, player_hand, dealer_hand, shallow_dv, shallow_pv, namount) # type: ignore  # after


        start = discord.Embed(colour=discord.Colour.dark_theme(),
                              description=f"The game has started. May the best win.\n"
                                          f"`\U000023e3 ~{format_number_short(namount)}` is up for grabs on the table.")

        start.add_field(name=f"{ctx.author.name} (Player)", value=f"**Cards** - {' '.join(shallow_pv)}\n"
                                                                  f"**Total** - `{sum(player_hand)}`")
        start.add_field(name=f"{ctx.guild.me.name} (Dealer)", value=f"**Cards** - {shallow_dv[0]} `?`\n"
                                                               f"**Total** - ` ? `")
        avatar = ctx.author.avatar or ctx.author.default_avatar
        start.set_author(icon_url=avatar.url, name=f"{ctx.author.name}'s blackjack game")
        start.set_footer(text="K, Q, J = 10  |  A = 1 or 11")
        await ctx.send(content="What do you want to do?\n"
                               "Type `>h` to **hit** or `>s` to **stand**, ending the game.",
                       embed=start)

    @app_commands.command(name="bet",
                          description="bet your robux on a dice roll to win or lose robux.")
    @app_commands.guilds(discord.Object(id=829053898333225010), discord.Object(id=780397076273954886))
    @app_commands.checks.dynamic_cooldown(owners_nolimit)
    @app_commands.rename(exponent_amount='robux')
    @app_commands.describe(exponent_amount='the amount of robux to bet. Supports Shortcuts (max, all, exponents).')
    async def bet(self, interaction: discord.Interaction, exponent_amount: str):
        """Bet your robux on a gamble to win or lose robux."""

        # --------------- Contains checks before betting i.e. has keycard, meets bet constraints. -------------
        async with self.client.pool_connection.acquire() as conn: # type: ignore
            if await self.can_call_out(interaction.user, conn):
                return await interaction.response.send_message(embed=self.not_registered) # type: ignore
            conn: asqlite_Connection
            keycard_amt = await self.get_one_inv_data_new(interaction.user, "Keycard", conn)
            wallet_amt = await self.get_wallet_data_only(interaction.user, conn)
            pmulti = await self.get_pmulti_data_only(interaction.user, conn)
            has_keycard = keycard_amt >= 1
            expo = determine_exponent(exponent_amount)  # negatives and decimals removed already

            try:
                assert isinstance(expo, int)
                amount = expo
            except AssertionError:
                if exponent_amount.lower() in {'max', 'all'}:
                    amount = 100000000 if has_keycard else 50000000
                else:
                    return await interaction.response.send_message(embed=ERR_UNREASON) # type: ignore

            if amount == 0:
                await interaction.response.send_message(embed=ERR_UNREASON) # type: ignore
            if has_keycard:
                # if the user has a keycard
                if (amount > 100000000) or (amount < 100000):
                    err = discord.Embed(colour=0x2F3136, description=f'## You did not meet the bet criteria:\n'
                                                                     f'- You wanted to bet {CURRENCY}**{amount:,}**\n'
                                                                     f' - A minimum bet of {CURRENCY}**100,000** must '
                                                                     f'be made\n'
                                                                     f' - A maximum bet of {CURRENCY}**100,000,000** '
                                                                     f'can only be made.')
                    return await interaction.response.send_message(embed=err) # type: ignore
                elif amount > wallet_amt:
                    err = discord.Embed(colour=0x2F3136, description=f'Cannot perform this action, '
                                                                     f'you only have {CURRENCY}**{wallet_amt:,}**\n'
                                                                     f'You\'ll need {CURRENCY}**{amount - wallet_amt:,}**'
                                                                     f' more in your wallet first.')
                    return await interaction.response.send_message(embed=err) # type: ignore
            else:
                if (amount > 50000000) or (amount < 500000):
                    err = discord.Embed(colour=0x2F3136, description=f'## You did not meet the bet criteria:\n'
                                                                     f'- You wanted to bet {CURRENCY}**{amount:,}**\n'
                                                                     f' - A minimum bet of {CURRENCY}**500,000** must '
                                                                     f'be made (this can decrease when you acquire a'
                                                                     f' <:lanyard:1165935243140796487> Keycard).\n'
                                                                     f' - A maximum bet of {CURRENCY}**50,000,000** '
                                                                     f'can only be made (this can increase when you '
                                                                     f'acquire a <:lanyard:1165935243140796487> '
                                                                     f'Keycard).')
                    return await interaction.response.send_message(embed=err) # type: ignore
                elif amount > wallet_amt:
                    err = discord.Embed(colour=0x2F3136, description=f'Cannot perform this action, '
                                                                     f'you only have {CURRENCY}**{wallet_amt:,}**\n'
                                                                     f'You\'ll need {CURRENCY}**{amount - wallet_amt:,}**'
                                                                     f' more in your wallet first.')
                    return await interaction.response.send_message(embed=err) # type: ignore

            # --------------------------------------------------------

            if has_keycard:
                your_choice = choices([1, 2, 3, 4, 5, 6], weights=[40/3, 40/3, 40/3, 60/3, 60/3, 60/3], k=1)
                bot_choice = choices([1, 2, 3, 4, 5, 6],
                                     weights=[70/4, 70/4, 70/4, 70/4, 15, 15], k=1)
            else:
                bot_choice = choices([1, 2, 3, 4, 5, 6],
                                     weights=[10, 10, 15, 27, 15, 23], k=1)
                your_choice = choices([1, 2, 3, 4, 5, 6], weights=[55/3, 55/3, 55/3, 45/3, 45/3, 45/3], k=1)

            content_before = (f"{interaction.user.mention}, you don't have a personal multiplier yet. **Set "
                              f"one up now:** </multi view:1179817617251369074>.") if pmulti[0] in {"0", 0} else ""

            if your_choice[0] > bot_choice[0]:  # this roll is considered a win, so give them the amount bet PLUS the multi effect.

                bet_stuff = await self.get_bank_data_new(interaction.user, conn)
                id_won_amount, id_lose_amount = bet_stuff[5], bet_stuff[6]
                avatar = interaction.user.display_avatar or interaction.user.default_avatar

                new_multi = SERVER_MULTIPLIERS.setdefault(interaction.guild.id, 0) + pmulti[0]
                amount_after_multi = floor(((new_multi / 100) * amount) + amount)
                tma = amount_after_multi - amount
                new_amount_balance = await self.update_bank_new(interaction.user, conn, amount_after_multi)
                new_id_won_amount = await self.update_bank_new(interaction.user, conn, 1, "betw")
                new_total = id_lose_amount + new_id_won_amount[0]

                prcntw = round((new_id_won_amount[0]/new_total)*100, 1)

                embed = discord.Embed(description=f"## {interaction.user.mention}'s winning gambling game\n"
                                                  f"\U0000279c You won {CURRENCY}**{amount_after_multi:,}** robux.\n"
                                                  f"\U0000279c Bonus: {PREMIUM_CURRENCY} **{tma:,}** via "
                                                  f"a `{new_multi}x` multiplier.\n"
                                                  f"<:linkit:1176970030961930281> `{pmulti[0]}x` Personal Multi, "
                                                  f"`{new_multi-pmulti[0]}x` Server Multi.\n"
                                                  f"\U0000279c Your new `wallet` balance is {CURRENCY}"
                                                  f"**{new_amount_balance[0]:,}**.",
                                      colour=discord.Color.brand_green())

                embed.set_footer(text=f"You've won {prcntw}% of all games. ({new_id_won_amount[0]:,}/{new_total:,})",
                                 icon_url=avatar.url)

            elif your_choice[0] == bot_choice[0]:
                embed = discord.Embed(description=f"## {interaction.user.mention}'s gambling game\n"
                                                  f"**Tie.** You lost nothing nor gained anything!",
                                      colour=discord.Color.yellow())

            else:  # not considered a win

                bet_stuff = await self.get_bank_data_new(interaction.user, conn)
                id_won_amount, id_lose_amount = bet_stuff[5], bet_stuff[6]
                avatar = interaction.user.display_avatar or interaction.user.default_avatar

                new_amount_balance = await self.update_bank_new(interaction.user, conn, -amount)
                new_id_lose_amount = await self.update_bank_new(interaction.user, conn, 1, "betl")
                new_total = id_won_amount + new_id_lose_amount[0]

                prcntl = round((new_id_lose_amount[0]/new_total)*100, 1)

                embed = discord.Embed(description=f"## {interaction.user.mention}'s losing gambling game\n"
                                                   f"\U0000279c You lost {CURRENCY}**{amount:,}**.\n"
                                                   f"\U0000279c No multiplier accrued due to a lost bet.\n"
                                                   f"\U0000279c Your new `wallet` balance "
                                                   f"is {CURRENCY}**{new_amount_balance[0]:,}**.",
                                       colour=discord.Color.brand_red())

                embed.set_footer(
                    text=f"You've lost {prcntl}% of all games. ({new_id_lose_amount[0]:,}/{new_total:,})",
                    icon_url=avatar.url)

            embed.add_field(name=interaction.user.name, value=f"Rolled `{your_choice[0]}`")
            embed.add_field(name=self.client.user.name, value=f"Rolled `{bot_choice[0]}`")
            await interaction.response.send_message(content=content_before, embed=embed)  # type: ignore

async def setup(client: commands.Bot):
    await client.add_cog(Economy(client))
