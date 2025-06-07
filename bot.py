import os
import django
import logging
import random
import requests

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# Настройка Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "strongly_typed_wagtail.settings")
django.setup()

from home.models import UserWeight

# API ключи


# Логирование
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

# Состояния пользователя
user_states = {}

# Клавиатура
main_keyboard = ReplyKeyboardMarkup(
    [["📋 Меню", "📈 Ввести вес"], ["💡 Совет", "📅 План питания"]],
    resize_keyboard=True,
)

# Функция для запроса к OpenRouter
def ask_openrouter(prompt: str) -> str:
    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",  # Убедитесь, что переменная есть
        "Content-Type": "application/json",
        "X-Title": "HealthBot"
    }

    payload = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [{"role": "user", "content": prompt}]
    }

    try:
        response = requests.post(url, headers=headers, json=payload)

        # Логируем статус и весь текст ответа от OpenRouter
        print("=== OpenRouter Debug ===")
        print("Status code:", response.status_code)
        print("Response text:", response.text)
        print("========================")

        if response.status_code == 200:
            data = response.json()
            if "choices" in data and data["choices"]:
                return data["choices"][0]["message"]["content"].strip()
            else:
                logging.error(f"⚠️ Ответ не содержит 'choices': {data}")
                return "⚠️ ИИ не вернул совет. Возможно, ошибка в модели или токене."
        else:
            logging.error(f"⚠️ Ошибка от OpenRouter: {response.status_code} {response.text}")
            return "⚠️ Ошибка от OpenRouter. Проверь API-ключ и модель."
    except Exception as e:
        logging.error(f"❌ Сбой при обращении к OpenRouter: {str(e)}", exc_info=True)
        return "⚠️ Возникла ошибка при обращении к ИИ."



# Команды бота
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я твой бот-диетолог 🤖🥗\nЗадай вопрос или выбери кнопку ниже.",
        reply_markup=main_keyboard,
    )

async def save_weight(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_id = update.message.from_user.id
    try:
        weight = float(text.replace(",", "."))
        user_weight, created = UserWeight.objects.get_or_create(telegram_user_id=user_id)
        previous = user_weight.weight if not created else None
        user_weight.weight = weight
        user_weight.save()
        user_states[user_id] = None

        if previous:
            delta = weight - previous
            change = f"📉 Ты сбросил {abs(delta):.1f} кг!" if delta < 0 else f"📈 Ты набрал {delta:.1f} кг."
            await update.message.reply_text(
                f"✅ Вес сохранён!\n📊 Предыдущий: {previous} кг\n{change}"
            )
        else:
            await update.message.reply_text("✅ Вес сохранён! Первый результат занесён.")
    except ValueError:
        await update.message.reply_text("❗Пожалуйста, введи вес в формате числа, например: 85.3")

async def daily_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    menu = (
        "🍽️ Примерное меню на день:\n\n"
        "🥣 Завтрак: овсянка с ягодами и орехами\n"
        "🍗 Обед: куриная грудка с гречкой и овощами\n"
        "🥗 Ужин: салат с тунцом и яйцом\n"
        "🍏 Перекусы: фрукты, йогурт, орешки"
    )
    await update.message.reply_text(menu)

async def weekly_plan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    plan = "📅 План питания на неделю:\n"
    for i in range(1, 8):
        plan += f"\nДень {i}:\n- Завтрак: яйца + овощи\n- Обед: суп + мясо\n- Ужин: кефир + творог\n"
    await update.message.reply_text(plan)

motivations = [
    "💪 Ты справишься! Маленькие шаги = большой результат",
    "✨ Ты уже лучше, чем вчера",
    "🔥 Каждый день — шанс стать сильнее",
    "⏳ Терпение и упорство — ключ к успеху",
    "🌟 Ты заслуживаешь быть здоровым!",
]

async def motivation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(random.choice(motivations))

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_text = update.message.text

    if user_text == "📋 Меню":
        await daily_menu(update, context)
        return
    elif user_text == "📈 Ввести вес":
        user_states[user_id] = "WAIT_WEIGHT"
        await update.message.reply_text("Введи текущий вес, например: 85.2")
        return
    elif user_text == "💡 Совет":
        await motivation(update, context)
        return
    elif user_text == "📅 План питания":
        await weekly_plan(update, context)
        return

    if user_states.get(user_id) == "WAIT_WEIGHT":
        await save_weight(update, context)
        return

    prompt = (
        "Ты — доброжелательный эксперт по здоровью, диетам и похудению. "
        "Отвечай строго на русском языке. "
        "Дай подробный и вдохновляющий ответ: " + user_text
    )

    answer = ask_openrouter(prompt)
    await update.message.reply_text(answer)

def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("✅ Бот запущен!")
    app.run_polling()

if __name__ == "__main__":
    main()
