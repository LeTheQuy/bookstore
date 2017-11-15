import unittest
import coverage

from order.test import suites

COV = coverage.coverage(branch=True, include='app/*')
COV.start()

unittest.TextTestRunner(verbosity=2).run(suites)

COV.stop()
COV.report()
