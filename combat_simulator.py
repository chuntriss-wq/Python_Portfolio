import random
# Using the external 'random' module to create unpredictable damage

# --- 1. DATA STORAGE RECIPES (Dictionaries) ---

# Define the player's starting statistics
player = {
    "name": "The Champion",
    "health": 100, 
    "attack_power": 15
}

# Define the enemy's starting statistics
enemy = {
    "name": "chris_lionheart",  
    "health": 200,
    "attack_power": 10 
}

# --- 2. CODE REUSABILITY RECIPE (Function) ---

# This function will calculate random damage for a cleaner main loop.
def calculate_damage(max_power):
   
    damage = random.randint(5, max_power)
    return damage

# --- 3. GAME START ---
print("=" * 40)
print(f"A wild {enemy['name']} appears! Get ready to fight!")
print(f"You ({player['name']}) have {player['health']} HP.")
print("=" * 40)


# --- 4. CONTROL FLOW RECIPE (WHILE Loop - The Battle) ---
# The loop runs as long as BOTH the player's health AND the enemy's health are above zero.
while player['health'] > 0 and enemy['health'] > 0:
    
    # 1. Player's Turn
    player_hit = calculate_damage(player['attack_power'])
    enemy['health'] = enemy['health'] - player_hit
    print(f"⚔️ {player['name']} hits {enemy['name']} for {player_hit} damage!")
    
    # A quick check to see if the enemy died from this hit
    if enemy['health'] <= 0:
        break # Breaks out of the while loop immediately if the enemy is defeated.
        
    # 2. Enemy's Turn
   
    enemy_hit = calculate_damage(enemy['attack_power']) 
    # We subtract the random damage amount stored in 'enemy_hit'
    player['health'] = player['health'] - enemy_hit 
    print(f"🤕 {enemy['name']} retaliates, hitting {player['name']} for {enemy_hit} damage!")
    
    # 3. Status Update
    print(f"\nSTATUS: {player['name']} HP: {player['health']} | {enemy['name']} HP: {enemy['health']}\n")


# --- 5. DECISION RECIPE (IF/ELIF/ELSE - Win/Loss Check) ---

# This is where the game will land after the loop breaks. We check who survived.
if player['health'] > 0:
    print("✨🏆 VICTORY! You defeated the enemy! 🏆✨")
else:
    print("💀 GAME OVER! You have been defeated. 💀")
    

