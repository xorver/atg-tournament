from random import *

class Player:

    def name(self, index):
        self.me = index
        [self.opp1, self.opp2] = [i for i in range(3) if i != self.me]
        self.stack = 300

    def hand(self, card):
        self.card = card
    
    def bet1(self, min):
        return randint(min, self.stack)

    def bet1_info(self, bets):
        opp1_bet = bets[self.opp1]
        opp2_bet = bets[self.opp2]

    def call1(self, bet):
        return bool(randint(0, 1))

    def call1_info(self, in_game):
        opp1_in_game = in_game[self.opp1]
        opp2_in_game = in_game[self.opp2]

    def bet2(self, min):
        return randint(min, self.stack)

    def bet2_info(self, bets):
        opp1_bet = bets[self.opp1]
        opp2_bet = bets[self.opp2]

    def call2(self, bet):
        return bool(randint(0, 1))

    def call2_info(self, in_game):
        opp1_in_game = in_game[self.opp1]
        opp2_in_game = in_game[self.opp2]

    def showdown(self, hand):
        opp1_hadd = hand[self.opp1]
        opp2_hand = hand[self.opp2]

    def result(self, winnings):
        my_winnings = winnings[self.me]
        opp1_winnings = winnings[self.opp1]
        opp2_winnings = winnings[self.opp2]