#include <Keyboard.h>
#include <Mouse.h>

void setup() {
  Serial.begin(9600);
  Keyboard.begin();
  Mouse.begin();
}

void loop() {
  if (Serial.available() > 0) {
    byte slotID = Serial.read();

    // Handshake
    if (slotID == 0xFF) {
      Serial.write(0xAA);
      return;
    }

    // Movement Flag Update (Special Byte 0xFE)
    if (slotID == 0xFE) {
      isMoving = !isMoving; // Toggle or set explicit state
      return;
    }

    // BLOODLUST MODE (Special Byte 0xFC)
    // "High APM" Mode - Tighter Jitter for Haste specs
    if (slotID == 0xFC) {
      isLust = !isLust;
      return;
    }

    // MOUSE FLICK COMMAND (Special Byte 0xFD)
    // Packet: [0xFD] [SlotID] [X_High] [X_Low] [Y_High] [Y_Low]
    if (slotID == 0xFD) {
      while (Serial.available() < 5)
        ; // Wait for 5 bytes (Slot + 4 coords)
      byte pressSlot = Serial.read();
      int16_t dx = (Serial.read() << 8) | Serial.read();
      int16_t dy = (Serial.read() << 8) | Serial.read();

      // 1. FLICK TO TARGET
      performHumanFlick(dx, dy);

      // 2. PRESS CHORD (Universal Grid)
      // We map the Slot ID back to the physical key inside executeChord logic
      // But executeChord has delays. We need a "Press but don't release" or
      // standard pulse? For "Heroic Leap" (Press -> Click -> Release), it's:

      // A. Decode Slot ID to Keys (Simplified for this atomic block)
      // This requires looking up the key map. For efficiency, we assume the PC
      // Sends the MODIFIER and KEY codes directly in a different packet
      // structure? The user prompt asked for "Pulse the Chord". We can call a
      // helper.

      // Fast Pulse for reticle activation
      // Note: Limitation - we need to map SlotID -> Key here.
      // Re-using executeChord logic but modifying it to hold while clicking?
      // For now, simpler: Click initiates the ground spell if reticle is
      // active. If "Quick Cast" is off, we need: Press Spell -> Wait Reticle ->
      // Click. We assume "Press Spell" brings up reticle.

      executeChordForSlot(pressSlot); // Helper to find/press key

      // 3. PULSE CLICK (Confirm Reticle)
      delay(random(15, 30));
      Mouse.click();
      delay(random(15, 30));

      // 4. ZERO-SUM RETURN (Restore Camera)
      performHumanFlick(-dx, -dy);

      return;
    }

    // THE PHYSICAL AIR-GAP LOGIC
    // Maps Serial Byte -> Hardware F-Key Chord
    // PC sends Logic (Slot 1), Arduino sends Physical Key (Shift+F13)

    switch (slotID) {
    // BLOCK 1: NO MODIFIER (Slots 01-12) -> F13-F24
    case 0x01:
      executeChord(KEY_F13, 0);
      break;
    case 0x02:
      executeChord(KEY_F14, 0);
      break;
    case 0x03:
      executeChord(KEY_F15, 0);
      break;
    case 0x04:
      executeChord(KEY_F16, 0);
      break;
    case 0x05:
      executeChord(KEY_F17, 0);
      break;
    case 0x06:
      executeChord(KEY_F18, 0);
      break;
    case 0x07:
      executeChord(KEY_F19, 0);
      break;
    case 0x08:
      executeChord(KEY_F20, 0);
      break;
    case 0x09:
      executeChord(KEY_F21, 0);
      break;
    case 0x0A:
      executeChord(KEY_F22, 0);
      break;
    case 0x0B:
      executeChord(KEY_F23, 0);
      break;
    case 0x0C:
      executeChord(KEY_F24, 0);
      break;

    // BLOCK 2: SHIFT (Slots 13-24) -> Shift + F13-F24
    case 0x0D:
      executeChord(KEY_F13, MODIFIERKEY_SHIFT);
      break; // Slot 13
    case 0x0E:
      executeChord(KEY_F14, MODIFIERKEY_SHIFT);
      break;
    case 0x0F:
      executeChord(KEY_F15, MODIFIERKEY_SHIFT);
      break;
    case 0x10:
      executeChord(KEY_F16, MODIFIERKEY_SHIFT);
      break;
    case 0x11:
      executeChord(KEY_F17, MODIFIERKEY_SHIFT);
      break;
    case 0x12:
      executeChord(KEY_F18, MODIFIERKEY_SHIFT);
      break;
    case 0x13:
      executeChord(KEY_F19, MODIFIERKEY_SHIFT);
      break;
    case 0x14:
      executeChord(KEY_F20, MODIFIERKEY_SHIFT);
      break;
    case 0x15:
      executeChord(KEY_F21, MODIFIERKEY_SHIFT);
      break;
    case 0x16:
      executeChord(KEY_F22, MODIFIERKEY_SHIFT);
      break;
    case 0x17:
      executeChord(KEY_F23, MODIFIERKEY_SHIFT);
      break;
    case 0x18:
      executeChord(KEY_F24, MODIFIERKEY_SHIFT);
      break;

    // BLOCK 3: CTRL (Slots 25-36) -> Ctrl + F13-F24
    case 0x19:
      executeChord(KEY_F13, MODIFIERKEY_CTRL);
      break; // Slot 25
    case 0x1A:
      executeChord(KEY_F14, MODIFIERKEY_CTRL);
      break;
    case 0x1B:
      executeChord(KEY_F15, MODIFIERKEY_CTRL);
      break;
    case 0x1C:
      executeChord(KEY_F16, MODIFIERKEY_CTRL);
      break;
    case 0x1D:
      executeChord(KEY_F17, MODIFIERKEY_CTRL);
      break;
    case 0x1E:
      executeChord(KEY_F18, MODIFIERKEY_CTRL);
      break;
    case 0x1F:
      executeChord(KEY_F19, MODIFIERKEY_CTRL);
      break;
    case 0x20:
      executeChord(KEY_F20, MODIFIERKEY_CTRL);
      break;
    case 0x21:
      executeChord(KEY_F21, MODIFIERKEY_CTRL);
      break;
    case 0x22:
      executeChord(KEY_F22, MODIFIERKEY_CTRL);
      break;
    case 0x23:
      executeChord(KEY_F23, MODIFIERKEY_CTRL);
      break;
    case 0x24:
      executeChord(KEY_F24, MODIFIERKEY_CTRL);
      break; // Slot 36

    // BLOCK 4: ALT (Slots 37-48) -> Alt + F13-F24
    case 0x25:
      executeChord(KEY_F13, MODIFIERKEY_ALT);
      break; // Slot 37
    case 0x26:
      executeChord(KEY_F14, MODIFIERKEY_ALT);
      break;
    case 0x27:
      executeChord(KEY_F15, MODIFIERKEY_ALT);
      break;
    case 0x28:
      executeChord(KEY_F16, MODIFIERKEY_ALT);
      break;
    case 0x29:
      executeChord(KEY_F17, MODIFIERKEY_ALT);
      break;
    case 0x2A:
      executeChord(KEY_F18, MODIFIERKEY_ALT);
      break;
    case 0x2B:
      executeChord(KEY_F19, MODIFIERKEY_ALT);
      break;
    case 0x2C:
      executeChord(KEY_F20, MODIFIERKEY_ALT);
      break;
    case 0x2D:
      executeChord(KEY_F21, MODIFIERKEY_ALT);
      break;
    case 0x2E:
      executeChord(KEY_F22, MODIFIERKEY_ALT);
      break;
    case 0x2F:
      executeChord(KEY_F23, MODIFIERKEY_ALT);
      break;
    case 0x30:
      executeChord(KEY_F24, MODIFIERKEY_ALT);
      break; // Slot 48
    }
  }
}

