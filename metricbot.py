'''
This file contains the main functions for the freedomunits_bot.

'''

import praw

import config

import convert

from prawcore import PrawcoreException

import time

'''
This method returns a reddit instance of the bot so that it could login.
'''
def login():
	reddit = praw.Reddit(username = config.username, 
						password = config.password,
						client_id = config.client_id,
						client_secret = config.client_secret,
						user_agent = config.user_agent)

	print("Login successful")

	return reddit

'''
This bot is the main method of the bot, and finds the comments that contain the units 
(that is not posted by the bot) and then extracts the value and unit within the comment.
Then, after getting the converted value, 
'''
def run(reddit):
	print("Get comments from r/test...")

	for comment in reddit.subreddit('test').comments():
		if comment.author != reddit.user.me():
			mode = "in"

			#if "cm" or "lb" or "kg" or "inch" or "inches" or "celsius" or "fahrenheit" in comment.body:
			if unit_equals_to(comment.body, mode):
			#if "cm" in comment.body or "kg" in comment.body or:
				print("Get comment that contains metric or imperial")

				comment_words = []
				#Gather each words within the comment.
				comment_words = comment.body.split(" ")

				unit = 0
				value = 0
				mode = "equal"

				#Search for the unit and value within the comment
				for i in range(len(comment_words)):
					if unit_equals_to(comment_words[i], mode):
						print("Found unit and value in comment!")

						unit = comment_words[i]
						value = comment_words[i-1]
						break

				#If bot doesn't find unit that doesn't match, skip this round
				if unit == 0 or value == 0:
					continue

				#Prevent bot from replying to comments that have an invalid unit or value
				#e.g word before unit is not a number, unit is not in list
				try:
					#Retrieve the converted value and unit
					conv_value, conv_unit = bot_convert(value, unit)
					#Get body for the replying comment, which is changed depending if the
					#unit is metric or imperial
					reply_body = replied_comment(value, unit, conv_value, conv_unit)
				
				except ValueError:
					print("The value is not a number!")
					continue
				
				except InvalidUnitError:
					print("This unit is not a legitimate unit!")
					continue

				comment.reply(reply_body)
				print("Successfully replied to comment!")

				time.sleep(5)

'''
This method determines by unit which unit to convert it to, and then returns the converted 
value in a string format by calling respective functions from convert.py.
The legitimate units used in this function will be cm, inches, kg, lb, celsius, and farenheit.
If the value is not a number, it will raise a ValueError, and if the unit is not a one that
is listed above, it will raise an Exception.
Both exceptions will prevent the program from replying to said comment.
'''
def bot_convert(value, unit):
	#Not only will this change the value to be able to be calculated, it will detect whether or 
	#not "value" is a number. Will raise ValueError if not.
	value = float(value)
	print("Value is a number!")

	print("Start conversion...")

	if unit == "cm":
		converted = convert.cm_to_inches(value)
		conv_unit = "inches"

		#If the total amount of inches is larger than 12, convert it so that it will be
		#shown as feet and inches (e.g 58 inches -> 4'10)
		if converted > 12:
			feet,inches = convert.feet_and_inches(converted)
			converted = str(feet) + "'" + str(inches) + "''"
			conv_unit = "feet and inches"

	elif unit == "inches" or unit == "inch":
		converted = convert.inches_to_cm(value)
		conv_unit = "cm"

	elif unit == "lb":
		converted = convert.lb_to_kg(value)
		conv_unit = "kg"

	elif unit == "kg":
		converted = convert.kg_to_lb(value)
		conv_unit = "lb"

	elif unit == "fahrenheit":
		converted = convert.f_to_c(value)
		conv_unit = "°C"

	elif unit == "celsius":
		converted = convert.c_to_f(value)
		conv_unit = "°F"

	else:
		raise InvalidUnitError

	print("Conversion has been successful!")

	converted = str(converted)

	return converted, conv_unit

'''
This method creates the body for the reply to the original comment that contained the
metric or imperial value. 
It will tailor the text depending on the units that was contained within the comment.
If the converted unit is invalid, it will raise an Exception to prevent the bot 
replying to the comment.
'''
def replied_comment(value, unit, conv_value, conv_unit):
	print("Start creating reply body...")

	#Determine if the converted unit is in metric or imperial. 
	if conv_unit == "cm" or conv_unit == "kg" or conv_unit == "°C":
		reply_body = "In metric units, " + value + " " + unit + " is equal to " + conv_value + " " + conv_unit + ".\n"
	
	elif conv_unit == "inches" or conv_unit == "inch" or conv_unit == "lb" or conv_unit == "°F":
		reply_body = "In imperial units, " + value + " " + unit + " is equal to " + conv_value + " " + conv_unit + ".\n"
	
	#If the converted unit is in feet and inches, the reply comment will not include units.
	#e.g "In imperial, 155 cm is equal to 5'1"
	elif conv_unit == "feet and inches":
		reply_body = "In imperial units, " + value + " " + unit + " is equal to " + conv_value + ".\n"
	
	else:
		print(conv_unit)
		print(unit)
		raise InvalidUnitError

	reply_body += "\n---\n\n"

	reply_body += "^This ^bot ^converts ^metric ^and ^imperial ^units. ^Creator: ^/u/xicedlemonteax"

	print("Successfully created reply comment body!")

	return reply_body 

'''
This method compares 
'''
def unit_equals_to(unit, mode):
	#Used for Line 57, find exact word that contains unit
	if mode == "equal":
		if unit == "cm":
			return True
		elif unit == "inches":
			return True
		elif unit == "inch":
			return True
		elif unit == "kg":
			return True
		elif unit == "lb":
			return True
		elif unit == "fahrenheit":
			return True
		elif unit == "celsius":
			return True
		else:
			return False
	#Used for Line 43, find listed unit in comment body
	elif mode == "in":
		if "cm" in unit:
			return True
		elif "inches" in unit:
			return True
		elif"inch" in unit:
			return True
		elif "kg" in unit:
			return True
		elif "lb" in unit:
			return True
		elif "fahrenheit" in unit:
			return True
		elif "celsius" in unit:
			return True
		else:
			return False

class Error(Exception):
	pass

class InvalidUnitError(Error):
	pass

'''
This is the main program
'''
reddit = login()

while True:
	run(reddit)
	time.sleep(10)