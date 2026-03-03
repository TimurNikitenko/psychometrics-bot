COMMANDS_EN: dict[str, str] = {
    '/start': 'Hello! 👋 I am a bot that determines your MBTI personality type using two methods:\n\n'
              '1. <b>AI Text Analysis (/text)</b> — send me your reflections, forum posts, or thoughts on any topic. The model analyzes your communication style to predict your type.\n'
              '2. <b>Classic Full Test (/test)</b> — 70 questions for the most precise result.\n\n'
              '<b>Smart tip:</b> You can start with the text analysis. If your text is highly versatile and some dimensions are hard to pinpoint, I will offer a short <b>adaptive test</b> with just a few questions to refine your type!',
    '/help': 'Here is what I can do:\n\n'
             '🧠 /text — Analyze your personality based on your text (posts, thoughts, reflections).\n'
             '📝 /test — Take the classic 70-question psychological test.\n'
             '🚪 /cancel — Exit the current testing mode.',
    '/text': 'Please paste a text for analysis (at least 20 words, but more is better!).\n\n'
             '<b>What works best:</b> Your personal reflections, forum posts (like Reddit), your opinion on a complex topic, or a story about how you make decisions.\n'
             '<i>Note: The model was trained on live internet discussions, so honest, conversational thoughts work much better than formal resumes or dry facts!</i>',
    '/test': 'You are about to take the classic MBTI test. It consists of 70 questions and takes about 10-15 minutes.\n\n'
             'Please answer as honestly as possible. Don\'t overthink it — your first genuine reaction is usually the right one. If a situation is unfamiliar, imagine how you would most likely act.',
    'wrong': 'You are not currently in testing mode. Choose /text or /test to begin.',
    '/cancel': 'Testing canceled! Let me know when you are ready to try again.'
}

COMMANDS_RU: dict[str, str] = {
    '/start': 'Привет! 👋 Я бот для определения типа личности по методике MBTI. Я умею делать это двумя способами:\n\n'
              '1. <b>ИИ-анализ текста (/text)</b> — отправь мне свои рассуждения, посты с форумов или мысли на любую тему, и нейросеть определит твой тип по стилю общения.\n'
              '2. <b>Классический тест (/test)</b> — 70 вопросов для максимально точного результата.\n\n'
              '<b>Фишка:</b> Начни с текста! Если твой характер окажется многогранным и нейросеть засомневается в некоторых шкалах, я предложу <b>короткий адаптивный тест</b> — ответишь всего на пару вопросов, и мы получим идеальный результат.',
    '/help': 'Доступные команды:\n\n'
             '🧠 /text — Узнать тип личности по твоему тексту (посты, мнения, рефлексия).\n'
             '📝 /test — Пройти полный психологический тест (70 вопросов).\n'
             '🚪 /cancel — Прервать текущий тест.',
    '/text': 'Отправь мне текст для анализа (минимум 20 слов, но чем больше — тем точнее!).\n\n'
             '<b>Что подойдет идеально:</b> твои личные размышления, длинные сообщения с форумов (в стиле Reddit), мнение на какую-то тему или рассказ о том, как ты принимаешь сложные решения.\n'
             '<i>Подсказка: нейросеть училась на живых дискуссиях, поэтому искренние рассуждения сработают в разы лучше, чем сухое резюме или перечисление фактов.</i>',
    '/test': 'Впереди классический тест MBTI. В нем 70 вопросов, прохождение займет около 10-15 минут.\n\n'
             'Отвечай максимально честно и не думай слишком долго — обычно первая реакция самая верная. Если ты не был(а) в описанной ситуации, представь, как бы ты, скорее всего, поступил(а).',
    'wrong': 'Ты сейчас не в режиме тестирования. Выбери /text или /test.',
    '/cancel': 'Тестирование прервано! Возвращайся, когда будет время.'
}

COMMANDS = {
    'ru': COMMANDS_RU,
    'en': COMMANDS_EN
}

TEXT_PROMPT_RU = 'Отправь текст для анализа (от 20 слов). Лучше всего сработают твои искренние рассуждения, мнения или посты в формате форумных дискуссий.'
TEXT_PROMPT_EN = 'Send a text for analysis (20+ words). Personal reflections, opinions, or forum-style posts work best.'

