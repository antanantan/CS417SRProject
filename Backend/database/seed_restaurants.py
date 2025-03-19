import json
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
            {"name": "JP's Diner", "address": "5151 Park Ave, Fairfield, CT 06825", "zipcode": "06825", "latitude": 41.221084063951835, "longitude": -73.2458533422555, "phone": "+12033966540", "category": "Diner", "price_range": "$", "image_filename": "jpsdiner.jpg",
            "hours": json.dumps({
                "Monday": "Closed",
                "Tuesday": "10:00 AM - 10:00 PM",
                "Wednesday": "10:00 AM - 10:00 PM",
                "Thursday": "10:00 AM - 12:00 AM",
                "Friday": "10:00 AM - 12:00 AM",
                "Saturday": "10:00 AM - 6:00 PM",
                "Sunday": "10:00 AM - 6:00 PM"
            })},
            {"name": "63's", "address": "5151 Park Ave, Fairfield, CT 06825", "zipcode": "06825", "latitude": 41.221324131985746, "longitude": -73.2417259529118, "phone": None, "category": "Self service restaurant", "price_range": "$", "image_filename": None},
# beginning of new items
            {"name": "Linda's", "address": "5151 Park Ave, Fairfield, CT 06825", "zipcode": "06825", "latitude": 41.220993050671055, "longitude": -73.24309661708993, "phone": None, "category": "Self service restaurant", "price_range": "$", "image_filename": None},
            {"name": "Texas Roadhouse", "address": "524 Saw Mill Rd, West Haven, CT 06516", "zipcode": "06516", "latitude": 41.26876626494863, "longitude": -72.97658457647321, "phone": "+12039376222", "category": "Dine-in restaurant", "price_range": "$", "image_filename": None},
            {"name": "Bonchon", "address": "170 College St, New Haven, CT 06510", "zipcode": "06510", "latitude": 41.35852219585518, "longitude": -72.92732000662564, "phone": "+12035072159", "category": "Dine-in restaurant", "price_range": "$$", "image_filename": None},
            {"name": "Pret A Manger", "address": "4 Bryant Pk, New York, NY 10018", "zipcode": "10018", "latitude": 40.75412660177139, "longitude": -73.98523105085792, "phone": "+16464102071", "category": "Self service restaurant", "price_range": "$", "image_filename": None},
            {"name": "Gusto Trattoria", "address": "255 Boston Post Rd, Milford, CT 06460", "zipcode": "06460", "latitude": 41.22202654726118, "longitude": -73.07294690359569, "phone": "+12038767464", "category": "Dine-in restaurant", "price_range": "$$$", "image_filename": None},
            {"name": "Mecha Noodle Bar", "address": "1215 Post Rd, Fairfield, CT 06824", "zipcode": "06824", "latitude": 41.14315588504152, "longitude": -73.25367464777568, "phone": "+12032928222", "category": "Dine-in restaurant", "price_range": "$$$", "image_filename": None},
            {"name": "Colony Grill", "address": "1520 Post Rd, Fairfield, CT 06824", "zipcode": "06824", "latitude": 41.14146723874369, "longitude": -73.25834169111461, "phone": "+12032591989", "category": "Dine-in restaurant", "price_range": "$$", "image_filename": None},
            {"name": "Colony Grill", "address": "36 Broad St, Milford, CT 06460", "zipcode": "06460", "latitude": 41.221875168272504, "longitude": -73.05747449194841, "phone": "+12038761935", "category": "Dine-in restaurant", "price_range": "$$", "image_filename": None}
        ]

        for restaurant in restaurants:
            new_restaurant = Restaurant(
                name=restaurant["name"],
                address=restaurant["address"],
                zipcode=restaurant["zipcode"],
                latitude=restaurant["latitude"],
                longitude=restaurant["longitude"],
                phone=restaurant["phone"] if restaurant.get("phone") else None,
                category=restaurant["category"] if restaurant.get("category") else None,
                price_range=restaurant["price_range"] if restaurant.get("price_range") else None,
                image_filename=restaurant["image_filename"] if restaurant.get("image_filename") else None,
                hours=json.dumps(restaurant["hours"]) if restaurant.get("hours") else None,
            )
            db.session.add(new_restaurant)

        db.session.commit()
        print("✅ Restaurants inserted successfully!")

    except Exception as e:
        db.session.rollback()
        print(f"❌ Error seeding restaurants: {e}")