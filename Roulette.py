#! python

import random
from abc import ABC, abstractmethod
from functools import partial
# import csv
# import os


class Outcome:
    def __init__(self, name, odds):
        self.name = name
        self.odds = odds

    def __eq__(self, other):
        return self.name == other.name

    def __ne__(self, other):
        return self.name != other.name

    def __hash__(self):
        return hash(self.name)

    def __str__(self):
        return f'{self.name} ({self.odds}:1)'

    def __repr__(self):
        return f'Outcome({self.name}, {self.odds})'

    def winAmount(self, amount):
        return (amount*self.odds)


class Bin(frozenset):
    pass


class Wheel:
    def __init__(self, rules=None):
        self.bins = [Bin() for i in range(38)]
        self.rng = random.Random()
        self.all_outcomes = set()
        self.rules = rules

        if self.rules is None:
            builder = BinBuilder()
            builder.buildBins(self)
        if self.rules == 'Euro':
            builder = EuroBinBuilder()
            builder.buildBins(self)

    def add(self, bin, outcome):
        # Collect all possible outcomes to match player bet
        self.all_outcomes.add(outcome)

    def getOutcome(self, name):
        # Match bet to one of possible outcomes
        return [oc for oc in self.all_outcomes if oc.name == name][0]

    # Adds outcome to each bin by union
    # Accesses individual bin/frozenset using index in tuple list
    def add_outcome(self, number, outcome):
        self.bins[number] = Bin(self.bins[number] | Bin([outcome]))

        if outcome not in self.all_outcomes:
            self.all_outcomes.add(outcome)

    def next(self):
        # Produce winning bin by randint we can identify winner
        x = self.rng.randint(0, len(self.bins) - 1)
        print('Winning bin: ' + str(x))
        return self.bins[x]

    def get(self, idx):
        return self.bins[idx]


# Wrapper class passes built bins to wheel
class BinBuilder:
    def __init__(self):
        pass
    # When called will fill bins out

    def buildBins(self, wheel):
        self.StraightBet(wheel)
        self.SplitBet(wheel)
        self.StreetBet(wheel)
        self.CornerBet(wheel)
        self.LineBet(wheel)
        self.DozenBet(wheel)
        self.ColumnBet(wheel)
        self.EvenMoneyBet(wheel)
        self.FiveBet(wheel)

    def StraightBet(self, wheel):
        oddsOut = 35
        for i in range(38):
            if i == 37:
                wheel.add_outcome(i, Outcome('Straight 00', oddsOut))
            else:
                wheel.add_outcome(i, Outcome(f'Straight {i}', oddsOut))

    def SplitBet(self, wheel):
        oddsOut = 17
        # add outcome to idx and # to the right of og idx

        def add_left_right_pair(outcome, idx, wheel):
            wheel.add_outcome(idx, outcome)
            wheel.add_outcome(idx + 1, outcome)
        # add outcome to idx and # below og idx

        def add_top_down_pair(outcome, idx, wheel):
            wheel.add_outcome(idx, outcome)
            wheel.add_outcome(idx + 3, outcome)

        for r in range(12):
            # cycle through 1 and 2 to jump between columns
            for i in range(1, 3):
                n = 3*r + i
                pair_outcome = Outcome(f'Split {n}-{n+1}', oddsOut)
                add_left_right_pair(pair_outcome, n, wheel)
        # give all numbers 1-33 top down pairs
        for n in range(1, 34):
            pair_outcome = Outcome(f'Split {n}-{n+3}', oddsOut)
            add_top_down_pair(pair_outcome, n, wheel)

    def StreetBet(self, wheel):
        oddsOut = 11
        for r in range(12):
            n = 3*r + 1
            street_outcome = Outcome(f'Street {n}-{n+1}-{n+2}', oddsOut)
            for x in range(3):
                wheel.add_outcome(n + x, street_outcome)

    def CornerBet(self, wheel):
        oddsOut = 8

        def add_corner_bets(outcome, idx, wheel):
            for x in [0, 1, 3, 4]:
                wheel.add_outcome(idx + x, outcome)

        for r in range(11):
            for i in range(1, 3):
                n = 3*r + i
                corner_outcome = Outcome(f'Corner {n}-{n+1}-{n+3}-{n+4}',
                                         oddsOut)
                add_corner_bets(corner_outcome, n, wheel)

    def LineBet(self, wheel):
        oddsOut = 5
        for r in range(11):
            n = 3*r + 1
            line_outcome = Outcome(f'Line {n}-{n+1}-{n+2}-{n+3}-{n+4}-{n+5}',
                                   oddsOut)
            for x in range(6):
                a = n + x
                wheel.add_outcome(a, line_outcome)

    def DozenBet(self, wheel):
        oddsOut = 2
        for d in range(3):
            dozen_outcome = Outcome(f'{d+1} Dozen', oddsOut)
            for m in range(12):
                wheel.add_outcome(12*d + m + 1, dozen_outcome)

    def ColumnBet(self, wheel):
        oddsOut = 2
        for c in range(3):
            column_outcome = Outcome(f'Column {c+1}', oddsOut)
            for r in range(12):
                wheel.add_outcome(3*r + c + 1, column_outcome)

    def EvenMoneyBet(self, wheel):
        oddsOut = 1
        red_outcome = Outcome('Red', oddsOut)
        black_outcome = Outcome('Black', oddsOut)
        even_outcome = Outcome('Even', oddsOut)
        odd_outcome = Outcome('Odd', oddsOut)
        high_outcome = Outcome('High', oddsOut)
        low_outcome = Outcome('Low', oddsOut)

        red_bins = {1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23,
                    25, 27, 30, 32, 34, 36}

        for n in range(1, 37):
            if n < 19:
                wheel.add_outcome(n, low_outcome)
            else:
                wheel.add_outcome(n, high_outcome)
            if n % 2 == 0:
                wheel.add_outcome(n, even_outcome)
            else:
                wheel.add_outcome(n, odd_outcome)
            if n in red_bins:
                wheel.add_outcome(n, red_outcome)
            else:
                wheel.add_outcome(n, black_outcome)

    def FiveBet(self, wheel):
        oddsOut = 6
        five_bet = Outcome('Fiver 00-0-1-2-3', oddsOut)
        for i in range(4):
            wheel.add_outcome(i, five_bet)
        wheel.add_outcome(37, five_bet)


