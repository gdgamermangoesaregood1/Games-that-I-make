# Game Enhancement Summary: Hiring System & Poison Mechanic

## New Features Added

### 1. **HiredNPC Class**
A new NPC class for workers that can be hired to assist with survival tasks.

**Attributes:**
- `type`: "hunter", "gatherer", "scout", or "cook"
- `name`: Randomly selected from profession-specific names
- `effectiveness`: 60-100% success rate for tasks
- `loyalty`: 0-100 (affected by treatment/results)
- `morale`: 0-100 (affects performance)
- `cost_per_day`: Daily wages (hunter=10, gatherer=5, scout=8, cook=7 gold)

### 2. **Gold & Currency System**
- `available_gold`: Track currency for hiring workers
- Gold can be found in cabins (20-50 coins initially, 30-75 more inside)
- Gold is needed to hire and maintain workers

### 3. **Hiring NPCs**
**Available Worker Types:**
- **Hunter** (10 gold/day): 
  - Increased success hunting animals
  - Can catch fish at rivers
  - Benefits from high morale
  
- **Gatherer** (5 gold/day):
  - Best for resource collection
  - Cheapest option
  
- **Scout** (8 gold/day):
  - Exploration assistance
  - Good middle ground
  
- **Cook** (7 gold/day):
  - **Special ability: Cook raw meat to cooked_meat**
  - Prevents poison buildup when preparing meals

### 4. **Poison Counter System**
**Mechanic:**
- Eating raw_meat without a cook increases poison_counter by 15-35%
- Poison damage = counter × 0.5 health loss per day
- Poison decays by 10% per day naturally
- Eating cooked_meat has no poison penalty

**Health Penalties:**
- Raw meat eaten without cook: -5 health, poison buildup
- Cooked meat: +10 health, -25 hunger, no penalty
- Fresh fish: +8 health, -20 hunger

**Status Display:**
- Poison level shown in red (⚠) when active
- Shows poison % and effective damage dealt

### 5. **New Menu Options**
Added options [8] and [9] to main game loop:
- **[8] Manage Hired NPCs**: Hire, fire, pay, view worker status
- **[9] Eat food/Cook raw meat**: Choose what to eat with cooking options

### 6. **Worker Management System**
**Features:**
- View each worker's stats (effectiveness, mood, loyalty)
- Pay daily wages (if you can't afford it, workers become angry and lose morale)
- Fire workers when needed
- Workers gain loyalty from successful hunts/tasks

### 7. **Enhanced Hunting & Fishing**
- Hunters can be hired to dramatically improve success rates
- Forest events now detect hired hunters and offer them
- River fishing improved with hunter assistance

## Game Balance Changes

**Cabin Treasure:**
- Now has 40% chance to find 30-75 gold coins
- Additional treasure location for early funding

**Food System:**
- Multiple copies of food items allowed in inventory
- Raw meat becomes strategic decision (poison vs immediate hunger relief)

**Economic Loop:**
1. Find gold in cabins/treasures
2. Hire workers with gold
3. Workers help gather more resources
4. Use resources to survive longer

## How to Use New Features

### Hiring Workers:
```
1. Collect gold (find in cabins, buried treasures)
2. Choose [8] Manage Hired NPCs
3. Select worker type to hire
4. Pay daily wages when prompted
5. Workers assist with exploration/hunting automatically
```

### Managing Raw Meat:
```
Without Cook:
- Eating raw_meat: poison +15-35%, health -5
- Poison deals ~50% damage daily until it decays

With Cook:
- Hire cook (7 gold/day)
- Use [9] Eat food, select raw_meat
- Cook will prepare it into cooked_meat automatically
- +10 health, -25 hunger, no poison
```

## Files Modified
- **game.py**: Added HiredNPC class, poison system, hiring menus, worker management

## Next Enhancements (Ready When You Are!)
- Add more NPC types (medic, blacksmith, cartographer)
- Weather-based hunting bonuses/penalties
- Worker leveling system (effectiveness increases over time)
- Different food spoilage mechanics
- Quest rewards integration with hiring system
