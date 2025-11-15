import random
import os

class NPC:
    """Dynamic NPC with personality and backstory"""
    def __init__(self, npc_type):
        self.type = npc_type
        self.names = {
            "hermit": ["Marcus", "Jacob", "Solomon", "Thomas"],
            "villager": ["Emma", "James", "Sarah", "David", "Alice"],
            "merchant": ["Zeke", "Petra", "Silas", "Iris"]
        }
        self.name = random.choice(self.names.get(npc_type, ["Stranger"]))
        self.personality = random.choice(["kind", "gruff", "mysterious", "cheerful"])
        self.backstory = self.generate_backstory()
        self.likes = random.choice([["honey", "fresh_fish"], ["berries", "herbs"], ["tools", "crafted_items"]])
        
    def generate_backstory(self):
        backstories = {
            "hermit": [
                f"{self.name} retreated here 20 years ago seeking peace.",
                f"{self.name} is hiding from a painful past in the city.",
                f"{self.name} came here searching for enlightenment and stayed.",
            ],
            "villager": [
                f"{self.name} was born and raised in this village.",
                f"{self.name} found refuge here after escaping hardship.",
                f"{self.name} leads the village with wisdom and care.",
            ],
            "merchant": [
                f"{self.name} travels between settlements trading goods.",
                f"{self.name} knows secrets from everywhere they've been.",
                f"{self.name} seeks rare items to expand their collection.",
            ]
        }
        return random.choice(backstories.get(self.type, ["Their past is a mystery."]))
        
    def greet(self):
        greetings = {
            "kind": f"{self.name} smiles warmly at you.",
            "gruff": f"{self.name} grunts in acknowledgment.",
            "mysterious": f"{self.name} studies you with an unreadable expression.",
            "cheerful": f"{self.name} greets you enthusiastically!"
        }
        return greetings.get(self.personality, f"{self.name} nods at you.")

class HiredNPC:
    """Hired NPC worker with skills and effectiveness"""
    def __init__(self, npc_type, name):
        self.type = npc_type  # "hunter", "gatherer", "scout", "cook"
        self.name = name
        self.effectiveness = random.randint(60, 100)  # 60-100% success rate
        self.loyalty = 50  # Starts neutral, affected by treatment
        self.cost_per_day = {"hunter": 10, "gatherer": 5, "scout": 8, "cook": 7}.get(npc_type, 5)
        self.morale = 100
        
    def get_description(self):
        mood = "happy" if self.morale >= 70 else "neutral" if self.morale >= 40 else "unhappy"
        return f"{self.name} ({self.type.title()}) - Effectiveness: {self.effectiveness}% | Mood: {mood} | Loyalty: {self.loyalty}"

class Quest:
    """Quest system with tracking and rewards"""
    def __init__(self, quest_id, title, description, reward_items, reward_health=0):
        self.id = quest_id
        self.title = title
        self.description = description
        self.reward_items = reward_items
        self.reward_health = reward_health
        self.completed = False
        self.progress = 0
        
    def check_progress(self, game_state):
        """Check if quest conditions are met"""
        pass