class EuroBinBuilder(BinBuilder):
    def StraightBet(self, wheel):
        oddsOut = 35
        for i in range(1, 37):
            wheel.add_outcome(i, Outcome(f'Straight {i}', oddsOut))
        wheel.add_outcome(0, PrisonOutcome('Straight 0', oddsOut))

    # When super() calls BinBuilder it will pass on Fivebet

    def FiveBet(self, wheel):
        pass

    def FourBet(self, wheel):
        oddsOut = 6
        four_bet = Outcome('Four 0-1-2-3', oddsOut)
        for i in range(4):
            wheel.add_outcome(i, four_bet)

    # Call parent's buildBins and add Fourbet

    def buildBins(self, wheel):
        super().buildBins(wheel)
        self.FourBet(wheel)


class Bet:
    def __init__(self, amount, outcome):
        self.amountBet = amount
        self.outcome = outcome

    def __str__(self):
        return f'{self.amountBet} on {self.outcome}'

    def __repr__(self):
        return f'Bet ({self.amountBet}, {self.outcome})'

    def winAmount(self):
        winnings = self.amountBet*self.outcome.odds + self.amountBet
        return winnings

    def loseAmount(self):
        # Add separate outcome if instance is prisonoutcome
        return (-self.amountBet)


class InvalidBet(Exception):
    pass


class Table:
    def __init__(self, wheel, limit=10000):
        self.limit = limit
        self.bets = []
        self.wheel = wheel

    def __iter__(self):
        # Tells an iterative function to iterate through bets list
        return iter(self.bets)

    def __str__(self):
        n = '\n'
        return f'Bets: {(n.join(str(x) for x in self.bets))}'\
               f'{n}Total: ${sum(bet.amountBet for bet in self.bets)}'

    def __repr__(self):
        return f'Table({self.bets})'

    def placeBet(self, bet):
        self.bets.append(bet)

        if not self.isValid():
            raise InvalidBet

    def isValid(self):
        if sum(bet.amountBet for bet in self.bets) > self.limit:
            return False
        return True

    def clearTable(self):
        self.bets = []


class Player(ABC):
    def __init__(self, table):
        self.stake = None
        self.roundsToGo = None
        self.table = table
        self.default = 100

    def playing(self):
        if self.roundsToGo is None or self.stake is None:
            return False
        if self.roundsToGo > 0 and self.stake > 0:
            return True
        return False

    @abstractmethod
    def placeBets(self):
        desiredBet = sum(c.amountBet for c in self.table.bets)
        if self.stake >= desiredBet:
            self.stake -= desiredBet
            return True
        else:
            return False
        # Need to handle invalid bet

    def set_stake(self, stake):
        self.stake = stake

    def set_rounds(self, rounds):
        self.roundsToGo = rounds

    def winners(self, outcomes):
        if self.roundsToGo:
            self.roundsToGo -= 1

    def win(self, bet):
        print('Win!')
        self.stake += bet.winAmount()
        return self.stake

    def lose(self, bet):
        print('Loss.')
        if isinstance(bet.outcome, PrisonOutcome):
            return bet.loseAmount()*.5
        return self.stake


