class MBTI_question:

    def __init__(self, question, answers, rule):
        self.question = question
        self.answers = answers
        self.rule = rule
        
class MBTI_test:

    def __init__(self, questions: list[MBTI_question]):
        self.questions = questions

    def evaluate(self, answers):

        results = {'E': 0, 'I': 0, 'S': 0, 'N': 0, 'T': 0, 'F': 0, 'J': 0, 'P': 0}

        for i in range(len(self.questions)):
            ans = answers[i]
            quest = self.questions[i]
            direction = quest.rule[ans]
            results[direction] += 1

        ei = 'E' if results['E'] >= results['I'] else 'I'
        sn = 'S' if results['S'] >= results['N'] else 'N'
        tf = 'T' if results['T'] >= results['F'] else 'F'
        jp = 'J' if results['J'] >= results['P'] else 'P'

        return ei + sn + tf + jp


# Размерность по букве: E/I -> 0, S/N -> 1, T/F -> 2, J/P -> 3
LETTER_TO_DIMENSION = {"E": 0, "I": 0, "S": 1, "N": 1, "T": 2, "F": 2, "J": 3, "P": 3}
DIMENSION_PAIRS = [(("E", "I"), 0), (("S", "N"), 1), (("T", "F"), 2), (("J", "P"), 3)]


def _question_dimension(rule: dict) -> int:
    """Индекс шкалы (0..3) по правилу вопроса."""
    letter = next(iter(rule.values()))
    return LETTER_TO_DIMENSION.get(letter, 0)


def get_questions_for_dimensions(
    dimension_indices: list[int],
    lang: str = "ru",
) -> list[tuple["MBTI_question", int]]:

    questions = MBTI_questions_ru if lang == "ru" else MBTI_questions
    out = []
    dim_set = set(dimension_indices)
    for q in questions:
        dim = _question_dimension(q.rule)
        if dim in dim_set:
            out.append((q, dim))
    return out


def get_question_indices_and_dims_for_dimensions(
    dimension_indices: list[int],
    lang: str = "ru",
) -> list[tuple[int, int]]:
    questions = MBTI_questions_ru if lang == "ru" else MBTI_questions
    dim_set = set(dimension_indices)
    out = []
    for i, q in enumerate(questions):
        dim = _question_dimension(q.rule)
        if dim in dim_set:
            out.append((i, dim))
    return out


def get_question_by_index(index: int, lang: str = "ru") -> tuple["MBTI_question", int] | None:
    questions = MBTI_questions_ru if lang == "ru" else MBTI_questions
    if index < 0 or index >= len(questions):
        return None
    q = questions[index]
    return (q, _question_dimension(q.rule))


def evaluate_adaptive(
    questions_with_dims: list[tuple["MBTI_question", int]],
    answers: list[int],
) -> dict[int, str]:

    results = {0: {"E": 0, "I": 0}, 1: {"S": 0, "N": 0}, 2: {"T": 0, "F": 0}, 3: {"J": 0, "P": 0}}
    for (q, dim), ans in zip(questions_with_dims, answers):
        if ans not in (1, 2):
            continue
        letter = q.rule.get(ans)
        if letter and dim in results:
            pair = list(results[dim].keys())
            if letter in pair:
                results[dim][letter] += 1
    out = {}
    for dim, counts in results.items():
        if sum(counts.values()) == 0:
            continue
        pair = list(counts.keys())
        out[dim] = pair[0] if counts[pair[0]] >= counts[pair[1]] else pair[1]
    return out


