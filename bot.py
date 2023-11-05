from telebot.async_telebot import AsyncTeleBot
from decouple import config
import logging
import asyncio
from database import Vectorizer
import utcnow
from telebot import types
from messages import intro_doctor

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
                process_kyc_admin = types.KeyboardButton('Share KYC Data', request_contact=True)
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                markup.add(process_kyc_admin)
                await bot.send_message(message.chat.id, "To start KYC, please share your KYC data with us.", reply_markup=markup)
            
            else:
                await bot.send_message(message.chat.id, text="You're already an admin.", parse_mode="Markdown")
                
@bot.message_handler(content_types=['contact'])
async def process_kyc(message):

    user_id = message.from_user.id
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    phone_number = message.contact.phone_number

    vecotrizer = Vectorizer(user_id=user_id, folder='admins')
    result = vecotrizer.is_user_admin() #check if user is admin
    msg = f"""
        Hi, {first_name} {last_name}, with Id of {user_id} is requesting to become an admin.\n\n/Approve{user_id} or /Deny{user_id}. Call {phone_number} to verify.
    """
    doctor_is_admin = ('doctor' in message.reply_to_message.text)
    if result == 0:
        # Handle KYC for doctors
        # TODO: Handle KYC for pharmacists.
        response_message = f"Thank you for sharing your KYC data. Expect a call or text on ({phone_number}) from an admin."
        msg = f"Hi, {first_name} {last_name}, with Id of {user_id} is requesting to become a doctor. Call {phone_number} to verify. /ApproveDoc{user_id} or /DenyDoc{user_id}."
    else:
        # Handle KYC if doctors are admin.
        if doctor_is_admin:
            status_, admin_id_ = vecotrizer.get_first_admin()
            
            response_message = f"Thank you for sharing your KYC data. Expect a call or text on ({phone_number}) from an admin."
            msg = f"Hi, {first_name} {last_name}, with Id of {user_id} is requesting to become a doctor. Call {phone_number} to verify. /ApproveDoc{user_id} or /DenyDoc{user_id}."

        else:
            # Handle KYC for admins
            response_message = f"Thank you for sharing your KYC data. Your phone number ({phone_number}) has been recorded."
            msg = f"Hi, {first_name} {last_name}, with Id of {user_id} is requesting to become an admin. Call {phone_number} to verify. Then /ApproveAdmin{user_id} or /DenyAdmin{user_id}."

            status_, admin_id_ = vecotrizer.get_first_admin()

    await bot.send_message(user_id, response_message, parse_mode="Markdown")
    await bot.send_message(chat_id=admin_id_, text=msg, parse_mode="Markdown")

@bot.message_handler(regexp=r'/ApproveAdmin\d+')
async def approve_admin_request(message):
    # Extract the ID from the message
    try:
        user_id_to_approve = int(message.text.split('/ApproveAdmin')[1])
        approval_date = utcnow.get()
        
        # Process the approval for the user with the ID user_id_to_approve
        vecotrizer = Vectorizer(user_id=user_id_to_approve, folder='admins')
        vecotrizer.save_admins(approval_date)
        
        # Inform the user that their request has been accepted

        await bot.send_message(message.chat.id, f"Approval granted for user with ID {user_id_to_approve}")
        await bot.send_message(chat_id=user_id_to_approve, text="Welcome to script-warden, you're now an admin", parse_mode="Markdown")
        # TODO: add more functions to admins.
        # TODO: Send message explaining admin functions.
    
    except (ValueError, IndexError):
        await bot.send_message(message.chat.id, "Invalid /Approve command format. Use /Approve<user_id>.")

@bot.message_handler(regexp=r'/DenyAdmin\d+')
async def deny_admin_request(message):
    # Extract the ID from the message
    try:
        user_id_to_deny = int(message.text.split('/DenyAdmin')[1])
        
        # Inform the user that their request has been denied

        await bot.send_message(message.chat.id, f"Request denied for user with ID {user_id_to_deny}")
        await bot.send_message(user_id_to_deny, f"Request denied!")
    
    except (ValueError, IndexError):
        await bot.send_message(message.chat.id, "Invalid /Deny command format. Use /Deny<user_id>.")

@bot.message_handler(regexp=r'/ApproveDoc\d+')
async def approve_doc_request(message):
    # Extract the ID from the message
    try:
        user_id_to_approve = int(message.text.split('/ApproveDoc')[1])
        approval_date = utcnow.get()
        # Process the approval for the user with the ID user_id_to_approve
        vecotrizer = Vectorizer(user_id=user_id_to_approve, folder='doctors')
        vecotrizer.save_doctor(approval_date)
       
        # Inform the user that their request has been accepted

        await bot.send_message(message.chat.id, f"Approval granted for user with ID {user_id_to_approve}")
        await bot.send_message(chat_id=user_id_to_approve, text="Welcome to script-warden, Doctor", parse_mode="Markdown")
        # TODO: add more functions to admins.
        # TODO: Send message explaining admin functions.
    
    except (ValueError, IndexError):
        await bot.send_message(message.chat.id, "Invalid /Approve command format. Use /Approve<user_id>.")

@bot.message_handler(regexp=r'/DenyDoc\d+')
async def deny_doc_request(message):
    # Extract the ID from the message
    try:
        user_id_to_deny = int(message.text.split('/DenyDoc')[1])
        
        # Inform the user that their request has been denied

        await bot.send_message(message.chat.id, f"Request denied for user with ID {user_id_to_deny}")
        await bot.send_message(user_id_to_deny, f"Request denied!")
    
    except (ValueError, IndexError):
        await bot.send_message(message.chat.id, "Invalid /Deny command format. Use /Deny<user_id>.")
    

@bot.message_handler(commands=['doctor'])
async def doctor(message):
    # f"Hi {message.chat.username}, Nice to have you here. Can I get your ID?",
    await bot.send_message(
        message.chat.id,
        intro_doctor,
    )
    process_kyc_doctor = types.KeyboardButton('Verify Identity', request_contact=True)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(process_kyc_doctor)
    await bot.send_message(message.chat.id, "To complete your registration as a doctor and verify your identity, please click the 'Verify Identity' button to share your KYC data with us.", reply_markup=markup)


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