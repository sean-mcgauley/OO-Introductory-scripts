class Time:
    pass


time = Time()
time.hours = 11
time.minutes = 59
time.seconds = 30


def printTime(timeObj):
    print(str(timeObj.hours) + ':' + str(timeObj.minutes)
          + ':' + str(timeObj.seconds))


def convertToSeconds(t):
    minutes = t.hours * 60 + t.minutes
    seconds = minutes * 60 + t.seconds
    return seconds


def makeTime(seconds):
    time = Time()
    # returns quotient less remainder which equals total hours
    time.hours = seconds // 3600
    # returns remainder of time.hours and divides by 60 which equals minutes
    time.minutes = (seconds % 3600) // 60
    # returns remainder of seconds over 60, since remainder will
    # be smallest remainder of 60 this makes sense
    time.seconds = seconds % 60

    printTime(time)


def increment(timeObj, seconds):
    # Create pure function by instantiating a new object
    new_time = Time()
    new_time.seconds = timeObj.seconds + (seconds % 60)
    new_time.minutes = timeObj.minutes + ((seconds % 3600) // 60)
    new_time.hours = timeObj.hours + (seconds // 3600)
    if new_time.minutes >= 60:
        new_time.hours += (new_time.minutes // 60)
        new_time.minutes -= 60
    if new_time.hours >= 24:
        new_time.hours = new_time.hours % 24

    printTime(timeObj)
    printTime(new_time)
