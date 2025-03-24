import json
import pandas as pd
from database.db_models import db, Restaurant

def seed_restaurants(file_path):
    """
    Read an Excel file and seed restaurants into the database.
    """
    try:
        # read Excel file
        df = pd.read_excel(file_path, sheet_name="restaurants", dtype=str)
        
        # delete ' from the beginning of the string if applicable
        df = df.map(lambda x: x.lstrip("'") if isinstance(x, str) else x)

        # clear restaurant table
        db.session.query(Restaurant).delete()
        db.session.flush()
        print("🗑️ Restaurant table cleared!")

        # add restaurants to DB
        for _, row in df.iterrows():
            # if cell is empty, set it to None
            name = row["name"]
            category = row["category"] if pd.notna(row["category"]) else None
            price_range = row["price_range"] if pd.notna(row["price_range"]) else None
            address = row["address"]
            zipcode = row["zipcode"]
            phone = row["phone"] if pd.notna(row["phone"]) else None
            image_filename = row["image_filename"] if pd.notna(row["image_filename"]) else None
            
            # convert latitude and longitude to float
            if pd.notna(row["lattitude"]):
                latitude = float(row["lattitude"])
            else:
                raise ValueError(f"Invalid latitude value: {row['lattitude']}")
            if pd.notna(row["longtitude"]):
                longitude = float(row["longtitude"])
            else:
                raise ValueError(f"Invalid longitude value: {row['longtitude']}")

            # column names for days of the week
            days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]

            # save opening hours as a dictionary (if empty, set to "Closed")
            hours = {day.capitalize(): row[day] if pd.notna(row[day]) else "Closed" for day in days}

            # if all values are "Closed", set hours to None
            if all(value == "Closed" for value in hours.values()):
                hours = None

            new_restaurant = Restaurant(
                name=name,
                category=category,
                price_range=price_range,
                address=address,
                zipcode=zipcode,
                latitude=latitude,
                longitude=longitude,
                phone=phone,
                image_filename=image_filename,
                hours=json.dumps(hours)
            )
            db.session.add(new_restaurant)

        # commit changes
        db.session.commit()
        print("✅ Restaurants inserted successfully!")

    except Exception as e:
        db.session.rollback()
        print(f"❌ Error seeding restaurants: {e}")
