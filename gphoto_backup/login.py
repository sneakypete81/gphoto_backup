import os
import warnings
from datetime import datetime, timedelta

import httplib2
from gdata.photos.service import PhotosService
from oauth2client.file import Storage
from oauth2client.client import flow_from_clientsecrets

from util import CONFIG_PATH

CLIENT_SECRETS = os.path.join(CONFIG_PATH, ".client_secrets.json")
CREDENTIAL_STORE = os.path.join(CONFIG_PATH, ".credential_store.{email}")
USER_AGENT = "sneakypete81gphototools"
SCOPE = "https://picasaweb.google.com/data/"

def login(email):
    if not os.path.exists(CONFIG_PATH):
        os.makedirs(CONFIG_PATH)
    if not os.path.exists(CLIENT_SECRETS):
        _generate_client_secrets()

    credentials = _load_credentials(email)

    additional_headers = {"Authorization" : "Bearer %s" % credentials.access_token}
    gd_client = PhotosService(source=USER_AGENT, email=email,
                              additional_headers=additional_headers)
    return gd_client

def _generate_client_secrets():
    print "Before you can use gphoto_backup, you need to ask Google for access."
    print "This is a bit of a pain, but will only need to be done once."
    print
    print "1) Open your browser and go to https://console.google.com."
    print "2) Log in to your Google account, if necessary."
    print "3) Click 'Create Project' and give it a name (eg. 'GPhoto Backup')."
    print "4) Click 'Credentials', 'Create Credentials' then 'OAuth client ID'."
    print "5) Click 'Configure Consent Screen', enter a name (eg. 'GPhoto Backup'),"
    print "   and click 'Save'. You can leave the other fields blank."
    print "6) In 'Application Type' select 'Other', enter a name (eg. 'GPhoto Backup'),"
    print "   and click 'Create'"
    print "7) Your client ID and Secret will be displayed. Just click ok."
    print "8) In the client ID list, click the 'Download JSON' icon at the far right."
    print "9) Copy the contents of the file and paste it below:"

    json = raw_input(">").strip()
    with open(CLIENT_SECRETS, "w") as output_file:
        output_file.write(json)
    print
    print "Saved client secrets to %s" % CLIENT_SECRETS

def _load_credentials(email):
    warnings.filterwarnings("ignore", "Cannot access")
    storage = Storage(CREDENTIAL_STORE.format(email=email))
    credentials = storage.get()
    warnings.filterwarnings("default", "Cannot access")

    if credentials is None or credentials.invalid:
        flow = flow_from_clientsecrets(CLIENT_SECRETS, scope=SCOPE,
                                       redirect_uri="urn:ietf:wg:oauth:2.0:oob")
        url = flow.step1_get_authorize_url()

        code = _get_authorization_code(email, url)
        credentials = flow.step2_exchange(code)
        storage.put(credentials)

    if (credentials.token_expiry - datetime.utcnow()) < timedelta(minutes=5):
        http = httplib2.Http()
        http = credentials.authorize(http)
        credentials.refresh(http)

    return credentials

def _get_authorization_code(email, url):
    print
    print "You need to get permission to access the photos of %s." % email
    print "Open the following link in your browser, and enter the resulting code below:"
    print
    print url
    print
    return raw_input(">").strip()
