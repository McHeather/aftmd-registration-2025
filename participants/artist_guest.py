from datetime import datetime
from util.map import set_field_if_exists

class Artist_Guest:
	def __init__(self, staff_dict):
		self.fname = staff_dict['First Name']
		self.lname = staff_dict['Last Name']
		self.pronouns = set_field_if_exists('If you would like your pronouns included on your badge, please add them here (optional)', staff_dict)
		self.role = set_field_if_exists('My role at AFTMD 2025 is', staff_dict)
		# first responses have this mistake in them
		# self.role = set_field_if_exists('My role at AFTMD 2024 is', staff_dict)
		self.badge_name = set_field_if_exists('First and Last Names you would like to appear on your badge (if different from above)', staff_dict)
		self.guests = set_field_if_exists('Do you plan to have a partner/family member attend the festival with you?', staff_dict)
		self.mainer = set_field_if_exists('Are you a Maine resident?', staff_dict)

		# # guests details
		self.email = set_field_if_exists('Email address', staff_dict)
		self.phone = set_field_if_exists('Phone Number', staff_dict)
		self.who_accompanying = set_field_if_exists('Name of the faculty member you will be accompanying', staff_dict)
		if self.who_accompanying == "":
			self.who_accompanying = set_field_if_exists('Name of the director you will be accompanying', staff_dict)
		self.age = set_field_if_exists('I am under 18', staff_dict)
		if self.age == "Yes":
			self.age = "Under 18"
		if self.age == "No":
			self.age = "Over 18"
		self.housing = set_field_if_exists('Will you be staying on campus at COA?', staff_dict)
		self.discipline = set_field_if_exists('What morning classes will you be taking?', staff_dict)
		if self.discipline is not None and self.discipline != "":
			self.group = set_field_if_exists(self.discipline+' group', staff_dict)
		else:
			self.group = ""

		# # faculty contact details
		if self.email == "":
			self.email = set_field_if_exists('Preferred email for communications', staff_dict)
		if self.phone == "":
			self.phone = set_field_if_exists('Mobile phone number', staff_dict)
		self.street = set_field_if_exists('Street Address', staff_dict)
		self.city = set_field_if_exists('City', staff_dict)
		self.state = set_field_if_exists('State', staff_dict)
		if self.state == "":
			self.state = set_field_if_exists('Province', staff_dict)
		self.zip = set_field_if_exists('Zip/Postal Code', staff_dict)
		
		# # options
		self.all_camp_list = set_field_if_exists('I am happy for you to include my email in the "all camp" list that will be distributed to participants after the festival.', staff_dict)
		self.residency = set_field_if_exists('Residency', staff_dict)
		self.photo_optout = set_field_if_exists('Please give me a red sticker on my name tag', staff_dict)
		
		# # COA
		self.meals = set_field_if_exists('Meal Plan', staff_dict)
		self.meal_reqs = set_field_if_exists('Dietary Requirements', staff_dict)
		self.meal_other_reqs = set_field_if_exists('Other dietary requirements', staff_dict)
		self.lobster = set_field_if_exists('Would you like to add the Wednesday night lobster dinner?', staff_dict)
		self.housing_needs = set_field_if_exists('Do you (or your accompanying guests) have any housing needs we should be aware of?', staff_dict)
		
		# # socials, bio
		self.bio = set_field_if_exists('Please add a brief bio (approx. 200 words) here:', staff_dict)
		self.web_url = set_field_if_exists('Website URL:', staff_dict)
		self.fb_profile_url = set_field_if_exists('Facebook profile URL', staff_dict)
		self.fb_page_url = set_field_if_exists('Facebook page URL', staff_dict)
		self.insta_handle = set_field_if_exists('Instagram/Threads handle:', staff_dict)
		self.youtube = set_field_if_exists('YouTube handle or channel URL:', staff_dict)
		self.classroom_reqs = set_field_if_exists('Please let us know if there is anything you’d like to request for your classroom (i.e. Bluetooth speaker, white board or easel)', staff_dict)

		# videos and spotify tracks
		self.video1 = set_field_if_exists('Video 1 URL:', staff_dict)
		self.video2 = set_field_if_exists('Video 2 URL:', staff_dict)
		self.spotify1 = set_field_if_exists('Spotify track link 1:', staff_dict)
		self.spotify2 = set_field_if_exists('Spotify track link 2:', staff_dict)

		self.photos = []
		self.photos.append(set_field_if_exists('Photo 1:', staff_dict))
		self.photos.append(set_field_if_exists('Photo 2:', staff_dict))
		self.photos.append(set_field_if_exists('Photo 3:', staff_dict))
		self.photos.append(set_field_if_exists('Photo 4:', staff_dict))
		self.photos.append(set_field_if_exists('Please upload a photo for our website/marketing:', staff_dict))

		match self.role:
			case 'Director':
				self.meals = 'Full meal plan'
				self.housing = 'Lodging provided'
			case 'Faculty':
				self.meals = 'Full meal plan'
				self.housing = 'Lodging provided'

		# # fields outside of 'data' json
		self.regfox_id = set_field_if_exists('id', staff_dict)
		self.order_display_id = set_field_if_exists('order_display_id', staff_dict)
		self.created = set_field_if_exists('created', staff_dict)
		self.income = set_field_if_exists('income', staff_dict)

	def __str__(self):
		return f'{self.regfox_id}: {self.fname} {self.lname} ({self.role})'

	def to_str(self):
		return f'{self.regfox_id}: {self.fname} {self.lname} ({self.role})\n'

	def to_row(self):
		return [ [
		# Notes / First Name / Last Name / Email / Phone Number / Badge Name / Pronouns / Role
		None, self.fname, self.lname, self.email, self.phone, self.badge_name, self.pronouns, self.role,
		
		# Accompanying / Age / Maine? / NA / NA / NA / NA / Festival Pass / Volunteer
		self.who_accompanying, self.age, None, None, None, None, None, None, None,
		
		# Scholarship / Discipline / Group / Lodging / Roommate / Room Waitlist / Housing Needs / NA / NA
		None, self.discipline, self.group, self.housing, None, None, self.housing_needs, None, None,
		
		# Meals / Dietary Reqs / Other Reqs / Lobster / Meals Waitlist / City / State / Photo optout / Income
		self.meals, self.meal_reqs, self.meal_other_reqs, self.lobster, None, self.city, self.state, self.photo_optout, self.income,
		
		# Created / Entered / ID
		self.created, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), self.regfox_id
		] ]

	def bio_to_row(self):
		return [ [
		# First Name / Last Name / Bio / Classroom Reqs / Web URL
		self.fname, self.lname, self.bio, self.classroom_reqs, self.web_url,

		# FB profile / FB page / Insta / YouTube
		self.fb_profile_url, self.fb_page_url, self.insta_handle, self.youtube,

		# Video 1 / Video 2 / Spotify 1 / Spotify 2
		self.video1, self.video2, self.spotify1, self.spotify2,

		# Guests / Residency 
		self.guests, self.residency
		] ]
		