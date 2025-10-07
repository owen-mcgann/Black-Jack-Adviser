"""
Unit tests for basic strategy implementation.
Verifies basic strategy matches published S17 charts.
"""
import unittest
from src.core import Hand, Card, Rank
from src.strategy import BasicStrategy, Action


class TestBasicStrategy(unittest.TestCase):
    """Test cases for basic strategy implementation."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.strategy = BasicStrategy()
    
    def test_hard_totals_basic_cases(self):
        """Test basic hard total cases."""
        # Always hit low totals
        hand = Hand([Card(Rank.THREE), Card(Rank.FIVE)])  # Hard 8
        action = self.strategy.get_action(hand, 6)
        self.assertEqual(action, Action.HIT)
        
        # Always stand on 17+
        hand = Hand([Card(Rank.TEN), Card(Rank.SEVEN)])  # Hard 17
        action = self.strategy.get_action(hand, 10)
        self.assertEqual(action, Action.STAND)
        
        # Double 11 vs most cards
        hand = Hand([Card(Rank.SIX), Card(Rank.FIVE)])  # Hard 11
        action = self.strategy.get_action(hand, 9)
        self.assertEqual(action, Action.DOUBLE)
    
    def test_soft_totals_basic_cases(self):
        """Test basic soft total cases."""
        # Soft 18 vs 9: Hit
        hand = Hand([Card(Rank.ACE), Card(Rank.SEVEN)])  # Soft 18
        action = self.strategy.get_action(hand, 9)
        self.assertEqual(action, Action.HIT)
        
        # Soft 19: Always stand
        hand = Hand([Card(Rank.ACE), Card(Rank.EIGHT)])  # Soft 19
        action = self.strategy.get_action(hand, 6)
        self.assertEqual(action, Action.STAND)
        
        # Soft 16 vs 6: Double
        hand = Hand([Card(Rank.ACE), Card(Rank.FIVE)])  # Soft 16
        action = self.strategy.get_action(hand, 6)
        self.assertEqual(action, Action.DOUBLE)
    
    def test_pairs_basic_cases(self):
        """Test basic pair cases."""
        # Always split Aces
        hand = Hand([Card(Rank.ACE), Card(Rank.ACE)])
        action = self.strategy.get_action(hand, 10)
        self.assertEqual(action, Action.SPLIT)
        
        # Always split 8s
        hand = Hand([Card(Rank.EIGHT), Card(Rank.EIGHT)])
        action = self.strategy.get_action(hand, 10)
        self.assertEqual(action, Action.SPLIT)
        
        # Never split 10s
        hand = Hand([Card(Rank.TEN), Card(Rank.KING)])
        action = self.strategy.get_action(hand, 6)
        self.assertEqual(action, Action.STAND)
        
        # Never split 5s (treat as 10)
        hand = Hand([Card(Rank.FIVE), Card(Rank.FIVE)])
        action = self.strategy.get_action(hand, 6)
        self.assertEqual(action, Action.DOUBLE)
    
    def test_doubling_restrictions(self):
        """Test doubling when not allowed."""
        # Should hit instead of double when can_double=False
        hand = Hand([Card(Rank.SIX), Card(Rank.FIVE)])  # Hard 11
        action = self.strategy.get_action(hand, 9, can_double=False)
        self.assertEqual(action, Action.HIT)
        
        # Soft double should become hit
        hand = Hand([Card(Rank.ACE), Card(Rank.FIVE)])  # Soft 16
        action = self.strategy.get_action(hand, 6, can_double=False)
        self.assertEqual(action, Action.HIT)
    
    def test_specific_strategy_points(self):
        """Test specific strategy decision points."""
        # 12 vs 2: Hit
        hand = Hand([Card(Rank.TEN), Card(Rank.TWO)])
        action = self.strategy.get_action(hand, 2)
        self.assertEqual(action, Action.HIT)
        
        # 12 vs 4: Stand
        hand = Hand([Card(Rank.TEN), Card(Rank.TWO)])
        action = self.strategy.get_action(hand, 4)
        self.assertEqual(action, Action.STAND)
        
        # 16 vs 10: Hit (basic strategy)
        hand = Hand([Card(Rank.TEN), Card(Rank.SIX)])
        action = self.strategy.get_action(hand, 10)
        self.assertEqual(action, Action.HIT)
        
        # 9 vs 2: Hit (not double)
        hand = Hand([Card(Rank.FIVE), Card(Rank.FOUR)])
        action = self.strategy.get_action(hand, 2)
        self.assertEqual(action, Action.HIT)
        
        # 9 vs 3: Double
        hand = Hand([Card(Rank.FIVE), Card(Rank.FOUR)])
        action = self.strategy.get_action(hand, 3)
        self.assertEqual(action, Action.DOUBLE)
    
    def test_insurance_basic_strategy(self):
        """Test insurance basic strategy (always no)."""
        self.assertFalse(self.strategy.should_take_insurance(True))
        self.assertFalse(self.strategy.should_take_insurance(False))
    
    def test_edge_cases(self):
        """Test edge cases and boundary conditions."""
        # Blackjack should stand
        hand = Hand([Card(Rank.ACE), Card(Rank.KING)])
        self.assertTrue(hand.is_blackjack)
        action = self.strategy.get_action(hand, 10)
        self.assertEqual(action, Action.STAND)
        
        # Busted hand should stand
        hand = Hand([Card(Rank.TEN), Card(Rank.TEN), Card(Rank.FIVE)])
        self.assertTrue(hand.is_busted)
        action = self.strategy.get_action(hand, 6)
        self.assertEqual(action, Action.STAND)
        
        # Soft total that becomes hard
        hand = Hand([Card(Rank.ACE), Card(Rank.FIVE), Card(Rank.SEVEN)])  # A,5,7 = Hard 13
        self.assertTrue(hand.is_hard)
        self.assertEqual(hand.total, 13)
        action = self.strategy.get_action(hand, 6)
        self.assertEqual(action, Action.STAND)


class TestCountAccuracy(unittest.TestCase):
    """Test Hi-Lo counting accuracy."""
    
    def test_hi_lo_values(self):
        """Test Hi-Lo values for all ranks."""
        # Low cards (+1)
        for rank in [Rank.TWO, Rank.THREE, Rank.FOUR, Rank.FIVE, Rank.SIX]:
            card = Card(rank)
            self.assertEqual(card.hi_lo_value, 1, f"{rank} should be +1")
        
        # Neutral cards (0)
        for rank in [Rank.SEVEN, Rank.EIGHT, Rank.NINE]:
            card = Card(rank)
            self.assertEqual(card.hi_lo_value, 0, f"{rank} should be 0")
        
        # High cards (-1)
        for rank in [Rank.TEN, Rank.JACK, Rank.QUEEN, Rank.KING, Rank.ACE]:
            card = Card(rank)
            self.assertEqual(card.hi_lo_value, -1, f"{rank} should be -1")


class TestHandEvaluation(unittest.TestCase):
    """Test hand evaluation accuracy."""
    
    def test_soft_hard_detection(self):
        """Test soft/hard hand detection."""
        # Soft hands
        hand = Hand([Card(Rank.ACE), Card(Rank.SEVEN)])  # A,7 = Soft 18
        self.assertTrue(hand.is_soft)
        self.assertEqual(hand.total, 18)
        
        # Hard hands
        hand = Hand([Card(Rank.TEN), Card(Rank.SEVEN)])  # 10,7 = Hard 17
        self.assertTrue(hand.is_hard)
        self.assertEqual(hand.total, 17)
        
        # Soft becoming hard
        hand = Hand([Card(Rank.ACE), Card(Rank.FIVE), Card(Rank.SEVEN)])  # A,5,7 = Hard 13
        self.assertTrue(hand.is_hard)
        self.assertEqual(hand.total, 13)
    
    def test_pair_detection(self):
        """Test pair detection."""
        # Same rank pairs
        hand = Hand([Card(Rank.EIGHT), Card(Rank.EIGHT)])
        self.assertTrue(hand.is_pair)
        self.assertEqual(hand.pair_rank, Rank.EIGHT)
        
        # Same value different rank (10-value cards)
        hand = Hand([Card(Rank.TEN), Card(Rank.KING)])
        self.assertTrue(hand.is_pair)  # Both worth 10
        
        # Not pairs
        hand = Hand([Card(Rank.EIGHT), Card(Rank.NINE)])
        self.assertFalse(hand.is_pair)
    
    def test_blackjack_detection(self):
        """Test blackjack detection."""
        # Natural blackjack
        hand = Hand([Card(Rank.ACE), Card(Rank.KING)])
        self.assertTrue(hand.is_blackjack)
        self.assertEqual(hand.total, 21)
        
        # 21 but not blackjack (3 cards)
        hand = Hand([Card(Rank.SEVEN), Card(Rank.SEVEN), Card(Rank.SEVEN)])
        self.assertFalse(hand.is_blackjack)
        self.assertEqual(hand.total, 21)


if __name__ == "__main__":
    unittest.main()