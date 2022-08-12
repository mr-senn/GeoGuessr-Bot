
#imports
import asyncio
import os
import discord
import random
import mysql.connector
from os import environ
from geoguessr import *
from inputs import africa, asia, na, sa, europe, oceania, misc, custom, definitions
from discord import embeds
from discord.ext.commands.errors import *
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType, CommandOnCooldown

# Variables for setting up the bot.
TOKEN = environ['TOKEN']
db_host = environ['DB_HOST']
db_database = environ['DB_DATABASE']
db_user = environ['DB_USER']
db_password = environ['DB_PASSWORD']
db_port = environ['DB_PORT']

client = commands.Bot(command_prefix = '-', case_insensitive=True)
client.remove_command('help')
game = GeoGuessorBot()

@client.event
async def on_ready():
    # Tells user that the bot is ready to be used
    print('Discord Bot Initiated')

@client.command(aliases = ["maps"])
async def mapsinfo(ctx):
    # A help command that tells the user of the maps available for the bot to use.
    page_count = 0
    buttons = [u"\u23EA", u"\u2B05", u"\u27A1", u"\u23E9"]
    remove_char = ["{", "}", "'"]
    author = ctx.author
    
    africa_list = (', '.join(sorted(filter(lambda i: i not in remove_char, africa))))
    asia_list = (', '.join(sorted(filter(lambda i: i not in remove_char, asia))))
    na_list = (', '.join(sorted(filter(lambda i: i not in remove_char, na))))
    sa_list = (', '.join(sorted(filter(lambda i: i not in remove_char, sa))))
    europe_list = (', '.join(sorted(filter(lambda i: i not in remove_char, europe))))
    oceania_list = (', '.join(sorted(filter(lambda i: i not in remove_char, oceania)))) 
    misc_list = (', '.join(sorted(filter(lambda i: i not in remove_char, misc))))
    custom_list = (', '.join(sorted(filter(lambda i: i not in remove_char, custom))))

    page1 = discord.Embed(
        color = discord.Color.orange(),
        title = "Maps",
        description = "Flip through all the pages to find all official GeoGuessr maps. Custom Maps are on the last page."

    )
    page2 = discord.Embed(
        color = discord.Color.orange(),
    )
    page3 = discord.Embed(
        color = discord.Color.orange(),
    )
    page4 = discord.Embed(
        color = discord.Color.orange(),
    )
    page5 = discord.Embed(
        color = discord.Color.orange(),
    )
    page6 = discord.Embed(
        color = discord.Color.orange(),
    )
    page7 = discord.Embed(
        color = discord.Color.orange(),
    )
    page8 = discord.Embed(
        color = discord.Color.orange(),
    )
    page9 = discord.Embed(
        color = discord.Color.orange(),
    )
    page1.add_field(name = "Note:" , value = "You can use any of these maps listed in this message with the -geo command. Use -help to learn the correct syntax.")
    page1.set_footer(icon_url= author.avatar_url, text= "Page 1")
    
    page2.add_field(name = "Africa Maps", value = africa_list, inline = True)
    page2.add_field(name = "Example of playing an Africa Map", value = "-geo madagascar nm", inline = True)
    page2.set_footer(icon_url= author.avatar_url, text= "Page 2")
    
    page3.add_field(name = "Asia Maps", value = asia_list, inline = True)
    page3.add_field(name = "Example of playing an Asia Map", value = "-geo india nm", inline = True)
    page3.set_footer(icon_url= author.avatar_url, text= "Page 3")
    
    page4.add_field(name = "Europe Maps", value = europe_list, inline = True)
    page4.add_field(name = "Example of playing an Europe Map", value = "-geo uk nm", inline = True)
    page4.set_footer(icon_url= author.avatar_url, text= "Page 4")
    
    page5.add_field(name = "Miscellaneous Maps", value = misc_list, inline = True)
    page5.add_field(name = "Example of playing a Miscellaneous Map", value = "-geo famous-places nm", inline = True)
    page5.set_footer(icon_url= author.avatar_url, text= "Page 5")
    
    page6.add_field(name = "North America Maps", value = na_list, inline = True)
    page6.add_field(name = "Example of playing a North America Map", value = "-geo usa nm", inline = True)
    page6.set_footer(icon_url= author.avatar_url, text= "Page 6")

    page7.add_field(name = "South America Maps", value = sa_list, inline = True)
    page7.add_field(name = "Example of playing a South America Map", value = "-geo peru nm", inline = True)
    page7.set_footer(icon_url= author.avatar_url, text= "Page 7")

    page8.add_field(name = "Oceania Maps", value = oceania_list, inline = True)
    page8.add_field(name = "Example of playing an Oceania Map", value = "-geo australia nm", inline = True)
    page8.set_footer(icon_url= author.avatar_url, text= "Page 8")
    
    page9.add_field(name = "Custom Maps", value = custom_list, inline = True)
    page9.add_field(name = "Example of playing a Custom Map", value = "-geo urban-world-nobrr nm", inline = True)
    page9.set_footer(icon_url= author.avatar_url, text= "Page 9")


    help_pages = [page1, page2, page3, page4, page5, page6, page7, page8, page9]
    message = await ctx.send(embed = help_pages[page_count])

    for button in buttons:
        await message.add_reaction(button)
    
    while True:
        try: 
            reaction, user = await client.wait_for("reaction_add", check = lambda reaction, user: user == ctx.author and reaction.emoji in buttons, timeout = 60.0)
        except asyncio.TimeoutError:
            pass

        else:
            prev_page = page_count
            
            if reaction.emoji == u"\u23EA":
                page_count = 0

            elif reaction.emoji  == u"\u2B05":
                if page_count > 0:
                    page_count -= 1

            elif reaction.emoji == u"\u27A1":
                if page_count < len(help_pages)-1:
                    page_count += 1

            elif reaction.emoji == u"\u23E9":
                page_count = len(help_pages)-1
            
            for button in buttons:
                await message.remove_reaction(button, ctx.author)
            
            if page_count != prev_page:
                await message.edit(embed = help_pages[page_count])

