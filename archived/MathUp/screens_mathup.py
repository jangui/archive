import os
import json
import time
from random import randint

def main_screen():
	print("\n\n+++++++++++ MATHUP +++++++++++")
	response_raw = input("-Enter 's' to start.\n"
		+ "-Enter 'h' for highscores.\n"
		+ "-Enter 'o' for options.\n"
		+ "-Enter 'q' to quit at anytime.\n")
	return response_raw


def points_screen(points):
	print("Time's up!\n"
		+ "\nTotal Answers: " + str(points['total_answers'])
		+ "\nCorrect Answers: " + str(points['correct_answers'])
		+ "\nWrong Answers: " + str(points['wrong_answers'])
		+ "\nBest Streak: " + str(points['best_streak'])
		+ "\nFinal Score: " + str(points['final_score']))

def options_main_screen():
	print("\n\n-------------- Options --------------")
	options_input = input("1. Operation Type.\n"
		+ "2. Difficulty.\n"
		+ "3. User Settings\n\n"
		+ "Enter a number to change that option.\n"
		+ "Enter 'o' to view current options.\n"
		+ "Enter any other key to go back.\n")
	return options_input

def options_current_screen(options_input, operation, difficulty, clear):
	if options_input == 'o' or options_input == 'options':
			os.system(clear)
			print("\n")

			if operation == 1:
				print("Operation: Addition")
			if operation == 2:
				print("Operation: Subraction")
			if operation == 3:
				print("Operation: Multiplication")
			if operation == 4:
				print("Operation: Division")

			print("Difficulty: " + str(difficulty))

def options_difficulty(clear):
	os.system(clear)
	print("\n\n----------- Difficulty Settings -----------"
		+ "\n\n'1'      - Easy af   -      Digits 1-10"
		+ "\n'2'      - EZ Money  -      Digits 1-12"
		+ "\n'3'      - Dumb Cunt -      Digits 1-15"
		+ "\n'4'      - Twat Shit -      Digits 1-20"
		+ "\n'5'      - Medium    -      Digits 1-100"
		+ "\n'6'      - Hard      -      Digits 1-1000"
		+ "\n'7'      - Expert    -      Digits 1-10000")

def options_operation_type(clear):
	os.system(clear)
	print(""
		+ "\n\n----- Operation Type -----"
		+ "\n\n'1'    + Addition +"
		+ "\n'2'    - Subtraction -"
		+ "\n'3'    · Multiplication ·"
		+ "\n'4'    / Division /")

def user_config(clear):
	os.system(clear)
	filename = 'user.json'
	with open(filename, 'r') as f_obj:
		user = json.load(f_obj)
	print(""
		+ "\n\n----------- User Settings -----------"
		+ "\n\nCurrent User:", user, ""
		+ "\n\nPress enter to leave current settings,"
		+ "\nor type in a new user name."
                        + "\n--Note: Relaunch game to save user settings.")
	return user


def highscores(clear):
	os.system(clear)
	filename = 'highscores.json'
	print("\n\n########################### HIGHSCORES ##########################\n")
	with open(filename, 'r') as f_obj:
		scores = json.load(f_obj)
		for score in scores:
			if score['operation'] == 1:
				score['operation'] = "Addition"
			elif score['operation'] == 2:
				score['operation'] = "Subtraction"
			elif score['operation'] == 3:
				score['operation'] = "Multiplication"
			elif score['operation'] == 4:
				score['operation'] = "Division"
			print(str(score['score']) + " - " + score['user'] + " - " + score['date']
				+ " - (" + score['operation'] + ", Difficulty: " + str(score['difficulty']) + ")")

def loading_bar(speed=2):
    cancelled = False
    if speed == 1:
        speed = 10000
    elif speed == 2:
        speed = 25000
    elif speed == 3:
        speed = 50000
    elif speed == 4:
        speed = 75000
    elif speed == 5:
        speed = 100000
    dash =''

    try:
        for i in range(101):
            if i%2 == 0:
                dash  += '-'
            arrow = dash + '>'
            space = (52 - len(arrow)) * ' '
            bar = "[" + arrow + space + "]"
            message = "%LOADING% " + bar + str(i).rjust(4) + "%"
            print(message, end='')
            print('\b' * len(str(message)), end='', flush=True)
            delay = randint(1, speed) / 100000
            time.sleep(delay)

    except KeyboardInterrupt:
        cancelled = True
        print("\nCancelled.")
