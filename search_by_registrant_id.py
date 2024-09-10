from __future__ import print_function
import json
import requests
import sys

from util import map, config_parser
from api import regfox
from participants.artist_guest import Artist_Guest
from participants.student import Student
from participants.chaperone import Chaperone
from participants.crew import Crew
from participants.sound_engineer_guest import Sound_Engineer_Guest
from participants.board_member import Board_Member

def main():
	if len(sys.argv) != 2:
		print("Error! Usage: python3 search_by_registrant_id.py '<id>'")
		exit()
	
	else:
		id = sys.argv[1]
		
		response = json.loads(regfox.get_registrants_by_id(id))	
		response_data = response['data']
		form_id = str(response_data['formId'])
		print('\n', response_data, '\n')

		# try to map the registrant to a known form role
		config_data = config_parser.read_config()	
		forms = {}
		forms[config_data['artist_guest_form']] = Artist_Guest
		forms[config_data['crew_form']] = Crew
		forms[config_data['sound_engineer_guest_form']] = Sound_Engineer_Guest
		forms[config_data['student_form']] = Student
		forms[config_data['chaperone_form']] = Chaperone
		forms[config_data['board_form']] = Board_Member

		participant_dict = map.all_fields(response_data)

		participant = forms[form_id](participant_dict)

		print(participant.to_row(), '\n')

if __name__ == '__main__':
	main()