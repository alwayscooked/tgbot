import asyncio
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

#State for get_user_by_id
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
                                KeyboardButton(text='/close')
                            ]],
                            resize_keyboard=True
                        )
                    )

@dp.message(User.action, Command('get_balance'))
async def get_balance(message:Message, state:FSMContext):
    data = await state.get_data()
    await state.clear()
    await message.answer(f'For user who has so id-card {data['id_u']} number of bonuses: {db.select('users','balance',data['id_u'])}', reply_markup=ReplyKeyboardRemove())

@dp.message(User.action, Command('set_balance'))
async def set_balance(message:Message, state:FSMContext):
    await state.update_data(action=message.text)
    await state.set_state(User.balance)
    await message.answer("Enter value", reply_markup=ReplyKeyboardRemove())


@dp.message(User.balance)
async def set_balance(message:Message, state:FSMContext):
    await state.update_data(balance=message.text)
    data = await state.get_data()
    await state.clear()
    value = int(db.select('users','balance',data['id_u']))+int(data['balance'])
    print(value)
    if value<0:
        await message.answer("Not enough bonuses")
        return
    
    db.update('users',data['id_u'],'balance',str(value))
    await message.answer('Operation is done successfully! Current value for user '+data['id_u']+' = '+str(value))

@dp.message(User.action, Command('close'))
async def set_balance(message:Message, state:FSMContext):
    await state.clear()
    await message.answer("Canceled!", reply_markup=ReplyKeyboardRemove())

async def main(token):
    bot = Bot(token=token)
    await dp.start_polling(bot)

asyncio.run(main('nigga'))