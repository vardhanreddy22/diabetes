from geopy.geocoders import Nominatim

def get_latitude_longitude(location):
    geolocator = Nominatim(user_agent="my-app")  # Create a geolocator object

    try:
        # Use geocoder to get the location information
        location_data = geolocator.geocode(location)

        # Extract latitude and longitude from the location data
        latitude = location_data.latitude
        longitude = location_data.longitude

        return latitude, longitude

    except Exception as e:
        print("Error:", e)
        return None

# Example usage
address = "SJCE, Mysuru"
coordinates = get_latitude_longitude(address)
if coordinates:
    latitude, longitude = coordinates
    print(f"Latitude: {latitude}")
    print(f"Longitude: {longitude}")