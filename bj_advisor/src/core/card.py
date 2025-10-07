"""
Card system implementation for blackjack advisor.
Includes Rank enum, Card dataclass, and Shoe tracking.
"""
from enum import Enum
from dataclasses import dataclass
from typing import List, Optional
import random


class Rank(Enum):
    """Card ranks with blackjack values."""
    TWO = ("2", 2, 1)
    THREE = ("3", 3, 1)
    FOUR = ("4", 4, 1)
    FIVE = ("5", 5, 1)
    SIX = ("6", 6, 1)
    SEVEN = ("7", 7, 0)
    EIGHT = ("8", 8, 0)
    NINE = ("9", 9, 0)
    TEN = ("T", 10, -1)
    JACK = ("J", 10, -1)
    QUEEN = ("Q", 10, -1)
    KING = ("K", 10, -1)
    ACE = ("A", 11, -1)

    def __init__(self, symbol: str, bj_value: int, hi_lo_value: int):
        self.symbol = symbol
        self.bj_value = bj_value
        self.hi_lo_value = hi_lo_value

    @classmethod
    def from_string(cls, rank_str: str) -> 'Rank':
        """Parse rank from string (case insensitive)."""
        rank_str = rank_str.upper()
        if rank_str == "10":
            rank_str = "T"
        
        for rank in cls:
            if rank.symbol == rank_str:
                return rank
        raise ValueError(f"Invalid rank: {rank_str}")

    def __str__(self):
        return self.symbol


@dataclass
class Card:
    """Playing card with Hi-Lo counting value."""
    rank: Rank

    @property
    def hi_lo_value(self) -> int:
        """Hi-Lo counting value: +1 for 2-6, 0 for 7-9, -1 for T-A."""
        return self.rank.hi_lo_value

    @property
    def value(self) -> int:
        """Blackjack value of the card."""
        return self.rank.bj_value

    def __str__(self):
        return str(self.rank)

    @classmethod
    def from_string(cls, card_str: str) -> 'Card':
        """Create card from string representation."""
        return cls(Rank.from_string(card_str))


class Shoe:
    """Shoe tracking for blackjack game with Hi-Lo counting."""
    
    def __init__(self, num_decks: int = 6, penetration_threshold: float = 0.75):
        self.num_decks = num_decks
        self.penetration_threshold = penetration_threshold
        self.cards_dealt: List[Card] = []
        self.running_count = 0
        
    @property
    def cards_remaining(self) -> int:
        """Number of cards remaining in shoe."""
        total_cards = self.num_decks * 52
        return total_cards - len(self.cards_dealt)
    
    @property
    def decks_remaining(self) -> float:
        """Approximate number of decks remaining."""
        return self.cards_remaining / 52.0
    
    @property
    def true_count(self) -> float:
        """True count (running count / decks remaining)."""
        if self.decks_remaining <= 0:
            return 0.0
        return self.running_count / self.decks_remaining
    
    @property
    def penetration(self) -> float:
        """Percentage of cards dealt from shoe."""
        total_cards = self.num_decks * 52
        return len(self.cards_dealt) / total_cards
    
    @property
    def needs_shuffle(self) -> bool:
        """True if penetration threshold exceeded."""
        return self.penetration >= self.penetration_threshold
    
    def deal_card(self, card: Card) -> None:
        """Record a card being dealt and update running count."""
        self.cards_dealt.append(card)
        self.running_count += card.hi_lo_value
    
    def shuffle(self) -> None:
        """Reset shoe to beginning."""
        self.cards_dealt.clear()
        self.running_count = 0
    
    def get_count_info(self) -> dict:
        """Get comprehensive count information."""
        return {
            "running_count": self.running_count,
            "true_count": round(self.true_count, 2),
            "decks_remaining": round(self.decks_remaining, 1),
            "cards_dealt": len(self.cards_dealt),
            "cards_remaining": self.cards_remaining,
            "penetration": round(self.penetration * 100, 1)
        }