from urllib.parse import urlparse
import requests as req

class GitHubAuthentication:

	def __init__(self, username = None, token = None):
		if (username is None and token is None):
			self.auth = None
		elif(token is not None):
			self.auth = token
		else:
			self.auth = (username, token)

	def __printWithTimeStamp(self, text):
		today = datetime.datetime.today()
		print('[' + str(today) + ']: ' + text)

	def genericApiCall(self, root, url, paginationArg, params={}, headers={}, perPage=100):
		url = urlparse(url).path.strip('/')
		if (not paginationArg in params):
			params[paginationArg] = perPage
		resp = self._doApiCall(root + url, params=params, headers=headers)
		jsonList = self._processResp(url, resp)
		nextUrl = self._getNextURL(resp)
		while (nextUrl is not None):
			resp = self._doApiCall(nextUrl, params=params, headers=headers)
			if (resp is None): # This should not happen
				return jsonList
			newJsonList = self._processResp(nextUrl, resp)
			jsonList.extend(newJsonList)
			nextUrl = self._getNextURL(resp)
		return jsonList
	
	def _doApiCall(self, url, params={}, headers={}):
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