class Martingale(Player):
    def __init__(self, table):
        super().__init__(table)
        self.lossCount = 0
        self.betMultiple = 1
        self.bet = self.table.wheel.getOutcome('Black')

    def placeBets(self):
        self.table.placeBet(Bet(self.betMultiple * self.default, self.bet))
        success = super().placeBets()
        if not success:
            self.set_rounds(0)
            self.lossCount = 0
            self.betMultiple = 1
            raise InvalidBet

    def win(self, bet):
        self.lossCount = 0
        self.betMultiple = 1
        return super().win(bet)

    def lose(self, bet):
        self.lossCount += 1
        self.betMultiple *= 2
        return super().lose(bet)


class Passenger57(Player):
    def __init__(self, table):
        super().__init__(table)
        # Uses getOutcome to produce bet Outcome object
        self.black = self.table.wheel.getOutcome('Black')

    def placeBets(self):
        # Append a bet object and store it in self.bets of table
        self.table.placeBet(Bet(self.default, self.black))
        super().placeBets()


class SevenReds(Martingale):
    def __init__(self, table):
        super().__init__(table)
        self.redCount = 7
        self.red = self.table.wheel.getOutcome('Red')

    def placeBets(self):
        if self.redCount == 0:
            super().placeBets()

    def winners(self, outcomes):
        super().winners(outcomes)
        if self.red in outcomes:
            self.redCount -= 1
        else:
            self.redCount = 7


class RandomPlayer(Player):
    def __init__(self, table):
        super().__init__(table)
        self.randPool = self.table.wheel.all_outcomes

    def placeBets(self):
        outcome = self.table.wheel.rng.sample(self.randPool, 1)
        # Allows for multiple bets by iterating over x sampled outcomes
        for x in outcome:
            self.table.placeBet(Bet(self.default, x))
            super().placeBets()


class PlayerFibonacci(Player):
    def __init__(self, table):
        super().__init__(table)
        self.recent = 1
        self.previous = 0
        self.fibnum = int()
        self.black = self.table.wheel.getOutcome('Black')

    def placeBets(self):
        self.fibnum = self.recent + self.previous
        self.table.placeBet(Bet(self.default * self.fibnum, self.black))
        super().placeBets()

    def win(self, bet):
        self.recent, self.previous = 1, 0
        super().win(bet)

    def lose(self, bet):
        self.recent, self.previous = self.fibnum, self.recent
        super().lose(bet)


class PlayerCancel(Player):
    def __init__(self, table):
        super().__init__(table)
        self.sequence = []
        self.resetSequence()
        self.multiple = 0
        self.outcome = self.table.wheel.getOutcome('Black')

    def resetSequence(self):
        self.sequence = [i for i in range(1, 7)]

    def placeBets(self):
        try:
            self.multiple = self.sequence[0] + self.sequence[-1]
        except IndexError:
            raise InvalidBet
        self.table.placeBet((Bet(self.default * self.multiple, self.outcome)))
        super().placeBets()

    def win(self, bet):
        try:
            self.sequence.pop(0)
            self.sequence.pop(-1)
        except IndexError:
            raise InvalidBet
        super().win(bet)

    def lose(self, bet):
        self.sequence.append(self.multiple)
        super().lose(bet)


'''Player1326 uses a factory to build states as needed, each state
   will only be created once it has been determined that the state
   will be used in the next bet.  Partial calls create new state for
   player and pass to variable referenced on win.'''


class Player1326(Player):
    def __init__(self, table):
        super().__init__(table)
        self.outcome = self.table.wheel.getOutcome('Black')
        self.state = Player1326StateFactory.getInstance('Zero', self)

    def placeBets(self):
        self.state.currentBet()
        super().placeBets()

    def win(self, bet):
        self.state.nextWon()
        super().win(bet)

    def lose(self, bet):
        self.state.nextLost()
        super().lose(bet)


class Player1326StateFactory():
    _values = dict()

    @classmethod
    def getInstance(cls, name, player):
        if name in cls._values:
            return cls._values[name]

        if name == 'Zero':
            plr = Player1326NoWins(player)
            cls._values['Zero'] = plr
            return cls._values['Zero']

        elif name == 'One':
            plr = Player1326OneWin(player)
            cls._values['One'] = plr
            return cls._values['One']

        elif name == 'Two':
            plr = Player1326TwoWins(player)
            cls._values['Two'] = plr
            return cls._values['Two']

        elif name == 'Three':
            plr = Player1326ThreeWins(player)
            cls._values['Three'] = plr
            return cls._values['Three']


