<p align="center">
  <img src="Screenshots/DD_Logo.png" alt="Diamond Detonator Logo" width="300">
</p>

# Diamond Detonator

Diamond Detonator is a fast, strategic twist on the classic match-3. Built with Python + Pygame and a sleek gothic UI from Figma, it lets you choose match sizes (3–5) and play across multiple board layouts. Trigger chain reactions with Special Diamonds that clear all gems of their color, rack up combo scores, and chase your personal best with local high scores (SQLite). Hints, pause, and sound toggles keep it friendly for quick sessions or deep runs—how big can you detonate?

## 🎥 Demo
<p align="center">
  <a href="https://youtu.be/a-OIm_v7aKQ?si=2XCH77O_Lt7uL-ua">
    <img src="https://img.youtube.com/vi/a-OIm_v7aKQ/maxresdefault.jpg" width="500">
  </a>
</p>

## 📸 Screenshots
<p align="center">
  <img src="Screenshots/DD_SplashScreen.png" alt="Splash Screen" width="500">
</p>
<p align="center">
  <img src="Screenshots/DD_MainScreen.png" alt="Main Screen" width="500">
</p>
<p align="center">
  <img src="Screenshots/DD_GameplayScreen00.png" alt="Gameplay Screen" width="500">
</p>
<p align="center">
  <img src="Screenshots/DD_GameplayScreen01.png" alt="Gameplay Screen" width="500">
</p>
<p align="center">
  <img src="Screenshots/DD_PauseScreen.png" alt="Pause Screen" width="500">
</p>
<p align="center">
  <img src="Screenshots/DD_SettingsScreen.png" alt="Settings Screen" width="500">
</p>
<p align="center">
  <img src="Screenshots/DD_GameoverScreen.png" alt="Game Over Screen" width="500">
</p>

## ✨ Features
- Match-any size: Choose 3, 4, or 5-in-a-row for different challenge levels.
- Special Diamonds: Trigger color-clears and chain reactions for huge combo scores.
- Combo & Multiplier System: Back-to-back detonations ramp your multiplier.
- Multiple Board Layouts: Swap between curated grids for fresh pacing.
- Smart Hints: Optional move suggestions when you’re stuck.
- Power-Up Ready: Framework in place for future boosters (row/column blasts, etc.).
- Local High Scores: SQLite-backed leaderboard to track personal bests by name.
- Flexible Controls: Mouse/trackpad drag-and-swap; keyboard shortcuts for UI.
- Polished UX: Pause, restart, and toggle sound/music in-game.
- SFX & Music: Crisp audio cues for matches, detonations, and milestones.
- Responsive Performance: Smooth animations with Pygame on modest hardware.
- Clean Save/Load: Persists settings (audio, match size, layout) between sessions.

## 📦 Tech Stack
- **Language:** Python
- **Framework:** Pygame
- **Database:** SQLite (local high score storage)
- **Design:** Figma (UI/UX layout and assets)
- **Platform:** Desktop (Windows/macOS/Linux)

## 🛠 Requirements
- Python 3.9+
- Pygame 2

## 💻 Installation
On Linux or macOS, Python3 is preinstalled.  
On Windows, download the latest version of Python3 from the [official website](https://www.python.org/) and install it.  
Make sure you check the **"Add Python3 to PATH"** box at the start of the installation.

Then, install Pygame:

```bash
pip3 install pygame


## 🚀 Run the Game

You can launch Diamond Detonator in two ways:

**1️⃣ Double-click method (GUI)**
- Navigate to the game folder.
- Double-click on `diamondDetonator.py`.

**2️⃣ Terminal/Command Line method**
```bash
python3 diamondDetonator.py
