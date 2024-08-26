def all_fields(participant):
	fields_dict = {}
	
	fields_dict['id'] = str(participant['id'])
	fields_dict['order_display_id'] = participant['orderDisplayId']
	fields_dict['income'] = participant['amount']
	fields_dict['created'] = participant['dateCreated']

	field_data = participant['fieldData']
	for field in field_data:
		if 'value' in field:
			fields_dict[field['label']] = field['value']
		# see field_structure.txt for the annoying structure which necessitates this
		# for fields which are not free text, the label and value are stored in different fields
		if 'amount' in field:
			fields_dict[preceding_field_label] = field['label']
		preceding_field_label = field['label']

	for field in field_data:
		# go back and treat like a free text field, rather than a double-field data format (see field_structure.txt)
		if field['label'] == 'If you wish for the name on your badge to appear differently to the one entered above, please let us know here:':
			fields_dict[field['label']] = field['value']

	fname_lname_email(field_data, fields_dict)
	
	return fields_dict


def fname_lname_email(field_data, fields_dict):
	# participant name gets overwritten by emergency contact name
	# reset participant name here
	for field in field_data:
		if field['label'] == 'First Name' and field['path'] == 'name.first':
			fields_dict[field['label']] = field['value']
		if field['label'] == 'Last Name' and field['path'] == 'name.last':
			fields_dict[field['label']] = field['value']
		
		# email gets overwritten by 'share email to camp list', so also reset here
		if field['label'] == 'Email' and field['path'] == 'email':
			fields_dict[field['label']] = field['value']
		# faculty email field
		if field['label'] == 'Preferred email for communications' and field['path'] == 'preferredEmailForCommunications':
			fields_dict[field['label']] = field['value']
	return fields_dict


def set_field_if_exists(field_name, role_dict):
	if field_name in role_dict:
		return role_dict[field_name]
	else:
		return ""

def set_blank_na(field_data):
	if field_data == "":
		return "NA"
	else:
		return field_data
