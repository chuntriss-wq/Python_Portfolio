// --- 1. DATA STORAGE (Objects) ---
const player = {
    name: "The Champion",
    health: 100,
    attack_power: 15
};

const enemy = {
    name: "chris_lionheart",
    health: 200,
    attack_power: 10
};
const MIN_DAMAGE = 5;

// --- DOM Elements (References to HTML elements) ---
const playerStatsDiv = document.getElementById('player-stats');
const enemyStatsDiv = document.getElementById('enemy-stats');
const battleLog = document.getElementById('battle-log');
const attackButton = document.getElementById('attack-button');

// --- 2. CODE REUSABILITY (Function) ---
function calculateDamage(maxPower) {
    const MIN_DAMAGE = 5;
    // Base damage calculation remains the same
    let damage = Math.floor(Math.random() * (maxPower - MIN_DAMAGE + 1)) + MIN_DAMAGE;

    // New: Critical Hit Logic (e.g., 15% chance)
    const CRIT_CHANCE = 0.15; // 15%
    if (Math.random() < CRIT_CHANCE) {
        damage *= 2; // Double the damage
        return { damage: damage, isCrit: true }; // Return an object
    }

    return { damage: damage, isCrit: false }; // Return an object
}
// --- 3. GAME FUNCTIONS ---

// Function to update the visible stats on the page
function updateStats() {
    playerStatsDiv.innerHTML = `
        <div class="stats">
            <h2>Player Stats</h2>
            <h3>${player.name}</h3>
            <p>❤️ HP: <strong>${player.health}</strong></p>
            <p>⚔️ Max Attack: ${player.attack_power}</p>
        </div>
    `;

    enemyStatsDiv.innerHTML = `
        <div class="stats">
            <h3>${enemy.name}</h3>
            <p>❤️ HP: <strong>${enemy.health}</strong></p>
            <p>⚔️ Max Attack: ${enemy.attack_power}</p>
        </div>
    `;
}

// Function to add a message to the battle log
function logMessage(message) {
    // We add the new message to the top (prepend)
    const p = document.createElement('p');
    p.innerHTML = message;
    battleLog.prepend(p);
}

// The main battle function, triggered by the button click

function handleAttack() {
    if (player.health <= 0 || enemy.health <= 0) {
        logMessage("The battle is over!");
        attackButton.disabled = true;
        return; // Stop the function if the game is already over
    }

    // --- Player's Turn ---
    const playerHitResult = calculateDamage(player.attack_power); // Result is { damage: X, isCrit: Y }
    const playerDamage = playerHitResult.damage; // Extract the actual damage number
    
    enemy.health -= playerDamage; // ✅ FIX 1: Subtract the damage number
    
    const playerLog = playerHitResult.isCrit ? 
        `💥 CRITICAL HIT! 💥 **${player.name}** hits **${enemy.name}** for **${playerDamage}** damage!` :
        `⚔️ **${player.name}** hits **${enemy.name}** for **${playerDamage}** damage!`;
    logMessage(playerLog);

    // --- Win/Loss Check (after player's turn) ---
    if (enemy.health <= 0) {
        enemy.health = 0;
        updateStats();
        logMessage("✨🏆 **VICTORY!** You defeated the enemy! 🏆✨");
        attackButton.disabled = true;
        return;
    }

    // --- Enemy's Turn ---
    const enemyHitResult = calculateDamage(enemy.attack_power); // Result is { damage: X, isCrit: Y }
    const enemyDamage = enemyHitResult.damage; // Extract the actual damage number
    
    player.health -= enemyDamage; // ✅ FIX 2: Subtract the damage number
    
    const enemyLog = enemyHitResult.isCrit ?
        `💥 CRITICAL HIT! 💥 🤕 **${enemy.name}** retaliates, hitting **${player.name}** for **${enemyDamage}** damage!` :
        `🤕 **${enemy.name}** retaliates, hitting **${player.name}** for **${enemyDamage}** damage!`;
    logMessage(enemyLog);

    // --- Win/Loss Check (after enemy's turn) ---
    if (player.health <= 0) {
        player.health = 0;
        updateStats();
        logMessage("💀 **GAME OVER!** You have been defeated. 💀");
        attackButton.disabled = true;
    }

    // Update the visual stats after the turn
    updateStats();
}

// --- 4. GAME START ---
// Set up the initial button listener and game state
attackButton.addEventListener('click', handleAttack);
updateStats(); // Display initial health
logMessage(`A wild **${enemy.name}** appears! Get ready to fight!`);
logMessage(`You (**${player.name}**) have **${player.health}** HP.`);

// Play Again button
const playAgainButton = document.getElementById('play-again-button');
playAgainButton.addEventListener('click', () => {
    // 1. Clear the battle log for a fresh start
    battleLog.innerHTML = ''; 
    
    // 2. Reset player and enemy stats
    player.health = 100;
    enemy.health = 200;
    
    // 3. Re-enable the attack button
    attackButton.disabled = false;
    
    // 4. Update the visual stats and log the start message
    updateStats();
    logMessage(`A wild **${enemy.name}** appears! Get ready to fight!`);
    logMessage(`You (**${player.name}**) have **${player.health}** HP.`);
});