"""
Advisor implementation that combines basic strategy and index plays.
Provides comprehensive advice with count-based deviations.
"""
from typing import Optional, Dict, Any
from ..core import Hand, Table
from .basic_strategy import BasicStrategy, Action
from .index_plays import IndexPlays


class Advisor:
    """Complete blackjack advisor combining basic strategy and index plays."""
    
    def __init__(self):
        self.basic_strategy = BasicStrategy()
        self.index_plays = IndexPlays()
    
    def get_advice(self, hand: Hand, dealer_upcard_value: int, true_count: float, 
                   can_double: bool = True, can_split: bool = False) -> Dict[str, Any]:
        """Get comprehensive strategy advice including count-based deviations."""
        
        # Get basic strategy recommendation first
        basic_advice = self.basic_strategy.get_action(
            hand, dealer_upcard_value, can_double
        )
        
        # Check for index plays (count-based deviations)
        final_action, index_play = self.index_plays.get_index_action(
            hand, dealer_upcard_value, true_count, basic_advice
        )
        
        # Determine if count influenced the decision
        count_influenced = index_play is not None
        deviation_reason = index_play.name if index_play else None
        
        # Validate action based on game state
        if not can_double and final_action == Action.DOUBLE:
            final_action = Action.HIT
            if count_influenced:
                deviation_reason += " (hit instead of double - can't double)"
        
        if not (can_split and hand.is_pair) and final_action == Action.SPLIT:
            final_action = Action.STAND if hand.total >= 17 else Action.HIT
            if count_influenced:
                deviation_reason += " (can't split - using backup action)"
        
        # Format true count display
        count_display = f"{true_count:+.1f}" if true_count >= 0 else f"{true_count:.1f}"
        
        # Create advice response
        advice = {
            'action': final_action,
            'basic_strategy': basic_advice,
            'count_influenced': count_influenced,
            'true_count': true_count,
            'count_display': count_display,
            'reasoning': self._get_reasoning(hand, dealer_upcard_value, basic_advice, 
                                           index_play, final_action, true_count)
        }
        
        if deviation_reason:
            advice['deviation'] = deviation_reason
            
        return advice
    
    def _get_reasoning(self, hand: Hand, dealer_upcard: int, basic_action: Action,
                      index_play: Optional, final_action: Action, 
                      true_count: float) -> str:
        """Generate detailed reasoning for the recommendation."""
        
        hand_desc = self._format_hand_description(hand)
        dealer_desc = f"dealer {dealer_upcard}" if dealer_upcard != 11 else "dealer A"
        count_desc = f"TC {true_count:+.1f}" if true_count >= 0 else f"TC {true_count:.1f}"
        
        if index_play:
            # Count-based deviation
            threshold = index_play.true_count_threshold
            threshold_desc = f"TC ≥ {threshold:+.1f}" if threshold >= 0 else f"TC ≤ {threshold:.1f}"
            
            return (
                f"🎯 COUNT DEVIATION: {index_play.name} "
                f"({threshold_desc}) - Current {count_desc} triggers "
                f"{final_action.value.upper()} vs basic {basic_action.value.upper()}"
            )
        else:
            # Basic strategy
            if abs(true_count) >= 2.0:
                count_note = f" (Count {count_desc} doesn't trigger deviation)"
            else:
                count_note = f" (Count {count_desc} neutral)"
                
            return f"📚 BASIC STRATEGY: {hand_desc} vs {dealer_desc} = {final_action.value.upper()}{count_note}"
    
    def _format_hand_description(self, hand: Hand) -> str:
        """Format hand description for display."""
        if hand.is_pair:
            card_value = hand.cards[0].value
            if card_value == 11:
                return "A,A"
            else:
                return f"{card_value},{card_value}"
        elif hand.is_soft:
            non_ace_total = hand.total - 11
            return f"A,{non_ace_total}"
        else:
            return str(hand.total)
    
    def get_insurance_advice(self, true_count: float) -> Dict[str, Any]:
        """Get advice for insurance decision."""
        should_take = true_count >= self.index_plays.insurance_threshold
        
        return {
            'take_insurance': should_take,
            'true_count': true_count,
            'threshold': self.index_plays.insurance_threshold,
            'reasoning': (
                f"Insurance at TC ≥ +{self.index_plays.insurance_threshold:.1f}. "
                f"Current TC {true_count:+.1f} - "
                f"{'TAKE' if should_take else 'SKIP'} insurance"
            )
        }