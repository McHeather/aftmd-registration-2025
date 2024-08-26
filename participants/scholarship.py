from util.map import set_field_if_exists

class Scholarship:
	def __init__(self, student_dict):

		self.q1 = set_field_if_exists('1. Please tell us a little about your interest in studying traditional music and/or dance. Why do you want to attend Acadia Festival of Traditional Music & Dance?', student_dict)
		self.q2 = set_field_if_exists('2. Please tell us a little about why you are applying for financial assistance through the scholarship program.', student_dict)
		self.q3 = set_field_if_exists('3. The amount of scholarship assistance offered depends on the amount of funding we have for this program. Which of the following would you like to be considered for?  Please select one based on your need.', student_dict)
		self.q4 = set_field_if_exists('4. Is there anything else you’d like us to know?', student_dict)
		self.volunteer = set_field_if_exists('5. If I receive a scholarship, I am willing to volunteer while attending the festival.', student_dict)