"""
Game rules configuration for blackjack advisor.
"""
from dataclasses import dataclass


@dataclass
class Rules:
    """Blackjack game rules configuration."""
    
    # Dealer rules
    dealer_stands_soft_17: bool = True  # S17 rules
    
    # Deck configuration
    num_decks: int = 6
    
    # Player options
    double_after_split: bool = True  # DAS allowed
    surrender_allowed: bool = False  # No surrender (project-wide)
    
    # Payouts
    blackjack_payout: float = 1.5  # 3:2 blackjack
    
    # Split rules
    max_split_hands: int = 4
    split_aces_one_card: bool = True  # Only one card per split Ace
    
    # Shoe rules
    penetration_threshold: float = 0.75  # 75% penetration
    
    def __str__(self):
        """Human-readable rules description."""
        dealer_rule = "S17" if self.dealer_stands_soft_17 else "H17"
        das = "DAS" if self.double_after_split else "No DAS"
        surrender = "Surrender" if self.surrender_allowed else "No Surrender"
        blackjack = f"BJ {self.blackjack_payout}:1"
        
        return f"{dealer_rule}, {self.num_decks}D, {das}, {blackjack}, {surrender}"


# Default S17 rules as specified in requirements
DEFAULT_RULES = Rules(
    dealer_stands_soft_17=True,
    num_decks=6,
    double_after_split=True,
    surrender_allowed=False,
    blackjack_payout=1.5,
    max_split_hands=4,
    split_aces_one_card=True,
    penetration_threshold=0.75
)