@client.command(aliases = ["options", "game-rules"])
async def optioninfo(ctx):
    # a help command that tells the user of all the options the bot can use.
    remove_char = ["{", "}", "'"]
    options_list = (', '.join(sorted(filter(lambda i: i not in remove_char, options))))
    definitions_list = ('\n'.join(sorted(filter(lambda i: i not in remove_char, definitions))))

    options_page = discord.Embed(
        color = discord.Color.orange(),
        title = "Options",
        description = "You can make a game with custom game rules that GeoGuessr has to offer."
    )
    options_page.add_field(name = "Options:", value = options_list, inline = True)
    options_page.add_field(name = "Game Setting Explainations:", value = definitions_list, inline = True)
    options_page.add_field(name = "Example of using an option (game rule):", value = "-geo diverse-world nm", inline = False)
    options_page.add_field(name = "Note:", value = "The time rule has not been implemented yet. It will be implemented in a future update :)", inline = False)

    await ctx.send(embed = options_page)

@client.command()
async def disclaimer(ctx):
    disclaimer_msg = discord.Embed(
        color = discord.Color.blue(),
        title = "Disclaimer",
        description = "Please keep in mind that this bot is using the GeoGuessr.com website to generate links. If the developers of GeoGuessr.com change their website at anytime, this bot has a chance of breaking."
    )
    disclaimer_msg.set_footer(text = "If the bot breaks, please contact #senn0526. Let the server staff know the bot is not working as well.")
    await ctx.send(embed = disclaimer_msg)

