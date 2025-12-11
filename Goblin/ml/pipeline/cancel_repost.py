"""
Cancel/Repost Automation - Detect undercuts and manage reposting
"""
from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta
from loguru import logger
import time

@dataclass
class ActiveAuction:
    """Represents an active auction."""
    auction_id: int
    item_id: int
    stack_size: int
    price_per_item: int
    time_left: str  # 'SHORT', 'MEDIUM', 'LONG', 'VERY_LONG'
    posted_at: datetime
    
@dataclass
class UndercutDetection:
    """Detected undercut."""
    our_auction: ActiveAuction
    undercut_price: int
    undercut_amount: int
    should_cancel: bool
    reason: str

class CancelRepostManager:
    """Manage auction cancellations and reposts."""
    
    def __init__(self):
        self.our_auctions: List[ActiveAuction] = []
        self.cancel_queue: List[int] = []
        self.repost_queue: List[Dict] = []
        self.last_scan_time = None
        self.min_cancel_interval = 60  # seconds between cancel scans
        
    def scan_for_undercuts(self, ah_data: List[Dict]) -> List[UndercutDetection]:
        """
        Scan AH for undercuts on our auctions.
        
        ah_data: List of current AH listings
        Returns: List of detected undercuts
        """
        undercuts = []
        
        for our_auction in self.our_auctions:
            # Find lowest competing price for this item
            competing_prices = [
                listing['price_per_item'] 
                for listing in ah_data 
                if listing['item_id'] == our_auction.item_id 
                and listing.get('auction_id') != our_auction.auction_id
            ]
            
            if not competing_prices:
                continue  # No competition
            
            lowest_competitor = min(competing_prices)
            
            if lowest_competitor < our_auction.price_per_item:
                # We've been undercut!
                undercut_amount = our_auction.price_per_item - lowest_competitor
                
                # Decide if we should cancel
                should_cancel = self._should_cancel_auction(
                    our_auction, lowest_competitor, undercut_amount
                )
                
                undercuts.append(UndercutDetection(
                    our_auction=our_auction,
                    undercut_price=lowest_competitor,
                    undercut_amount=undercut_amount,
                    should_cancel=should_cancel,
                    reason=self._get_cancel_reason(our_auction, undercut_amount)
                ))
        
        logger.info(f"Found {len(undercuts)} undercuts, {sum(1 for u in undercuts if u.should_cancel)} recommended to cancel")
        return undercuts
    
    def _should_cancel_auction(self, auction: ActiveAuction, 
                               competitor_price: int, undercut_amount: int) -> bool:
        """Determine if auction should be cancelled."""
        
        # Don't cancel if just posted (give it time)
        if (datetime.now() - auction.posted_at).seconds < 300:  # 5 min
            return False
        
        # Don't cancel if almost expired anyway
        if auction.time_left == 'SHORT':
            return False
        
        # Cancel if undercut is significant
        undercut_pct = (undercut_amount / auction.price_per_item) * 100
        if undercut_pct > 5:  # More than 5% undercut
            return True
        
        # Cancel if undercut by more than 1 gold
        if undercut_amount > 10000:
            return True
        
        return False
    
    def _get_cancel_reason(self, auction: ActiveAuction, undercut_amount: int) -> str:
        """Get human-readable reason for cancellation."""
        undercut_pct = (undercut_amount / auction.price_per_item) * 100
        
        if undercut_pct > 10:
            return f"Heavily undercut ({undercut_pct:.1f}%)"
        elif undercut_amount > 10000:
            return f"Undercut by {undercut_amount//10000}g+"
        else:
            return f"Undercut by {undercut_amount} copper"
    
    def queue_cancel(self, auction_id: int):
        """Add auction to cancel queue."""
        if auction_id not in self.cancel_queue:
            self.cancel_queue.append(auction_id)
            logger.info(f"Queued auction {auction_id} for cancellation")
    
    def queue_repost(self, item_id: int, quantity: int, new_price: int):
        """Add item to repost queue."""
        self.repost_queue.append({
            'item_id': item_id,
            'quantity': quantity,
            'price': new_price,
            'queued_at': datetime.now()
        })
        logger.info(f"Queued item {item_id} for repost at {new_price} copper")
    
    def process_cancel_queue(self) -> List[int]:
        """
        Return list of auctions ready to cancel.
        (Addon will handle actual cancellation via user click)
        """
        ready_to_cancel = self.cancel_queue.copy()
        self.cancel_queue.clear()
        return ready_to_cancel
    
    def process_repost_queue(self, delay_seconds: int = 60) -> List[Dict]:
        """
        Return list of items ready to repost.
        Respects delay to avoid spam.
        """
        now = datetime.now()
        ready_to_post = []
        remaining = []
        
        for item in self.repost_queue:
            if (now - item['queued_at']).seconds >= delay_seconds:
                ready_to_post.append(item)
            else:
                remaining.append(item)
        
        self.repost_queue = remaining
        return ready_to_post
    
    def auto_cancel_repost_cycle(self, ah_data: List[Dict], 
                                 operations_manager) -> Dict:
        """
        Complete cycle: scan, detect undercuts, cancel, repost.
        
        Returns summary of actions taken.
        """
        # Scan for undercuts
        undercuts = self.scan_for_undercuts(ah_data)
        
        # Queue cancellations
        for undercut in undercuts:
            if undercut.should_cancel:
                self.queue_cancel(undercut.our_auction.auction_id)
                
                # Queue repost with new price (1 copper under competitor)
                new_price = undercut.undercut_price - 1
                self.queue_repost(
                    undercut.our_auction.item_id,
                    undercut.our_auction.stack_size,
                    new_price
                )
        
        # Process queues
        cancellations = self.process_cancel_queue()
        reposts = self.process_repost_queue()
        
        return {
            'undercuts_found': len(undercuts),
            'cancellations_queued': len(cancellations),
            'reposts_ready': len(reposts),
            'timestamp': datetime.now()
        }


