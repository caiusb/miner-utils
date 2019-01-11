import unittest
from minerutils import Travis

class TravisTest(unittest.TestCase):

    def setUp(self):
        self.t = Travis()

    def test_get_builds(self):
        builds = self.t.getBuilds("cs361fall2018/cs361fall2018.github.io")
        self.assertTrue(len(builds) > 10)

    def test_get_a_build(self):
        build = self.t.getBuild(462369732)
        self.assertEqual("passed", build['state'])

    def test_get_a_job(self):
        job = self.t.get("/job/462369733")
        self.assertIsNotNone(job)

    def test_get_multiple_pages(self):
        builds = self.t.getBuilds("scala/scala")
        self.assertTrue(len(builds) > 100)
        
if __name__ == '__main__':
	unittest.main()
