import unittest

from hartinator import PartWriter
from constants import allNotes

class TestPartWriter(unittest.TestCase):
    def testVoiceCrossing(self):
        testObject = PartWriter("C", "I V I")
        testObject.bassLine = ["C3", "G3", "C4"]
        testObject.tenorLine = ["E3", "G3", "E3"]
        newNoteIndex = allNotes.index(testObject.tenorLine[2])
        del testObject.tenorLine[-1]
        self.assertTrue(testObject.isVoiceCrossing("tenor", 1, newNoteIndex))

    def testIsParallelFifthOctave(self):
        testObject = PartWriter("C", "I V I")
        testObject.sopranoLine = ["C5", "G5", "C5"]
        testObject.bassLine = ["C3", "G3", "C3"]
        newNoteIndex = allNotes.index(testObject.bassLine[1])
        self.assertTrue(testObject.isParallel5thOctave("bass", ["soprano"], 1, newNoteIndex))

if __name__ == '__main__':
    unittest.main()