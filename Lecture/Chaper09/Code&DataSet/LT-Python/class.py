#!/usr/bin/python
class Employee:
		'Common base class for all employees'
		empCount = 0
		
		def _init_(self, name, salary):
			self.name = name
			self.salary = salary
			Employee.empCount += 1
		
		def displayCount(self):
			print "Total Employee %d" %Employee.empCount
			
		def displayEmployee(self):
			print "Name: ", self.name, ", Salary: ", self.salary
emp1 = Employee("Toto", 2000)
