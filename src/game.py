import random
from enum import IntEnum

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
				self.all_cards.append((j,rank))
		self.pile = list.copy(self.all_cards)

	def pick_card(self):
		card = random.choice(self.pile)
		self.pile.remove(card)
		return card

	def pile_size(self):
		return len(self.pile)

	def card_to_string(self, card):
		return card[1].name + " of " + card[0]

class BlackJack:

	def __init__(self):
		self.dealer_hand = []
		self.player_hand = []
		self.deck = Deck()

	def get_hand_value(self, hand):
		result = []
		for card in hand:
			suit,rank = card
			if rank == 11 or rank == 12 or rank == 13:
				result.append(10)
			elif rank == 1:
				result.append(11)
			else:
				result.append(rank.value)
		return result

	def get_sum(self, hand):
		hand = self.get_hand_value(hand)
		ace = 0
		sum = 0
		for i in hand:
			sum += i
			if i == 11:
				ace += 1
		for i in range(ace):
			if sum > 21:
				sum -= 10
			else:
				break
		return sum

	def start_game(self):
		self.dealer_hand.append(self.deck.pick_card())
		self.dealer_hand.append(self.deck.pick_card())
		while self.get_sum(self.player_hand) < 12:
			self.player_hand.append(self.deck.pick_card())
		self.play()
		player_sum = self.get_sum(self.player_hand)
		if player_sum <= 21:
			while self.get_sum(self.dealer_hand) < player_sum:
				self.dealer_hand.append(self.deck.pick_card())
			dealer_sum = self.get_sum(self.dealer_hand)
			print("Dealers cards are:")
			self.print_hand(self.dealer_hand)
			if dealer_sum <= 21 and dealer_sum > player_sum:
				print("THE DEALER WINS ")
				self.result = -1
			elif dealer_sum == player_sum:
				print("GAME DRAW!!!!!")
				self.result = 0
			else:
				print("YOU WIN!!!!!")
				self.result = 1

	def play(self):
		while True:
			action = self.get_input()
			if action == "0":
				print("You have decided to Stand at a total of " + str(self.get_sum(self.player_hand)))
				return
			if action == "1":
				new_card = self.deck.pick_card()
				self.player_hand.append(new_card)
				print("You picked " + self.deck.card_to_string(new_card))
				sum = self.get_sum(self.player_hand)
				if sum >= 21:
					print("YOU GOT BUSTED!!!!!")
					self.result = -1
					return

	def get_input(self):
		print("Dealers first card is: " + self.deck.card_to_string(self.dealer_hand[0]))
		print("Your current cards are:")
		self.print_hand(self.player_hand)
		str = "Please choose action, 1 for HIT or 0 for STAND: "
		action = input(str)
		return action

	def print_hand(self, hand):
		for i in hand:
			print("\t" + self.deck.card_to_string(i))


if __name__ == "__main__":
	BlackJack().start_game()