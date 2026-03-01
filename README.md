# AETHERFALL: The Shadow King

An AI-driven, modular Python text-based RPG with NLP intent prediction, finite state machine gameplay, and strategic narrative choices.

## Quick Start

```bash
# 1. Install dependencies (Python 3.8+)
pip install -r requirements.txt

# 2. Run the game
python main.py

# 3. Follow the prompts
```

## Game Overview

**AETHERFALL: The Shadow King** is a dark fantasy adventure where you must defeat an ancient evil through strategic planning and proper execution of a sacred ritual. Simple combat won't save the realm—only a perfectly executed ritual can seal the Shadow King's fate forever.

### Core Loop

1. **Explore** 10 interconnected locations
2. **Collect** 6 items with different values and purposes
3. **Meet NPCs** who teach you crucial abilities
4. **Prepare** for the final confrontation
5. **Execute the Ritual** perfectly to achieve true victory

## How to Win

### Winning Conditions (The True Ending)

To defeat the Shadow King and achieve the **TRUE ENDING**, you must:

1. **Defeat General Kael** at the Ancient Bridge
   - Requirement: Sword + HP ≥ 60
   - **Combat System**: Turn-based combat where BOTH you and Kael deal damage each turn
   - **Kael Damage**: 8-18 damage per turn (significant threat!)
   - **Your Damage**: 10-15 with normal Sword, 15-25 with Blessed Sword
   - Victory: Bridge access to Mountain Peak unlocked

2. **Bless the Sword** at the River
   - At River location
   - command: `bless sword`
   - Requires: Sword + Magic Amulet

3. **Learn the True Strike** from Captain Ardyn
   - At Castle Gate
   - Command: `true strike` or `learn strike`
   - Requires: Fully trusted (4+ trust with guard)

4. **Get the Oath Token** from Captain Ardyn
   - At Castle Gate
   - Requires: Fully trusted (4+ trust with guard)

5. **Reach Mountain Peak** (after defeating Kael)
   - Confront the Shadow King

6. **Execute the Ritual Perfectly** (Three mandatory steps):

   **Step 1: Remove the Crown**
   - Command: `remove crown`
   - If wearing Golden Crown, take it off
   - Corruption prevents ritual success

   **Step 2: Activate the Amulet**
   - Command: `activate amulet`
   - Magic Amulet must be in inventory
   - Channels divine power

   **Step 3: Wait for Shadows to Separate**
   - Command: `wait` or `shadow` or `prepare`
   - King's darkness must split from the man

   **Step 4: True Strike**
   - Command: `true strike` or `final strike`
   - Requires: Blessed Sword + True Strike knowledge
   - Defeats the Shadow King permanently

### Building Guard Trust (for Oath Token & True Strike)

Captain Ardyn at Castle Gate trusts actions over words. Perform 4 of these 5 actions:

1. **Solve Wizard Riddle** - Wizard Tower: `solve riddle`
2. **Bless the Sword** - River: `bless sword`
3. **Donate to Village** - Castle Gate: `donate` (10 points)
4. **Refuse the Crown** - Don't wear the Golden Crown
5. **Repair Ancient Bridge** - Ancient Bridge: `repair bridge`

Each action can only be done once. Gain +1 trust per action (max 5). At 4+ trust, guard gives Oath Token and teaches True Strike.

**✅ TRUST CLARIFICATION: You do NOT need 5/5 trust. 4/5 is sufficient to gain Oath Token and True Strike. The 5th action is optional.**

**⚠️ CRITICAL: Oath Token is REQUIRED for the ritual to succeed. Without it, you will trigger the Dark Ending even if all other conditions are met!**

## Shadow King Two-Phase System

The final boss battle has **TWO distinct phases**:

### Phase 1: Combat
- Reduce Shadow King's HP to 0
- King deals **10-20 damage per turn** in combat
- Use Blessed Sword for maximum damage (15-25 vs 10-15)
- This phase tests your combat preparation

### Phase 2: Ritual
- Triggered automatically when King's HP reaches 0
- **Combat no longer works** - you MUST follow the 4-step ritual
- If you attack during this phase: **King deals 30 damage as punishment**
- Ritual requires:
  - Oath Token (MANDATORY or Dark Ending)
  - Blessed Sword
  - Magic Amulet
  - NOT wearing Crown
  - True Strike knowledge
  - Bridge repaired
  - Kael defeated

