# Inventory Manager: Uses nested dictionaries for item tracking

# --- 1. DATA STORAGE RECIPE (Nested Dictionary) ---
# Outer key: Item Name (String)
# Inner value: Dictionary of properties (quantity, weight, description)
inventory = {
    "Iron Sword": {
        "quantity": 1, 
        "weight": 5.5, 
        "description": "A sturdy, basic sword."
    },
    "Healing Potion": {
        "quantity": 5, 
        "weight": 0.5, 
        "description": "Restores health on use."
    },
    "Gold Coin": {
        "quantity": 260, 
        "weight": 0.2, 
        "description": "The primary currency."
    },
    "Leather Boots": {
        "quantity": 2, 
        "weight": 0.7, 
        "description": "Lightweight and flexible footwear."
    }
}

# --- 2. CODE REUSABILITY RECIPES (Functions) ---

def display_inventory():
    print("\n--- CURRENT INVENTORY ---")
    total_weight = 0.0
    
    # Use a FOR loop to iterate through every item name (key) in the inventory
    for item_name in inventory:
        # Access the inner dictionary of properties (quantity, weight, etc.)
        item_props = inventory[item_name]
        
        # 1. Calculate the weight of all items of this type
        item_total_weight = item_props['quantity'] * item_props['weight'] 
        
        # 2. Add the item's total weight to the running total_weight
        total_weight = total_weight + item_total_weight
        
        # Print the formatted output for this item
        print(f"| {item_name:<15} | Qty: {item_props['quantity']:<3} | Total Wgt: {item_total_weight:^5.1f} |")
    
    print("-" * 40)
    print(f"Total Carry Weight: {total_weight:.1f} lbs")
    print("----------------------------------------\n")

# This function will add an item to the inventory
def add_item(item, quantity, weight, description=""):
    # --- DECISION RECIPE: IF BLOCK ---
    # Check if the item name already exists as a key in the inventory dictionary
    if item in inventory:
        # If it exists, just update its quantity
        inventory[item]['quantity'] += quantity
        print(f"➕ Added {quantity} x {item}. New quantity: {inventory[item]['quantity']}\n")
    
    # --- DECISION RECIPE: ELSE BLOCK ---
    else:
        # If it's a new item, add the full set of properties to the inventory
        # The key is the item name, and the value is the new item's property dictionary
        inventory[item] = {
            "quantity": quantity,
            "weight": weight,
            "description": description 
        }
        print(f"✨ New item added: {item} x {quantity}\n")


# This function will remove an item from the inventory
def remove_item(item, quantity):
    # 1. Check if the item exists in the inventory at all
    if item in inventory:
        current_qty = inventory[item]['quantity']
        
        # 2. Check if we are trying to remove a valid quantity
        if quantity < current_qty:
            # We are removing some, but not all of the item
            
           
            inventory[item]['quantity'] = current_qty - quantity 
            
            print(f"➖ Removed {quantity} x {item}. Remaining: {inventory[item]['quantity']}\n")

        elif quantity >= current_qty:
            # We are removing all or more than we have (which should delete the entry)
            
           
            del inventory[item]
            
            print(f"🔥 Removed all {item}s from inventory.\n")
        
        else:
            # This handles cases where quantity might be negative (though we assume positive input)
            print(f"❌ Cannot remove 0 or a negative quantity of {item}.\n")
            
    else:
        # Item doesn't exist
        print(f"⚠️ ERROR: {item} not found in inventory.\n")


# --- 3. MAIN APPLICATION LOOP (Test Calls) ---

# 1. Initial Inventory Display
display_inventory()

# 2. Test the add_item function
add_item("Healing Potion", 2, 0.5) # Case 1: Item already exists (quantity should go from 5 to 7)