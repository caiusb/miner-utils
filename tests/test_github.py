import unittest
from github import GitHub

class GitHubTest(unittest.TestCase):

	def setUp(self):
		self.g = GitHub()

	def tearDown(self):
		self.g = None

	def test_repo_exists(self):
		self.assertTrue(self.g.repoExists("caiusb", "github-utils"))

	def test_repo_doesnt_exit(self):
		self.assertFalse(self.g.repoExists("caiusb", "invalid"))

	def test_rate_limit(self):
		if (self.g.usesAuth()):
			limit = 5000
		else:
			limit = 60
		self.assertTrue(self.g.getRemainingRateLimit() <= limit)

	def test_paginated_call(self):
		reposNo = len(self.g.doApiCall('users/caiusb/repos', perPage=10))
		self.assertTrue(reposNo >= 47)

if __name__ == '__main__':
	unittest.main()