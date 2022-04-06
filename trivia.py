import json
import time
from tabulate import tabulate
import os
from colorama import Fore

# Helpers


def welcome():
    print(
        f"""
 █████  ██████████   ██████ █████████  
░░███  ░░██░░██████ ██████ ███░░░░░███ 
 ░███   ░███░███░█████░███░███    ░███ 
 ░███   ░███░███░░███ ░███░███████████ 
 ░███   ░███░███ ░░░  ░███░███░░░░░███ 
 ░███   ░███░███      ░███░███    ░███ 
 ░░████████ █████     █████████   █████
  ░░░░░░░░ ░░░░░     ░░░░░░░░░   ░░░░░ 
            Trivia Maker\n
Configuring...
"""
    )
    time.sleep(5)


def clear_console():
    command = "clear"
    if os.name in ("nt", "dos"):
        command = "cls"
    os.system(command)


def ask_difficulty():
    difficulty = input(Fore.BLUE + "Difficulty:(Easy/Hard)\n")
    if difficulty in ["Easy", "easy", "Hard", "hard"]:
        clear_console()
        return difficulty
    else:
        exit(print(Fore.RED + "Wrong Difficulty"))


def ask_question():
    question = input(Fore.BLUE + "Write Question:\n")
    clear_console()
    return question


def ask_answers(difficulty: str):
    ans1 = input(Fore.BLUE + "Write Answer 1: ")
    ans2 = input(Fore.BLUE + "Write Answer 2: ")
    ans3 = None
    ans4 = None
    if difficulty in ["hard", "Hard"]:
        ans3 = input(Fore.BLUE + "Write Answer 3: ")
        ans4 = input(Fore.BLUE + "Write Answer 4: ")
    if ans3 != None:
        return [ans1, ans2, ans3, ans4]
    else:
        return [ans1, ans2]


def correct_answer(answers: list):
    if len(answers) == 2:
        ans_given = "1/2"
        ans_given_int = 2
    else:
        ans_given = "1/2/3/4"
        ans_given_int = 4
    is_ans_given = False
    while is_ans_given == False:
        c_answer = int(
            input(f"\n{Fore.BLUE}What answer is correct({ans_given}):{Fore.BLUE}")
        )
        clear_console()
        if ans_given_int == 2:
            if c_answer in range(0, 3):
                is_ans_given = True
                return c_answer
            else:
                is_ans_given = False
        else:
            if c_answer in range(0, 5):
                is_ans_given = True
                return c_answer
            else:
                is_ans_given = False


def confirmation(question: str, answers: list, difficulty: str, correct_answer: str):
    q_confirm = input(
        f"{Fore.RESET}Confirm the Question:\n{Fore.GREEN}{question}\n(Y/N):{Fore.BLUE}"
    )
    if q_confirm in ["Y", "y"]:
        if len(answers) == 4:
            ops = ["A", "B", "C", "D"]
        else:
            ops = ["A", "B"]
        clear_console()
        headers = ["No.", "Ans."]
        print(Fore.BLUE + "Confirm your Answers\n")
        answers_tab = zip(ops, answers)
        print(Fore.GREEN + tabulate(answers_tab, headers=headers))
        print(Fore.GREEN + f"\nCorrect Answer: {answers[correct_answer-1]}")
        a_confirm = input(f"{Fore.GREEN}(Y/N):{Fore.BLUE}")
        if a_confirm in ["Y", "y"]:
            data_to_dump = {
                "question": question,
                "answers": answers,
                "correct_answer": answers[correct_answer - 1],
            }
            with open("./trivia.json", "r") as f:
                pre_data = json.load(f)
                pre_data[difficulty.lower()].append(data_to_dump)
            with open("./trivia.json", "w") as f:
                json.dump(pre_data, f, indent=4)
            clear_console()
        else:
            print(Fore.RED + "Cancelled\n")
    else:
        print(Fore.RED + "Cancelled\n")


if __name__ == "__main__":
    try:
        clear_console()
        welcome()
        clear_console()
        while True:
            difficulty = ask_difficulty()
            question = ask_question()
            answers = ask_answers(difficulty)
            c_answer = correct_answer(answers)
            confirmation(question, answers, difficulty, c_answer)
    except Exception as e:
        print(f"{Fore.RESET}Exited with error: {e}")
