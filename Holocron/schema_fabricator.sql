-- schema_fabricator.sql
-- The Fabricator: Multi-Alt Crafting Dependency Graph

CREATE SCHEMA IF NOT EXISTS fabricator;

-- Recipes: Master list of all known recipes
CREATE TABLE IF NOT EXISTS fabricator.recipes (
    recipe_id INT PRIMARY KEY, -- Spell ID of the craft
    name VARCHAR(255) NOT NULL,
    profession VARCHAR(50), -- 'Alchemy', 'Blacksmithing', etc.
    crafted_item_id INT, -- The resulting item ID
    min_yield INT DEFAULT 1,
    max_yield INT DEFAULT 1,
    cooldown INT DEFAULT 0, -- Seconds (e.g., Transmutes)
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Reagents: What is needed for each recipe
CREATE TABLE IF NOT EXISTS fabricator.reagents (
    recipe_id INT REFERENCES fabricator.recipes(recipe_id),
    item_id INT NOT NULL,
    count INT NOT NULL,
    is_optional BOOLEAN DEFAULT FALSE, -- For finishing reagents
    PRIMARY KEY (recipe_id, item_id)
);

-- Character Recipes: Which character knows which recipe
CREATE TABLE IF NOT EXISTS fabricator.character_recipes (
    character_guid VARCHAR(255) REFERENCES holocron.characters(character_guid),
    recipe_id INT REFERENCES fabricator.recipes(recipe_id),
    skill_level INT, -- Current skill in this profession
    PRIMARY KEY (character_guid, recipe_id)
);

-- Work Orders: Requests for crafting
CREATE TABLE IF NOT EXISTS fabricator.work_orders (
    order_id SERIAL PRIMARY KEY,
    target_item_id INT NOT NULL,
    quantity INT NOT NULL,
    status VARCHAR(50) DEFAULT 'PENDING', -- 'PENDING', 'IN_PROGRESS', 'COMPLETED'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Work Order Steps: The dependency chain
CREATE TABLE IF NOT EXISTS fabricator.work_order_steps (
    step_id SERIAL PRIMARY KEY,
    order_id INT REFERENCES fabricator.work_orders(order_id),
    step_order INT NOT NULL, -- 1, 2, 3...
    character_guid VARCHAR(255), -- Who needs to do this
    action VARCHAR(50) NOT NULL, -- 'CRAFT', 'BUY', 'MAIL'
    item_id INT NOT NULL,
    quantity INT NOT NULL,
    recipe_id INT, -- If crafting
    status VARCHAR(50) DEFAULT 'PENDING'
);