void executeChord(char key, char mod) {
  // MOVEMENT WEIGHTING & LUST MODE
  // If moving, increase mean delay (Heavy)
  // If Lust, decrease mean delay (Snappy)

  // Global state tracking
  bool isMoving = false;
  bool isLust = false; // High Haste State: 25.0;
  float travelMean = isMoving ? 42.0 : 25.0;
  if (isLust)
    travelMean *= 0.7; // 30% faster hands

  float travelDev = isMoving ? 10.0 : 5.0;
  if (isLust)
    travelDev = 3.0;

  float holdMean = isMoving ? 85.0 : 60.0;
  if (isLust)
    holdMean = 40.0; // Rapid Taps (40ms)

  float holdDev = isMoving ? 15.0 : 10.0;
  if (isLust)
    holdDev = 5.0;

  // 1. TRAVEL TIME (Decision -> Hand reaches key)
  int travel = (int)constrain(getGaussianLimit(travelMean, travelDev), 5, 80);
  delay(travel);

  // 2. MODIFIER PRESS (Inter-Chord Gap)
  if (mod != 0) {
    Keyboard.press(mod);
    int gap = (int)constrain(getGaussianLimit(isLust ? 8 : 15, 3), 2, 30);
    delay(gap);
  }

  // 3. KEY PRESS
  Keyboard.press(key);

  // 4. KEY DEPRESS (Hold Time)
  int hold = (int)constrain(getGaussianLimit(holdMean, holdDev), 15, 160);
  delay(hold);
  Keyboard.releaseAll();
}

