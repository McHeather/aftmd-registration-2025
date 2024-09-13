from __future__ import print_function
import json
from datetime import datetime
import os.path
import requests
import sys

## Local Modules ##
# import waitlist
import api.google_drive.auth
import api.google_drive.upload
from api.mailchimp import tag_email
from api.regfox import get_registrants_by_form
import util.map
import util.file_io
from util import config_parser
from participants.artist_guest import Artist_Guest
from participants.crew import Crew
from participants.sound_engineer_guest import Sound_Engineer_Guest
from participants.student import Student
from participants.chaperone import Chaperone
from participants.board_member import Board_Member


def map_form_responses(form_id, participant_class, date_after='2024-08-01 12:00', date_before='2025-06-30 12:00'):
	new_participants = []
	
	complete_responses = json.loads(api.regfox.get_registrants_by_form(form_id, date_after, date_before, "COMPLETED"))
	pending_responses = json.loads(api.regfox.get_registrants_by_form(form_id, date_after, date_before, "PENDING FINAL PAYMENT"))
	waitlist_responses = json.loads(api.regfox.get_registrants_by_form(form_id, date_after, date_before, "WAITLISTED"))

	response_data = complete_responses['data'] + pending_responses['data'] + waitlist_responses['data']

	for response in response_data:
		participant = participant_class(util.map.all_fields(response))
		is_new_participant = util.file_io.is_new_registration(participant, 'participants.txt')
		
		if is_new_participant:
			new_participants.append(participant)

	return new_participants


def is_taking_classes(participant):
	return participant.discipline != ""


def is_artist(participant):
	return participant.role in ('Director', 'Faculty', 'Artist in Residence', 'Artistic Work Study Student')


def is_artist_or_crew(participant):
	return participant.role in ('Director', 'Faculty', 'Artist in Residence', 'Artistic Work Study Student', 'Crew', 'Sound Engineer', 'Board')


def is_scholarship(participant):
	return (participant.role in ('Student', 'Chaperone')) and (participant.scholarship == 'Yes')


def needs_chaperone(participant):
	if (participant.role == 'Student') and (participant.age in ('12 - 14', '15 - 17')):
		print("Adding chaperone (", participant.chaperone_email, ") to Mailchimp")
		return True
	else:
		return False


def is_waitlisted(participant):
	return (participant.room_waitlist != "" or participant.meals_waitlist != "")


def main():
	creds = api.google_drive.auth.authenticate()

	config_data = config_parser.read_config()	
	forms = {}
	forms[Artist_Guest] = config_data['artist_guest_form']
	forms[Crew] = config_data['crew_form']
	forms[Sound_Engineer_Guest] = config_data['sound_engineer_guest_form']
	forms[Student] = config_data['student_form']
	forms[Chaperone] = config_data['chaperone_form']
	forms[Board_Member] = config_data['board_form']

	new_participants = []
	for form_type, form_id in forms.items():
		participants = map_form_responses(form_id, form_type)
		new_participants += participants
	
	print("\nNew participants: ")
	for new_participant in new_participants:	
	
		print(new_participant)
		api.google_drive.upload.append_registrant(creds, config_data['reg_master_sheet'], "A1:BA1", "USER_ENTERED", new_participant.to_row())
		
		## Check if extra uploads are needed ##

		if is_taking_classes(new_participant):
			api.mailchimp.tag_email(new_participant.email, "2025-students")

		if is_artist(new_participant):
			api.google_drive.upload.append_registrant(creds, config_data['bios_sheet'], "A1:BA1", "USER_ENTERED", new_participant.bio_to_row())
		
		if is_artist_or_crew(new_participant):
			api.mailchimp.tag_email(new_participant.email, "2025-artists-crew")

		if is_scholarship(new_participant):
			api.google_drive.upload.append_registrant(creds, config_data['scholarships_sheet'], "A1:BA1", "USER_ENTERED", new_participant.applicant_to_row())
		
		if needs_chaperone(new_participant):
			api.mailchimp.tag_chaperone(new_participant.chaperone_email, "2025-chaperones")

		# if is_waitlisted(new_participant):
		# waitlist.upload_to_room_meals_waitlist(new_participant)

	print("\n> registration_master.py finished running at", datetime.now())


if __name__ == '__main__':
	main()
