import discord
import requests
import json

headers = {
    'Accept': 'application/json',
    'Authorization': 'Bot YOUR_DISCORD_TOKEN_HERE'
}

inviteList = []
inviteListNew = []
guildID = "YOUR_GUILD_ID_HERE"
channelID = YOUR_CHANNEL_ID_HERE
firstRun = 0
   
class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')
        print('Gathering Invites')

        theguild = requests.get('https://discordapp.com/api/v6/guilds/' + guildID + '/invites', headers=headers)
        guildResponse = theguild.content
        guildOutput = json.loads(guildResponse)
        print(str(guildOutput))
        
        for invite in guildOutput:
            invitee = invite['inviter']['username']
            invCount = invite['uses']
            
            inviteList.append((invite['code'], invitee, invCount))
        print (inviteList)
        invite = ""
        print('Gathering Invites Completed')
        
    async def on_member_join(self, member):
            print("A new member has joined: " + str(member.name))
            global firstRun 
            global inviteList
            global inviteListNew
            #channel = member.guild.system_channel
            channel = client.get_channel(channelID)
            
            if firstRun == 1:
                print("First Run Check: It is NOT the First Run")
                inviteList = inviteListNew[:]
                inviteListNew = []
                
                theguild = requests.get('https://discordapp.com/api/v6/guilds/' + guildID + '/invites', headers=headers)
                guildResponse = theguild.content
                guildOutput = json.loads(guildResponse)
                
                for invite in guildOutput:
                    invitee = invite['inviter']['username']
                    invCount = invite['uses']
                    
                    inviteListNew.append((invite['code'], invitee, invCount))
                    
                print("Updated Invite Code Uses")
                for a, b in zip(inviteList, inviteListNew):
                    if a != b:
                        print("Updated Invite Code was Detected")
                        await channel.send(str(member.name) + " joined\nInvite Code: " + str(b[0]) + "\nCreated by " + str(b[1]) + "\nUsed " + str(b[2]) + " times")                        
                        badInvite = 0

                invite = ""

            else:
                print("First Run Check: It IS the First Run")
                theguild = requests.get('https://discordapp.com/api/v6/guilds/' + guildID + '/invites', headers=headers)
                guildResponse = theguild.content
                guildOutput = json.loads(guildResponse)
                
                for invite in guildOutput:
                    invitee = invite['inviter']['username']
                    invCount = invite['uses']
                    
                    inviteListNew.append((invite['code'], invitee, invCount))
                print("Updated Invite Code Uses")
                    
                for a, b in zip(inviteList, inviteListNew):
                    if a != b:
                        print("Updated Invite Code was Detected")
                        #await channel.send(str(a) + "is different from" + str(b))
                        await channel.send(str(member.name) + " joined\nInvite Code: " + str(b[0]) + "\nCreated by: " + str(b[1]) + "\nUsed " + str(b[2]) + " times")
                        badInvite = 0
                        
                inviteList = inviteListNew[:]
                invite = ""
                firstRun = 1 
                             
            if badInvite != 0:
                await channel.send("I cannot figure out how " + str(member.name) + " joined the server.")
            print("On Member Code Execution Completed")

client = MyClient()
client.run('YOUR_BOT_TOKEN_HERE')    

    
