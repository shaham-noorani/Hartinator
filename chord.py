from constants import majorChordMap, minorChordMap, minorKeys, majorKeys

class Chord:
    def __init__(self, romanNumeral, key):
        if key in majorKeys:
            chordAsScaleDegree = majorChordMap[romanNumeral]
            self.root = majorKeys[key][chordAsScaleDegree - 1]
            if chordAsScaleDegree >= 6:
                self.third = majorKeys[key][chordAsScaleDegree-1 + 2 - 7]
                self.fifth = majorKeys[key][chordAsScaleDegree-1 + 4 - 7]
            elif chordAsScaleDegree >= 4:
                self.third = majorKeys[key][chordAsScaleDegree-1 + 2]
                self.fifth = majorKeys[key][chordAsScaleDegree-1 + 4 - 7]
            else:
                self.third = majorKeys[key][chordAsScaleDegree-1 + 2]
                self.fifth = majorKeys[key][chordAsScaleDegree-1 + 4]
        if key in minorKeys:
            chordAsScaleDegree = minorChordMap[romanNumeral]
            self.root = minorKeys[key][chordAsScaleDegree - 1]
            if chordAsScaleDegree >= 6:
                self.third = minorKeys[key][chordAsScaleDegree-1 + 2 - 7]
                self.fifth = minorKeys[key][chordAsScaleDegree-1 + 4 - 7]
            elif chordAsScaleDegree >= 4:
                self.third = minorKeys[key][chordAsScaleDegree-1 + 2]
                self.fifth = minorKeys[key][chordAsScaleDegree-1 + 4 - 7]
            else:
                self.third = minorKeys[key][chordAsScaleDegree-1 + 2]
                self.fifth = minorKeys[key][chordAsScaleDegree-1 + 4]