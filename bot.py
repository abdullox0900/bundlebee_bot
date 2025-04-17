import os
import logging
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.enums import ParseMode
import asyncio

# Загрузка переменных окружения
load_dotenv()

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=os.getenv('BOT_TOKEN'))
dp = Dispatcher()
router = Router()

# Создание инлайн-клавиатуры с кнопками меню
def get_menu_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='🟡 Launch', callback_data='launch'),
                InlineKeyboardButton(text='💡 AI Coin Architect', callback_data='ai_coin')
            ],
            [
                InlineKeyboardButton(text='💵 Wallets', callback_data='wallets')
            ],
            [
                InlineKeyboardButton(text='🚀 Bump & Volume Bots', callback_data='bump'),
                InlineKeyboardButton(text='💬 Commenter', callback_data='commenter')
            ],
            [
                InlineKeyboardButton(text='💎 Subscription', callback_data='subscription'),
                InlineKeyboardButton(text='👥 Referrals', callback_data='referrals')
            ],
            [
                InlineKeyboardButton(text='⚙️ Settings', callback_data='settings')
            ]
        ]
    )
    return keyboard

# Создание клавиатуры для кнопки "Назад" в меню помощи
def get_back_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='⬅️ Back', callback_data='back_to_main')
            ]
        ]
    )
    return keyboard

# Создание клавиатуры для страницы Bump & Volume Bots
def get_bump_volume_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='🚀 Bump Bot', url='https://t.me/repump_me_bot'),
                InlineKeyboardButton(text='📊 Volume Bot', url='https://t.me/chartup_bot')
            ],
            [
                InlineKeyboardButton(text='⬅️ Back', callback_data='back_to_main')
            ]
        ]
    )
    return keyboard

# Создание клавиатуры для страницы Wallets
def get_wallets_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='💰 Create Buy Wallets', callback_data='create_buy_wallets')
            ],
            [
                InlineKeyboardButton(text='➕ Add Existing Buy Wallets', callback_data='add_existing_wallets')
            ],
            [
                InlineKeyboardButton(text='⬅️ Back', callback_data='back_to_main')
            ]
        ]
    )
    return keyboard

# Создание клавиатуры для страницы Create Buy Wallets
def get_create_wallets_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='⬅️ Back', callback_data='back_to_wallets')
            ]
        ]
    )
    return keyboard

# Создание клавиатуры для страницы Add Existing Buy Wallets
def get_add_wallets_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='⬅️ Back', callback_data='back_to_wallets')
            ]
        ]
    )
    return keyboard

# Функция для получения текста для страницы Wallets
def get_wallets_text():
    return "💰 Create Buy Wallets used to purchase the token."

# Функция для получения текста для страницы Create Buy Wallets
def get_create_wallets_text():
    return "💰 Please enter the number of buy wallets to generate (1 to 28):"

# Функция для получения текста для страницы Add Existing Buy Wallets
def get_add_wallets_text():
    return "🔑 Please enter each Buy Wallet private key on a new line. For Example:\nKey 1\nKey 2"

# Функция для получения текста предупреждения о отсутствии кошельков
def get_no_wallets_warning():
    return "⚠️ You don't have any wallets!\n\nPlease press the button below to go to the wallets menu to create or load wallets."

# Обработчик команды /start
@router.message(Command("start"))
async def send_welcome(message: Message):
    """
    Обработчик команды /start
    """
    username = message.from_user.username or message.from_user.first_name
    
    welcome_text = get_main_text(username)

    # Отправляем сообщение с инлайн-клавиатурой и HTML-форматированием, но без превью ссылок
    await message.answer(welcome_text, reply_markup=get_menu_keyboard(), parse_mode=ParseMode.HTML, disable_web_page_preview=True)

# Функция для создания текста справки
def get_help_text():
    return """🐝 Welcome to the BundleBee help menu:

Main Menu:
🔍 Quick access to all major functions of the bot.
Use: /start

Subscription Menu:
💎 Subscribe and manage your subscription.
Use: /subscription

Wallet Menu:
💵 Create and manage wallets, and distribute SOL to buy wallets.
Use: /wallets

Coin Menu:
🟡 Create and manage your coins.
Use: /tokens

AI Architect Menu:
💡 Generate coin ideas based on market trends.
Use: /architect

Settings Menu:
⚙️ Adjust transaction fees, slippage, and tips.
Use: /settings

Referral Menu:
👥 Check out bonuses and details about our referral program.
Use: /referrals

👨‍💻 Support - <a href="https://discord.gg/bundlebee">Alpha Discord</a>

📚 For detailed information, check our <a href="https://gitbook.io/bundlebee">GitBook</a>!"""

# Обработчик команды /help
@router.message(Command("help"))
async def send_help(message: Message):
    """
    Обработчик команды /help с подробным меню помощи
    """
    help_text = get_help_text()

    # Отправляем сообщение с кнопкой "Назад" и HTML-форматированием, но без превью ссылок
    await message.answer(help_text, reply_markup=get_back_keyboard(), parse_mode=ParseMode.HTML, disable_web_page_preview=True)