mbti_questions = [
    "At a party do you:",
    "Are you more:",
    "Is it worse to:",
    "Are you more impressed by:",
    "Are you more drawn toward the:",
    "Do you prefer to work:",
    "Do you tend to choose:",
    "At parties do you:",
    "Are you more attracted to:",
    "Are you more interested in:",
    "In judging others are you more swayed by:",
    "In approaching others is your inclination to be somewhat:",
    "Are you more:",
    "Does it bother you more having things:",
    "In your social groups do you:",
    "In doing ordinary things are you more likely to:",
    "Writers should:",
    "Which appeals to you more:",
    "Are you more comfortable in making:",
    "Do you want things:",
    "Would you say you are more:",
    "In phoning do you:",
    "Facts:",
    "Are visionaries:",
    "Are you more often:",
    "Is it worse to be:",
    "Should one usually let events occur:",
    "Do you feel better about:",
    "In company do you:",
    "Common sense is:",
    "Children often do not:",
    "In making decisions do you feel more comfortable with:",
    "Are you more:",
    "Which is more admirable:",
    "Do you put more value on:",
    "Does new and non-routine interaction with others:",
    "Are you more frequently:",
    "Are you more likely to:",
    "Which is more satisfying:",
    "Which rules you more:",
    "Are you more comfortable with work that is:",
    "Do you tend to look for:",
    "Do you prefer:",
    "Do you go more by:",
    "Are you more interested in:",
    "Which is more of a compliment:",
    "Do you value in yourself more that you are:",
    "Do you more often prefer the:",
    "Are you more comfortable:",
    "Do you speak easily and at length with strangers:",
    "Are you more likely to trust your:",
    "Do you feel:",
    "Which person is more to be complimented — one of:",
    "Are you inclined more to be:",
    "Is it preferable mostly to:",
    "In relationships should most things be:",
    "When the phone rings do you:",
    "Do you prize more in yourself:",
    "Are you drawn more to:",
    "Which seems the greater error:",
    "Do you see yourself as basically:",
    "Which situation appeals to you more:",
    "Are you a person that is more:",
    "Are you more inclined to be:",
    "In writings do you prefer:",
    "Is it harder for you to:",
    "Which do you wish more for yourself:",
    "Which is the greater fault:",
    "Do you prefer the:",
    "Do you tend to be more:"
]

mbti_answers = [
    ("Interact with many, including strangers", "Interact with a few, known to you"),
    ("Realistic than speculative", "Speculative than realistic"),
    ("Have your 'head in the clouds'", "Be 'in a rut'"),
    ("Principles", "Emotions"),
    ("Convincing", "Touching"),
    ("To deadlines", "Just 'whenever'"),
    ("Rather carefully", "Somewhat impulsively"),
    ("Stay late, with increasing energy", "Leave early with decreased energy"),
    ("Sensible people", "Imaginative people"),
    ("What is actual", "What is possible"),
    ("Laws than circumstances", "Circumstances than laws"),
    ("Objective", "Personal"),
    ("Punctual", "Leisurely"),
    ("Incomplete", "Completed"),
    ("Keep abreast of others’ happenings", "Get behind on the news"),
    ("Do it the usual way", "Do it your own way"),
    ("'Say what they mean and mean what they say'", "Express things more by use of analogy"),
    ("Consistency of thought", "Harmonious human relationships"),
    ("Logical judgments", "Value judgments"),
    ("Settled and decided", "Unsettled and undecided"),
    ("Serious and determined", "Easy-going"),
    ("Rarely question that it will all be said", "Rehearse what you’ll say"),
    ("'Speak for themselves'", "Illustrate principles"),
    ("Somewhat annoying", "Rather fascinating"),
    ("A cool-headed person", "A warm-hearted person"),
    ("Unjust", "Merciless"),
    ("By careful selection and choice", "Randomly and by chance"),
    ("Having purchased", "Having the option to buy"),
    ("Initiate conversation", "Wait to be approached"),
    ("Rarely questionable", "Frequently questionable"),
    ("Make themselves useful enough", "Exercise their fantasy enough"),
    ("Standards", "Feelings"),
    ("Firm than gentle", "Gentle than firm"),
    ("The ability to organize and be methodical", "The ability to adapt and make do"),
    ("Finite", "Open-minded"),  
    ("Stimulate and energize you", "Tax your reserves"),
    ("A practical sort of person", "A fanciful sort of person"),
    ("See how others are useful", "See how others see"),
    ("To discuss an issue thoroughly", "To arrive at agreement on an issue"),
    ("Your head", "Your heart"),
    ("Contracted", "Done on a casual basis"),
    ("The orderly", "Whatever turns up"),
    ("Many friends with brief contact", "A few friends with more lengthy contact"),
    ("Facts", "Principles"),
    ("Production and distribution", "Design and research"),
    ("'There is a very logical person.'", "'There is a very sentimental person.'"),
    ("Unwavering", "Devoted"),
    ("Final and unalterable statement", "Tentative and preliminary statement"),
    ("After a decision", "Before a decision"),
    ("Speak easily and at length with strangers", "Find little to say to strangers"),
    ("Experience", "Hunch"),
    ("More practical than ingenious", "More ingenious than practical"),
    ("Clear reason", "Strong feeling"),
    ("Fair-minded", "Sympathetic"),
    ("Make sure things are arranged", "Just let things happen"),
    ("Re-negotiable", "Random and circumstantial"),
    ("Hasten to get to it first", "Hope someone else will answer"),
    ("A strong sense of reality", "A vivid imagination"),
    ("Fundamentals", "Overtones"),
    ("To be too passionate", "To be too objective"),
    ("Hard-headed", "Soft-hearted"),
    ("The structured and scheduled", "The unstructured and unscheduled"),
    ("routinized than whimsical", "whimsical than routinized"),
    ("easy to approach", "somewhat reserved"),
    ("the more literal", "the more figurative"),
    ("identify with others", "utilize others"),
    ("clarity of reason", "strength of compassion"),
    ("being indiscriminate", "being critical"),
    ("planned event", "unplanned event"),
    ("deliberate than spontaneous", "spontaneous than deliberate")
]



