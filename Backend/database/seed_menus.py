from database.db_models import db, Menu, Restaurant, MenuOptionGroup, MenuOptionItem, MenuOptionMapping

def seed_menus():
    """
    Seed menu items linked to restaurants.
    """
    try:
        # JP's Diner を取得
        restaurant_jps = Restaurant.query.filter_by(name="JP's Diner").first()

        if not restaurant_jps:
            print("❌ Error: JP's Diner not found. Please seed restaurants first!")
            return

        # メニュー項目の作成
        tea_latte = Menu.query.filter_by(name="Tea Latte", restaurant_id=restaurant_jps.id).first()
        if not tea_latte:
            tea_latte = Menu(
                name="Tea Latte",
                category="Drinks",
                sub_category="Hot Beverages",
                price=4.50,
                ingredients="Tea, Milk",
                allergens="Milk",
                description="A warm and comforting tea latte with your choice of milk.",
                restaurant_id=restaurant_jps.id
            )
            db.session.add(tea_latte)
            db.session.flush()  # ID を取得するため

        # Milk オプショングループの作成
        milk_option_group = MenuOptionGroup.query.filter_by(name="Milk").first()
        if not milk_option_group:
            milk_option_group = MenuOptionGroup(name="Milk")
            db.session.add(milk_option_group)
            db.session.flush()  # ID を取得するため

        # Milk のオプションアイテム作成
        milk_options = [
            {"name": "Whole Milk", "extra_price": 0.00},
            {"name": "0% Milk", "extra_price": 0.00},
            {"name": "2% Milk", "extra_price": 0.00}
        ]

        for option in milk_options:
            option_item = MenuOptionItem.query.filter_by(name=option["name"], group_id=milk_option_group.id).first()
            if not option_item:
                option_item = MenuOptionItem(name=option["name"], extra_price=option["extra_price"], group_id=milk_option_group.id)
                db.session.add(option_item)
                db.session.flush()

        # メニューとオプショングループの関連付け
        mapping = MenuOptionMapping.query.filter_by(menu_id=tea_latte.id, option_group_id=milk_option_group.id).first()
        if not mapping:
            mapping = MenuOptionMapping(menu_id=tea_latte.id, option_group_id=milk_option_group.id)
            db.session.add(mapping)

        db.session.commit()
        print("✅ Tea Latte with Milk options added successfully!")

    except Exception as e:
        db.session.rollback()
        print(f"❌ Error seeding menu: {e}")
