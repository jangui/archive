from random import randint
import json
import operator

def numbers_calc(difficulty):
    numbers = {}
    if difficulty == 1:
    	x = 10
    elif difficulty == 2:
        x = 12
    elif difficulty == 3:
        x = 15
    elif difficulty == 4:
    	x = 20
    elif difficulty == 5:
        x = 100
    elif difficulty == 6:
        x = 1000
    elif difficulty == 7:
        x = 10000
    num1 = randint(2,x)
    num2 = randint(2,x)
    numbers['num1'] = num1
    numbers['num2'] = num2
    return numbers


def addition_mathup(difficulty):
	numbers = numbers_calc(difficulty)
	output = {}
	msg = str(numbers['num1']) + " + " + str(numbers['num2']) + " = "
	ans = numbers['num1'] + numbers['num2']
	output['message'] = msg
	output['answer'] = ans
	return output

def subtraction_mathup(difficulty):
	numbers = numbers_calc(difficulty)
	output = {}
	msg = str(numbers['num1']) + " - " + str(numbers['num2']) + " = "
	ans = numbers['num1'] - numbers['num2']
	output['message'] = msg
	output['answer'] = ans
	return output

def multiplication_mathup(difficulty):
	numbers = numbers_calc(difficulty)
	output = {}
	msg = str(numbers['num1']) + " x " + str(numbers['num2']) + " = "
	ans = numbers['num1'] * numbers['num2']
	output['message'] = msg
	output['answer'] = ans
	return output

def division_mathup(difficulty):
	numbers = numbers_calc(difficulty)
	output = {}
	dividend = numbers['num1'] * numbers['num2']
	msg = str(dividend) + " / " + str(numbers['num2']) + " = "
	ans = dividend / numbers['num2']
	output['message'] = msg
	output['answer'] = ans
	return output

def check_user():
	try:
		with open('user.json', 'r') as f_obj:
			user = json.load(f_obj)
			return user
	except:
		with open('user.json', 'w') as f_obj:
			user = 'none'
			json.dump(user, f_obj)
			return user

def check_highscore():
	try:
		with open('highscores.json', 'r') as f_obj:
			test = json.load(f_obj)
	except:
		with open('highscores.json', 'w') as f_obj:
			scores = []
			json.dump(scores, f_obj)

def save_score(points, today, user, operation, difficulty):
	scoreInfo = {}
	scoreInfo['score'] = points['total_score']
	scoreInfo['date'] = today
	scoreInfo['user'] = user
	scoreInfo['operation'] = operation
	scoreInfo['difficulty'] = difficulty
	filename = 'highscores.json'
	with open(filename, 'r') as f_obj:
		scores = json.load(f_obj)
	scores.append(scoreInfo)
	scores.sort(key=operator.itemgetter('score'), reverse = True)
	scores = scores[0:5]
	filename = 'highscores.json'
	with open(filename, 'w') as f_obj:
		json.dump(scores, f_obj)
