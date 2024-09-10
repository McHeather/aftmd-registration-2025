import configparser
 
def read_config():
    config = configparser.ConfigParser()
 
    config.read('config.ini')
 
    # Access values from the configuration file
    regfox_api_key = config.get('Keys', 'REGFOX_API_KEY')
    mailchimp_api_key = config.get('Keys', 'MAILCHIMP_API_KEY')
  
    reg_master_sheet = config.get('Google Sheets', 'REG_MASTER_SHEETS_ID')
    bios_sheet = config.get('Google Sheets', 'BIOS_SHEETS_ID')
    scholarships_sheet = config.get('Google Sheets', 'SCHOLARSHIPS_SHEETS_ID')
    
    artist_guest_form = config.get('RegFox Forms', 'ARTIST_GUEST_FORM_ID')
    crew_form = config.get('RegFox Forms', 'CREW_FORM_ID')
    sound_engineer_guest_form = config.get('RegFox Forms', 'SOUND_ENGINEER_GUEST_FORM_ID')
    student_form = config.get('RegFox Forms', 'STUDENT_FORM_ID')
    chaperone_form = config.get('RegFox Forms', 'CHAPERONE_FORM_ID')
    board_form = config.get('RegFox Forms', 'BOARD_FORM_ID')


    acadia_trad_list_id = config.get('Mailchimp', 'ACADIA_TRAD_LIST_ID')
 
    # Return a dictionary with the retrieved values
    config_values = {
        'regfox_api_key': regfox_api_key,
        'mailchimp_api_key': mailchimp_api_key,
        
        'reg_master_sheet': reg_master_sheet,
        'bios_sheet': bios_sheet,
        'scholarships_sheet': scholarships_sheet,
        
        'artist_guest_form': artist_guest_form,
        'crew_form': crew_form,
        'sound_engineer_guest_form': sound_engineer_guest_form,
        'student_form': student_form,
        'chaperone_form': chaperone_form,
        'board_form': board_form,
        
        'acadia_trad_list_id': acadia_trad_list_id
    }
 
    return config_values