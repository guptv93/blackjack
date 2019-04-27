import random
from enum import IntEnum
import csv


class Rank(IntEnum):
    Ace = 1
    Two = 2
    Three = 3
    Four = 4
    Five = 5
    Six = 6
    Seven = 7
    Eight = 8
    Nine = 9
    Ten = 10
    Jack = 11
    Queen = 12
    King = 13


class Deck:
    suit = ["Hearts", "Clubs", "Spades", "Diamonds"]

    def __init__(self):
        self.all_cards = []
        for rank in Rank:
            for j in Deck.suit:
                self.all_cards.append((j, rank))
        # self.pile = list.copy(self.all_cards)

    def pick_card(self):
        card = random.choice(self.all_cards)
        # self.pile.remove(card)
        return card

    def pile_size(self):
        return len(self.pile)

    def card_to_string(self, card):
        return card[1].name + " of " + card[0]


class Status(IntEnum):
    STILL_PLAYING = 1
    PLAYER_BUST = 2
    PLAYER_WON = 3
    PLAYER_LOST = 4
    GAME_DRAW = 5


class BlackJack:

    def __init__(self):
        self.dealer_hand = []
        self.player_hand = []
        self.deck = Deck()
        self.result = 0
        self.hasAce = False
        self.decision = []
        self.feed = []

    def get_player_hand(self):
        return self.player_hand

    def get_dealer_hand(self):
        return self.dealer_hand

    def get_hand_value(self, hand):
        ret_value = []
        for card in hand:
            suit, rank = card
            if rank == 11 or rank == 12 or rank == 13:
                ret_value.append(10)
            elif rank == 1:
                ret_value.append(11)
            else:
                ret_value.append(rank.value)
        return ret_value

    def get_sum(self, hand):
        hand = self.get_hand_value(hand)
        ace = 0
        sum = 0
        self.hasAce = False
        for i in hand:
            sum += i
            if i == 11:
                ace += 1
        for i in range(ace):
            if sum > 21:
                sum -= 10
            else:
                self.hasAce = True
                break
        return sum

    def start_game(self):
        self.dealer_hand.append(self.deck.pick_card())
        self.dealer_hand.append(self.deck.pick_card())
        while self.get_sum(self.player_hand) < 12:
            self.player_hand.append(self.deck.pick_card())
        self.feed.append("Start Playing!")

    def hit(self):
        self.record_action("HIT")
        new_card = self.deck.pick_card()
        self.player_hand.append(new_card)
        sum = self.get_sum(self.player_hand)
        if sum > 21:
            self.result = -1
            self.record_reward()
            return Status.PLAYER_BUST
        else:
            return Status.STILL_PLAYING

    def stand(self):
        self.record_action("STAND")
        player_sum = self.get_sum(self.player_hand)
        if player_sum <= 21:
            while self.get_sum(self.dealer_hand) < player_sum:
                self.dealer_hand.append(self.deck.pick_card())
            dealer_sum = self.get_sum(self.dealer_hand)
            if 21 >= dealer_sum > player_sum:
                self.result = -1
                self.record_reward()
                return Status.PLAYER_LOST
            elif dealer_sum == player_sum:
                self.result = 0
                self.record_reward()
                return Status.GAME_DRAW
            else:
                self.result = 1
                self.record_reward()
                return Status.PLAYER_WON

    def get_status_string(self, stat):
        status_string = ""
        if stat == 1:
            status_string = "Your total is " + \
                str(self.get_sum(self.player_hand)) + ". Continue playing."
        elif stat == 2:
            status_string = "Your total exceeds 21. You got Busted!!"
        elif stat == 3:
            status_string = "You Win!!"
        elif stat == 4:
            status_string = "The Dealer Wins!!"
        elif stat == 5:
            status_string = "The Dealer's sum is exactly equal to yours. Game Draw!!"
        return status_string

    def get_feed(self, stat):
        new_feed = self.get_status_string(stat)
        self.feed.append(new_feed)
        return self.feed

    def print_hand(self, hand):
        for i in hand:
            print("\t" + self.deck.card_to_string(i))

    def record_action(self, action):
        individual_decision = [str(self.get_sum(self.player_hand)), self.dealer_hand[
            0][1].value, str(self.hasAce), str(action)]
        self.decision.append(individual_decision)

    def record_reward(self):
        count = 0
        for d in reversed(self.decision):
            d.append(count)
            d.append(self.result)
            count += 1
        self.write_to_csv()

    def write_to_csv(self):
        with open('userData.csv', 'a') as f:
            writer = csv.writer(f)
            writer.writerows(self.decision)
        f.close()
