import unittest
from githubutils import GitHub

class GitHubTest(unittest.TestCase):

	def setUp(self):
		self.g = GitHub("test2", "f5ea68446042e23f3de1f7583868e8416ef012d5")

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

	def test_headers(self):
		stargazers = self.g.doApiCall('/repos/caiusb/gitective/stargazers', headers={'Accept': 'application/vnd.github.v3.star+json'})
		self.assertTrue(len(stargazers) > 0)
		self.assertTrue(len(stargazers[0].keys()) == 2)

	def test_follow_links(self):
		repo = self.g.doApiCall('/repos/caiusb/gitective')
		print(repo['forks_url'])
		forks = self.g.doApiCall(repo['forks_url'])
		self.assertTrue(len(forks) > 0)

if __name__ == '__main__':
	unittest.main()
