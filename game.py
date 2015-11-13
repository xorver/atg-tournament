from random import *
from sys import *

##############################################
# Parameters
##############################################

HANDS_TO_PLAY = 100000
BIG_BLIND = 10
HAND_MAX = 9
STACK = 300

##############################################
# Helper functions
##############################################

def message(kind, msg):
    print "### POKER( %s ): %s" % (kind, msg)

def winnings(hand, bet):
    payment = [0, 0, 0]
    [(h1, b1, i1), (h2, b2, i2), (h3, b3, i3)] = \
        sorted(zip(hand, bet, range(3)), reverse=True)
    if h1 == h2 == h3:
        return payment
    if h1 == h2:
        payment[i1] = b3 / 2
        payment[i2] = b3 / 2
        payment[i3] = -b3
        return payment
    payment[i1] = b2 + b3
    payment[i2] = -b2
    payment[i3] = -b3
    return payment

def valid_bet(bet, min, max):
    return bet in range(min, max+1, 1)

def hand_not_finished(player_in_game):
    [p1, p2, p3] = player_in_game
    return (p1 and p2) or (p1 and p3) or (p2 and p3)

def create_players(names):
    players = []
    i = 0
    for name in names:
        X = __import__(name)
        players += [X.Player()]
        try:
            players[i].name(i)
        except:
            pass
        i += 1

    return players

##############################################
# Game
##############################################

def game(names):
    scores = [0, 0, 0]

    message("START GAME", str(names))
    players = create_players(names)

    for i in range(HANDS_TO_PLAY):
        message("HAND START", str(i + 1))
        scores = play_hand(players, scores)

    s = ""
    for i in range(3):
        s += names[i] + "(" + str(scores[i]) + ")  "
    message("GAME RESULT", s)

    return scores


def play_hand(players, scores):
    # stan gry
    hand = [randint(0, HAND_MAX), randint(0, HAND_MAX), randint(0, HAND_MAX)] # wylosowane karty
    in_game = [True, True, True]  # czy gracz pozostaje w grze
    bet = [0, 0, 0]  # wartosci licytacji
    result = [0, 0, 0]  # bilans rozdania

    # rozdaj karty
    for i in range(3):
        try:
            players[i].hand(hand[i])
        except:
            message("EXCEPTION", "players[%i].hand()" % i)

    # pierwsza runda licytacji - obstawianie
    for i in range(3):
        try:
            bet[i] = players[i].bet1(BIG_BLIND)
            if not valid_bet(bet[i], BIG_BLIND, STACK):
                bet[i] = BIG_BLIND
                in_game[i] = False
                hand[i] = None
        except:
            message("EXCEPTION", "players[%i].bet1()" % i)

    best_bet1 = max(bet)

    # pierwsza runda licytacji - info o obstawianiu
    for i in range(3):
        try:
            players[i].bet1_info(bet)
        except:
            message("EXCEPTION", "players[%i].bet1_info()" % i)

    # pierwsza runda licytacji - sprawdzanie
    if hand_not_finished(in_game):
        for i in range(3):
            if in_game[i] and bet[i] != best_bet1:
                try:
                    calls = players[i].call1(best_bet1)
                    if calls:
                        bet[i] = best_bet1
                    else:
                        in_game[i] = False
                        hand[i] = None
                except:
                    message("EXCEPTION", "players[%i].call1()" % i)

    # pierwsza runda licytacji  - info o graczach w grze
    for i in range(3):
        try:
            players[i].call1_info(in_game)
        except:
            message("EXCEPTION", "players[%i].call1_info()" % i)

    # druga runda licytacji - obstawianie
    if hand_not_finished(in_game):
        for i in range(3):
            if in_game[i]:
                try:
                    bet[i] = players[i].bet2(best_bet1)
                    if bet[i] not in range(best_bet1, STACK+1, 1):
                        bet[i] = best_bet1
                        in_game[i] = False
                        hand[i] = None
                except:
                    message("EXCEPTION", "players[%i].bet2()" % i)

    best_bet2 = max(bet)

    # druga runda licytacji  - info o obstawianiu
    for i in range(3):
        try:
            players[i].bet2_info(bet)
        except:
            message("EXCEPTION", "players[%i].bet2_info()" % i)

    # druga runda licytacji - sprawdzanie
    if hand_not_finished(in_game):
        for i in range(3):
            if in_game[i] and bet[i] != best_bet2:
                try:
                    calls = players[i].call2(best_bet2)
                    if calls:
                        bet[i] = best_bet2
                    else:
                        in_game[i] = False
                        hand[i] = None
                except:
                    message("EXCEPTION", "players[%i].call2()" % i)

    # druga runda licytacji  - info o  o graczach w grze
    for i in range(3):
        try:
            players[i].call2_info(in_game)
        except:
            message("EXCEPTION", "players[%i].call2_info()" % i)

    # okazanie kart
    for i in range(3):
        try:
            if hand_not_finished(in_game):
                players[i].showdown(hand)
            else:
                players[i].showdown([None, None, None])
        except:
            message("EXCEPTION", "players[%i].showdown()" % i)

    # podsumowanie
    for i in range(3):
        try:
            result = winnings(hand, bet)
            players[i].result(result)
        except:
            message("EXCEPTION", "players[%i].result()" % i)

    for i in range(3):
        scores[i] += result[i]

    return scores

##############################################
# Main
##############################################

if __name__ == "__main__":
    seed()
    if len(argv) < 4:
        print "Invocation:"
        print "   game player1 player2 player3"
        exit()

    scores = game(argv[1:4])
    print scores
