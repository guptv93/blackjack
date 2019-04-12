import random
from enum import Enum

class Rank(Enum):
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
				self.all_cards.append((j,rank))
		self.pile = list.copy(self.all_cards)

	def pick_card(self):
		card = random.choice(self.pile)
		self.pile.remove(card)
		return card

	def pile_size(self):
		return len(self.pile)



if __name__ == "__main__":
	my_deck = Deck()
	print(my_deck.pick_card())
	print(my_deck.pile_size())
	print(len(my_deck.all_cards))