void performHumanFlick(int16_t targetX, int16_t targetY) {
  // Non-linear Humanized Curve
  // Faster start, slower end (Ease-Out)

  float currentX = 0;
  float currentY = 0;
  float remainingX = targetX;
  float remainingY = targetY;

  // Break movement into chunks to mimic polling rate/human rendering
  while (abs(remainingX) > 0 || abs(remainingY) > 0) {
    // Move 30% of remaining distance (Zeno's Paradox approach for Ease-Out)
    int stepX = remainingX * 0.3;
    int stepY = remainingY * 0.3;

    // Min step size to prevent infinite loop
    if (stepX == 0 && remainingX != 0)
      stepX = (remainingX > 0) ? 1 : -1;
    if (stepY == 0 && remainingY != 0)
      stepY = (remainingY > 0) ? 1 : -1;

    Mouse.move(stepX, stepY, 0);

    remainingX -= stepX;
    remainingY -= stepY;

    // Micro-sleep for human polling feel (1-3ms)
    delay(random(1, 4));
  }
}

void executeChordForSlot(byte slotID) {
  char key_code;
  char mod_code = 0;

  // Reverse Map (Slot -> F-Key + Mod)
  // 1-12: F13-F24
  if (slotID >= 1 && slotID <= 12) {
    key_code = KEY_F13 + (slotID - 1);
  }
  // 13-24: Shift + F13-F24
  else if (slotID >= 13 && slotID <= 24) {
    mod_code = KEY_LEFT_SHIFT;
    key_code = KEY_F13 + (slotID - 13);
  }
  // 25-36: Ctrl + F13-F24
  else if (slotID >= 25 && slotID <= 36) {
    mod_code = KEY_LEFT_CTRL;
    key_code = KEY_F13 + (slotID - 25);
  }
  // 37-48: Alt + F13-F24
  else if (slotID >= 37 && slotID <= 48) {
    mod_code = KEY_LEFT_ALT;
    key_code = KEY_F13 + (slotID - 37);
  } else {
    return;
  }

  if (mod_code != 0)
    Keyboard.press(mod_code);
  Keyboard.press(key_code);
  delay(random(10, 20)); // Brief hold to register spell cast
  Keyboard.release(key_code);
  if (mod_code != 0)
    Keyboard.release(mod_code);
}
