import matplotlib.pyplot as plt
import pandas as pd
from db_helper import getMeansPerMonth
import numpy as np

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

def getData(post_data):
    need_kid = post_data.get('kid', None)
    need_daterange = post_data.get('datarange', None)

    if need_kid == None and need_daterange == None:
        if post_data.get('dataplot') == 'Means':
            try:
                program = post_data.get('program')
                incident_type = post_data.get('incident')
                x,y = getMeansPerMonth(incident_type)
            except Exception as e:
                print(e)

            return x,y,program,incident_type
    
# Given a labeled x and y data set, generate and return a bar graph plot object
def makeBarGraph(post_data):
    x,y,program,incident_type = getData(post_data)
    x_key = [*x][0]
    y_key = [*y][0]

    x_labels = []
    frequencies = None
    try:
        plot_title = program + '-' + incident_type + ': ' + x_key+ ' vs ' + y_key

        for item in x[x_key]:
            x_labels.append(x_key.split(' ')[0] +' '+ (str(item)))

        frequencies = y[y_key]
        freq_series = pd.Series(frequencies)

        # Plot the figure.
        plt.figure(figsize=(12, 8))
        ax = freq_series.plot(kind='bar')
        ax.set_title(plot_title)
        ax.set_xlabel(x_key)
        ax.set_ylabel(y_key)
        ax.set_xticklabels(x_labels, rotation=40, ha='center')

        rects = ax.patches
        # For each bar: Place a label
        for rect in rects:
            # Get X and Y placement of label from rect.
            y_value = rect.get_height()
            x_value = rect.get_x() + rect.get_width() / 2

            # Number of points between bar and label. Change to your liking.
            space = 5
            # Vertical alignment for positive values
            va = 'bottom'

            # If value of bar is negative: Place label below bar
            if y_value < 0:
                # Invert space to place label below
                space *= -1
                # Vertically align label at top
                va = 'top'

            # Use Y value as label and format number with one decimal place
            label = "{}".format(y_value)

            

            # Create annotation
            plt.annotate(label, (x_value, y_value), xytext=(0, space), textcoords="offset points", ha='center', va=va)
        # properties = {"rotation" : 90}
        # plt.setp(ax.get_xticklabels(), **properties)
        return plt, plot_title

    except Exception as e:
        print(e)

    

    # index = np.arange(len(x_labels))
    # plt.bar(index, y['means'])

    # plt.xlabel([*x][0], fontsize=14)
    # plt.ylabel([*y][0], fontsize=14)
    # plt.xticks(index, x_labels, fontsize=8, rotation=30)
    # plt.title(incident_type+': '+ [*x][0]+' vs '+[*y][0])

   
   