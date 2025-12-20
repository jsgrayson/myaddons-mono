// Master Chord Mapping - SkillWeaver Midnight V2.11
// No longer limited to 4-button model.

#ifndef KEYBOARD_MAP_H
#define KEYBOARD_MAP_H

struct Chord {
  uint8_t modifier; // Shift, Ctrl, Alt, or None
  uint8_t key;      // Primary Scan Code
};

// Modifier Constants
#define MOD_NONE 0x00
#define MOD_CTRL 0x80
#define MOD_SHIFT 0x81
#define MOD_ALT 0x82
#define MOD_GUI 0x83

// Mapping Action IDs to specific hardware chords
const Chord ActionRegistry[] = {
    {MOD_NONE, 0x00},  // [0] NULL
    {MOD_SHIFT, 0x04}, // [1] Spell_ID_343527 (Execution Sentence) - 'A'
    {MOD_CTRL, 0x05},  // [2] Spell_ID_255937 (Wake of Ashes) - 'B'
    {MOD_ALT, 0x06},   // [3] Spell_ID_383328 (Final Verdict) - 'C'
    {MOD_NONE, 0x2C},  // [4] SPACE (JUMP/CANCEL)
    {MOD_NONE, '1'},   // [5] Standard Rotation Key 1
    {MOD_NONE, '2'},   // [6] Standard Rotation Key 2
    {MOD_NONE, '3'},   // [7] Standard Rotation Key 3
    {MOD_NONE, '4'},   // [8] Standard Rotation Key 4
    {MOD_NONE, '5'},   // [9] Standard Rotation Key 5
                       // ... Capacity for 255+ unique chords
};

#endif
