from __future__ import print_function
import json
import requests
import sys

import util.map
import util.config_parser
from api import regfox
from participants.artist_guest import Artist_Guest
from participants.student import Student
from participants.chaperone import Chaperone


class FormIds:
	ARTIST_GUEST = util.config_parser.read_config()['artist_guest_form']
	STUDENT = util.config_parser.read_config()['student_form']
	CHAPERONE = util.config_parser.read_config()['chaperone_form']

def main():
	if len(sys.argv) != 2:
		print("Error! Usage: python3 search_by_registrant_id.py '<id>'")
		exit()
	else:
		id = sys.argv[1]
		response = json.loads(regfox.get_registrants_by_id(id))	
		data = response['data']
		form_id = data['formId']
		print('\n', data, '\n')
		
		role_dict = util.map.all_fields(data)
		print('\n', role_dict, '\n')

		match form_id:
			case FormIds.ARTIST_GUEST:
				artist_guest = Artist_Guest(role_dict)
				print(artist_guest.to_row(), '\n')
			case FormIds.STUDENT:
				student = Student(role_dict)
				print(student.to_row(), '\n')
			case FormIds.CHAPERONE:
				chaperone = Chaperone(role_dict)
				print(chaperone.to_row(), '\n')

if __name__ == '__main__':
	main()