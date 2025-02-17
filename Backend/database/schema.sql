-- User information
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL
);

-- Allergen groups (in general)
CREATE TABLE IF NOT EXISTS allergen_groups (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL -- eg: "Tree Nuts", "Dairy"
);

-- Allergens (in detail)
CREATE TABLE IF NOT EXISTS allergens (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    group_id INTEGER NOT NULL,
    name TEXT UNIQUE NOT NULL, -- eg: "Almond", "Milk"
    FOREIGN KEY (group_id) REFERENCES allergen_groups(id) ON DELETE CASCADE
);

-- User's allergy information
CREATE TABLE IF NOT EXISTS user_allergies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    allergen_id INTEGER NOT NULL,
    scale INTEGER NOT NULL, -- 0: Intolerance, 1: Mild, 2: Moderate, 3: Severe
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (allergen_id) REFERENCES allergens(id) ON DELETE CASCADE
);

-- Restaurant information
CREATE TABLE IF NOT EXISTS restaurants (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    address TEXT NOT NULL,
    zipcode INTEGER NOT NULL,
    lattitude REAL NOT NULL,
    longitude REAL NOT NULL,
    phone TEXT NOT NULL,
    category TEXT NOT NULL,
    price_range TEXT NOT NULL,
    image_filename TEXT
);

-- Menu information
CREATE TABLE IF NOT EXISTS menus (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    store_id INTEGER NOT NULL,
    category TEXT NOT NULL,
    name TEXT NOT NULL,
    price REAL NOT NULL,
    ingredients TEXT NOT NULL,
    allergens TEXT,
    description TEXT,
    image_filename TEXT,
    FOREIGN KEY (store_id) REFERENCES stores(id) ON DELETE CASCADE
);

-- Menu options
CREATE TABLE IF NOT EXISTS menu_options (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    extra_price REAL NOT NULL
);

-- ORM table for menu options
CREATE TABLE IF NOT EXISTS menu_option_mapping (
    menu_id INTEGER NOT NULL,
    option_id INTEGER NOT NULL,
    FOREIGN KEY (menu_id) REFERENCES menus(id) ON DELETE CASCADE,
    FOREIGN KEY (option_id) REFERENCES menu_options(id) ON DELETE CASCADE
);