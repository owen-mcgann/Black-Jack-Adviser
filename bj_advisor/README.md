# 🎰 Professional Blackjack Advisor

A terminal-based blackjack advisor that tracks live casino games and provides real-time, count-aware strategy advice using the Hi-Lo counting system with professionally accurate index plays.

## 🚀 Quick Start

**To run the advisor:**
```bash
python3 simulate.py
```

That's it! This is the **main entry point** for the complete blackjack tracking system.

## 🎯 What This Does

This is a **professional-grade card counting trainer** that:

- ✅ **Tracks live casino blackjack games** in real-time
- ✅ **Provides count-aware strategy advice** using exact Wizard of Odds thresholds  
- ✅ **Includes the complete Illustrious 18** index plays with precise true count deviations
- ✅ **Supports multiple players** and realistic casino game flow
- ✅ **Features comprehensive undo system** for error correction
- ✅ **Uses S17 rules** (6 decks, dealer stands soft 17, 3:2 blackjack, DAS allowed)

## 🎲 Core Features

### **Professional Card Counting**
- **Hi-Lo counting system** with automatic running/true count calculation
- **Mathematically precise index plays** from Wizard of Odds Illustrious 18
- **Insurance decisions** at TC ≥ +3 (professional standard)
- **Negative count deviations** for accurate low-count play

### **Expert Strategy Advice**
- **S17 basic strategy tables** with complete coverage
- **Count-based deviations** that override basic strategy when profitable
- **Detailed reasoning** explaining why each decision was made
- **Professional presentation** with clear action recommendations

### **Live Casino Simulation**
- **Multi-player support** with realistic seating
- **Proper dealing sequence** following casino procedures
- **Split hand management** up to 4 hands per player
- **Real-time count updates** as cards are revealed

## 📖 Usage Guide

### **Setting Up a Game**
```
setup Player1 Player2* Player3
```
(* marks you as the user - you'll get strategy advice)

### **Playing Hands**
```
newround          # Start a new round with casino-style dealing
advise           # Get detailed strategy advice for your hand
```

### **Card Input Format**
```
K, Q, J, T, 9, 8, 7, 6, 5, 4, 3, 2, A
```
Examples: `K` `QH` `TS` `A` (suits optional, ignored for counting)

### **Key Commands**
- `status` - Show complete table state with counts
- `shuffle` - Reset shoe and restart counting
- `undo` - Undo last card/action (comprehensive undo system)
- `help` - Show all available commands
- `quit` - Exit the advisor

## 🧠 Index Plays Included

The system includes **24 professional index plays** based on Wizard of Odds standards:

### **Most Important Plays**
1. **16 vs 10** (TC ≥ 0) - Stand instead of hit
2. **15 vs 10** (TC ≥ +4) - Stand instead of hit  
3. **Insurance** (TC ≥ +3) - Take when count is high
4. **10,10 vs 5** (TC ≥ +5) - Split the pair
5. **10,10 vs 6** (TC ≥ +4) - Split the pair

### **Key Doubling Plays**
- **11 vs A** (TC ≥ +1) - Double instead of hit
- **9 vs 2** (TC ≥ +1) - Double instead of hit
- **10 vs 10** (TC ≥ +4) - Double instead of hit

### **Negative Count Deviations**
- **13 vs 2** (TC ≤ -1) - Hit instead of stand
- **12 vs 4** (TC ≤ 0) - Hit instead of stand
- **12 vs 5** (TC ≤ -2) - Hit instead of stand
- **12 vs 6** (TC ≤ -1) - Hit instead of stand

## 🔧 Testing

Run the professional test suite:
```bash
python3 tests/test_professional_plays.py
```

Run basic strategy unit tests:
```bash
python3 -m pytest tests/test_basic_strategy.py
```

## 📁 Project Structure

```
bj_advisor/
├── simulate.py              # 🚀 MAIN ENTRY POINT
├── src/
│   ├── core/               # Game engine
│   │   ├── card.py         # Hi-Lo card system
│   │   ├── hand.py         # Hand evaluation
│   │   ├── table.py        # Game state management
│   │   └── rules.py        # S17 rules
│   ├── strategy/           # Strategy engine  
│   │   ├── basic_strategy.py # S17 basic strategy tables
│   │   ├── index_plays.py    # Illustrious 18 + deviations
│   │   └── advisor.py        # Integrated recommendations
│   └── tui/               # Terminal interface
│       └── table_simulator.py # Enhanced UI with undo system
└── tests/                 # Test suite
    ├── test_basic_strategy.py      # Unit tests
    └── test_professional_plays.py  # Index play verification
```

## 🎖️ Professional Standards

This advisor implements **exact thresholds from trusted sources**:

- **Wizard of Odds** Illustrious 18 index plays
- **Blackjack Apprenticeship** professional standards  
- **Stanford Wong** methodology from "Professional Blackjack"
- **Don Schlesinger** index play research from "Blackjack Attack"

## ⚠️ Legal Notice

This software is for **educational and training purposes only**. Use responsibly and in accordance with local laws and casino policies.

---

**Ready to become a better blackjack player? Run `python3 simulate.py` and start practicing!** 🃏