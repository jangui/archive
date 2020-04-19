import operations_mathup as o

def operation_type(operation, difficulty):

    if operation == 1:
        output = o.addition_mathup(difficulty)
        return output

    if operation == 2:
        output = o.subtraction_mathup(difficulty)
        return output

    if operation == 3:
        output = o.multiplication_mathup(difficulty)
        return output

    if operation == 4:
        output = o.division_mathup(difficulty)
        return output

def run_game(operation, difficulty):
    final = operation_type(operation, difficulty)
    answer_str = input("\n\n" + final['message'] + "\n")
    if answer_str == 'q':
        score = 'quit'
        return score

    try:
        answer = int(answer_str)
    except:
        answer = None
    else:
        answer = int(answer_str)

    if answer == final['answer']:
        print("Correct!")
        score = 15
        return score
    else:
        print("Wrong!")
        score = -5
        return score


