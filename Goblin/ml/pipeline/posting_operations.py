"""
Posting Operations System - Manage auction posting with operations
"""
import json
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from loguru import logger

@dataclass
class PostingOperation:
    """Defines how to post an item on AH."""
    name: str
    item_ids: List[int]
    
    # Pricing
    pricing_method: str  # 'fixed', 'dbmarket', 'ml_predicted', 'custom_formula'
    fixed_price: Optional[int] = None
    price_multiplier: float = 1.0
    custom_formula: Optional[str] = None
    
    # Undercut
    undercut_type: str = 'copper'  # 'copper', 'silver', 'gold', 'percent'
    undercut_amount: int = 1
    
    # Limits
    min_price: Optional[int] = None
    max_price: Optional[int] = None
    
    # Stack size
    stack_size: int = 1
    max_stacks: int = 5
    
    # Duration
    duration: str = '24h'  # '12h', '24h', '48h'
    
    # Repost settings
    auto_cancel_undercut: bool = True
    repost_delay_seconds: int = 60
    
    def calculate_price(self, market_price: int, ml_prediction: int, current_lowest: int) -> int:
        """Calculate posting price based on operation settings."""
        base_price = None
        
        if self.pricing_method == 'fixed':
            base_price = self.fixed_price
        elif self.pricing_method == 'dbmarket':
            base_price = market_price
        elif self.pricing_method == 'ml_predicted':
            base_price = ml_prediction
        elif self.pricing_method == 'custom_formula':
            # Would evaluate custom formula
            base_price = market_price
        else:
            base_price = market_price
        
        # Apply multiplier
        base_price = int(base_price * self.price_multiplier)
        
        # Calculate undercut
        undercut_price = current_lowest
        if self.undercut_type == 'copper':
            undercut_price -= self.undercut_amount
        elif self.undercut_type == 'silver':
            undercut_price -= self.undercut_amount * 100
        elif self.undercut_type == 'gold':
            undercut_price -= self.undercut_amount * 10000
        elif self.undercut_type == 'percent':
            undercut_price = int(current_lowest * (1 - self.undercut_amount / 100))
        
        # Use lower of base_price or undercut_price
        final_price = min(base_price, undercut_price) if undercut_price > 0 else base_price
        
        # Apply limits
        if self.min_price and final_price < self.min_price:
            final_price = self.min_price
        if self.max_price and final_price > self.max_price:
            final_price = self.max_price
        
        return max(1, final_price)  # At least 1 copper


class PostingManager:
    """Manage posting operations."""
    
    def __init__(self):
        self.operations: Dict[str, PostingOperation] = {}
        
    def add_operation(self, operation: PostingOperation):
        """Add or update a posting operation."""
        self.operations[operation.name] = operation
        logger.info(f"Added operation: {operation.name}")
    
    def remove_operation(self, name: str):
        """Remove an operation."""
        if name in self.operations:
            del self.operations[name]
            logger.info(f"Removed operation: {name}")
    
    def get_operation_for_item(self, item_id: int) -> Optional[PostingOperation]:
        """Find which operation applies to this item."""
        for op in self.operations.values():
            if item_id in op.item_ids:
                return op
        return None
    
    def generate_posting_instructions(self, item_id: int, quantity: int,
                                     market_price: int, ml_prediction: int,
                                     current_lowest: int) -> Dict:
        """
        Generate instructions for posting item.
        
        Returns dict with:
        - price: copper per item
        - stack_size: items per stack
        - num_stacks: how many stacks to post
        - duration: '12h', '24h', '48h'
        """
        operation = self.get_operation_for_item(item_id)
        
        if not operation:
            # Default operation
            return {
                'price': min(market_price, current_lowest - 1),
                'stack_size': 1,
                'num_stacks': min(quantity, 5),
                'duration': '24h',
                'operation_name': 'Default'
            }
        
        price = operation.calculate_price(market_price, ml_prediction, current_lowest)
        stack_size = operation.stack_size
        num_stacks = min(quantity // stack_size, operation.max_stacks)
        
        return {
            'price': price,
            'stack_size': stack_size,
            'num_stacks': num_stacks,
            'duration': operation.duration,
            'operation_name': operation.name,
            'auto_cancel_undercut': operation.auto_cancel_undercut
        }
    
    def save(self, filepath: str):
        """Save operations to file."""
        data = {name: asdict(op) for name, op in self.operations.items()}
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        logger.success(f"Saved {len(self.operations)} operations")
    
    def load(self, filepath: str):
        """Load operations from file."""
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
            
            self.operations = {}
            for name, op_dict in data.items():
                op = PostingOperation(**op_dict)
                self.operations[name] = op
            
            logger.success(f"Loaded {len(self.operations)} operations")
        except FileNotFoundError:
            logger.warning("No operations file found")


# Example operations
def create_default_operations() -> PostingManager:
    """Create some default operations."""
    manager = PostingManager()
    
    # Herbs - fast turnover
    manager.add_operation(PostingOperation(
        name="Herbs - Quick Flip",
        item_ids=[],  # Would be populated
        pricing_method='ml_predicted',
        undercut_type='copper',
        undercut_amount=1,
        stack_size=20,
        max_stacks=10,
        duration='12h',
        auto_cancel_undercut=True
    ))
    
    # Transmog - high value
    manager.add_operation(PostingOperation(
        name="Transmog - Premium",
        item_ids=[],
        pricing_method='dbmarket',
        price_multiplier=0.95,  # 95% of market
        undercut_type='percent',
        undercut_amount=2,
        stack_size=1,
        max_stacks=1,
        duration='48h',
        min_price=50000,  # 5g minimum
        auto_cancel_undercut=False  # Don't cancel, let it sit
    ))
    
    # Crafted items - cost-based
    manager.add_operation(PostingOperation(
        name="Crafted - Profit Margin",
        item_ids=[],
        pricing_method='custom_formula',
        custom_formula='crafting_cost * 1.3',  # 30% profit
        undercut_type='gold',
        undercut_amount=1,
        stack_size=1,
        max_stacks=5,
        duration='24h',
        auto_cancel_undercut=True
    ))
    
    return manager


if __name__ == "__main__":
    # Example
manager = create_default_operations()
    manager.save("posting_operations.json")
    
    # Example instruction generation
    instructions = manager.generate_posting_instructions(
        item_id=12345,
        quantity=100,
        market_price=5000,
        ml_prediction=5500,
        current_lowest=4800
    )
    
    print("Posting Instructions:")
    for k, v in instructions.items():
        print(f"  {k}: {v}")
