def existing_ids(filename):
	f = open(filename,'r')
	content = f.readlines()
	f.close()
	return [line.split(':')[0] for line in content]