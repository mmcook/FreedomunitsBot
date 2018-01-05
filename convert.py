'''
This file contains all the functions used to convert the value from metric to imperial
and vice versa. 
All values will be rounded to the first decimal value.
All the conversions are between centimeters and inches, pounds and kilograms, celsius
and farenheit.
If the total amount of inches are more than 12, it will convert from inches to feet and
inches, and also vice versa (feet and inches to just inches).
'''

def cm_to_inches(cm):
	inches = cm * 0.39
	inches = round(inches, 1)
	return inches

def inches_to_cm(inches):
	cm = inches * 2.54
	cm = round(cm, 1)
	return cm

def feet_and_inches(tot_inches):
	feet, inches = divmod(tot_inches, 12)
	feet = round(feet, 0)
	feet = int(feet)
	inches = round(inches, 1)
	return feet, inches

def total_inches(feet, inches):
	tot_inches = feet * 12 + inches
	return tot_inches

def kg_to_lb(kg):
	lb = kg*2.2046
	lb = round(lb, 1)
	return lb

def lb_to_kg(lb):
	kg = lb /2.2046
	kg = round(kg,1)
	return kg

def c_to_f(c):
	f = c * (9/5) + 32
	f = round(f, 1)
	return f

def f_to_c(f):
	c = (f - 32) * (5/9)
	c = round(c, 1)
	return c