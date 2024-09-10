def get_existing_ids(filename):
	f = open(filename,'r')
	content = f.readlines()
	f.close()
	return [line.split(':')[0] for line in content]


def is_new_registration(participant, filename='participants.txt'):
	existing_ids = get_existing_ids(filename)

	log = open(filename, 'a')
	if participant.regfox_id not in existing_ids:
		log.write(participant.to_str())
		log.close()
		return True

	else:
		return False