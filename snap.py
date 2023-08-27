import random
from typing import NamedTuple
from enum import Enum


class Suits(Enum):
    HEARTS = "Hearts"
    DIAMONDS = "Diamonds"
    CLUBS = "Clubs"
    SPADES = "Spades"


class Ranks(Enum):
    TWO = "2"
    THREE = "3"
    FOUR = "4"
    FIVE = "5"
    SIX = "6"
    SEVEN = "7"
    EIGHT = "8"
    NINE = "9"
    TEN = "10"
    JACK = "Jack"
    QUEEN = "Queen"
    KING = "King"
    ACE = "Ace"


class Card(NamedTuple):
    suit: Suits
    rank: Ranks

    def __repr__(self):
        return f"{self.rank.value} of {self.suit.value}"


class Player:
    def __init__(self, name: str) -> None:
        self.name = name
        self.face_up_cards: list[Card] = []
        self.face_down_cards: list[Card] = []
        self.winning_pile: list[Card] = []

    def next_turn(self) -> None:
        self.face_up_cards.append(self.face_down_cards.pop())

    def top_card(self) -> Card:
        if not self.face_up_cards:
            raise ValueError("No cards in face up pile")

        return self.face_up_cards[-1]


def add_cards_to_winners_pile(winner: Player, loser: Player) -> None:
    winner.winning_pile.extend(winner.face_up_cards + loser.face_up_cards)
    winner.face_up_cards = []
    loser.face_up_cards = []


def create_deck(num_decks):
    deck = [
        Card(suit=suit, rank=value)
        for _ in range(num_decks)
        for suit in Suits
        for value in Ranks
    ]
    random.shuffle(deck)
    return deck


def determine_round_winner(players: list[Player]) -> Player:
    return random.choice(players)


def deal_cards(deck: list, all_players: list[Player]) -> None:
    while deck:
        for player in all_players:
            if deck:
                player.face_down_cards.append(deck.pop())


def any_player_has_face_down_cards(all_players: list[Player]) -> bool:
    return sum(len(player.face_down_cards) for player in all_players) > 0


def get_user_input() -> int:
    while True:
        num_decks = input(
            "Enter the number of playing card decks to use.\nLeave blank for 1 deck\n - Decks: "
        )
        if num_decks.isdigit() and int(num_decks) > 0:
            return int(num_decks)
        elif num_decks == "":
            return 1
        else:
            print("\nPlease enter a valid number! 🙏\n")


def play_snap(all_players: list[Player]):
    game_round = 0
    # Check all players have face down cards remaining
    while any_player_has_face_down_cards(all_players):
        game_round += 1

        print(f"\n==================== Round {game_round} ====================\n")

        cards_seen_in_round = set()
        card_match = False
        for player in all_players:
            player.next_turn()
            top_card = player.top_card()

            if top_card.rank.value in cards_seen_in_round:
                card_match = True
            else:
                cards_seen_in_round.add(top_card.rank.value)
            print(f"{player.name} turned over {top_card}")

        if card_match:
            winner = determine_round_winner(all_players)
            loser = [player for player in all_players if player != winner][0]
            # Add cards to winning pile
            add_cards_to_winners_pile(winner, loser)
            print(f"{winner.name} said SNAP! first and won the round\n")
        else:
            print("No match! Next round...\n")

        print("Winning piles:")
        for player in all_players:
            print(f"{player.name}: {len(player.winning_pile)}")

    print("\nGame over!\n")

    # Determine winner
    max_pile_size = max(len(player.winning_pile) for player in all_players)
    players_with_max_pile = [
        player for player in all_players if len(player.winning_pile) == max_pile_size
    ]
    if len(players_with_max_pile) > 1:
        print("It's a tie! 🙀 \n")
    else:
        print("Player with biggest pile wins!")
        winner = players_with_max_pile[0]
        print(f"{winner.name} won the game! 🎉 \n")


def main() -> None:
    # Get user input
    num_decks = get_user_input()

    # Create combined deck for game
    deck = create_deck(num_decks)

    # Initialize players
    player_one = Player(name="Player 1")
    player_two = Player(name="Player 2")
    all_players = [player_one, player_two]

    # Deal cards until none left
    deal_cards(deck, all_players)

    print("Let's play Snap!")

    # Start game
    play_snap(all_players)


if __name__ == "__main__":
    main()
