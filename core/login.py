from fyers_apiv3 import fyersModel
import yaml
from config.config_update import ConfigUpdate
import requests
import pyotp
import json
from urllib import parse
import time
from urllib.parse import parse_qs,urlparse
import sys
class TradeLogin(ConfigUpdate):
	
    def __init__(self):
        self.login_config = None
        self.ERROR = "error"
        self.SUCCESS = "success"
        self.BASE_URL = 'https://api-t2.fyers.in/vagator/v2'
        self.BASE_URL_2 = 'https://api-t1.fyers.in/api/v3'
        self.URL_SEND_LOGIN_OTP = self.BASE_URL + '/send_login_otp'
        self.URL_VERIFY_TOTP = self.BASE_URL + '/verify_otp'
        self.URL_VERIFY_PIN = self.BASE_URl + '/verify_pin'
        self.URL_TOKEN  = self.BASE_URL_2+ '/token'
        self.URL_VALIDATION_AUTH_CODE = self.BASE_URL_2 + '/validate-authcode'
        with open('./config/config.yaml') as stream:
            try:
                self.login_config = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                 print(exc)

    def send_login_otp(self,fyers_id,app_id):
        try:
            result_string = requests.post(url=self.URL_SEND_LOGIN_OTP,json={"fy_id":self.login_config['fyers_id'],'app_id':self.login_config['client_id'].split('-')[0]})
            if result_string.status_code!=200:
                return [self.ERROR,result_string.text]
            result = json.loads(result_string.text)
            request_key = result['request_key']
            return [self.SUCCESS,request_key]
        except Exception as e:
            return [self.ERROR,str(e)]

    def generate_totp(self,secret):
        try:
            generated_totp = pyotp.TOTP(secret).now()
            return [self.SUCCESS, generated_totp]
        except Exception as e:
            return [self.ERROR,str(e)]

    def verify_PIN(self,request_key,pin):
        try:
            payload = {
                    "request_key":request_key,
                    "identity_type":"pin",
                    "identifier":self.login_config['pin']
                    }
            result_string = requests.post(url=self.URL_VERIFY_PIN,json=payload)
            if result_string.status_code!=200:
                return [self.ERROR,result_string.text]

            result = json.loads(result_string.text)
            access_token = result['data']['access_token']

            return [self.SUCCESS, access_token]
        except Exception as e:
             return [self.ERROR,str(e)]

    def token(self,fyers_id,app_id,redirect_uri,app_type,access_token):
        try:
            payload={
                    "fyers_id": fyers_id,
                    "app_id": app_id,
                    "redirect_uri": redirect_uri,
                    "appType": app_type,
                    "code_challenge":"",
                    "scope":"",
                    "nonce":"",
                    "response_type":"code",
                    "create_cookie":True

                    }
            headers = {'Authorization':f'Bearer {access_token}'}

            result_string = requests.post(url=self.URL_TOKEN,json=payload,headers=headers)
            if result_string.status_code!=200:
                return [self.ERROR,result_string.text]
            result = json.loads(result_string.text)
            url = result['Url']
            auth_code = parse.parse_qs(parse.urlparse(url).query)['auth_code'][0]

            return [self.SUCCESS,auth_code]
        except Exception as e:
            return [self.ERROR,str(e)]


    def automate_login(self):
        #Retrieve request key
        self.session = fyersModel.SessionModel(
                        client_id=self.login_config['client_id'],
                        secret_key=self.login_config['secret_key'],
                        redirect_uri=self.login_config['redirect_uri'],
                        response_type=self.login_config['response_type']
        )
        urlToActivate = self.session.generate_authcode()
        print(f'URL to activate app: {urlToActivate}')

        send_otp_result = self.send_login_otp(fyers_id=self.login_config['fyers_id'],app_id=self.login_config['client_id'].split('-')[0])

        if send_otp_result[0]!=self.SUCCESS:
            print(f'send_login_otp msg failure: {send_otp_result[1]}')
            status = False
            sys.exit()
        else:
            print('send login otp success')
            status =  False


        #generate totp

        generate_totp_result = self.generate_totp(secret=self.login_config['totp_key'])

        if generate_totp_result[0]!=self.SUCCESS:
            print(f'generate totp msg failure: {generate_totp_result[1]}')
            sys.exit()
        else:
            print('generate totp success')


        #verify totp,request_key

        for i in range(1,3):
            request_key = send_otp_result[1]
            totp = generate_totp_result[1]
            print('totp>>>',totp)

            verify_totp_result = self.verify_totp(request_key=request_key,totp=totp)

            if verify_totp_result[0]!=self.SUCCESS:
                print(f'verify totp msg failure: {verify_totp_result[1]}')
                status = False
                
                time.sleep(1)
            else:
                print(f'verify totp success: {verify_totp_result[1]}')
                status = False
                break

            if verify_totp_result[0]==self.SUCCESS:
                request_key_2 = verify_totp_result[1]

                #verify pin and send back access token

                ses = requests.Session()
                verify_pin_result = self.verify_PIN(request_key=request_key_2,pin=self.login_config['pin'])
                if verify_pin_result[0]!=self.SUCCESS:
                    print(f'verify pin failure {verify_pin_result[1]}')
                    sys.exit()
                else:
                    print('verify pin sucess')


                ses.headers.update({
                    'Authorization': f'Bearer {verify_pin_result[1]}'
                    })


                #get auth code

                token_result = self.token(fyers_id=self.login_config['fyers_id'],
                                          app_id=self.login_config['client_id'].split('-')[0],
                                          redirect_uri=self.login_config['redirect_uri'],
                                          app_type=self.login_config['client_id'].split('-')[1],
                                          access_token=verify_pin_result[1])
                if token_result[0]!=self.SUCCESS:
                    print(f'token result msg failure: {token_result[1]}')
                    sys.exit()
                else:
                    print('token result success')

                #validating auth code
                auth_code = token_result[1]
                self.session.set_token(auth_code)
                response = self.session.generate_token()
                if response['s']==self.ERROR:
                    print('cannot login,check credentials')
                    status = False
                    time.sleep(10)
                    sys.exit()

                access_token = response['access_token']
                print(access_token)

    def login(self):
        """Creation of session for authentication"""
        self.session = fyersModel.SessionModel(
						client_id=self.login_config['client_id'],
						secret_key=self.login_config['secret_key'],
						redirect_uri=self.login_config['redirect_uri'],
						response_type=self.login_config['response_type']
		)
        if self.login_config['auth_code'] is not None and self.login_config['access_token'] is None :
            self.session = fyersModel.SessionModel(
						client_id=self.login_config['client_id'],
						secret_key=self.login_config['secret_key'],
						redirect_uri=self.login_config['redirect_uri'],
						response_type=self.login_config['response_type'],
						grant_type=self.login_config['grant_type']
		)
            self.session.set_token(self.login_config['auth_code'])
            response = self.session.generate_token()
            self.access_token = response['access_token']
            ConfigUpdate().updateAccessToken(response['access_token'])
        elif self.login_config['access_token'] is not None:
            return self.login_config['access_token']
        else:
            response = self.session.generate_authcode()
            print(response)

	
