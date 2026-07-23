import random
import time

suits = ["♠", "♥", "♣", "♦"]
ranks = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
class Card:
    values = {
        "A": 1,
        "2": 2,
        "3": 3,
        "4": 4,
        "5": 5,
        "6": 6,
        "7": 7,
        "8": 8,
        "9": 9,
        "10": 10,
        "J": 10,
        "Q": 10,
        "K": 10
    }

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return f"{self.rank} {self.suit}"

    def value(self):
        return self.values[self.rank]

class Deck:
    def __init__(self):
        self.cards = []
        for suit in suits:
            for rank in ranks:
                self.cards.append(Card(suit, rank))

    def shuffle(self):
        random.shuffle(self.cards)

    def deal_card(self):
        return self.cards.pop()

class Player:
    def __init__(self):
        self.hand = []

    def receive_card(self, card):
        self.hand.append(card)

    def show_hand(self):
        for card in self.hand:
            print(card)

    def calculate_score(self):
        total = 0
        aces = 0
        for card in self.hand:
            total += card.value()
            if card.value() == 1:
                aces += 1

        while total + 10 <= 21  and aces > 0:
            total += 10
            aces -= 1
        return total

    def has_blackjack(self):
        return len(self.hand) == 2 and self.calculate_score() == 21

class Dealer(Player):
    def show_visible_hand(self):
        print("?")
        print(self.hand[1])

class Game:
    def __init__(self):
        self.deck = Deck()
        self.player = Player()
        self.dealer = Dealer()

    def play(self):
        self.start_game()
        self.display_game()
        self.player_turn()

    def start_game(self):
        self.deck.shuffle()
        for _ in range(2):
            self.player.receive_card(self.deck.deal_card())
            self.dealer.receive_card(self.deck.deal_card())

    def display_game(self):
        print("Your hand:")
        self.player.show_hand()
        print(f"Your score: {self.player.calculate_score()}")
        print()
        print("Dealer hand:")
        self.dealer.show_visible_hand()

    def display_final_game(self):
        print("Your final hand:")
        self.player.show_hand()
        print(f"Your final score: {self.player.calculate_score()}")
        print()
        print("Dealer hand:")
        for card in self.dealer.hand:
            print(card)
        print(f"Dealer score: {self.dealer.calculate_score()}")
        for _ in range(5):
            print()

    def player_turn(self):
        while self.player.calculate_score() < 21:
            player_choice = input("(H)it or (S)tand ").lower()

            if player_choice == "h":
                for _ in range(5):
                    print()
                self.player.receive_card(self.deck.deal_card())
                self.display_game()

            elif player_choice == "s":
                for _ in range(5):
                    print()
                self.dealer_turn()
                return


        if self.player.calculate_score() == 21:
            for _ in range(5):
                print()
            self.dealer_turn()
        elif self.player.calculate_score() > 21:
            print("Bust!")

    def dealer_turn(self):
        self.display_final_game()
        while self.dealer.calculate_score() < 17:
            time.sleep(2)
            self.dealer.receive_card(self.deck.deal_card())
            self.display_final_game()

        self.determine_winner()

    def determine_winner(self):
        player_score = self.player.calculate_score()
        dealer_score = self.dealer.calculate_score()
        player_blackjack = self.player.has_blackjack()
        dealer_blackjack = self.dealer.has_blackjack()

        if player_blackjack and dealer_blackjack:
            print("Both have Blackjack! Push!")

        elif player_blackjack:
            print("Blackjack! You win!")

        elif dealer_blackjack:
            print("Dealer Blackjack! Dealer wins!")

        else:
            if player_score > 21:
                print("Dealer wins!")

            elif dealer_score > 21:
                print("You win!")

            elif player_score > dealer_score:
                print("You win!")

            elif dealer_score > player_score:
                print("Dealer wins!")

            else:
                print("Push! It's a tie!")

if __name__ == "__main__":
    while True:
        game = Game()
        game.play()

        replay = input("Do you want to play again? (Y/N) ").lower()
        if replay == "n":
            print("Thank you for playing!")
            break