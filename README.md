GSoC 2026 Prototype: Hindu Lunisolar Holiday Engine
Target Library: python-holidays
This repository contains a technical proof-of-concept for a dynamic astronomical engine designed to calculate Hindu festival dates. Unlike static date arrays, this engine utilizes planetary ephemerides to ensure accuracy across a 150-year range (1950–2100).

Technical Overview
The prototype replaces Gregorian-based approximations with a localized Vedic observation model.

Core Features
Astronomical Solver: Integrated PyEphem to calculate the ecliptic longitude of the Sun and Moon to determine Tithi boundaries (12° lunar separation).

Search Optimization: Implemented a two-stage "Coarse-to-Fine" search (Day-sweep followed by Binary Search) to ensure the solver converges on the correct lunar month.

Temporal Offsets: Developed a coordinate-aware layer to handle UTC-to-IST midnight crossovers, preventing the common +1 day calculation error.

Key Challenges Resolved
During development, the following astronomical edge cases were identified and addressed:

1. Phase-Aliasing (October 2024 Case)
Standard numerical solvers often snap to the nearest lunar phase. This prototype implements a solar-month anchor to distinguish between Ashwin and Kartik Amavasya, correctly identifying October 31 as the date for Diwali 2024.

2. Pradosh Kaal Logic (2025 Shift)
Hindu festivals are often determined by the Tithi active at sunset rather than midnight. The engine includes a "Sunset Trigger" to handle localized observation rules, which is critical for the 2025 holiday cycle.

3. Library Compatibility
The implementation resolves type-compatibility conflicts between legacy C-extensions (PyEphem) and modern Python datetime objects, ensuring a stable dependency tree for the python-holidays library.

Directory Structure
gsoc_dev/hindu_engine_v1.py: The core astronomical solver and observation logic.

gsoc_dev/test_engine.py: Automated validation suite using Python's unittest framework.

How to Run
PowerShell
# Install required astronomical library
pip install ephem

# Execute the validation suite
python gsoc_dev/test_engine.py
