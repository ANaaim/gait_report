def extraction_info_enf(filename):
    # extraction du fichier contenant les pas
    fd = open(filename, 'r')
    text = fd.readlines()
    notes_exist = False
    notes = ''
    description_exist = False
    description = ''
    for lign in text:
        if 'NOTES' in lign:
            notes = lign
            notes_exist = True
        elif 'DESCRIPTION' in lign:
            description = lign
            description_exist = True
    return [notes, notes_exist, description, description_exist]
