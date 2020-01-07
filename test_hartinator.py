import unittest

from hartinator import PartWriter
from constants import allNotes

class TestPartWriter(unittest.TestCase):
    def testVoiceCrossing(self):
        testObject = PartWriter("C", "I V I")
        bassline = ["C4", "G4", "C4"]
        tenorLine = ["E3", "B3", "E3"]
        newNoteIndex = allNotes.index(tenorLine[2])
        self.assertTrue(testObject.isVoiceCrossing(bassline, 1, newNoteIndex, True))

    def testIsParallelFifthOctave(self):
        testObject = PartWriter("C", "I V I")
        testObject.generateKeystring()
        testObject.setChordProgression()
        sopranoLine = ["C5", "G5", "C5"]
        bassline = ["C3", "G3", "C3"]
        newNoteIndex = allNotes.index(bassline[1])
        self.assertTrue(testObject.isParallel5thOctave(sopranoLine, bassline, 0, newNoteIndex, False))

if __name__ == '__main__':
    unittest.main()