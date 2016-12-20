import webbrowser
from datetime import datetime, timedelta
import httplib2

from gdata.photos.service import PhotosService
from oauth2client.file import Storage
from oauth2client.client import flow_from_clientsecrets

USER_AGENT = "sneakypete81gphototools"
CREDENTIAL_STORE = ".credential_store.{email}"
CLIENT_SECRETS = ".client_secrets.json"

def login(email):
    scope = "https://picasaweb.google.com/data/"

    storage = Storage(CREDENTIAL_STORE.format(email=email))
    credentials = storage.get()
    if credentials is None or credentials.invalid:
        flow = flow_from_clientsecrets(CLIENT_SECRETS, scope=scope,
                                       redirect_uri='urn:ietf:wg:oauth:2.0:oob')
        uri = flow.step1_get_authorize_url()
        webbrowser.open(uri)
        code = raw_input('Enter the authentication code: ').strip()
        credentials = flow.step2_exchange(code)
        storage.put(credentials)

    if (credentials.token_expiry - datetime.utcnow()) < timedelta(minutes=5):
        http = httplib2.Http()
        http = credentials.authorize(http)
        credentials.refresh(http)

    additional_headers = {'Authorization' : 'Bearer %s' % credentials.access_token}
    gd_client = PhotosService(source=USER_AGENT, email=email,
                              additional_headers=additional_headers)
    return gd_client
