# Implements a basic Character Creation system using Python OOP principles.
# Demonstrates Encapsulation, Inheritance, Polymorphism, Class Attributes, DUNDER Methods, and COMPOSITION.

import random
# NEW: Import ABC and abstractmethod for structural enforcement
from abc import ABC, abstractmethod

# --- CUSTOM EXCEPTION CLASS ---
class InvalidStatError(Exception):
    """Custom exception raised when a character is created with invalid (e.g., negative) stats."""
    pass

# --- ITEM CLASS (Basic Data Structure) ---
class Item:
    """Represents a simple game item."""
    def __init__(self, name: str, weight: float):
        self.name = name
        self.weight = weight

    # DUNDER METHOD: __str__ (allows clean printing of the item)
    def __str__(self):
        return f"{self.name} ({self.weight}kg)"

# --- INVENTORY CLASS (DUNDER Method Demonstration) ---
class Inventory:
    """
    Manages a collection of Items. 
    Implements dunder methods to act like a native Python container/list.
    """
    def __init__(self):
        self.items = []
        self.max_weight = 50.0 # Instance attribute: capacity limit

    # DUNDER METHOD: __len__ (allows use of len() function)
    def __len__(self):
        """Returns the number of items in the inventory."""
        return len(self.items)

    # DUNDER METHOD: __add__ (allows use of the + operator)
    def __add__(self, item_to_add):
        """
        Adds an item to the inventory using the '+' operator.
        Returns the Inventory object itself for chaining.
        """
        # ERROR HANDLING: Check if the object being added is the correct type
        if not isinstance(item_to_add, Item):
            raise TypeError("Only 'Item' objects can be added to the Inventory.")
        
        current_weight = sum(item.weight for item in self.items)
        if current_weight + item_to_add.weight <= self.max_weight:
            self.items.append(item_to_add)
            print(f"  [Inventory] Added {item_to_add.name}.")
        else:
            print(f"  [Inventory] Failed to add {item_to_add.name}. Max weight reached!")
        return self

    # DUNDER METHOD: __str__ (allows clean printing of the inventory contents)
    def __str__(self):
        if not self.items:
            return "Empty Inventory."
        
        item_list = "\n".join([f"    - {item}" for item in self.items])
        current_weight = sum(item.weight for item in self.items)
        return (f"Inventory ({len(self.items)} items, {current_weight:.1f}/{self.max_weight:.1f}kg used):\n"
                f"{item_list}")

# --- RACE CLASSES (Composition Demonstration) ---

class Race(ABC):
    """Abstract Base Class for all races. Character HAS A Race."""
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def apply_bonus(self) -> tuple[int, int]:
        """Returns (strength_bonus, intelligence_bonus)"""
        pass

    def __str__(self):
        return self.name

class Human(Race):
    def __init__(self):
        super().__init__("Human")

    def apply_bonus(self) -> tuple[int, int]:
        # Humans get a generalist bonus
        return (2, 2) 

class Elf(Race):
    def __init__(self):
        super().__init__("Elf")

    def apply_bonus(self) -> tuple[int, int]:
        # Elves get an Intelligence bonus
        return (0, 5) 