@client.command(aliases = ["help"])
async def help_command(ctx):
    # a help command that gives instructions on how to use the bot on discord.
    author = ctx.author

    help_page = discord.Embed(
        color = discord.Color.orange(),
        title = "Help Page",
        description = "Welcome to the help page! Learn about all the commands for this bot below!"
    )

    help_page.add_field(name = "-geo", value = "The -geo command is how you can start a GeoGuessr game.\n Alternatively you can use -g or -game! \n -geo [map] [rule]" , inline = True)
    help_page.add_field(name = "Example of using the -geo command", value = "-geo usa nm \n -g usa nm \n -game usa nm", inline = True)
    help_page.add_field(name = "Note:" , value = "You must put in a map and game rule! See -maps and -options for more details. \n There is a 60 second cooldown for this command.", inline = True)
    help_page.add_field(name = "-rematch", value = "The -rematch command will create a GeoGuessr game with the last played map and game rule.", inline = False)
    help_page.add_field(name = "-current", value = "The -current command will show you the current game that is being played.", inline = False)
    help_page.add_field(name = "-random", value = "The -random command will create a random GeoGuessr game with a random map and game rule!", inline = False)
    help_page.add_field(name = "-maps", value = "The -maps command will list all the available maps to play!", inline = False)
    help_page.add_field(name = "-options", value = "The -options command will list all the game rule options you can use!", inline= False)
    help_page.add_field(name = "-bookmark", value = "The -bookmark will let you store the latest GeoGuessr game for you to play at a later time! The command will only store the most current game.", inline= False)
    help_page.add_field(name = "-saves", value = "The -saves command will show you all your bookmarked GeoGuessr games!", inline= False)
    help_page.add_field(name = "-clear", value = "The -clear command will clear all your bookmarked GeoGuessr games.\nCAUTION: This command will permanently delete all your bookmarks and it is non-reversible!", inline= False)
    help_page.add_field(name = "-author", value = "Learn about who made this bot :)", inline= False)
    help_page.set_footer(icon_url = author.avatar_url, text = "\n\nPlease read -disclaimer")
    await ctx.send(embed = help_page)

@client.command(aliases = ["author"])
async def credits(ctx):
    # a command that tells the user of who made this bot.
    about = discord.Embed(
        color = discord.Color.dark_red(),
        title = "Credits:",
        description = "This bot was made by #senn0526" 
    )
    about.set_thumbnail(url = "https://cdn.discordapp.com/avatars/239941463717314560/a_5199b98813b8a9c90327c033b3440f9e.gif?size=1024")
    about.add_field(name = "Cash App", value = "$SohomSen", inline = False)
    await ctx.send(embed = about)