class Game:
    def __init__(self):
        self.player_name = ""
        self.health = 100
        self.hunger = 50
        self.inventory = []
        self.location = "forest"
        self.day = 1
        self.game_over = False
        self.won = False
        self.events_triggered = set()
        self.reputation = {"villagers": 0, "hermit": 0}
        self.crafted_items = set()
        self.visited_locations = set()
        self.npcs = {}
        self.quests = {}
        self.active_quests = []
        self.completed_quests = []
        self.easter_eggs_found = set()
        self.ending_type = None
        self.hired_npcs = []
        self.poison_counter = 0
        self.available_gold = 0
        
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        
    def display_status(self):
        print("\n" + "="*50)
        print(f"DAY {self.day} | {self.player_name}")
        print(f"Health: {self.health}/100 | Hunger: {self.hunger}/100")
        if self.poison_counter > 0:
            print(f"⚠ Raw Meat Poison: {self.poison_counter}% | Hired NPCs: {len(self.hired_npcs)}")
        elif len(self.hired_npcs) > 0:
            print(f"Hired NPCs: {len(self.hired_npcs)}")
        print(f"Location: {self.location.title()}")
        if self.available_gold > 0:
            print(f"Gold: {self.available_gold}")
        if self.inventory:
            print(f"Inventory: {', '.join(self.inventory)}")
        else:
            print("Inventory: Empty")
        if len(self.active_quests) > 0:
            print(f"Active Quests: {len(self.active_quests)}")
        if len(self.easter_eggs_found) > 0:
            print(f"🔍 Secrets Found: {len(self.easter_eggs_found)}")
        print("="*50 + "\n")
        
    def add_item(self, item):
        if item not in self.inventory:
            self.inventory.append(item)
            print(f"✓ Added {item} to inventory.")
        else:
            if "meat" in item or "fish" in item or "berries" in item or "food" in item:
                self.inventory.append(item)
                print(f"✓ Added {item} to inventory.")
            else:
                print(f"{item} already in inventory.")
            
    def has_item(self, item):
        return item in self.inventory
        
    def remove_item(self, item):
        if item in self.inventory:
            self.inventory.remove(item)
            return True
        return False
        
    def modify_stats(self, health=0, hunger=0):
        self.health = max(0, min(100, self.health + health))
        self.hunger = max(0, min(100, self.hunger + hunger))
    
    def apply_poison_damage(self):
        """Apply damage from raw meat poison counter"""
        if self.poison_counter > 0:
            damage = int(self.poison_counter * 0.5)
            self.modify_stats(health=-damage)
            self.poison_counter = max(0, self.poison_counter - 10)
            if damage > 0:
                print(f"⚠ Poison damage: {damage} health lost. Poison level: {self.poison_counter}%")
    
    def hire_npc(self, npc_type):
        """Hire an NPC worker"""
        available_names = {
            "hunter": ["Garrett", "Helena", "Quinn", "Roan"],
            "gatherer": ["Felix", "Iris", "Milo", "Nina"],
            "scout": ["Axel", "Sage", "Kai", "Scout"],
            "cook": ["Bruno", "Rosa", "Claude", "Mira"]
        }
        hired_npc = HiredNPC(npc_type, random.choice(available_names.get(npc_type, ["Worker"])))
        self.hired_npcs.append(hired_npc)
        print(f"✓ Hired {hired_npc.name} the {npc_type}! (Effectiveness: {hired_npc.effectiveness}%)")
        return hired_npc
    
    def pay_workers(self):
        """Pay daily wages to hired NPCs"""
        total_cost = sum(npc.cost_per_day for npc in self.hired_npcs)
        if self.available_gold >= total_cost:
            self.available_gold -= total_cost
            print(f"Paid workers {total_cost} gold. Remaining: {self.available_gold}")
            return True
        else:
            if len(self.hired_npcs) > 0:
                print(f"⚠ Cannot afford to pay workers! Need {total_cost}, have {self.available_gold}")
                print("Workers are getting angry...")
                for npc in self.hired_npcs:
                    npc.morale -= 20
            return False
    
    def hunt_with_hired(self, hunter):
        """Use a hired hunter to help hunt"""
        success_rate = hunter.effectiveness + (10 if hunter.morale >= 70 else -10 if hunter.morale < 40 else 0)
        if random.randint(1, 100) <= success_rate:
            self.add_item("venison")
            print(f"{hunter.name}: 'Got one! Fresh meat for the group!'")
            hunter.loyalty += 5
            hunter.morale = min(100, hunter.morale + 10)
            return True
        else:
            print(f"{hunter.name}: 'It got away. These beasts are wily.'")
            hunter.morale = max(0, hunter.morale - 5)
            return False
    
    def cook_with_hired(self, cook, item):
        """Use a hired cook to prepare food"""
        if item == "raw_meat":
            self.remove_item(item)
            self.add_item("cooked_meat")
            print(f"{cook.name}: 'Let me fix that up for you. Nothing worse than raw meat.'")
            cook.loyalty += 3
            cook.morale = min(100, cook.morale + 5)
            return True
        return False
        
    def craft_item(self, recipe_name):
        """Craft items from inventory"""
        recipes = {
            "bow": ["wooden_branch", "vine"],
            "spear": ["wooden_branch", "sharp_stone"],
            "medicine": ["herbs", "honey"],
            "rope": ["vine", "vine"],
            "fire_kit": ["dry_wood", "flint"],
            "water_bottle": ["leather", "clay"],
        }
        
        if recipe_name not in recipes:
            print(f"Unknown recipe: {recipe_name}")
            return False
            
        required = recipes[recipe_name]
        for item in required:
            if not self.has_item(item):
                print(f"Missing: {item}")
                return False
                
        for item in required:
            self.remove_item(item)
            
        self.add_item(recipe_name)
        self.crafted_items.add(recipe_name)
        print(f"✓ Crafted {recipe_name}!")
        return True
        
    def intro(self):
        self.clear_screen()
        print("╔════════════════════════════════════════════════════════╗")
        print("║            SURVIVAL: Lost in the Wild                 ║")
        print("╚════════════════════════════════════════════════════════╝\n")
        print("You wake up in a dense forest with no memory of how you got there.")
        print("Your goal: survive for 7 days and escape the wilderness.\n")
        self.player_name = input("What is your name? ").strip() or "Survivor"
        print(f"\nWelcome, {self.player_name}. Good luck out there.\n")
        
        self.npcs["hermit"] = NPC("hermit")
        self.npcs["villager_1"] = NPC("villager")
        self.npcs["merchant"] = NPC("merchant")
        
        self.quests["rescue"] = Quest("rescue", "Escape the Wilderness", 
                                      "Reach the village and catch the helicopter by day 7",
                                      [], 0)
        self.quests["find_hermit"] = Quest("find_hermit", "Find the Hermit",
                                          "Discover the hermit in the northern cave",
                                          ["hermit_wisdom"], 0)
        self.quests["gather_food"] = Quest("gather_food", "Stock Up on Food",
                                          "Collect 3 food items for the journey",
                                          ["travelers_ration"], 5)
        
        input("Press Enter to begin...")
        
    def forest_event(self):
        """Random events in the forest"""
        event_roll = random.randint(1, 100)
        
        if event_roll < 20 and "easter_artifact" not in self.easter_eggs_found:
            print("You find a strange glowing stone deep in the forest...")
            print("[1] Take it")
            print("[2] Leave it")
            choice = input("> ").strip()
            if choice == "1":
                self.add_item("mysterious_stone")
                self.easter_eggs_found.add("easter_artifact")
                print("The stone pulses with an ancient energy.")
                
        elif event_roll < 30:
            print("You stumble upon berry bushes laden with ripe berries.")
            print("[1] Eat some berries (gain food)")
            print("[2] Leave them (suspicious)")
            choice = input("> ").strip()
            if choice == "1":
                self.add_item("berries")
                self.modify_stats(hunger=-20)
                print("You eat some berries. They're delicious and fill your stomach.")
            else:
                print("You wisely decide to move on.")
                
        elif event_roll < 60:
            print("You find wooden branches and dry leaves.")
            print("[1] Gather materials for shelter")
            print("[2] Keep moving")
            choice = input("> ").strip()
            if choice == "1":
                self.add_item("shelter_materials")
                print("You gather materials for a proper shelter.")
            else:
                print("You continue on.")
                
        elif event_roll < 85:
            print("A deer appears in the clearing ahead.")
            hunters = [npc for npc in self.hired_npcs if npc.type == "hunter"]
            if hunters:
                print(f"[1] Hunt with {hunters[0].name}'s help")
                print("[2] Let it pass")
                choice = input("> ").strip()
                if choice == "1":
                    if self.hunt_with_hired(hunters[0]):
                        self.events_triggered.add("hunted_deer")
                else:
                    print("You let the deer go unharmed.")
            elif self.has_item("bow"):
                print("[1] Hunt it with your bow")
                print("[2] Let it pass")
                choice = input("> ").strip()
                if choice == "1" and random.randint(1, 100) > 30:
                    self.add_item("venison")
                    print("Success! You hunt the deer and gain fresh meat.")
                    self.events_triggered.add("hunted_deer")
                elif choice == "1":
                    print("You miss. The deer bounds away.")
                else:
                    print("You let the deer go unharmed.")
            else:
                print("[1] Try to catch it (unlikely without tools)")
                print("[2] Watch it pass")
                choice = input("> ").strip()
                if choice == "1" and random.randint(1, 100) > 70:
                    print("Miraculously, you catch the deer! But you need to process it...")
                    self.add_item("raw_meat")
                else:
                    print("The deer escapes easily. You should find better tools.")
                    
        else:
            print("You hear a low growl... A wolf emerges from the trees!")
            print("[1] Run away")
            print("[2] Stand your ground")
            print("[3] Offer food")
            choice = input("> ").strip()
            if choice == "1":
                if random.randint(1, 100) > 40:
                    print("You run and hide. The wolf loses interest.")
                else:
                    self.modify_stats(health=-25)
                    print("The wolf catches you! You suffer wounds.")
            elif choice == "2":
                print("The wolf sizes you up and backs away. You're tougher than it thought.")
            elif choice == "3" and self.has_item("berries"):
                self.remove_item("berries")
                print("You toss berries to the wolf. It eats them and wanders off.")
                self.events_triggered.add("fed_wolf")
            else:
                self.modify_stats(health=-15)
                print("The wolf attacks! You manage to escape but take damage.")
                
    def mountain_event(self):
        """Events in the mountains"""
        event_roll = random.randint(1, 100)
        
        if event_roll < 40:
            print("You discover a cave entrance.")
            print("[1] Enter the cave")
            print("[2] Pass by")
            choice = input("> ").strip()
            if choice == "1":
                if random.randint(1, 100) > 60:
                    self.add_item("cave_treasure")
                    print("Inside, you find gold coins! Someone was here before...")
                    self.events_triggered.add("found_treasure")
                else:
                    print("The cave is empty but sheltered. Good place to sleep.")
                    self.add_item("shelter_materials")
            else:
                print("You continue up the mountain.")
                
        elif event_roll < 70:
            print("Dark clouds roll in. A storm is coming!")
            if self.has_item("shelter_materials"):
                print("[1] Build shelter (costs shelter_materials)")
                print("[2] Keep moving")
                choice = input("> ").strip()
                if choice == "1":
                    self.remove_item("shelter_materials")
                    print("You build a makeshift shelter. You stay dry and warm.")
                    self.modify_stats(health=10)
                else:
                    self.modify_stats(health=-20, hunger=10)
                    print("You're caught in the storm. Cold, wet, and exhausted.")
            else:
                print("No shelter materials! The storm hammers you.")
                self.modify_stats(health=-30, hunger=20)
                
        else:
            print("You reach a high vantage point. In the distance, you see smoke...")
            print("[1] Head toward the smoke (risky)")
            print("[2] Stay safe in the mountains")
            choice = input("> ").strip()
            if choice == "1":
                print("You head toward the smoke. Hope rises!")
                self.location = "village"
                self.events_triggered.add("found_village_smoke")
            else:
                print("You decide the safe route is best for now.")
                
    def village_event(self):
        """Village events - easier survival with branching storyline"""
        event_roll = random.randint(1, 100)
        
        if event_roll < 50 and "met_villagers" not in self.events_triggered:
            print("You find a small village! Smoke rises from chimneys.")
            print(f"You see {self.npcs['villager_1'].name} approaching cautiously...")
            print("[1] Approach the villagers")
            print("[2] Stay hidden and watch")
            print("[3] Ask about the hermit")
            choice = input("> ").strip()
            if choice == "1":
                print(f"{self.npcs['villager_1'].name}: 'Are you alright? Where did you come from?'")
                print("The villagers welcome you! They offer food and shelter.")
                self.add_item("fresh_food")
                self.add_item("warm_bed")
                self.modify_stats(health=20, hunger=-30)
                self.reputation["villagers"] += 10
                self.events_triggered.add("met_villagers")
                print("They tell you: 'A helicopter lands at the valley airstrip at dawn on day 7.'")
                print(f"{self.npcs['villager_1'].name}: 'But beware the forest. There are old things in those woods.'")
                self.events_triggered.add("know_rescue")
            elif choice == "2":
                print("You watch the villagers go about their day. They seem kind and organized.")
                print("You learn that the helicopter comes at dawn.")
                self.events_triggered.add("know_rescue")
            elif choice == "3":
                print(f"{self.npcs['villager_1'].name} lowers their voice: 'The hermit? Few speak of him...'")
                print(f"'He lives in the northern caves. They say he's been there for decades.'")
                self.events_triggered.add("heard_of_hermit")
                self.events_triggered.add("know_rescue")
        else:
            print("You rest in the village.")
            if "met_villagers" in self.events_triggered:
                print(f"{self.npcs['villager_1'].name} brings you hot soup.")
            self.modify_stats(health=5, hunger=-10)
            
    def river_event(self):
        """Events at the river"""
        event_roll = random.randint(1, 100)
        
        if event_roll < 35:
            print("You reach a crystal-clear river. Fish swim lazily in the shallows.")
            hunters = [npc for npc in self.hired_npcs if npc.type == "hunter"]
            if hunters:
                print(f"[1] Fish with {hunters[0].name}'s help")
                print("[2] Collect water and move on")
                choice = input("> ").strip()
                if choice == "1":
                    if hunters[0].effectiveness > random.randint(1, 100):
                        self.add_item("fresh_fish")
                        print(f"{hunters[0].name}: 'Got one! Beautiful catch!'")
                        hunters[0].loyalty += 3
                        self.events_triggered.add("caught_fish")
                    else:
                        print(f"{hunters[0].name}: 'They're too fast today.'")
                else:
                    self.add_item("fresh_water")
                    print("You fill up on fresh, clean water.")
            else:
                print("[1] Try to catch fish (risky)")
                print("[2] Collect water and move on")
                choice = input("> ").strip()
                if choice == "1":
                    if random.randint(1, 100) > 40:
                        self.add_item("fresh_fish")
                        print("You manage to catch a fish! Fresh protein!")
                        self.events_triggered.add("caught_fish")
                    else:
                        self.modify_stats(health=-5)
                        print("You slip on the rocks. You catch nothing but a bruise.")
                else:
                    self.add_item("fresh_water")
                    print("You fill up on fresh, clean water.")
                
        elif event_roll < 70:
            print("Along the riverbank, you find useful items.")
            print("[1] Collect clay and leather")
            print("[2] Keep moving")
            choice = input("> ").strip()
            if choice == "1":
                self.add_item("clay")
                self.add_item("leather")
                print("You gather clay and find animal hide. Useful for crafting!")
            else:
                print("You continue along the river.")
                
        else:
            print("A massive bear emerges from the forest, heading to the river to fish...")
            print("[1] Hide and stay quiet")
            print("[2] Make noise and run")
            print("[3] Offer food (if you have any)")
            choice = input("> ").strip()
            if choice == "1":
                if random.randint(1, 100) > 50:
                    print("You hide perfectly. The bear doesn't notice you.")
                else:
                    self.modify_stats(health=-30)
                    print("The bear spots you! You take severe damage escaping.")
            elif choice == "2":
                if random.randint(1, 100) > 30:
                    print("You run and escape! Your heart pounds.")
                else:
                    self.modify_stats(health=-35)
                    print("The bear is faster than you! You take a swipe.")
            elif choice == "3" and (self.has_item("fresh_fish") or self.has_item("berries")):
                self.remove_item("fresh_fish") if self.has_item("fresh_fish") else self.remove_item("berries")
                print("The bear eats the food and wanders off, satisfied.")
                self.events_triggered.add("fed_bear")
            else:
                self.modify_stats(health=-40)
                print("The bear attacks! You barely escape.")
                
    def cabin_event(self):
        """Abandoned cabin event"""
        if "cabin_explored" in self.events_triggered:
            print("You return to the abandoned cabin. It's still quiet.")
            print("[1] Rest here")
            print("[2] Check for gold")
            print("[3] Leave")
            choice = input("> ").strip()
            if choice == "1":
                self.modify_stats(health=15, hunger=5)
                print("You sleep in the cabin. It's surprisingly comfortable.")
            elif choice == "2":
                gold_found = random.randint(20, 50)
                self.available_gold += gold_found
                print(f"You find {gold_found} gold coins hidden in the cabin! Total: {self.available_gold}")
        else:
            print("You discover an abandoned cabin deep in the woods!")
            print("The door creaks open...")
            print("[1] Enter cautiously")
            print("[2] Walk away (bad omen)")
            choice = input("> ").strip()
            if choice == "1":
                if random.randint(1, 100) > 40:
                    print("Inside, you find supplies: canned food, a map, and flint!")
                    self.add_item("canned_food")
                    self.add_item("map")
                    self.add_item("flint")
                    if random.randint(1, 100) > 60:
                        gold_found = random.randint(30, 75)
                        self.available_gold += gold_found
                        print(f"You also find {gold_found} gold coins! Total: {self.available_gold}")
                    self.events_triggered.add("cabin_treasure")
                else:
                    print("The cabin is mostly bare. You find some dry wood though.")
                    self.add_item("dry_wood")
                self.events_triggered.add("cabin_explored")
            else:
                print("You wisely turn back.")
                
    def ruins_event(self):
        """Ancient ruins with secrets"""
        if "ruins_explored" in self.events_triggered:
            print("You return to the ancient ruins. Strange stone carvings mark the walls.")
            print("[1] Investigate further")
            print("[2] Leave")
            choice = input("> ").strip()
            if choice == "1":
                print("You find a hidden chamber with ceremonial artifacts.")
                if "ruined_statue" not in self.inventory:
                    self.add_item("ruined_statue")
                    print("You take a mysterious stone statue.")
        else:
            print("You stumble upon ancient ruins overgrown with vines.")
            print("Carved symbols cover crumbling stone walls...")
            print("[1] Explore the ruins")
            print("[2] Avoid them (eerie)")
            choice = input("> ").strip()
            if choice == "1":
                print("You carefully navigate the ruins.")
                if random.randint(1, 100) > 50:
                    print("You find honey stored in clay jars - perfectly preserved!")
                    self.add_item("honey")
                    self.events_triggered.add("found_honey")
                else:
                    self.add_item("herbs")
                    print("You gather rare medicinal herbs.")
                self.events_triggered.add("ruins_explored")
                if random.randint(1, 100) > 70:
                    print("You also discover old writings mentioning a 'hermit in the north.'")
                    self.events_triggered.add("heard_of_hermit")
            else:
                print("You back away slowly. Best not to disturb ancient places.")
                
    def check_easter_eggs(self):
        """Random Easter eggs hidden throughout the game"""
        egg_roll = random.randint(1, 1000)
        
        if egg_roll < 5 and "easter_camp" not in self.easter_eggs_found:
            print("\n✦ You stumble upon an old survivor camp with faded writing on a tree...")
            print("'If you're reading this, you made it. - John, Day 47'")
            print("Someone was here much longer than 7 days...")
            self.easter_eggs_found.add("easter_camp")
            self.add_item("john_journal")
            
        elif egg_roll < 10 and "easter_artifact" not in self.easter_eggs_found:
            print("\n✦ You find a strange glowing stone. It hums softly.")
            print("'The ancient ones left their marks,' you think.")
            self.easter_eggs_found.add("easter_artifact")
            self.add_item("mysterious_stone")
            self.modify_stats(health=5)
            
        elif egg_roll < 15 and "easter_lake" not in self.easter_eggs_found and self.location == "ruins":
            print("\n✦ Behind a hidden wall, you discover an underground lake with glowing fish!")
            print("You fill your bottle with luminescent water.")
            self.easter_eggs_found.add("easter_lake")
            self.add_item("glowing_water")
            
        elif egg_roll < 20 and "easter_loop" not in self.easter_eggs_found:
            print("\n✦ You find a calendar scratched into a rock: Day 1, Day 1, Day 1, Day 1...")
            print("Someone was trapped in a loop. Or were they?")
            self.easter_eggs_found.add("easter_loop")
            
        elif egg_roll < 25 and "easter_message" not in self.easter_eggs_found:
            print("\n✦ Carved into a tree: 'TRUST THE HERMIT'")
            print("Someone left a warning or a guide.")
            self.easter_eggs_found.add("easter_message")
            
    def check_secret_events(self):
        """Trigger special hidden story events"""
        if self.day == 3 and "secret_illness" not in self.events_triggered and random.randint(1, 100) < 40:
            print("\n⚠ You feel a strange illness coming on. Your head spins...")
            print("A fever overtakes you. Was it the water? The food?")
            self.modify_stats(health=-20, hunger=15)
            self.events_triggered.add("secret_illness")
            if self.reputation["hermit"] > 5:
                print("(You remember the hermit's medicine could have helped...)")
                
        elif self.day == 5 and "secret_visitor" not in self.events_triggered and random.randint(1, 100) < 30:
            print("\n✦ At night, you hear footsteps. Someone passes through your camp.")
            print("In the morning, there's fresh meat and a carved wooden figure left behind.")
            self.add_item("gift_from_stranger")
            self.events_triggered.add("secret_visitor")
        elif "met_hermit" not in self.events_triggered:
            print(f"Deep in a cave, you find an old {self.npcs['hermit'].personality} man tending a fire.")
            print(f"{self.npcs['hermit'].greet()}")
            print(f"\nHermit {self.npcs['hermit'].name}: \"{self.npcs['hermit'].backstory}\"")
            print("\n[1] Greet him peacefully")
            print("[2] Ask for help")
            print("[3] Leave quietly")
            choice = input("> ").strip()
            if choice == "1":
                print(f"The hermit nods. '{self.npcs['hermit'].name} does not see many visitors out here.'")
                self.reputation["hermit"] += 5
                self.add_item("hermit_bread")
                print("He gives you some bread made from wild grains.")
                self.events_triggered.add("met_hermit")
                self.completed_quests.append("find_hermit")
            elif choice == "2":
                print(f"The hermit studies you carefully.")
                if "heard_of_hermit" in self.events_triggered:
                    print(f"'{self.npcs['hermit'].name}: Ah, you know of me from the old stones, I see.'")
                    print("He teaches you to make fire. You gain flint and dry_wood knowledge.")
                    self.reputation["hermit"] += 10
                    self.add_item("flint")
                    self.add_item("fire_knowledge")
                else:
                    print(f"'{self.npcs['hermit'].name}: Why should I help a stranger?'")
                    self.reputation["hermit"] -= 5
                self.events_triggered.add("met_hermit")
            else:
                print("You slip out silently. The hermit doesn't notice.")
        else:
            print(f"You return to {self.npcs['hermit'].name}'s cave.")
            print(f"The {self.npcs['hermit'].personality} man offers you more bread and wisdom.")
            self.modify_stats(hunger=-15, health=5)
            print(f"'{self.npcs['hermit'].name}: Survive, and you'll find peace,' he says.")

            
    def display_ending_harmony(self):
        """Best ending - gained trust from all NPCs"""
        print(f"\n{'='*60}")
        print(f"VICTORY - THE HARMONY ENDING")
        print(f"{'='*60}\n")
        print(f"You arrive at the village and the helicopter awaits.")
        print(f"Both {self.npcs['hermit'].name} and {self.npcs['villager_1'].name} wave you off.")
        print(f"\n{self.npcs['villager_1'].name}: 'You brought peace to our lands. We are grateful.'")
        print(f"{self.npcs['hermit'].name}: 'Go live the life you're meant to live.'")
        print(f"\nYou board the helicopter, forever changed by this wilderness...")
        print(f"  • Both hermit and villagers respected you deeply")
        print(f"  • Health: {self.health}/100 | Hunger: {self.hunger}/100")
        print(f"  • Locations Discovered: {len(self.visited_locations)}")
        print(f"  • Items Crafted: {len(self.crafted_items)}")
        print(f"  • Hidden Secrets Found: {len(self.easter_eggs_found)}")
        print(f"{'='*60}\n")
        
    def display_ending_enlightenment(self):
        """Secret ending - discovered all Easter eggs"""
        print(f"\n{'='*60}")
        print(f"VICTORY - THE ENLIGHTENMENT ENDING")
        print(f"{'='*60}\n")
        print(f"As you board the helicopter, a realization strikes you.")
        print(f"All the clues, the messages, the ancient ruins...")
        print(f"Someone else has walked this path before. Many someones.")
        print(f"\nYou clutch the mysterious stone. It pulses with warmth.")
        print(f"The helicopter ascends, and you swear you see petroglyphs")
        print(f"from the air spelling out: 'WELCOME TO THE CYCLE.'")
        print(f"\nWhat was this place? Will you be back?")
        print(f"  • Easter Eggs Discovered: {len(self.easter_eggs_found)}")
        print(f"  • NPCs Met: {len([k for k in self.npcs.keys()])}")
        print(f"  • Secrets Unlocked: Several")
        print(f"{'='*60}\n")
        
    def display_ending_healthy(self):
        """Strong ending - excellent physical condition"""
        print(f"\n{'='*60}")
        print(f"VICTORY - THE CHAMPION ENDING")
        print(f"{'='*60}\n")
        print(f"You stride into the village looking remarkably well.")
        print(f"The villagers are shocked by your vitality.")
        print(f"\n'You didn't just survive,' {self.npcs['villager_1'].name} says.")
        print(f"'You thrived. Are you even human?'")
        print(f"\nYou board the helicopter with pride.")
        print(f"Your adventure has made you stronger than you were before.")
        print(f"  • Final Health: {self.health}/100 (EXCELLENT)")
        print(f"  • Survival Skills: Mastered")
        print(f"  • Days Survived: {self.day}")
        print(f"{'='*60}\n")
        
    def display_ending_hero(self):
        """Good ending - helped many NPCs"""
        print(f"\n{'='*60}")
        print(f"VICTORY - THE HERO ENDING")
        print(f"{'='*60}\n")
        print(f"You arrive at the village. The people line up to thank you.")
        print(f"Stories of your kindness have spread:")
        print(f"  • The wolf you spared tells its pack you're not a threat")
        print(f"  • The hermit speaks fondly of your wisdom")
        print(f"  • The villagers see you as a savior")
        print(f"\nYou are the hero of this wilderness.")
        print(f"  • Reputation Points Earned: {self.reputation['villagers'] + self.reputation['hermit']}")
        print(f"  • Lives Touched: Many")
        print(f"  • Legacy: Hero of the Wild")
        print(f"{'='*60}\n")
        
    def display_ending_basic(self):
        """Standard ending"""
        print(f"\n{'='*60}")
        print(f"VICTORY!")
        print(f"{self.player_name} reached the village and escaped via helicopter!")
        print(f"{'='*60}\n")
        print(f"You made it out alive. Against the odds, you survived.")
        print(f"\nSurvived {self.day} days with condition:")
        print(f"  • Health: {self.health}/100")
        print(f"  • Hunger: {self.hunger}/100")
        print(f"  • Locations Visited: {len(self.visited_locations)}")
        if len(self.easter_eggs_found) > 0:
            print(f"  • Secrets Found: {len(self.easter_eggs_found)}")
        print(f"\n--- Key Achievements ---")
        if "hunted_deer" in self.events_triggered:
            print(f"  ✓ Hunted a deer for survival")
        if "fed_wolf" in self.events_triggered:
            print(f"  ✓ Made peace with a wolf")
        if "found_treasure" in self.events_triggered:
            print(f"  ✓ Found hidden treasure")
        if "caught_fish" in self.events_triggered:
            print(f"  ✓ Caught fresh fish from the river")
        if "fed_bear" in self.events_triggered:
            print(f"  ✓ Pacified a grizzly bear")
        if "met_hermit" in self.events_triggered:
            print(f"  ✓ Met {self.npcs['hermit'].name} the hermit")
        if len(self.crafted_items) > 0:
            print(f"  ✓ Crafted {len(self.crafted_items)} items")
        print(f"{'='*60}\n")
        
    def check_end_conditions(self):
        """Check if game should end with different ending types"""
        if self.health <= 0:
            self.game_over = True
            self.won = False
            self.ending_type = "death"
            print(f"\n{'='*50}")
            print(f"GAME OVER - {self.player_name} collapsed from exhaustion.")
            print(f"{'='*50}\n")
            
        elif self.hunger >= 90:
            self.game_over = True
            self.won = False
            self.ending_type = "starvation"
            print(f"\n{'='*50}")
            print(f"GAME OVER - {self.player_name} starved.")
            print(f"{'='*50}\n")
            
        elif self.day >= 7 and self.location == "village" and "know_rescue" in self.events_triggered:
            self.game_over = True
            self.won = True
            
            if self.reputation["hermit"] > 15 and self.reputation["villagers"] > 15:
                self.ending_type = "harmony"
                self.display_ending_harmony()
            elif len(self.easter_eggs_found) >= 4:
                self.ending_type = "enlightenment"
                self.display_ending_enlightenment()
            elif self.health > 80:
                self.ending_type = "healthy_escape"
                self.display_ending_healthy()
            elif self.reputation["villagers"] > 10:
                self.ending_type = "hero"
                self.display_ending_hero()
            else:
                self.ending_type = "bare_escape"
                self.display_ending_basic()
                
        elif self.day >= 8:
            self.game_over = True
            self.won = False
            self.ending_type = "timeout"
            print(f"\n{'='*50}")
            print(f"GAME OVER - {self.player_name} ran out of time.")
            print(f"The helicopter has come and gone. You are truly alone now.")
            print(f"{'='*50}\n")
            
    def next_day(self):
        """Advance day and apply survival costs"""
        self.day += 1
        self.modify_stats(hunger=random.randint(5, 15))
        
        if not self.has_item("warm_bed"):
            self.modify_stats(health=random.randint(-5, -1))
            
        print(f"\nThe sun rises on Day {self.day}...\n")
        
    def play_day(self):
        """Main gameplay loop for a single day"""
        while not self.game_over:
            self.display_status()
            
            self.apply_poison_damage()
            
            self.check_secret_events()
            self.check_easter_eggs()
            
            print("What do you do?")
            print("[1] Explore")
            print("[2] Rest (reduces hunger by 5, minor health recovery)")
            print("[3] Forage (search for food)")
            print("[4] Check inventory")
            print("[5] Build shelter (if you have materials)")
            print("[6] Craft items")
            print("[7] Move to another location")
            print("[8] Manage Hired NPCs")
            print("[9] Eat food/Cook raw meat")
            
            choice = input("> ").strip()
            
            if choice == "1":
                self.clear_screen()
                if self.location == "forest":
                    self.forest_event()
                elif self.location == "mountain":
                    if random.randint(1, 100) > 50:
                        self.location = "mountain"
                    else:
                        self.location = "forest"
                    self.mountain_event()
                elif self.location == "village":
                    self.village_event()
                elif self.location == "river":
                    self.river_event()
                elif self.location == "cabin":
                    self.cabin_event()
                elif self.location == "ruins":
                    self.ruins_event()
                elif self.location == "hermit_cave":
                    self.check_secret_events()
                    
            elif choice == "2":
                self.clear_screen()
                self.modify_stats(health=10, hunger=5)
                print("You rest and recover.")
                
            elif choice == "3":
                self.clear_screen()
                if random.randint(1, 100) > 60:
                    self.add_item("foraged_berries")
                    print("You find some edible berries and nuts.")
                else:
                    print("Your search yields nothing of value.")
                    
            elif choice == "4":
                self.clear_screen()
                if self.inventory:
                    print(f"You have: {', '.join(self.inventory)}")
                else:
                    print("Your inventory is empty.")
                    
            elif choice == "5":
                self.clear_screen()
                if self.has_item("shelter_materials"):
                    self.remove_item("shelter_materials")
                    self.add_item("shelter")
                    print("You build a shelter.")
                else:
                    print("You need shelter materials to build a shelter.")
                    
            elif choice == "6":
                self.clear_screen()
                print("Available recipes:")
                print("[1] Bow (needs: wooden_branch, vine)")
                print("[2] Spear (needs: wooden_branch, sharp_stone)")
                print("[3] Medicine (needs: herbs, honey)")
                print("[4] Rope (needs: vine, vine)")
                print("[5] Fire Kit (needs: dry_wood, flint)")
                print("[6] Back")
                recipe_choice = input("> ").strip()
                recipes_map = {"1": "bow", "2": "spear", "3": "medicine", "4": "rope", "5": "fire_kit"}
                if recipe_choice in recipes_map:
                    self.craft_item(recipes_map[recipe_choice])
                    
            elif choice == "7":
                self.clear_screen()
                print("Where do you want to go?")
                print("[1] Forest")
                print("[2] Mountain")
                print("[3] Village")
                print("[4] River")
                print("[5] Cabin")
                print("[6] Ruins")
                print("[7] Hermit Cave")
                print("[8] Cancel")
                loc_choice = input("> ").strip()
                locations_map = {
                    "1": "forest", "2": "mountain", "3": "village",
                    "4": "river", "5": "cabin", "6": "ruins", "7": "hermit_cave"
                }
                if loc_choice in locations_map:
                    self.location = locations_map[loc_choice]
                    self.visited_locations.add(self.location)
                    print(f"You travel to {self.location.title()}...")
                    
            elif choice == "8":
                self.clear_screen()
                self.manage_hired_npcs()
                
            elif choice == "9":
                self.clear_screen()
                self.eat_or_cook()
                    
            else:
                self.clear_screen()
                print("Invalid choice.")
                continue
                
            self.check_end_conditions()
            if not self.game_over:
                input("\nPress Enter to continue...")
                self.clear_screen()
                self.next_day()
    
    def manage_hired_npcs(self):
        """Menu to manage hired NPCs"""
        while True:
            print("\n=== Manage Hired NPCs ===")
            if len(self.hired_npcs) == 0:
                print("You have no hired NPCs.")
                print("\n[1] Hire a Hunter (10 gold/day)")
                print("[2] Hire a Gatherer (5 gold/day)")
                print("[3] Hire a Scout (8 gold/day)")
                print("[4] Hire a Cook (7 gold/day)")
                print("[5] Back")
                print(f"\nAvailable Gold: {self.available_gold}")
                choice = input("> ").strip()
                if choice == "1" and self.available_gold >= 10:
                    self.hire_npc("hunter")
                elif choice == "2" and self.available_gold >= 5:
                    self.hire_npc("gatherer")
                elif choice == "3" and self.available_gold >= 8:
                    self.hire_npc("scout")
                elif choice == "4" and self.available_gold >= 7:
                    self.hire_npc("cook")
                elif choice in ["1", "2", "3", "4"]:
                    print("Not enough gold!")
                elif choice == "5":
                    break
            else:
                for i, npc in enumerate(self.hired_npcs, 1):
                    print(f"[{i}] {npc.get_description()}")
                print(f"[{len(self.hired_npcs) + 1}] Hire new NPC")
                print(f"[{len(self.hired_npcs) + 2}] Pay workers (Cost: {sum(npc.cost_per_day for npc in self.hired_npcs)} gold)")
                print(f"[{len(self.hired_npcs) + 3}] Fire an NPC")
                print(f"[{len(self.hired_npcs) + 4}] Back")
                print(f"\nAvailable Gold: {self.available_gold}")
                choice = input("> ").strip()
                
                if choice.isdigit():
                    idx = int(choice) - 1
                    if 0 <= idx < len(self.hired_npcs):
                        print(f"\n{self.hired_npcs[idx].get_description()}")
                        print(f"Backstory: {self.hired_npcs[idx].name} is a {self.hired_npcs[idx].type}")
                    elif idx == len(self.hired_npcs):
                        print("\n[1] Hire a Hunter (10 gold/day)")
                        print("[2] Hire a Gatherer (5 gold/day)")
                        print("[3] Hire a Scout (8 gold/day)")
                        print("[4] Hire a Cook (7 gold/day)")
                        hire_choice = input("> ").strip()
                        hire_map = {"1": "hunter", "2": "gatherer", "3": "scout", "4": "cook"}
                        if hire_choice in hire_map:
                            cost = {"hunter": 10, "gatherer": 5, "scout": 8, "cook": 7}[hire_map[hire_choice]]
                            if self.available_gold >= cost:
                                self.hire_npc(hire_map[hire_choice])
                            else:
                                print("Not enough gold!")
                    elif idx == len(self.hired_npcs) + 1:
                        self.pay_workers()
                    elif idx == len(self.hired_npcs) + 2:
                        print("\nWho do you want to fire?")
                        for j, npc in enumerate(self.hired_npcs, 1):
                            print(f"[{j}] {npc.name}")
                        fire_choice = input("> ").strip()
                        if fire_choice.isdigit() and 0 <= int(fire_choice) - 1 < len(self.hired_npcs):
                            fired = self.hired_npcs.pop(int(fire_choice) - 1)
                            print(f"{fired.name} has been fired and left your group.")
                    elif idx == len(self.hired_npcs) + 3:
                        break
    
    def eat_or_cook(self):
        """Eat food or cook raw meat"""
        food_items = [item for item in self.inventory if "meat" in item or "fish" in item or "berries" in item or "food" in item]
        if not food_items:
            print("You have no food to eat.")
            return
            
        print("\nWhat do you want to eat?")
        for i, item in enumerate(food_items, 1):
            print(f"[{i}] {item}")
        print(f"[{len(food_items) + 1}] Cancel")
        
        choice = input("> ").strip()
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(food_items):
                item = food_items[idx]
                self.remove_item(item)
                
                if item == "raw_meat":
                    cooks = [npc for npc in self.hired_npcs if npc.type == "cook"]
                    if cooks:
                        print(f"\n{cooks[0].name}: 'Let me cook that for you!'")
                        self.cook_with_hired(cooks[0], item)
                        self.modify_stats(hunger=-25, health=5)
                        print(f"You eat the cooked meat. It's delicious!")
                    else:
                        print("\n⚠ You eat raw meat. It's unsafe, but satisfies hunger...")
                        self.modify_stats(hunger=-20, health=-5)
                        poison_increase = random.randint(15, 35)
                        self.poison_counter += poison_increase
                        print(f"Poison level increased by {poison_increase}% (Total: {self.poison_counter}%)")
                        print("You feel a bit queasy... eating raw meat is dangerous!")
                elif item == "cooked_meat" or item == "venison":
                    self.modify_stats(hunger=-25, health=10)
                    print(f"You eat the {item}. It's delicious and nourishing!")
                elif item == "fresh_fish":
                    self.modify_stats(hunger=-20, health=8)
                    print(f"You eat the fresh fish. Tasty and healthy!")
                elif "berries" in item or "foraged" in item:
                    self.modify_stats(hunger=-15, health=5)
                    print(f"You eat the {item}. Sweet and refreshing!")
                else:
                    self.modify_stats(hunger=-15, health=5)
                    print(f"You eat the {item}. Not bad!")
                
    def run(self):
        """Main game loop"""
        self.intro()
        self.clear_screen()
        self.play_day()
        
        if self.won:
            print("Thanks for playing!\n")
        else:
            print("Better luck next time!\n")

if __name__ == "__main__":
    game = Game()
    game.run()
