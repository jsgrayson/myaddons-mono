#!/usr/bin/env python3
"""
Profession Specialization Recommender
Analyzes current spec investments and recommends next knowledge points for maximum profit
"""

import os
import psycopg2
import json

DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://jgrayson@localhost/holocron')

# Profession specialization trees (Dragonflight/TWW)
SPEC_TREES = {
    "Alchemy": {
        "Potion Mastery": {
            "max_points": 30,
            "bonuses": [
                {"points": 5, "bonus": "5% more potions crafted"},
                {"points": 15, "bonus": "Unlock rare potion recipes"},
                {"points": 30, "bonus": "Double potion proc chance"}
            ],
            "profit_rating": 8,  # Out of 10
            "market_demand": "High"
        },
        "Phial Cauldrons": {
            "max_points": 30,
            "bonuses": [
                {"points": 5, "bonus": "5% phial quality"},
                {"points": 15, "bonus": "Unlock cauldron recipes"},
                {"points": 30, "bonus": "Guaranteed rank 3 phials"}
            ],
            "profit_rating": 9,
            "market_demand": "Very High"
        },
        "Alchemical Theory": {
            "max_points": 30,
            "bonuses": [
                {"points": 10, "bonus": "Longer transmute cooldowns"},
                {"points": 20, "bonus": "More transmute procs"},
                {"points": 30, "bonus": "Transmute mastery"}
            ],
            "profit_rating": 7,
            "market_demand": "Medium"
        }
    },
    "Blacksmithing": {
        "Armorsmithing": {
            "max_points": 30,
            "bonuses": [
                {"points": 10, "bonus": "Better armor quality"},
                {"points": 20, "bonus": "Unlock plate recipes"},
                {"points": 30, "bonus": "Guaranteed rank 3 armor"}
            ],
            "profit_rating": 7,
            "market_demand": "Medium"
        },
        "Weaponsmithing": {
            "max_points": 30,
            "bonuses": [
                {"points": 10, "bonus": "Better weapon quality"},
                {"points": 20, "bonus": "Unlock rare weapons"},
                {"points": 30, "bonus": "Guaranteed rank 3 weapons"}
            ],
            "profit_rating": 9,
            "market_demand": "High"
        }
    },
    "Inscription": {
        "Rune Mastery": {
            "max_points": 30,
            "bonuses": [
                {"points": 5, "bonus": "Better rune quality"},
                {"points": 15, "bonus": "More runes per craft"},
                {"points": 30, "bonus": "Rune mastery"}
            ],
            "profit_rating": 6,
            "market_demand": "Medium"
        },
        "Archiving": {
            "max_points": 30,
            "bonuses": [
                {"points": 10, "bonus": "Better contract quality"},
                {"points": 20, "bonus": "Unlock rare contracts"},
                {"points": 30, "bonus": "Contract mastery"}
            ],
            "profit_rating": 8,
            "market_demand": "High"
        }
    }
}

def get_character_spec_data(character_name, profession):
    """Get character's current specialization points (mock for now)"""
    # TODO: Import from addon SavedVariables when available
    # For now, return sample data
    return {
        "total_points_spent": 25,
        "specs": {
            "Potion Mastery": 15,
            "Phial Cauldrons": 10,
            "Alchemical Theory": 0
        }
    }

def recommend_next_points(profession, current_specs):
    """
    Recommend where to spend next knowledge points
    
    IMPORTANT: WoW specs are PERMANENT - can't respec!
    So we recommend continuing current paths, but warn if bad investment.
    """
    
    if profession not in SPEC_TREES:
        return {"error": "Profession not supported yet"}
    
    trees = SPEC_TREES[profession]
    recommendations = []
    total_invested = sum(current_specs.values())
    
    # Analyze each spec tree
    for spec_name, spec_data in trees.items():
        current_points = current_specs.get(spec_name, 0)
        max_points = spec_data["max_points"]
        
        if current_points >= max_points:
            continue  # Already maxed
        
        # Find next milestone
        next_bonus = None
        for bonus in spec_data["bonuses"]:
            if current_points < bonus["points"]:
                next_bonus = bonus
                break
        
        # Calculate recommendation score
        score = 0
        
        # Factor 1: Already invested (MUST continue since can't respec) +50%
        if current_points > 0:
            score += 50  # Strong weight - you're committed!
        
        # Factor 2: Profit rating +40%
        score += spec_data["profit_rating"] * 4
        
        # Factor 3: Close to milestone +30%
        if next_bonus:
            points_to_milestone = next_bonus["points"] - current_points
            if points_to_milestone <= 5:
                score += 30 - (points_to_milestone * 5)
        
        recommendations.append({
            "spec": spec_name,
            "current_points": current_points,
            "max_points": max_points,
            "next_bonus": next_bonus,
            "profit_rating": spec_data["profit_rating"],
            "market_demand": spec_data["market_demand"],
            "recommendation_score": score,
            "reason": _generate_reason(spec_name, current_points, next_bonus, spec_data),
            "is_current_path": current_points > 0
        })
    
    # Sort by recommendation score
    recommendations.sort(key=lambda x: x["recommendation_score"], reverse=True)
    
    # Check for bad investment warning
    warning = None
    if total_invested > 10:  # Only warn if significantly invested
        current_paths = [r for r in recommendations if r["is_current_path"]]
        best_alternative = [r for r in recommendations if not r["is_current_path"]]
        
        if current_paths and best_alternative:
            current_best = current_paths[0]
            alternative_best = best_alternative[0]
            
            # Warn if alternative would be 30%+ better profit
            profit_diff = alternative_best["profit_rating"] - current_best["profit_rating"]
            if profit_diff >= 3:  # 3+ points difference (30%+)
                warning = {
                    "severity": "HIGH",
                    "message": f"⚠️  WARNING: {alternative_best['spec']} would be {profit_diff*10}% more profitable!",
                    "current_path": current_best["spec"],
                    "better_path": alternative_best["spec"],
                    "profit_difference": profit_diff * 10,
                    "recommendation": f"For FUTURE {profession} alts, invest in {alternative_best['spec']} instead"
                }
    
    return {
        "recommendations": recommendations,
        "warning": warning
    }