@client.command(aliases = ["g", "game"])
@commands.cooldown(1,60, BucketType.guild)
async def geo(ctx, arg1, arg2):
    # this command is the call for using the GeoGuessr.py functions. It takes in two arugments from the user in discord: map and rule
    current_server_id = str(ctx.guild.id)
    current_server_name = ctx.guild.name
    author = ctx.author
    user_map = arg1.lower()
    rule = arg2.lower()

    connection = mysql.connector.connect(host= db_host,
                                         database= db_database,
                                         user= db_user,
                                         password = db_password,
                                         port = db_port)
    cursor = connection.cursor(prepared=True)

    generatelink_message = discord.Embed(
        color = discord.Color.gold(),
    )
    
    if user_map in maps and rule in options:
        
        generatelink_message.add_field(name = "Thanks for the request! Generating the GeoGuessr link now!", value = f"Map selected: {user_map}\nGame rule selected: {rule}", inline = False)
        generatelink_message.set_footer(icon_url= author.avatar_url, text = f"Game requested by {author.display_name} ({author}) ")
        await ctx.send(embed = generatelink_message)
        
        print("Game sent to generate")
        
        game_link = game.map_generator(user_map, rule)
        
        game_message = discord.Embed(
            color = discord.Color.green(),
        )
        game_message.add_field(name = "Enjoy the game!", value = f"Map selected: {user_map}\nGame rule selected: {rule}\n{game_link}", inline = False)
        game_message.set_footer(icon_url= author.avatar_url, text = f"Game generated by {author.display_name} ({author})")
        await ctx.send(embed = game_message)
        print("Game link sent")     
        try:
            sql_insert_query = """ INSERT INTO discord_servers (server_id, server_name, map_used, rule_used, map_link)
                                                VALUES 
                                                (%s,%s,%s,%s,%s) AS s
                                                ON DUPLICATE KEY UPDATE
                                                map_used = s.map_used, server_name = s.server_name, rule_used = s.rule_used, map_link = s.map_link;"""
            map_played = (current_server_id, current_server_name, user_map, rule, game_link)
            cursor.execute(sql_insert_query, map_played)
            connection.commit()
            print(f"The following was stored in the database successfully: Server: {current_server_name}, Map: {user_map}, Rule: {rule}, Game Link: {game_link}")

        except mysql.connector.Error as error:
            print("Uh oh. Something went wrong. {}".format(error))
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

        if game_link == False:
            bad_map  = discord.Embed(
                color = discord.Color.red(),
            )
            bad_map.add_field(name = "Uh oh!", value = "Something went wrong, please try again.", inline = False)
            await ctx.send(embed = bad_map)
            #await ctx.send("Something went wrong, please try again.") 
    else:
        bad_map  = discord.Embed(
            color = discord.Color.red(),
        )
        bad_map.add_field(name = "Uh oh!", value = "Game link could not be generated based on your input. Reference -help for help!", inline = False)
        await ctx.send(embed = bad_map)
        ctx.command.reset_cooldown(ctx)
        print("Input was wrong")

@client.command(aliases = ["re"])
@commands.cooldown(1,60, BucketType.guild)
async def rematch(ctx):

    connection = mysql.connector.connect(host= db_host,
                                         database= db_database,
                                         user= db_user,
                                         password = db_password,
                                         port = db_port)

    cursor = connection.cursor(prepared=True)

    author = ctx.author
    current_server_id = str(ctx.guild.id)
    current_server_name = ctx.guild.name

 

    generatelink_message = discord.Embed(
        color = discord.Color.gold(),
    )

    try:
        sql_select_query = f"SELECT map_used, rule_used from discord_servers WHERE server_id = {current_server_id};"
        cursor = connection.cursor()
        cursor.execute(sql_select_query)
        retrieve_last_map = cursor.fetchall()
        for row in retrieve_last_map:
            user_map = row[0]
            rule = row[1]
        print(f"The following was retrieved from the database successfully: Server: {current_server_name}, Map: {user_map}, Rule: {rule}")
        if user_map in maps and rule in options:
            
            generatelink_message.add_field(name = "Thanks for the request! Generating the GeoGuessr link with the previous configurations now!", value = f"Previous map: {user_map}\nPrevious game rule: {rule}", inline = False)
            generatelink_message.set_footer(icon_url= author.avatar_url, text = f"Game requested by {author.display_name} ({author}) ")
            await ctx.send(embed = generatelink_message)
            
            print("Game sent to generate")
            
            game_link = game.map_generator(user_map, rule)
            
            game_message = discord.Embed(
                color = discord.Color.green(),
            )
            game_message.add_field(name = "Enjoy the game!", value = f"Map selected: {user_map}\nGame rule selected: {rule}\n{game_link}", inline = False)
            game_message.set_footer(icon_url= author.avatar_url, text = f"Game generated by {author.display_name} ({author})")
            await ctx.send(embed = game_message)
            print("Game link sent")
            try:
                sql_insert_query = """ INSERT INTO discord_servers (server_id, server_name, map_used, rule_used, map_link)
                                                    VALUES 
                                                    (%s,%s,%s,%s,%s) AS s
                                                    ON DUPLICATE KEY UPDATE
                                                    map_used = s.map_used, server_name = s.server_name, rule_used = s.rule_used, map_link = s.map_link;"""
                map_played = (current_server_id, current_server_name, user_map, rule, game_link)
                cursor.execute(sql_insert_query, map_played)
                connection.commit()
                print(f"The following was stored in the database successfully: Server: {current_server_name}, Map: {user_map}, Rule: {rule}, Game Link: {game_link}")

            except mysql.connector.Error as error:
                print("Uh oh. Something went wrong. {}".format(error))
            finally:
                if connection.is_connected():
                    cursor.close()
                    connection.close()     

            if game_link == False:
                bad_map  = discord.Embed(
                    color = discord.Color.red(),
                )
                bad_map.add_field(name = "Uh oh!", value = "Something went wrong, please try again.", inline = False)
                await ctx.send(embed = bad_map)
                #await ctx.send("Something went wrong, please try again.") 
        else:
            bad_map  = discord.Embed(
                color = discord.Color.red(),
            )
            bad_map.add_field(name = "Uh oh!", value = "Game link could not be generated based on your input. Reference -help for help!", inline = False)
            await ctx.send(embed = bad_map)
            ctx.command.reset_cooldown(ctx)
            print("Input was wrong")

    except mysql.connector.Error as error:
        print("Uh oh. Something went wrong. {}".format(error))
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()  

