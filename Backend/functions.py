def validFile(filename):
    EXTENSTIONS = set(['xlsx', 'xls', 'csv'])
    if filename.rsplit('.', 1)[1] in EXTENSTIONS:
        return True
    return False