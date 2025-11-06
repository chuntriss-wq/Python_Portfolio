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

// --- DOM Elements (References to HTML elements) ---
const playerStatsDiv = document.getElementById('player-stats');
const enemyStatsDiv = document.getElementById('enemy-stats');
const battleLog = document.getElementById('battle-log');
const attackButton = document.getElementById('attack-button');

// --- 2. CODE REUSABILITY (Function) ---
function calculateDamage(maxPower) {
    // Math.random gives a number between 0 and 1.
    // Math.floor rounds down to a whole number.
    // Damage is between 5 and maxPower (inclusive).
    return Math.floor(Math.random() * (maxPower - 5 + 1)) + 5;
}

// --- 3. GAME FUNCTIONS ---

// Function to update the visible stats on the page
function updateStats() {
    playerStatsDiv.innerHTML = `
        <h2>${player.name}</h2>
        <p>❤️ HP: **${player.health}**</p>
        <p>⚔️ Max Attack: ${player.attack_power}</p>
    `;

    enemyStatsDiv.innerHTML = `
        <h2>${enemy.name}</h2>
        <p>❤️ HP: **${enemy.health}**</p>
        <p>⚔️ Max Attack: ${enemy.attack_power}</p>
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
    const playerHit = calculateDamage(player.attack_power);
    enemy.health -= playerHit;
    logMessage(`⚔️ **${player.name}** hits **${enemy.name}** for **${playerHit}** damage!`);

    // --- Win/Loss Check (after player's turn) ---
    if (enemy.health <= 0) {
        enemy.health = 0; // Prevent negative HP display
        updateStats();
        logMessage("✨🏆 **VICTORY!** You defeated the enemy! 🏆✨");
        attackButton.disabled = true;
        return;
    }

    // --- Enemy's Turn ---
    const enemyHit = calculateDamage(enemy.attack_power);
    player.health -= enemyHit;
    logMessage(`🤕 **${enemy.name}** retaliates, hitting **${player.name}** for **${enemyHit}** damage!`);

    // --- Win/Loss Check (after enemy's turn) ---
    if (player.health <= 0) {
        player.health = 0; // Prevent negative HP display
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