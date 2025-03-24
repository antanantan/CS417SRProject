import pandas as pd
from database.db_models import db, Restaurant, Menu, MenuOptionGroup, MenuOptionItem, MenuOptionMapping

def style_heading(text: str) -> str:
    small_words = {"or", "the", "and", "of", "a", "an", "to", "in", "on", "at", "for", "but", "nor", "with", "by", "as", "up", "out", "off", "so", "yet", "not"}
    if not text:
        return ""
    words = text.lower().split()
    formatted_words = [words[0].capitalize()] + [
        word if word in small_words else word.capitalize() for word in words[1:]
    ]
    return " ".join(formatted_words) if text else ""

def style_main(text: str) -> str:
    return text.lower().capitalize() if text else ""

def seed_menus(file_path):
    """
    Read an Excel file and seed menus into the database.
    """
    try:
        # read Excel file
        xls = pd.ExcelFile(file_path)

        # read restaurants sheet
        df_restaurants = pd.read_excel(xls, sheet_name="restaurants", dtype=str)
        df_restaurants = df_restaurants.map(lambda x: x.lstrip("'") if isinstance(x, str) else x)

        # clear menu-related tables
        db.session.query(Menu).delete()
        db.session.query(MenuOptionGroup).delete()
        db.session.query(MenuOptionItem).delete()
        db.session.query(MenuOptionMapping).delete()
        db.session.flush()
        print("🗑️ Menu-related tables cleared!")

        # process each restaurant
        for _, row in df_restaurants.iterrows():
            restaurant_name = row["name"]
            menu_sheet_name = row["menu_sheet_name"]
            
            # get restaurant from DB
            restaurant = db.session.query(Restaurant).filter_by(
                name=restaurant_name,
                address=row["address"], zipcode=row["zipcode"]
            ).first()
            if not restaurant:
                raise ValueError(f"Restaurant '{restaurant_name}' not found in DB.")

            # read menu sheet
            if menu_sheet_name not in xls.sheet_names:
                raise ValueError(f"Sheet '{menu_sheet_name}' not found in Excel.")

            df_menu = pd.read_excel(xls, sheet_name=menu_sheet_name, dtype=str)
            df_menu = df_menu.map(lambda x: x.lstrip("'") if isinstance(x, str) else x)

            # variables to keep track of category, sub_category, and option_group_id
            last_category, last_sub_category, last_option_group_id = None, None, None

            for _, menu_row in df_menu.iterrows():
                # process category and sub_category
                if pd.notna(menu_row["category"]):
                    category = menu_row["category"]
                    last_sub_category = None
                else:
                    category = last_category
                sub_category = menu_row["sub_category"] if pd.notna(menu_row["sub_category"]) else last_sub_category
                last_category, last_sub_category = category, sub_category

                # if name of menu item is provided, save it to DB
                if pd.notna(menu_row["name"]):
                    new_menu = Menu(
                        restaurant_id=restaurant.id,
                        category=style_heading(category),
                        sub_category=style_heading(sub_category),
                        name=style_heading(menu_row["name"]),
                        price=float(menu_row["price"]) if pd.notna(menu_row["price"]) else 0.0,
                        ingredients=style_main(menu_row["ingredients"]) if pd.notna(menu_row["ingredients"]) else None,
                        allergens=style_heading(menu_row["allergens"]) if pd.notna(menu_row["allergens"]) else None,
                        description=style_main(menu_row["description"]) if pd.notna(menu_row["description"]) else None,
                        image_filename=f"{menu_sheet_name}/{menu_row["image_filename"]}" if pd.notna(menu_row["image_filename"]) else None
                    )
                    db.session.add(new_menu)
                    db.session.flush() # flush to get the id of the new menu

                # process option groups
                # if option_group_description is provided   
                if pd.notna(menu_row["option_group_description"]):
                    # create reference_key for option_group (menu_sheet_name+'_'+option_group_id)
                    reference_key = f"{menu_sheet_name}_{menu_row['option_group_id']}" if pd.notna(menu_row["option_group_id"]) else None

                    # check if option group already exists
                    existing_option_group = db.session.query(MenuOptionGroup).filter_by(reference_key=reference_key).first()

                    if existing_option_group:
                        option_group_ids = [existing_option_group.id]
                    else:
                        if not pd.notna(menu_row["option_min_quantity"]) or not pd.notna(menu_row["option_max_quantity"]):
                            raise ValueError(f"Missing option_min_quantity or option_max_quantity.")

                        # make new option group
                        new_option_group = MenuOptionGroup(
                            reference_key=reference_key,
                            description=style_main(menu_row["option_group_description"]),
                            min_quantity=int(menu_row["option_min_quantity"]),
                            max_quantity=int(menu_row["option_max_quantity"])
                        )
                        db.session.add(new_option_group)
                        db.session.flush()
                        option_group_ids = [new_option_group.id]

                # if option_group_id only is provided
                elif pd.notna(menu_row["option_group_id"]):
                    option_group_ids = [int(id.strip()) for id in str(menu_row["option_group_id"]).split(',')]

                    # if option_group_id provided is not valid
                    if not option_group_ids:
                        raise ValueError(f"Missing referenced option_group_id for menu item '{menu_row['name']}'")

                else:
                    # no option if no option_group_description or option_group_id
                    option_group_ids = []

                # save option group relationship to menu to DB
                for group_id in option_group_ids:
                    new_mapping = MenuOptionMapping(menu_id=new_menu.id, option_group_id=group_id)
                    db.session.add(new_mapping)

                # renew last_option_group_id
                if option_group_ids:
                    last_option_group_id = option_group_ids[-1]

                # process option items
                if pd.notna(menu_row["option_item_name"]):
                    new_option_item = MenuOptionItem(
                        group_id=last_option_group_id,
                        name=style_main(menu_row["option_item_name"]),
                        extra_price=float(menu_row["extra_price"]) if pd.notna(menu_row["extra_price"]) else 0.0,
                        allergens=style_heading(menu_row["option_allergens"]) if pd.notna(menu_row["option_allergens"]) else None
                    )
                    db.session.add(new_option_item)

        # commit changes
        db.session.commit()
        print("✅ Menus inserted successfully!")

    except Exception as e:
        db.session.rollback()
        print(f"❌ Error seeding menu: {e}")
