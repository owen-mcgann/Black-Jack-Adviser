#!/usr/bin/env python3
"""Test professional index plays system with exact Wizard of Odds thresholds."""

from src.core.hand import Hand
from src.core.card import Card, Rank
from src.strategy.advisor import Advisor

def test_professional_index_plays():
    advisor = Advisor()
    
    print('🎯 TESTING PROFESSIONAL INDEX PLAYS (Wizard of Odds Standards)')
    print('=' * 70)
    
    # EXACT ILLUSTRIOUS 18 TEST CASES
    test_cases = [
        # === MOST IMPORTANT INDEX PLAYS ===
        
        # 16 vs 10 - THE most important (80% of deviation value)
        {'hand': [Rank.TEN, Rank.SIX], 'dealer': 10, 'count': 0.0, 'desc': '16 vs 10 at EXACT threshold (TC 0)'},
        {'hand': [Rank.TEN, Rank.SIX], 'dealer': 10, 'count': -0.1, 'desc': '16 vs 10 just below threshold'},
        {'hand': [Rank.TEN, Rank.SIX], 'dealer': 10, 'count': 0.1, 'desc': '16 vs 10 just above threshold'},
        
        # 15 vs 10 - Second most important
        {'hand': [Rank.NINE, Rank.SIX], 'dealer': 10, 'count': 4.0, 'desc': '15 vs 10 at EXACT threshold (TC +4)'},
        {'hand': [Rank.NINE, Rank.SIX], 'dealer': 10, 'count': 3.9, 'desc': '15 vs 10 just below threshold'},
        {'hand': [Rank.NINE, Rank.SIX], 'dealer': 10, 'count': 4.1, 'desc': '15 vs 10 just above threshold'},
        
        # === NEGATIVE COUNT DEVIATIONS (Critical!) ===
        
        # 13 vs 2 - Negative deviation at TC ≤ -1
        {'hand': [Rank.TEN, Rank.THREE], 'dealer': 2, 'count': -1.0, 'desc': '13 vs 2 at EXACT negative threshold (TC -1)'},
        {'hand': [Rank.TEN, Rank.THREE], 'dealer': 2, 'count': -0.9, 'desc': '13 vs 2 just above negative threshold'},
        {'hand': [Rank.TEN, Rank.THREE], 'dealer': 2, 'count': -1.1, 'desc': '13 vs 2 just below negative threshold'},
        
        # 12 vs 4 - Negative deviation at TC ≤ 0
        {'hand': [Rank.TEN, Rank.TWO], 'dealer': 4, 'count': 0.0, 'desc': '12 vs 4 at EXACT negative threshold (TC 0)'},
        {'hand': [Rank.TEN, Rank.TWO], 'dealer': 4, 'count': 0.1, 'desc': '12 vs 4 just above negative threshold'},
        {'hand': [Rank.TEN, Rank.TWO], 'dealer': 4, 'count': -0.1, 'desc': '12 vs 4 just below negative threshold'},
        
        # === DOUBLING DEVIATIONS ===
        
        # 11 vs A - Double at TC ≥ +1
        {'hand': [Rank.FIVE, Rank.SIX], 'dealer': 11, 'count': 1.0, 'desc': '11 vs A at EXACT threshold (TC +1)'},
        {'hand': [Rank.FIVE, Rank.SIX], 'dealer': 11, 'count': 0.9, 'desc': '11 vs A just below threshold'},
        {'hand': [Rank.FIVE, Rank.SIX], 'dealer': 11, 'count': 1.1, 'desc': '11 vs A just above threshold'},
        
        # 9 vs 2 - Double at TC ≥ +1
        {'hand': [Rank.FOUR, Rank.FIVE], 'dealer': 2, 'count': 1.0, 'desc': '9 vs 2 at EXACT threshold (TC +1)'},
        {'hand': [Rank.FOUR, Rank.FIVE], 'dealer': 2, 'count': 0.9, 'desc': '9 vs 2 just below threshold'},
        {'hand': [Rank.FOUR, Rank.FIVE], 'dealer': 2, 'count': 1.1, 'desc': '9 vs 2 just above threshold'},
        
        # === PAIR SPLITTING ===
        
        # 10,10 vs 5 - Split at TC ≥ +5 (extreme play)
        {'hand': [Rank.TEN, Rank.TEN], 'dealer': 5, 'count': 5.0, 'desc': '10,10 vs 5 at EXACT threshold (TC +5)'},
        {'hand': [Rank.TEN, Rank.TEN], 'dealer': 5, 'count': 4.9, 'desc': '10,10 vs 5 just below threshold'},
        {'hand': [Rank.TEN, Rank.TEN], 'dealer': 5, 'count': 5.1, 'desc': '10,10 vs 5 just above threshold'},
        
        # === INSURANCE TEST ===
        {'hand': [Rank.TEN, Rank.NINE], 'dealer': 11, 'count': 3.0, 'desc': 'Insurance at EXACT threshold (TC +3)'},
        {'hand': [Rank.TEN, Rank.NINE], 'dealer': 11, 'count': 2.9, 'desc': 'Insurance just below threshold'},
        {'hand': [Rank.TEN, Rank.NINE], 'dealer': 11, 'count': 3.1, 'desc': 'Insurance just above threshold'},
    ]
    
    for i, case in enumerate(test_cases, 1):
        print(f'\n{i:2d}. {case["desc"]}')
        print('-' * 55)
        
        hand = Hand()
        for rank in case['hand']:
            hand.add_card(Card(rank))
        
        advice = advisor.get_advice(hand, case['dealer'], case['count'], can_split=hand.is_pair)
        
        # Display comprehensive advice - showing simplified output for now
        print(f'Hand: {hand.total} vs dealer {case["dealer"]}')
        print(f'True Count: TC {case["count"]:+.1f}')
        print(f'Basic Strategy: {advice["basic_strategy"].value.upper()}')
        print(f'Final Action: {advice["action"].value.upper()}')
        print(f'Count Influenced: {"YES" if advice["count_influenced"] else "NO"}')
        
        # Show change if count influenced
        if advice["count_influenced"]:
            print(f'Deviation: {advice["basic_strategy"].value.upper()} -> {advice["action"].value.upper()}')
    
    # Summary statistics
    print(f'\n' + '='*50)
    print(f'PROFESSIONAL INDEX PLAYS SUMMARY')
    print(f'='*50)
    print(f'Total Index Plays Loaded: {len(advisor.index_plays.plays)}')
    print(f'Insurance Threshold: TC >= +{advisor.index_plays.insurance_threshold}')
    print(f'Based on: Wizard of Odds Illustrious 18')
    print(f'Rules: 6 decks, S17, DAS, 3:2 BJ, No Surrender')

if __name__ == '__main__':
    test_professional_index_plays()