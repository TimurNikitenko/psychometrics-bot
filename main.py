import os
import time
import random
from environs import Env
import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import (CallbackQuery, InlineKeyboardButton,
                           InlineKeyboardMarkup, Message, PhotoSize)
import tests


env = Env() 
env.read_env()  
        
token = env('BOT_TOKEN') 
bot = Bot(token=token)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)
user_dict: dict[int, str] = {}
test = tests.MBTI_test(tests.MBTI_questions)
questions = test.questions

class Interview(StatesGroup):
    waiting_answers = State()

@dp.message(Command(commands="start"))
async def process_start_command(message: Message):
    await message.answer(
        'Hello! This bot can analyze your personality type in two formats:\n\n'
        '1. Official psychological test - you need to answer N questions to get result\n'
        '2. Text in free form - you need to write at least 20 words, ideally about yourself (feelings, habits, hobbies, etc.)\n\n'
        'Then you get precise result if you have taken the test and supposed result if you have send text in free form. \n' 
        'For better precision you can use 2 formats consequently'
    )

@dp.message(Command(commands="help"))
async def process_help_command(message: Message):
    await message.answer(
        'For taking the psychological test you need to send command \\test\n' 
        'For completing analysis through free text form you need to send command \\text'
    )

@dp.message(Command(commands="test"), StateFilter(default_state))
async def process_test_command(message: Message, state: FSMContext):

    await state.update_data(
    current_question=0,
    answers=[],
    total_questions=70
    )

    chat_id = message.chat.id

    await message.answer(
        'In order to complete test you will need to answer 70 questions. The test will take about 15 minutes\n'
        'For each of the following questions, please answer as honestly as possible.\n' 
        'If you have not been in a situation which it alludes to, then answer as you believe you would act.' 
    )   

    await ask_question(chat_id, 0, state)

async def ask_question(chat_id: int, question_ind: int, state: FSMContext):
    q = questions[question_ind]
    q_txt = q.question
    a_option = q.answers[0]
    b_option = q.answers[1]

    await bot.send_message(chat_id, f'Question №{question_ind+1}\n\n {q_txt}\n\n Options:\n 0: {a_option}\n 1: {b_option}') 
    await state.set_state(Interview.waiting_answers)

    
@dp.message(StateFilter(Interview.waiting_answers))
async def take_answer(message: Message, state: FSMContext):
    data = await state.get_data()
    answers = data['answers']
    curr_ind = data['current_question']

    answers.append(int(message.text))

    if curr_ind + 1 < data['total_questions']:
        await state.update_data(
        current_question=curr_ind + 1,
        answers=answers
        )
        await ask_question(message.chat.id, curr_ind + 1, state)

    else:
        result = test.evaluate(answers)
        await bot.send_message(message.chat.id, 
                               f'Test is ended! \nYour personality type is {result}')
        user_dict[message.from_user.id] = {'type': result}
        await state.clear()



""" async def main():
    results = await conduct_test()

asyncio.run(main()) """

if __name__ == '__main__':
    dp.run_polling(bot)
    

     

