import requests

if __name__ == '__main__':
    res = requests.get('http://127.0.0.1:5000/data')
    if res.ok:
        data = res.json()
        print(data)