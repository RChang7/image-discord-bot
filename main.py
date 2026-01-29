import discord
from discord import Client
from config import *


def run_discord_bot():
    # Define the intents and enable them
    intents = discord.Intents.all()

    bot = Client(intents=intents)

    # elevator_music = AudioSource()

    @bot.event
    async def on_ready():
        print(f'{bot.user} is now running!')
        global general_chat 
        general_chat= bot.get_channel(general_chat_channel)


    # whenever typing_member is typing send this message
    @bot.event
    async def on_typing(channel, user, when):
        if (channel.id == general_chat_channel and user.id == typing_member):
            await channel.send(typing_message)

    # whenever someone starts playing a game from the bad games list of public shaming
    @bot.event
    async def on_presence_update(before, after):

        #extract the name of the activities into a set
        before_activities_names = set(item.name for item in before.activities if isinstance(item, discord.Activity))
        after_activities_names = set(item.name for item in after.activities if isinstance(item, discord.Activity))

        #compare the before and after sets
        odd_one_out = before_activities_names ^ after_activities_names

        for item in odd_one_out:
            #Check if the game is not None, is not in before (so they stared playing it) and it is being tracked
            if (item != None and item not in before_activities_names and item in tracked_games):
                await general_chat.send(tracked_game_message)


    # ---------Work in Progress, currently not working
    # @bot.event
    # async def on_voice_state_update(member, before, after):
    #     # Join elevator channel and play music
    #     if after.channel and after.channel.id == elevator and member.id != bot_id:
    #         voice_client = discord.utils.get(bot.voice_clients, guild=member.guild)
    # 
    #         if not voice_client:
    #             voice_client = await after.channel.connect()
    # 
    #             def play_loop(vc):
    #                 audio = discord.opus.OpusFile("elevator.opus")
    #                 vc.play(audio, after=lambda e: play_loop(vc) if e is None else None)
    # 
    #             play_loop(voice_client)
    # 
    # 
    #     # Leave when alone
    #     voice_client = discord.utils.get(bot.voice_clients, guild=member.guild)
    #     if voice_client and len(voice_client.channel.members) <= 1:
    #         await voice_client.disconnect()


    # Run the bot
    bot.run(token)



if __name__ == '__main__':
    run_discord_bot()
    pass