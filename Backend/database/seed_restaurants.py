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
            {"name": "63's", "address": "5151 Park Ave, Fairfield, CT 06825", "zipcode": "06825", "latitude": 41.221324131985746, "longitude": -73.2417259529118, "phone": None, "category": "Self service restaurant", "price_range": "$", "image_filename": None},
            {"name": "Texas Roadhouse", "address": "524 Saw Mill Rd, West Haven, CT 06516", "zipcode": "06516", "latitude": 41.26876626494863, "longitude": -72.97658457647321, "phone": "+12039376222", "category": "Dine-in restaurant", "price_range": "$", "image_filename": None},
            {"name": "Bonchon", "address": "170 College St, New Haven, CT 06510", "zipcode": "06510", "latitude": 41.35852219585518, "longitude": -72.92732000662564, "phone": "+12035072159", "category": "Dine-in restaurant", "price_range": "$$", "image_filename": None},
            {"name": "Pret A Manger", "address": "4 Bryant Pk, New York, NY 10018", "zipcode": "10018", "latitude": 40.75412660177139, "longitude": -73.98523105085792, "phone": "+16464102071", "category": "Self service restaurant", "price_range": "$", "image_filename": None}
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