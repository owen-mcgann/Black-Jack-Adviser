"""
Table state management for blackjack advisor.
Tracks multiple seats, dealer cards, and game state.
"""
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Union
from .card import Card, Shoe, Rank
from .hand import Hand, SplitHands
from .rules import Rules, DEFAULT_RULES


@dataclass
class Seat:
    """Player seat at blackjack table."""
    seat_id: str
    hands: Union[Hand, SplitHands]
    is_user: bool = False
    is_active: bool = True
    
    def __init__(self, seat_id: str, is_user: bool = False):
        self.seat_id = seat_id
        self.hands = Hand()
        self.is_user = is_user
        self.is_active = True
    
    @property
    def primary_hand(self) -> Hand:
        """Get the primary (or only) hand for this seat."""
        if isinstance(self.hands, SplitHands):
            return self.hands.current_hand
        return self.hands
    
    @property
    def all_hands(self) -> List[Hand]:
        """Get all hands for this seat (list for splits)."""
        if isinstance(self.hands, SplitHands):
            return self.hands.all_hands
        return [self.hands]
    
    @property
    def has_splits(self) -> bool:
        """True if this seat has split hands."""
        return isinstance(self.hands, SplitHands)
    
    def add_card(self, card: Card) -> None:
        """Add card to current hand."""
        if isinstance(self.hands, SplitHands):
            self.hands.add_card_to_current(card)
        else:
            self.hands.add_card(card)
    
    def split_hand(self) -> None:
        """Split the current hand."""
        if isinstance(self.hands, SplitHands):
            if self.hands.can_split_current():
                self.hands.split_current()
            else:
                raise ValueError("Cannot split current hand further")
        else:
            if self.hands.can_split:
                self.hands = SplitHands(self.hands)
            else:
                raise ValueError("Hand cannot be split")
    
    def can_split(self) -> bool:
        """True if current hand can be split."""
        if isinstance(self.hands, SplitHands):
            return self.hands.can_split_current()
        return self.hands.can_split
    
    def describe_hands(self) -> str:
        """Description of all hands at this seat."""
        if isinstance(self.hands, SplitHands):
            descriptions = []
            for i, hand in enumerate(self.hands.all_hands):
                marker = " *" if i == self.hands.current_hand_index else ""
                descriptions.append(f"  Hand {i+1}: {hand}{marker}")
            return "\n".join(descriptions)
        else:
            return f"  {self.hands}"


class DealerHand:
    """Special handling for dealer hand with upcard/hole card."""
    
    def __init__(self):
        self.upcard: Optional[Card] = None
        self.hole_card: Optional[Card] = None
        self.hit_cards: List[Card] = []
    
    @property
    def all_cards(self) -> List[Card]:
        """All dealer cards."""
        cards = []
        if self.upcard:
            cards.append(self.upcard)
        if self.hole_card:
            cards.append(self.hole_card)
        cards.extend(self.hit_cards)
        return cards
    
    @property
    def hand(self) -> Hand:
        """Dealer hand as Hand object."""
        return Hand(self.all_cards)
    
    @property
    def shows_ace(self) -> bool:
        """True if dealer upcard is Ace."""
        return self.upcard and self.upcard.rank == Rank.ACE
    
    @property
    def upcard_value(self) -> Optional[int]:
        """Value of dealer upcard."""
        return self.upcard.value if self.upcard else None
    
    def add_hit_card(self, card: Card) -> None:
        """Add a hit card to dealer hand."""
        self.hit_cards.append(card)
    
    def reset(self) -> None:
        """Reset dealer hand for new round."""
        self.upcard = None
        self.hole_card = None
        self.hit_cards.clear()
    
    def describe(self) -> str:
        """Description of dealer hand."""
        if not self.upcard:
            return "Dealer: No cards"
        
        cards_str = str(self.upcard)
        if self.hole_card:
            cards_str += f",{self.hole_card}"
        if self.hit_cards:
            hit_str = ",".join(str(card) for card in self.hit_cards)
            cards_str += f",{hit_str}"
        
        if self.hole_card or self.hit_cards:
            total = self.hand.total
            description = self.hand.describe()
            return f"Dealer: [{cards_str}] - {description}"
        else:
            return f"Dealer: [{cards_str},?]"