**💡 Strategy**: Combat gets you to the ritual phase, but only the ritual can achieve true victory.

## Game Map

**10 Locations** in the Enchanted Forest realm:

### Safe Zones (No combat)

- **Enchanted Forest** 🌲 (START) - Contains: Wood (5 pts)
- **Village** 🏘️ - Safe rest area, can heal HP (30 HP once per game)
- **River** 💧 - Sacred waters, ritual blessings work here
- **Hidden Cave** 🕳️ - Contains: Torch (10 pts)

### Medium Danger

- **Castle Gate** 🏰 - Captain Ardyn (guard NPC), Contains: Rusty Key (15 pts)
- **Royal Courtyard** 👑 - Contains: Golden Crown (25 pts) ⚠️ corrupts stats
- **Wizard Tower** 🧙 - Contains: Magic Amulet (30 pts) ⭐ CRITICAL

### High Danger

- **Dark Dungeon** 🖤 - Contains: Sword (20 pts) - Takes 15 damage entering without Sword!
- **Ancient Bridge** 🌉 - General Kael (BOSS) - Must defeat to progress
- **Mountain Peak** 🏔️ - Shadow King (FINAL BOSS) - Can only reach after defeating Kael

### Movement Directions

```
        Enchanted Forest (START)
             ↓ (N/S)
          Village ←→ River → Hidden Cave → Castle Gate → Royal Courtyard → Wizard Tower
                                                            ↓
                                                       Dark Dungeon

          (From River: N → Ancient Bridge → N → Mountain Peak)
```

## Available Commands

```
MOVEMENT:
  move north/south/east/west/up/down

EXPLORATION:
  look              - Examine current location
  take [item]       - Pick up an item
  inventory         - Check your inventory

INTERACTION:
  talk [npc]        - Talk to an NPC
  attack [target]   - Attack an enemy
  use [item]        - Use an item

SPECIAL ACTIONS:
  bless sword       - Bless sword at River (requires Sword + Amulet)
  donate            - Donate points to village (at Castle Gate, costs 10 pts)
  solve riddle      - Solve puzzle (at Wizard Tower)
  repair bridge     - Fix bridge (at Ancient Bridge)

RITUAL COMMANDS (at Mountain Peak):
  remove crown      - Remove crown
  activate amulet   - Activate amulet
  wait / prepare    - Wait for ritual moment
  true strike       - Execute final blow

GAME:
  help              - Show all commands
  quit/exit         - Quit game
```

## Inventory System

Items can be **worn** (some give bonuses/penalties):

- **Golden Crown**: +5 damage BUT +10 corruption (darkens your soul)
- **Sword**: Essential for dungeon and boss fights
- **Magic Amulet**: Required for blessing rituals

Commands for items:

- `take [item]` - Pick up
- `use [item]` - Use or consume
- `wear [item]` / `remove [item]` - Equip worn items

## Health & Healing

- **Starting HP**: 100
- **Max HP**: 100

When to heal:

- Health < 40: **⚠️ WARNING** - You're vulnerable!
- Health < 20: **🚨 CRITICAL** - Danger of death!

Healing methods:

1. **Village Rest** - First visit to Village: +30 HP (one-time only)
   - **Important**: Only works if HP < 100
   - If at full health: "You are already at full strength. Rest is unnecessary."
   - Prevents wasting your only rest opportunity
2. **Healing Potions** - If found during gameplay: +40 HP (single-use items)
   - Cannot exceed max HP (100)

## Alignment & Morality

Your actions shape your soul:

- **Pure Heart** (Righteousness > Corruption by 20+): Best ending, pure victory
- **Neutral** (Within 5 of balanced): Middle ground ending
- **Corrupted** (Corruption > Righteousness by 20+): Dark ending possible

**Avatar Corruption Effects:**

- Wearing Golden Crown: +10 corruption points
- Removing Crown: +5 righteousness points
- Helping NPCs: +righteousness bonuses

## Scoring & Points

Total possible points: **105 points** (collectible items)

Item point values:

- Wood: 5 pts
- Torch: 10 pts
- Rusty Key: 15 pts
- Sword: 20 pts
- Golden Crown: 25 pts
- Magic Amulet: 30 pts

