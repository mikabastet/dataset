from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="geo_mika")

direccion = "Maipu 997, Corrientes, Argentina"
location = geolocator.geocode(direccion)

print(location)