def _generate_reason(spec_name, current_points, next_bonus, spec_data):
    """Generate human-readable recommendation reason"""
    reasons = []
    
    if current_points > 0:
        reasons.append(f"You've already invested {current_points} points")
    
    if next_bonus:
        points_needed = next_bonus["points"] - current_points
        reasons.append(f"Only {points_needed} points to unlock: {next_bonus['bonus']}")
    
    if spec_data["profit_rating"] >= 8:
        reasons.append(f"High profit potential ({spec_data['market_demand']} demand)")
    
    return " | ".join(reasons) if reasons else "Good general investment"

def generate_spec_guide(character_name, profession):
    """Generate complete specialization guide for character"""
    
    # Get current spec state
    current_specs = get_character_spec_data(character_name, profession)
    
    # Get recommendations
    result = recommend_next_points(profession, current_specs["specs"])
    
    guide = {
        "character": character_name,
        "profession": profession,
        "total_knowledge_spent": current_specs["total_points_spent"],
        "current_specializations": current_specs["specs"],
        "recommendations": result["recommendations"][:3],  # Top 3
        "warning": result.get("warning"),  # Spec path warning
        "summary": _generate_summary(result["recommendations"][0]) if result["recommendations"] else None
    }
    
    return guide

def _generate_summary(top_rec):
    """Generate actionable summary"""
    return {
        "action": f"Invest next points in {top_rec['spec']}",
        "reason": top_rec['reason'],
        "expected_benefit": top_rec['next_bonus']['bonus'] if top_rec['next_bonus'] else "General improvement"
    }

def main():
    print("=" * 60)
    print("PROFESSION SPECIALIZATION RECOMMENDER")
    print("=" * 60)
    
    # Example: Analyze specs for different professions
    examples = [
        ("Vaxo", "Alchemy"),
        ("Vacco", "Inscription"),
        ("Slaythe", "Blacksmithing")
    ]
    
    all_guides = {}
    
    for char_name, profession in examples:
        print(f"\n📖 {char_name} - {profession}")
        
        guide = generate_spec_guide(char_name, profession)
        all_guides[f"{char_name}_{profession}"] = guide
        
        # Display recommendations
        if "recommendations" in guide:
            print(f"   Current: {guide['total_knowledge_spent']} knowledge points spent")
            
            # Show warning if bad path
            if guide.get("warning"):
                warning = guide["warning"]
                print(f"\n   {warning['message']}")
                print(f"   Current: {warning['current_path']} | Better: {warning['better_path']} (+{warning['profit_difference']:.0f}% profit)")
                print(f"   💡 {warning['recommendation']}")
            
            print(f"\n   Top 3 Recommendations:")
            for i, rec in enumerate(guide["recommendations"], 1):
                marker = "📍" if rec.get("is_current_path") else "💰"
                print(f"   {i}. {marker} {rec['spec']} (Score: {rec['recommendation_score']/10:.1f}/10)")
                print(f"      • {rec['reason']}")
                if rec['next_bonus']:
                    print(f"      • Next: {rec['next_bonus']['bonus']}")
        
        if guide.get("summary"):
            print(f"\n   ✅ Recommended Action: {guide['summary']['action']}")
            print(f"      {guide['summary']['reason']}")
    
    # Save guides
    output_file = 'spec_recommendations.json'
    with open(output_file, 'w') as f:
        json.dump(all_guides, f, indent=2)
    
    print(f"\n✅ Saved specialization guides to {output_file}")

if __name__ == "__main__":
    main()