TEXT_TOO_SHORT_RU = 'Текст слишком короткий! 🤏 Для качественного анализа нужно минимум 20 слов. Расскажи чуть подробнее.'
TEXT_TOO_SHORT_EN = 'Text is too short! 🤏 I need at least 20 words for a good analysis. Please elaborate a bit more.'

TEXT_RESULT_HEADER_RU = '📊 По твоему тексту предполагаемый тип личности:'
TEXT_RESULT_HEADER_EN = '📊 Based on your text, the suggested personality type is:'

TEXT_CONFIDENCE_LABEL_RU = 'Уверенность нейросети по шкалам:'
TEXT_CONFIDENCE_LABEL_EN = 'Model confidence by dimension:'

TEXT_UNCERTAIN_RU = 'По некоторым шкалам картина не совсем однозначная. Чтобы получить 100% точный результат, рекомендую пройти полный тест: /test'
TEXT_UNCERTAIN_EN = 'The results are a bit nuanced on some dimensions. For absolute certainty, I recommend the full test: /test'

TEXT_CONFIDENCE_HIGH_RU = 'Отличный результат! Уверенность по всем шкалам высокая. Полный тест (/test) нужен только если хочешь перепроверить себя классическим методом.'
TEXT_CONFIDENCE_HIGH_EN = 'Great text! Confidence is high across all dimensions. The full /test is only needed if you want to double-check with the classic method.'

ADAPTIVE_OFFER_RU = 'Твой текст оказался очень многогранным! По некоторым шкалам значения пограничные. Давай уточним их с помощью пары вопросов?'
ADAPTIVE_OFFER_EN = 'Your text is quite nuanced! A few dimensions are on the borderline. Let\'s refine them with a couple of quick questions?'

ADAPTIVE_BUTTON_RU = '🎯 Уточнить результат (быстро)'
ADAPTIVE_BUTTON_EN = '🎯 Refine result (quick)'

ADAPTIVE_REFINED_HEADER_RU = '✨ Твой уточнённый тип личности:'
ADAPTIVE_REFINED_HEADER_EN = '✨ Your refined personality type:'

ADAPTIVE_QUESTION_WORD_RU = 'Вопрос'
ADAPTIVE_QUESTION_WORD_EN = 'Question'

TEXT_UNAVAILABLE_RU = '⚙️ Анализ по тексту сейчас временно недоступен (модель загружается или отключена). Пока можешь пройти полный /test!'
TEXT_UNAVAILABLE_EN = '⚙️ Text analysis is temporarily unavailable (the model is loading or offline). You can still take the full /test!'

# Названия полюсов шкал для вывода уверенности (предсказанный полюс — процент)
# Порядок: I/E, N/S, T/F, P/J
TRAIT_POLE_NAMES_RU = {
    ("I/E", "I"): "Интроверсия",
    ("I/E", "E"): "Экстраверсия",
    ("N/S", "N"): "Интуиция",
    ("N/S", "S"): "Ощущение",
    ("T/F", "T"): "Мышление",
    ("T/F", "F"): "Чувство",
    ("P/J", "J"): "Суждение",
    ("P/J", "P"): "Восприятие",
}
TRAIT_POLE_NAMES_EN = {
    ("I/E", "I"): "Introversion",
    ("I/E", "E"): "Extraversion",
    ("N/S", "N"): "Intuition",
    ("N/S", "S"): "Sensing",
    ("T/F", "T"): "Thinking",
    ("T/F", "F"): "Feeling",
    ("P/J", "J"): "Judging",
    ("P/J", "P"): "Perception",
}


ISTJ = 'Quiet, serious, earn success by being thorough and dependable. ' \
'Practical, matter-of-fact, realistic, and responsible. ' \
'Decide logically what should be done and work toward it steadily, regardless of distractions. ' \
'Take pleasure in making everything orderly and organized—their work, their home, their life.' \
' Value traditions and loyalty.'

ISFJ = 'Quiet, friendly, responsible, and conscientious. ' \
'Committed and steady in meeting their obligations. ' \
'Thorough, painstaking, and accurate. ' \
'Loyal, considerate, notice and remember specifics about people who are important to them, concerned with how others feel. ' \
'Strive to create an orderly and harmonious environment at work and at home.'

