import time
import os
import math_mathup as m
import screens_mathup as s
import operations_mathup as o
import json
import time

active = True
while active:
	try:
		with open('os.json', 'r') as f_obj:
			clear = json.load(f_obj)
			active = False
	except:
		os = input("Please enter your os type: ('win' / 'osx' / 'linux')\n")
		if os == 'osx' or os == 'linux':
			clear = 'clear'
			with open('os.json', 'w') as f_obj:
				json.dump(clear, f_obj)
		elif os == 'win' or os == 'w':
			clear = 'cls'
			with open('os.json', 'w') as f_obj:
				json.dump(clear, f_obj)

#default settings
operation = 3
difficulty = 3

#date
today = time.strftime('%x')

user = o.check_user()
o.check_highscore()

active = True
while active:
	try:
		os.system(clear)
	except AttributeError:
		s.loading_bar(1)
		print("\nOS has be registered. Please run the program again.")
		break

	response_raw = s.main_screen()

	response = response_raw.lower()
	if response == 'start' or response == 's':
		os.system(clear)
		duration = 30 #secconds
		t_end = time.time() + duration

		points = {'answer_streak': 0,
			'best_streak': 0,
			'correct_answers': 0,
			'wrong_answers': 0,
			'total_answers': 0,
			'total_score': 0
				}


		while time.time() < t_end:
			score = m.run_game(operation, difficulty)
			if score == 'quit':
				t_end = time.time()
			elif score == 15:
				points['total_score'] += score
				points['total_answers'] += 1
				points['correct_answers'] += 1
				points['answer_streak'] += 1
				if points['answer_streak'] >= points['best_streak']:
					points['best_streak'] = points['answer_streak']
			elif score == -5:
				points['total_score'] += score
				points['total_answers'] += 1
				points['wrong_answers'] += 1
				points['answer_streak'] = 0
		if score != 'quit':
			points['final_score'] = points['total_score'] + points['best_streak'] * 3
			s.points_screen(points)
			next = input("\nPress Enter to continue.")
		o.save_score(points, today, user, operation, difficulty)
	elif response == 'q' or response == 'quit':
		break
	elif response == 'o' or response == 'options':
		os.system(clear)
		options_input = s.options_main_screen()

		if options_input == 'o' or options_input == 'options':
			s.options_current_screen(options_input, operation, difficulty, clear)
			next = input("\nPress Enter to continue.")

		if options_input == '1':
			s.options_operation_type(clear)
			try:
				operation = int(input("\nEnter a number to change to that operation.\n"))
			except:
				options_input = 'o'
		elif options_input == '2':
			s.options_difficulty(clear)
			try:
				difficulty = int(input("\nEnter a number to change to that difficulty.\n"))
			except:
				options_input = 'o'
		elif options_input == '3':
			s.user_config(clear)
			username = input("")
			filename = 'user.json'
			if username:
				with open(filename, 'w') as f_obj:
					json.dump(username, f_obj)
		continue

	elif response == 'h' or response == 'highscores':
		s.highscores(clear)
		next = input("\nPress any key to continue, or 'd' to delete all highscores.\n")
		if next == 'd':
			with open('highscores.json', 'w') as f_obj:
				scores = []
				json.dump(scores, f_obj)

	else:
		continue

try:
	os.system(clear)
except:
	pass
