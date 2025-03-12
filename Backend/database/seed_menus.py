from database.db_models import db, Menu, Restaurant

def seed_menus():
    """
    Seed menu items linked to restaurants.
    """
    restaurant_1 = Restaurant.query.filter_by(name="Healthy Bites").first()
    restaurant_2 = Restaurant.query.filter_by(name="Seafood Delight").first()

    if not restaurant_1 or not restaurant_2:
        print("Error: Restaurants not found. Please seed restaurants first!")
        return

    menu_items = [
        {"name": "Vegan Salad", "price": 9.99, "ingredients": "Lettuce, Tomato, Avocado", "allergens": "", "restaurant_id": restaurant_1.id},
        {"name": "Chocolate Chip Pancakes", "price": 12.99, "ingredients": "Egg, Milk, Wheat, Chocolate", "allergens": "Wheat, Egg, Dairy", "restaurant_id": restaurant_1.id},
        {"name": "Nutella Milkshake", "price": 8.99, "ingredients": "Milk, Sugar, Chocolate, Hazelnut", "allergens": "Hazelnut, Dairy", "restaurant_id": restaurant_1.id},
        {"name": "Peanut Butter Sandwich", "price": 5.99, "ingredients": "Peanut Butter, Bread", "allergens": "Peanuts, Wheat", "restaurant_id": restaurant_1.id},
        {"name": "Grilled Salmon", "price": 14.99, "ingredients": "Salmon, Lemon, Herbs", "allergens": "Fish", "restaurant_id": restaurant_2.id},
        {"name": "California Rolls", "price": 9.99, "ingredients": "Avocado, Imitation Crab, Cucumber, Rice, Nori", "allergens": "Fish, Gluten", "restaurant_id": restaurant_3.id},
        {"name": "Chicken Tenders and Fries", "price": 8.99, "ingredients": "Chicken, Flour, Potatoes, Salt", "allergens": "Gluten, Milk, Soy, Eggs", "restaurant_id": restaurant_3.id},
        {"name": "Sirloin & Ribs", "price": 23.99, "ingredients": "Pork, Steak, BBQ Sauce, Sweet Potato", "allergens": "", "restaurant_id": restaurant_4.id},
        {"name": "Cactus Blossom", "price": 15.99, "ingredients": "Flour, Milk, Egg, Onions", "allergens": "Peanuts, Gluten, Dairy, Eggs", "restaurant_id": restaurant_4.id},
        {"name": "Pork Belly Buns", "price": 15.99, "ingredients": "Eggs, Wheat, Soy, Pork, Sesame", "allergens": "Peanuts, Tree Nuts, Gluten, Soy, Eggs, Sesame", "restaurant_id": restaurant_5.id},
        {"name": "Popcorn Shrimp", "price": 13.99, "ingredients": "Shrimp, Milk, Eggs, Wheat, Sesame", "allergens": "Gluten, Soy, Fish, Eggs, Sesame", "restaurant_id": restaurant_5.id},
        {"name": "Korean Cheese Corn", "price": 4.99, "ingredients": "Corn, Cheese, Eggs, Wheat", "allergens": "Gluten, Eggs, Dairy", "restaurant_id": restaurant_5.id},
        {"name": "Classic Mac & Cheese", "price": 10.99, "ingredients": "Wheat, Cheese, Egg", "allergens": " Gluten, Eggs, Dairy", "restaurant_id": restaurant_6.id},
        {"name": "Crunchy Miso Mushroom Wrap", "price": 10.99, "ingredients": "Mushroom, Carrots, Avocado, Cabbage, Lettuce, Tortilla", "allergens": " Wheat, Sesame, Soy", "restaurant_id": restaurant_6.id},
        {"name": "Roasted Veggie Harvest Soup", "price": 10.99, "ingredients": "Zucchini, Potato, Sweet Potato, Cabbage, Carrots, Celery, Pepper, Onions, Garlic", "allergens": "", "restaurant_id": restaurant_6.id},
        {"name": "Fresh Burrata and Beefsteak Tomatoes", "price": 14.95, "ingredients": "Tomato, Beef, Cheese, Balsamic Vinegar, Arugula", "allergens": " Wheat, Dairy", "restaurant_id": restaurant_7.id},
        {"name": "Pizza Scampi", "price": 16.95, "ingredients": "Shrimp, Tomato, Cheese, Garlic, Cheese, Wheat, Egg", "allergens": " Wheat, Dairy, Eggs, Fish", "restaurant_id": restaurant_7.id},
        {"name": "Tofu Hand Rolls", "price": 10.99, "ingredients": "Tofu, Chili Pesto, Rice, Sesame Seeds, Nori", "allergens": "Fish, Soy, Gluten, Sesame", "restaurant_id": restaurant_8.id},
        {"name": "Shoyu Paitan", "price": 14.99, "ingredients": "Chicken Broth, Shoyu Tare, Tonkotsu Noodles, Chicken, Scallions, Garlic Oil, Nori", "allergens": "Egg, Fish, Soy, Gluten", "restaurant_id": restaurant_8.id},
        {"name": "Spicy Miso", "price": 14.99, "ingredients": "Chicken Broth, Red Miso, Chili Oil, Tonkusen Noodles, Chashu, Mushrooms, Scallions", "allergens": "Egg, Sesame, Soy, Gluten", "restaurant_id": restaurant_8.id},
        {"name": "Cheese Pizza", "price": 12.99, "ingredients": "Wheat, Tomato, Cheese", "allergens": "Gluten, Dairy, Tomato", "restaurant_id": restaurant_9.id},
        {"name": "Anchovy Pizza", "price": 12.99, "ingredients": "Wheat, Tomato, Cheese, Anchovy", "allergens": "Gluten, Dairy, Tomato, Fish", "restaurant_id": restaurant_9.id},
        {"name": "Cheese Pizza", "price": 12.99, "ingredients": "Wheat, Tomato, Cheese", "allergens": "Gluten, Dairy, Tomato", "restaurant_id": restaurant_10.id},
        {"name": "Anchovy Pizza", "price": 12.99, "ingredients": "Wheat, Tomato, Cheese, Anchovy", "allergens": "Gluten, Dairy, Tomato, Fish", "restaurant_id": restaurant_10.id}
    ]

    for item in menu_items:
        menu = Menu.query.filter_by(name=item["name"]).first()
        if not menu:
            menu = Menu(
                name=item["name"],
                price=item["price"],
                ingredients=item["ingredients"],
                allergens=item["allergens"],
                restaurant_id=item["restaurant_id"]
            )
            db.session.add(menu)

    db.session.commit()
    print("Menu items inserted successfully!")