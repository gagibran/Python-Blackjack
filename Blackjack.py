import random
import sys

"""
RULES:
    The goal is that the human player has to get closer to a total value of 21 than the computer dealer does. The total value is the sum of the 
    current faced up cards that the human player has. If the player is still under 21, the dealer hits until it either beats the player or until 
    it busts, which is summing over 21. The human player will start with a bankroll of 20,000 Digital Currency (DC). The player starts with 2 
    cards faced and the computer dealer starts with one card faced up, and one card faced down.
        up.

SPECIAL RULES:
    Face Cards (Jack, Queen, King) count as a value of 10; and
    Aces can count as either 1 or 11 preferable to the player.

POSSIBLE ENDINGS:
    1. Player busting;
    2. Computer dealer beats the player by getting  closer to 21 without busting;
    3. Player beats the the computer dealer by getting  closer to 21 without busting; and
    3. Computer dealer busting.

HUMAN PLAYER AND COMPUTER DEALER ACTIONS:
    HIT: receives a new card from the deck; and
    STAY: stops receiving cards.
"""

class Bankroll:
    def __init__(self):
        self.avaliable_money = 20000.0

    def how_much(self, quantity):
        self.quantity = float(quantity)
        if self.quantity > self.avaliable_money:
            return False
        else:
            self.avaliable_money -= self.quantity
            return True

    def double_it(self):
        self.quantity *= 2
        self.avaliable_money += self.quantity
        return round(self.avaliable_money,2)
    
    def draw(self):
        self.avaliable_money += self.quantity
        return round(self.avaliable_money,2)


class Deck:
    """
    A standard 52-card deck contains 4 unique suits sets of cards which ranges like: A, 2, 3, 4, 5, 6, 7, 8, 9, 10, J, Q, K. The suits are: clubs, diamonds, hearts and 
    spades. Every set of suits contains 13 cards.
    """

    def __init__(self):
        self.deck_dict = {
            "clubs": ["A", 2, 3, 4, 5, 6, 7, 8, 9, 10, "J", "Q", "K"],
            "diamonds": ["A", 2, 3, 4, 5, 6, 7, 8, 9, 10, "J", "Q", "K"],
            "hearts": ["A", 2, 3, 4, 5, 6, 7, 8, 9, 10, "J", "Q", "K"],
            "spades": ["A", 2, 3, 4, 5, 6, 7, 8, 9, 10, "J", "Q", "K"]
        }
        self.card_value_list = []

    def hit_me(self, is_faced_down=False):
        """
        Defines the HIT command, which subtracts one card from the deck.
        Returns the randomly selected card
        """
        self.deck_card_counter = 0
        self.selected_suit_and_card_list = []
        while True:
            self.random_suit_card_list = list(random.choice(list(self.deck_dict.items())))
            try:
                self.selected_card = self.random_suit_card_list[1].pop(random.randint(0, len(self.random_suit_card_list[1])-1))
            except:
                continue
            else:
                break
        self.deck_dict.update({self.random_suit_card_list[0]: self.random_suit_card_list[1]})
        self.selected_suit_and_card_list.append(self.random_suit_card_list[0])
        self.selected_suit_and_card_list.append(self.selected_card)
        if is_faced_down == False:
            self.card_value_list.append(self.selected_card)
        return self.selected_suit_and_card_list

    def number_of_cards(self):
        self.deck_card_counter = 0
        for cards in self.deck_dict.values():
            self.deck_card_counter += len(cards)
        return self.deck_card_counter

    def ace_value(self, value_choice, pc=False):
        if pc:
            if value_choice == "1":
                self.card_value_list.remove(0)
                self.card_value_list.append(1)
            if value_choice == "11":
                self.card_value_list.remove(0)
                self.card_value_list.append(11)
        else:
            if value_choice == "1":
                self.card_value_list.remove("A")
                self.card_value_list.append(1)
            if value_choice == "11":
                self.card_value_list.remove("A")
                self.card_value_list.append(11)

    def reveal_card(self, card_to_reveal):
        self.card_value_list.append(card_to_reveal)


