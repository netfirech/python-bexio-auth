import random
import string
import requests

from urllib.parse import urlencode


class BexioAuthClient:
    BEXIO_BASE_URL = 'https://office.bexio.com/api2.php/'
    BEXIO_AUTH_URL = 'https://office.bexio.com/oauth/authorize/'
    BEXIO_TOKEN_URL = 'https://office.bexio.com/oauth/access_token/'
    BEXIO_REFRESH_URL = 'https://office.bexio.com/oauth/refresh_token/'

    def __init__(self, client_id, client_secret, redirec_uri,
                 base_url=None, auth_url=None, token_url=None, refresh_url=None):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirec_uri

        self.base_url = base_url or self.BEXIO_BASE_URL
        self.auth_url = auth_url or self.BEXIO_AUTH_URL
        self.token_url = token_url or self.BEXIO_TOKEN_URL
        self.refresh_url = refresh_url or self.BEXIO_REFRESH_URL

        self.organisation = ''
        self.access_token = ''
        self.refresh_token = ''

    def _get_state(self, size):
        return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(size))

    def _api_url(self, endpoint):
        return f'{self.base_url}{self.organisation}{endpoint}'

    def _refresh_token(self):
        response = requests.post(self.refresh_url, data={
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'refresh_token': self.refresh_token
        })

        if response.status_code == 200:
            data = response.json()
            self.access_token = data['access_token']
            self.refresh_token = data['refresh_token']

    def get_auth_url(self, scope):
        params = {
            'scope': scope,
            'client_id': self.client_id,
            'state': self._get_state(10),
            'redirect_uri': self.redirect_uri
        }
        return f'{self.auth_url}?{urlencode(params)}'

    def get_access_token(self, code):
        response = requests.post(self.token_url, data={
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri,
            'client_secret': self.client_secret,
            'code': code
        })

        if response.status_code == 200:
            data = response.json()
            self.organisation = data['org']
            self.access_token = data['access_token']
            self.refresh_token = data['refresh_token']

        else:
            raise Exception(f'Failed to obtain an access token: {response.text}')

    def get(self, endpoint):
        return self._request('get', endpoint)

    def post(self, endpoint, data=None):
        return self._request('post', endpoint, data)

    def put(self, endpoint, data=None):
        return self._request('put', endpoint, data)

    def delete(self, endpoint, data=None):
        return self._request('delete', endpoint, data)

    def _request(self, method, endpoint, data=None):
        data = data or {}
        headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {self.access_token}',
        }

        response = getattr(requests, method)(self._api_url(endpoint), params=data, headers=headers)

        if response.status_code == 401:
            """ If request ist unauthorized try to refresh the access token. Then retry the request """
            self._refresh_token()
            return self._request(method, endpoint, data)

        if response.status_code not in (200, 201):
            raise Exception(f'Failed to query Bexio: {response.text}')

        return response.json()
