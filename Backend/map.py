import folium
from geopy.geocoders import Nominatim
from flask import Flask, request, jsonify

# restricting it to the United States for now to keep our initial functionality small
def get_coordinates(zip_code, country='US'):
    geolocator = Nominatim(user_agent="map")
    location = geolocator.geocode(f"{zip_code}, {country}")
    if location:
        return location.latitude, location.longitude
    else:
        print("Invalid Zip Code.")
        return None
    

def create_map(zip_code):
    coordinates = get_coordinates(zip_code)
    if coordinates:
        latitude, longitude = coordinates
        m = folium.Map(location=[latitude, longitude], zoom_start=12)
        
        folium.Marker([latitude, longitude]).add_to(m)
        
        m.save("Frontend/src/assets/map.html")


zip_code = input("Enter a ZIP code: ")
create_map(zip_code)

# ref: https://realpython.com/python-folium-web-maps-from-data
# ref: https://www.google.com/search?q=insert+map+in+vue+using+folium&oq=insert+map+in+vue+using+folium&gs_lcrp=EgZjaHJvbWUyBggAEEUYOdIBCDQ0MDFqMGo3qAIAsAIA&sourceid=chrome&ie=UTF-8

# ref: https://www.geopostcodes.com/blog/python-zip-code-map/
# ref: https://medium.com/geekculture/location-marking-with-folium-in-python-329d0c11fa8b

# refL https://www.tutorialspoint.com/how-to-get-geolocation-in-python