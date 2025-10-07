"""
Index plays implementation for blackjack advisor.
Illustrious 18 (no surrender) count-based deviations.
"""
from dataclasses import dataclass
from typing import List, Optional
from ..core import Hand
from .basic_strategy import Action


@dataclass
class IndexPlay:
    """Individual index play with count threshold."""
    name: str
    description: str
    player_total: int
    dealer_upcard: int
    is_soft: bool
    is_pair: bool
    true_count_threshold: float
    basic_action: Action
    index_action: Action
    
    def applies(self, hand: Hand, dealer_upcard_value: int, true_count: float) -> bool:
        """Check if this index play applies to the current situation."""
        # Check hand total
        if hand.total != self.player_total:
            return False
        
        # Check dealer upcard
        if dealer_upcard_value != self.dealer_upcard:
            return False
        
        # Check soft/hard
        if self.is_soft and not hand.is_soft:
            return False
        if not self.is_soft and hand.is_soft:
            return False
        
        # Check pair
        if self.is_pair and not hand.is_pair:
            return False
        if not self.is_pair and hand.is_pair:
            return False
        
        # CRITICAL FIX: Handle both positive AND negative count thresholds
        # For positive thresholds: apply when count >= threshold
        # For negative thresholds: apply when count <= threshold
        if self.true_count_threshold >= 0:
            return true_count >= self.true_count_threshold
        else:
            return true_count <= self.true_count_threshold
    
    def get_action(self, true_count: float) -> Action:
        """Get the action for this index play given the true count."""
        # CRITICAL FIX: Proper logic for positive and negative deviations
        if self.true_count_threshold >= 0:
            # Positive deviation: use index action when count is high enough
            if true_count >= self.true_count_threshold:
                return self.index_action
        else:
            # Negative deviation: use index action when count is low enough
            if true_count <= self.true_count_threshold:
                return self.index_action
                
        return self.basic_action