class Table:
    """Blackjack table state management."""
    
    def __init__(self, rules: Rules = DEFAULT_RULES):
        self.rules = rules
        self.shoe = Shoe(rules.num_decks, rules.penetration_threshold)
        self.dealer = DealerHand()
        self.seats: Dict[str, Seat] = {}
        self.user_seat_id: Optional[str] = None
        self.round_active = False
    
    def add_seat(self, seat_id: str, is_user: bool = False) -> None:
        """Add a player seat to the table."""
        if seat_id in self.seats:
            raise ValueError(f"Seat {seat_id} already exists")
        
        self.seats[seat_id] = Seat(seat_id, is_user)
        if is_user:
            self.user_seat_id = seat_id
    
    def get_user_seat(self) -> Optional[Seat]:
        """Get the user's seat."""
        if self.user_seat_id and self.user_seat_id in self.seats:
            return self.seats[self.user_seat_id]
        return None
    
    def start_round(self) -> None:
        """Start a new round."""
        if self.round_active:
            raise ValueError("Round already active")
        
        # Reset all hands
        self.dealer.reset()
        for seat in self.seats.values():
            seat.hands = Hand()
            seat.is_active = True
        
        self.round_active = True
    
    def end_round(self) -> None:
        """End current round."""
        self.round_active = False
    
    def add_card_to_player(self, seat_id: str, card: Card) -> None:
        """Add card to player hand and update shoe."""
        if seat_id not in self.seats:
            raise ValueError(f"Seat {seat_id} not found")
        
        self.seats[seat_id].add_card(card)
        self.shoe.deal_card(card)
    
    def add_dealer_upcard(self, card: Card) -> None:
        """Add dealer upcard."""
        if self.dealer.upcard:
            raise ValueError("Dealer upcard already set")
        
        self.dealer.upcard = card
        self.shoe.deal_card(card)
    
    def add_dealer_hole_card(self, card: Card) -> None:
        """Add dealer hole card."""
        if self.dealer.hole_card:
            raise ValueError("Dealer hole card already set")
        
        self.dealer.hole_card = card
        self.shoe.deal_card(card)
    
    def add_dealer_hit_card(self, card: Card) -> None:
        """Add dealer hit card."""
        self.dealer.add_hit_card(card)
        self.shoe.deal_card(card)
    
    def split_player_hand(self, seat_id: str) -> None:
        """Split player hand."""
        if seat_id not in self.seats:
            raise ValueError(f"Seat {seat_id} not found")
        
        self.seats[seat_id].split_hand()
    
    def can_take_insurance(self) -> bool:
        """True if insurance is available (dealer shows Ace)."""
        return self.dealer.shows_ace
    
    def get_status(self) -> str:
        """Get comprehensive table status."""
        lines = []
        
        # Shoe info
        count_info = self.shoe.get_count_info()
        lines.append(f"Count: RC {count_info['running_count']:+d}, "
                    f"TC {count_info['true_count']:+.1f}, "
                    f"Decks Remaining: {count_info['decks_remaining']}")
        lines.append(f"Cards: {count_info['cards_dealt']}/{count_info['cards_dealt'] + count_info['cards_remaining']} "
                    f"({count_info['penetration']:.1f}% penetration)")
        
        # Dealer
        lines.append("")
        lines.append(self.dealer.describe())
        
        # Players
        if self.seats:
            lines.append("")
            lines.append("Players:")
            for seat_id, seat in self.seats.items():
                user_marker = " (USER)" if seat.is_user else ""
                lines.append(f"{seat_id}{user_marker}:")
                lines.append(seat.describe_hands())
        
        return "\n".join(lines)