import asyncio
import discord
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import re

scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive", "https://www.googleapis.com/auth/drive.file"]



# Form "ABC" ~Max
content_pattern1 = '(?<=\").+?(?=\"\s*~)'
author_pattern1 = '(?<=~).*(?=\s?)'

# Form Max: (")ABC(")
content_pattern2 = ':(\s*)(\"?).+(?=\")'
author_pattern2 = '.*(?=:)'

async def fetchAllData(ctx):
    channel = ctx.channel
    creds = ServiceAccountCredentials.from_json_keyfile_name("key.json", scope)
    client = gspread.authorize(creds)
    sheet = client.open('Zitate').sheet1
    async for message in channel.history:
        text = message.content
        author = message.author.name
        date = message.created_at.strftime("%d.%m.%Y")
        content = re.findall(content_pattern1, text)
        citer = re.findall(author_pattern1, text)
        if(not bool(content)):
            content = re.findall(content_pattern2, text)
            if(not bool(content)):
                content = "X"
                citer = "X"
            else:
                citer = re.findall(author_pattern2, text)
        sheet.append([text, content, citer, author, date])
    
        
