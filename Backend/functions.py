import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from db_helper import getMeansPerMonth
import numpy as np
import os, shutil


# Check if a filename ends in the proper extension
def validFile(filename):
    if filename.rsplit('.', 1)[1] in set(['xlsx', 'xls', 'csv']):
        return True
    return False

def cleanExcelFiles():
    directory = "csvs"
    files = os.listdir(directory)

    for file in files:
        if file.endswith(".xlsx"):
            os.remove(os.path.join(directory, file))     

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
    kid = post_data.get('kid', None)
    daterange = post_data.get('datarange', None)

    if kid == None and daterange == None:
        if post_data.get('dataplot') == 'Means':
            try:
                program = post_data.get('program')
                incident_type = post_data.get('incident')
                x,y = getMeansPerMonth(incident_type,0,0)
                return x,y,program,incident_type
            except Exception as e:
                print(e)

           
    
    if kid and daterange:
        if post_data.get('dataplot') == 'Means':
            try:
                program = post_data.get('program')
                incident_type = post_data.get('incident')
                x,y = getMeansPerMonth(incident_type,kid,daterange)
                return x,y,program,incident_type
            except Exception as e:
                print(e)

    if kid:
         if post_data.get('dataplot') == 'Means':
            try:
                program = post_data.get('program')
                incident_type = post_data.get('incident')
                x,y = getMeansPerMonth(incident_type,kid,0)
                return x,y,program,incident_type
            except Exception as e:
                print(e)
    
    elif daterange:
         if post_data.get('dataplot') == 'Means':
            try:
                program = post_data.get('program')
                incident_type = post_data.get('incident')
                x,y = getMeansPerMonth(incident_type,0,daterange)
                return x,y,program,incident_type
            except Exception as e:
                print(e)

    return None,None,None,None

   
    
# Given a labeled x and y data set, generate and return a bar graph plot object
def makeBarGraph(post_data):
    # Get requested data from the db
    x,y,program,incident_type = getData(post_data)

    if x is None:
        return

    custom_title = post_data.get('filename')        


    # Parse the x and y keys
    # Example: x=month in placement,  y=mean percentage
    x_key = [*x][0]
    y_key = [*y][0]

    plot_title = ''
    file_name = ''
    
    # Create title and file names
    if custom_title:
        plot_title = custom_title
        file_name = f'{custom_title}.png'
    else:
        kid = post_data.get('kid')
        date = post_data.get('datarange')
        print(date)


        if kid:
            plot_title += f'{kid}-'
            file_name += f'{kid}-'
        
        if date:
            plot_title += f'{date}-'
            file_name += f'{date}-'

        plot_title += f'{program}-{incident_type}: {x_key} vs {y_key}'
        file_name += f'{program}{incident_type}{x_key}vs{y_key}.png'

    destination = 'static/images/'

   
    x_labels = []
    frequencies = None
    try:
        # Create a label for every X tick on the bar graph
        # Example: Month 1, Month 2, ...
        for item in x[x_key]:
            x_labels.append(x_key.split(' ')[0] +' '+ (str(item)))

        # Get the frequencies
        frequencies = y[y_key]
        freq_series = pd.Series(frequencies)

        # Define the plot figure
        plt.figure(figsize=(16, 9))
        ax = freq_series.plot(kind='bar')
        ax.set_title(plot_title)
        ax.set_xlabel(x_key)
        ax.set_ylabel(y_key)
        ax.set_xticklabels(x_labels, rotation=40, ha='center')
        # ax.set_ylim(bottom=0.0)
        # ax.set_xlim(left=0.0)

        # Get the list of bar objects
        rects = ax.patches

        # For each bar: Place a label
        for rect in rects:
            # Get X and Y placement of label from rect.
            y_value = rect.get_height()
            x_value = rect.get_x() + rect.get_width() / 2

            # Number of points between bar and label
            space = 5

            # Vertical alignment for positive values
            va = 'bottom'

            # If value of bar is negative: Place label below bar
            # if y_value < 0:
                # Invert space to place label below
                # space *= -1
                # Vertically align label at top
                # va = 'top'

            # Use Y value as label and format number with one decimal place
            label = "{}".format(y_value)

            # Create annotation
            plt.annotate(label, (x_value, y_value), xytext=(0, space), textcoords="offset points", ha='center', va=va)

        # Save the figure as a png and move it to the right directory
        plt.savefig(file_name)
        shutil.move(os.path.join('.', file_name), os.path.join(destination, file_name))
        
        # Close the figure to avoid memory issues
        plt.clf()

        # Return the title and the filename
        print(plot_title,file_name)
        return plot_title, file_name
    except Exception as e:
        print(e)

def makeChartDict(data):
    d = {}
    chart_data = data.split(',')
    for key_vals in chart_data:
        key,val = key_vals.split(':')
        d.update({ key:val })
    return d