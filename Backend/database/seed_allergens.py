from database.db_models import db, AllergenGroup, Allergen

def seed_allergens():
    """
    Seed allergen groups and allergens.
    """
    try:
        # clear existing data
        db.session.query(Allergen).delete()
        db.session.query(AllergenGroup).delete()
        db.session.flush()
        print("🗑️ Allergen table cleared!")

        # insert new data
        allergen_groups = {
            "Milk": [],
            "Eggs": [],
            "Fish": ["Tilapia", "Salmon", "Cod", "Trout", "Tuna"],
            "Crustacean Shellfish": ["Shrimp", "Crab", "Lobster"],
            "Tree Nuts": ["Almonds", "Brazil Nuts", "Cashews", "Chestnuts", "Hazelnuts", "Macadamia Nuts", "Pecans", "Pistachios", "Walnuts"],
            "Peanuts": [],
            "Wheat": [],
            "Soybeans": [],
            "Sesame": [],
            "Fruits": ["Apple", "Avocado", "Banana", "Cherry", "Kiwi", "Melon", "Peach", "Pear", "Pinapple", "Plum", "Strawberry", "Watermelon"],
            "Mustard": [],
            "Celery": [],
            "Garlic": [],
            "Buckwheat": []
        }

        for group_name, allergen_list in allergen_groups.items():
            group = AllergenGroup.query.filter_by(name=group_name).first()
            if not group:
                group = AllergenGroup(name=group_name)
                db.session.add(group)
                db.session.flush()

            # if allergen_list is empty, use group_name as allergen name
            if not allergen_list:
                allergen_list = [group_name]

            for allergen_name in allergen_list:
                allergen = Allergen.query.filter_by(name=allergen_name).first()
                if not allergen:
                    allergen = Allergen(name=allergen_name, group_id=group.id)
                    db.session.add(allergen)

        db.session.commit()
        print("✅ Allergens updated successfully!")

    except Exception as e:
        db.session.rollback()
        print(f"❌ Error seeding allergens: {e}")