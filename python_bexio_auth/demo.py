from pip._vendor.distlib.compat import raw_input
from client import BexioAuthClient

scope = 'contact_show'

bexio = BexioAuthClient(
    client_id='YOUR_CLIENT_ID',
    client_secret='YOUR_CLIENT_SECRET',
    redirec_uri='YOUR_REDIRECT_URL')

print(bexio.get_auth_url(scope))
code = raw_input('Enter code parameter from URL: ')
bexio.get_access_token(code)
print(bexio.get('/contacts'))
