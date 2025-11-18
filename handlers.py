from aiogram import Router, F
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.types import (CallbackQuery, InlineKeyboardButton, 
                           InlineKeyboardMarkup, Message, ReplyKeyboardRemove)

from lexicon import LEXICON_EN



def create_router(logger, test, questions, user_dict):
    router = Router()

    class Interview(StatesGroup):
        waiting_answers = State()

    button_1 = InlineKeyboardButton(
    text="1", callback_data="1"
    )
    button_2 = InlineKeyboardButton(
        text="2", callback_data="2"
    )

    # Создаем объект инлайн-клавиатуры
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_1], [button_2]])

    """ button_1 = KeyboardButton(text='1')
    button_2 = KeyboardButton(text='2')
    
    keyboard = ReplyKeyboardMarkup(keyboard=[[button_1, button_2]],
                                   resize_keyboard=True,
                                   one_time_keyboard=True) """

    @router.message(CommandStart())
    async def process_start_command(message: Message):
        await message.answer(LEXICON_EN[message.text])

    @router.message(Command(commands="help"))
    async def process_help_command(message: Message):
        await message.answer(LEXICON_EN[message.text])

    @router.message(Command(commands="test"), StateFilter(default_state))
    async def process_test_command(message: Message, state: FSMContext):

        await state.update_data(
        current_question=0,
        answers=[],
        total_questions=70
        )
        await message.answer(LEXICON_EN[message.text])   

        await ask_question(message, 0, state)
 
    async def ask_question(message, question_ind: int, state: FSMContext):
        q = questions[question_ind]
        q_txt = q.question
        a_option = q.answers[0]
        b_option = q.answers[1]

        await message.bot.send_message(chat_id=message.chat.id, text=f'Question №{question_ind+1}\n\n {q_txt}\n\n 1. {a_option}\n 2. {b_option}', 
                                       reply_markup=keyboard) 
        await state.set_state(Interview.waiting_answers)

        
    @router.callback_query(F.data.in_(["1", "2"]) and StateFilter(Interview.waiting_answers))
    async def take_answer(callback: CallbackQuery, state: FSMContext):

        data = await state.get_data()
        answers = data['answers']
        curr_ind = data['current_question']

    
        if callback.data.isdigit() and int(callback.data) in (1, 2):
            answers.append(int(callback.data))

            if curr_ind + 1 < data['total_questions']:
                await state.update_data(
                current_question=curr_ind + 1,
                answers=answers
                )
                await callback.answer(text='Answer is accepted!')
                await ask_question(callback.message, curr_ind + 1, state)

            else:
                result = test.evaluate(answers)
                await callback.answer(text='Answer is accepted!')
                await callback.message.answer(
                                    f'Test is ended! \nYour personality type is {result}\n\n'\
                                        f'Your answers: {answers}', 
                                    reply_markup=ReplyKeyboardRemove()
                                    )
                
                user_dict[callback.from_user.id] = {'type': result}
                await state.clear()

        else:
            logger.info('User entered incorrect value')
            await callback.message.answer(
                                    'Please enter correct value (1 or 2)'
                                    )

    return router


