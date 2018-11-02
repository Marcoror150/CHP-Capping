# Check if a filename ends in the proper extension
def validFile(filename):
    if filename.rsplit('.', 1)[1] in set(['xlsx', 'xls', 'csv']):
        return True
    return False

# Cleanse input from bad characters
def cleanse(input):
    output = cleanseWhiteSpace(input)
    output = output.replace(',', '')
    output = output.replace('-', '')
    output = output.replace('\r', '')
    output = output.replace('\n', '')
    return output

# Cleanses items in a list
def cleanseMany(input):
    for i, item in enumerate(input):
        input[i] = cleanse(item)
    return input

# Cleanse input from whitespace
def cleanseWhiteSpace(input):
    return input.replace(' ', '')

# Strip all characters that are not numbers or decimal
def cleanseNonNumbers(input):
    regex = re.compile(r'[^0-9^.,]')
    return regex.sub('', input)