"""Provides tests for the pumper package."""
import unittest
from pumper.Pumper import Pumper

class TestPumper(unittest.TestCase):
	"""Provides tests for the Pumper class."""
	def setUp(self):
		self.p = Pumper()

	def testPumpListAfterInsert(self):
		"""Tests if the pump list remains valid after insert."""
		self.p.addPump(3, 1)
		self.assertEqual(len(self.p.pumps), 1,
		                 "Pump list length not like expected after insert")
		self.assertEqual(self.p.pumps[3]._pumpNr, 3, "PumpNr changed after insert")

	def testPumpAttributes(self):
		"""Checks if the attribute of newly inserted pumps remains valid."""
		self.p.addPump(3, 2)
		self.assertEqual(self.p.pumps[3]._gpio, 2,
		                 "Gpio of created pump not like expexted")

	def testPumpDuplicates(self):
		"""Ensures that an Exception ist raised if a pumpNr is already in use"""
		self.p.addPump(3, 1)
		self.assertRaises(ValueError, self.p.addPump, 3, 2)

if __name__ == '__main__':
	unittest.main()
