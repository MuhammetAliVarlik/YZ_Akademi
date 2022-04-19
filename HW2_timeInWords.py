# Function to convert 24 hour time format to 12 hour time format.
def twentyFourToTwelve(h):  # It only takes the time value as integer input
    if h > 12:  # if the number is greater than 12, the number minus 12 is our converted value
        h = h - 12
    return h  # returns the result


# ----------------------------------------------------------------------------------------------------------------------
# Function that converts time variable to text
def timeToWords(h, m):  # It takes the hour value (h) and the minute value (m) as integer input
    minutes_array = ['', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine',
                     'ten', 'eleven', 'twelve', 'thirteen', 'fourteen', 'quarter', 'sixteen', 'seventeen', 'eighteen',
                     'nineteen',
                     ]  # text equivalent of minutes
    hours_array = ['', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'eleven',
                   'twelve']  # text equivalent of minutes
    if m < 20:
        if m == 15 or m == 0:  # quarter and o' clock are special cases and we don't need to use "minutes"
            m = minutes_array[m]
        else:
            m = minutes_array[m] + " minutes"
    elif 20 <= m < 30:
        # Since the numbers between 20 and 30 are in the format of twenty+ones digits, I did not include this part in
        # the array. I used the text equivalent of the ones digit
        if int(str(m)[1]) != 0:
            m = "twenty " + minutes_array[int(str(m)[1])] + " minutes"
        else:
            m = "twenty minutes"
    else:
        m = "half"
    h = hours_array[h]
    return h, m  # returns str equivalent of hours and minutes


# ----------------------------------------------------------------------------------------------------------------------
#   main function

def timeInWords(h, m):  # timeInWords returns the text equivalent of the entered hour and minute variables.

    # Constraints control
    if h < 1 or h > 23:
        print("Error! The operation cannot be performed.Hour must be between 1 and 23")
        return 0  # exit code
    if m < 0 or m > 59:
        print("Error! The operation cannot be performed.Minutes must be between 0 and 59")
        return 0  # exit code
    h = twentyFourToTwelve(h)  # to convert 24h format to 12h format

    # to print to the screen in the appropriate order
    if 30 >= m >= 1:
        t = "past"
        hiw, miw = timeToWords(h, m)
        print("{} {} {}".format(miw, t, hiw))
    elif m == 0:
        t = "o' clock"
        hiw, miw = timeToWords(h, m)
        print("{} {} {}".format(hiw, t, miw))
    else:
        m = 60 - m
        h = h + 1
        t = "to"
        hiw, miw = timeToWords(h, m)
        print("{} {} {}".format(miw, t, hiw))


# ----------------------------------------------------------------------------------------------------------------------
# To catch ValueError and output a warning to the screen
try:
    print("The timeInWords function is to print the entered hour and minute on the screen.\n\ntimeInWords function "
          "has 2 inputs:\nIn the first line, the hour value must be entered as an integer and 1<=hour<=23 \nIn the "
          "second line, the minutes value must be entered as an integer and 0<=minutes<=59.")
    hour = int(input())  # in integer format
    minutes = int(input())  # in integer format
    timeInWords(hour, minutes)  # Call main function
except ValueError:
    print("Error! The operation cannot be performed.Hour and minutes must be in integer form")
