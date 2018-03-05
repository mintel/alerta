
import requests
from flask import current_app, request, jsonify
from flask_cors import cross_origin

from alerta.auth.utils import is_authorized, create_token, get_customer
from alerta.exceptions import ApiError
from . import auth


@auth.route('/auth/dex', methods=['OPTIONS', 'POST'])
@cross_origin(supports_credentials=True)
def dex():

    if not current_app.config['DEX_URL']:
        return jsonify(status="error", message="Must define DEX_URL setting in server configuration."), 503

    access_token_url = "{0}/auth".format(current_app.config['DEX_URL'])

    payload = {
        'client_id': request.json['clientId'],
        'client_secret': current_app.config['OAUTH2_CLIENT_SECRET'],
        'redirect_uri': request.json['redirectUri'],
        'code': request.json['code'],
        'access_type': 'offline'
    }
    
    print(payload)
    try:
        r = requests.post(access_token_url, data=payload)
    except Exception:
        return jsonify(status="error", message="Failed to call Dex API over HTTPS")
    access_token = r.json()

    # Dex does not support a userinfo point yet
    # FIXME
    # headers = {"Authorization": "{0} {1}".format(access_token['token_type'], access_token['access_token'])}
    #r = requests.get("{0}/authrealms/{1}/protocol/openid-connect/userinfo".format(current_app.config['KEYCLOAK_URL'], current_app.config['KEYCLOAK_REALM']), headers=headers)
    #profile = r.json()

    #roles = profile['roles']
    #login = profile['preferred_username']

    login = 'test user'
    roles = ['test-role1', 'test-role2']
    if is_authorized('ALLOWED_DEX_ROLES', roles):
        raise ApiError("User %s is not authorized" % login, 403)

    customer = get_customer(login, groups=roles)

    token = create_token(profile['sub'], profile['name'], login, provider='dex', customer=customer, roles=roles)
    return jsonify(token=token.tokenize)