'''Generic state that establishes methods and player for each state'''


class Player1326State():
    def __init__(self, player):
        self.player = player
        self.multi = int()

    def currentBet(self):
        self.player.table.placeBet(
            Bet(self.player.default * self.multi, self.player.outcome))

    # Stores state for win
    def nextWon(self):
        self.player.state = self.nextStateWin()

    # Restarts at 0 win on loss
    def nextLost(self):
        self.player.state = Player1326StateFactory.getInstance('Zero', self)


class Player1326NoWins(Player1326State):
    def __init__(self, player):
        super().__init__(player)
        self.multi = 1
        self.nextStateWin = partial(
            Player1326StateFactory.getInstance, 'One', self.player)


class Player1326OneWin(Player1326State):
    def __init__(self, player):
        super().__init__(player)
        self.multi = 3
        self.nextStateWin = partial(
            Player1326StateFactory.getInstance, 'Two', self.player)


class Player1326TwoWins(Player1326State):
    def __init__(self, player):
        super().__init__(player)
        self.multi = 2
        self.nextStateWin = partial(
            Player1326StateFactory.getInstance, 'Three', self.player)


class Player1326ThreeWins(Player1326State):
    def __init__(self, player):
        super().__init__(player)
        self.multi = 6
        self.nextStateWin = partial(
            Player1326StateFactory.getInstance, 'Zero', self.player)


class Game:
    def __init__(self, table):
        self.table = table
        self.outcomes = []
        # Catches an invalid bet and breaks the loop
        self.Catch = False

    def cycle(self, player):
        try:
            self.Catch = False
            if player.playing():
                player.placeBets()
            win_bin = self.table.wheel.next()
            player.winners(win_bin)
            print(str(self.table) + '\n')
            print('Left in pocket after bet: $' + str(player.stake) + '\n')
            for b in self.table.bets:
                if b.outcome in win_bin:
                    self.outcomes.append(player.win(b))
                else:
                    self.outcomes.append(player.lose(b))
            print('='*20)
            self.table.clearTable()
            # self.count_rounds(player)
        except InvalidBet:
            print('Invalid bet was attempted.')
            self.Catch = True

    def endGame(self):
        self.table.clearTable()
        # print(self.outcomes)
        print('Player has left the table.')
        print(
            f'My pocket: ${player.stake} after {len(self.outcomes)}'
            f' total bets.')
        self.outcomes = []
    # Double counting rounds now that winners counts round
    # def count_rounds(self, player):
    #     player.roundsToGo -= 1


class PrisonOutcome(Outcome):
    def __repr__(self):
        return f'PrisonOutcome ({self.name}, {self.odds})'


class Simulator:
    def __init__(self, game, player):
        self.init_Duration = 1000
        self.init_Stake = 1000
        self.samples = 100
        self.durations = RouletteStats()
        self.maxima = RouletteStats()
        self.player = player
        self.game = game

    def session(self):
        self.player.__init__(self.player.table)
        self.player.set_stake(self.init_Stake)
        self.player.set_rounds(self.init_Duration)
        stakes = [self.player.stake]
        duration = 0
        while self.player.playing():
            self.game.cycle(self.player)
            stakes.append(self.player.stake)
            if self.game.Catch is True:
                break
            duration += 1
        self.game.endGame()
        self.maxima.append(max(stakes))
        self.durations.append(duration)

    def gather(self):
        for x in range(self.samples):
            print(f'===== Session {x+1} =====')
            self.session()
            # os.chdir('C:\\Users\\smcgauley\\Documents\\')
            # outputFile = open('output.csv', 'w', newline='')
            # outputWriter = csv.writer(outputFile)
            # outputWriter.writerow(range(1, 11))
            # outputWriter.writerow(self.maxima)
            # outputFile.close()
            print(self.maxima)
            print(self.durations)
        print(self.maxima.mean(), self.durations.mean())
        print(self.maxima.stdev(), self.durations.stdev())
        print(f'{self.maxima.stdev()/self.maxima.mean()}  '
              f'{self.durations.stdev()/self.durations.mean()}')


class RouletteStats(list):
    def mean(self):
        return sum(self)/len(self)

    def stdev(self):
        return (sum((x - self.mean())**2 for x in self) /
                (len(self)-1))**.5


actwheel = Wheel()
tab = Table(actwheel, 10000)
game = Game(tab)
player = PlayerFibonacci(tab)
sim = Simulator(game, player)

sim.gather()
