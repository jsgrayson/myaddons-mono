"""
Accounting System - Track all gold earned, spent, and profit/loss
"""
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import json
import os
from loguru import logger

@dataclass
class Transaction:
    """A single buy or sell transaction."""
    timestamp: datetime
    transaction_type: str  # 'buy', 'sell', 'craft_cost', 'ah_cut'
    item_id: int
    item_name: str
    quantity: int
    price_per_item: int
    total_amount: int  # Positive for income, negative for expenses
    character: str
    realm: str
    notes: Optional[str] = None
    
class AccountingSystem:
    """Track financial performance."""
    
    def __init__(self):
        self.transactions: List[Transaction] = []
        self.session_start = datetime.now()
        self.starting_gold = {}  # Per character
        
    def record_purchase(self, item_id: int, item_name: str, quantity: int,
                       price_per_item: int, character: str, realm: str):
        """Record an item purchase."""
        total = quantity * price_per_item
        
        self.transactions.append(Transaction(
            timestamp=datetime.now(),
            transaction_type='buy',
            item_id=item_id,
            item_name=item_name,
            quantity=quantity,
            price_per_item=price_per_item,
            total_amount=-total,  # Negative (expense)
            character=character,
            realm=realm
        ))
        
        logger.info(f"Recorded purchase: {item_name} x{quantity} for {total} copper")
    
    def record_sale(self, item_id: int, item_name: str, quantity: int,
                   price_per_item: int, character: str, realm: str):
        """Record an item sale."""
        gross = quantity * price_per_item
        ah_cut = int(gross * 0.05)
        net = gross - ah_cut
        
        # Record sale
        self.transactions.append(Transaction(
            timestamp=datetime.now(),
            transaction_type='sell',
            item_id=item_id,
            item_name=item_name,
            quantity=quantity,
            price_per_item=price_per_item,
            total_amount=net,  # Positive (income)
            character=character,
            realm=realm
        ))
        
        # Record AH cut
        self.transactions.append(Transaction(
            timestamp=datetime.now(),
            transaction_type='ah_cut',
            item_id=item_id,
            item_name=item_name,
            quantity=quantity,
            price_per_item=price_per_item,
            total_amount=-ah_cut,  # Negative (fee)
            character=character,
            realm=realm,
            notes=f"5% AH cut on sale of {item_name}"
        ))
        
        logger.info(f"Recorded sale: {item_name} x{quantity} for {net} copper (after cut)")
    
    def set_starting_gold(self, character: str, gold_amount: int):
        """Set starting gold for a character."""
        self.starting_gold[f"{character}"] = gold_amount
    
    def get_total_profit(self) -> int:
        """Get total profit across all transactions."""
        return sum(t.total_amount for t in self.transactions)
    
    def get_session_profit(self) -> int:
        """Get profit for current session."""
        session_transactions = [
            t for t in self.transactions 
            if t.timestamp >= self.session_start
        ]
        return sum(t.total_amount for t in session_transactions)
    
    def get_profit_by_character(self) -> Dict[str, int]:
        """Get profit breakdown by character."""
        by_char = {}
        for t in self.transactions:
            key = t.character
            by_char[key] = by_char.get(key, 0) + t.total_amount
        return by_char
    
    def get_profit_by_item(self) -> List[Dict]:
        """Get profit breakdown by item (best/worst sellers)."""
        by_item = {}
        
        for t in self.transactions:
            if t.item_id not in by_item:
                by_item[t.item_id] = {
                    'item_id': t.item_id,
                    'item_name': t.item_name,
                    'total_profit': 0,
                    'total_sold': 0,
                    'total_bought': 0
                }
            
            by_item[t.item_id]['total_profit'] += t.total_amount
            
            if t.transaction_type == 'sell':
                by_item[t.item_id]['total_sold'] += t.quantity
            elif t.transaction_type == 'buy':
                by_item[t.item_id]['total_bought'] += t.quantity
        
        # Sort by profit
        items = sorted(by_item.values(), key=lambda x: x['total_profit'], reverse=True)
        return items
    
    def get_daily_report(self, days: int = 7) -> Dict:
        """Get profit per day for last N days."""
        cutoff = datetime.now() - timedelta(days=days)
        recent = [t for t in self.transactions if t.timestamp >= cutoff]
        
        by_day = {}
        for t in recent:
            day = t.timestamp.date()
            by_day[day] = by_day.get(day, 0) + t.total_amount
        
        return dict(sorted(by_day.items()))
    
    def get_session_stats(self) -> Dict:
        """Get detailed session statistics."""
        session_txns = [t for t in self.transactions if t.timestamp >= self.session_start]
        
        buys = [t for t in session_txns if t.transaction_type == 'buy']
        sells = [t for t in session_txns if t.transaction_type == 'sell']
        
        total_spent = abs(sum(t.total_amount for t in buys))
        total_earned = sum(t.total_amount for t in sells)
        profit = sum(t.total_amount for t in session_txns)
        
        session_duration = (datetime.now() - self.session_start).seconds
        gold_per_hour = (profit / session_duration * 3600) if session_duration > 0 else 0
        
        return {
            'session_start': self.session_start,
            'session_duration_minutes': session_duration // 60,
            'total_transactions': len(session_txns),
            'items_bought': sum(t.quantity for t in buys),
            'items_sold': sum(t.quantity for t in sells),
            'total_spent': total_spent,
            'total_earned': total_earned,
            'net_profit': profit,
            'gold_per_hour': int(gold_per_hour),
            'roi_percent': (profit / total_spent * 100) if total_spent > 0 else 0
        }
    
    def export_to_csv(self, filepath: str):
        """Export transactions to CSV."""
        import csv
        
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        with open(filepath, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Timestamp', 'Type', 'Character', 'Item ID', 'Item Name', 
                           'Quantity', 'Price Per Item', 'Total Amount', 'Notes'])
            
            for t in self.transactions:
                writer.writerow([
                    t.timestamp.isoformat(),
                    t.transaction_type,
                    t.character,
                    t.item_id,
                    t.item_name,
                    t.quantity,
                    t.price_per_item,
                    t.total_amount,
                    t.notes or ''
                ])
        
        logger.success(f"Exported {len(self.transactions)} transactions to {filepath}")
    
    def save(self, filepath: str):
        """Save accounting data."""
        data = {
            'session_start': self.session_start.isoformat(),
            'starting_gold': self.starting_gold,
            'transactions': [asdict(t) for t in self.transactions]
        }
        
        # Convert datetime objects to strings
        for txn in data['transactions']:
            txn['timestamp'] = txn['timestamp'].isoformat()
        
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        
        logger.success(f"Saved accounting data to {filepath}")
    
    def load(self, filepath: str):
        """Load accounting data."""
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
            
            self.session_start = datetime.fromisoformat(data['session_start'])
            self.starting_gold = data['starting_gold']
            
            self.transactions = []
            for txn_dict in data['transactions']:
                txn_dict['timestamp'] = datetime.fromisoformat(txn_dict['timestamp'])
                self.transactions.append(Transaction(**txn_dict))
            
            logger.success(f"Loaded {len(self.transactions)} transactions")
        except FileNotFoundError:
            logger.warning("No accounting data found")


if __name__ == "__main__":
    # Example
    accounting = AccountingSystem()
    accounting.set_starting_gold("MainChar-Dalaran", 5000000)  # 500g
    
    # Simulate some transactions
    accounting.record_purchase(12345, "Eternal Fire", 20, 5000, "MainChar", "Dalaran")
    accounting.record_sale(12345, "Eternal Fire", 20, 6000, "MainChar", "Dalaran")
    
    stats = accounting.get_session_stats()
    print("Session Stats:")
    for k, v in stats.items():
        print(f"  {k}: {v}")
    
    print(f"\nProfit: {stats['net_profit']} copper ({stats['net_profit']//10000}g)")
    print(f"Gold/hour: {stats['gold_per_hour']//10000}g/hr")
