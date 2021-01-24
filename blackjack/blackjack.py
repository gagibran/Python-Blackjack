"""
RULES:
    The goal is that the human player has to get closer to a total value of 21 than the computer dealer does. The total value is the sum of the 
    current faced up cards that the human player has. If the player is still under 21, the dealer hits until it either beats the player or until 
    it busts, which is summing over 21. The human player will start with a bankroll of 20,000.00 Digital Currency (DC). The player starts with 2 
    cards faced and the computer dealer starts with one card faced up, and one card faced down.

SPECIAL RULES:
    Face Cards (Jack, Queen, King) count as a value of 10; and
    Aces can count as either 1 or 11 preferable to the player.

POSSIBLE ENDINGS:
    1. Player busting;
    2. Computer dealer beats the player by getting closer to 21 without busting;
    3. Player beats the the computer dealer by getting closer to 21 without busting; and
    3. Computer dealer busting.

HUMAN PLAYER AND COMPUTER DEALER ACTIONS:
    HIT: receives a new card from the deck; and
    STAY: stops receiving cards.
"""

import random
import sys

class Bankroll:
    """
    Handles the amount of DC the player has.
    """

    def __init__(self):
        """
        The player starts with 20,000.00 DC.
        """
        self.avaliable_money = 20000.0

    def how_much(self, quantity):
        """
        Handles how much DC the player wants to bet. If the betting is successful, it takes the amount of money they bet from the total.

        INPUT:
        quantity: how much they want to bet (str)

        OUTPUT:
        Returns whether the betting was successful (bool).
        """
        self.quantity = float(quantity)
        if self.quantity > self.avaliable_money:
            return False
        self.avaliable_money -= self.quantity
        return True

    def double_it(self):
        """
        If the player gets a Blackjack, it doubles the current bet.

        INPUT:
        Not input. It reads the class variables quantity and avaliable_money (float).

        OUTPUT:
        rounded_double: Returns a rounded value of the total amount of DC after doubling the bet (float).
        """
        self.quantity *= 2
        self.avaliable_money += self.quantity
        rounded_double = round(self.avaliable_money, 2)
        return rounded_double
    
    def draw(self):
        """
        If the game ends with a draw, the player doesn't lose any money.

        INPUT:
        No input. It reads the class variable avaliable_money, which is the total amount of DC the palyer has and adds the amount they bet back to it (float).

        OUTPUT
        rounded_value: The updated amount of DC the player has (float).
        """
        self.avaliable_money += self.quantity
        rounded_value = round(self.avaliable_money, 2)
        return rounded_value


