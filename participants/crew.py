from datetime import datetime
from util.map import set_field_if_exists
from util.map import set_discipline

class Crew:
	def __init__(self, crew_dict):
		self.role = "Crew"

		# badge details
		self.fname = set_field_if_exists('First Name', crew_dict)
		self.lname = set_field_if_exists('Last Name', crew_dict)
		self.email = set_field_if_exists('Email', crew_dict)
		self.all_camp_list = set_field_if_exists('I am happy for you to include my email in the "all camp" list that will be distributed to participants after the festival.', crew_dict)
		self.phone = set_field_if_exists('Phone Number', crew_dict)
		self.badge_name = set_field_if_exists('First and Last Names you would like to appear on your badge (if different from above)', crew_dict)
		self.pronouns = set_field_if_exists('If you would like your pronouns included on your badge, please add them here (optional)', crew_dict)
		
		# contact details
		self.city = set_field_if_exists('City', crew_dict)
		self.state = set_field_if_exists('State', crew_dict)
		if self.state == "":
			self.state = set_field_if_exists('Province', crew_dict)
		
		# logistics
		self.photo_optout = set_field_if_exists('Please give me a red sticker on my name badge', crew_dict)
		self.parking = set_field_if_exists('Will you need a parking pass?', crew_dict)

		# tuition
		# capitalize to ensure that self.group is set correctly
		self.discipline = set_field_if_exists('Major discipline:', crew_dict).capitalize()
		if self.discipline[:6] == "Option":
			self.discipline = set_discipline(self.discipline)
		self.group = set_field_if_exists(self.discipline+' group', crew_dict)
		if self.group != "":
			self.group = self.group.split()[0]

		# housing
		self.housing = "Lodging provided"
		self.housing_needs = set_field_if_exists('Do you have any health-related concerns you would like us to be aware of?', crew_dict)
		
		# meals
		self.meals = "Full meal plan"
		self.meal_reqs = set_field_if_exists('Dietary Requirements', crew_dict)
		self.meal_other_reqs = set_field_if_exists('Other dietary requirements', crew_dict)
		self.lobster = set_field_if_exists('Would you like to add on the Wednesday night lobster dinner?', crew_dict)

		# bookkeeping
		self.regfox_id = crew_dict['id']
		self.created = crew_dict['created']
		self.order_display_id = set_field_if_exists('order_display_id', crew_dict)
		self.income = crew_dict['income']


	def __str__(self):
		return f'{self.regfox_id}: {self.fname} {self.lname} ({self.role})'

	def to_str(self):
		return f'{self.regfox_id}: {self.fname} {self.lname} ({self.role})\n'

	def to_row(self):
		return [ [
		# Notes / First Name / Last Name / Email / Phone Number / Badge Name / Pronouns / Role
		None, self.fname, self.lname, self.email, self.phone, self.badge_name, self.pronouns, self.role,
		
		# Accompanying / Age / Maine? / NA / NA / NA / NA / Festival Pass / Volunteer
		None, None, None, None, None, None, None, None, None,
		
		# Scholarship / Discipline / Group 
		None, self.discipline, self.group,

		# Lodging / Roommate / Room Waitlist / Housing Needs / NA / NA
		self.housing, None, None, self.housing_needs, None, None,
		
		# Meals / Dietary Reqs / Other Reqs / Lobster / Meals Waitlist / City / State / Photo optout / Parking Pass / Income
		self.meals, self.meal_reqs, self.meal_other_reqs, self.lobster, None, self.city, self.state, self.photo_optout, self.parking, self.income,
		
		# Created / Entered / ID
		self.created, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), self.regfox_id
		] ]