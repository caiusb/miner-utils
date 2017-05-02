#!/opt/local/bin/python

import os
import time
import requests as req
import re
import json
import datetime

class GitHub:

	root = 'https://api.github.com/'

	def __init__(self, username = None, token = None): 
		if (username is None or token is None):
			self.auth = None
		else:
			self.auth = (username, token)

	def __printWithTimeStamp(self, text):
		today = datetime.datetime.today()
		print('[' + str(today) + ']: ' + text)

	def doApiCall(self, url, params={}, listKey=None, perPage=100):
		url = url.strip('/')
		if (not 'per_page' in params):
			params['per_page'] = perPage
		resp = self.__doRawApiCall(self.root + url, params=params)
		jsonList = json.loads(resp.text)
		nextUrl = self.__getNextURL(resp)
		while (nextUrl is not None):
			resp = self.__doRawApiCall(nextUrl, params=params)
			newJsonList = json.loads(resp.text)
			jsonList.extend(newJsonList)
			nextUrl = self.__getNextURL(resp)
		return jsonList

	def __doRawApiCall(self, url, params={}):
		resp = req.get(url, auth=self.auth, params=params)
		if (resp.status_code == 403):
			while resp.headers['X-RateLimit-Remaining'] == '0':
				resetTime = float(resp.headers['X-RateLimit-Reset'])
				sleepTime = resetTime - time.time()
				if sleepTime > 0:
					self.__printWithTimeStamp('Exhausted the API Rate Limit. Sleeping for ' + str(sleepTime))
					time.sleep(sleepTime)
				resp = req.get(url, auth=self.auth, params=params)
			self.__printWithTimeStamp("Resuming...")
		return resp

	def __getNextURL(self, resp):
		if (not 'Link' in resp.headers):
			return None
		linksText = resp.headers['Link']
		links = linksText.split(',')
		for link in links:
			if 'rel=\"next\"' in link:
				url = re.sub('<', '', re.sub('>', '', link.split(';')[0]))
				return url
		return None

	def getRepoRoot(self, repo):
		return self.root + repo['username'] + '/' + repo['repo']

	def getRemainingRateLimit(self):
		limit = self.doApiCall('rate_limit')
		return limit['rate']['remaining']

	def printRemainingRateLimit(self):
		self.__printWithTimeStamp('Remaining api calls: ' + str(self.getRemainingRateLimit()))

	def __getTextFromJson(self, jsonDict):
		return json.dumps(jsonDict, separators=(',',':'))

	def repoExists(self, user, repo):
		resp = self.__doRawApiCall(self.root + 'repos/' + user + '/' + repo)
		if (resp.status_code == 404):
			return False
		else:
			return True

	def usesAuth(self):
		return not self.auth is None
