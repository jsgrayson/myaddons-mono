// --------------------------------------------------------------------------------
// ARDUINO SKILLWEAVER "DIGITAL TWIN" FIRMWARE (DECEMBER 2025 META)
// --------------------------------------------------------------------------------
#include <Keyboard.h>
#include <Mouse.h>
#include <math.h>

// --- CONFIGURATION ---
const int BAUD_RATE = 250000;  // High-Density Proc Handling (Dec 2025 Standard)
const int KILL_SWITCH_PIN = 2; // Physical Interrupt Toggle

// --- STATE MACHINE ---
unsigned long channelTimer = 0;
int lastPulsedSlot = -1;
bool isKillSwitchActive = false;

void setup() {
  Serial.begin(BAUD_RATE);
  pinMode(KILL_SWITCH_PIN, INPUT_PULLUP);
  Keyboard.begin();
  Mouse.begin();

  // Random Seed initialization for Biometrics
  randomSeed(analogRead(0));
}

void loop() {
  // 1. "VANISH PROTOCOL" (Kill Switch)
  if (digitalRead(KILL_SWITCH_PIN) == LOW) {
    if (!isKillSwitchActive) {
      // Falling Edge: Execute Vanish
      isKillSwitchActive = true;
      lastPulsedSlot = -1;
      Keyboard.releaseAll();

      // Panic Cancel Pulse (Vanish)
      Keyboard.press(KEY_ESC);
      delay(random(25, 45)); // Non-deterministic cancel
      Keyboard.release(KEY_ESC);
    }
    return; // Halt all processing while switch is OFF
  } else {
    isKillSwitchActive = false; // Reset state when toggle is ON
  }

  // 2. Data Bus
  if (Serial.available() > 0) {
    int incomingByte = Serial.read();

    // 3. Channel Guard (Hardware Level) - Protects Fists of Fury, Disintegrate,
    // Hymn
    if (millis() < channelTimer) {
      return;
    }

    executeCommand(incomingByte);
  }
}

// --- BIOMETRIC ENGINE (Humanization) ---

void humanizedMove(char keyChar, int durationBase) {
  // Biometric Drift: Gaussian-style randomization
  // Simulates "Thumb Weight" and "Decision Latency"

  // 1. Decision Latency (The "Thought" Gap)
  delay(random(8, 22));

  Keyboard.press(keyChar);

  // 2. Drift Variance (Wobble)
  // Calculates 'Effective Press Time'
  int actualDuration = durationBase + random(-15, 35);
  delay(actualDuration);

  Keyboard.release(keyChar);

  // 3. Stabilization Micro-Adjustment (The "Correction")
  // Occasional micro-pause to simulate grip adjustment
  if (random(0, 100) > 85) {
    delay(random(5, 15));
  }
}

void executeBluff(uint8_t key) {
  // Variable Cancellation (The "Double Bait")
  // Anxiety Engine Implementation

  // Cast...
  Keyboard.press(key);
  delay(random(40, 80)); // Server Register
  Keyboard.release(key);

  // Wait... (The Bait)
  delay(random(280, 550));

  // Cancel
  Keyboard.press(KEY_ESC);
  delay(random(20, 50));
  Keyboard.release(KEY_ESC);
}

void executeCommand(int cmd) {
  // Sine-Wave Jitter (Anti-Heuristic) to modulate press durations
  int jitter = 15 + (5 * sin(millis() / 150.0));

  // Combo Guard (Prevent machine-gunning same key unless allowed)
  // Exceptions: Movement, Bluffing, Jitter, Mouse
  if (cmd == lastPulsedSlot && cmd != 'M' && cmd != 'Q' && cmd != 'W' &&
      cmd != 'E' && cmd != 'J') {
    return;
  }

  switch (cmd) {
  // --- ROTATION SLOTS (biometrically smoothed by pressKey) ---
  case '1':
    pressKey(KEY_F13, jitter);
    break;
  case '2':
    pressKey(KEY_F14, jitter);
    break;
  case '3':
    pressKey(KEY_F15, jitter);
    break;
  case '4':
    pressKey(KEY_F16, jitter);
    break;
  case '5':
    pressKey(KEY_F17, jitter);
    break;
  case '6':
    pressKey(KEY_F18, jitter);
    break;
  case '7':
    pressKey(KEY_F19, jitter);
    break;
  case '8':
    pressKey(KEY_F20, jitter);
    break;

  // --- UTILITY ---
  case 'A':
    pressKey(KEY_F21, jitter);
    break; // Interrupts
  case 'B':
    pressKey(KEY_F22, jitter);
    break; // Defensives

  // --- MOVEMENT (Biometric) ---
  case 'M':
    humanizedMove('w', 100);
    break; // Forward Drift / Micro-Adjust

  // --- BLUFFING (Anxiety Engine) ---
  case 'Q':
    executeBluff(KEY_F13);
    break; // Bluff Slot 1 (Flash Heal/Rake)
  case 'W':
    executeBluff(KEY_F16);
    break; // Bluff Slot 4 (Chaos Bolt)
  case 'E':
    executeBluff(KEY_F18);
    break; // Bluff Slot 6 (Cyclone)

  // --- SPECIAL MECHANICS ---
  case 'C': // Channel Lock (3.2s) - Fists of Fury
    pressKey(KEY_F16, jitter);
    channelTimer = millis() + 3200;
    break;

  case 'H': // Empowered Hold (EVOKER) - Fire Breath
    Keyboard.press(KEY_F15);
    delay(1050 + random(0, 100)); // Tier 1 + Variance
    Keyboard.release(KEY_F15);
    channelTimer = millis() + 3500;
    break;

  case 'D': // DIAGNOSTIC MODE
    // Sequential Pulse to verify wiring
    for (int i = 0; i < 4; i++) {
      pressKey(KEY_F13 + i, 50);
      delay(100);
    }
    break;

  case 'J': // Idle Jitter
    Mouse.move(1, 0);
    delay(2);
    Mouse.move(-1, 0);
    break;
  }

  // Update History unless it's a utility command that allows repetition
  if (cmd != 'J' && cmd != 'M') {
    lastPulsedSlot = cmd;
  }
}

void pressKey(uint8_t k, int meanDuration) {
  // Basic humanized press wrapper
  Keyboard.press(k);
  delay(meanDuration + random(0, 15));
  Keyboard.release(k);
}
