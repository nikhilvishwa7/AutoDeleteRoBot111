import asyncio
from script import Script
from db_functions import save_to_motor_db
from pyrogram import Client, filters, enums
from config import API_ID, API_HASH, BOT_TOKEN
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup

Client = app(
  "AutoDeleteRoBot",
  api_id=API_ID,
  api_hash=API_HASH,
  bot_token=BOT_TOKEN
)

auto_delete_tasks = {}

@app.on_message(filters.command('start'))
async def start(bot, msg: Message):
    btn = InlineKeyboardMarkup([[
       InlineKeyboardButton('Add Me To Your Group', url=f'https://t.me/{temp.U_name}?startgroup=true')
     ],[
       InlineKeyboardButton('Updates', url='https://t.me/ZiB_BoTs'),
       InlineKeyboardButton('Support', url='https://t.me/discussatZIB')
    ]]
    reply_markup=btn            
    await msg.reply_text(
      text=Script.START_TXT.formate(msg.from_user,mention),
      reply_markup=reply_markup,
      disable_web_page_preview=true
    )

# Define a handler for the command in group chats
@app.on_message(filters.group & filters.command("autodl"))
def autodl_group_command_handler(client, message):
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
                auto_delete_messages(client, group_id, time_in_seconds)
            )
            
            # Save the group and time in seconds to MongoDB
            save_to_motor_db(group_id, time_in_seconds, time_in_minutes)
            
            response_text = f"Auto delete set for {time_in_minutes} minutes in this group."
          message.reply_text(response_text)
        except :
            response_text = "Invalid time provided."
    else:
        response_text = "No time provided."

    # Reply to the message with the response
    message.reply_text(response_text)


# Auto delete messages after the given time
async def auto_delete_messages(client, group_id, time_in_seconds):
    await asyncio.sleep(time_in_seconds)
    
    # Delete messages in the group
    async for message in client.iter_history(group_id):
        await client.delete_messages(group_id, message.message_id)



# Run the client
app.run()


