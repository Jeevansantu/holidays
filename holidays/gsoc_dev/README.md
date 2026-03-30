# GSoC 2026 Prototype: Hindu Lunisolar Holiday Engine

### Target Library: `python-holidays`

This repository contains the **Technical Proof of Concept (PoC)** for the proposed 350-hour Google Summer of Code project to implement a high-precision Hindu calendar engine for the `python-holidays` library.

## 🚀 Overview

Currently, many Indian holidays in the library are either missing or use static hardcoded arrays. This prototype demonstrates a dynamic **Astronomical Solver** that calculates holiday dates for any year between 1950 and 2100 using NASA-grade planetary data.

## 🛠️ Technical Implementation

- **Core Engine:** Built using `PyEphem` (C-extensions) to calculate Ecliptic Longitude for the Sun and Moon.
- **Tithi Logic:** Implemented a `(Moon_Lon - Sun_Lon) % 360 / 12` algorithm to determine the 30 lunar phases (Tithis).
- **Solver:** Utilizes a **Coarse-to-Fine Search** (Day-sweep followed by Binary Search) to locate exact Tithi boundaries with sub-second precision.

## 🔍 Critical Challenges Identified (The "350-Hour" Justification)

During the development of this prototype, three major astronomical edge cases were identified and resolved, proving the complexity of the full project:

1. **Phase-Aliasing (The Oct 17 vs Oct 31 Trap):**
   - _Problem:_ A naive search can snap to the wrong lunar month (Ashwin vs Kartik).
   - _Solution:_ Implemented a Solar-Month Anchored search window to ensure the engine targets the correct Amavasya for Diwali.

2. **UTC-IST Midnight Crossover:**
   - _Problem:_ Astronomical events in UTC often cross the midnight boundary in Indian Standard Time (IST), causing a +1 day shift (e.g., Oct 31 vs Nov 1).
   - _Solution:_ Developed a temporal offset layer to align calculations with Indian Civil Days.

3. **Pradosh Kaal (Observation Rules):**
   - _Problem:_ Hindu holidays are determined by the Tithi active at **Sunset**, not midnight.
   - _Solution:_ Integrated a Sunset trigger to handle the 2025 Diwali shift (Oct 21), demonstrating localized observation rules.

## 🧪 How to Run

```powershell
# Install dependencies
pip install ephem

# Run the validation suite
python gsoc_dev/test_engine.py
```
