import requests

if __name__ == '__main__':
    res = requests.post('https://www.digilearn.be/geolocation/geocode', json={
        'address': '50 avenue Franklin Roosevelt, 1050 Bruxelles'
    }, headers={
        'Authorization': 'Bearer test'
    })
    if res.ok:
        data = res.json()
        print(data)
    else:
        print(res.status_code)