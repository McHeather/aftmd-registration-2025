from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

import requests

def append_registrant(credentials, spreadsheet_id, range_name, value_input_option, values):
	# https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets.values/append
	try:
		service = build('sheets', 'v4', credentials=credentials)
		body = {'values': values}
		result = service.spreadsheets().values().append(spreadsheetId=spreadsheet_id, range=range_name, valueInputOption=value_input_option, body=body).execute()
		# print(f"Range {result['updates']['updatedRange']} updated.\n")
		return result
	
	except HttpError as error:
		print(f"An error occurred: {error}")
		return error


# # Aug 2025: RegFox has changed security around photo downloads - can no longer access from API 

# def upload_media(credentials, folder_id, photos):
# 	try:
# 		service = build('drive', 'v3', credentials=credentials)
# 		for photo in photos:
# 			print("- Uploading "+photo+"...")
# 			file_metadata = {'name': photo,
# 							'parents': [folder_id]}
# 			photo = MediaFileUpload(photo,
# 									mimetype='image/jpeg')
# 			file = service.files().create(body=file_metadata, media_body=photo, uploadType='media',
# 										  fields='id', supportsAllDrives=True).execute()

# 	except HttpError as error:
# 		print(f'An error occurred: {error}')

# def upload_photos(credentials, staff_dict):
# 	photos = []
# 	for count, photo in enumerate(staff_dict.photos):
# 		if photo != '':
# 			# get photos from RegFox S3 bucket and save locally
# 			try:
# 				data = requests.get("https://s3.amazonaws.com/uploads.form.webconnex.com/store/"+staff_dict.order_display_id+"/"+photo).content
# 				photos.append(staff_dict.fname+" "+str(count)+'.jpg')
# 				f = open(staff_dict.fname+" "+str(count)+'.jpg','wb')
# 				f.write(data)
# 				f.close()
# 			except RuntimeError as error:
# 				print(f'An error occurred: {error}')

# 	upload_media(credentials, FACULTY_PHOTOS_FOLDER_ID, photos)

# def upload_maine_ids(credentials, student_dict):
# 	photos = []
# 	maine_id = student_dict.maine_id
# 	if maine_id != '':
# 		# get photos from RegFox S3 bucket and save locally
# 			try:
# 				data = requests.get("https://s3.amazonaws.com/uploads.form.webconnex.com/store/"+student_dict.order_display_id+"/"+maine_id).content
# 				photos.append(student_dict.fname+" "+student_dict.lname+'.jpg')
# 				f = open(student_dict.fname+" "+student_dict.lname+'.jpg','wb')
# 				f.write(data)
# 				f.close()
# 			except RuntimeError as error:
# 				print(f'An error occurred: {error}')

# 	upload_media(credentials, GOOGLE_MAINE_IDS_FOLDER, photos)