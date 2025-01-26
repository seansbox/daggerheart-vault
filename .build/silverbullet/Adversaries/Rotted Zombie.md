---
displayName: "Rotted Zombie"
description: "A decaying corpse ambling toward its prey."
tier: 1
type: Standard
hp: 1
stress: 1
attack:
   name: Bite
   bonus: -3
   distance: Melee
   damage: 4
   effect: phy
thresholds:
   difficulty: 8
   major: 
   severe: 
tags: adversary
---
# Rotted Zombie (Tier 1 Standard)
_A decaying corpse ambling toward its prey._

- **Motives & Tactics** _Hunger, Maul, Surround, Eat Flesh_
- **Difficulty** _8_ | **Attack Modifier** _-3_ | **Bite** _Melee 4 phy_
- **Major** _≥_ | **Severe** _≥_

1. **HP** 1
   **Stress** 1
2. **HP** 1
   **Stress** 1
3. **HP** 1
   **Stress** 1

## Minion (4) - Passive
This adversary is defeated if they take any damage. For every 4 damage a PC deals to this adversary, defeat an additional minion in the attack’s range. _“You hack through multiple bodies in the tight press of the undead.”_

## Group Attack - Action (2)
Choose a target and activate all Rotten Zombies within Close range of them. Those minions move into melee with the target and make one shared attack roll. On a success, they deal 4 phy damage each. Combine this damage together. _“Though zombies move forward mindlessly, seeming to attack in a coordinated effort of instinct.”_
