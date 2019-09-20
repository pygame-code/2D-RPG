# 2D-RPG
Code for a first 2D Adventure RPG. Uses the pygame module.

## Classes
1.) Warrior  - Tank specialist and melee combat.

               Health = 100, Stamina = 30
               
2.) Rogue    - Stealth specialist and melee combat.

               Health = 80, Stamina = 50
               
3.) Predator - Ranged bow specialist. Can tame beasts. 

               Health = 85, Stamina = 40
               
4.) Mystic   - Elemental damage specialist. Casts spells dealing instant damage. 

               Health = 70, Mana = 90
               
5.) Cultist  - Dark magic damage specialist. Casts damage over time spells.

               Health = 70, Mana = 90
               
6.) Priest   - Divine magic damage and healing specialist.

               Health = 65, Mana = 100

## Skills

1.) Blacksmithing

2.) Armoring

3.) Smelting

4.) Mining

5.) Gardening

6.) Herb Gathering

6.) Alchemy

7.) Fishing

8.) Enchanting

9.) Fabric Weaving

10.) Cooking

## Abilities

### All-Class Abilities:

1.) Health Regeneration (passive) - All classes regenerate 1% of their health every 5 seconds while not in combat.

2.) Teleport - Can teleport to the town that the player has designated as their home. Can only use this once every hour.

3.) Stamina/Mana Regeneration (passive) - Stamina (Mana) regenerates at a rate of 4% (1%) every second. 

### Class-Specific Abilities:

#### Warrior:

1.) Base Attack - Default attack dealing normal melee damage.

2.) Harden (passive) - Every 4th Base Attack received adds a stack that increases armour. 5 stacks max. Stacks disappear after leaving combat.

#### Rogue:

1.) Base Attack - Default attack dealing normal melee damage.

2.) Puncture (passive) - Chance of Base Attack dealing additional damage over time for the next 2 moves totaling 100% Base Attack damage. Effect does not stack. Uses 50% of max stamina.

#### Predator:

1.) Base Attack - Default attack dealing normal arrow damage.

2.) Kick - Deals 25% Base Attack damage and sends the enemy stumbling backward. The enemy cannot melee attack you for their next move. Uses 40% max stamina.

#### Mystic:

1.) Base Attack - Default attack dealing elemental magic damage of the Mystic's current type.

2.) Elemental Call - Switches elemental damage type used by all abilities. Choose between fire, water, earth, and wind magic. After switching damage types, the next Base Attack deals 50% increased damage. Uses 20% of max mana.

#### Cultist:

1.) Base Attack - Default attack dealing dark magic damage.

2.) Curse - Deals 20% of Base Attack damage every move for 5 moves. Uses 20% of max mana. Once the last move is over, it deals an additional 50% of Base Attack damage.

#### Priest:

1.) Base Attack - Default attack dealing divine magic damage.

2.) Flash of Light - When used on player or ally, heals for 25% of Priest's max health. When used on enemy, deals 25% of Priest's current health. Uses 30% of max mana.
