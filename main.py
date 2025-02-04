import asyncio
import configparser
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.types.reply_keyboard_markup import ReplyKeyboardMarkup
from aiogram.types.reply_keyboard_remove import ReplyKeyboardRemove
from aiogram.types.keyboard_button import KeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

import db 

dp = Dispatcher()

class User(StatesGroup):
    id_u = State()
    action = State()
    balance = State()

@dp.message(Command('start','new'))
async def admin(message:Message, state:FSMContext):
    await state.set_state(User.id_u)
    await message.answer("Please, enter user card's id")

@dp.message(User.id_u)
async def choose_one(message:Message, state:FSMContext):
    await state.update_data(id_u=message.text)
    await state.set_state(User.action)
    await message.answer("Please choose one",
                        reply_markup=ReplyKeyboardMarkup(
                            keyboard=[[
                                KeyboardButton(text='/set_balance'),
                                KeyboardButton(text='/get_balance'),
                                KeyboardButton(text='/cancel')
                            ]],
                            resize_keyboard=True
                        )
                    )

@dp.message(User.action, Command('get_balance'))
async def get_balance(message:Message, state:FSMContext):
    await state.update_data(action=message.text)
    data = await state.get_data()

    data['id_u'] = ''.join(filter(str.isalnum,data['id_u']))

    await state.clear()
    req = db.request("SELECT balance FROM users WHERE id_card='"+data['id_u']+"';")
    if not req:
        await message.answer("User id is invalid!")
        return

    await message.answer(f'For user who has so id-card {data['id_u']} number of bonuses: {req[0][0]}', reply_markup=ReplyKeyboardRemove())

@dp.message(User.action, Command('set_balance'))
async def set_balance(message:Message, state:FSMContext):
    await state.update_data(action=message.text)
    await state.set_state(User.balance)
    await message.answer("Enter value", reply_markup=ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='/cancel')]],resize_keyboard=True))

@dp.message(Command('cancel'))
async def close(message:Message, state:FSMContext):
    await state.clear()
    await message.answer("Canceled!", reply_markup=ReplyKeyboardRemove())

@dp.message(User.balance)
async def set_balance(message:Message, state:FSMContext):
    await state.update_data(balance=message.text)
    data = await state.get_data()
    await state.clear()

    data['id_u'] = ''.join(filter(str.isalnum,data['id_u']))
    req = db.request("SELECT balance FROM users WHERE id_card='"+data['id_u']+"';")
    print(req)
    if not req:
        await message.answer("User id is invalid!")
        return
    value = req[0][0]+int(data['balance'])
    if value<0:
        await message.answer("Not enough bonuses")
        return
    
    db.request(f'UPDATE users SET balance={value} WHERE id_card = \'{data['id_u']}\';')
    await message.answer(f'Operation is done successfully! User\'s {data['id_u']} balance: {req}->{value}')

async def main(token):    
    bot = Bot(token=token)
    print("Bot is started successfully!")
    await dp.start_polling(bot)

if __name__=='__main__':
    config = configparser.ConfigParser()
    config.read('config.ini')
    asyncio.run(main(config['telegram.bot']['bot_api']))