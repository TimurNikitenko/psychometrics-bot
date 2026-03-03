import asyncio
import logging
from aiogram import Router, F
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.types import (CallbackQuery, InlineKeyboardButton,
                           InlineKeyboardMarkup, Message, ReplyKeyboardRemove)

from lexicon import (
    COMMANDS,
    RESULT_RU,
    RESULT_EN,
    TEXT_PROMPT_RU,
    TEXT_PROMPT_EN,
    TEXT_TOO_SHORT_RU,
    TEXT_TOO_SHORT_EN,
    TEXT_RESULT_HEADER_RU,
    TEXT_RESULT_HEADER_EN,
    TEXT_CONFIDENCE_LABEL_RU,
    TEXT_CONFIDENCE_LABEL_EN,
    TRAIT_POLE_NAMES_RU,
    TRAIT_POLE_NAMES_EN,
    TEXT_UNCERTAIN_RU,
    TEXT_UNCERTAIN_EN,
    TEXT_CONFIDENCE_HIGH_RU,
    TEXT_CONFIDENCE_HIGH_EN,
    TEXT_UNAVAILABLE_RU,
    TEXT_UNAVAILABLE_EN,
    ADAPTIVE_OFFER_RU,
    ADAPTIVE_OFFER_EN,
    ADAPTIVE_BUTTON_RU,
    ADAPTIVE_BUTTON_EN,
    ADAPTIVE_REFINED_HEADER_RU,
    ADAPTIVE_REFINED_HEADER_EN,
    ADAPTIVE_QUESTION_WORD_RU,
    ADAPTIVE_QUESTION_WORD_EN,
)
import testing_utils
from translator import prepare_text_for_mbti

logger = logging.getLogger(__name__)

ADAPTIVE_CONFIDENCE_THRESHOLD = 0.75