# --- BASE CLASS: Character (Abstract Base Class - Enforces Structure) ---
# Character now inherits from ABC to become an Abstract Base Class
class Character(ABC):
    """
    The abstract base class for all characters in the game.
    Manages core attributes common to all types and enforces required methods.
    """
    # CLASS ATTRIBUTE: Tracks the total number of Character objects created.
    total_characters_created = 0

    # Character now requires a Race object for initialization
    def __init__(self, name: str, strength: int, intelligence: int, race: Race):
        """Initializes a new character instance."""
        
        # ERROR HANDLING: Check for invalid stats before proceeding
        if strength < 0 or intelligence < 0:
            raise InvalidStatError(f"Cannot create {name}: Strength ({strength}) and Intelligence ({intelligence}) must be non-negative.")
            
        # COMPOSITION: Character HAS A Race object
        self.race = race
        
        # Apply race bonuses BEFORE setting instance attributes
        str_bonus, int_bonus = self.race.apply_bonus()
        
        # Instance Attributes (Unique to each character)
        self.name = name
        self.strength = strength + str_bonus # Apply bonus here
        self.intelligence = intelligence + int_bonus # Apply bonus here
        self.health = 100
        # Each character gets their own unique Inventory instance
        self.inventory = Inventory()
        
        # Protected Attribute (Encapsulation demonstration - convention only)
        self._base_attack_value = 10 
        
        # Update the Class Attribute
        Character.total_characters_created += 1
        
    # Property to check if the character is alive (better readability)
    @property
    def is_alive(self):
        return self.health > 0

    # Combat method
    def strike(self, target: 'Character'):
        """Calculates power and applies damage to the target."""
        if not self.is_alive:
            print(f"[{self.name}] is defeated and cannot strike.")
            return

        damage = self.calculate_special_power()
        
        # Apply damage to the target's health
        target.health -= damage
        
        # Ensure health does not go below zero
        if target.health < 0:
            target.health = 0
            
        print(f"[{self.name} ({self.__class__.__name__})] strikes {target.name} for {damage} damage!")
        print(f"[{target.name}] Health remaining: {target.health}")
        
        if not target.is_alive:
            print(f"*** [{target.name}] has been defeated! ***")
        
    def display_stats(self):
        """Prints the base statistics of the character."""
        # Print the race name
        print(f"--- {self.name} the {self.race.name} ({self.__class__.__name__}) ---")
        print(f"Health: {self.health}")
        print(f"Strength: {self.strength}")
        print(f"Intelligence: {self.intelligence}")

    # ABSTRACT METHOD: Subclasses MUST implement this method (Polymorphism)
    @abstractmethod
    def calculate_special_power(self) -> int:
        """
        Abstract method. Subclasses must override this to calculate their 
        specific power (damage, spell power, etc.).
        """
        # Note: The body of an abstract method is usually empty or just passes
        pass

    def __str__(self):
        """Dunder method for nice string representation (good OOP practice)."""
        return f"{self.name} the {self.__class__.__name__}"


# --- SUBCLASS 1: Warrior (Inheritance and Specialization) ---
class Warrior(Character):
    """
    Specialized character class focused on Strength and physical combat.
    Inherits all properties and methods from Character.
    """
    def __init__(self, name: str, strength: int, intelligence: int, race: Race):
        # Call the Parent Class's constructor, passing the race object
        super().__init__(name, strength, intelligence, race)
        self.weapon = "Greatsword"
        
        # Add a starting weapon using the Dunder __add__ method!
        self.inventory + Item(self.weapon, 5.5)

    def calculate_special_power(self) -> int:
        """
        POLYMOPRHISM: Overrides the parent abstract method to calculate damage 
        based on the Warrior's strength attribute.
        """
        # Damage = Base Attack + (Strength multiplier)
        damage = self._base_attack_value + (self.strength * 2)
        return damage
        
    def display_stats(self):
        """Overrides parent method to add warrior-specific details."""
        super().display_stats()
        print(f"Weapon: {self.weapon}")
        print(f"Calculated Damage: {self.calculate_special_power()}")
        print(str(self.inventory))


# --- SUBCLASS 2: Mage (Inheritance and Specialization) ---
class Mage(Character):
    """
    Specialized character class focused on Intelligence and magical power.
    Inherits all properties and methods from Character.
    """
    def __init__(self, name: str, strength: int, intelligence: int, race: Race):
        # Call the Parent Class's constructor, passing the race object
        super().__init__(name, strength, intelligence, race)
        self.spell = "Fireball"
        
        # Add a starting item using the Dunder __add__ method!
        self.inventory + Item("Mystic Staff", 3.0)
        
    def calculate_special_power(self) -> int:
        """
        POLYMOPRHISM: Overrides the parent abstract method to calculate spell power 
        based on the Mage's intelligence attribute.
        """
        # Spell Power = Base Attack + (Intelligence multiplier)
        spell_power = self._base_attack_value + (self.intelligence * 3)
        return spell_power

    def display_stats(self):
        """Overrides parent method to add mage-specific details."""
        super().display_stats()
        print(f"Favorite Spell: {self.spell}")
        print(f"Calculated Spell Power: {self.calculate_special_power()}")
        print(str(self.inventory))


# --- NEW: Testing Functions ---

