  #!/usr/bin/env python3
###################################################################
#
#   CSSE1001/7030 - Assignment 1
#
#   Student Username: s4396043
#
#   Student Name: Armaan Dhaliwal-McLeod
#
###################################################################

#####################################
# Support given below - DO NOT CHANGE
#####################################

from assign1_support import *

#####################################
# End of support 
#####################################

# Add your code here


def interact():
    """prints "Welcome to the Stastistic Summariser!". Then prompts the user to enter the name
    of the data filename. Then prompts commands for the user.

    interact(None) -> None
    """
    print('Welcome to the Statistic Summariser')
    print('')
    filename = input("Please enter the data source file: ")
    data = load_data(filename) 
    while True: 
        print('')
        command = input("Command: ")
        command_str = command 
        command = command.split()#splits command into separate conditions
        if 'summary' in command:
            display_set_summaries(data_summary(data)) 
        elif 'sets' in command and len(command) >= 2: #checks whether sets is equal or less than 2, with 2 2 True booleans
            new_list = [] 
            sets_data = [] 
            for x in command[1:]: 
                new_list.append(int(x)) #appends integers to new_list for testing of 'sets'
            for i in new_list: #loop through list checking for indices 
                sets_data.append(data_summary(data)[i]) #appends indices to 'sets'
            display_set_summaries(sets_data) #displays sets in term of indices after 'sets'
        elif command[0] == 'q':
            break  
        else:
            print ("Unknown command: "+ command_str) 
            
       
def load_data(filename): 
    """Return data(string) into a list of tuples containing the subset name(string)
    along with a list of floating point data values. 

    load_data(str) -> list[tup(str,list[float])]
    """
    fd = open(filename,'r')
    data = fd 
    datalist = [] #first list in data
    for x in data:
        if x.strip(): #strips whitespaces between points
            a = x.split(',',1) #splits comma between string and floats but puts extra space
            num = a[1]
        datalist2 = [] #second list in data
        for x in num.split(','): #similar to above but splits each row with commas
            x = float(x) 
            datalist2.append(x)
        y = (a[0],) + (datalist2,) #adding subset inside tuple to list of floats in list
        datalist.append(y) 
    fd.close()
    return datalist

def get_count(data):
    """Returns number of floating point values in data sets.

    get_count(str) -> len(range[start,end])
    """
    count = len(data) 
    return count 

def get_ranges(data):
    """Returns maximum and minimum of data sets respectively. Takes a list
    of floating point numbers and returns tuple containing two floats.
    
    get_ranges(str)-> (tuple,tuple)
    """
    minimum = min(data) 
    maximum = max(data)
    return minimum,maximum
    
def get_mean(data): 
    """Returns the mean from a list of datapoints.

    get_mean(str) -> float
    """
    total_sum = sum(data) 
    length = len(data)
    average = total_sum / length #exactly like calculating it on paper
    return average
   
def get_median(data):
    """Returns the middle value(median) from the list of data points. The average
    of the two middle points will return.

    get_median(str) -> float
    """
    new_data = sorted(data)
    x = len(new_data)
    if x % 2 == 0: #if count of data has no remainders,then apply
        return(float(new_data[(x//2)]) + float(new_data[((x//2)-1)]))/2 #top + bottom middle values and dividing by integer to give back float
    else: #if remainders, then apply
        return float(new_data[(x//2)]) # middle value is easily attainable because odd number of data
        
def get_std_dev(data):
    """Returns Standard Deviation of those lists of data points.

    get_std_dev(str) -> float
    """
    values = data
    length = len(values) 
    average = sum(values)/len(values) # need average to calculate std dev
    result = 0 #we need to add up numbers for equation
    for x in range(length):
        result += (values[x] - average )**2 # adding to result to cycle through numbers
    sd = result*1.0/length #using 1.0 to get float
    return sd**0.5 
    

def data_summary(data):
    """Returns the Summary Statistics in a list of tuples from each subset. This
    is taken from load_data(filename). 

    data_summary(str) -> list[tuple]
    """
    summary_list= [] #starting off with a list, as required
    for x in range(len(data)): # looping through start and end of data
        names = data[x][0] #indexing 0 to extract string names out of data
        count = get_count(data[x][1]) # indexing 1 to extract count out of list of floats
        mean = get_mean(data[x][1])
        median = get_median(data[x][1])
        ranges = get_ranges(data[x][1])
        sd = get_std_dev(data[x][1])
        summary = (names,count,mean,median,ranges[0],ranges[1],sd) #summing everything into tuple
        summary_list.append(summary) 
        
    return summary_list
    
def display_set_summaries(data):
    """Displays the summary information for the data set summaries. Same
    format as returned from data_summary(data) except values are rounded to two
    decimal places .Returns None and prints to stdout.
    
    display_set_summaries(list) -> None
    """
    print('Set Summaries') 
    print('')
    h1 = "" #Starting off by setting strings to variables
    h2 = "Count:"
    h3 = "Mean:"
    h4 = "Median:"
    h5 = "Minimum:"
    h6 = "Maximum:"
    h7 = "Std Dev:"
    headers = [h1,h2,h3,h4,h5,h6,h7] # adding headings to total list
    data_list = range(0,len(headers))  
    for x in data_list: #looping through the headers, start to end
        display_with_padding(headers[x]) # using support file to format headings
        y = 0 #setting variable to 0, to check if numbers in data equal zero or not
        for number in data:
            if x != y: # if not, round number
                display_with_padding(round(number[x],2))
            elif x == y: # if yes, do not round as it is not required
                display_with_padding(number[x])
            else:
                print("Unable to display Set Summaries") # if data has numbers, impossible to display summary
        print("")
          
def display_with_padding(s):
    """
    Something to print stuff prettily.

    display_with_padding(str) -> None
    
    """
    print("{0: <15}".format(s), end = '')   
##################################################
# !!!!!! Do not change (or add to) the code below !!!!!
# 
# This code will run the interact function if
# you use Run -> Run Module  (F5)
# Because of this we have supplied a "stub" definition
# for interact above so that you won't get an undefined
# error when you are writing and testing your other functions.
# When you are ready please change the definition of interact above.
###################################################

if __name__ == '__main__':
    interact()
