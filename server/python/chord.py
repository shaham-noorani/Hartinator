from constants import majorChordMap, minorChordMap, minorKeys, majorKeys

class Chord:
    def __init__(self, romanNumeral, key):
        if len(romanNumeral) == 1 or ((len(romanNumeral) == 2 or len(romanNumeral) == 3) and not "6" in romanNumeral):
            romanNumeralWithoutInversion = romanNumeral
        elif (len(romanNumeral) == 2 and "6" in romanNumeral) or (len(romanNumeral) == 3 and "64" in romanNumeral):
            romanNumeralWithoutInversion = romanNumeral[0:1]
        elif (len(romanNumeral) == 3 and "6" in romanNumeral) or (len(romanNumeral) == 4 and "64" in romanNumeral):
            romanNumeralWithoutInversion = romanNumeral[0:2]
        else:
            romanNumeralWithoutInversion = romanNumeral[0:3]
        if key in majorKeys:
            chordAsScaleDegree = majorChordMap[romanNumeralWithoutInversion]
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
            chordAsScaleDegree = minorChordMap[romanNumeralWithoutInversion]
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
        if "64" in romanNumeral:
            oldRoot = self.root
            self.root = self.fifth
            self.fifth = self.third
            self.third = oldRoot
        elif "6" in romanNumeral:
            oldRoot = self.root
            self.root = self.third
            self.third = self.fifth
            self.fifth = oldRoot
