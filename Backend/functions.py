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

def makeBarGraph(incident_type):
    x,y = getMeansPerMonth(incident_type)
    x_labels = []
    for month in x['months']:
        x_labels.append('Month '+(str(month)))

    # index = np.arange(len(x_labels))
    # plt.bar(index, y['means'])

    # plt.xlabel([*x][0], fontsize=14)
    # plt.ylabel([*y][0], fontsize=14)
    # plt.xticks(index, x_labels, fontsize=8, rotation=30)
    # plt.title(incident_type+': '+ [*x][0]+' vs '+[*y][0])

    frequencies = y['means']
    freq_series = pd.Series(frequencies)

    # Plot the figure.
    plt.figure(figsize=(12, 8))
    ax = freq_series.plot(kind='bar')
    ax.set_title(incident_type+': '+ [*x][0]+' vs '+[*y][0])
    ax.set_xlabel([*x][0])
    ax.set_ylabel([*y][0])
    ax.set_xticklabels(x_labels)

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
        plt.annotate(
            label,                      # Use `label` as label
            (x_value, y_value),         # Place label at end of the bar
            xytext=(0, space),          # Vertically shift label by `space`
            textcoords="offset points", # Interpret `xytext` as offset in points
            ha='center',                # Horizontally center label
            va=va)                      # Vertically align label differently for
                                        # positive and negative values.

    plt.show()