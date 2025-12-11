#!/usr/bin/env python3
"""
Daily Briefing - AI Executive Assistant
Aggregates high-priority items from all Holocron modules into a morning report.
"""

from typing import List, Dict, Any
from datetime import datetime
import random

class BriefingEngine:
    """
    Aggregates data from other engines to generate a prioritized briefing.
    """
    
    def __init__(self, scout, diplomat, warden, vault, knowledge, goblin, quartermaster=None, museum=None):
        self.scout = scout
        self.diplomat = diplomat
        self.warden = warden
        self.vault = vault
        self.knowledge = knowledge
        self.goblin = goblin
        self.quartermaster = quartermaster
        self.museum = museum
        
    def generate_briefing(self) -> Dict[str, Any]:
        """
        Generate the full briefing data structure.
        """
        print("DEBUG: Starting generate_briefing")
        now = datetime.now()
        
        # 1. Executive Summary
        print("DEBUG: Generating Executive Summary...")
        summary = self._generate_executive_summary()
        print("DEBUG: Executive Summary Done")
        
        # 3. Collect Action Items
        action_items = []
        action_items.extend(self._collect_action_items())
        action_items.extend(self._collect_logistics_items())
        action_items.extend(self._collect_museum_items())
        print("DEBUG: Action Items Done")
        
        # 3. Market Opportunities
        print("DEBUG: Getting Market Highlights...")
        market_opps = self._get_market_highlights()
        print("DEBUG: Market Highlights Done")
        
        # 4. Progression Status
        print("DEBUG: Getting Progression Status...")
        progression = self._get_progression_status()
        print("DEBUG: Progression Status Done")
        
        return {
            "date": now.strftime("%A, %B %d, %Y"),
            "greeting": self._get_greeting(now),
            "summary": summary,
            "action_items": action_items,
            "market": market_opps,
            "progression": progression
        }
        
    def _get_greeting(self, now: datetime) -> str:
        hour = now.hour
        if hour < 12:
            return "Good morning, Champion."
        elif hour < 18:
            return "Good afternoon, Champion."
        else:
            return "Good evening, Champion."

    def _generate_executive_summary(self) -> Dict:
        """High-level account overview"""
        # Mock data for now, eventually pull from a Warden module
        return {
            "gold_change": "+15,400g",
            "ilvl_avg": 615,
            "vault_status": f"{self.vault.get_status()['summary']['unlocked_slots']}/9 Slots",
            "alert_level": "Normal" if not self.scout.get_alerts() else "High"
        }
        
    def _collect_action_items(self) -> List[Dict]:
        """Aggregate and sort actionable items"""
        items = []
        
        # Diplomat Emissaries
        emissaries = self.diplomat.get_active_emissaries()
        for emissary in emissaries:
            if emissary['is_urgent'] or emissary['days_remaining'] <= 1:
                items.append({
                    "priority": "High",
                    "source": "Diplomat",
                    "text": f"Emissary Expiring: {emissary['title']} ({emissary['days_remaining']} day left)",
                    "action": "Complete Now",
                    "link": "/diplomat"
                })
            elif emissary['days_remaining'] <= 3:
                items.append({
                    "priority": "Medium",
                    "source": "Diplomat",
                    "text": f"Emissary Active: {emissary['title']}",
                    "action": "Plan Route",
                    "link": "/diplomat"
                })

        # Scout Alerts (Critical)
        alerts = self.scout.get_alerts()
        for alert in alerts:
            if alert['urgency'] == 'Critical':
                items.append({
                    "priority": "Critical",
                    "source": "Scout",
                    "text": f"{alert['event']} is active in {alert['zone']}",
                    "action": "Go Now",
                    "link": "/scout"
                })
                
        # Diplomat Opportunities (High)
        diplomat_data = self.diplomat.get_opportunities()
        for opp in diplomat_data:
            if opp.get('percent', 0) >= 90:
                items.append({
                    "priority": "High",
                    "source": "Diplomat",
                    "text": f"{opp['faction_name']} is {opp['percent']}% to Paragon",
                    "action": "Complete WQs",
                    "link": "/diplomat"
                })
                
        # Vault (Medium)
        vault_summary = self.vault.get_status()['summary']
        if vault_summary['unlocked_slots'] < 3:
             items.append({
                "priority": "Medium",
                "source": "Vault",
                "text": "Great Vault is mostly empty",
                "action": "Run M+ or Raid",
                "link": "/vault"
            })
            
        # Knowledge (Medium)
        knowledge = self.knowledge.get_status()
        if knowledge['weekly_progress'] < 100:
            items.append({
                "priority": "Medium",
                "source": "Knowledge",
                "text": f"Weekly Knowledge at {knowledge['weekly_progress']}%",
                "action": "Collect Points",
                "link": "/knowledge"
            })
            
        return items
        
    def _collect_logistics_items(self) -> List[Dict]:
        """Collect logistics-related action items from Quartermaster."""
        logistics_items = []
        if self.quartermaster:
            logistics_report = self.quartermaster.get_logistics_report()
            if logistics_report['pending_jobs'] > 0:
                for job in logistics_report['jobs']:
                    logistics_items.append({
                        "priority": "Medium",
                        "source": "Quartermaster",
                        "text": f"Logistics: Send {job['quantity']}x {job['item_name']} to {job['target']}",
                        "action": "Fulfill Order",
                        "link": "/quartermaster"
                    })
        return logistics_items

    def _collect_museum_items(self) -> List[Dict]:
        """Collect shadow collection items from Museum."""
        museum_items = []
        if self.museum:
            report = self.museum.get_shadow_collection()
            if report['total_items'] > 0:
                for item in report['items']:
                    museum_items.append({
                        "priority": "Low",
                        "source": "The Curator",
                        "text": f"Shadow Collection: Found unlearned {item['type']} '{item['name']}' on {item['character']} ({item['location']})",
                        "action": "Learn Item",
                        "link": "/museum"
                    })
        return museum_items

    def _get_market_highlights(self) -> List[Dict]:
        """Top market moves"""
        analysis = self.goblin.analyze_market()
        return analysis['opportunities'][:3]
        
    def _get_progression_status(self) -> Dict:
        """Raid/M+ progress summary"""
        # Mock data for now
        return {
            "raid_progress": "4/8 Heroic",
            "mythic_rating": 2450,
            "season_best": "+10"
        }