@client.command(aliases = ["cg", "c"])
async def current(ctx):

    connection = mysql.connector.connect(host= db_host,
                                         database= db_database,
                                         user= db_user,
                                         password = db_password,
                                         port = db_port)

    cursor = connection.cursor(prepared=True)

    author = ctx.author
    current_server_id = str(ctx.guild.id)
    current_server_name = ctx.guild.name

 

    generatelink_message = discord.Embed(
        color = discord.Color.green(),
    )

    try:
        sql_select_query = f"SELECT map_used, rule_used, map_link from discord_servers WHERE server_id = {current_server_id};"
        cursor = connection.cursor()
        cursor.execute(sql_select_query)
        retrieve_last_map = cursor.fetchall()
        for row in retrieve_last_map:
            user_map = row[0]
            rule = row[1]
            last_link = row[2]
        print(f"The following was retrieved from the database successfully: Server: {current_server_name}, Map: {user_map}, Rule: {rule}, Game link: {last_link}")

        generatelink_message.add_field(name = "Here is the current map being played:", value = f"Current map: {user_map}\nGame rule selected: {rule}\n{last_link}", inline = False)
        generatelink_message.set_footer(icon_url= author.avatar_url, text = f"Enjoy the game {author.display_name} ({author})! ")
        await ctx.send(embed = generatelink_message)
            
        print("Game successfully retrieved")  

    except mysql.connector.Error as error:
        print("Uh oh. Something went wrong. {}".format(error))
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()  

