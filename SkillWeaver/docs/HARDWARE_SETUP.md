# Arduino Kill Switch Wiring Guide

To enable the **Vanish Protocol** (Instant Cutoff), you must wire a physical toggle switch or button to the Arduino.

## Circuit Diagram

1.  **Pin 2:** Connect one leg of your Switch/Button here.
2.  **GND (Ground):** Connect the other leg of your Switch/Button here.

## Logic (Active Low)
The firmware uses `INPUT_PULLUP`.
*   **Switch OPEN (OFF):** Pin 2 reads HIGH (Internal 5V). **Bot is ACTIVE.**
*   **Switch CLOSED (ON):** Pin 2 connects to GND (Reads LOW). **Bot is KILLED.**

> **WARNING:** Ensure your switch is easily accessible. This is your hardware-level safety beat.
