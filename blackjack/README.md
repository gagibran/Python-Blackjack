# Blackjack with Python

## A Blackjack game with a custom AI in Python.

## Table of content

- [Installation](#installation)
- [Instructions](#instructions)
- [Next steps](#next-steps)

### Installation

This projects was developed using Python 3.8.5. For more information on how to install Python, refer to [the official website](https://www.python.org/).<br>

The script doesn't require a requirements.txt installer nor a virtual environment, because it only uses the packages sys and random, which come with Python by default. So, to run the game, download the project folder, go to the directory's command prompt, and run:
```sh
python blackjack.py
```

For a Linux distribution, most likely run:
```sh
python3 blackjack.py
```

**NOTE: This is a safe script, but always check on which kind of script you are running on your PC, specially when it's been downloaded from the Internet!**<br> 
**NOTE 2: The code documentation can be found inside the script.**

## Instructions

The instructions can be found by executing the script, the prompts lead you to do what is needed. But here is a breakdown of the game:

**RULES**:
The goal is that the human player has to get closer to a total value of 21 than the computer dealer does. The total value is the sum of the current faced up cards that the human player has. If the player is still under 21, the dealer hits until it either beats the player or until it busts, which is summing over 21. The human player will start with a bankroll of 20,000.00 Digital Currency (DC). The player starts with 2 cards faced and the computer dealer starts with one card faced up, and one card faced down.

**SPECIAL RULES**:
- Face Cards (Jack, Queen, King) count as a value of 10; and
- Aces can count as either 1 or 11 preferable to the player.

**POSSIBLE ENDINGS**:
- Player busting;
- Computer dealer beats the player by getting closer to 21 without busting;
- Player beats the the computer dealer by getting closer to 21 without busting; and
- Computer dealer busting.

**HUMAN PLAYER AND COMPUTER DEALER ACTIONS**:
- HIT: receives a new card from the deck; and
- STAY: stops receiving cards.

## Next steps

The next steps to this project are:
- Optimize the script in general;
- Create a framework by standardizing the classes further so that future card based game scripts can inherit from common base one.