# Функция для получения основного текста
def get_main_text(username):
    return f"""👋 Welcome {username}!
Get started with launching and managing your tokens, all with AI features.

🟡 Launch
Try our bot with only the Dev Wallet purchasing. Subscribe for more!

💡 AI Coin Architect
Get ready to launch coin ideas based on the most successful coins in the current 24h.

💵 Wallets
Prepare wallets for a quick and efficient token launch.

🚀 Bump & Volume Bots
Boost your coin visibility and trading volume with specialized tools.

💬 Commenter
Add comments that will be posted automatically on the token page.

💎 Subscription
Unlock the full potential with a subscription plan.

👥 Referrals
Share and earn through our referral system.

⚙️ Settings
Adjust slippage settings, gas fees for transactions, and tip amounts for Jito.

📢 Socials
Join us on <a href="https://t.me/bundlebee">Telegram</a>, <a href="https://twitter.com/bundlebee">Twitter</a> and <a href="https://youtube.com/bundlebee">Youtube</a>.

⚠️ Beta Access
BundleBee is currently in beta, if you encounter any bugs please report them in our <a href="https://discord.gg/bundlebee">Discord</a>.

❓ Need help? Type /help."""

# Функция для получения текста реферальной страницы
def get_referral_text(user_id):
    referral_link = f"https://t.me/BundleBeeBot?start=q0x{user_id}"
    
    # В реальном приложении эти данные должны быть получены из базы данных
    ref_count = 0
    ref_with_sub = 0
    bonus_percent = "20%"
    bonus_balance = "0 SOL"
    
    return f"""🐝 Share your referral link, and earn bonuses!
For each referral who purchases their first subscription, you will earn a bonus of the subscription's cost.

📢 Your Account:
🔗 Referral Link: {referral_link}

👥 Number of Referrals: {ref_count}
📊 Number of Referrals with Subscription: {ref_with_sub}

🔍 Bonus: {bonus_percent}
💰 Bonus Balance: {bonus_balance}"""

# Функция для получения текста страницы Bump & Volume Bots
def get_bump_volume_text():
    return """🐝 Our Bump & Volume bots are still under development!
They will be available in the near future, for now please use the bots below:"""

# Обработчики инлайн-кнопок
@router.callback_query(F.data)
async def process_callback(callback_query):
    """
    Обработчик инлайн-кнопок
    """
    await callback_query.answer()
    
    if callback_query.data == 'back_to_main':
        # Возврат к основному меню при нажатии на "Back"
        username = callback_query.from_user.username or callback_query.from_user.first_name
        main_text = get_main_text(username)

        # Редактируем текущее сообщение
        await callback_query.message.edit_text(
            main_text, 
            reply_markup=get_menu_keyboard(),
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True
        )
    elif callback_query.data == 'launch':
        text = "Launch section. Try our bot with only the Dev Wallet purchasing. Subscribe for more!"
        await callback_query.message.edit_text(text, reply_markup=get_menu_keyboard(), parse_mode=ParseMode.HTML)
    elif callback_query.data == 'ai_coin':
        text = "AI Coin Architect. Get ready to launch coin ideas based on the most successful coins in the current 24h."
        await callback_query.message.edit_text(text, reply_markup=get_menu_keyboard(), parse_mode=ParseMode.HTML)
    elif callback_query.data == 'wallets':
        # Показываем страницу с Wallets
        wallets_text = get_wallets_text()
        await callback_query.message.edit_text(
            wallets_text,
            reply_markup=get_wallets_keyboard(),
            parse_mode=ParseMode.HTML
        )
    elif callback_query.data == 'create_buy_wallets':
        # Показываем страницу Create Buy Wallets
        create_wallets_text = get_create_wallets_text()
        await callback_query.message.edit_text(
            create_wallets_text,
            reply_markup=get_create_wallets_keyboard(),
            parse_mode=ParseMode.HTML
        )
    elif callback_query.data == 'add_existing_wallets':
        # Показываем страницу Add Existing Buy Wallets
        add_wallets_text = get_add_wallets_text()
        await callback_query.message.edit_text(
            add_wallets_text,
            reply_markup=get_add_wallets_keyboard(),
            parse_mode=ParseMode.HTML
        )
    elif callback_query.data == 'back_to_wallets':
        # Возврат к меню Wallets
        wallets_text = get_wallets_text()
        await callback_query.message.edit_text(
            wallets_text,
            reply_markup=get_wallets_keyboard(),
            parse_mode=ParseMode.HTML
        )
    elif callback_query.data == 'bump':
        # Показываем страницу с Bump & Volume ботами
        bump_volume_text = get_bump_volume_text()
        await callback_query.message.edit_text(
            bump_volume_text, 
            reply_markup=get_bump_volume_keyboard(),
            parse_mode=ParseMode.HTML
        )
    elif callback_query.data == 'commenter':
        text = "Commenter section. Add comments that will be posted automatically on the token page."
        await callback_query.message.edit_text(text, reply_markup=get_menu_keyboard(), parse_mode=ParseMode.HTML)
    elif callback_query.data == 'subscription':
        text = "Subscription section. Unlock the full potential with a subscription plan."
        await callback_query.message.edit_text(text, reply_markup=get_menu_keyboard(), parse_mode=ParseMode.HTML)
    elif callback_query.data == 'referrals':
        # Показываем страницу с реферальной программой
        user_id = callback_query.from_user.id
        referral_text = get_referral_text(user_id)
        await callback_query.message.edit_text(
            referral_text, 
            reply_markup=get_back_keyboard(),
            parse_mode=ParseMode.HTML
        )
    elif callback_query.data == 'settings':
        # Показываем предупреждение об отсутствии кошельков для страницы Settings
        no_wallets_text = get_no_wallets_warning()
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text='⬅️ Back', callback_data='back_to_main'),
                    InlineKeyboardButton(text='💰 Wallets', callback_data='wallets')
                ]
            ]
        )
        await callback_query.message.edit_text(
            no_wallets_text,
            reply_markup=keyboard,
            parse_mode=ParseMode.HTML
        )

# Регистрация роутера
dp.include_router(router)

# Запуск бота
async def main():
    logging.info("Бот BundleBee запущен!")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())