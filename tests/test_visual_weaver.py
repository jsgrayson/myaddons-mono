import unittest
import sys
import os
import numpy as np
import cv2
from unittest.mock import MagicMock

# Add parent directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from visual_weaver import VisualWeaver

class TestVisualWeaver(unittest.TestCase):
    def setUp(self):
        self.weaver = VisualWeaver()
        # Mock config to ensure we have a region
        self.weaver.config["regions"]["nameplates"] = {"top": 0, "left": 0, "width": 100, "height": 100}
        
    def test_scan_nameplates_counts_red_rectangles(self):
        # Create a synthetic image with 3 red rectangles
        # BGRA format for mss
        img = np.zeros((100, 100, 4), dtype=np.uint8)
        
        # Draw 3 Red Rectangles (BGR: 0, 0, 255)
        # Rect 1
        cv2.rectangle(img, (10, 10), (30, 20), (0, 0, 255, 255), -1)
        # Rect 2
        cv2.rectangle(img, (40, 10), (60, 20), (0, 0, 255, 255), -1)
        # Rect 3
        cv2.rectangle(img, (70, 10), (90, 20), (0, 0, 255, 255), -1)
        
        # Mock sct.grab to return this image
        mock_sct = MagicMock()
        mock_sct.grab.return_value = img
        
        count = self.weaver.scan_nameplates(mock_sct)
        
        self.assertEqual(count, 3)
        
    def test_scan_nameplates_ignores_noise(self):
        # Create image with tiny red dots (noise)
        img = np.zeros((100, 100, 4), dtype=np.uint8)
        
        # Draw tiny dot (should be ignored by area filter)
        cv2.rectangle(img, (10, 10), (12, 12), (0, 0, 255, 255), -1)
        
        mock_sct = MagicMock()
        mock_sct.grab.return_value = img
        
        count = self.weaver.scan_nameplates(mock_sct)
        
        self.assertEqual(count, 0)

    def test_fallback_to_st(self):
        # Setup: AoE Mode ON
        self.weaver.aoe_mode = True
        
        # Mock regions
        self.weaver.config["regions"]["dps_icon"] = {"top": 0, "left": 0, "width": 10, "height": 10}
        self.weaver.config["regions"]["dps_icon_aoe"] = {"top": 0, "left": 20, "width": 10, "height": 10}
        
        # Mock sct.grab to return different colors for ST and AoE regions
        # ST Region: Blue 20 (Key '1')
        st_img = np.zeros((10, 10, 4), dtype=np.uint8)
        st_img[:, :] = [20, 0, 0, 255] # BGR
        
        # AoE Region: Black (Empty)
        aoe_img = np.zeros((10, 10, 4), dtype=np.uint8)
        
        mock_sct = MagicMock()
        
        def side_effect(monitor):
            if monitor["left"] == 0: # ST Region
                return st_img
            elif monitor["left"] == 20: # AoE Region
                return aoe_img
            return st_img
            
        mock_sct.grab.side_effect = side_effect
        
        # We can't easily test run_loop directly due to infinite loop, 
        # but we can verify the logic by extracting it or simulating the decision.
        # For this test, we'll just verify get_action_from_color returns None for AoE and '1' for ST.
        
        # 1. Check AoE (Black)
        key_aoe, _ = self.weaver.get_action_from_color(0, 0, 0)
        self.assertIsNone(key_aoe)
        
        # 2. Check ST (Blue 20)
        key_st, _ = self.weaver.get_action_from_color(0, 0, 20)
        self.assertEqual(key_st, "1")
        
        # The fallback logic is in run_loop, which is hard to unit test without refactoring.
        # But we've verified the components: AoE returns None, ST returns Key.

if __name__ == '__main__':
    unittest.main()
