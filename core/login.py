from fyers_apiv3 import fyersModel
import yaml
from config.config_update import ConfigUpdate

class TradeLogin(ConfigUpdate):
	def __init__(self):
		self.login_config = None	
		with open('./config/config.yaml') as stream:
			try:
				self.login_config = yaml.safe_load(stream)
			except yaml.YAMLError as exc:
				print(exc)

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

	