Bonus Points:

- Solving puzzles: Hidden secret points
- Completing quests: Bonus rewards

## Game Difficulty Progression

| Location         | Difficulty  | Enemies      | Why Go                          |
| ---------------- | ----------- | ------------ | ------------------------------- |
| Enchanted Forest | ★ Easy      | None         | Start, get Wood                 |
| Village          | ★ Easy      | None         | Heal, rest                      |
| Hidden Cave      | ★ Easy      | None         | Get Torch                       |
| Castle Gate      | ★★ Calm     | Guard NPC    | Meet Ardyn, get Key             |
| River            | ★ Easy      | None         | Bless sword, rituals            |
| Royal Courtyard  | ★★ Calm     | None         | Get Crown (risky!)              |
| Wizard Tower     | ★★ Calm     | None         | Get Amulet (essential!)         |
| Dark Dungeon     | ★★★ Danger  | Traps        | Get Sword, 15 dmg if unequipped |
| Ancient Bridge   | ★★★★ Boss   | General Kael | MUST WIN to progress            |
| Mountain Peak    | ★★★★★ Final | Shadow King  | Final battle & ritual           |

## NLP & Intent System

The game uses PyTorch neural network with NLTK processing:

- **7 Action Intents**: move, take, look, inventory, help, talk, attack, use
- **Confidence Threshold**: 75% certainty required
- **Smart Parsing**: Natural language commands understood
  - "go north" = move north
  - "pick up sword" = take sword
  - "what's in my bag" = inventory
  - "talk to guard" = talk

## Technical Architecture

```
aetherfall/
├── main.py                 # Entry point, game UI
├── requirements.txt        # Dependencies
├── game/
│   ├── engine.py          # FSM & intent handling
│   ├── world.py           # Central game state
│   ├── health.py          # HP management & healing
│   ├── inventory.py       # Item management
│   ├── morality.py        # Alignment tracking
│   ├── guard.py           # NPC trust system
│   ├── general_kael.py    # Kael boss fight
│   ├── ritual.py          # Ritual system
│   ├── scoring.py         # Points system
│   ├── puzzles.py         # World puzzles
│   └── map_graph.py       # Location graph
├── utils/
│   └── config.py          # Game balance constants
├── nlp/
│   ├── predictor.py       # Intent prediction
│   ├── training_data.py   # Training dataset
│   └── model.pth          # Trained PyTorch model
└── data/
    └── [placeholder for saves]
```

## Key Design Principles

### Modular Architecture

- Each system is independent (Health, Inventory, Morality, etc.)
- Systems communicate through World coordinator
- Easy to extend without breaking other systems

### No Farming Exploits

