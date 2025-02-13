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
        {"name": "Grilled Salmon", "price": 14.99, "ingredients": "Salmon, Lemon, Herbs", "allergens": "Fish", "restaurant_id": restaurant_2.id},
        {"name": "Peanut Butter Sandwich", "price": 5.99, "ingredients": "Peanut Butter, Bread", "allergens": "Peanuts, Wheat", "restaurant_id": restaurant_1.id}
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