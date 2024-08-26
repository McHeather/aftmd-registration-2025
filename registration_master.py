from __future__ import print_function
import json
from datetime import datetime
import os.path
import requests
import sys

# import waitlist
import api.google_drive.auth
import api.google_drive.upload
import api.mailchimp
import api.regfox
import util.map
import util.file_io
from util import config_parser
from participants.artist_guest import Artist_Guest
from participants.student import Student
from participants.chaperone import Chaperone


def main(date_after='2024-08-01 12:00', date_before='2025-06-30 12:00'):
	creds = api.google_drive.auth.authenticate()

	config_data = config_parser.read_config()
	
	forms = {}
	forms['Artist_Guest'] = config_data['artist_guest_form']
	forms['Student'] = config_data['student_form']
	forms['Chaperone'] = config_data['chaperone_form']

	participants = []
	for role, form_id in forms.items():
		response_complete = json.loads(api.regfox.registrants_by_form(form_id, date_after, date_before, "COMPLETED"))
		response_pending = json.loads(api.regfox.registrants_by_form(form_id, date_after, date_before, "PENDING FINAL PAYMENT"))
		# response_waitlist = json.loads(api.regfox.registrants_by_form(form_id, date_after, date_before, "WAITLISTED"))
		
		# deal with class waitlists in its own module - they are not registrants yet
		# waitlist.class_waitlist(response_waitlist['data'])
		
		data = response_complete['data'] + response_pending['data']
		for participant in data:
			match role:
				case 'Artist_Guest':
					artist_guest = Artist_Guest(util.map.all_fields(participant))
					participants.append(artist_guest)
				case 'Student':
					print(participant)
					student = Student(util.map.all_fields(participant))
					participants.append(student)
				case 'Chaperone':
					print(participant)
					chaperone = Chaperone(util.map.all_fields(participant))
					participants.append(chaperone)

	existing_ids = util.file_io.existing_ids('participants.txt')
	
	# append participants list with new participants
	new_participants = []
	log = open('participants.txt', 'a')
	for participant in participants:
		if participant.regfox_id not in existing_ids:
			log.write(participant.to_str())
			new_participants.append(participant)
	log.close()
	
	print("\nNew participants: ")
	for new_participant in new_participants:	
		
		print(new_participant)
		api.google_drive.upload.append_registrant(creds, config_data['reg_master_sheet'], "A1:BA1", "USER_ENTERED", new_participant.to_row())
		
		# if new_participant.room_waitlist != "" or new_participant.meals_waitlist != "":
			# waitlist.upload_to_room_meals_waitlist(new_participant)

		if new_participant.role in ('Director', 'Faculty', 'Artist in Residence', 'Artistic Work Study Student'):
			api.google_drive.upload.append_registrant(creds, config_data['bios_sheet'], "A1:BA1", "USER_ENTERED", new_participant.bio_to_row())
				
		if (new_participant.role in ('Student', 'Chaperone')) and (new_participant.scholarship == 'Yes'):
			api.google_drive.upload.append_registrant(creds, config_data['scholarships_sheet'], "A1:BA1", "USER_ENTERED", new_participant.applicant_to_row())
		
		if (new_participant.role == 'Student') and (new_participant.age in ('12 - 14', '15 - 17')):
			print("Adding chaperone (", new_participant.chaperone_email, ") to Mailchimp")
			api.mailchimp.tag_chaperone(new_participant.chaperone_email)

	print("\n> registration_master.py finished running at", datetime.now())


if __name__ == '__main__':
	main()