INFJ = 'Seek meaning and connection in ideas, relationships, and material possessions. ' \
'Want to understand what motivates people and are insightful about others. ' \
'Conscientious and committed to their firm values. Develop a clear vision about how best to serve the common good. ' \
'Organized and decisive in implementing their vision.'

INTJ = 'Have original minds and great drive for implementing their ideas and achieving their goals. ' \
'Quickly see patterns in external events and develop long-range explanatory perspectives. ' \
'When committed, organize a job and carry it through. Skeptical and independent, ' \
'have high standards of competence and performance—for themselves and others.'

ISTP = 'Tolerant and flexible, quiet observers until a problem appears, then act quickly to find workable solutions. ' \
'Analyze what makes things work and readily get through large amounts of data to isolate the core of practical problems. ' \
'Interested in cause and effect, organize facts using logical principles, value efficiency.'

ISFP = "Quiet, friendly, sensitive, and kind. Enjoy the present moment, what's going on around them. " \
"Like to have their own space and to work within their own time frame. " \
"Loyal and committed to their values and to people who are important to them. " \
"Dislike disagreements and conflicts; don't force their opinions or values on others."

INFP = 'Idealistic, loyal to their values and to people who are important to them. Want to live a life that is congruent with their values. ' \
'Curious, quick to see possibilities, can be catalysts for implementing ideas. ' \
'Seek to understand people and to help them fulfill their potential. ' \
'Adaptable, flexible, and accepting unless a value is threatened.'

INTP = 'Seek to develop logical explanations for everything that interests them. ' \
'Theoretical and abstract, interested more in ideas than in social interaction. ' \
'Quiet, contained, flexible, and adaptable. Have unusual ability to focus in depth to solve problems in their area of interest. ' \
'Skeptical, sometimes critical, always analytical.'

ESTP = 'Flexible and tolerant, take a pragmatic approach focused on immediate results. ' \
'Bored by theories and conceptual explanations; want to act energetically to solve the problem. ' \
'Focus on the here and now, spontaneous, enjoy each moment they can be active with others. ' \
'Enjoy material comforts and style. Learn best through doing.'

ESFP = 'Outgoing, friendly, and accepting. Exuberant lovers of life, people, and material comforts. ' \
'Enjoy working with others to make things happen. ' \
'Bring common sense and a realistic approach to their work and make work fun. ' \
'Flexible and spontaneous, adapt readily to new people and environments. ' \
'Learn best by trying a new skill with other people.'

ENFP = 'Warmly enthusiastic and imaginative. ' \
'See life as full of possibilities. ' \
'Make connections between events and information very quickly, and confidently proceed based on the patterns they see. ' \
'Want a lot of affirmation from others, and readily give appreciation and support. ' \
'Spontaneous and flexible, often rely on their ability to improvise and their verbal fluency.'

ENTP = 'Quick, ingenious, stimulating, alert, and outspoken. ' \
'Resourceful in solving new and challenging problems. ' \
'Adept at generating conceptual possibilities and then analyzing them strategically. ' \
'Good at reading other people. ' \
'Bored by routine, will seldom do the same thing the same way, apt to turn to one new interest after another.'

ESTJ = 'Practical, realistic, matter-of-fact. Decisive, quickly move to implement decisions. ' \
'Organize projects and people to get things done, focus on getting results in the most efficient way possible. ' \
'Take care of routine details. ' \
'Have a clear set of logical standards, systematically follow them and want others to also.' \
'Forceful in implementing their plans.'

ESFJ = 'Warmhearted, conscientious, and cooperative. Want harmony in their environment, work with determination to establish it. ' \
'Like to work with others to complete tasks accurately and on time. ' \
'Loyal, follow through even in small matters. ' \
'Notice what others need in their day-to-day lives and try to provide it. ' \
'Want to be appreciated for who they are and for what they contribute.'

ENFJ = 'Warm, empathetic, responsive, and responsible. ' \
'Highly attuned to the emotions, needs, and motivations of others. ' \
'Find potential in everyone, want to help others fulfill their potential. ' \
'May act as catalysts for individual and group growth. ' \
'Loyal, responsive to praise and criticism. Sociable, facilitate others in a group, and provide inspiring leadership.'

