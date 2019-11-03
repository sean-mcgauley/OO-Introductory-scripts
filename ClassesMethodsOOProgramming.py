class Time:
    def __init__(self, hours=0, minutes=0, seconds=0):
        self.hours = hours
        self.minutes = minutes
        self.seconds = seconds

    def printTime(time):
        print(str(time.hours) + ':' +
              str(time.minutes) + ':' +
              str(time.seconds))

    def increment(self, seconds):
        # Create pure function by instantiating a new object
        new_time = Time()
        new_time.seconds = self.seconds + (seconds % 60)
        new_time.minutes = self.minutes + ((seconds % 3600) // 60)
        new_time.hours = self.hours + (seconds // 3600)
        if new_time.minutes >= 60:
            new_time.hours += (new_time.minutes // 60)
            new_time.minutes -= 60
        if new_time.hours >= 24:
            new_time.hours = new_time.hours % 24

        self.printTime()
        new_time.printTime()

    def after(self, time2):
        # Example uses 1/0 instead of True/False
        # If self is > time2 then return True and do whatever follows
        # EX: If currentTime.after(breadTime):
        #       print('Bread time has passed my dawg')
        if self.hours > time2.hours:
            return True
        if self.hours < time2.hours:
            return False
        if self.minutes > time2.minutes:
            return True
        if self.minutes < time2.minutes:
            return False
        if self.seconds > time2.seconds:
            return True
        return False

    def increment(self, seconds):
        self.seconds += seconds
        while self.seconds >= 60:
            self.seconds -= 60
            self.minutes += 1
        while self.minutes >= 60:
            self.minutes -= 60
            self.hours += 1


currentTime = Time(11, 59, 30)
breadTime = Time(6, 36, 57)
