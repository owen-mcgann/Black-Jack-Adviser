#!/usr/bin/env python3
"""
Blackjack Table Simulator - Enhanced Main Entry Point

Realistic blackjack table simulator with proper game flow:
- Set up multiple players in seating order
- Follow casino dealing sequence
- Guided decision-making process
- Count-aware strategy advice
- Proper round progression

Usage:
    python simulate.py

Game Flow:
    1. setup - Configure players and seating
    2. deal - Deal initial cards to all players
    3. Players make decisions in casino order
    4. Dealer plays following S17 rules
    5. Results shown for all hands
    6. Continue to next round

Commands:
    setup               - Set up table with players
    deal                - Start new round
    hit / h             - Current player hits
    stand / s           - Current player stands
    double / d          - Current player doubles down
    split               - Current player splits pair
    advise              - Get count-aware strategy advice
    status              - Show complete table state
    shuffle             - Reset shoe and counts
    help                - Show all commands
    quit                - Exit simulator

Features:
    • Realistic casino table setup and flow
    • Multiple players with seating order
    • Automatic count tracking (Hi-Lo system)
    • Basic strategy + Illustrious 18 advice
    • Insurance decisions when dealer shows Ace
    • Split hands up to 4 per player
    • S17 dealer rules
"""

from src.tui.table_simulator import main

if __name__ == "__main__":
    main()