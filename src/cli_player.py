from game import *

game = BlackJack()
game.start_game()

def get_input():
	print("Dealers first card is:")
	game.print_hand([game.get_dealer_hand()[0]])
	print("Your current cards are:")
	game.print_hand(game.get_player_hand())
	s = "Please choose action, 1 for HIT or 0 for STAND: "
	action = input(s)
	return action

while True:
	action = get_input()
	if action == "0":
		print("You have decided to Stand at a total of " + str(game.get_sum(game.get_player_hand())))
		status = game.stand()
		print("The Dealer drew:")
		game.print_hand(game.get_dealer_hand())
		print(game.get_status_string(status))
		break;
	if action == "1":
		status = game.hit()
		print("You picked up the card:")
		player_hand = game.get_player_hand()
		game.print_hand([player_hand[len(player_hand) - 1]])
		if(status == Status.PLAYER_BUST):
			print("You got Busted!!")
			break;