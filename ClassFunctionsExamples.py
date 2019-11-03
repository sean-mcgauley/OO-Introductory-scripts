class Time:
    pass


time = Time()
time.hours = 11
time.minutes = 59
time.seconds = 30


def printTime(timeObj):
    print(str(timeObj.hours) + ':' + str(timeObj.minutes)
          + ':' + str(timeObj.seconds))


def addTime(t1, t2):
    sumT = Time()
    sumT.hours = t1.hours + t2.hours
    sumT.minutes = t1.minutes + t2.minutes
    sumT.seconds = t1.seconds + t2.seconds

    if sumT.seconds >= 60:
        sumT.seconds -= 60
        sumT.minutes += 1

    if sumT.minutes >= 60:
        sumT.minutes -= 60
        sumT.hours += 1

    return sumT


def increment(timeObj, seconds):
    # Create pure function by instantiating a new object
    new_time = Time()
    # assign new object OG object seconds + increment
    new_time.seconds = timeObj.seconds + seconds
    # divmod creates tuple of Q quotient and R remainder, assign
    # two variables (add_mins, remain_seconds) then modify timeObj attributes
    # and assign these values to new_time attributes
    add_mins, remain_seconds = divmod(new_time.seconds, 60)
    new_time.seconds = remain_seconds
    new_time.minutes = timeObj.minutes + add_mins
    # modify new_time hours
    add_hours, remain_minutes = divmod(new_time.minutes, 60)
    new_time.hours = timeObj.hours + add_hours
    new_time.minutes = remain_minutes
    # Function call to display original time and new time
    printTime(timeObj)
    printTime(new_time)