class WinBust(Deck):
    """
    Defines the value of the "A", "J", "K" and "Q" cards, the sum of points (from both player and PC), and if whether the PC or the player have busted.
    """

    def __init__(self):
        Deck.__init__(self)

    def sum_of_points(self):
        """
        Calculates the sum of points.
        """
        for i, card in enumerate(self.card_value_list):
            if isinstance(card, str):
                if card == "A":
                    self.card_value_list[i] = 0
                else:
                    self.card_value_list[i] = 10
        return sum(self.card_value_list)

    def busting(self):
        """
        Checks whether the PC or the player busted.
        """
        if self.sum_of_points() == 21:
            return "blackjackflag"
        elif self.sum_of_points() > 21:
            return "busted"


class HumanPlayer(WinBust, Bankroll): 
    """
    Defines the attributes of the human player.
    The human player plays first.
    """

    def __init__(self):
        WinBust.__init__(self)


class ComputerDealer(WinBust):
    """
    Defines the attributes of the computer dealer.
    The computer dealer plays after the human player.
    """

    def __init__(self):
        WinBust.__init__(self)


if __name__ == "__main__":
    # Instantiating the bank:
    bank_roll = Bankroll()

    # CHECKING PLAYER'S MONEY:
    while True:

        # Instantiating the used classes in the game:
        player_turn = HumanPlayer()
        pc_turn = ComputerDealer()

        # ASK FOR BET:
        print("How much money do you want to bet? You have {} DC avaliable.".format(round(bank_roll.avaliable_money,2)))
        bet_input = input("Type in the amount of money: \n")
        while bank_roll.how_much(bet_input) == False:
            print("You don't have that amount of money. Please, insert a valid amount.\n")
            bet_input = input("Type the amount of money: \n")

        # STARTING HANDS:
        # Player:
        print("The game will be played with a 52 cards, 4 suits (clubs, diamonds, hearts and spades) deck.\n")
        print("The dealer gives you two faced up cards. They are: \n")
        for i in range(0,2):
            player_card = player_turn.hit_me()
            pc_turn.deck_dict = player_turn.deck_dict
            print("A(n) {} of {}.\n".format(player_card[1], player_card[0]))
            while player_card[1] == "A":
                print("Do you wish to make this ace a 1 or an 11?\n")
                card_input = input("1 or 11\n")
                if card_input != "1" and card_input != "11":
                    print('You must type "1" or "11".\n')
                    continue
                else:
                    player_turn.ace_value(card_input)
                    break
        # Dealer:
        print("It takes for itself two cards, one faced up and one faced down. The faced up card is: \n")
        pc_card = pc_turn.hit_me()
        player_turn.deck_dict = pc_turn.deck_dict
        print("A(n) {} of {}.\n".format(pc_card[1], pc_card[0]))
        if pc_card[1] == "A":
            if pc_turn.sum_of_points() <= 7:
                card_input = "11"
            else:
                card_input = "1"
            pc_turn.ace_value(card_input, True)
        pc_faced_down_card = pc_turn.hit_me(True)
        player_turn.deck_dict = pc_turn.deck_dict
        print("The deck has {} cards.\n".format(player_turn.number_of_cards()))
        print("The dealer has {} points.\n".format(str(pc_turn.sum_of_points())))

        # PLAYER TURN:
        while len(player_turn.deck_dict["clubs"]) > 0 or len(player_turn.deck_dict["diamonds"]) > 0 or len(player_turn.deck_dict["hearts"]) > 0 or len(player_turn.deck_dict["spades"]) > 0:
            print("You have {} points.\n".format(str(player_turn.sum_of_points())))
            if player_turn.busting() == "blackjackflag":
                print("Blackjack!\n")
                print("You win double your bet!\n")
                bank_roll.double_it()
                break
            elif player_turn.busting() == "busted":
                print("You busted!\n")
                break
            print("Do you want another a card?\n")
            hit_Stand = input("hit me/stand: \n")
            if hit_Stand == "hit me":
                card = player_turn.hit_me()
                pc_turn.deck_dict = player_turn.deck_dict
                print("You got a(n) {} of {}.\n".format(card[1], card[0]))
                while card[1] == "A":
                    print("Do you wish to make this ace a 1 or an 11?\n")
                    card_input = input("1 or 11\n")
                    if card_input != "1" and card_input != "11":
                        print('You must type "1" or "11".\n')
                        continue
                    else:
                        player_turn.ace_value(card_input)
                        break
                print("The deck has {} cards.\n".format(player_turn.number_of_cards()))
            elif hit_Stand == "stand":
                print("Your turn has ended.\n")
                break
            else:
                print('You must type "hit me" or "stand".\n')
                continue

        # PC TURN:
        if player_turn.busting() == "blackjackflag" or player_turn.busting():
            pass
        else:
            while len(pc_turn.deck_dict["clubs"]) > 0 or len(pc_turn.deck_dict["diamonds"]) > 0 or len(pc_turn.deck_dict["hearts"]) > 0 or len(pc_turn.deck_dict["spades"]) > 0:
                print("The dealer reveals its faced down card. It's: \n")
                print("A(n) {} of {}.\n".format(pc_faced_down_card[1], pc_faced_down_card[0]))
                pc_turn.reveal_card((pc_faced_down_card[1]))
                if pc_faced_down_card[1] == "A":
                    if pc_turn.sum_of_points() <= 7:
                        card_input = "11"
                    else:
                        card_input = "1"
                    pc_turn.ace_value(card_input, True)
                print("The dealer has {} points.\n".format(str(pc_turn.sum_of_points())))
                while pc_turn.sum_of_points() <= player_turn.sum_of_points():
                    pc_card = pc_turn.hit_me()
                    player_turn.deck_dict = pc_turn.deck_dict
                    if pc_turn.sum_of_points() >= 16 and pc_turn.sum_of_points() == player_turn.sum_of_points():
                        print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAaaa")
                        break
                    print("The dealer decides to take another card. It got a(n) {} of {}.\n".format(pc_card[1], pc_card[0]))
                    if pc_card[1] == "A":
                        if pc_turn.sum_of_points() <= 7:
                            card_input = "11"
                        else:
                            card_input = "1"
                        pc_turn.ace_value(card_input, True)
                    print("The dealer has {} points.\n".format(str(pc_turn.sum_of_points())))
                    if pc_turn.busting() == "blackjackflag":
                        break
                    elif pc_turn.busting() == "busted":
                        break
                if pc_turn.busting() == "blackjackflag":
                    break
                elif pc_turn.busting() == "busted":
                    break
                print("The dealer has decided to stand.\n")
                break

            # CHECKING THE SCORES
            if pc_turn.busting() == "blackjackflag":
                print("The dealer's got a Blackjack!\n")
                print("You have lost your bet to the dealer.\n")
            elif pc_turn.busting():
                print("The dealer busted!\n")
                print("You win double your bet!\n")
                bank_roll.double_it()
            else:
                print("The scores are being checked...\n")
                print("Your score: {}. Dealer's score: {}.\n".format(player_turn.sum_of_points(), pc_turn.sum_of_points()))
                if pc_turn.sum_of_points() > player_turn.sum_of_points() and pc_turn.sum_of_points() < 21:
                    print("You have lost your bet to the dealer.\n")
                elif pc_turn.sum_of_points() == player_turn.sum_of_points():
                    print("Draw!\n")
                    print("You haven't lost any money.\n")
                    bank_roll.draw()
                else:
                    print("You win double your bet!\n")
                    bank_roll.double_it()
        if bank_roll.avaliable_money <= 0:
                print("You don't have any money. The game will be terminated.\n")
                input("Press ENTER to continue...")
                sys.exit(0)
        print("Avaliable money: {} DC.\n".format(round(bank_roll.avaliable_money,2)))
        print("Do you want to play again?\n")
        while True:
            play_again_input = input("(y/n)\n")
            if play_again_input == "y":
                break
            elif play_again_input == "n":
                input("Press ENTER to continue...")
                sys.exit(0)
            elif play_again_input != "n" or play_again_input != "y":
                print('You must type "y" or "n".\n')
                continue
