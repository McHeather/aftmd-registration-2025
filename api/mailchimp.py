# see https://mailchimp.com/developer/marketing/api/list-members/

import mailchimp_marketing as MailchimpMarketing
from mailchimp_marketing.api_client import ApiClientError
from util import config_parser


def tag_email(email, tag):
  MAILCHIMP_API_KEY = config_parser.read_config()['mailchimp_api_key']
  ACADIA_TRAD_LIST_ID = config_parser.read_config()['acadia_trad_list_id']

  add_email(email)

  try:
    client = MailchimpMarketing.Client()
    client.set_config({
      "api_key": MAILCHIMP_API_KEY,
      "server": "us5"
    })

    response = client.lists.update_list_member_tags(ACADIA_TRAD_LIST_ID, email, {"tags": [{"name": tag, "status": "active"}]})
  except ApiClientError as error:
    print("Error: {}".format(error.text))


def add_email(email):
  MAILCHIMP_API_KEY = config_parser.read_config()['mailchimp_api_key']
  ACADIA_TRAD_LIST_ID = config_parser.read_config()['acadia_trad_list_id']

  try:
    client = MailchimpMarketing.Client()
    client.set_config({
      "api_key": MAILCHIMP_API_KEY,
      "server": "us5"
    })

    response = client.lists.set_list_member(ACADIA_TRAD_LIST_ID, email, {"email_address": email, "status_if_new": "subscribed"})
  except ApiClientError as error:
    print("Error: {}".format(error.text))