class Deck:
    """
    Handles the deck used in the game by the player and the computer.
    """

    def __init__(self):
        """
        A standard 52-card deck contains 4 unique suits sets of cards which ranges like: A, 2, 3, 4, 5, 6, 7, 8, 9, 10, J, Q, K. The suits are: clubs, diamonds, hearts and 
        spades. Every set of suits contains 13 cards.
        """
        self.deck_dict = {
            "clubs": ["A", 2, 3, 4, 5, 6, 7, 8, 9, 10, "J", "Q", "K"],
            "diamonds": ["A", 2, 3, 4, 5, 6, 7, 8, 9, 10, "J", "Q", "K"],
            "hearts": ["A", 2, 3, 4, 5, 6, 7, 8, 9, 10, "J", "Q", "K"],
            "spades": ["A", 2, 3, 4, 5, 6, 7, 8, 9, 10, "J", "Q", "K"]
        }
        self.card_value_list = [] # Holds the current value of the cards.

    def hit_me(self, is_faced_down=False):
        """
        Defines the HIT command, which subtracts one card from the deck.

        INPUT:
        is_faced_down: whether the card is faced down (bool). Default value: False.

        OUTPUT:
        selected_suit_and_card_list: Returns the randomly selected card (list of str).
        """

        # Initializers:
        self.deck_card_counter = 0
        self.selected_suit_and_card_list = [] # Holds the current card value.

        # Handling the dynamic changes to the deck:
        while True:
            self.random_suit_card_list = list(random.choice(list(self.deck_dict.items()))) # Chooses a random suit and returns it into a list instead of a tuple.
            try:
                self.selected_card = self.random_suit_card_list[1].pop(random.randint(0, len(self.random_suit_card_list[1])-1)) # Tries to select one card from the deck.
            except:
                continue # If there are not cards of a certain suit anymore, tries again.
            else:
                break # If it succeeds, breaks the while-loop.

        # Handling the aftermath of drawing a card:
        self.deck_dict.update({self.random_suit_card_list[0]: self.random_suit_card_list[1]}) # Updates the deck when a card is removed from it.
        self.selected_suit_and_card_list.append(self.random_suit_card_list[0]) # Updates the list with the value of the selected card.
        self.selected_suit_and_card_list.append(self.selected_card) # Updates the list with the value of the selected suit.

        # Handling the computer's faced down card:
        if not is_faced_down:
            self.card_value_list.append(self.selected_card) # If the card is not faced down, appends its value to the current card value's list.
        return self.selected_suit_and_card_list

    def reveal_card(self, card_to_reveal):
        """
        Reveals the computer dealer's hidden card.

        INPUT:
        card_to_reveal: A faced down card to be revealed (str).

        OUTPUT:
        No output. It appends this card to the list that holds the current card value.
        """
        self.card_value_list.append(card_to_reveal)

    def ace_value(self, value_choice, pc=False):
        """
        Method that allows the player or the computer dealer to choose what value the ace will have (1 or 11).

        INPUT:
        value_choice: whether the ace will be 1 or 11 (str).

        OUTPUT:
        No output. It appends the value to the list that holds the current value of a card.
        """
        if pc: # The ace card is handled differently for the computer dealer, because when it needs to decide what value it will have based on the score it currently has.
            if value_choice == "1":
                self.card_value_list.remove(0) # The ace card's value is, by default, 0 in order to sum_of_points from Win_bust be able to calculate the points for the PC.
                self.card_value_list.append(1)
            elif value_choice == "11":
                self.card_value_list.remove(0)
                self.card_value_list.append(11)
        else: # Since the player's decision is not scripted and the card's value is shown to them beforehand, it handles the ace normally.
            if value_choice == "1":
                self.card_value_list.remove("A")
                self.card_value_list.append(1)
            elif value_choice == "11":
                self.card_value_list.remove("A")
                self.card_value_list.append(11)

    def number_of_cards(self):
        """
        Counts the number of cards of a deck.

        INPUT:
        No input. It reads the deck dictionary.

        OUTPUT:
        deck_card_counter: The number of cards in a deck (int).
        """
        self.deck_card_counter = 0
        for cards in self.deck_dict.values():
            self.deck_card_counter += len(cards)
        return self.deck_card_counter


class Win_bust(Deck):
    """
    Defines the value of the "A", "J", "K" and "Q" cards, the sum of points (from both player and the computer dealer), and whether the PC or the player have busted.
    """

    def __init__(self):
        Deck.__init__(self) # Initialized with the variables from the instanciated Deck class.

    def sum_of_points(self):
        """
        Calculates the sum of points.

        INPUT:
        No input. It reads the current cards on the player's or the computer dealer's hand.

        OUTPUT:
        total_points: A summation of all the values fo the cards in a hand (int).
        """
        for i, card in enumerate(self.card_value_list):
            if isinstance(card, str): # If there's an ace in the player's or computer dealer's hand.
                if card == "A":
                    self.card_value_list[i] = 0
                else:
                    self.card_value_list[i] = 10
        total_points = sum(self.card_value_list)
        return total_points


    def busting(self):
        """
        Checks whether the the player or the computer dealer busted or achieved blackjack.

        INPUT:
        No input. it reads and compares the total sum of points by executing the method sum_of_points().

        OUTPUT:
        blackjack_busted: A flag stating whether the player or the computer dealer busted or achieved blackjack (str).
        """
        blackjack_busted = ""
        if self.sum_of_points() == 21:
            blackjack_busted = "blackjackflag"
        elif self.sum_of_points() > 21:
            blackjack_busted = "busted"
        return blackjack_busted


