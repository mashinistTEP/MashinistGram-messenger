import requests

class API:
    @staticmethod
    def request(endpoint, method='GET', data=None):
        from config import API_URL
        url = f"{API_URL}/{endpoint}"
        try:
            if method == 'GET':
                r = requests.get(url, params=data, timeout=10, verify=False)
            else:
                r = requests.post(url, data=data, timeout=10, verify=False)
            return r.json()
        except Exception as e:
            return {'error': str(e)}