class AuctionTracker:
    """Track our posted auctions."""
    
    def __init__(self):
        self.auctions: Dict[int, ActiveAuction] = {}
    
    def add_auction(self, auction: ActiveAuction):
        """Track a newly posted auction."""
        self.auctions[auction.auction_id] = auction
        logger.info(f"Tracking auction {auction.auction_id}")
    
    def remove_auction(self, auction_id: int):
        """Stop tracking (sold or cancelled)."""
        if auction_id in self.auctions:
            del self.auctions[auction_id]
            logger.info(f"Stopped tracking auction {auction_id}")
    
    def get_active_auctions(self) -> List[ActiveAuction]:
        """Get all currently tracked auctions."""
        return list(self.auctions.values())
    
    def update_from_ah_scan(self, ah_scan_data: List[Dict]):
        """Update tracked auctions based on AH scan."""
        # Remove auctions no longer on AH (sold)
        current_ids = {a['auction_id'] for a in ah_scan_data if 'auction_id' in a}
        
        sold = []
        for auction_id in list(self.auctions.keys()):
            if auction_id not in current_ids:
                sold.append(auction_id)
                self.remove_auction(auction_id)
        
        if sold:
            logger.info(f"{len(sold)} auctions sold!")
        
        return sold


if __name__ == "__main__":
    # Example
    manager = CancelRepostManager()
    tracker = AuctionTracker()
    
    # Simulate auction
    auction = ActiveAuction(
        auction_id=12345,
        item_id=6789,
        stack_size=20,
        price_per_item=5000,
        time_left='LONG',
        posted_at=datetime.now() - timedelta(minutes=10)
    )
    
    tracker.add_auction(auction)
    manager.our_auctions = [auction]
    
    # Simulate AH data with undercut
    ah_data = [
        {'auction_id': 99999, 'item_id': 6789, 'price_per_item': 4500}
    ]
    
    result = manager.auto_cancel_repost_cycle(ah_data, None)
    print("Cancel/Repost Cycle Result:")
    for k, v in result.items():
        print(f"  {k}: {v}")
