import folium

# reference: https://realpython.com/python-folium-web-maps-from-data
# ref: https://www.google.com/search?q=insert+map+in+vue+using+folium&oq=insert+map+in+vue+using+folium&gs_lcrp=EgZjaHJvbWUyBggAEEUYOdIBCDQ0MDFqMGo3qAIAsAIA&sourceid=chrome&ie=UTF-8

m = folium.Map(location=[40.7128, -74.0060], zoom_start=12)

# Add a marker
folium.Marker([40.7128, -74.0060], popup="New York City").add_to(m)

# Save the map as an HTML file
m.save("/Frontend/src/assets/map.html")
# i might be trippin but how do you have it save in a certain folder


# TODO: how do you display this on a Vue webpage?