@client.command(aliases = ["b", "bm"])
async def bookmark(ctx):

    connection = mysql.connector.connect(host= db_host,
                                         database= db_database,
                                         user= db_user,
                                         password = db_password,
                                         port = db_port)

    server_cursor = connection.cursor(prepared=True)
    bookmark_cursor = connection.cursor(prepared=True)

    author = ctx.author
    current_server_id = str(ctx.guild.id)
    current_server_name = ctx.guild.name
    bookmark_author_id = str(ctx.author.id)
    
    generatelink_message = discord.Embed(
        color = discord.Color.green(),
    )

    try:
        sql_select_query = f"SELECT map_link from discord_servers WHERE server_id = {current_server_id};"
        sql_insert_query = """ INSERT INTO bookmark (server_id, server_name, user_id, map_link)
                                                VALUES 
                                                (%s,%s,%s,%s) AS s
                                                ON DUPLICATE KEY UPDATE
                                                map_link = s.map_link;"""
        sql_count_query = f"SELECT COUNT(map_link) FROM bookmark WHERE user_id = {bookmark_author_id} and server_id = {current_server_id}"
        
        server_cursor.execute(sql_select_query)
        retrieve_last_map = server_cursor.fetchall()
        for row in retrieve_last_map:
            last_link = row[0]
        print(f"The following was retrieved from the database successfully: Server: {current_server_name}, Game link: {last_link}")

        bookmark_map = (current_server_id, current_server_name, bookmark_author_id, last_link)
        bookmark_cursor.execute(sql_insert_query, bookmark_map)
        print(f"Bookmark for {author}. The following was stored in the database successfully: Server: {current_server_name}, Server ID: {current_server_id}, User ID: {bookmark_author_id}, Game Link: {last_link}")

        bookmark_cursor.execute(sql_count_query)
        retrieve_count = bookmark_cursor.fetchall()
        for row in retrieve_count:
            bookmark_count = row[0]
        print("Count was successfuly retrieved from the database")

        connection.commit()
        generatelink_message.add_field(name = "GeoGuessr Game Bookmarked!", value = f"You bookmarked the last GeoGuessr Game that was generated:\n{last_link}", inline = False)
        if bookmark_count > 1:
            generatelink_message.set_footer(icon_url= author.avatar_url, text = f"{author.display_name} ({author}), you have {bookmark_count} bookmarks stored! ")
        else:
            generatelink_message.set_footer(icon_url= author.avatar_url, text = f"{author.display_name} ({author}), you have {bookmark_count} bookmark stored! ")
        await ctx.send(embed = generatelink_message)


    except mysql.connector.Error as error:
        print("Uh oh. Something went wrong. {}".format(error))
    finally:
        if connection.is_connected():
            bookmark_cursor.close()
            server_cursor.close()
            connection.close()  

@client.command(aliases = ["s", "saved"])
async def saves(ctx):

    connection = mysql.connector.connect(host= db_host,
                                         database= db_database,
                                         user= db_user,
                                         password = db_password,
                                         port = db_port)

    bookmark_cursor = connection.cursor(prepared=True)

    author = ctx.author
    current_server_id = str(ctx.guild.id)
    bookmark_author_id = str(ctx.author.id)
    remove_char = ["[", "]", "'"]
    
    generatelink_message = discord.Embed(
        color = discord.Color.green(),
    )

    try:
        sql_count_query = f"SELECT COUNT(map_link) FROM bookmark WHERE user_id = {bookmark_author_id} and server_id = {current_server_id}"
        sql_select_query = f"SELECT map_link from bookmark WHERE user_id = {bookmark_author_id} and server_id = {current_server_id};"
        bookmark_cursor.execute(sql_count_query)
        retrieve_count = bookmark_cursor.fetchall()
        
        for row in retrieve_count:
            bookmark_count = row[0]
        print("Count was retrieved successfuly")

        if bookmark_count > 0:
            bookmark_cursor.execute(sql_select_query)
            retrieve_maps = bookmark_cursor.fetchall()
            all_maps = [row[0] for row in retrieve_maps]
            game_list = ('\n'.join(filter(lambda i: i not in remove_char, all_maps)))
            print("Maps retrieved successfully")

            generatelink_message.add_field(name = "Bookmarked Games", value = f"Here are all your bookmarked GeoGuessr Games:\n{game_list}", inline = False)
            if bookmark_count > 1:
                generatelink_message.set_footer(icon_url= author.avatar_url, text = f"{author.display_name} ({author}), you have {bookmark_count} bookmarks stored! ")
            else:
                generatelink_message.set_footer(icon_url= author.avatar_url, text = f"{author.display_name} ({author}), you have {bookmark_count} bookmark stored! ")
            await ctx.send(embed = generatelink_message)
        else:
            generatelink_message.add_field(name = "No Bookmarked Games!", value = "You have no bookmarked games!", inline = False)
            generatelink_message.set_footer(icon_url= author.avatar_url, text = "To bookmark the latest GeoGuessr games, use -bookmark")
            await ctx.send(embed = generatelink_message)

    except mysql.connector.Error as error:
        print("Uh oh. Something went wrong. {}".format(error))
    finally:
        if connection.is_connected():
            bookmark_cursor.close()
            connection.close()  

