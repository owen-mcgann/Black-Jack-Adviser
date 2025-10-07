"""
V1 BlackJack Game Tracker.
"""
import sys
from typing import NoReturn, List, Optional
from ..core import Table, DEFAULT_RULES, Card
from ..strategy import Advisor


class BlackjackTableSimulator:
    """Simple BlackJack Game Tracker."""
    
    def __init__(self):
        self.table = None
        self.advisor = None
        self.players = []
        self.user_position = None
        self.action_history = []  # Stack of actions for undo functionality
    
    def welcome_message(self) -> str:
        """Show enhanced welcome message."""
        return """
╔══════════════════════════════════════════════════════════════╗
║                  🎰 LIVE BLACKJACK TRACKER 🎰                 ║
╠══════════════════════════════════════════════════════════════╣
║  Simulated card counting and strategy advisor for live       ║
║  casino blackjack games. Track multiple seats, get real-     ║
║  time count updates, and receive expert strategy advice.     ║
╠══════════════════════════════════════════════════════════════╣
║                        🚀 COMMANDS                            ║
╠══════════════════════════════════════════════════════════════╣
║  setup <player> <user*>     │ Set up table (* marks YOU)           ║
║  newround                   │ Start round with REAL casino flow    ║
║  advise                     │ Get detailed strategy breakdown      ║
║  status                     │ Show complete table state            ║
║  shuffle                    │ Reset shoe and counts                ║
║  undo                       │ Undo last card/action                ║
║  help                       │ Show all commands                    ║
║  quit                       │ Exit tracker                         ║
╠══════════════════════════════════════════════════════════════╣
║                     📋 CARD FORMAT                            ║ 
╠══════════════════════════════════════════════════════════════╣
║  K, Q, J, T, 9, 8, 7, 6, 5, 4, 3, 2, A                       ║
║  Suits Optional: KH, QS, etc. (suits ignored for counting)   ║
╠══════════════════════════════════════════════════════════════╣
║                    🎯 GAME FEATURES                          ║
╠══════════════════════════════════════════════════════════════╣
║  ✓ Hi-Lo card counting system                                ║
║  ✓ S17 basic strategy tables                                 ║
║  ✓ Illustrious 18 index plays                                ║
║  ✓ Multi-player support                                      ║
║  ✓ Complete round management                                 ║
║  ✓ Real-time count tracking                                  ║
╚══════════════════════════════════════════════════════════════╝
        """.strip()
    
    def setup_players(self, names_str: str) -> str:
        """Set up players."""
        if not names_str:
            return "Usage: setup <player names with * for you>"
        
        names = names_str.split()
        self.players = []
        self.user_position = None
        
        for i, name in enumerate(names):
            if name.endswith('*'):
                name = name[:-1]
                self.user_position = i + 1
            self.players.append(name)
        
        if self.user_position is None:
            return "Mark yourself with * (e.g., 'setup Alice Me* Charlie')"
        
        # Initialize table
        self.table = Table(DEFAULT_RULES)
        self.advisor = Advisor()
        
        # Add seats
        for i, name in enumerate(self.players):
            is_user = (i + 1 == self.user_position)
            self.table.add_seat(name, is_user)
        
        # Show setup
        result = f"\n{'='*60}\n"
        result += f"🎰 BLACKJACK TABLE SETUP COMPLETE\n"
        result += f"{'='*60}\n\n"
        result += f"📍 SEATING ORDER:\n\n"
        
        for i, name in enumerate(self.players):
            marker = " ← YOU" if i + 1 == self.user_position else ""
            result += f"   Seat {i+1}: {name}{marker}\n"
        
        result += f"\n   🏛️  DEALER: House\n\n"
        result += f"{'='*60}\n"
        result += f"Ready! Type 'newround' to start.\n"
        result += f"{'='*60}"
        
        return result
    
    def _record_action(self, action_type: str, **kwargs):
        """Record an action for undo functionality."""
        action = {
            'type': action_type,
            'data': kwargs.copy()
        }
        self.action_history.append(action)
        
        # Limit history size to prevent memory issues
        if len(self.action_history) > 50:
            self.action_history.pop(0)
    
    def undo_last_action(self) -> str:
        """Undo the last recorded action."""
        if not self.action_history:
            return "❌ No actions to undo"
        
        if not self.table:
            return "❌ No active table"
            
        action = self.action_history.pop()
        action_type = action['type']
        data = action['data']
        
        try:
            if action_type == 'player_card':
                return self._undo_player_card(data['player'], data['card'])
            elif action_type == 'dealer_upcard':
                return self._undo_dealer_upcard(data['card'])
            elif action_type == 'dealer_hole_card':
                return self._undo_dealer_hole_card(data['card'])
            elif action_type == 'dealer_hit':
                return self._undo_dealer_hit(data['card'])
            elif action_type == 'round_start':
                return self._undo_round_start()
            else:
                return f"❌ Cannot undo action type: {action_type}"
                
        except Exception as e:
            # If undo fails, put action back
            self.action_history.append(action)
            return f"❌ Undo failed: {e}"
    
    def _undo_player_card(self, player: str, card: Card) -> str:
        """Undo adding a card to player."""
        if player not in self.table.seats:
            return f"❌ Player {player} not found"
            
        seat = self.table.seats[player]
        hand = seat.hands
        
        if not hand.cards or hand.cards[-1] != card:
            return f"❌ Cannot undo: {card} not the last card for {player}"
            
        # Remove card from hand
        hand.cards.pop()
        
        # Remove from shoe tracking and update count
        if card in self.table.shoe.cards_dealt:
            self.table.shoe.cards_dealt.remove(card)
            self.table.shoe.running_count -= card.hi_lo_value
            
        return f"✅ Undone: Removed {card} from {player} (RC: {self.table.shoe.running_count:+d})"
    
    def _undo_dealer_upcard(self, card: Card) -> str:
        """Undo dealer upcard."""
        if self.table.dealer.upcard != card:
            return f"❌ Cannot undo: {card} is not the dealer upcard"
            
        self.table.dealer.upcard = None
        
        # Remove from shoe tracking
        if card in self.table.shoe.cards_dealt:
            self.table.shoe.cards_dealt.remove(card)
            self.table.shoe.running_count -= card.hi_lo_value
            
        return f"✅ Undone: Removed dealer upcard {card} (RC: {self.table.shoe.running_count:+d})"
    
    def _undo_dealer_hole_card(self, card: Card) -> str:
        """Undo dealer hole card."""
        if self.table.dealer.hole_card != card:
            return f"❌ Cannot undo: {card} is not the dealer hole card"
            
        self.table.dealer.hole_card = None
        
        # Remove from shoe tracking  
        if card in self.table.shoe.cards_dealt:
            self.table.shoe.cards_dealt.remove(card)
            self.table.shoe.running_count -= card.hi_lo_value
            
        return f"✅ Undone: Removed dealer hole card {card} (RC: {self.table.shoe.running_count:+d})"
    
    def _undo_dealer_hit(self, card: Card) -> str:
        """Undo dealer hit card."""
        if not self.table.dealer.hit_cards or self.table.dealer.hit_cards[-1] != card:
            return f"❌ Cannot undo: {card} not the last dealer hit card"
            
        self.table.dealer.hit_cards.pop()
        
        # Remove from shoe tracking
        if card in self.table.shoe.cards_dealt:
            self.table.shoe.cards_dealt.remove(card)
            self.table.shoe.running_count -= card.hi_lo_value
            
        return f"✅ Undone: Removed dealer hit {card} (RC: {self.table.shoe.running_count:+d})"
    
    def _undo_round_start(self) -> str:
        """Undo round start."""
        if self.table.round_active:
            self.table.end_round()
            return "✅ Undone: Round ended"
        return "❌ No active round to undo"

    def start_new_round(self) -> str:
        """Start new round (EXACT REAL CASINO FLOW)."""
        if not self.table:
            return "Setup table first with: setup <playernames>"

        try:
            self.table.start_round()
            self._record_action('round_start')
            
            print(f"\n{'='*60}")
            print(f"🎴 NEW ROUND - REAL CASINO DEALING SEQUENCE")
            print(f"{'='*60}")
            
            # ROUND 1: First card to each player, then dealer upcard
            print(f"\n🔄 ROUND 1: First card around the table...")
            for i, name in enumerate(self.players):
                marker = " ⭐ (YOU)" if i + 1 == self.user_position else ""
                card1 = self._get_card_input(f"  {name}{marker} - Card 1: ")
                self.table.add_card_to_player(name, card1)
                self._record_action('player_card', player=name, card=card1)
                print(f"    ✓ {name}: {card1}")
            
            # Dealer upcard
            dealer_upcard = self._get_card_input(f"  🏛️  Dealer Upcard: ")
            self.table.add_dealer_upcard(dealer_upcard)
            self._record_action('dealer_upcard', card=dealer_upcard)
            print(f"    ✓ Dealer shows: {dealer_upcard}")
            
            # ROUND 2: Second card to each player, then dealer hole card
            print(f"\n🔄 ROUND 2: Second card around the table...")
            for i, name in enumerate(self.players):
                marker = " ⭐ (YOU)" if i + 1 == self.user_position else ""
                card2 = self._get_card_input(f"  {name}{marker} - Card 2: ")
                self.table.add_card_to_player(name, card2)
                self._record_action('player_card', player=name, card=card2)
                
                hand = self.table.seats[name].hands
                print(f"    ✓ {name}: {hand}")
            
            # Dealer hole card (dealt but hidden)
            dealer_hole = self._get_card_input(f"  🏛️  Dealer Hole Card (hidden): ")
            self.table.add_dealer_hole_card(dealer_hole)
            self._record_action('dealer_holecard', card=dealer_hole)
            print(f"    ✓ Dealer: {dealer_upcard} [hole card dealt but hidden]")
            
            # INSURANCE CHECK (when dealer shows Ace)
            if dealer_upcard.rank == 'A':
                if not self._handle_insurance():
                    return ""  # Round ended if dealer has blackjack
            
            # BLACKJACK CHECK (when dealer shows 10-value or Ace)
            if dealer_upcard.value == 10 or dealer_upcard.rank == 'A':
                if self.table.dealer.hand.is_blackjack():
                    print(f"\n🚨 DEALER BLACKJACK! {self.table.dealer.hand}")
                    print("Round ends immediately - no player decisions needed.")
                    self._show_results()
                    return ""
            
            # Show table state for decision making
            print(f"\n{'='*60}")
            print(f"🎯 READY FOR PLAYER DECISIONS")
            print(f"{'='*60}")
            self._show_table()
            
            # Player decisions
            print(f"\n{'='*60}")
            print(f"🎯 PLAYER DECISIONS")
            print(f"{'='*60}")
            
            for i, name in enumerate(self.players):
                self._handle_player(name, i + 1)
            
            # Dealer turn
            print(f"\n{'='*60}")
            print(f"🏛️  DEALERS TURN") 
            print(f"{'='*60}")
            
            self._handle_dealer()
            
            # Final results
            self._show_results()
            
            return ""
            
        except Exception as e:
            return f"Error: {e}"
    
    def _parse_card(self, card_str: str) -> Card:
        """Parse card from string."""
        # Remove whitespace and convert to uppercase
        card_str = card_str.strip().upper()
        
        # Handle common non-card inputs
        if card_str in ['STATUS', 'HELP', 'QUIT', 'EXIT', 'UNDO']:
            raise ValueError(f"'{card_str}' is not a valid card")
        
        # Remove suit characters (H, S, D, C) but preserve rank
        rank_str = ''.join(c for c in card_str if c not in 'HSDC')
        if not rank_str:
            rank_str = card_str[0] if card_str else ''
            
        return Card.from_string(rank_str)
    
    def _get_card_input(self, prompt: str) -> Card:
        """Get card input with special command handling."""
        while True:
            try:
                user_input = input(prompt).strip().upper()
                
                # Handle special commands during card input
                if user_input == 'UNDO':
                    result = self.undo_last_action()
                    print(f"    {result}")
                    continue
                elif user_input in ['STATUS', 'HELP']:
                    print(f"    Use '{user_input.lower()}' command outside of card input.")
                    continue
                elif user_input in ['QUIT', 'EXIT']:
                    print("    Use 'quit' command to exit the tracker.")
                    continue
                
                return self._parse_card(user_input)
                
            except EOFError:
                # Handle EOF gracefully (when no input is available)
                print("\n    No input available. Exiting...")
                raise SystemExit(0)
            except ValueError as e:
                print(f"    Error: {e}. Try again.")
            except Exception as e:
                print(f"    Invalid input: {e}. Try again.")
    
    def _get_action_input(self, prompt: str, player_name: str, position: int) -> str:
        """Get action input with undo support."""
        while True:
            try:
                action = input(f"{prompt}: ").strip().lower()
                
                # Handle undo special case
                if action == 'undo':
                    result = self.undo_last_action()
                    print(f"    {result}")
                    
                    # Check if undo changed the game state significantly
                    if "Round restarted" in result or "No actions" in result:
                        continue
                    else:
                        # Signal that we need to restart player decisions
                        return 'UNDO_RESTART'
                        
                # Valid actions
                if action in ['h', 'hit', 's', 'stand', 'd', 'double', 'p', 'split', 'a', 'advise']:
                    return action
                    
                print("Invalid choice. Use: h(it), s(tand), d(ouble), a(dvise)")
                
            except EOFError:
                # Handle EOF gracefully
                print("\n    No input available. Exiting...")
                raise SystemExit(0)
            except Exception as e:
                print(f"    Input error: {e}. Try again.")
    
    def _should_return_to_decision(self, player_name: str) -> bool:
        """Check if after undo we should return to this player's decision."""
        if player_name in self.table.seats:
            seat = self.table.seats[player_name]
            hand = seat.primary_hand
            # Player should decide if they have cards and aren't busted/21
            return (len(hand.cards) > 0 and 
                   not hand.is_busted and 
                   not hand.is_blackjack and 
                   hand.total < 21)
        return False
    
    def _show_table(self) -> None:
        """Show table state."""
        print(f"\n{'='*60}")
        print(f"🎰 TABLE STATE")
        print(f"{'='*60}")
        
        for i, name in enumerate(self.players):
            seat = self.table.seats[name]
            hand = seat.hands
            marker = " ← YOU" if i + 1 == self.user_position else ""
            print(f"   {name}{marker}: {hand}")
        
        dealer = self.table.dealer
        if hasattr(dealer, 'hand') and len(dealer.all_cards) >= 2:
            print(f"   DEALER: {dealer.hand}")
        elif dealer.upcard:
            print(f"   DEALER: {dealer.upcard} [?]")
        
        count = self.table.shoe.running_count
        true_count = self.table.shoe.true_count
        print(f"\n💎 COUNT: RC {count:+d} | TC {true_count:+.1f}")
        
        # Check for blackjacks
        blackjacks = []
        for name in self.players:
            hand = self.table.seats[name].hands
            if hand.is_blackjack:
                blackjacks.append(name)
        
        if blackjacks:
            print(f"\n🎉 BLACKJACK: {', '.join(blackjacks)}")
    
    def _handle_player(self, name: str, position: int) -> None:
        """Handle one player's complete turn."""
        while True:
            seat = self.table.seats[name]
            hand = seat.hands
            
            # Check if done
            if hand.is_blackjack or hand.is_busted or hand.total >= 21:
                if hand.is_blackjack:
                    print(f"\n{name}: BLACKJACK - No action needed")
                elif hand.is_busted:
                    print(f"\n{name}: BUSTED - No action needed")
                else:
                    print(f"\n{name}: 21 - No action needed")
                break
            
            marker = " (YOU)" if position == self.user_position else ""
            print(f"\n{name}{marker}: {hand}")
            
            # Show advice for user
            if position == self.user_position:
                try:
                    # Get required parameters for advice
                    dealer_upcard_value = self.table.dealer.upcard.value if self.table.dealer.upcard else 10
                    count_info = self.table.shoe.get_count_info()
                    true_count = count_info['true_count']
                    
                    advice = self.advisor.get_advice(hand, dealer_upcard_value, true_count)
                    print(f"💡 ADVICE: {advice['action'].value.upper()}")
                except Exception as e:
                    print(f"💡 ADVICE: Error - {e}")
            
            # Get decision with undo support
            can_split = hand.is_pair and not seat.has_splits
            if position == self.user_position:
                options = "(h)it, (s)tand, (d)ouble, (a)dvise"
                if can_split:
                    options += ", (p)split"
                print(f"Options: {options}")
            else:
                options = "(h)it, (s)tand, (d)ouble"
                if can_split:
                    options += ", (p)split"  
                print(f"Options: {options}")
            
            decision = self._get_action_input(f"{name} action", name, position)
            
            # Handle undo restart signal
            if decision == 'UNDO_RESTART':
                # An undo took us to an earlier state, restart player decisions
                return
            
            if decision in ['h', 'hit']:
                card = self._get_card_input(f"Card for {name}")
                self.table.add_card_to_player(name, card)
                self._record_action('player_card', player=name, card=card)
                new_hand = seat.hands
                print(f"✓ {name}: {card} → {new_hand}")
                
                if new_hand.is_busted:
                    print(f"🚨 {name} BUSTS!")
                    break
                elif new_hand.total == 21:
                    print(f"🎯 {name} has 21!")
                    break
            
            elif decision in ['s', 'stand']:
                print(f"✓ {name} stands on {hand}")
                break
            
            elif decision in ['d', 'double'] and hand.can_double:
                card = self._get_card_input(f"Double card for {name}")
                self.table.add_card_to_player(name, card)
                self._record_action('player_card', player=name, card=card)
                new_hand = seat.hands
                print(f"✓ {name} doubles: {card} → {new_hand}")
                
                if new_hand.is_busted:
                    print(f"🚨 {name} BUSTS!")
                break
            
            elif decision in ['p', 'split'] and can_split:
                # Split the hand
                self.table.split_player_hand(name)
                print(f"✓ {name} splits {hand.pair_rank.symbol},{hand.pair_rank.symbol}")
                
                # Handle each split hand
                split_hands = seat.all_hands
                for i, split_hand in enumerate(split_hands):
                    hand_num = i + 1
                    print(f"\n{name} Hand {hand_num}: {split_hand}")
                    
                    # Deal second card to each split hand
                    card = self._get_card_input(f"Card for {name} Hand {hand_num}")
                    # Add card to specific split hand
                    split_hand.add_card(card)
                    self.table.shoe.deal_card(card)  # Update count
                    self._record_action('player_card', player=name, card=card)
                    print(f"✓ {name} Hand {hand_num}: {card} → {split_hand}")
                    
                    # Special rule: Aces get one card only
                    if split_hand.has_ace and len(split_hand.cards) == 2:
                        print(f"✓ {name} Hand {hand_num}: Aces get one card only")
                        continue
                        
                # After splitting, continue with each hand's decisions
                break
            
            elif decision in ['a', 'advise']:
                if position == self.user_position:
                    print(self.get_advice())
                    continue
                else:
                    print(f"Advise option only available for you (marked position)")
                    continue
            
            else:
                if position == self.user_position:
                    valid_options = "h(it), s(tand), d(ouble), a(dvise)"
                    if can_split:
                        valid_options += ", p(split)"
                    print(f"Invalid choice. Use: {valid_options}")
                else:
                    valid_options = "h(it), s(tand), d(ouble)"
                    if can_split:
                        valid_options += ", p(split)"
                    print(f"Invalid choice. Use: {valid_options}")
                continue
        
        # Show count after each player
        print(f"💎 Count: RC {self.table.shoe.running_count:+d} | TC {self.table.shoe.true_count:+.1f}")
    
    def _handle_dealer(self) -> None:
        """Handle dealer's complete turn."""
        # Get hole card with retry
        while True:
            try:
                hole_card = self._get_card_input(f"Dealer hole card: ")
                self.table.add_dealer_hole_card(hole_card)
                self._record_action('dealer_hole_card', card=hole_card)
                dealer_hand = self.table.dealer.hand
                print(f"✓ Dealer reveals: {hole_card} → {dealer_hand}")
                break
            except Exception as e:
                print(f"Error adding hole card: {e}. Try again.")
                continue
            
        # Dealer hits to 17 with retry logic
        while self.table.dealer.hand.total < 17:
            dealer_hand = self.table.dealer.hand  # Refresh hand each iteration
            hit_card = self._get_card_input(f"Dealer hits (total {dealer_hand.total}): ")
            self.table.add_dealer_hit_card(hit_card)
            self._record_action('dealer_hit', card=hit_card)
            dealer_hand = self.table.dealer.hand  # Refresh after hit
            print(f"✓ Dealer: {hit_card} → {dealer_hand}")
                    
            if dealer_hand.is_busted:
                print(f"🚨 DEALER BUSTS!")
                break
        
        # Final dealer status
        final_dealer_hand = self.table.dealer.hand
        if not final_dealer_hand.is_busted and final_dealer_hand.total >= 17:
            print(f"✓ Dealer stands on {final_dealer_hand.total}")
    
    def _show_results(self) -> None:
        """Show final results."""
        dealer_hand = self.table.dealer.hand
        
        print(f"\n{'='*60}")
        print(f"🏁 FINAL RESULTS")
        print(f"{'='*60}")
        
        # Show dealer result without duplicate status
        if dealer_hand.is_busted:
            print(f"DEALER: {dealer_hand} - BUST")
        elif dealer_hand.is_blackjack:
            print(f"DEALER: {dealer_hand} - Blackjack!")
        else:
            print(f"DEALER: {dealer_hand} - {dealer_hand.total}")
        print(f"")
        
        for name in self.players:
            seat = self.table.seats[name]
            hand = seat.hands
            marker = " (YOU)" if name == self.table.user_seat_id else ""
            
            if hand.is_blackjack and not dealer_hand.is_blackjack:
                result = "BLACKJACK! 🎉"
            elif hand.is_busted:
                result = "BUST 🚨"
            elif dealer_hand.is_busted and not hand.is_busted:
                result = "WIN! 🎯"
            elif hand.total > dealer_hand.total and not hand.is_busted:
                result = "WIN! 🎯"
            elif hand.total == dealer_hand.total and not hand.is_busted and not dealer_hand.is_busted:
                result = "PUSH 🤝"
            else:
                result = "LOSE 😞"
            
            print(f"{name}{marker}: {hand} - {result}")
        
        # Final count
        count = self.table.shoe.running_count
        true_count = self.table.shoe.true_count
        cards_dealt = len(self.table.shoe.cards_dealt)
        penetration = (cards_dealt / (self.table.shoe.num_decks * 52)) * 100
        
        print(f"\n💎 FINAL COUNT: RC {count:+d} | TC {true_count:+.1f}")
        print(f"📊 Cards dealt: {cards_dealt} ({penetration:.1f}% penetration)")
        
        # Check if penetration suggests shuffle (like real casino)
        if self.table.shoe.needs_shuffle:
            print(f"⚠️  High penetration! Consider 'shuffle' command.")
        
        print(f"\n🎰 Round complete! Type 'newround' for next hand.")
        
        # End the round to allow next round
        self.table.end_round()
    
    def _handle_insurance(self) -> bool:
        """Handle insurance when dealer shows Ace. Returns True if round continues."""
        print(f"\n🛡️  INSURANCE OPTION (Dealer shows Ace)")
        print(f"{'='*60}")
        
        # Get true count for insurance decision
        count_info = self.table.shoe.get_count_info()
        true_count = count_info['true_count']
        
        print(f"📊 True Count: {true_count:+.1f}")
        print(f"💡 Insurance Strategy: Take insurance at True Count +3 or higher")
        
        # Ask user for insurance decision
        while True:
            try:
                response = input(f"\nTake insurance? (y/n): ").strip().lower()
                if response in ['y', 'yes']:
                    print(f"✓ Insurance taken")
                    break
                elif response in ['n', 'no']:
                    print(f"✓ No insurance")
                    break
                else:
                    print("Please enter 'y' or 'n'")
            except (EOFError, KeyboardInterrupt):
                print(f"\n✓ No insurance (default)")
                response = 'n'
                break
        
        # Check for dealer blackjack
        if self.table.dealer.hand.is_blackjack():
            print(f"\n🚨 DEALER HAS BLACKJACK!")
            print(f"Dealer: {self.table.dealer.hand}")
            
            if response in ['y', 'yes']:
                print(f"🛡️  Insurance pays 2:1 - You break even!")
            else:
                print(f"💸 No insurance - You lose main bet")
            
            # Show player blackjacks vs dealer blackjack
            for name in self.players:
                hand = self.table.seats[name].hands
                if hand.is_blackjack:
                    print(f"{name}: {hand} - PUSH (tie with dealer)")
                else:
                    print(f"{name}: {hand} - LOSES to dealer blackjack")
            
            return False  # Round ends
        else:
            print(f"✓ Dealer does NOT have blackjack")
            if response in ['y', 'yes']:
                print(f"💸 Insurance bet loses")
            return True  # Round continues
    
    def process_command(self, line: str) -> bool:
        """Process commands with enhanced error handling."""
        line = line.strip()
        if not line:
            return True
        
        parts = line.split()
        command = parts[0].lower()
        
        try:
            if command == "setup":
                result = self.setup_players(' '.join(parts[1:]))
            elif command == "newround":
                if self.table is None:
                    result = "Please run 'setup' first to configure players."
                else:
                    result = self.start_new_round()
            elif command == "advise":
                result = self.get_advice()
            elif command == "status":
                result = self.get_status()
            elif command == "shuffle":
                result = self.shuffle_shoe()
            elif command == "undo":
                result = self.undo_last_action()
            elif command in ["quit", "q", "exit"]:
                return False
            elif command == "help":
                result = self.welcome_message()
            else:
                result = f"❌ Unknown command: '{command}'. Type 'help' to see all commands."
            
            if result:
                print(result)
                
        except Exception as e:
            print(f"❌ Error: {e}")
        
        return True
    
    def get_advice(self) -> str:
        """Get detailed strategy advice with complete breakdown."""
        if not self.table or not self.table.user_seat_id:
            return "No user seat set up"
        
        try:
            user_seat = self.table.get_user_seat()
            user_hand = user_seat.hands
            dealer_upcard = self.table.dealer.upcard
            
            # Get count metrics
            count_info = self.table.shoe.get_count_info()
            
            # Get advice with correct parameters
            dealer_upcard_value = dealer_upcard.value if dealer_upcard else 10
            true_count = count_info['true_count']
            advice = self.advisor.get_advice(user_hand, dealer_upcard_value, true_count)
            
            # Format strings properly
            hand_str = str(user_hand)
            dealer_str = str(dealer_upcard)
            basic_action = advice['basic_strategy'].value.upper()
            final_action = advice['action'].value.upper()
            index_info = advice['reasoning'] if advice['count_influenced'] else 'None applicable'
            
            # Hand analysis
            hand_strength = 'Strong' if user_hand.total >= 17 else 'Moderate' if user_hand.total >= 12 else 'Weak'
            dealer_risk = 'High (Bust Card)' if dealer_upcard.value >= 2 and dealer_upcard.value <= 6 else 'Low (Pat Card)' if dealer_upcard.value >= 7 else 'Medium'
            count_favor = 'Player (+EV)' if count_info['true_count'] > 1 else 'House (-EV)' if count_info['true_count'] < -1 else 'Neutral'
            
            result = f"""
╔══════════════════════════════════════════════════════════════╗
║                    💡 STRATEGY ANALYSIS 💡                    ║
╠══════════════════════════════════════════════════════════════╣
║ Your Hand: {hand_str:<47}                                    ║
║ Dealer Up: {dealer_str:<47}                                  ║
╠══════════════════════════════════════════════════════════════╣
║                     📊 COUNT METRICS                          ║
╠══════════════════════════════════════════════════════════════╣
║ Running Count: {count_info['running_count']:+3d}             ║
║ True Count:    {count_info['true_count']:+5.1f}              ║
║ Decks Left:    {count_info['decks_remaining']:5.1f}          ║
║ Penetration:   {count_info['penetration']:5.1f}%             ║
╠══════════════════════════════════════════════════════════════╣
║                   🎯 DECISION BREAKDOWN                       ║
╠══════════════════════════════════════════════════════════════╣
║ Basic Strategy: {basic_action:<42}                           ║
║ Index Plays:    {index_info:<42}                             ║
║                                                              ║
║ >>> RECOMMENDATION: {final_action:<37} <<<                   ║
║                                                              ║
║ Reasoning: {advice['reasoning']:<48}                         ║
╠══════════════════════════════════════════════════════════════╣
║                   📈 MATHEMATICAL ANALYSIS                    ║
╠══════════════════════════════════════════════════════════════╣
║ Hand Strength: {hand_strength:<47}                           ║
║ Dealer Risk:   {dealer_risk:<47}                             ║
║ Count Favor:   {count_favor:<47}                             ║
║ Win Prob Est:  {'High' if user_hand.total >= 17 and dealer_upcard.value <= 6 else 'Medium' if user_hand.total >= 12 else 'Low':<47} ║
╠══════════════════════════════════════════════════════════════╣
║                     🔢 COMPUTATION LOGIC                      ║
╠══════════════════════════════════════════════════════════════╣
║ 1. Hand Type: {'Soft total' if user_hand.is_soft else 'Pair' if user_hand.is_pair else 'Hard total':<48} ║
║ 2. Basic Strategy Table Lookup: {user_hand.total if not user_hand.is_pair else str(user_hand.pair_rank.symbol)} vs {dealer_upcard.value:<20} ║
║ 3. Index Play Check: TC {count_info['true_count']:+.1f} vs thresholds     ║
║ 4. Final Decision: {final_action} (Basic Strategy)               ║
╚══════════════════════════════════════════════════════════════╝"""
            return result
        except Exception as e:
            return f"Error getting advice: {e}"
    
    def get_status(self) -> str:
        """Get table status."""
        if not self.table:
            return "No table set up"
        return self.table.get_status()
    
    def shuffle_shoe(self) -> str:
        """Reset shoe."""
        if not self.table:
            return "No table set up"
        self.table.shoe = self.table.shoe.__class__(
            self.table.rules.num_decks, 
            self.table.rules.penetration_threshold
        )
        # Clear action history after shuffle
        self.action_history.clear()
        return "🔄 Shoe shuffled. Counts reset."


def main() -> NoReturn:
    """Main game loop."""
    simulator = BlackjackTableSimulator()
    print(simulator.welcome_message())
    
    while True:
        try:
            line = input("\ninput> ")
            if not simulator.process_command(line):
                break
        except KeyboardInterrupt:
            break
        except EOFError:
            break
    
    print("Goodbye!")
    sys.exit(0)


if __name__ == "__main__":
    main()