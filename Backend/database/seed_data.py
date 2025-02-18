from database.db_models import db
from database.seed_allergens import seed_allergens
from database.seed_menus import seed_menus
from database.seed_restaurants import seed_restaurants

def seed_db():
    """
    Seed the database with initial data for allergens, restaurants, and menus.
    """
    try:
        seed_allergens()  
        seed_restaurants()  
        # seed_menus()

        print("✅ Database seeded successfully!")

    except Exception as e:
        db.session.rollback()
        print(f"❌ Error seeding database: {e}")

    finally:
        db.session.close() 