import unittest

from hartinator import PartWriter
from constants import allNotes
from voice_leading import is7thResolved, isParallel5thOctave, isSpacingValid, isVoiceCrossing

class TestPartWriter(unittest.TestCase):
    def testVoiceCrossing(self):
        testObject = PartWriter("C", "I V I")
        testObject.voices["bass"] = ["C3", "G3", "C4", "D4"]
        testObject.voices["tenor"] = ["E3", "G3", "E3"]
        testObject.voices["alto"] = ["C4", "C4", "C4", "C4"]
        testObject.voices["soprano"] = ["C5", "C5", "C5", "C5"]
        newNoteIndex = allNotes.index("F3")
        self.assertTrue(isVoiceCrossing("tenor", 3, newNoteIndex, testObject.voices))
        testObject.voices["bass"] = ["C3", "C3", "C3", "C3"]
        testObject.voices["tenor"] = ["C3", "C3", "C3"]
        newNoteIndex = allNotes.index("C3")
        self.assertFalse(isVoiceCrossing("tenor", 3, newNoteIndex, testObject.voices))

    def testIsParallelFifthOctave(self):
        testObject = PartWriter("C", "I V")
        testObject.voices["soprano"] = ["D5", "C5"]
        testObject.voices["alto"] = ["G4"] # F4
        testObject.voices["tenor"] = ["C3"] # C3
        testObject.voices["bass"] = ["C2", "C2"]
        self.assertTrue(isParallel5thOctave("alto", 1, allNotes.index("F4"), testObject.voices))
        self.assertFalse(isParallel5thOctave("tenor", 1, allNotes.index("C3"), testObject.voices))

    def testIs7thResolved(self):
        testObject = PartWriter("C", "I V")
        testObject.voices["soprano"] = ["B4"]
        testObject.voices["bass"] = ["B3"]
        self.assertTrue(is7thResolved("soprano", 1, allNotes.index("C5"), testObject.key, testObject.voices))
        self.assertFalse(is7thResolved("bass", 1, allNotes.index("A3"), testObject.key, testObject.voices))

    def testIsSpacingValid(self):
        testObject = PartWriter("C", "I V")
        testObject.voices["soprano"] = ["C5"] # F4
        testObject.voices["alto"] = ["B3"] # F4
        testObject.voices["tenor"] = ["G3"] # C3
        testObject.voices["bass"] = ["C3"]
        self.assertFalse(isSpacingValid("alto", 0, allNotes.index("B3"), testObject.voices))
        self.assertTrue(isSpacingValid("tenor", 0, allNotes.index("G3"), testObject.voices))

    # def testFollowsVoiceLeading(self):
    #     testObject = PartWriter("A", "I")
    #     testObject.voices["soprano"] = ['C5', 'C5', 'D5', 'D5', 'E5', 'D5', 'A4', 'B4']
    #     testObject.voices["alto"] = ['E4', 'F4', 'F4', 'F4', 'G4', 'G4', 'E4', 'E4']
    #     testObject.voices["tenor"] = ['A3', 'A3', 'A3', 'B3', 'B3', 'B3', 'C4', '']
    #     testObject.voices["bass"] = ['A2', 'F2', 'D3', 'B2', 'E3', 'G3', 'A3', 'E3']
    #     testObject.printAllVoices()
    #     beat = 7
    #     self.assertTrue(testObject.followsAllVoiceLeading("tenor", beat, allNotes.index("G3")))
    #     print("new beat " + str(beat))


if __name__ == '__main__':
    unittest.main()