@client.command(aliases = ["cl"])
async def clear(ctx):

    connection = mysql.connector.connect(host= db_host,
                                         database= db_database,
                                         user= db_user,
                                         password = db_password,
                                         port = db_port)

    bookmark_cursor = connection.cursor(prepared=True)

    author = ctx.author
    current_server_id = str(ctx.guild.id)
    bookmark_author_id = str(ctx.author.id)
    
    generatelink_message = discord.Embed(
        color = discord.Color.green(),
    )

    try:
        sql_count_query = f"SELECT COUNT(map_link) FROM bookmark WHERE user_id = {bookmark_author_id} and server_id = {current_server_id}"
        sql_delete_query = f"DELETE FROM bookmark WHERE user_id = {bookmark_author_id} AND server_id = {current_server_id};"
        bookmark_cursor.execute(sql_count_query)
        retrieve_count = bookmark_cursor.fetchall()

        for row in retrieve_count:
            bookmark_count = row[0]
        print("Count was retrieved successfuly")

        if bookmark_count > 0:
            bookmark_cursor.execute(sql_delete_query)
            connection.commit()
            print(f"{bookmark_count} were deleted from the database for user: {bookmark_author_id}")

            if bookmark_count > 1:
                generatelink_message.add_field(name = "Bookmarks cleared!", value = f"You successfully cleared {bookmark_count} bookmarks", inline = False)
                generatelink_message.set_footer(icon_url= author.avatar_url, text = f"{author.display_name} ({author}), you have no bookmarks anymore.")
            else:
                generatelink_message.add_field(name = "Bookmarks cleared!", value = f"You successfully cleared {bookmark_count} bookmark", inline = False)
                generatelink_message.set_footer(icon_url= author.avatar_url, text = f"{author.display_name} ({author}), you have no bookmarks anymore.")
            await ctx.send(embed = generatelink_message)
        else:
            generatelink_message.add_field(name = "No Bookmarked Games!", value = "You have no bookmarked games!", inline = False)
            generatelink_message.set_footer(icon_url= author.avatar_url, text = "To bookmark the latest GeoGuessr games, use -bookmark")
            await ctx.send(embed = generatelink_message)
    except mysql.connector.Error as error:
        print("Uh oh. Something went wrong. {}".format(error))
    finally:
        if connection.is_connected():
            bookmark_cursor.close()
            connection.close()  

@client.command(aliases = ["r", "random", "ran"])
@commands.cooldown(1,60, BucketType.guild)
async def randomgame(ctx):
    # this command generates a random GeoGuessr link with a random map and random game rule

    user_map = random.choice(list(maps))
    rule = random.choice(list(options))

    generatelink_message = discord.Embed(
        color = discord.Color.gold(),
    )
    author = ctx.author
        
    generatelink_message.add_field(name = "Thanks for the request! Generating random GeoGuessr link now!", value = f"Random map selected: {user_map}\nRandom game rule selected: {rule}", inline = False)
    generatelink_message.set_footer(icon_url= author.avatar_url, text = f"Random game requested by {author.display_name} ({author}) ")
    await ctx.send(embed = generatelink_message)
        
    print("Random game sent to generate")
        
    game_link = game.map_generator(user_map, rule)
        
    game_message = discord.Embed(
        color = discord.Color.green(),
    )
    game_message.add_field(name = "Enjoy the game!", value = f"Random map selected: {user_map}\nRandom game rule selected: {rule}\n{game_link}", inline = False)
    game_message.set_footer(icon_url= author.avatar_url, text = f"Random game generated by {author.display_name} ({author})")
    await ctx.send(embed = game_message)
    print("Random game link sent")     

    if game_link == False:
        bad_map  = discord.Embed(
            color = discord.Color.red(),
        )
        bad_map.add_field(name = "Uh oh!", value = "Something went wrong, please try again.", inline = False)
        await ctx.send(embed = bad_map)
        #await ctx.send("Something went wrong, please try again.") 

