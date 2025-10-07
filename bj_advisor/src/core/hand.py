"""
Hand evaluation for blackjack advisor.
Handles soft/hard totals, pairs, blackjack detection, and bust detection.
"""
from dataclasses import dataclass
from typing import List, Optional, Tuple
from .card import Card, Rank


@dataclass
class Hand:
    """Blackjack hand with soft/hard evaluation."""
    cards: List[Card]
    
    def __init__(self, cards: Optional[List[Card]] = None):
        self.cards = cards or []
    
    def add_card(self, card: Card) -> None:
        """Add a card to the hand."""
        self.cards.append(card)
    
    @property
    def is_empty(self) -> bool:
        """True if hand has no cards."""
        return len(self.cards) == 0
    
    @property
    def is_pair(self) -> bool:
        """True if hand is exactly two cards of same rank."""
        return (len(self.cards) == 2 and 
                self.cards[0].rank.bj_value == self.cards[1].rank.bj_value)
    
    @property
    def pair_rank(self) -> Optional[Rank]:
        """Return the rank if this is a pair, None otherwise."""
        if self.is_pair:
            return self.cards[0].rank
        return None
    
    @property
    def has_ace(self) -> bool:
        """True if hand contains at least one Ace."""
        return any(card.rank == Rank.ACE for card in self.cards)
    
    @property
    def ace_count(self) -> int:
        """Number of Aces in hand."""
        return sum(1 for card in self.cards if card.rank == Rank.ACE)
    
    def _calculate_total(self) -> Tuple[int, bool]:
        """Calculate hand total and whether it's soft.
        
        Returns:
            Tuple of (total, is_soft)
        """
        if not self.cards:
            return 0, False
        
        # Count non-ace cards
        total = sum(card.value for card in self.cards if card.rank != Rank.ACE)
        aces = self.ace_count
        
        if aces == 0:
            return total, False
        
        # Start with all aces as 1
        total += aces
        
        # Try to make one ace worth 11 if it doesn't bust
        if total + 10 <= 21:
            return total + 10, True
        else:
            return total, False
    
    @property
    def total(self) -> int:
        """Best possible total for the hand."""
        total, _ = self._calculate_total()
        return total
    
    @property
    def is_soft(self) -> bool:
        """True if hand total includes an Ace counted as 11."""
        _, soft = self._calculate_total()
        return soft
    
    @property
    def is_hard(self) -> bool:
        """True if hand is not soft (no Ace as 11)."""
        return not self.is_soft
    
    @property
    def is_blackjack(self) -> bool:
        """True if hand is natural blackjack (21 with exactly 2 cards)."""
        return len(self.cards) == 2 and self.total == 21
    
    @property
    def is_busted(self) -> bool:
        """True if hand total exceeds 21."""
        return self.total > 21
    
    @property
    def can_double(self) -> bool:
        """True if hand is eligible for doubling (exactly 2 cards)."""
        return len(self.cards) == 2
    
    @property
    def can_split(self) -> bool:
        """True if hand can be split (is a pair)."""
        return self.is_pair
    
    def describe(self) -> str:
        """Human-readable description of the hand."""
        if self.is_empty:
            return "Empty hand"
        
        if self.is_pair:
            return f"Pair of {self.pair_rank.symbol}s"
        elif self.is_soft:
            return f"Soft {self.total}"
        else:
            return f"Hard {self.total}"
    
    def card_string(self) -> str:
        """String representation of cards in hand."""
        return ",".join(str(card) for card in self.cards)
    
    def __str__(self):
        """String representation of hand."""
        if self.is_empty:
            return "[]"
        
        cards_str = self.card_string()
        description = self.describe()
        
        if self.is_busted:
            return f"[{cards_str}] - {description} (BUST)"
        elif self.is_blackjack:
            return f"[{cards_str}] - Blackjack!"
        else:
            return f"[{cards_str}] - {description}"
    
    def copy(self) -> 'Hand':
        """Create a copy of this hand."""
        return Hand(self.cards.copy())


class SplitHands:
    """Container for managing split hands."""
    
    def __init__(self, original_hand: Hand):
        if not original_hand.can_split:
            raise ValueError("Cannot split non-pair hand")
        
        # Create two hands, each with one card from the original pair
        self.hands = [
            Hand([original_hand.cards[0]]),
            Hand([original_hand.cards[1]])
        ]
        self.current_hand_index = 0
        self.completed_hands = set()
    
    @property
    def current_hand(self) -> Hand:
        """Currently active hand."""
        return self.hands[self.current_hand_index]
    
    @property
    def all_hands(self) -> List[Hand]:
        """All split hands."""
        return self.hands
    
    @property
    def is_complete(self) -> bool:
        """True if all hands are complete."""
        return len(self.completed_hands) == len(self.hands)
    
    def add_card_to_current(self, card: Card) -> None:
        """Add card to currently active hand."""
        self.current_hand.add_card(card)
    
    def complete_current_hand(self) -> None:
        """Mark current hand as complete and move to next."""
        self.completed_hands.add(self.current_hand_index)
        
        # Find next incomplete hand
        for i in range(len(self.hands)):
            if i not in self.completed_hands:
                self.current_hand_index = i
                return
    
    def can_split_current(self) -> bool:
        """True if current hand can be split further."""
        return (self.current_hand.can_split and 
                len(self.hands) < 4)  # Max 4 hands
    
    def split_current(self) -> None:
        """Split the current hand into two new hands."""
        if not self.can_split_current():
            raise ValueError("Cannot split current hand")
        
        current = self.current_hand
        if not current.is_pair:
            raise ValueError("Current hand is not a pair")
        
        # Replace current hand with two new hands
        new_hand1 = Hand([current.cards[0]])
        new_hand2 = Hand([current.cards[1]])
        
        self.hands[self.current_hand_index] = new_hand1
        self.hands.insert(self.current_hand_index + 1, new_hand2)