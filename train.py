import re
import random
from typing import List, Dict


class Session:
    session = None

    def __init__(self):
        self.correct = 0
        self.invalid = 0
        self.skipped = 0
        self.errors = []

    @staticmethod
    def get() -> 'Session':
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
        self.answered = False

    def check(self, answers):
        session = Session.get()
        for i, answer in enumerate(answers):
            if answer == self.answers[i]:
                session.correct += 1
                self.answered = True
                print("OK")
            elif answer == self.__latinize__(self.answers[i]):
                session.correct += 1
                self.answered = True
                print("Almost OK: " + self.answers[i])
            else:
                session.invalid += 1
                session.errors.append("Yours: " + answer +", correct: " + self.answers[i])
                print("Wrong: " + self.answers[i])

    @staticmethod
    def __latinize__(text):
        replaces = {
            "é": "e",
            "è": "e",
            "ê": "e",
            "à": "a",
            "â": "a",
            "ù": "u",
            "û": "u",
            "î": "i",
            "ô": "o",
            "ç": "c",
            "ï": "i"
        }
        for key, replace in replaces.items():
            text = text.replace(key, replace)
        return text


class Task:
    def __init__(self, title: str, questions: List[Question]):
        self.title = title  # type: str
        self.questions = questions  # type: List[Question]
        self.completed = False

    def pick(self):
        unanswered_questions = []
        for question in self.questions:
            if not question.answered:
                unanswered_questions.append(question)
        if len(unanswered_questions) == 0:
            task.completed = True
            return None
        number = random.randint(0, len(unanswered_questions) - 1)
        return unanswered_questions[number]

    def run(self):
        question = self.pick()
        while question is not None:
            print("Task: " + self.title + ", question: " + question.request)
            inp = input().strip()
            if self.handle_commands(inp):
                continue
            else:
                question.check([inp])
                question = self.pick()

    def handle_commands(self, inp):
        commands = ["/stat", "/errors", "/exit"]
        if inp not in commands:
            return False
        else:
            session = Session.get()
            if inp == "/stat":
                print(session)
            if inp == "/errors":
                print(session.errors)
            if inp == "/exit":
                exit(0)
        return True

    def __repr__(self):
        return self.title


class Section:
    def __init__(self, title: str, tasks: Dict[str, Task]):
        self.title = title  # type: str
        self.tasks = tasks  # type: Dict[str, Task]

    def pick(self):
        uncompleted_tasks = []
        for task in self.tasks.values():
            if not task.completed:
                uncompleted_tasks.append(task)
        if len(uncompleted_tasks) == 0:
            return None
        number = random.randint(0, len(uncompleted_tasks) - 1)
        return uncompleted_tasks[number]

    def __repr__(self):
        return self.title

if __name__ == "__main__":
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
            tasks = {}
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
                tasks[task_title] = task
            section = Section(section_title, tasks)
            sections[section_title] = section

    print("Выберите секцию: " + str(list(sections.values())))
    section_title = input().strip()
    section = sections[section_title]
    print("Выберите задание или введите /all: " + str(list(section.tasks.values())))
    task_name = input().strip()
    if task_name == "/all":
        task = section.pick()
        while task is not None:
            task.run()
            task = section.pick()
    else:
        task = section.tasks[task_name]
        task.run()