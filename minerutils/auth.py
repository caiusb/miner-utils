from urllib.parse import urlparse, parse_qs
import requests as req
import datetime

class MinerWithAuthentication:

	def __init__(self, username = None, token = None):
		if (username is None and token is None):
			self.auth = None
		elif(token is not None and username is None):
			self.auth = token
		else:
			self.auth = (username, token)

	def _printWithTimeStamp(self, text):
		today = datetime.datetime.today()
		print('[' + str(today) + ']: ' + text)

	def genericApiCall(self, root, url, paginationArg, params={}, headers={}, perPage=100):
		parsedUrl = urlparse(url)
		url = parsedUrl.path.strip('/')
		query = parse_qs(parsedUrl.query)
		params = {**params, **query}
		if (not paginationArg in params):
			params[paginationArg] = perPage
		resp = self._get(root + url, params=params, headers=headers)
		jsonList = self._processResp(url, resp)
		nextUrl = self._getNextURL(resp)
		while (nextUrl is not None):
			resp = self._get(nextUrl, params=params, headers=headers)
			if (resp is None): # This should not happen
				return jsonList
			newJsonList = self._processResp(nextUrl, resp)
			jsonList.extend(newJsonList)
			nextUrl = self._getNextURL(resp)
		return jsonList
	
	def _get(self, url, params={}, headers={}):
		resp = req.get(url, auth=self.auth, params=params, headers=headers)
		if (resp.status_code == 200):
			return resp
		return None
	
	def _processResp(self, url, resp):
		pass
	
	def _getNextURL(self, resp):
		pass

	def usesAuth(self):
		return not self.auth is None