def run_tests():
    """Runs a series of simple checks using assert statements."""
    print("\n" + "=" * 40)
    print("--- 4. Running Assert Tests for Core Logic ---")
    
    # Setup races for testing
    test_human = Human()
    test_elf = Elf()
    
    # Test 1: Inheritance/Composition - Check applied bonuses (Human Warrior: 25+2=27 Str)
    warrior_test = Warrior("TestWar", strength=25, intelligence=5, race=test_human)
    # Strength = 25 (base) + 2 (human bonus) = 27
    assert warrior_test.strength == 27, f"Test 1 failed. Expected Str 27, got {warrior_test.strength}"
    print("✅ Test 1: Human Warrior Strength bonus applied correctly.")
    
    # Test 2: Dunder Method __len__ - Check inventory count (1 initial item)
    assert len(warrior_test.inventory) == 1, f"Test 2 failed. Expected 1 item, got {len(warrior_test.inventory)}"
    print("✅ Test 2: Inventory length (via __len__) is correct.")
    
    # Test 3: Polymorphism/Calculation - Check Mage power calculation (Elf Mage: 22+5=27 Int)
    mage_test = Mage("TestMage", strength=8, intelligence=22, race=test_elf)
    # Power = 10 (base) + (27 Int * 3 multiplier) = 91
    expected_power = 10 + (27 * 3)
    assert mage_test.calculate_special_power() == expected_power, f"Test 3 failed. Expected Power {expected_power}, got {mage_test.calculate_special_power()}"
    print(f"✅ Test 3: Elf Mage Power calculation (91) is correct.")
    
    # Test 4: Combat/Health Floor - Check that health cannot go below zero.
    dummy_target = Warrior("Dummy", 1, 1, test_human) # Health 100
    
    # Create an intentionally overpowered attacker (Inheritance/Polymorphism test helper)
    class OverpoweredWarrior(Warrior):
        def calculate_special_power(self) -> int:
            return 200 # Guaranteed kill damage
            
    op_attacker = OverpoweredWarrior("OP", 50, 50, test_human)
    op_attacker.strike(dummy_target)
    
    # Assert that health is exactly 0 after the fatal strike
    assert dummy_target.health == 0, f"Test 4 failed. Health should be 0, got {dummy_target.health}"
    print("✅ Test 4: Character health correctly floored at 0 after defeat.")
    
    print("--- All Core Logic Tests Passed Successfully! ---")
    print("=" * 40)


def run_demo():
    """Contains the original demonstration of exception handling and combat."""
    
    # Define races (Composition Objects)
    human_race = Human()
    elf_race = Elf()
    
    # 1. Demonstration of Exception Handling (Invalid Creation)
    print("--- 1. Testing Invalid Character Creation ---")
    try:
        # This will raise the custom InvalidStatError
        broken_char = Warrior("Ogre", strength=-5, intelligence=10, race=human_race)
        print("Error: Character created successfully when it should have failed.")
    except InvalidStatError as e:
        print(f"Successfully handled error: {e}")
    except Exception as e:
        print(f"Caught unexpected error: {e}")
    print("-" * 30)


    # 2. Demonstration of Exception Handling (Type Error in Inventory)
    print("--- 2. Testing Invalid Inventory Addition ---")
    combatant_c = Warrior("ValidTest", strength=10, intelligence=10, race=human_race)
    try:
        # This will raise the built-in TypeError
        combatant_c.inventory + "A String, not an Item!"
    except TypeError as e:
        print(f"Successfully handled error: {e}")
    except Exception as e:
        print(f"Caught unexpected error: {e}")
    print("-" * 30)
    

    # 3. Simple Combat Simulation
    print("--- 3. Starting Combat Simulation ---")
    
    # Combatant A: A powerful Human Warrior (Focus on Strength)
    combatant_a = Warrior("Kratos", strength=25, intelligence=5, race=human_race)
    
    # Combatant B: A wise Elf Mage (Focus on Intelligence)
    combatant_b = Mage("Gandalf", strength=8, intelligence=22, race=elf_race)
    
    print(f"\nTotal characters created: {Character.total_characters_created}\n")
    
    combatant_a.display_stats()
    print("-" * 30)
    combatant_b.display_stats()
    print("-" * 30)

    print("\n--- Combat (Turn-Based) ---")
    
    turn = 1
    # Loop continues as long as both characters are alive
    while combatant_a.is_alive and combatant_b.is_alive:
        print(f"\n--- Turn {turn} ---")
        
        # Character A attacks Character B
        combatant_a.strike(combatant_b)
        if not combatant_b.is_alive:
            break # B defeated
        
        # Character B attacks Character A
        combatant_b.strike(combatant_a)
        if not combatant_a.is_alive:
            break # A defeated
            
        turn += 1
        
    print("\n--- Combat Concluded ---")
    if combatant_a.is_alive:
        print(f"{combatant_a.name} wins in {turn} turns!")
    elif combatant_b.is_alive:
        print(f"{combatant_b.name} wins in {turn} turns!")
    else:
        print("A rare double KO!")


# --- Execution Start ---
if __name__ == "__main__":
    # Run tests before running the main demo
    run_tests()
    run_demo()