class Human_player(Win_bust, Bankroll): 
    """
    Defines the attributes of the human player. The human player plays first. It uses methods from both inherited classes.
    """

    def __init__(self):
        Win_bust.__init__(self) # Initialized with the variables from the instanciated Win_bust class.


class Computer_dealer(Win_bust):
    """
    Defines the attributes of the computer dealer. The computer dealer plays after the human player.
    """

    def __init__(self):
        Win_bust.__init__(self) # Initialized with the variables from the instanciated Win_bust class.


if __name__ == "__main__":

    # Instantiating the bank:
    bank_roll = Bankroll()

    # Runs until the player quits or the amount of DC ends:
    while True:

        # Instantiating the used classes in the game:
        player_turn = Human_player()
        pc_turn = Computer_dealer()

        # Handling the player's bet:
        print("How much money do you want to bet? You have {} DC avaliable.".format(round(bank_roll.avaliable_money,2)))
        bet_input = input("Type in the amount of money: \n")
        while bank_roll.how_much(bet_input) == False:
            print("You don't have that amount of money. Please, insert a valid amount.\n")
            bet_input = input("Type the amount of money: \n")

        # Player's starting hand:
        print("The game will be played with a 52 cards, 4 suits (clubs, diamonds, hearts and spades) deck.\n")
        print("The dealer gives you two faced up cards. They are: \n")

        # For the two cards in the player's hand:
        for i in range(2):
            player_card = player_turn.hit_me()
            pc_turn.deck_dict = player_turn.deck_dict
            print("A(n) {} of {}.\n".format(player_card[1], player_card[0]))

            # If the player gets an ace on their starting hand:
            while player_card[1] == "A":
                print("Do you wish to make this ace a 1 or an 11?\n")
                card_input = input("1 or 11\n")
                if card_input != "1" and card_input != "11":
                    print('You must type "1" or "11".\n')
                    continue
                player_turn.ace_value(card_input)
                break

        # Dealer's starting hand:
        print("It takes for itself two cards, one faced up and one faced down. The faced up card is: \n")
        pc_card = pc_turn.hit_me()
        player_turn.deck_dict = pc_turn.deck_dict # Updates the variable class deck dictionary of both classes so that they share a common deck throughout the game.
        print("A(n) {} of {}.\n".format(pc_card[1], pc_card[0]))

        # If the computer dealer has an ace on its starting hand:
        if pc_card[1] == "A":
            if pc_turn.sum_of_points() <= 7:
                card_input = "11"
            else:
                card_input = "1"
            pc_turn.ace_value(card_input, pc=True)
        
        # Handling the computer dealer's faced down card's reveal:
        pc_faced_down_card = pc_turn.hit_me(is_faced_down=True)
        player_turn.deck_dict = pc_turn.deck_dict # Updates dictionary again, after another hit me from the computer dealer.
        print("The deck has {} cards.\n".format(player_turn.number_of_cards()))
        print("The dealer has {} points.\n".format(pc_turn.sum_of_points()))

        # Player's turn:
        # While there are still cards inside the suits from the deck:
        while len(player_turn.deck_dict["clubs"]) > 0 or len(player_turn.deck_dict["diamonds"]) > 0 or len(player_turn.deck_dict["hearts"]) > 0 or len(player_turn.deck_dict["spades"]) > 0:
            print("You have {} points.\n".format(player_turn.sum_of_points()))

            # Checks to see if the player has busted or achieved blackjack:
            if player_turn.busting() == "blackjackflag":
                print("Blackjack!\n")
                print("You win double your bet!\n")
                bank_roll.double_it()
                break
            elif player_turn.busting() == "busted":
                print("You busted!\n")
                break

            # If neither happened, asks the player if they want to hit or stand:
            print("Do you want another a card?\n")
            hit_stand = input("hit me/stand: \n")

            # Handling the choice:
            if hit_stand == "hit me":
                card = player_turn.hit_me()
                pc_turn.deck_dict = player_turn.deck_dict
                print("You got a(n) {} of {}.\n".format(card[1], card[0]))

                # Handling the ace:
                while card[1] == "A":
                    print("Do you wish to make this ace a 1 or an 11?\n")
                    card_input = input("1 or 11\n")
                    if card_input != "1" and card_input != "11":
                        print('You must type "1" or "11".\n')
                        continue
                    player_turn.ace_value(card_input)
                    break
                print("The deck has {} cards.\n".format(player_turn.number_of_cards()))
            elif hit_stand == "stand":
                print("Your turn has ended.\n")
                break
            else:
                print('You must type "hit me" or "stand".\n')
                continue

        # Computer dealer's turn:
        if player_turn.busting(): # Checks if the player has busted or achieved blackjack.
            pass
        else: # If not:

            # While there are still cards inside the suits from the deck:
            while len(pc_turn.deck_dict["clubs"]) > 0 or len(pc_turn.deck_dict["diamonds"]) > 0 or len(pc_turn.deck_dict["hearts"]) > 0 or len(pc_turn.deck_dict["spades"]) > 0:
                print("The dealer reveals its faced down card. It's: \n")
                print("A(n) {} of {}.\n".format(pc_faced_down_card[1], pc_faced_down_card[0]))
                pc_turn.reveal_card((pc_faced_down_card[1]))

                # Handling the ace:
                if pc_faced_down_card[1] == "A":
                    if pc_turn.sum_of_points() <= 7:
                        card_input = "11"
                    else:
                        card_input = "1"
                    pc_turn.ace_value(card_input, True)
                print("The dealer has {} points.\n".format(pc_turn.sum_of_points()))

                # The A.I.: while the computer dealer has less points than the player:
                while pc_turn.sum_of_points() <= player_turn.sum_of_points():
                    pc_card = pc_turn.hit_me()
                    player_turn.deck_dict = pc_turn.deck_dict # Updates dictionary again, after another hit me from the player.

                    # If the computer dealer has more points than the player and this sum is greater than 16, it stops hitting:
                    if pc_turn.sum_of_points() >= 16 and pc_turn.sum_of_points() == player_turn.sum_of_points():
                        break
                    print("The dealer decides to take another card. It got a(n) {} of {}.\n".format(pc_card[1], pc_card[0]))

                    # Handling another ace:
                    if pc_card[1] == "A":
                        if pc_turn.sum_of_points() <= 7:
                            card_input = "11"
                        else:
                            card_input = "1"
                        pc_turn.ace_value(card_input, True)

                    # Checking whether the computer dealer has busted or achieved blackjack while the player has more points:
                    print("The dealer has {} points.\n".format(pc_turn.sum_of_points()))
                    if pc_turn.busting() == "blackjackflag":
                        break
                    elif pc_turn.busting() == "busted":
                        break

                # Checking whether the computer dealer has busted or achieved blackjack if it has more points than the player to begin with:
                if pc_turn.busting() == "blackjackflag":
                    break
                elif pc_turn.busting() == "busted":
                    break
                print("The dealer has decided to stand.\n")
                break

            # Checking the scores:
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

        # Checks whether the player still has any DC. If none is found, it ends the game.
        if bank_roll.avaliable_money <= 0:
                print("You don't have any money. The game will be terminated.\n")
                input("Press ENTER to continue...")
                sys.exit(0)
        print("Avaliable money: {} DC.\n".format(round(bank_roll.avaliable_money,2)))
        print("Do you want to play again?\n")

        # Checks if the player wants to play again if they lost or not.
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
