# Pygame Survival Game - Quick Start Guide

## Installation
Pygame has been installed automatically. To run the game:

```powershell
cd c:\Users\Rishi\Downloads
python game_pygame.py
```

## Game Features

### Visual Interface
- Clean black interface with yellow/green text
- Stats displayed at top (Health, Hunger, Gold, Poison)
- Message log showing events and feedback
- Color-coded menus

### Core Gameplay

**Main Menu (EXPLORING state)**
- [1] Explore - triggers random events in current location
- [2] Rest - recover health, advance day
- [3] Forage - search for food
- [4] Inventory - view collected items
- [5] Craft - craft items (expand later)
- [6] Travel - move to new location
- [7] Hire NPCs - hire hunters/cooks/gatherers
- [8] Eat/Cook - consume food or cook raw meat
- [Q] Quit - exit game

### Locations
- **Forest** - Find berries, encounter wolves
- **Village** - Meet NPCs, find rescue helicopter info
- **River** - Fish, encounter bears
- **Mountain** - Caves, storms, treasure
- **Cabin** - Shelter, gold coins
- **Ruins** - Ancient artifacts, honey, herbs
- **Hermit Cave** - Meet the hermit NPC

### NPC Hiring System
- **Hunter** (10 gold/day) - Better hunting/fishing
- **Gatherer** (5 gold/day) - Resource collection
- **Scout** (8 gold/day) - Exploration
- **Cook** (7 gold/day) - Cooks raw meat, prevents poison

### Poison System
- Eating raw meat without cook: poison +15-35%
- Poison deals damage each day (~50% of counter)
- Hire a cook to convert raw_meat → cooked_meat safely
- Poison decays 10% per day naturally

### Survival Stats
- **Health** (0-100): Die if reaches 0
- **Hunger** (0-100): Starve if reaches 90+
- **Gold**: Currency for hiring NPCs
- **Poison**: Raw meat danger meter
- **Day**: Must reach day 7 in village to escape

### Win Condition
Reach day 7 in the village with the helicopter arriving = VICTORY

### Lose Conditions
- Health reaches 0 (exhaustion)
- Hunger reaches 90+ (starvation)
- Day reaches 8 (helicopter left)

## Controls

### Text Input (Name Entry)
- Type your name
- Press ENTER to start game

### Main Game
- Number keys [1-8] for menu options
- [Q] to quit
- [SPACE] to go back in menus
- Letter keys for travel ([F]orest, [V]illage, etc.)

### Screens
- **Intro**: Enter name to begin
- **Exploring**: Main game interface with all options
- **Event**: Encounter triggered with choices
- **Inventory**: View all items
- **Hiring**: Manage hired NPCs
- **Eating**: Choose food to consume
- **Travel**: Select destination
- **Game Over**: View final stats, press SPACE to restart

## Game Tips

1. **Find Gold Early**: Check cabins for 20-75 gold coins
2. **Hire a Cook ASAP**: Prevents poison from raw meat
3. **Hunters Help**: Double your hunting success rate
4. **Daily Survival**: Health/hunger decrease each day
5. **Stay Fed**: Eating food restores hunger and health
6. **Build Relationships**: Some events give reputation points
7. **Escape Plan**: Reach village by day 7 for rescue

## Files
- `game_pygame.py` - Main Pygame version (this file)
- `game.py` - Original text-based version (still available)

## Future Enhancements
- Crafting system UI
- More detailed event descriptions
- NPC leveling/experience
- Save/load functionality
- Sound effects and music
- Animated sprites
- Quest log display
- Multiple ending cinematics

Enjoy your survival adventure!