class IndexPlays:
    """Complete professional index plays for optimal card counting."""
    
    def __init__(self):
        # Illustrious 18 + additional high-value index plays
        self.plays: List[IndexPlay] = [
            # CORE ILLUSTRIOUS 18 (Properly implemented)
            
            # 1. 16 vs 10: Stand at TC ≥ 0 (Most important play)
            IndexPlay(
                name="16 vs 10",
                description="Stand 16 vs 10 at TC ≥ 0",
                player_total=16,
                dealer_upcard=10,
                is_soft=False,
                is_pair=False,
                true_count_threshold=0.0,
                basic_action=Action.HIT,
                index_action=Action.STAND
            ),
            
            # 2. 15 vs 10: Stand at TC ≥ +4
            IndexPlay(
                name="15 vs 10",
                description="Stand 15 vs 10 at TC ≥ +4",
                player_total=15,
                dealer_upcard=10,
                is_soft=False,
                is_pair=False,
                true_count_threshold=4.0,
                basic_action=Action.HIT,
                index_action=Action.STAND
            ),
            
            # 3. 10 vs 10: Double at TC ≥ +4
            IndexPlay(
                name="10 vs 10",
                description="Double 10 vs 10 at TC ≥ +4",
                player_total=10,
                dealer_upcard=10,
                is_soft=False,
                is_pair=False,
                true_count_threshold=4.0,
                basic_action=Action.HIT,
                index_action=Action.DOUBLE
            ),
            
            # 4. 12 vs 3: Stand at TC ≥ +2
            IndexPlay(
                name="12 vs 3",
                description="Stand 12 vs 3 at TC ≥ +2",
                player_total=12,
                dealer_upcard=3,
                is_soft=False,
                is_pair=False,
                true_count_threshold=2.0,
                basic_action=Action.HIT,
                index_action=Action.STAND
            ),
            
            # 5. 12 vs 2: Stand at TC ≥ +3
            IndexPlay(
                name="12 vs 2",
                description="Stand 12 vs 2 at TC ≥ +3",
                player_total=12,
                dealer_upcard=2,
                is_soft=False,
                is_pair=False,
                true_count_threshold=3.0,
                basic_action=Action.HIT,
                index_action=Action.STAND
            ),
            
            # 6. 11 vs A: Double at TC ≥ +1
            IndexPlay(
                name="11 vs A",
                description="Double 11 vs A at TC ≥ +1",
                player_total=11,
                dealer_upcard=11,
                is_soft=False,
                is_pair=False,
                true_count_threshold=1.0,
                basic_action=Action.HIT,
                index_action=Action.DOUBLE
            ),
            
            # 7. 9 vs 2: Double at TC ≥ +1
            IndexPlay(
                name="9 vs 2",
                description="Double 9 vs 2 at TC ≥ +1",
                player_total=9,
                dealer_upcard=2,
                is_soft=False,
                is_pair=False,
                true_count_threshold=1.0,
                basic_action=Action.HIT,
                index_action=Action.DOUBLE
            ),
            
            # 8. 10 vs A: Double at TC ≥ +4
            IndexPlay(
                name="10 vs A",
                description="Double 10 vs A at TC ≥ +4",
                player_total=10,
                dealer_upcard=11,
                is_soft=False,
                is_pair=False,
                true_count_threshold=4.0,
                basic_action=Action.HIT,
                index_action=Action.DOUBLE
            ),
            
            # 9. 9 vs 7: Double at TC ≥ +3
            IndexPlay(
                name="9 vs 7",
                description="Double 9 vs 7 at TC ≥ +3",
                player_total=9,
                dealer_upcard=7,
                is_soft=False,
                is_pair=False,
                true_count_threshold=3.0,
                basic_action=Action.HIT,
                index_action=Action.DOUBLE
            ),
            
            # 10. 16 vs 9: Stand at TC ≥ +5
            IndexPlay(
                name="16 vs 9",
                description="Stand 16 vs 9 at TC ≥ +5",
                player_total=16,
                dealer_upcard=9,
                is_soft=False,
                is_pair=False,
                true_count_threshold=5.0,
                basic_action=Action.HIT,
                index_action=Action.STAND
            ),
            
            # NEGATIVE COUNT DEVIATIONS (Critical for accuracy!)
            
            # 11. 13 vs 2: HIT at TC ≤ -1 (Negative deviation)
            IndexPlay(
                name="13 vs 2 (negative)",
                description="Hit 13 vs 2 at TC ≤ -1",
                player_total=13,
                dealer_upcard=2,
                is_soft=False,
                is_pair=False,
                true_count_threshold=-1.0,
                basic_action=Action.STAND,
                index_action=Action.HIT
            ),
            
            # 12. 12 vs 4: HIT at TC ≤ 0 (Negative deviation)
            IndexPlay(
                name="12 vs 4 (negative)",
                description="Hit 12 vs 4 at TC ≤ 0",
                player_total=12,
                dealer_upcard=4,
                is_soft=False,
                is_pair=False,
                true_count_threshold=0.0,
                basic_action=Action.STAND,
                index_action=Action.HIT
            ),
            
            # 13. 12 vs 5: HIT at TC ≤ -2
            IndexPlay(
                name="12 vs 5 (negative)",
                description="Hit 12 vs 5 at TC ≤ -2",
                player_total=12,
                dealer_upcard=5,
                is_soft=False,
                is_pair=False,
                true_count_threshold=-2.0,
                basic_action=Action.STAND,
                index_action=Action.HIT
            ),
            
            # 14. 12 vs 6: HIT at TC ≤ -1
            IndexPlay(
                name="12 vs 6 (negative)",
                description="Hit 12 vs 6 at TC ≤ -1",
                player_total=12,
                dealer_upcard=6,
                is_soft=False,
                is_pair=False,
                true_count_threshold=-1.0,
                basic_action=Action.STAND,
                index_action=Action.HIT
            ),
            
            # 15. 13 vs 3: HIT at TC ≤ -2
            IndexPlay(
                name="13 vs 3 (negative)",
                description="Hit 13 vs 3 at TC ≤ -2",
                player_total=13,
                dealer_upcard=3,
                is_soft=False,
                is_pair=False,
                true_count_threshold=-2.0,
                basic_action=Action.STAND,
                index_action=Action.HIT
            ),
            
            # ADDITIONAL HIGH-VALUE INDEX PLAYS
            
            # 16. 20 vs 5: Split at TC ≥ +5 (Extreme positive count)
            IndexPlay(
                name="20 vs 5 (split)",
                description="Split 10,10 vs 5 at TC ≥ +5",
                player_total=20,
                dealer_upcard=5,
                is_soft=False,
                is_pair=True,
                true_count_threshold=5.0,
                basic_action=Action.STAND,
                index_action=Action.SPLIT
            ),
            
            # 17. 20 vs 6: Split at TC ≥ +4
            IndexPlay(
                name="20 vs 6 (split)",
                description="Split 10,10 vs 6 at TC ≥ +4",
                player_total=20,
                dealer_upcard=6,
                is_soft=False,
                is_pair=True,
                true_count_threshold=4.0,
                basic_action=Action.STAND,
                index_action=Action.SPLIT
            ),
            
            # 18. A,A vs A: Stand at TC ≤ -1 (Rare negative deviation)
            IndexPlay(
                name="AA vs A (negative)",
                description="Stand A,A vs A at TC ≤ -1",
                player_total=12,  # A,A = 12 or 2
                dealer_upcard=11,
                is_soft=True,
                is_pair=True,
                true_count_threshold=-1.0,
                basic_action=Action.SPLIT,
                index_action=Action.STAND
            ),
            
            # ADDITIONAL PROFESSIONAL INDEX PLAYS
            
            # 19. 8 vs 6: Double at TC ≥ +2
            IndexPlay(
                name="8 vs 6",
                description="Double 8 vs 6 at TC ≥ +2",
                player_total=8,
                dealer_upcard=6,
                is_soft=False,
                is_pair=False,
                true_count_threshold=2.0,
                basic_action=Action.HIT,
                index_action=Action.DOUBLE
            ),
            
            # 20. 15 vs A: Stand at TC ≥ +5
            IndexPlay(
                name="15 vs A",
                description="Stand 15 vs A at TC ≥ +5",
                player_total=15,
                dealer_upcard=11,
                is_soft=False,
                is_pair=False,
                true_count_threshold=5.0,
                basic_action=Action.HIT,
                index_action=Action.STAND
            ),
            
            # 21. 14 vs 10: Stand at TC ≥ +3
            IndexPlay(
                name="14 vs 10",
                description="Stand 14 vs 10 at TC ≥ +3",
                player_total=14,
                dealer_upcard=10,
                is_soft=False,
                is_pair=False,
                true_count_threshold=3.0,
                basic_action=Action.HIT,
                index_action=Action.STAND
            ),
            
            # 22. A,6 vs 2: Double at TC ≥ +1 (Soft total)
            IndexPlay(
                name="A,6 vs 2",
                description="Double A,6 vs 2 at TC ≥ +1",
                player_total=17,
                dealer_upcard=2,
                is_soft=True,
                is_pair=False,
                true_count_threshold=1.0,
                basic_action=Action.HIT,
                index_action=Action.DOUBLE
            ),
            
            # 23. A,5 vs 4: Double at TC ≥ +2
            IndexPlay(
                name="A,5 vs 4",
                description="Double A,5 vs 4 at TC ≥ +2",
                player_total=16,
                dealer_upcard=4,
                is_soft=True,
                is_pair=False,
                true_count_threshold=2.0,
                basic_action=Action.HIT,
                index_action=Action.DOUBLE
            ),
            
            # 24. 13 vs 4: HIT at TC ≤ -1 (Negative deviation)
            IndexPlay(
                name="13 vs 4 (negative)",
                description="Hit 13 vs 4 at TC ≤ -1",
                player_total=13,
                dealer_upcard=4,
                is_soft=False,
                is_pair=False,
                true_count_threshold=-1.0,
                basic_action=Action.STAND,
                index_action=Action.HIT
            ),
        ]
        
        # Insurance threshold (most important index play)
        self.insurance_threshold = 3.0  # Take insurance at TC ≥ +3
    
    def get_applicable_plays(self, hand: Hand, dealer_upcard_value: int, 
                           true_count: float) -> List[IndexPlay]:
        """Get all index plays that apply to the current situation."""
        applicable = []
        for play in self.plays:
            if play.applies(hand, dealer_upcard_value, true_count):
                applicable.append(play)
        return applicable
    
    def get_index_action(self, hand: Hand, dealer_upcard_value: int, 
                        true_count: float, basic_action: Action) -> tuple[Action, Optional[IndexPlay]]:
        """Get action considering index plays.
        
        Returns:
            Tuple of (action, applicable_index_play)
        """
        applicable_plays = self.get_applicable_plays(hand, dealer_upcard_value, true_count)
        
        if applicable_plays:
            # Use the first applicable play (they should be mutually exclusive)
            play = applicable_plays[0]
            return play.get_action(true_count), play
        
        return basic_action, None
    
    def should_take_insurance(self, true_count: float) -> bool:
        """Check if insurance should be taken based on true count."""
        return true_count >= self.insurance_threshold
    
    def get_insurance_explanation(self, true_count: float) -> str:
        """Get explanation for insurance decision."""
        if true_count >= self.insurance_threshold:
            return f"Take insurance (TC {true_count:+.1f} ≥ +3.0)"
        else:
            return f"Skip insurance (TC {true_count:+.1f} < +3.0)"