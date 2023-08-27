from snap import (
    Card,
    Suits,
    Ranks,
    Player,
    add_cards_to_winners_pile,
    any_player_has_face_down_cards,
    create_deck,
    deal_cards,
)
import pytest


@pytest.mark.parametrize(
    "suit, rank, expected",
    [
        (Suits.HEARTS, Ranks.ACE, "Ace of Hearts"),
        (Suits.SPADES, Ranks.TWO, "2 of Spades"),
        (Suits.DIAMONDS, Ranks.KING, "King of Diamonds"),
        (Suits.CLUBS, Ranks.QUEEN, "Queen of Clubs"),
    ],
)
def test_card_representation(suit: Suits, rank: Ranks, expected: str) -> None:
    card = Card(suit=suit, rank=rank)
    assert repr(card) == expected


def test_next_turn():
    player = Player(name="Test Player")
    player.face_down_cards = [Card(suit=Suits.DIAMONDS, rank=Ranks.THREE)]
    assert len(player.face_up_cards) == 0
    player.next_turn()
    assert len(player.face_up_cards) == 1
    assert not player.face_down_cards


def test_top_card():
    player = Player(name="Test Player")
    mock_card = Card(suit=Suits.CLUBS, rank=Ranks.FOUR)
    player.face_up_cards = [mock_card]
    assert player.top_card() == mock_card


def test_add_cards_to_winners_pile() -> None:
    player_one = Player(name="Test Player One")
    player_two = Player(name="Test Player Two")

    mock_card_one = [Card(suit=Suits.HEARTS, rank=Ranks.TWO)]
    mock_card_two = [Card(suit=Suits.DIAMONDS, rank=Ranks.THREE)]

    player_one.face_up_cards = mock_card_one
    player_two.face_up_cards = mock_card_two

    # Test player one winning
    add_cards_to_winners_pile(winner=player_one, loser=player_two)
    assert player_one.winning_pile == mock_card_one + mock_card_two
    assert not player_one.face_up_cards
    assert not player_two.face_up_cards


def test_create_deck_unique_cards() -> None:
    num_decks = 1
    deck = create_deck(num_decks)
    all_unique_cards = set(deck)
    assert len(deck) == 52
    assert len(all_unique_cards) == 52


def test_create_deck_multiple_decks() -> None:
    num_decks = 2
    deck = create_deck(num_decks)
    all_unique_cards = set(deck)
    assert len(deck) == 104
    assert len(all_unique_cards) == 52


def test_deal_cards() -> None:
    num_decks = 2
    deck = create_deck(num_decks)
    player_one = Player(name="Test Player One")
    player_two = Player(name="Test Player Two")
    all_players = [player_one, player_two]
    deal_cards(deck, all_players)
    assert len(player_one.face_down_cards) == 52
    assert len(player_two.face_down_cards) == 52
    assert len(deck) == 0


@pytest.mark.parametrize(
    "mock_cards, expected",
    [
        ([Card(suit=Suits.CLUBS, rank=Ranks.TWO)], True),
        ([], False),
    ],
)
def test_any_player_has_face_down_cards(mock_cards: list[Card], expected: bool) -> None:
    player1 = Player(name="Player 1")
    player2 = Player(name="Player 2")
    player1.face_down_cards = mock_cards
    assert any_player_has_face_down_cards([player1, player2]) == expected
