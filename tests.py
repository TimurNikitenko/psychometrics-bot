import random

class MBTI_question:

    def __init__(self, question, answers, rule):
        self.question = question
        self.answers = answers
        self.rule = rule
        
class MBTI_test:

    def __init__(self, questions: list[MBTI_question]):
        self.questions = questions
        self.user_answers = []

    def evaluate(self):

        results = {'E': 0, 'I': 0, 'S': 0, 'N': 0, 'T': 0, 'F': 0, 'J': 0, 'P': 0}

        for i in range(len(self.questions)):
            ans = self.user_answers[i]
            quest = self.questions[i]
            direction = quest.rule[ans]
            results[direction] += 1

        ei = 'E' if results['E'] >= results['I'] else 'I'
        sn = 'S' if results['S'] >= results['N'] else 'N'
        tf = 'T' if results['T'] >= results['F'] else 'F'
        jp = 'J' if results['J'] >= results['P'] else 'P'

        return ei + sn + tf + jp

    def add_answer(self, answer):
        self.user_answers.append(answer)


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
    ("Finite", "Open-minded"),  # PDF said "infinite" but it's a known typo → original MBTI uses "finite"
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
    ("Planned event", "Unplanned event"),
    ("Deliberate than spontaneous", "Spontaneous than deliberate")
]

mbti_rules = [
    {0: 'E', 1: 'I'},  # Col 1
    {0: 'S', 1: 'N'},  # Col 2
    {0: 'T', 1: 'F'},  # Col 3
    {0: 'J', 1: 'P'},  # Col 4
    {0: 'E', 1: 'I'},  # Col 5 = EI
    {0: 'S', 1: 'N'},  # Col 6 = SN
    {0: 'T', 1: 'F'},  # Col 7 = TF
] * 10


""" questions = [MBTI_question(q, a, r) for q, a, r in zip(mbti_questions, mbti_answers, mbti_rules)]
test = MBTI_test(questions)

stats = []
for i in range(100):
    test = MBTI_test(questions)
    _ = [test.add_answer(random.choice([0,1])) for i in range(70)]
    stats.append(test.evaluate())  """



