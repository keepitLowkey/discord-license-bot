import discord
from discord.ext import commands
import yaml


with open("./config.yml", 'r') as file:
    config = yaml.load(file, Loader = yaml.Loader)


client = commands.Bot(command_prefix =config['Prefix'])
client.remove_command('help')


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="your license"))
    print('License Bot - READY !')

@client.command()
async def upgrade(ctx, arg1):
    await ctx.message.delete()
    with open(config['SerialFile']) as license_file:
        if arg1 in license_file.read():
            embed2=discord.Embed(title=config['ValidTitle'], color=0x00ff00)
            embed2.add_field(name=config['ValidName'], value=config['ValidValue'], inline=False)
            embed2.set_author(
                            name = ctx.author.name,
                            icon_url = ctx.author.avatar_url)
            embed2.set_footer(text=config['ValidFooter'])
            await ctx.send(embed=embed2)
            role = discord.utils.get(ctx.guild.roles, name=config['RoleName'])
            user = ctx.message.author
            await user.add_roles(role)
            print('Valid license: ', str(user), arg1)
        else:
            embed2=discord.Embed(title=config['InvalidTitle'], color=0xFF0000)
            embed2.set_author(
                            name = ctx.author.name,
                            icon_url = ctx.author.avatar_url)
            embed2.set_footer(text=config['InvalidFooter'])
            await ctx.send(embed=embed2)
            print('Invalid license: ', str(user), arg1)
        with open(config['SerialFile'],"r+") as f:
            file_content = f.readlines()
            f.seek(0)
            for line in file_content:
                if arg1 not in line:
                    f.write(line)
            f.truncate()

client.run(config['TOKEN'])