mbti_rules = [
    {1: 'E', 2: 'I'},  # Col 1
    {1: 'S', 2: 'N'},  # Col 2
    {1: 'T', 2: 'F'},  # Col 3
    {1: 'J', 2: 'P'},  # Col 4
    {1: 'E', 2: 'I'},  # Col 5 = EI
    {1: 'S', 2: 'N'},  # Col 6 = SN
    {1: 'T', 2: 'F'},  # Col 7 = TF
] * 10

MBTI_questions = [MBTI_question(q, a, r) for q, a, r in zip(mbti_questions, mbti_answers, mbti_rules)]


mbti_questions_ru = [
    "На вечеринке вы обычно:",
    "Вы по натуре:",
    "Что, на ваш взгляд, хуже:",
    "При принятии решений на вас сильнее влияет:",
    "Что вас больше привлекает в людях или историях:",
    "Как вы предпочитаете работать:",
    "Принимая решения, вы действуете:",
    "Находясь в большой компании, вы:",
    "Вас больше привлекают люди:",
    "Вам интереснее обсуждать:",
    "Оценивая поступки других, вы чаще опираетесь на:",
    "При первом знакомстве вы обычно ведете себя:",
    "Что больше про вас:",
    "Вас больше напрягает, когда дела:",
    "В кругу друзей и знакомых вы:",
    "Выполняя привычные дела, вы предпочитаете:",
    "Как, по-вашему, лучше выражать мысли (например, писателям):",
    "Что для вас важнее в коллективе:",
    "Вам комфортнее опираться на:",
    "Вам нравится, когда планы:",
    "В работе или учебе вы скорее:",
    "Перед тем как позвонить кому-то по телефону, вы:",
    "Для вас факты — это:",
    "Люди, склонные фантазировать и строить грандиозные планы, кажутся вам:",
    "О вас чаще говорят, что вы:",
    "Какое качество кажется вам более неприятным:",
    "Как лучше действовать в большинстве ситуаций:",
    "Вам спокойнее на душе, когда вы:",
    "В новой компании вы обычно:",
    "Опираться на здравый смысл — это:",
    "По-вашему, дети часто:",
    "Вам легче принимать решения, руководствуясь:",
    "Вы считаете себя человеком:",
    "Что вызывает у вас большее восхищение:",
    "Вы больше цените:",
    "Новые знакомства и непривычное общение обычно:",
    "Вы скорее:",
    "Наблюдая за людьми, вы чаще обращаете внимание на то:",
    "Что приносит вам большее удовлетворение в споре:",
    "Что вами сильнее управляет по жизни:",
    "Вам комфортнее, когда работа:",
    "Вы предпочитаете, чтобы вокруг вас был:",
    "Какой формат общения вам ближе:",
    "Во что вы больше верите:",
    "Что вам больше по душе:",
    "Какой комплимент вам приятнее получить:",
    "Вы больше цените в себе то, что вы:",
    "Какая позиция вам ближе в споре:",
    "Вам спокойнее:",
    "Легко ли вы заводите долгие разговоры с незнакомцами?",
    "Чему вы больше доверяете:",
    "Вы считаете себя больше:",
    "Что важнее в спорной ситуации:",
    "Кто заслуживает большего уважения:",
    "Вы предпочитаете, чтобы события:",
    "Вам нравится, когда ваши отношения с людьми:",
    "Когда звонит телефон, вы:",
    "Что вы считаете своей сильной стороной:",
    "Вас больше интересует:",
    "Какая крайность кажется вам хуже:",
    "Вы описали бы себя как человека:",
    "Какой ритм жизни вам комфортнее:",
    "Вы скорее:",
    "Вы считаете себя человеком:",
    "В книгах и фильмах вы больше цените:",
    "Вам сложнее:",
    "Какое качество вы бы хотели в себе развить:",
    "Какой недостаток вы считаете более серьезным:",
    "Вам больше по душе:",
    "Вы склонны быть:"
]

