import requests

if __name__ == '__main__':
    res = requests.post('https://www.digilearn.be/geolocation/geocode', json={
        'address': '50 avenue Franklin Roosevelt, 1050 Bruxelles'
    }, headers={
        'Authorization': 'Bearer test'
    })
    if not res.ok:
        SystemError(1)
    data = res.json()
    print(data)
    originPlaceId = data['placeId']
    # placeId: ChIJB75Std3Ew0cRYG39Y4jeL7I
    res = requests.post('https://www.digilearn.be/geolocation/geocode', json={
        'address': 'Bd de la Plaine 2, Ixelles'
    }, headers={
        'Authorization': 'Bearer test'
    })
    if not res.ok:
        SystemError(1)
    data = res.json()
    print(data)
    # placeId: ChIJiT0fccnEw0cR3TYDFfl-9gE
    destinationPlaceId = data['placeId']
    res = requests.get(f'https://www.digilearn.be/geolocation/route/{originPlaceId}/{destinationPlaceId}')
    if not res.ok:
        SystemError(1)
    data = res.json()
    print(data)
    print(f"ULB to VUB is about {data['distance_in_m'] / 1000} km and {data['duration_in_s'] // 60} minutes by car")


