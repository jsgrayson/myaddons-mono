#include "HID-Project.h"
// Note: HID-Project includes Mouse support - don't include Mouse.h separately

// 8 base keys (Mac-compatible)
const KeyboardKeycode baseKeys[] = {KEY_F13, KEY_F16,  KEY_F17, KEY_F18,
                                    KEY_F19, KEY_HOME, KEY_END, KEY_DELETE};

void setup() {
  Serial.begin(250000);
  Keyboard.begin();
  Mouse.begin();
}

void fire(KeyboardKeycode k, bool s = false, bool c = false, bool a = false) {
  if (s)
    Keyboard.press(KEY_LEFT_SHIFT);
  if (c)
    Keyboard.press(KEY_LEFT_CTRL);
  if (a)
    Keyboard.press(KEY_LEFT_ALT);

  Keyboard.write(k);
  Keyboard.releaseAll();
}

// Get base key from slot byte
KeyboardKeycode getKeyFromSlot(byte slot) {
  byte idx = 0;
  bool shift = false, ctrl = false, alt = false;

  if (slot >= 0x01 && slot <= 0x08)
    idx = slot - 0x01;
  else if (slot >= 0x09 && slot <= 0x10) {
    idx = slot - 0x09;
    shift = true;
  } else if (slot >= 0x11 && slot <= 0x18) {
    idx = slot - 0x11;
    ctrl = true;
  } else if (slot >= 0x19 && slot <= 0x20) {
    idx = slot - 0x19;
    alt = true;
  } else
    return KEY_F13;

  return baseKeys[idx];
}

// Simple mouse flick (direct move, no easing)
void flickMouse(int16_t dx, int16_t dy) {
  // Direct move - simpler and more reliable than eased animation
  // HID mouse moves are limited to ±127 per call, so we may need multiple
  while (dx != 0 || dy != 0) {
    int8_t moveX = (dx > 127) ? 127 : (dx < -127) ? -127 : dx;
    int8_t moveY = (dy > 127) ? 127 : (dy < -127) ? -127 : dy;
    Mouse.move(moveX, moveY, 0);
    dx -= moveX;
    dy -= moveY;
    delay(2); // Small delay between chunks
  }
}

void loop() {
  if (Serial.available() > 0) {
    byte cmd = Serial.read();

    // === XOR HANDSHAKE (0xBD) ===
    // Python sends 0xBD (0xFF ^ 0x42), Arduino responds with 'K'
    if (cmd == 0xBD) {
      Serial.write('K');
      return;
    }

    // === GROUND TARGET FLICK (0xFD) ===
    // Packet: [0xFD] [slot] [x_hi] [x_lo] [y_hi] [y_lo]
    if (cmd == 0xFD) {
      while (Serial.available() < 5)
        ; // Wait for 5 more bytes
      byte slot = Serial.read();
      int16_t dx = (Serial.read() << 8) | Serial.read();
      int16_t dy = (Serial.read() << 8) | Serial.read();

      // 1. Flick to target
      flickMouse(dx, dy);
      delay(random(30, 50)); // Longer wait after flick

      // 2. Press spell key (activates reticle)
      byte idx = 0;
      bool s = false, c = false, a = false;
      if (slot >= 0x09 && slot <= 0x10) {
        idx = slot - 0x09;
        s = true;
      } else if (slot >= 0x11 && slot <= 0x18) {
        idx = slot - 0x11;
        c = true;
      } else if (slot >= 0x19 && slot <= 0x20) {
        idx = slot - 0x19;
        a = true;
      } else {
        idx = slot - 0x01;
      }
      fire(baseKeys[idx], s, c, a);
      delay(random(80, 120)); // Wait for reticle to appear

      // 3. Click to confirm ground target
      Mouse.click();
      delay(random(40, 60)); // Wait for click to register

      // 4. Return mouse to original position
      flickMouse(-dx, -dy);
      return;
    }

    // Flush any extra bytes for normal commands
    while (Serial.available() > 0)
      Serial.read();

    // Bar 1: Base (0x01-0x08)
    if (cmd >= 0x01 && cmd <= 0x08)
      fire(baseKeys[cmd - 0x01]);

    // Bar 2: Shift (0x09-0x10)
    else if (cmd >= 0x09 && cmd <= 0x10)
      fire(baseKeys[cmd - 0x09], true);

    // Bar 3: Ctrl (0x11-0x18)
    else if (cmd >= 0x11 && cmd <= 0x18)
      fire(baseKeys[cmd - 0x11], false, true);

    // Bar 4: Alt (0x19-0x20)
    else if (cmd >= 0x19 && cmd <= 0x20)
      fire(baseKeys[cmd - 0x19], false, false, true);

    // TAB key (0x21) - held for 50ms for reliable registration
    else if (cmd == 0x21) {
      Keyboard.press(KEY_TAB);
      delay(50);
      Keyboard.release(KEY_TAB);
    }

    // Shift+TAB key (0x22)
    else if (cmd == 0x22) {
      Keyboard.press(KEY_LEFT_SHIFT);
      Keyboard.press(KEY_TAB);
      delay(50);
      Keyboard.releaseAll();
    }
  }
}
