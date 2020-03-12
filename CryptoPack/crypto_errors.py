## Author:	Owen Cocjin
## Version:	1.0
## Date:	17/02/20
## Notes:
##	- Created crypto_errors.py

#------------------#
#    EXCEPTIONS    #
#------------------#
class DegreeError(Exception):
	'''Raised when an invalid degree is passed'''
	pass

class CoeffError(Exception):
	'''Raised when an invalid coefficient is passed'''
	pass

class TermError(Exception):
	'''Raised for a general Term error'''
	pass

class RangeError(Exception):
	'''Raised if an invalid range string was passed to Letters'''
	pass

class RuleError(Exception):
	'''Raised when a rule was broken'''
	def __init__(self, rule):
		Exception.__init__(self, rule)
