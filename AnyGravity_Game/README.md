# Tap Away Arrows — 100-Level Progressive Shape Escape Puzzle

A rich, responsive, mobile-first browser puzzle game based on the *Tap Away / Arrow Escape* genre, featuring winding orthogonal arrows with solid filled triangular arrowheads densely packed inside 36 recognizable 2D shape silhouettes from [arrowpuzzle.fun/shapes](https://www.arrowpuzzle.fun/shapes) and reference puzzle cards.

## Key Features

### 1. 100-Level Progressive Campaign & Unlocking System
- **Sequential Level Unlocking**: Level 1 is unlocked initially; player must complete each level to unlock the next level ($N \to N + 1$).
- **Locked Level Protection**: Locked levels display a 🔒 icon on the level map, and cannot be played until unlocked.
- **Completed Levels Tracker**: Real-time tracking (`Completed: X / 100 Cleared`) persisted in `localStorage` alongside `arrowCurrentLevel` and `arrowMaxUnlockedLevel`.
- **Level Map (1-100)**: Click the `🗺️` button in the header to open the interactive 100-level grid map. View completed levels with green checkmarks, current active level, and unlocked/locked status.
- **Difficulty Progression**:
  - **Levels 1 – 20 (Easy)**: 15×15 grid, gentle curves, ~30–35 arrows, fast satisfying clears.
  - **Levels 21 – 50 (Medium)**: 17×17 grid, balanced maze corridors, ~45–50 arrows.
  - **Levels 51 – 80 (Hard)**: 19×19 grid, tight turns, ~55–65 arrows, complex dependencies.
  - **Levels 81 – 100 (Expert)**: 21×21 grid, full-board labyrinth, ~68–80 arrows.

### 2. Tiered Shape Distribution (Starting Easy, Scaling to Hard)
Shapes scale progressively with level difficulty across 36 handcrafted silhouettes:
- **Easy Tier (Levels 1–20)**: Heart ❤️, Circle ⭕, Square ⏹️, Triangle 🔺, Diamond 💎, Star ⭐, Moon 🌙, Cloud ☁️.
- **Medium Tier (Levels 21–50)**: Apple 🍎, Bell 🔔, Fish 🐟, Tree 🌲, Trophy 🏆, Crown 👑, House 🏠, Sailboat ⛵, Mushroom 🍄, Plus ➕.
- **Hard Tier (Levels 51–80)**: Rocket 🚀, Cat 🐱, Butterfly 🦋, Ghost 👻, Pumpkin 🎃, Mountain ⛰️, Lighthouse 🗼, Gamepad 🎮, Shield 🛡️, Spade ♠️.
- **Expert Tier (Levels 81–100)**: Knight ♞, Elephant 🐘, Deer 🦌, Windmill 🪓, Pagoda ⛩️, Octagon 🛑, Pentagon ⬟, Lightning ⚡.

### 3. Vector-Based Grid Interpolation Engine
- **Coordinate Offset Vector Logic**: `Directions = { UP: (0, -1), DOWN: (0, 1), LEFT: (-1, 0), RIGHT: (1, 0) }` decoupling movement logic from visual representation.
- **O(1) Set-Based Collision Check (`isPathClear`)**: Grid coordinates of live arrows are indexed into a `Set` for instantaneous line-of-sight corridor clearance checks.
- **Constant Velocity Path Interpolation**: Animation duration scales linearly with cell distance traveled (`msPerCell`), providing realistic velocity with cubic-out easing.
- **Expanded Touch Hitbox**: Invisible `path.hit` layer with `stroke-width: 26px` ensuring high-precision tap and swipe gesture responsiveness.

### 4. Solid Filled Triangular Arrowheads (Reference Match)
- Bold rounded polylines terminating in **solid filled black triangular arrowheads**.
- State transitions:
  - **Idle**: Solid black `#000000` body and arrowhead.
  - **Escaping**: Vibrant electric blue `#2563eb` with luminous drop shadow.
  - **Blocked**: Warning red `#ef4444` with directional bump recoil.
  - **Hint**: Warm golden amber `#f59e0b` with pulsing glow.

### 5. Streamlined Controls
- Removed the `#` button from the bottom controls for a cleaner interface.
- Footer features the **Hint (`💡`)** button with live remaining counter.
- Top bar contains **Restart (`↻`)**, **Level Map (`🗺️`)**, and **Sound Toggle (`🔊`)**.

## Controls & How to Play
- **Tap or Swipe an Arrow**: If its line-of-sight exit path to the board edge is clear, it smoothly flies out along its polyline.
- **Blocked Arrows**: Tapping a blocked arrow triggers a bump and costs 1 of 3 hearts.
- **Level Map (`🗺️`)**: View unlocked levels and track campaign progress.
- **Hint (`💡`)**: Highlights an arrow that can escape immediately.
- **Restart (`↻`)**: Restarts the current board with full hearts.

## Running Locally
Open [index.html](file:///c:/Users/rupan/OneDrive/Desktop/arrow-escape/index.html) in any modern web browser. No build steps or external dependencies required.


## Updated character and victory presentation
- The Rescue Hero panel now plays `assets/character-unlock.webm`, a looping transparent-background (alpha) video that replaced the old 10 PNG frames. `assets/character-unlock-poster.png` is shown until it loads.
- The level progress meter has been moved directly below the header and redesigned as a compact gradient meter.
- At 100% completion only, the full-screen Congratulations video (`assets/congratulations.mp4`) plays. When it ends, the star award and Next Level button appear; selecting it starts the next level.
- Keep `assets/congratulations.mp4` alongside `index.html`, `game.js`, and `styles.css`.


## Latest UI update
- Removed the Rescue Hero card's LOCKED/Rescue Hero header and its mini percentage/cleared progress strip.
- Removed the status chip from over the character image; the transparent character is shown directly on the game page background.
- Changed the centered title to "Help him to escape".
- Added a smooth 190 ms crossfade between Rescue Hero progress frames.
- Preloaded the congratulations frames to reduce frame stalls during the full-screen sequence.
- Added a 1–3 star award after the congratulations animation. The award uses elapsed completion time and remaining hearts; Next Level appears after the star award.
- Kept the existing puzzle rules, levels, controls, and main progress HUD unchanged.


## Victory sequence update
- On reaching 100%, `assets/victory-sequence.mp4` plays full-screen as one continuous clip: boy in the cage -> padlock unlocks -> zoom-out celebration -> crossfade into the Congratulations animation. When it ends, the score card (stars, level, score, time, hearts) and Next Level button appear.
- Watermarks removed from both source clips. `assets/congratulations.mp4` is the cleaned standalone Congratulations clip (kept for reference).

## Mobile Responsiveness & Instant Victory Update
- **Instant Victory Sequence**: Moving the final remaining arrow immediately primes and triggers the rescue unlock video without hesitation or delay.
- **Ordered Video Sequence**: The character rescue/padlock unlock sequence plays first (`0s`–`7.4s`), seamlessly transitioning into the Congratulations celebration video (`7.4s`–`11.3s`), followed by the star rating award and "Next Level" progression.
- **Zero Scrollbars**: Eliminated all vertical and horizontal scrollbars across all screen sizes (mobile phones 375px/390px/412px, tablets 768px/1024px, laptops, and 1080p+ desktops) using dynamic viewport calculations (`100dvh`).
- **Mobile Video Fit**: Enabled `playsinline`, `webkit-playsinline`, and responsive `object-fit: contain` with color-matched background transitions (pure white during padlock escape, smooth gold during congratulations) so the video fits mobile screens cleanly without harsh black bars.
