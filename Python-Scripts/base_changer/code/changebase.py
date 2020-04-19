#!/usr/bin/env python3
#Base-n to Base-10 converter by Dangill

def change_base_n(input_number, input_base):

	input_number = input_number.lower()
	length = len(input_number)
	out_list = []
	base10 = 0

	def encode(digit):
		if digit == 'a':
			digit = 10
			return digit
		elif digit == 'b':
			digit = 11
			return digit
		elif digit == 'c':
			digit = 12
			return digit
		elif digit == 'd':
			digit = 13
			return digit
		elif digit == 'e':
			digit = 14
			return digit
		elif digit == 'f':
			digit = 15
			return digit


	for digit in input_number:
		try: 
			number = int(digit)
		except Exception:
			number = encode(digit)

		length = length - 1
		b = input_base**length * number
		base10 += b

	return base10


#ans = change_base_n('6ad1', 16)
#print(ans)
#if working 27345 should be printed

"""
Notes:
The limit base n that can be converted to decimal is base16.
However, mathematically the program can change base to a base greater than 16.
The only problem is the digits are not defined for bases higher than 16.
To increase the limit, define the rest of the digits.
To do so, in encode(digit) it defines 'a' as 10, 'b' as 11 ... etc
Simply add:

elif digit == 'g':
	digit = 16
	return digit

This will allow for base17 numbers to be accurately converted to base 10.
Define upto as many digits as needed.
-Dangill
"""