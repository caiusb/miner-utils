import json
import urllib
import urllib.parse
from minerutils.auth import MinerWithAuthentication

class Travis(MinerWithAuthentication):
    
    root = "http://api.travis-ci.org/"

    def __init__(self, token=None):
        super(Travis, self).__init__(None, token)

    def _getNextURL(self, resp):
        jsonResp = json.loads(resp.text)
        if (not '@pagination' in jsonResp):
            return None
        if (jsonResp['@pagination'] is None):
            return None
        if (jsonResp['@pagination']['next'] is None):
            return None
        if (jsonResp['@pagination']['next']['@href'] is None):
            return None
        return urllib.parse.urljoin(self.root, jsonResp['@pagination']['next']['@href'])

    def _processResp(self, url, resp):
        if (resp is None):
            return None
        jsonResp = json.loads(resp.text)
        if ('builds' in jsonResp):
            return jsonResp['builds']
        return jsonResp

    def getBuilds(self, repoSlug):
        encodedSlug = urllib.parse.quote(repoSlug,safe='')
        return self.get("/repo/" + encodedSlug + "/builds")

    def getBuild(self, buildId):
        return self.get("/build/" + str(buildId))

    def get(self, endpoint, params={}, headers={}):
        headers['Travis-API-Version'] = '3'
        return self.genericApiCall(self.root, endpoint, "limit", headers=headers)
