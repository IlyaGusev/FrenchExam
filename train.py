import re
import random


class Session:
    session = None

    def __init__(self):
        self.correct = 0
        self.invalid = 0
        self.skipped = 0
        self.errors = []

    @staticmethod
    def get():
        if Session.session is None:
            Session.session = Session()
        return Session.session

    def __str__(self):
        return "Correct: " + str(self.correct) + \
               ", invalid: " + str(self.invalid) + \
               ", skipped: " + str(self.skipped)


class Question:
    def __init__(self, line):
        self.request = re.sub(r"<[^>]+>", "_", line)
        self.answers = re.findall(r"<([^>]+)>", line)

    def check(self, answers):
        session = Session.get()
        for i, answer in enumerate(answers):
            if answer == self.answers[i]:
                session.correct += 1
                print("OK")
            else:
                session.invalid += 1
                session.errors.append("Yours: " + answer +", correct: " + self.answers[i])
                print("Wrong: " + self.answers[i])


class Task:
    def __init__(self, title, questions):
        self.title = title
        self.questions = questions

    def __repr__(self):
        return self.title

sections = {}
with open("tasks.txt", "r", encoding="utf-8") as f:
    text = f.read()
    sections_text = text.split("##")
    for section_text in sections_text:
        section_text = section_text.strip()
        section_title = section_text.split("\n")[0].strip()
        if section_title == "":
            continue
        section_text = "\n".join(section_text.split("\n")[1:])
        tasks = []
        sections[section_title] = tasks
        for task_text in section_text.split("#"):
            task_text = task_text.strip()
            task_title = task_text.split("\n")[0]
            if task_title == "":
                continue
            task_questions_texts = task_text.split("\n")[1:]
            questions = []
            for line in task_questions_texts:
                questions.append(Question(line))
            task = Task(task_title, questions)
            tasks.append(task)

commands = ["/stat", "/errors", "/skip", "/exit"]

while True:
    section_number = random.randint(0, len(sections)-1)
    section = list(sections.values())[section_number]
    task_number = random.randint(0, len(section)-1)
    task = section[task_number]
    question_number = random.randint(0, len(task.questions)-1)
    question = task.questions[question_number]
    print("Task: " + task.title + ", question: " + question.request)
    inp = input().strip()
    skip = False
    while inp in commands:
        session = Session.get()
        if inp == "/stat":
            print(session)
        if inp == "/errors":
            print(session.errors)
        if inp == "/skip":
            session.skipped += 1
            skip = True
            break
        if inp == "/exit":
            exit(0)
        print("Task: " + task.title + ", question: " + question.request)
        inp = input().strip()
    if not skip:
        question.check([inp])