from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command, CommandStart
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from database import User, Item
from config import settings

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message, session: AsyncSession):
    user = await session.scalar(select(User).where(User.telegram_id == message.from_user.id))
    if not user:
        session.add(User(telegram_id=message.from_user.id))
        await session.commit()
    
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Каталог", callback_data="catalog")],
        [InlineKeyboardButton(text="Профиль", callback_data="profile")]
    ])
    await message.answer("Добро пожаловать в ScniseShop!", reply_markup=kb)

@router.message(Command("admin"))
async def cmd_admin(message: Message, session: AsyncSession):
    if message.from_user.id != settings.admin_id:
        return
    
    users = (await session.scalars(select(User))).all()
    items = (await session.scalars(select(Item))).all()
    
    text = f"Панель администратора\nПользователей в базе: {len(users)}\nТоваров в каталоге: {len(items)}"
    await message.answer(text)

@router.callback_query(F.data == "profile")
async def show_profile(callback: CallbackQuery, session: AsyncSession):
    user = await session.scalar(select(User).where(User.telegram_id == callback.from_user.id))
    text = f"Ваш профиль:\nID: {user.telegram_id}\nБаланс: {user.balance} руб."
    
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Пополнить баланс (+500р)", callback_data="deposit_test")],
        [InlineKeyboardButton(text="Назад", callback_data="back_to_main")]
    ])
    await callback.message.edit_text(text, reply_markup=kb)

@router.callback_query(F.data == "deposit_test")
async def deposit_test(callback: CallbackQuery, session: AsyncSession):
    user = await session.scalar(select(User).where(User.telegram_id == callback.from_user.id))
    user.balance += 500.0
    await session.commit()
    
    text = f"Ваш профиль:\nID: {user.telegram_id}\nБаланс: {user.balance} руб."
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Пополнить баланс (+500р)", callback_data="deposit_test")],
        [InlineKeyboardButton(text="Назад", callback_data="back_to_main")]
    ])
    await callback.message.edit_text(text, reply_markup=kb)

@router.callback_query(F.data == "catalog")
async def show_catalog(callback: CallbackQuery, session: AsyncSession):
    items = (await session.scalars(select(Item))).all()
    if not items:
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Назад", callback_data="back_to_main")]
        ])
        await callback.message.edit_text("Каталог пуст.", reply_markup=kb)
        return
    
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=item.name, callback_data=f"item_{item.id}")] for item in items
    ])
    kb.inline_keyboard.append([InlineKeyboardButton(text="Назад", callback_data="back_to_main")])
    await callback.message.edit_text("Выберите товар:", reply_markup=kb)

@router.callback_query(F.data.startswith("item_"))
async def show_item(callback: CallbackQuery, session: AsyncSession):
    item_id = int(callback.data.split("_")[1])
    item = await session.get(Item, item_id)
    
    if not item:
        await callback.answer("Товар не найден.")
        return
    
    text = f"Товар: {item.name}\nЦена: {item.price} руб.\n\nОписание: {item.description}"
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Купить", callback_data=f"buy_{item.id}")],
        [InlineKeyboardButton(text="Назад в каталог", callback_data="catalog")]
    ])
    await callback.message.edit_text(text, reply_markup=kb)

@router.callback_query(F.data.startswith("buy_"))
async def buy_item(callback: CallbackQuery, session: AsyncSession):
    item_id = int(callback.data.split("_")[1])
    item = await session.get(Item, item_id)
    user = await session.scalar(select(User).where(User.telegram_id == callback.from_user.id))
    
    if not item:
        await callback.answer("Товар не найден.", show_alert=True)
        return
    
    if user.balance < item.price:
        await callback.answer("Недостаточно средств на балансе! Пополните его в профиле.", show_alert=True)
        return
    
    user.balance -= item.price
    await session.commit()
    
    text = f"Успешная покупка!\nВы приобрели: {item.name}\nСписано: {item.price} руб.\n\nВаш цифровой ключ:\n`SCNISE-SHOP-TEST-KEY-777`"
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="В каталог", callback_data="catalog")]
    ])
    await callback.message.edit_text(text, reply_markup=kb, parse_mode="Markdown")

@router.callback_query(F.data == "back_to_main")
async def back_to_main(callback: CallbackQuery):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Каталог", callback_data="catalog")],
        [InlineKeyboardButton(text="Профиль", callback_data="profile")]
    ])
    await callback.message.edit_text("Добро пожаловать в ScniseShop!", reply_markup=kb)