ENTJ = 'Frank, decisive, assume leadership readily. ' \
'Quickly see illogical and inefficient procedures and policies, develop and implement comprehensive systems to solve organizational problems. ' \
'Enjoy long-term planning and goal setting. ' \
'Usually well informed, well read, enjoy expanding their knowledge and passing it on to others. ' \
'Forceful in presenting their ideas.'

RESULT_EN: dict[str, str] = {
    'ISTJ': ISTJ,
    'INTJ': INTJ,
    'ISFJ': ISFJ,
    'INFJ': INFJ,
    'ISTP': ISTP,
    'INTP': INTP,
    'ISFP': ISFP,
    'INFP': INFP,
    'ESTJ': ESTJ,
    'ENTJ': ENTJ,
    'ESFJ': ESFJ,
    'ENFJ': ENFJ,
    'ESTP': ESTP,
    'ENTP': ENTP,
    'ESFP': ESFP,
    'ENFP': ENFP
}

ISTJ_RU = 'Спокойные, серьезные, добиваются успеха за счет основательности и надежности. ' \
'Практичные, реалистичные и ответственные. ' \
'Логически решают, что должно быть сделано, и неуклонно работают над этим, несмотря на отвлекающие факторы. ' \
'Получают удовольствие от наведения порядка и организации — своей работы, своего дома, своей жизни. Ценят традиции и верность.'

ISFJ_RU = 'Спокойные, дружелюбные, ответственные и добросовестные. ' \
'Преданные и стабильные в выполнении своих обязательств. ' \
'Тщательные, скрупулезные и точные. ' \
'Верные, внимательные, замечают и запоминают детали о людях, которые важны для них, беспокоятся о чувствах других. ' \
'Стремятся создать упорядоченную и гармоничную обстановку на работе и дома.'

INFJ_RU = 'Ищут смысл и связь в идеях, отношениях и материальных ценностях. ' \
'Хотят понять, что мотивирует людей, и обладают проницательностью в отношении других. ' \
'Добросовестные и преданные своим твердым ценностям. ' \
'Разрабатывают четкое видение того, как лучше служить общему благу. ' \
'Организованные и решительные в реализации своего видения.'

INTJ_RU = 'Обладают оригинальным мышлением и большим стремлением реализовывать свои идеи и достигать целей. ' \
'Быстро видят закономерности во внешних событиях и разрабатывают долгосрочные объяснительные перспективы. ' \
'Когда берут на себя обязательства, организуют работу и доводят ее до конца. ' \
'Скептичные и независимые, имеют высокие стандарты компетентности и производительности — как для себя, так и для других.'

ISTP_RU = 'Терпимые и гибкие, спокойные наблюдатели, пока не появится проблема, затем быстро действуют, чтобы найти рабочие решения. ' \
'Анализируют, что заставляет вещи работать, и легко просеивают большие объемы данных, чтобы выделить суть практических проблем. ' \
'Интересуются причинно-следственными связями, организуют факты с помощью логических принципов, ценят эффективность.'

ISFP_RU = 'Спокойные, дружелюбные, чувствительные и добрые. ' \
'Наслаждаются настоящим моментом, тем, что происходит вокруг них. ' \
'Любят иметь свое пространство и работать в своем собственном темпе. ' \
'Верные и преданные своим ценностям и людям, которые важны для них. ' \
'Не любят разногласия и конфликты; не навязывают свои мнения или ценности другим.'

INFP_RU = 'Идеалистичные, верные своим ценностям и людям, которые важны для них. ' \
'Хотят жить жизнью, соответствующей их ценностям. ' \
'Любознательные, быстро видят возможности, могут быть катализаторами реализации идей. ' \
'Стремятся понять людей и помочь им реализовать их потенциал. ' \
'Адаптивные, гибкие и принимающие, если только не находится под угрозой их ценность.'

INTP_RU = 'Стремятся разработать логические объяснения для всего, что их интересует. ' \
'Теоретические и абстрактные, больше интересуются идеями, чем социальным взаимодействием. ' \
'Спокойные, сдержанные, гибкие и адаптивные. ' \
'Обладают необычной способностью глубоко концентрироваться для решения проблем в своей области интересов. ' \
'Скептичные, иногда критичные, всегда аналитические.'

