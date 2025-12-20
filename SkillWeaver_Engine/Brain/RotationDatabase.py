class RotationDatabase:
    def __init__(self):
        # We start by populating the "Unlimited" mapping
        self.spec_data = {
            "70": { # Ret Paladin
                "DEFAULT": [
                    {"name": "Execution Sentence", "spell_id": 343527, "priority": 1},
                    {"name": "Wake of Ashes", "spell_id": 255937, "priority": 2},
                    {"name": "Final Verdict", "spell_id": 383328, "priority": 3}
                ],
                "PANIC": [
                    {"name": "Shield of Vengeance", "spell_id": 184662, "priority": 1},
                    {"name": "Word of Glory", "spell_id": 85673, "priority": 2}
                ]
            }
            # ... all 39 specs follow
        }

    def get_sequence(self, spec_id, context="DEFAULT"):
        return self.spec_data.get(str(spec_id), {}).get(context, [])
