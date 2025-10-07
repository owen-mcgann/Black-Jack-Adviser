"""
Basic strategy implementation for blackjack advisor.
Complete S17 lookup tables for hard totals, soft totals, and pairs.
"""
from enum import Enum
from typing import Dict, Tuple, Optional
from ..core import Rank, Hand


class Action(Enum):
    """Possible player actions in blackjack."""
    HIT = "Hit"
    STAND = "Stand"
    DOUBLE = "Double"
    SPLIT = "Split"
    
    def __str__(self):
        return self.value


class BasicStrategy:
    """Complete basic strategy tables for S17 rules."""
    
    def __init__(self):
        self._init_hard_totals()
        self._init_soft_totals()
        self._init_pairs()
    
    def _init_hard_totals(self):
        """Initialize hard total strategy table."""
        # Hard totals vs dealer upcard (2-A)
        # Format: {player_total: {dealer_upcard_value: action}}
        self.hard_totals: Dict[int, Dict[int, Action]] = {
            5: {2: Action.HIT, 3: Action.HIT, 4: Action.HIT, 5: Action.HIT, 6: Action.HIT, 7: Action.HIT, 8: Action.HIT, 9: Action.HIT, 10: Action.HIT, 11: Action.HIT},
            6: {2: Action.HIT, 3: Action.HIT, 4: Action.HIT, 5: Action.HIT, 6: Action.HIT, 7: Action.HIT, 8: Action.HIT, 9: Action.HIT, 10: Action.HIT, 11: Action.HIT},
            7: {2: Action.HIT, 3: Action.HIT, 4: Action.HIT, 5: Action.HIT, 6: Action.HIT, 7: Action.HIT, 8: Action.HIT, 9: Action.HIT, 10: Action.HIT, 11: Action.HIT},
            8: {2: Action.HIT, 3: Action.HIT, 4: Action.HIT, 5: Action.HIT, 6: Action.HIT, 7: Action.HIT, 8: Action.HIT, 9: Action.HIT, 10: Action.HIT, 11: Action.HIT},
            9: {2: Action.HIT, 3: Action.DOUBLE, 4: Action.DOUBLE, 5: Action.DOUBLE, 6: Action.DOUBLE, 7: Action.HIT, 8: Action.HIT, 9: Action.HIT, 10: Action.HIT, 11: Action.HIT},
            10: {2: Action.DOUBLE, 3: Action.DOUBLE, 4: Action.DOUBLE, 5: Action.DOUBLE, 6: Action.DOUBLE, 7: Action.DOUBLE, 8: Action.DOUBLE, 9: Action.DOUBLE, 10: Action.HIT, 11: Action.HIT},
            11: {2: Action.DOUBLE, 3: Action.DOUBLE, 4: Action.DOUBLE, 5: Action.DOUBLE, 6: Action.DOUBLE, 7: Action.DOUBLE, 8: Action.DOUBLE, 9: Action.DOUBLE, 10: Action.DOUBLE, 11: Action.DOUBLE},
            12: {2: Action.HIT, 3: Action.HIT, 4: Action.STAND, 5: Action.STAND, 6: Action.STAND, 7: Action.HIT, 8: Action.HIT, 9: Action.HIT, 10: Action.HIT, 11: Action.HIT},
            13: {2: Action.STAND, 3: Action.STAND, 4: Action.STAND, 5: Action.STAND, 6: Action.STAND, 7: Action.HIT, 8: Action.HIT, 9: Action.HIT, 10: Action.HIT, 11: Action.HIT},
            14: {2: Action.STAND, 3: Action.STAND, 4: Action.STAND, 5: Action.STAND, 6: Action.STAND, 7: Action.HIT, 8: Action.HIT, 9: Action.HIT, 10: Action.HIT, 11: Action.HIT},
            15: {2: Action.STAND, 3: Action.STAND, 4: Action.STAND, 5: Action.STAND, 6: Action.STAND, 7: Action.HIT, 8: Action.HIT, 9: Action.HIT, 10: Action.HIT, 11: Action.HIT},
            16: {2: Action.STAND, 3: Action.STAND, 4: Action.STAND, 5: Action.STAND, 6: Action.STAND, 7: Action.HIT, 8: Action.HIT, 9: Action.HIT, 10: Action.HIT, 11: Action.HIT},
            17: {2: Action.STAND, 3: Action.STAND, 4: Action.STAND, 5: Action.STAND, 6: Action.STAND, 7: Action.STAND, 8: Action.STAND, 9: Action.STAND, 10: Action.STAND, 11: Action.STAND},
            18: {2: Action.STAND, 3: Action.STAND, 4: Action.STAND, 5: Action.STAND, 6: Action.STAND, 7: Action.STAND, 8: Action.STAND, 9: Action.STAND, 10: Action.STAND, 11: Action.STAND},
            19: {2: Action.STAND, 3: Action.STAND, 4: Action.STAND, 5: Action.STAND, 6: Action.STAND, 7: Action.STAND, 8: Action.STAND, 9: Action.STAND, 10: Action.STAND, 11: Action.STAND},
            20: {2: Action.STAND, 3: Action.STAND, 4: Action.STAND, 5: Action.STAND, 6: Action.STAND, 7: Action.STAND, 8: Action.STAND, 9: Action.STAND, 10: Action.STAND, 11: Action.STAND},
            21: {2: Action.STAND, 3: Action.STAND, 4: Action.STAND, 5: Action.STAND, 6: Action.STAND, 7: Action.STAND, 8: Action.STAND, 9: Action.STAND, 10: Action.STAND, 11: Action.STAND},
        }
    
    def _init_soft_totals(self):
        """Initialize soft total strategy table."""
        # Soft totals vs dealer upcard (2-A)
        # Format: {player_total: {dealer_upcard_value: action}}
        self.soft_totals: Dict[int, Dict[int, Action]] = {
            13: {2: Action.HIT, 3: Action.HIT, 4: Action.HIT, 5: Action.DOUBLE, 6: Action.DOUBLE, 7: Action.HIT, 8: Action.HIT, 9: Action.HIT, 10: Action.HIT, 11: Action.HIT},  # A,2
            14: {2: Action.HIT, 3: Action.HIT, 4: Action.HIT, 5: Action.DOUBLE, 6: Action.DOUBLE, 7: Action.HIT, 8: Action.HIT, 9: Action.HIT, 10: Action.HIT, 11: Action.HIT},  # A,3
            15: {2: Action.HIT, 3: Action.HIT, 4: Action.DOUBLE, 5: Action.DOUBLE, 6: Action.DOUBLE, 7: Action.HIT, 8: Action.HIT, 9: Action.HIT, 10: Action.HIT, 11: Action.HIT},  # A,4
            16: {2: Action.HIT, 3: Action.HIT, 4: Action.DOUBLE, 5: Action.DOUBLE, 6: Action.DOUBLE, 7: Action.HIT, 8: Action.HIT, 9: Action.HIT, 10: Action.HIT, 11: Action.HIT},  # A,5
            17: {2: Action.HIT, 3: Action.DOUBLE, 4: Action.DOUBLE, 5: Action.DOUBLE, 6: Action.DOUBLE, 7: Action.HIT, 8: Action.HIT, 9: Action.HIT, 10: Action.HIT, 11: Action.HIT},  # A,6
            18: {2: Action.STAND, 3: Action.DOUBLE, 4: Action.DOUBLE, 5: Action.DOUBLE, 6: Action.DOUBLE, 7: Action.STAND, 8: Action.STAND, 9: Action.HIT, 10: Action.HIT, 11: Action.HIT},  # A,7
            19: {2: Action.STAND, 3: Action.STAND, 4: Action.STAND, 5: Action.STAND, 6: Action.STAND, 7: Action.STAND, 8: Action.STAND, 9: Action.STAND, 10: Action.STAND, 11: Action.STAND},  # A,8
            20: {2: Action.STAND, 3: Action.STAND, 4: Action.STAND, 5: Action.STAND, 6: Action.STAND, 7: Action.STAND, 8: Action.STAND, 9: Action.STAND, 10: Action.STAND, 11: Action.STAND},  # A,9
            21: {2: Action.STAND, 3: Action.STAND, 4: Action.STAND, 5: Action.STAND, 6: Action.STAND, 7: Action.STAND, 8: Action.STAND, 9: Action.STAND, 10: Action.STAND, 11: Action.STAND},  # A,10
        }
    
    def _init_pairs(self):
        """Initialize pair strategy table."""
        # Pairs vs dealer upcard (2-A)
        # Format: {pair_value: {dealer_upcard_value: action}}
        self.pairs: Dict[int, Dict[int, Action]] = {
            2: {2: Action.HIT, 3: Action.HIT, 4: Action.SPLIT, 5: Action.SPLIT, 6: Action.SPLIT, 7: Action.SPLIT, 8: Action.HIT, 9: Action.HIT, 10: Action.HIT, 11: Action.HIT},    # 2,2
            3: {2: Action.HIT, 3: Action.HIT, 4: Action.SPLIT, 5: Action.SPLIT, 6: Action.SPLIT, 7: Action.SPLIT, 8: Action.HIT, 9: Action.HIT, 10: Action.HIT, 11: Action.HIT},    # 3,3
            4: {2: Action.HIT, 3: Action.HIT, 4: Action.HIT, 5: Action.SPLIT, 6: Action.SPLIT, 7: Action.HIT, 8: Action.HIT, 9: Action.HIT, 10: Action.HIT, 11: Action.HIT},       # 4,4
            5: {2: Action.DOUBLE, 3: Action.DOUBLE, 4: Action.DOUBLE, 5: Action.DOUBLE, 6: Action.DOUBLE, 7: Action.DOUBLE, 8: Action.DOUBLE, 9: Action.DOUBLE, 10: Action.HIT, 11: Action.HIT},  # 5,5 (never split)
            6: {2: Action.HIT, 3: Action.SPLIT, 4: Action.SPLIT, 5: Action.SPLIT, 6: Action.SPLIT, 7: Action.HIT, 8: Action.HIT, 9: Action.HIT, 10: Action.HIT, 11: Action.HIT},    # 6,6
            7: {2: Action.SPLIT, 3: Action.SPLIT, 4: Action.SPLIT, 5: Action.SPLIT, 6: Action.SPLIT, 7: Action.SPLIT, 8: Action.HIT, 9: Action.HIT, 10: Action.HIT, 11: Action.HIT}, # 7,7
            8: {2: Action.SPLIT, 3: Action.SPLIT, 4: Action.SPLIT, 5: Action.SPLIT, 6: Action.SPLIT, 7: Action.SPLIT, 8: Action.SPLIT, 9: Action.SPLIT, 10: Action.SPLIT, 11: Action.SPLIT}, # 8,8 (always split)
            9: {2: Action.SPLIT, 3: Action.SPLIT, 4: Action.SPLIT, 5: Action.SPLIT, 6: Action.SPLIT, 7: Action.STAND, 8: Action.SPLIT, 9: Action.SPLIT, 10: Action.STAND, 11: Action.STAND}, # 9,9
            10: {2: Action.STAND, 3: Action.STAND, 4: Action.STAND, 5: Action.STAND, 6: Action.STAND, 7: Action.STAND, 8: Action.STAND, 9: Action.STAND, 10: Action.STAND, 11: Action.STAND}, # 10,10 (never split)
            11: {2: Action.SPLIT, 3: Action.SPLIT, 4: Action.SPLIT, 5: Action.SPLIT, 6: Action.SPLIT, 7: Action.SPLIT, 8: Action.SPLIT, 9: Action.SPLIT, 10: Action.SPLIT, 11: Action.SPLIT}, # A,A (always split)
        }
    
    def get_action(self, hand: Hand, dealer_upcard_value: int, can_double: bool = True) -> Action:
        """Get basic strategy action for a hand.
        
        Args:
            hand: Player hand
            dealer_upcard_value: Dealer's upcard value (2-11, where 11 = Ace)
            can_double: Whether doubling is allowed (False after hitting)
            
        Returns:
            Recommended action
        """
        if hand.is_busted:
            return Action.STAND  # No action needed for busted hands
        
        if hand.is_blackjack:
            return Action.STAND  # Stand on blackjack
        
        # Handle pairs first
        if hand.is_pair:
            pair_value = hand.pair_rank.bj_value
            if pair_value == 11:  # Aces
                pair_value = 11
            elif pair_value == 10:  # All 10-value cards treated as 10s
                pair_value = 10
            
            if pair_value in self.pairs:
                action = self.pairs[pair_value].get(dealer_upcard_value, Action.HIT)
                return action
        
        # Handle soft totals
        if hand.is_soft:
            total = hand.total
            if total in self.soft_totals:
                action = self.soft_totals[total].get(dealer_upcard_value, Action.HIT)
                # Convert double to hit if doubling not allowed
                if action == Action.DOUBLE and not can_double:
                    return Action.HIT
                return action
        
        # Handle hard totals
        total = hand.total
        if total in self.hard_totals:
            action = self.hard_totals[total].get(dealer_upcard_value, Action.HIT)
            # Convert double to hit if doubling not allowed
            if action == Action.DOUBLE and not can_double:
                return Action.HIT
            return action
        
        # Default for very low totals
        if total < 5:
            return Action.HIT
        
        # Default fallback
        return Action.HIT
    
    def should_take_insurance(self, dealer_shows_ace: bool) -> bool:
        """Basic strategy for insurance (always no for basic strategy)."""
        return False  # Never take insurance in basic strategy