ESTP_RU = 'Гибкие и терпимые, придерживаются прагматичного подхода, сфокусированного на немедленных результатах. ' \
'Скучают от теорий и концептуальных объяснений; хотят энергично действовать, чтобы решить проблему. ' \
'Сосредоточены на здесь и сейчас, спонтанные, наслаждаются каждым моментом, когда могут быть активны с другими. ' \
'Наслаждаются материальными удобствами и стилем. Лучше всего учатся на практике.'

ESFP_RU = 'Общительные, дружелюбные и принимающие. Жизнелюбивые, любят людей и материальные удобства. ' \
'Наслаждаются работой с другими, чтобы воплощать идеи в жизнь. ' \
'Привносят здравый смысл и реалистичный подход в свою работу и делают работу веселой. ' \
'Гибкие и спонтанные, легко адаптируются к новым людям и обстановке. ' \
'Лучше всего учатся, пробуя новый навык с другими людьми.'

ENFP_RU = 'Теплые, энтузиастичные и обладающие богатым воображением. ' \
'Видят жизнь полной возможностей. ' \
'Быстро устанавливают связи между событиями и информацией и уверенно действуют, основываясь на увиденных закономерностях. ' \
'Нуждаются в одобрении от других и охотно выражают признательность и поддержку. ' \
'Спонтанные и гибкие, часто полагаются на свою способность к импровизации и вербальную беглость.'

ENTP_RU = 'Быстрые, изобретательные, стимулирующие, бдительные и прямолинейные. ' \
'Находчивые в решении новых и сложных проблем. ' \
'Искусны в генерации концептуальных возможностей и их последующем стратегическом анализе. ' \
'Хорошо читают других людей. ' \
'Скучают от рутины, редко делают одно и то же одинаково, склонны переключаться с одного нового интереса на другой.'

ESTJ_RU = 'Практичные, реалистичные, деловитые. ' \
'Решительные, быстро переходят к реализации решений. ' \
'Организуют проекты и людей, чтобы добиться результатов, сосредоточены на достижении результатов наиболее эффективным способом. ' \
'Заботятся о рутинных деталях. ' \
'Имеют четкий набор логических стандартов, систематически следуют им и хотят, чтобы другие тоже. ' \
'Настойчивые в реализации своих планов.'

ESFJ_RU = 'Теплые, добросовестные и склонные к сотрудничеству. ' \
'Хотят гармонии в своей среде, с решимостью работают над ее установлением. ' \
'Любят работать с другими, чтобы точно и вовремя выполнять задачи. ' \
'Верные, доводят дело до конца даже в мелочах. ' \
'Замечают, что нужно другим в их повседневной жизни, и стараются это предоставить. ' \
'Хотят, чтобы их ценили такими, какие они есть, и за их вклад.'

ENFJ_RU = 'Теплые, эмпатичные, отзывчивые и ответственные. ' \
'Чутко настроены на эмоции, потребности и мотивации других. ' \
'Видят потенциал в каждом, хотят помочь другим реализовать их потенциал. ' \
'Могут выступать катализаторами индивидуального и группового роста. ' \
'Верные, восприимчивые к похвале и критике. ' \
'Общительные, способствуют взаимодействию в группе и обеспечивают вдохновляющее лидерство.'

ENTJ_RU = 'Прямолинейные, решительные, легко берут на себя лидерство. ' \
'Быстро видят нелогичные и неэффективные процедуры и политики, разрабатывают и внедряют комплексные системы для решения организационных проблем. ' \
'Наслаждаются долгосрочным планированием и постановкой целей. ' \
'Обычно хорошо информированы, начитаны, наслаждаются расширением своих знаний и передачей их другим. ' \
'Напористые в представлении своих идей.'

RESULT_RU: dict[str, str] = {
    'ISTJ': ISTJ_RU,
    'INTJ': INTJ_RU,
    'ISFJ': ISFJ_RU,
    'INFJ': INFJ_RU,
    'ISTP': ISTP_RU,
    'INTP': INTP_RU,
    'ISFP': ISFP_RU,
    'INFP': INFP_RU,
    'ESTJ': ESTJ_RU,
    'ENTJ': ENTJ_RU,
    'ESFJ': ESFJ_RU,
    'ENFJ': ENFJ_RU,
    'ESTP': ESTP_RU,
    'ENTP': ENTP_RU,
    'ESFP': ESFP_RU,
    'ENFP': ENFP_RU
}