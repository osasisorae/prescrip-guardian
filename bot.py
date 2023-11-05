from telebot.async_telebot import AsyncTeleBot
from decouple import config
import logging
import asyncio
from database import Vectorizer
import utcnow
from telebot import types

BOT_TOKEN = config('BOT_TOKEN')

bot = AsyncTeleBot(BOT_TOKEN)
LOG = logging.getLogger(__name__)


@bot.message_handler(commands=['start'])
async def start(message):
    
    await bot.send_message(
        message.chat.id,
        "Hi, my name is script warden, I'm here to help!"
        )
    
@bot.message_handler(commands=['set_admin'])
async def set_admin(message):
    user_id = message.from_user.id
    # check db, if admin already exist
    vecotrizer = Vectorizer(user_id=user_id, folder="admins")
    check_, result = vecotrizer.get_first_admin()
    
    if check_ == 0:
        # if no admin exist, set first user as admin. Store data.
        first_name = message.from_user.first_name
        last_name = message.from_user.last_name
        username = message.from_user.username
        date_ = utcnow.get()
        data = str(first_name), str(last_name), str(username), str(date_) # make all str incase we get None
        # print(data)
        vecotrizer.save_first_admin(data=data)
        
        await bot.send_message(chat_id=user_id, text="Congrats you're an admin", parse_mode="Markdown")

    else:
        if str(user_id) == result:
            await bot.send_message(chat_id=user_id, text="You're already an admin.", parse_mode="Markdown")
        else:
            # check if user already admin
            status_, data_ = vecotrizer.get_admin()
            
            if status_ == 0:
                # If user is not an admin yet
                kyc_request = types.KeyboardButton('Share KYC Data', request_contact=True)
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                markup.add(kyc_request)
                await bot.send_message(message.chat.id, "To start KYC, please share your KYC data with us.", reply_markup=markup)
            
            else:
                await bot.send_message(message.chat.id, text="You're already an admin.", parse_mode="Markdown")
                
                # print(f"Status: {status_}, Data: {data_}")
            
            
            

@bot.message_handler(content_types=['contact'])
async def process_kyc(message):
    
    user_id = message.from_user.id
    
    vecotrizer = Vectorizer(user_id=user_id, folder='admins')
    check_, result = vecotrizer.get_first_admin()
    
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    phone_number = message.contact.phone_number
    # Process the received KYC data (phone number)
    # print(f"User ID: {user_id}, Phone Number: {phone_number}")
    response_message = f"Thank you for sharing your KYC data. Your phone number ({phone_number}) has been recorded."
    # Reset Markdown formatting using backticks
    await bot.send_message(user_id, response_message, parse_mode="Markdown")
    
    msg = f"""
        Hi, {first_name} {last_name}, with Id of {user_id} is requesting to become an admin.\n\n/Approve{user_id} or /Deny{user_id}. Call {phone_number} to verify.
    """
    await bot.send_message(chat_id=result, text=msg, parse_mode="Markdown")

@bot.message_handler(regexp=r'/Approve\d+')
async def approve_admin_request(message):
    # Extract the ID from the message
    try:
        user_id_to_approve = int(message.text.split('/Approve')[1])
        approval_date = utcnow.get()
        # Process the approval for the user with the ID user_id_to_approve
        vecotrizer = Vectorizer(user_id=user_id_to_approve, folder='admins')
        vecotrizer.save_admins(approval_date)
        # You can perform any necessary actions here
        # For example, you can update the user's role in your database or system

        await bot.send_message(message.chat.id, f"Approval granted for user with ID {user_id_to_approve}")
        await bot.send_message(chat_id=user_id_to_approve, text="Welcome to script-warden, you're now an admin", parse_mode="Markdown")
        # TODO: add more functions to admins.
        # TODO: Send message explaining admin functions.
    
    except (ValueError, IndexError):
        await bot.send_message(message.chat.id, "Invalid /Approve command format. Use /Approve<user_id>.")

@bot.message_handler(regexp=r'/Deny\d+')
async def deny_admin_request(message):
    # Extract the ID from the message
    try:
        user_id_to_deny = int(message.text.split('/Deny')[1])
        
        # Process the denial for the user with the ID user_id_to_deny
        # You can perform any necessary actions here
        # For example, you can inform the user that their request has been denied

        await bot.send_message(message.chat.id, f"Request denied for user with ID {user_id_to_deny}")
        await bot.send_message(user_id_to_deny, f"Request denied!")
    
    except (ValueError, IndexError):
        await bot.send_message(message.chat.id, "Invalid /Deny command format. Use /Deny<user_id>.")

    
@bot.message_handler(commands=['doctor'])
async def doctor(message):
    bot.register_message_handler(
        await bot.send_message(
            message.chat.id,
            f"Hi {message.chat.username}, Nice to have you here. Can I get your ID?",
            ),
        register_doctor
    )

async def register_doctor(message):
    print(message)
    pass

@bot.message_handler(commands=['pharmacist'])
async def pharmacist(message):
    pass

@bot.message_handler(commands=['user'])
async def pharmacist(message):
    pass



asyncio.run(bot.infinity_polling())