from __future__ import print_function
import json
import requests
import sys

import util.map
from api import regfox
from participants.artist_guest import Artist_Guest
from participants.student import Student


class FormIds:
	ARTIST_GUEST = 758563
	STUDENT = 759287


def main():
	if len(sys.argv) != 2:
		print("Error! Usage: python3 search_by_registrant_id.py '<id>'")
		exit()
	else:
		id = sys.argv[1]
		response = json.loads(regfox.registrants_by_id(id))	
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

		# faculty photos url
		# https://s3.amazonaws.com/uploads.form.webconnex.com/store/01H9R2FP45QGTD4FFRG/sammy-photo-2023-qrvjf.jpg

if __name__ == '__main__':
	main()