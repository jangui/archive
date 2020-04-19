#!/usr/bin/env python3
#Base-10 to Base-n converter

def base_change(base10, base):
	digits = 0 #digits must be left at 0
	def determine_digits(digits):
		"""recursive function, determines amout of digits of new number"""
		if base**digits > base10:
			return digits
		else:
				return determine_digits(digits + 1)

	steps = determine_digits(digits)
	#steps determines amount of devisions necesarry to convert to another base
	#this so happens to be the number of digits the new number will contain

	output = [] #list to put output in
	def base_change(steps, base10):
		"""recurvsive function which finds digits of new number"""
		if steps == 0: #steps get reduced each time function runs, when 0, fucntion finishes
			return
		else:
			output.append(base10 // base**(steps-1)) #add to list first digit
			base10 = base10 % base**(steps-1) #the remainder is now the new input (base10)
			base_change(steps-1, base10) #runs function again with remainder as input


	def final_output():
		base_change(steps, base10) #run algorithm

		#convert digits 10 and up into letters a, b, c ...
		output_final = []
		for number in output:
			if number < 10:
				output_final.append(str(number))
			elif number == 10:
				output_final.append("a")
			elif number == 11:
				output_final.append("b")
			elif number == 12:
				output_final.append("c")
			elif number == 13:
				output_final.append("d")
			elif number == 14:
				output_final.append("e")
			elif number == 15:
				output_final.append("f")
			base_n = "".join(output_final) #saves output to a string
		return base_n
	return final_output()


#base10 is the number that will be input to change base
#base is the base the number will get converted to !!(limit base16)!!


"""
Notes:
The limit base that can be converted to is base16.
However, mathematically the program can change base to a base greater than 16.
The only problem is the digits are not defined for bases higher than 16.
To increase the limit, define the rest of the digits.
To do so, in final_output() it defines 10 as 'a', 11 as 'b' ... etc
Simply add:

elif number == 16:
	output_final.append("g")

This will make the program accurate upto base 17.
Define upto as many digits as needed.
"""
