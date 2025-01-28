import folium
import pandas
import plotly.express

# reference: https://realpython.com/python-folium-web-maps-from-data
# ref: https://www.google.com/search?q=insert+map+in+vue+using+folium&oq=insert+map+in+vue+using+folium&gs_lcrp=EgZjaHJvbWUyBggAEEUYOdIBCDQ0MDFqMGo3qAIAsAIA&sourceid=chrome&ie=UTF-8

# ref: https://www.geopostcodes.com/blog/python-zip-code-map/
# ref: https://medium.com/geekculture/location-marking-with-folium-in-python-329d0c11fa8b

m = folium.Map(location=[40.7128, -74.0060], zoom_start=12)


# Add a marker
folium.Marker([40.7128, -74.0060], popup="New York City").add_to(m)

# Save the map as an HTML file
m.save("../Frontend/src/assets/map.html")


