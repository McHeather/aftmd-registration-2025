from datetime import datetime
from util.map import set_field_if_exists
from participants.scholarship import Scholarship

class Chaperone:
	def __init__(self, student_dict):
		self.role = "Chaperone"

		# badge details
		self.fname = set_field_if_exists('First Name', student_dict)
		self.lname = set_field_if_exists('Last Name', student_dict)
		self.email = set_field_if_exists('Email', student_dict)
		self.phone = set_field_if_exists('Phone Number', student_dict)
		self.badge_name = set_field_if_exists('First and Last Names you would like to appear on your badge (if different from above)', student_dict)
		self.pronouns = set_field_if_exists('If you would like your pronouns included on your badge, please add them here (optional)', student_dict)
		self.u18_name = set_field_if_exists("Names of the under-18 student(s) that you will be accompanying", student_dict)

		self.festival_pass = set_field_if_exists("Festival pass", student_dict)
		self.mainer = set_field_if_exists('Are you a Maine resident?', student_dict)
		self.maine_id = set_field_if_exists('Please upload proof of Maine residency:', student_dict)

		# contact details
		self.city = set_field_if_exists('City', student_dict)
		self.state = set_field_if_exists('State', student_dict)
		if self.state == "":
			self.state = set_field_if_exists('Province', student_dict)
		self.all_camp_list = set_field_if_exists('I am happy for you to include my email in the "all camp" list that will be distributed to participants after the festival.', student_dict)
		self.volunteer = set_field_if_exists('Would you be interested in volunteering during the festival?', student_dict)
		if self.volunteer == "":
			self.volunteer = set_field_if_exists('5. If I receive a scholarship, I am willing to volunteer while attending the festival.', student_dict)
		self.photo_optout = set_field_if_exists('Please give me a red sticker on my name badge', student_dict)
		self.parking = set_field_if_exists('Will you need a parking pass?', student_dict)

		# tuition
		self.scholarship = set_field_if_exists('Would you like to apply for a scholarship?', student_dict)
		if self.scholarship == "Yes":
			self.applicant = Scholarship(student_dict)
		# - capitalize to ensure that self.group is set correctly
		self.discipline = set_field_if_exists('Major discipline:', student_dict).capitalize()
		if self.discipline[:6] == "Option":
			self.discipline = set_discipline(self.discipline)
		self.group = set_field_if_exists(self.discipline+' group', student_dict)
		self.group = self.group.split()[0]

		# hosuing
		self.housing = set_field_if_exists('Will you be staying on campus?', student_dict)
		self.room_waitlist = set_field_if_exists('I would like to join the wait list for a room on campus:', student_dict)
		self.roommate = set_field_if_exists('Name of your requested roommate:', student_dict)
		if self.roommate == "":
			self.roommate = set_field_if_exists('We match roommates based on age and gender. To help us do this, please enter your gender here (or let us know if you would prefer otherwise):', student_dict)
		self.housing_needs = set_field_if_exists('Do you have any health-related concerns you would like us to be aware of?', student_dict)
		
		# meals
		self.meals = set_field_if_exists('Meal plan', student_dict)
		self.meal_reqs = set_field_if_exists('Dietary Requirements', student_dict)
		self.meal_other_reqs = set_field_if_exists('Other dietary requirements', student_dict)
		self.lobster = set_field_if_exists('Would you like to add on the Wednesday night lobster dinner?', student_dict)
		self.meals_waitlist = set_field_if_exists('I would like to join the wait list for a meal plan:', student_dict)
		if self.meals_waitlist == "Yes":
			self.meals_waitlist = "Full Meal Plan"

		# bookkeeping
		self.regfox_id = student_dict['id']
		self.created = student_dict['created']
		self.order_display_id = set_field_if_exists('order_display_id', student_dict)
		self.income = student_dict['income']

	def __str__(self):
		return f'{self.regfox_id}: {self.fname} {self.lname} ({self.role})'

	def to_str(self):
		return f'{self.regfox_id}: {self.fname} {self.lname} ({self.role})\n'

	def to_row(self):
		return [ [
		# Notes / First Name / Last Name / Email / Phone Number / Badge Name / Pronouns / Role
		None, self.fname, self.lname, self.email, self.phone, self.badge_name, self.pronouns, self.role,
		
		# Accompanying / Age / Maine? / NA / NA / NA / NA / Festival Pass / Volunteer
		self.u18_name, None, self.mainer, None, None, None, None, self.festival_pass, self.volunteer,
		
		# Scholarship / Discipline / Group 
		self.scholarship, self.discipline, self.group, 

		# Lodging / Roommate / Room Waitlist / Housing Needs / NA / NA
		self.housing, None, self.room_waitlist, self.housing_needs, None, None,
		
		# Meals / Dietary Reqs / Other Reqs / Lobster / Meals Waitlist / City / State / Photo optout / Parking Pass / Income
		self.meals, self.meal_reqs, self.meal_other_reqs, self.lobster, self.meals_waitlist, self.city, self.state, self.photo_optout, self.parking, self.income,
		
		# Created / Entered / ID
		self.created, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), self.regfox_id
		] ]

	def applicant_to_row(self):
		return [ [
		# Name / Email / Q1 / Q2 / Q3 / Q4 / Q5: Volunteer
		self.fname+" "+self.lname, self.email, self.applicant.q1, self.applicant.q2, self.applicant.q3, self.applicant.q4, self.applicant.volunteer,

		# Awarded % / Awarded $ / Date Notified / Date Accepted / $ Outstanding / Date Paid or Refunded
		None, None, None, None, None, None,

		# Age / Mainer / Housing / Meals / Lobster / Paid / Created / ID
		None, self.mainer, self.housing, self.meals, self.lobster, None, self.created, self.regfox_id
		] ]