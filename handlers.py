from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram import Dispatcher
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message, PhotoSize


from lexicon_en import START_MESSAGE, HELP_MESSAGE, TEST_MESSAGE


class Interview(StatesGroup):
    waiting_answers = State()

def setup_handlers(dp: Dispatcher, bot, test, questions, user_dict):
    """Регистрируем все обработчики"""
    
    @dp.message(CommandStart())
    async def process_start_command(message: Message):
        await message.answer(START_MESSAGE)

    @dp.message(Command(commands="help"))
    async def process_help_command(message: Message):
        await message.answer(HELP_MESSAGE)

    @dp.message(Command(commands="test"), StateFilter(default_state))
    async def process_test_command(message: Message, state: FSMContext):

        await state.update_data(
        current_question=0,
        answers=[],
        total_questions=70
        )

        chat_id = message.chat.id

        await message.answer(TEST_MESSAGE)   

        await ask_question(chat_id, 0, state)

    async def ask_question(chat_id: int, question_ind: int, state: FSMContext):
        q = questions[question_ind]
        q_txt = q.question
        a_option = q.answers[0]
        b_option = q.answers[1]

        await bot.send_message(chat_id, f'Question №{question_ind+1}\n\n {q_txt}\n\n 1. {a_option}\n 2. {b_option}') 
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
