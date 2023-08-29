# error okay clear akunnundenki  # vech mention aakane
import os
import asyncio
from config import cfg
from script import Script
from db_functions import db
from db_functions import save_to_motor_db
from pyrogram import Client, filters, enums
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup

app = Client(
  "AutoDeleteRoBot",
  api_id=cfg.API_ID,
  api_hash=cfg.API_HASH,
  bot_token=cfg.BOT_TOKEN
)

auto_delete_tasks = {}

class temp(object):
    ME = None
    U_NAME = None
    B_NAME = None

@app.on_message(filters.command('start'))
async def start(bot, msg: Message):
    btn = InlineKeyboardMarkup([[
       InlineKeyboardButton('Add Me To Your Group', url=f'https://t.me/{temp.U_NAME}?startgroup=true')
     ],[
       InlineKeyboardButton('Updates', url='https://t.me/ZiB_BoTs'),
       InlineKeyboardButton('Support', url='https://t.me/discussatZIB')
    ]])
    reply_markup=btn            
    await msg.reply_text(
      text=Script.START_TXT.format(msg.from_user.mention),
      reply_markup=reply_markup,
      disable_web_page_preview=True,
      parse_mode=enums.ParseMode.HTML
    )

# Define a handler for the command in group chats
@app.on_message(filters.group & filters.command("autodl"))
async def autodl_group_command_handler(client, message):
    # Split the command into words
    command_parts = message.text.split()
    
    if len(command_parts) >= 2:
        try:
            # Extract the time in minutes from the second part of the command
            time_in_minutes = int(command_parts[1])
            
            # Convert minutes to seconds
            time_in_seconds = time_in_minutes * 60
            
            # Get the group ID
            group_id = message.chat.id

            # Cancel existing auto delete task if one exists
            if group_id in auto_delete_tasks:
                auto_delete_tasks[group_id].cancel()
                
            # Schedule a new auto delete task
            auto_delete_tasks[group_id] = asyncio.create_task(
                await auto_delete_messages(client, group_id, time_in_seconds)
            )
            response_text = f"Auto delete set for {time_in_minutes} minutes in this group."
            await message.reply_text(response_text)
            await db.insert_one({"group_id": group_id})
            await db.insert_one({"time_in_seconds": time_in_seconds})
            await db.insert_one({"time_in_minutes": time_in_minutes})

        except :
            response_text = "Invalid time provided."
    else:
        response_text = "No time provided."

    # Reply to the message with the response
    await message.reply_text(response_text)


# Auto delete messages after the given time
async def auto_delete_messages(bot, message):
    group_id = await db.find_one({"group_id": group_id})
    timedl = await db.find_one({"time_in_seconds": time_in_seconds})
    mtimedl = await db.find_one({"time_in_minutes": time_in_minutes})
    await asyncio.sleep(time_in_seconds)
    
    # Delete the command message
  if not message.pinned:
    await bot.delete_messages(message.chat.id, message.message_id)



# Run the client
app.run()



