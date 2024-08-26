# see https://docs.webconnex.io/api/v2/#api-reference
	
import requests
import util.config_parser

def registrants_by_form(form_id, date_after, date_before, status):
	REGFOX_API_KEY = util.config_parser.read_config()['regfox_api_key']

	try:
		response = requests.get(
			url="https://api.webconnex.com/v2/public/search/registrants",
			params={
				"product": "regfox.com",
				"formId": form_id,
				"sort": "asc",
				"dateCreatedAfter": date_after,
				"dateCreatedBefore": date_before,
				"status": status,
				"limit": 250
			},
			headers={
				"apiKey": REGFOX_API_KEY,
			},
		)
		# print('Response HTTP Status Code: {status_code}'.format(
			# status_code=response.status_code))
		return response.content
	except requests.exceptions.RequestException:
		print('HTTP Request failed')


def registrants_by_id(id):
	REGFOX_API_KEY = util.config_parser.read_config()['regfox_api_key']

	try:
		response = requests.get(
			url="https://api.webconnex.com/v2/public/search/registrants/"+id,
			params = {},
			headers = {
				"apiKey": REGFOX_API_KEY,
			},
		)
		return response.content
	except requests.exceptions.RequestException:
		print("HTTP Request failed")