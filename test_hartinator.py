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
        testObject = PartWriter("C", "I V")
        testObject.sopranoLine = ["D5", "A5"]
        testObject.altoLine = ["B4", "C5"]
        testObject.tenorLine = ["B3", "E4"]
        testObject.bassLine = ["G3", "A3"]
        newNoteIndex = allNotes.index(testObject.sopranoLine[1])
        self.assertFalse(testObject.isParallel5thOctave("soprano", ["bass, tenor, alto"], 1, newNoteIndex))
        newNoteIndex = allNotes.index(testObject.altoLine[1])
        self.assertFalse(testObject.isParallel5thOctave("alto", ["bass, tenor, soprano"], 1, newNoteIndex))
        newNoteIndex = allNotes.index(testObject.tenorLine[1])
        self.assertFalse(testObject.isParallel5thOctave("tenor", ["bass, bass, alto"], 1, newNoteIndex))
        # D5 A5
        # B4 C5
        # B3 E4
        # G3 A3

if __name__ == '__main__':
    unittest.main()