- Guard trust: 5 specific one-time actions (can't repeat)
- Dungeon damage: One-time penalty per playthrough
- Village healing: Single use then locked out
- All major resources non-renewable

### Mandatory Ritual

- Combat alone CANNOT defeat Shadow King
- Ritual requires 4-step sequence in correct order
- Each step has specific requirements
- Perfect execution required for true victory

### Difficulty Curve

- Forest → Village → Cave: Learning curve
- Castle Area: Medium difficulty
- Dungeon: First real danger
- Bridge: Boss encounter gating
- Peak: Final test of preparation

## Winning Strategy (Optimal Path)

### Phase 1: Early Exploration (Goal: Survive)

1. Start at Enchanted Forest, take Wood
2. Go north to Village, rest (+30 HP)
3. Take torch from Hidden Cave
4. Head to Castle Gate, meet Captain Ardyn

### Phase 2: Item Collection (Goal: Prepare for bosses)

1. Collect Rusty Key from Castle Gate
2. Get Magic Amulet from Wizard Tower (PRIORITY!)
3. Get Golden Crown from Royal Courtyard (risky but 25 pts)
4. Get Sword from Dark Dungeon (be ready for 15 dmg!)

### Phase 3: Trust Building (Goal: Get Oath Token & True Strike)

1. Solve Wizard riddle (+1 trust)
2. Bless Sword at River (+1 trust)
3. Donate 10 points at Village (+1 trust)
4. Repair bridge at Ancient Bridge (+1 trust)
5. → Now at 4+ trust, get Oath Token + True Strike

### Phase 4: Boss Preparation (Goal: Reach Peak)

1. Ensure Blessed Sword ✓
2. Ensure Oath Token ✓
3. Ensure Magic Amulet ✓
4. Ensure HP ≥ 60 ✓ (rest at Village once more if needed)
5. Remove Crown from inventory (don't wear it!)

### Phase 5: Ancient Bridge (Goal: Defeat Kael)

1. Visit Ancient Bridge, "attack kael"
2. Should pass: Has Sword, HP ≥ 60
3. Bridge clears, can reach Mountain Peak

### Phase 6: Final Battle (Goal: Execute Perfect Ritual)

1. Move to Mountain Peak
2. Follow 4-step ritual:
   - `remove crown`
   - `activate amulet`
   - `wait`
   - `true strike`
3. **✨ TRUE ENDING ACHIEVED ✨**

## Cheats & Hidden Features

The game intentionally has **no cheat codes** to preserve challenge. Exploits are prevented by:

- One-time dungeon damage flag
- Trust action restrictions with persistence
- Mandatory ritual sequence (cannot skip steps)
- State locking during boss battles

## Troubleshooting

**"General Kael won't let me pass"**

- Ensure you have Sword in inventory
- Ensure HP ≥ 60 (heal at Village if needed)
- Attack with `attack` command
- **Important**: Combat is turn-based; Kael will deal 8-18 damage per turn!
- Consider having Blessed Sword for higher damage (15-25 vs 10-15)

**"I repaired the bridge but still can't move north"**

- Bridge repair has TWO separate aspects:
  1. **Structural repair** (using Wood) - Increases guard trust, required for ritual
  2. **Kael's guard duty** - Blocks physical passage
- Repairing structure does NOT unlock movement
- You must DEFEAT Kael in combat to cross the bridge
- Both are required: Repair increases trust, defeating Kael unlocks path

**"I can't bless the sword"**

- Must be at **River** location
- Must have **Sword** in inventory
- Must have **Magic Amulet** in inventory
- Command: `bless sword`

**"Guard won't give Oath Token"**

- Trust level must be ≥ 4
- Can only get trust from 5 specific actions
- Each action only counts once
- Keep talking to verify your trust level

**"Ritual failed even though I followed steps"**

- **Oath Token is MANDATORY** - Without it, ritual triggers Dark Ending
- Must have Blessed Sword (not just regular Sword)
- Must have Magic Amulet in inventory
- Must NOT be wearing Golden Crown
- Bridge must be repaired
- Kael must be defeated
- Must have learned True Strike from guard
- Must complete ALL 4 ritual steps in order

**"Village won't let me rest"**

- If you have full HP (100/100), rest is blocked to prevent waste
- Message: "You are already at full strength. Rest is unnecessary."
- Rest is single-use per game - save it for when you need it!

**"Ritual won't work"**

- Must be at **Mountain Peak**
- Must follow steps in order:
  1. Remove Crown (not wearing it)
  2. Activate Amulet (have it)
  3. Wait (let shadows split)
  4. True Strike (have Blessed Sword + knowledge)
- Don't skip or repeat steps!

**"I died and want to retry"**

- Run `python main.py` again
- Fresh playthrough with new Save
- Plan better next time!

## Version History

- **v2.2** (Mar 2026) - Documentation polish: Shadow King two-phase system clarification, trust threshold explanation (4/5 sufficient), route naming fix, complete consistency across all docs
- **v2.1** (Mar 2026) - Kael damage fix (8-18), ritual failure improvements, bridge logic clarification, healing waste prevention
- **v2.0** (Feb 2026) - Architecture fix, balance fixes, mandatory ritual
- **v1.0** (Initial) - Core game with optional endings

## Credits

Built with:

- Python 3.8+
- PyTorch for NLP neural networks
- NLTK for tokenization
- Colorama for cross-platform terminal colors

## License

Educational project demonstrating:

- Text-based game design
- NLP intent prediction
- Finite State Machines
- Modular Python architecture
- Game balance and difficulty curves

---

## Have Fun and Good Luck!

May the light guide your journey through the shadow. Remember: **Only the ritual can save us all.**

🏆 **Can you defeat the Shadow King?** 🏆
