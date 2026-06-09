#!/usr/bin/python
def addTwo(a,b):
	return a + b
def divide(a,b):
	return (1.0*a)/b, a%b
y = input('y = ')
x = input('x = ')
z = addTwo(x,y)
print z
p, q = divide(x,y)
print p, q