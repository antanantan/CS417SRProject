from database.db_models import db, Restaurant

def seed_restaurants():
    """
    Seed restaurants.
    """
    try:
        db.session.query(Restaurant).delete()
        db.session.flush()
        print("🗑️ Restaurant table cleared!")

        restaurants = [
            {"name": "JP's Diner", "address": "5151 Park Ave, Fairfield, CT 06825", "zipcode": "06825", "latitude": 41.221084063951835, "longitude": -73.2458533422555, "phone": "+12033966540", "category": "Diner", "price_range": "$", "image_filename": None},
            {"name": "63's", "address": "5151 Park Ave, Fairfield, CT 06825", "zipcode": "06825", "latitude": 41.221324131985746, "longitude": -73.2417259529118, "phone": None, "category": "Self service restaurant", "price_range": "$", "image_filename": None}
        ]

        for restaurant in restaurants:
            new_restaurant = Restaurant(
                name=restaurant["name"],
                address=restaurant["address"],
                zipcode=restaurant["zipcode"],
                latitude=restaurant["latitude"],
                longitude=restaurant["longitude"],
                phone=restaurant["phone"],
                category=restaurant["category"],
                price_range=restaurant["price_range"],
                image_filename=restaurant["image_filename"]
            )
            db.session.add(new_restaurant)

        db.session.commit()
        print("✅ Restaurants inserted successfully!")

    except Exception as e:
        db.session.rollback()
        print(f"❌ Error seeding restaurants: {e}")