mbti_answers_ru = [
    ("Общаюсь со всеми подряд, включая незнакомцев", "Общаюсь только со своими, кого уже хорошо знаю"),
    ("Больше реалист, чем фантазёр", "Больше фантазёр, чем реалист"),
    ("Слишком сильно витать в облаках", "Безнадёжно застрять в рутине"),
    ("Логика и объективные правила", "Эмоции и человеческий фактор"),
    ("Убедительность и логичность", "Искренность и душевность"),
    ("По четкому графику и дедлайнам", "В своем темпе, по вдохновению"),
    ("Тщательно всё обдумав", "Полагаясь на импульс"),
    ("Остаетесь допоздна и заряжаетесь энергией", "Устаете и стараетесь уйти пораньше"),
    ("Разумные и практичные", "С богатым воображением и необычными идеями"),
    ("То, что происходит в реальности", "То, что могло бы произойти в теории"),
    ("Правила и законы", "Обстоятельства и мотивы человека"),
    ("Сдержанно и объективно", "Открыто и эмоционально"),
    ("Я пунктуальный человек", "Я никуда не тороплюсь"),
    ("Остаются незавершёнными", "Уже строго определены и завершены"),
    ("В курсе всех новостей и событий", "Часто узнаете новости последним"),
    ("Делать всё проверенным способом", "Искать свой собственный, новый подход"),
    ("Говорить прямо и по существу", "Использовать метафоры и аналогии"),
    ("Железная логика и последовательность мыслей", "Гармоничные отношения между людьми"),
    ("Трезвый расчет", "Свои внутренние ценности"),
    ("Четко определены и решены", "Остаются гибкими и открытыми"),
    ("Серьезны и нацелены на результат", "Расслабленны и легко адаптируетесь"),
    ("Просто звоните и говорите по ситуации", "Мысленно репетируете то, что собираетесь сказать"),
    ("Говорят сами за себя", "Нужны, чтобы иллюстрировать идеи"),
    ("Немного раздражают своей оторванностью от реальности", "Кажутся довольно увлекательными"),
    ("Хладнокровный и рассудительный", "Тёплый и отзывчивый"),
    ("Быть несправедливым", "Быть безжалостным"),
    ("Всё тщательно планировать и выбирать", "Довериться случаю и обстоятельствам"),
    ("Когда покупка уже сделана и выбор закрыт", "Когда у вас еще есть возможность выбирать"),
    ("Сами начинаете разговор", "Ждёте, пока к вам обратятся"),
    ("То, в чем редко стоит сомневаться", "То, что часто стоит ставить под сомнение"),
    ("Недостаточно помогают в практических делах", "Мало используют свою фантазию"),
    ("Объективные стандарты", "Свои и чужие чувства"),
    ("Твёрдым, чем мягким", "Мягким, чем твёрдым"),
    ("Умение все организовать и быть методичным", "Умение импровизировать на ходу"),
    ("Конкретику и законченность", "Открытость к новому и широту взглядов"),
    ("Стимулирует и заряжает энергией", "Утомляет и отнимает силы"),
    ("Человек дела и практики", "Человек идей и фантазий"),
    ("Чем они могут быть полезны в деле", "Как они смотрят на этот мир"),
    ("Разобрать проблему со всех сторон логически", "Прийти к общему согласию"),
    ("Разум", "Сердце"),
    ("Строго регламентирована и понятна", "Свободна и неформальна"),
    ("Порядок и система", "Естественный ход вещей (что подвернется)"),
    ("Много друзей и поверхностное общение", "Пара близких друзей и глубокие разговоры"),
    ("В сухие факты", "В общие принципы и идеи"),
    ("Производство и создание реального продукта", "Проектирование и генерация идей"),
    ("«Вы очень логичный человек»", "«Вы очень чуткий человек»"),
    ("Умение стоять на своём", "Умение быть преданным и заботливым"),
    ("Сделать окончательное, твёрдое заявление", "Высказать предварительную, гибкую мысль"),
    ("Когда решение уже принято", "Пока решение еще не принято (есть варианты)"),
    ("Да, легко и подолгу общаюсь", "Нет, с трудом нахожу темы для разговора"),
    ("Своему реальному опыту", "Своей интуиции (внутреннему чутью)"),
    ("Практичным, чем изобретательным", "Изобретательным, чем практичным"),
    ("Ясная логика", "Сильные чувства"),
    ("Справедливый и беспристрастный", "Понимающий и сочувствующий"),
    ("Шли по заранее составленному плану", "Складывались сами собой"),
    ("Можно было пересматривать и развивать", "Складывались стихийно и естественно"),
    ("Спешите ответить первым", "Надеетесь, что трубку возьмет кто-то другой"),
    ("Крепкую связь с реальностью", "Яркое воображение"),
    ("Основы и конкретные детали", "Скрытые смыслы и подтексты"),
    ("Быть слишком эмоциональным", "Быть слишком объективным и сухим"),
    ("Рациональным (руководствуюсь головой)", "Эмпатичным (руководствуюсь сердцем)"),
    ("Структурированный и предсказуемый", "Спонтанный и свободный от расписания"),
    ("Привыкли действовать по плану", "Склонны к внезапным порывам"),
    ("Довольно сдержанным в общении", "Легким на подъем и открытым"),
    ("Прямолинейность и буквальность", "Образность и метафоричность"),
    ("Поставить себя на место другого", "Использовать других для достижения цели"),
    ("Ясность ума и рассудка", "Глубину сострадания"),
    ("Поверхностное отношение ко всему", "Излишнюю критичность"),
    ("Спланированные заранее события", "Внезапные сюрпризы"),
    ("Действовать обдуманно", "Действовать спонтанно")
]

MBTI_questions_ru = [MBTI_question(q, a, r) for q, a, r in zip(mbti_questions_ru, mbti_answers_ru, mbti_rules)]

