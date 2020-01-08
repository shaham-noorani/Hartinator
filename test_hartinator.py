import unittest

from hartinator import PartWriter
from constants import allNotes

class TestPartWriter(unittest.TestCase):
    def testVoiceCrossing(self):
        testObject = PartWriter("C", "I V I")
        testObject.bassLine = ["C4", "G4", "C4"]
        testObject.tenorLine = ["E3", "B3", "E3"]
        newNoteIndex = allNotes.index(testObject.tenorLine[2])
        self.assertTrue(testObject.isVoiceCrossing("bass", ["tenor"], newNoteIndex))

    def testIsParallelFifthOctave(self):
        testObject = PartWriter("C", "I V I")
        testObject.sopranoLine = ["C5", "G5", "C5"]
        testObject.bassLine = ["C3", "G3", "C3"]
        newNoteIndex = allNotes.index(testObject.bassLine[1])
        self.assertTrue(testObject.isParallel5thOctave("soprano", ["bass"], 0, newNoteIndex))

if __name__ == '__main__':
    unittest.main()