def create_router(mbti_clf=None, mbti_clf_container=None):
    if mbti_clf_container is not None:
        _get_clf = lambda: mbti_clf_container[0] if mbti_clf_container else None
    else:
        _get_clf = lambda: mbti_clf

    router = Router()

    user_language: dict[int, str]

    class Interview(StatesGroup):
        waiting_answers = State()

    class WaitingText(StatesGroup):
        waiting_text = State()

    class AdaptiveInterview(StatesGroup):
        waiting_answers = State()

    choice_button_1 = InlineKeyboardButton(
    text="1", callback_data="1"
    )
    
    choice_button_2 = InlineKeyboardButton(
        text="2", callback_data="2"
    )

    choice_keyboard = InlineKeyboardMarkup(inline_keyboard=[[choice_button_1], [choice_button_2]])

    language_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Русский", callback_data="lang_ru")],
    [InlineKeyboardButton(text="English", callback_data="lang_en")]
        ])

    user_language = {}

    @router.message(Command("language"))
    async def cmd_language(message: Message):

        await message.answer(
            "🌍 Выбери язык для общения и прохождения тестов / Choose your preferred language:", 
            reply_markup=language_keyboard
        )

    @router.callback_query(F.data.startswith("lang_"))
    async def set_language(callback: CallbackQuery):
        lang_code = callback.data.split("_")[1]
        user_id = callback.from_user.id
        
        user_language[user_id] = lang_code
        
        responses = {
            'ru': "🇷🇺 Отлично! Язык изменен на русский. Отправь /help, чтобы посмотреть доступные команды.",
            'en': "🇬🇧 Awesome! Language switched to English. Send /help to see available commands."
        }
        await callback.message.edit_text(responses[lang_code])

    @router.message(CommandStart())
    async def process_start_command(message: Message):

        if message.from_user.id not in user_language:
            user_language[message.from_user.id] = 'ru'
        commands = COMMANDS[user_language[message.from_user.id]]

        await message.answer(commands[message.text])

    @router.message(Command(commands="help"))
    async def process_help_command(message: Message):
        commands = COMMANDS[user_language[message.from_user.id]]
        await message.answer(commands[message.text])

    @router.message(Command(commands="test"), StateFilter(default_state))
    async def process_test_command(message: Message, state: FSMContext):

        test = testing_utils.MBTI_test(testing_utils.MBTI_questions_ru if user_language[message.from_user.id] == 'ru' else testing_utils.MBTI_questions)
        questions = test.questions
        commands = COMMANDS[user_language[message.from_user.id]]

        await state.update_data(
        test=test,
        questions=questions,
        current_question=0,
        answers=[],
        total_questions=70,
        user_language = user_language
        )
        await message.answer(commands[message.text])   

        await ask_question(message, user_language[message.from_user.id], 0, state)
 
    @router.message(Command(commands="cancel"), StateFilter(default_state))
    async def process_cancel_outside_command(message: Message, state: FSMContext):
        commands = COMMANDS[user_language[message.from_user.id]]
        await message.answer(commands['wrong'])

    @router.message(Command(commands="cancel"), StateFilter(Interview.waiting_answers))
    async def process_cancel_command(message: Message, state: FSMContext):
        await state.clear()
        commands = COMMANDS[user_language[message.from_user.id]]
        await message.answer(commands[message.text])

    @router.message(Command(commands="cancel"), StateFilter(WaitingText.waiting_text))
    async def process_cancel_text(message: Message, state: FSMContext):
        await state.clear()
        lang = user_language.get(message.from_user.id, "ru")
        msg = "Анализ текста отменен. 🛑 Возвращайся, когда захочешь поделиться мыслями!" if lang == "ru" else "Text analysis cancelled. 🛑 Come back whenever you're ready to share your thoughts!"
        await message.answer(msg)

    @router.message(Command(commands="cancel"), StateFilter(AdaptiveInterview.waiting_answers))
    async def process_cancel_adaptive(message: Message, state: FSMContext):
        await state.clear()
        lang = user_language.get(message.from_user.id, "ru")
        msg = "Уточняющий тест прерван. 🛑 Твой предварительный результат сохранен выше." if lang == "ru" else "Refinement test cancelled. 🛑 Your preliminary result is saved above."
        await message.answer(msg)

    @router.message(Command(commands="text"), StateFilter(default_state))
    async def process_text_command(message: Message, state: FSMContext):
        if message.from_user.id not in user_language:
            user_language[message.from_user.id] = "ru"
        lang = user_language[message.from_user.id]
        if _get_clf() is None:
            await message.answer(TEXT_UNAVAILABLE_RU if lang == "ru" else TEXT_UNAVAILABLE_EN)
            return
        prompt = TEXT_PROMPT_RU if lang == "ru" else TEXT_PROMPT_EN
        await message.answer(prompt)
        await state.set_state(WaitingText.waiting_text)

    @router.message(F.text, StateFilter(WaitingText.waiting_text))
    async def process_user_text(message: Message, state: FSMContext):
        clf = _get_clf()
        if not message.text or clf is None:
            await state.clear()
            if not message.text:
                return
            lang = user_language.get(message.from_user.id, "ru")
            await message.answer(TEXT_UNAVAILABLE_RU if lang == "ru" else TEXT_UNAVAILABLE_EN)
            return
        text = message.text.strip()
        word_count = len(text.split())
        lang = user_language.get(message.from_user.id, "ru")
        if word_count < 20:
            too_short = TEXT_TOO_SHORT_RU if lang == "ru" else TEXT_TOO_SHORT_EN
            await message.answer(too_short)
            return

        text_for_model = prepare_text_for_mbti(text)
        if text_for_model != text:
            logger.info(
                "MBTI input: original -> translation: %s -> %s",
                text[:300] + ("..." if len(text) > 300 else ""),
                text_for_model[:300] + ("..." if len(text_for_model) > 300 else ""),
            )
        try:
            mbti_type, conf = await asyncio.to_thread(clf.predict, text_for_model, True)
        except Exception as e:
            logger.exception("MBTI prediction failed: %s", e)
            await message.answer("Упс! 🛠 Произошла ошибка при анализе текста. Возможно, он слишком длинный или содержит необычные символы. Попробуй отправить другой текст." if lang == "ru" else "Oops! 🛠 An error occurred during analysis. The text might be too long or contain unusual characters. Please try a different text.")
            await state.clear()
            return

        logger.info("MBTI prediction: type=%s confidence=%s", mbti_type, conf)

        description = RESULT_EN if lang == "en" else RESULT_RU
        header = TEXT_RESULT_HEADER_RU if lang == "ru" else TEXT_RESULT_HEADER_EN
        conf_label = TEXT_CONFIDENCE_LABEL_RU if lang == "ru" else TEXT_CONFIDENCE_LABEL_EN
        desc_block = description.get(mbti_type, "")

        confidence_line = ""
        low_conf_dims = []
        first_letters = ("I", "N", "T", "P")
        second_letters = ("E", "S", "F", "J")
        if conf and len(mbti_type) >= 4:
            traits = ("I/E", "N/S", "T/F", "P/J")
            names = TRAIT_POLE_NAMES_RU if lang == "ru" else TRAIT_POLE_NAMES_EN
            lines = []
            for i, t in enumerate(traits):
                p = conf.get(t, 0.5)
                letter = mbti_type[i]
                if letter == second_letters[i]:
                    confidence_pct = p * 100
                else:
                    confidence_pct = (1 - p) * 100
                name = names.get((t, letter), letter)
                lines.append(f"• {name} — {confidence_pct:.0f}%")
                if confidence_pct / 100.0 < ADAPTIVE_CONFIDENCE_THRESHOLD:
                    low_conf_dims.append(i)
            confidence_line = f"\n\n{conf_label}:\n" + "\n".join(lines)

        if low_conf_dims:
            footer = "\n\n" + (ADAPTIVE_OFFER_RU if lang == "ru" else ADAPTIVE_OFFER_EN)
            high_conf_msg = ""
        else:
            footer = ""
            high_conf_msg = "\n\n" + (TEXT_CONFIDENCE_HIGH_RU if lang == "ru" else TEXT_CONFIDENCE_HIGH_EN) if conf else ""

        if low_conf_dims:
            await state.update_data(
                adaptive_text_type=mbti_type,
                adaptive_low_conf_dims=low_conf_dims,
                adaptive_lang=lang,
            )
            btn_text = ADAPTIVE_BUTTON_RU if lang == "ru" else ADAPTIVE_BUTTON_EN
            adaptive_kbd = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text=btn_text, callback_data="adaptive_start")]
            ])
            await message.answer(
                f"{header}: <b>{mbti_type}</b>\n\n{desc_block}{confidence_line}{footer}",
                reply_markup=adaptive_kbd,
            )
        else:
            await message.answer(
                f"{header}: <b>{mbti_type}</b>\n\n{desc_block}{confidence_line}{high_conf_msg}",
                reply_markup=ReplyKeyboardRemove(),
            )
            await state.clear()

    @router.callback_query(F.data == "adaptive_start", StateFilter(WaitingText.waiting_text))
    async def start_adaptive(callback: CallbackQuery, state: FSMContext):
        data = await state.get_data()
        text_type = data.get("adaptive_text_type", "INFP")
        low_conf_dims = data.get("adaptive_low_conf_dims", [])
        lang = data.get("adaptive_lang", "ru")
        if not low_conf_dims:
            await callback.answer()
            await state.clear()
            return
        indices_dims = testing_utils.get_question_indices_and_dims_for_dimensions(low_conf_dims, lang)
        await state.update_data(
            adaptive_question_indices_dims=indices_dims,
            adaptive_answers=[],
            adaptive_current=0,
            adaptive_text_type=text_type,
            adaptive_lang=lang,
        )
        await state.set_state(AdaptiveInterview.waiting_answers)
        await callback.answer()
        await _ask_adaptive_question(callback.message, 0, indices_dims, lang, state)

    async def _ask_adaptive_question(
        message: Message, idx: int, indices_dims: list[tuple[int, int]], lang: str, state: FSMContext
    ):
        if idx >= len(indices_dims):
            return
        q_idx, _ = indices_dims[idx]
        q_and_dim = testing_utils.get_question_by_index(q_idx, lang)
        if not q_and_dim:
            return
        q, _ = q_and_dim
        word = ADAPTIVE_QUESTION_WORD_RU if lang == "ru" else ADAPTIVE_QUESTION_WORD_EN
        text = (f"🎯 <b>{word} {idx + 1}/{len(indices_dims)}</b>\n\n"
                f"<b>{q.question}</b>\n\n"
                f"1️⃣ {q.answers[0]}\n"
                f"2️⃣ {q.answers[1]}")
        await message.answer(text, reply_markup=choice_keyboard)

    @router.callback_query(F.data.in_(["1", "2"]), StateFilter(AdaptiveInterview.waiting_answers))
    async def take_adaptive_answer(callback: CallbackQuery, state: FSMContext):
        data = await state.get_data()
        indices_dims = data.get("adaptive_question_indices_dims", [])
        answers = data.get("adaptive_answers", [])
        current = data.get("adaptive_current", 0)
        text_type = data.get("adaptive_text_type", "INFP")
        lang = data.get("adaptive_lang", "ru")

        if not callback.data.isdigit() or int(callback.data) not in (1, 2):
            await callback.answer()
            return
        answers = answers + [int(callback.data)]
        current += 1

        if current < len(indices_dims):
            await state.update_data(adaptive_answers=answers, adaptive_current=current)
            await callback.answer()
            await _ask_adaptive_question(callback.message, current, indices_dims, lang, state)
            return

        questions_with_dims = []
        for (q_idx, dim) in indices_dims:
            q_and_dim = testing_utils.get_question_by_index(q_idx, lang)
            if q_and_dim:
                questions_with_dims.append(q_and_dim)
        adaptive_result = testing_utils.evaluate_adaptive(questions_with_dims, answers)
        type_chars = list(text_type) if len(text_type) >= 4 else ["I", "N", "F", "P"]
        for dim, letter in adaptive_result.items():
            if dim < 4:
                type_chars[dim] = letter
        refined_type = "".join(type_chars)

        description = RESULT_EN if lang == "en" else RESULT_RU
        header = ADAPTIVE_REFINED_HEADER_RU if lang == "ru" else ADAPTIVE_REFINED_HEADER_EN
        desc_block = description.get(refined_type, "")
        await callback.answer()
        await callback.message.answer(
            f"{header}: <b>{refined_type}</b>\n\n{desc_block}",
            reply_markup=ReplyKeyboardRemove(),
        )
        await state.clear()

    async def ask_question(message: Message, lang, question_ind: int, state: FSMContext):
        data = await state.get_data()
        questions = data['questions']
        q = questions[question_ind]
        q_txt = q.question
        a_option = q.answers[0]
        b_option = q.answers[1]

        word = ('Question', 'Вопрос')[lang == 'ru']
        await message.bot.send_message(
            chat_id=message.chat.id, 
            text=f'📝 <b>{word} {question_ind+1} из {data["total_questions"]}</b>\n\n'
                f'<b>{q_txt}</b>\n\n'
                f'1️⃣ {a_option}\n'
                f'2️⃣ {b_option}', 
            reply_markup=choice_keyboard
        ) 
        await state.set_state(Interview.waiting_answers)

        
    @router.callback_query(F.data.in_(["1", "2"]) and StateFilter(Interview.waiting_answers))
    async def take_answer(callback: CallbackQuery, state: FSMContext):

        logger.info(f'Пользователь выбрал {callback.data} вариант')

        data = await state.get_data()
        answers = data['answers']
        curr_ind = data['current_question']
        test = data['test']

        if callback.data.isdigit() and int(callback.data) in (1, 2):
            answers.append(int(callback.data))

            if curr_ind + 1 < data['total_questions']:
                await state.update_data(
                current_question=curr_ind + 1,
                answers=answers
                )
                await callback.answer()
                await ask_question(callback.message, user_language[callback.from_user.id], curr_ind + 1, state)

            else:
                result = test.evaluate(answers)

                description = RESULT_EN if user_language[callback.from_user.id] == 'en' else RESULT_RU
                w1, w2 = ('Тест завершен! \nВаш тип личности', 'Описание типа:') if user_language[callback.from_user.id] == 'ru' else \
                ('Test is ended! \nYour personality type', 'Type description:')
                await callback.answer()
                await callback.message.answer(
                                    f'{w1} {result}\n\n'\
                                        f'{w2}\n\n{description[result]}', 
                                    reply_markup=ReplyKeyboardRemove()
                                    )
                
                await state.clear()

        else:
            logger.info('User entered incorrect value')
            lang = user_language.get(callback.from_user.id, "ru")
            error_msg = 'Пожалуйста, используй кнопки 1 или 2 для ответа. 👇' if lang == 'ru' else 'Please use buttons 1 or 2 to answer. 👇'
            await callback.message.answer(error_msg)
  
    return router


