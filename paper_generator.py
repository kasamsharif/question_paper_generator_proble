import json
import constants
import sys


def get_marks_as_per_difficulty_level(question_paper):
    easy, medium, hard = 0, 0, 0
    for question_type in question_paper["questionType"]:
        if question_type["type"] == constants.EASY:
            easy = (question_type["percentage"] / 100.0) * question_paper["marks"]
        elif question_type["type"] == constants.MEDIUM:
            medium = (question_type["percentage"] / 100.0) * question_paper["marks"]
        elif question_type["type"] == constants.HARD:
            hard = (question_type["percentage"] / 100.0) * question_paper["marks"]
    return easy, medium, hard


def get_questions(question_list, marks):
    i = 0
    begin = 0
    sum_weightage = 0.0
    q_list = []  # question list
    q_code = question_list.keys()  # question code
    q_weightage = question_list.values()  # question weightage

    len_q_of_weightage = len(q_weightage)
    while i < len_q_of_weightage:
        sum_weightage += float(q_weightage[i])
        if sum_weightage < marks:
            q_list.append(q_code[i])
        elif sum_weightage == marks:
            q_list.append(q_code[i])
            break
        else:
            if i != len_q_of_weightage - 1 and i > 1:
                sum_weightage -= q_weightage[i]
                i = i - 1
                question_code = q_list[len(q_list) - 1]
                q_list.pop()
                sum_weightage -= question_list[question_code]

        if i == len_q_of_weightage - 1:
            q_list = []
            sum_weightage = 0
            i = begin
            begin += 1
        i = i + 1
    if len(q_list) == 0 and marks > 0:
        print "Summation of question marks not equal to marks"
        sys.exit(1)
    return q_list


if __name__ == '__main__':
    question_file = open('question_paper_data/questions.txt')
    question_data = json.load(question_file)

    easy, medium, hard = get_marks_as_per_difficulty_level(question_data["questionPaper"])

    all_quest = []
    easy_list, medium_list, hard_list = dict(), dict(), dict()
    for question in question_data["questions"]:
        if question["type"] == constants.EASY:
            easy_list.update({question["code"]: question["weightage"]})
        elif question["type"] == constants.MEDIUM:
            medium_list.update({question["code"]: question["weightage"]})
        elif question["type"] == constants.HARD:
            hard_list.update({question["code"]: question["weightage"]})
    all_quest += get_questions(easy_list, easy)
    all_quest += get_questions(medium_list, medium)
    all_quest += get_questions(hard_list, hard)
    print all_quest
