import unittest
from combat_log_parser import CombatLogParser

class TestCombatLogParser(unittest.TestCase):
    def setUp(self):
        self.parser = CombatLogParser("mock_path")

    def test_regex_parsing(self):
        # Test Ability Use
        log = "Starlette casts Powerball."
        result = self.parser._parse_log_line(log)
        self.assertEqual(result['type'], 'ability_use')
        self.assertEqual(result['details'], ('Starlette', 'Powerball'))

        # Test Damage
        log = "Starlette deals 250 damage to Enemy Pet."
        result = self.parser._parse_log_line(log)
        self.assertEqual(result['type'], 'damage')
        self.assertEqual(result['details'], ('Starlette', '250', 'Enemy Pet'))
        
        # Test Buff Gain
        log = "Enemy Pet gains Speed Boost."
        result = self.parser._parse_log_line(log)
        self.assertEqual(result['type'], 'buff_gain')
        self.assertEqual(result['details'], ('Enemy Pet', 'Speed Boost'))

    def test_auto_learn_logic(self):
        # Mock replay data with enemy pets info
        replay = {
            "enemy": "New Trainer",
            "enemy_pets": [
                {"name": "Enemy Pet A", "petID": 123, "displayID": 111},
                {"name": "Enemy Pet B", "petID": 456, "displayID": 222}
            ],
            "turns": [
                {
                    "events": [
                        {
                            "type": "ability_use",
                            "details": ("Enemy Pet A", "Ability 1")
                        }
                    ]
                },
                {
                    "events": [
                        {
                            "type": "ability_use",
                            "details": ("Enemy Pet A", "Ability 2")
                        }
                    ]
                },
                {
                    "events": [
                        {
                            "type": "ability_use",
                            "details": ("Enemy Pet B", "Ability 3")
                        }
                    ]
                }
            ]
        }
        
        # We capture stdout to verify the rotation print
        import io
        import sys
        captured_output = io.StringIO()
        sys.stdout = captured_output
        
        try:
            self.parser.auto_learn(replay)
            sys.stdout = sys.__stdout__
            output = captured_output.getvalue()
            
            print(output) # Print for manual verification
            
            # Verify rotations were captured
            self.assertIn('"Enemy Pet A": ["Ability 1", "Ability 2"]', output)
            self.assertIn('"Enemy Pet B": ["Ability 3"]', output)
            
        except Exception as e:
            sys.stdout = sys.__stdout__
            self.fail(f"Auto-learn failed: {e}")

if __name__ == '__main__':
    unittest.main()
