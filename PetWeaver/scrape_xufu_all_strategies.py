"""
Comprehensive Strategy Scraper for Xu-Fu's Pet Guides

Scrapes all winning strategies for all encounters to build a knowledge base
that can be used to:
1. Seed genetic algorithm with proven winners
2. Validate evolved teams against community solutions
3. Extract common winning patterns
"""

import requests
from bs4 import BeautifulSoup
import json
import time
import re
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field


@dataclass
class PetStrategy:
    """Represents a single pet in a strategy"""
    species_id: int
    species_name: str
    breed: str = "Any"  # B/B, P/P, S/S, etc.
    level: int = 25
    abilities: List[int] = field(default_factory=list)
    ability_names: List[str] = field(default_factory=list)
    notes: str = ""


@dataclass
class EncounterStrategy:
    """Complete strategy for an encounter"""
    encounter_name: str
    encounter_id: Optional[int] = None
    npc_name: str = ""
    pets: List[PetStrategy] = field(default_factory=list)
    notes: str = ""
    difficulty: str = "Unknown"
    win_rate: float = 0.0
    author: str = "Community"
    source_url: str = ""
    votes: int = 0


class XuFuStrategyScraper:
    """Scrapes winning strategies from Xu-Fu's Pet Guides"""
    
    BASE_URL = "https://www.wow-petguide.com"
    
    def __init__(self, delay: float = 1.0):
        """
        Args:
            delay: Delay between requests (be respectful)
        """
        self.delay = delay
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'PetWeaver Strategy Collector (Educational)'
        })
    
    def get_all_encounters(self) -> List[Dict]:
        """Get list of all available encounters"""
        # Xu-Fu has different pages for different categories
        categories = [
            "/index/World/Dragonflight",
            "/index/World/Shadowlands",
            "/index/World/Battle_for_Azeroth",
            "/index/World/Legion",
            "/index/World/Warlords_of_Draenor",
            "/index/World/Mists_of_Pandaria",
            "/index/World/Cataclysm",
            "/index/Dungeons",
            "/index/PvP"
        ]
        
        all_encounters = []
        
        for category in categories:
            print(f"Scraping category: {category}")
            try:
                url = f"{self.BASE_URL}{category}"
                response = self.session.get(url, timeout=10)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Find all encounter links
                # Xu-Fu uses specific structure - adjust as needed
                encounter_links = soup.find_all('a', href=re.compile(r'/Single/\d+'))
                
                for link in encounter_links:
                    encounter_url = self.BASE_URL + link['href']
                    encounter_name = link.text.strip()
                    encounter_id = re.search(r'/Single/(\d+)', link['href'])
                    
                    if encounter_id:
                        all_encounters.append({
                            'id': int(encounter_id.group(1)),
                            'name': encounter_name,
                            'url': encounter_url,
                            'category': category.split('/')[-1]
                        })
                
                time.sleep(self.delay)
                
            except Exception as e:
                print(f"Error scraping {category}: {e}")
                continue
        
        return all_encounters
    
    def scrape_encounter_strategies(
        self, 
        encounter_id: int,
        top_n: int = 5
    ) -> List[EncounterStrategy]:
        """
        Scrape top strategies for a specific encounter.
        
        Args:
            encounter_id: Xu-Fu encounter ID
            top_n: Number of top strategies to scrape
            
        Returns:
            List of EncounterStrategy objects
        """
        url = f"{self.BASE_URL}/Single/{encounter_id}"
        
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract encounter name
            encounter_name = soup.find('h1')
            encounter_name = encounter_name.text.strip() if encounter_name else f"Encounter_{encounter_id}"
            
            strategies = []
            
            # Find strategy blocks (structure varies - this is a template)
            strategy_blocks = soup.find_all('div', class_=re.compile(r'strategy|team'))[:top_n]
            
            for block in strategy_blocks:
                try:
                    strategy = self._parse_strategy_block(block, encounter_name, url)
                    if strategy and len(strategy.pets) == 3:  # Valid team
                        strategies.append(strategy)
                except Exception as e:
                    print(f"Error parsing strategy block: {e}")
                    continue
            
            time.sleep(self.delay)
            return strategies
            
        except Exception as e:
            print(f"Error scraping encounter {encounter_id}: {e}")
            return []
    
    def _parse_strategy_block(
        self, 
        block, 
        encounter_name: str,
        source_url: str
    ) -> Optional[EncounterStrategy]:
        """Parse a single strategy block from HTML"""
        # This is a template - actual parsing depends on Xu-Fu's HTML structure
        strategy = EncounterStrategy(
            encounter_name=encounter_name,
            source_url=source_url
        )
        
        # Extract pets (example selectors - adjust as needed)
        pet_elements = block.find_all('div', class_=re.compile(r'pet|slot'))
        
        for pet_elem in pet_elements[:3]:  # Max 3 pets
            try:
                # Extract pet name
                name_elem = pet_elem.find('a', href=re.compile(r'/npc=\d+'))
                if not name_elem:
                    continue
                    
                pet_name = name_elem.text.strip()
                
                # Extract species ID from URL
                species_match = re.search(r'npc=(\d+)', name_elem['href'])
                species_id = int(species_match.group(1)) if species_match else 0
                
                # Extract breed (if mentioned)
                breed_text = pet_elem.find(text=re.compile(r'[BHPS]/[BHPS]'))
                breed = breed_text.strip() if breed_text else "Any"
                
                # Extract abilities (look for ability links)
                ability_elems = pet_elem.find_all('a', href=re.compile(r'/spell=\d+'))
                abilities = []
                ability_names = []
                
                for ab_elem in ability_elems[:3]:  # Max 3 abilities
                    ab_match = re.search(r'spell=(\d+)', ab_elem['href'])
                    if ab_match:
                        abilities.append(int(ab_match.group(1)))
                        ability_names.append(ab_elem.text.strip())
                
                pet = PetStrategy(
                    species_id=species_id,
                    species_name=pet_name,
                    breed=breed,
                    abilities=abilities,
                    ability_names=ability_names
                )
                
                strategy.pets.append(pet)
                
            except Exception as e:
                print(f"Error parsing pet: {e}")
                continue
        
        # Extract strategy notes
        notes_elem = block.find('div', class_=re.compile(r'notes|description'))
        if notes_elem:
            strategy.notes = notes_elem.text.strip()
        
        # Extract votes/rating
        votes_elem = block.find(text=re.compile(r'\d+\s+votes?'))
        if votes_elem:
            votes_match = re.search(r'(\d+)', votes_elem)
            if votes_match:
                strategy.votes = int(votes_match.group(1))
        
        return strategy if strategy.pets else None
    
    def scrape_all_strategies(
        self,
        output_file: str = "xufu_strategies_complete.json",
        max_encounters: Optional[int] = None
    ) -> Dict:
        """
        Scrape strategies for ALL encounters.
        
        Args:
            output_file: Where to save results
            max_encounters: Limit for testing (None = all)
            
        Returns:
            Dictionary of encounter_id -> strategies
        """
        print("Fetching encounter list...")
        encounters = self.get_all_encounters()
        
        if max_encounters:
            encounters = encounters[:max_encounters]
        
        print(f"Found {len(encounters)} encounters to scrape")
        
        all_strategies = {}
        
        for i, encounter in enumerate(encounters, 1):
            print(f"[{i}/{len(encounters)}] Scraping: {encounter['name']}")
            
            strategies = self.scrape_encounter_strategies(encounter['id'], top_n=5)
            
            if strategies:
                all_strategies[encounter['id']] = {
                    'name': encounter['name'],
                    'category': encounter['category'],
                    'url': encounter['url'],
                    'strategies': [self._strategy_to_dict(s) for s in strategies]
                }
                print(f"  → Found {len(strategies)} strategies")
            else:
                print(f"  → No strategies found")
            
            # Save incrementally
            if i % 10 == 0:
                self._save_strategies(all_strategies, output_file)
                print(f"  → Saved progress ({i} encounters)")
        
        # Final save
        self._save_strategies(all_strategies, output_file)
        print(f"\n✓ Complete! Saved {len(all_strategies)} encounters to {output_file}")
        
        return all_strategies
    
    def _strategy_to_dict(self, strategy: EncounterStrategy) -> Dict:
        """Convert strategy to dictionary for JSON"""
        return {
            'encounter_name': strategy.encounter_name,
            'npc_name': strategy.npc_name,
            'pets': [
                {
                    'species_id': p.species_id,
                    'species_name': p.species_name,
                    'breed': p.breed,
                    'level': p.level,
                    'abilities': p.abilities,
                    'ability_names': p.ability_names,
                    'notes': p.notes
                }
                for p in strategy.pets
            ],
            'notes': strategy.notes,
            'difficulty': strategy.difficulty,
            'win_rate': strategy.win_rate,
            'author': strategy.author,
            'source_url': strategy.source_url,
            'votes': strategy.votes
        }
    
    def _save_strategies(self, data: Dict, filename: str):
        """Save strategies to JSON file"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)


def extract_seed_teams(strategies_file: str = "xufu_strategies_complete.json") -> Dict[str, List[List[int]]]:
    """
    Extract team compositions from scraped strategies for use as GA seeds.
    
    Returns:
        Dict of encounter_name -> list of [species_id, species_id, species_id]
    """
    with open(strategies_file) as f:
        data = json.load(f)
    
    seed_teams = {}
    
    for encounter_id, encounter_data in data.items():
        encounter_name = encounter_data['name']
        teams = []
        
        for strategy in encounter_data.get('strategies', []):
            team = [pet['species_id'] for pet in strategy['pets'] if pet['species_id'] > 0]
            if len(team) == 3:
                teams.append(team)
        
        if teams:
            seed_teams[encounter_name] = teams
    
    return seed_teams


if __name__ == "__main__":
    scraper = XuFuStrategyScraper(delay=2.0)  # 2 second delay between requests
    
    # Test with a few encounters first
    print("Starting strategy scrape (test mode)...")
    strategies = scraper.scrape_all_strategies(
        output_file="xufu_strategies_test.json",
        max_encounters=10  # Test with 10 encounters
    )
    
    print("\nSample strategies found:")
    for enc_id, enc_data in list(strategies.items())[:3]:
        print(f"\n{enc_data['name']}:")
        for strat in enc_data['strategies']:
            team = [p['species_name'] for p in strat['pets']]
            print(f"  - {' + '.join(team)}")
    
    # Extract seed teams
    print("\nExtracting seed teams...")
    seeds = extract_seed_teams("xufu_strategies_test.json")
    print(f"Extracted seeds for {len(seeds)} encounters")
