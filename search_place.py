import requests

def get_nearby_places(latitude, longitude, radius, amenity):
    # Define the Overpass API endpoint
    overpass_url = "http://overpass-api.de/api/interpreter"

    # Construct the Overpass query
    overpass_query = f"""
    [out:json];
    (
        node["amenity"="{amenity}"](around:{radius},{latitude},{longitude});
        way["amenity"="{amenity}"](around:{radius},{latitude},{longitude});
        relation["amenity"="{amenity}"](around:{radius},{latitude},{longitude});
    );
    out center;
    """

    # Send the request to the Overpass API
    response = requests.get(overpass_url, params={"data": overpass_query})

    # Parse the response and extract the relevant data
    nearby_places = []
    print(response)
    if response.status_code == 200:
        data = response.json()
        elements = data.get("elements", [])
        for element in elements:
            print("element",element)
            name = element.get("tags", {}).get("name", "")
            lat = element.get("lat")
            lon = element.get("lon")
            addressFull = element.get("tags")
            print(addressFull)
            district = ""
            addr = ""
            pin = ""
            if 'addr:district' in addressFull:
                district = addressFull['addr:district']
                district = ", " + district
            if 'addr:full' in addressFull:
                addr = addressFull['addr:full']
            if 'addr:postcode' in addressFull:
                pin = addressFull['addr:postcode']
                pin = ", " + pin
            address = addr + district + pin
            print(address)
            exclude_words = ["eye", "child", "surgery", "heart", "cancer", "addiction","dental","dentist"]
            if not any(word in name.lower() for word in exclude_words):
                nearby_places.append({"name": name, "latitude": lat, "longitude": lon, "address":address})

    return nearby_places

get_nearby_places(12.935492,77.6115927,1,"doctor")