#Error Checking
@client.event
async def on_command_error(ctx,error):
    
    errorEmbed = discord.Embed(
        color = discord.Color.red()
    )

    if isinstance(error, commands.CommandNotFound):
        errorEmbed.add_field(name = "Invalid command!", value = "Please check -help for all available GeoGuessr bot commands!", inline = False)
        await ctx.send(embed = errorEmbed)
        print("Invalid command was sent")

    if isinstance(error, CommandOnCooldown):
        author = ctx.author
        errorEmbed.add_field(name = f"Slow down {ctx.message.author.display_name}!", value = f"Bot is on cooldown. Use the bot in {error.retry_after:,.2f} seconds!", inline = False)
        errorEmbed.set_footer(icon_url = author.avatar_url, text = f"Just relax, {author.display_name} ({author}) :)")
        await ctx.send(embed = errorEmbed)
    
    else: 
        print(error)
    
@geo.error
async def geo_error(ctx, error):
    errorEmbed = discord.Embed(
        color = discord.Color.red()
    )

    if isinstance(error, commands.MissingRequiredArgument):
        errorEmbed.add_field(name = "Start a GeoGuessr Game!", value = "Use this format to start a game! -geo [map] [game rule]. More information can be found with -help", inline = False )
        await ctx.send(embed = errorEmbed)
        ctx.command.reset_cooldown(ctx)
    else: 
        print(error)

@rematch.error
async def rematch_error(ctx,error):
    errorEmbed = discord.Embed(
        color = discord.Color.red()
    )
    if isinstance(error, commands.CommandInvokeError):
        errorEmbed.add_field(name = "Uh oh!", value = "Looks like the previous map configurations are not stored. Do -geo to start a game! Use -help for help with syntax.", inline = False )
        await ctx.send(embed = errorEmbed)
        ctx.command.reset_cooldown(ctx)
    else: 
        print(error)

@current.error
async def current_error(ctx,error):
    errorEmbed = discord.Embed(
        color = discord.Color.red()
    )
    if isinstance(error, commands.CommandInvokeError):
        errorEmbed.add_field(name = "Uh oh!", value = "Looks like there is no current game. Start one with the -geo command!", inline = False )
        await ctx.send(embed = errorEmbed)
        ctx.command.reset_cooldown(ctx)
    else: 
        print(error)

@bookmark.error
async def bookmark_error(ctx,error):
    errorEmbed = discord.Embed(
        color = discord.Color.red()
    )
    if isinstance(error, commands.CommandInvokeError):
        errorEmbed.add_field(name = "Uh oh!", value = "Something went wrong here, contact senn#0526.", inline = False )
        await ctx.send(embed = errorEmbed)
        ctx.command.reset_cooldown(ctx)
    else: 
        print(error)

@saves.error
async def saves(ctx,error):
    errorEmbed = discord.Embed(
        color = discord.Color.red()
    )
    if isinstance(error, commands.CommandInvokeError):
        errorEmbed.add_field(name = "Uh oh!", value = "Something went wrong here, contact senn#0526.", inline = False )
        await ctx.send(embed = errorEmbed)
        ctx.command.reset_cooldown(ctx)
    else: 
        print(error)

@clear.error
async def clear(ctx,error):
    errorEmbed = discord.Embed(
        color = discord.Color.red()
    )
    if isinstance(error, commands.CommandInvokeError):
        errorEmbed.add_field(name = "Uh oh!", value = "Something went wrong here, contact senn#0526.", inline = False )
        await ctx.send(embed = errorEmbed)
        ctx.command.reset_cooldown(ctx)
    else: 
        print(error)


def main():
    game.login()
    print("Game Installed")
    client.run(TOKEN)

if __name__ == "__main__":
    main()