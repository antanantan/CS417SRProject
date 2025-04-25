import pandas as pd
from database.db_models import db, AllergenGroup, Allergen

def seed_allergens(file_path):
    """
    Seed allergen groups and allergens.
    """
    try:
        df_allergens = pd.read_excel(file_path, sheet_name="allergens", dtype=str)
        df_allergens = df_allergens.apply(lambda col: col.map(lambda x: x.lstrip("'").strip() if isinstance(x, str) else x))
        # clear existing data
        db.session.query(Allergen).delete()
        db.session.query(AllergenGroup).delete()
        db.session.flush()
        print("🗑️ Allergen tables cleared!")

        for _, row in df_allergens.iterrows():
            group_name    = row["allergen_group"]
            other_names = row.get("other_names", "")
            allergen_cell = row.get("allergen", "")
            group = AllergenGroup.query.filter_by(name=group_name).first()
            if not group:
                group = AllergenGroup(name=group_name)
                db.session.add(group)
                db.session.flush()
            
            if isinstance(other_names, str) and other_names.strip():
                group.other_names = other_names.strip()
            
            if pd.isna(allergen_cell) or not allergen_cell.strip():
                # if allergen_list is empty, use group_name as allergen name
                allergens_list = [group_name]
            else:
                allergens_list = [
                    a.strip() for a in allergen_cell.split(",") if a.strip()
                ]
            
            for allergen_name in allergens_list:
                exists = Allergen.query.filter_by(name=allergen_name).first()
                if not exists:
                    new_allergen = Allergen(
                        name=allergen_name,
                        group_id=group.id
                    )
                    db.session.add(new_allergen)

        # # insert new data
        # allergen_groups = {
        #     "Milk": [],
        #     "Eggs": [],
        #     "Fish": ["Tilapia", "Salmon", "Cod", "Trout", "Tuna", "Anchovy"],
        #     "Crustacean Shellfish": ["Shrimp", "Crab", "Lobster"],
        #     "Tree Nuts": ["Almonds", "Brazil Nuts", "Cashews", "Chestnuts", "Hazelnuts", "Macadamia Nuts", "Pecans", "Pistachios", "Walnuts", "Pine Nuts"],
        #     "Peanuts": [],
        #     "Wheat": [],
        #     "Soybeans": [],
        #     "Sesame": [],
        #     "Fruits": ["Apple", "Avocado", "Banana", "Cherry", "Kiwi", "Melon", "Peach", "Pear", "Pinapple", "Plum", "Strawberry", "Watermelon"],
        #     "Mustard": [],
        #     "Celery": [],
        #     "Garlic": [],
        #     "Buckwheat": [],
        #     "Coconut": []
        # }

        # for group_name, allergen_list in allergen_groups.items():
        #     group = AllergenGroup.query.filter_by(name=group_name).first()
        #     if not group:
        #         group = AllergenGroup(name=group_name)
        #         db.session.add(group)
        #         db.session.flush()

        #     # if allergen_list is empty, use group_name as allergen name
        #     if not allergen_list:
        #         allergen_list = [group_name]

        #     for allergen_name in allergen_list:
        #         allergen = Allergen.query.filter_by(name=allergen_name).first()
        #         if not allergen:
        #             allergen = Allergen(name=allergen_name, group_id=group.id)
        #             db.session.add(allergen)

        db.session.commit()
        print("✅ Allergens updated successfully!")

    except Exception as e:
        db.session.rollback()
        print(f"❌ Error seeding allergens: {e}")