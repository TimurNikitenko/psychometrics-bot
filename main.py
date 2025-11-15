import os
import time
from environs import Env
from aiogram import Bot, Dispatcher
import asyncio
from aiogram.filters import Command
from aiogram.types import Message
from aiogram import F
import tests


env = Env() 
env.read_env()  
                          
token = env('BOT_TOKEN') 
bot = Bot(token=token)
dp = Dispatcher()

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

@dp.message(Command(commands="test"))
async def process_test_command(message: Message):
    chat_id = message.chat.id

    await message.answer(
        'In order to complete test you will need to answer 70 questions. The test will take about 15 minutes\n'
        'For each of the following questions, please answer as honestly as possible.\n' 
        'If you have not been in a situation which it alludes to, then answer as you believe you would act.' 
    )   
    test = tests.MBTI_test()
    await start_test(chat_id, )



@dp.message(Command(commands="stats"))
async def process_stats_command(message: Message):
    user_id = message.from_user.id

    await message.answer(

    )

async def start_test(chat_id: int, test):
    test = test()
    await bot.send_message(chat_id=chat_id, text=question)
    time.sleep(1)



if __name__ == '__main__':
    dp.run_polling(bot)
    

     

