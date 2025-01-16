from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import requests
from button import olimpiada, telfon_raqam

import aiohttp
# API endpoint
DOMEN = "http://127.0.0.1:8000/"
API_URL = f"{DOMEN}api/v1/quiz/telegram_user/create/"

# Function to validate phone number
def is_valid_phone(phone):
    return phone.isdigit() and len(phone) in [10, 12]  # Example validation: length 10 or 12


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    telegram_id = user.id 
    url = f"{DOMEN}api/v1/quiz/telegram_user/list/check/?telegram_id={telegram_id}"

    try:
        response = requests.get(url)
        print(response.status_code)
        if response.status_code == 200:
            await update.message.reply_text(
                f"Assalom alaykum 👋 Natijangizni ko'rishingiz uchun pasdagi tugmani bosing 🔽",
                reply_markup=olimpiada()
            )
        else:
            # If the response is not 200, ask for contact information
            await update.message.reply_text(
                f"Assalom alaykum 🌟 IQMATH botiga xush kelibsiz! 🎉 Siz ro'yhatdan o'tish uchun telefon raqamingizni yuboring 📱📲",
                reply_markup=telfon_raqam()
            )
    except requests.exceptions.RequestException as e:
        await update.message.reply_text(f"Xatolik yuz berdi: {str(e)}")


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    telegram_id = update.effective_user.id


    url = F"{DOMEN}api/v1/quiz/telegram_user/result/"
    try:
        response = requests.post(url, json={"telegram_id": telegram_id})
        print(response)
        if response.status_code == 200:
            result = response.json()
           

            student = result.get("student")
            science = result.get("science")
            score = result.get("score")
            total_questions = result.get("total_questions")
            correct_answers = result.get("correct_answers")
  
            test_time = result.get("test_time")

            # Assuming 'student' is a dictionary with a 'full_name' field
            message = (
                f"🏅 Test natijalari:\n\n"
                f"👤 O'quvchi: {student}\n"
                f"🔬 Fan: {science}\n"
                f"✅ To'g'ri javoblar: {correct_answers}/{total_questions}\n"
                f"📊 Umumiy ball: {score}\n"
                f"⏱️ Test vaqti: {test_time}\n"
            )

            await update.message.reply_text(message)

        else:
            await update.message.reply_text(
                f"Siz hali Olimpiadada ishtirok etmagansiz ❗️🏅",
                
            )

    except requests.RequestException as e:
        await query.answer()
        await query.edit_message_text(f"Xatolik yuz berdi: {e}")


# Handler for received contact
async def handle_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    contact = update.message.contact
    if contact:  
        phone = contact.phone_number
        phone = phone.lstrip('+')  
        print(phone)

        telegram_id = update.effective_user.id

        payload = {
            "phone": phone,
            "telegram_id": telegram_id
        }

        try:
            response = requests.post(API_URL, json=payload)
            if response.status_code == 201 or response.status_code == 200:
                await update.message.reply_text(
                    "Tabriklaymiz! 🎉 Ro'yxatdan o'tdingiz ✅ Endi IQMATH imkoniyatlaridan to'liq foydalanishingiz mumkin! 💪📚 Natijalarni ko'rib chiqish, bilimlaringizni oshirish va o'z mahoratingizni sinash uchun har doim tayyormiz! 🚀",
                    reply_markup=olimpiada() # This will remove the keyboard
                )
            else:
                await update.message.reply_text(f"Siz hali iqmath.uz saytidan ro'yhatdan o'tmagansiz ⚠️❗")
        except requests.RequestException as e:
            await update.message.reply_text(f"Xatolik yuz berdi: {e}")
    else:
        await update.message.reply_text("Kontakt ma'lumotingizni yuboring.")

# Main function
def main():
    TOKEN = "7826335243:AAGXTZvtzJ8e8g35Hrx_Swy7mwmRPd3T7Po"  # Bot tokenni bu yerga yozing

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.CONTACT, handle_contact)) 
    app.add_handler(MessageHandler(filters.Regex(r"^🏅 Olimpiada natijalarini ko'rish 🏅$"), button_callback))
 

    app.run_polling()

if __name__ == "__main__":
    main()
