# fix voice crossing
# backtracking
# add flat keys
# fix ranges

majorKeys = {
    "C": "CDEFGAB",
    "G": ["G", "A", "B", "C", "D", "E", "F#"],
    "D": ["D", "E", "F#", "G", "A", "B", "C#"],
    "A": ["A", "B", "C#", "D", "E", "F#", "G#"],
    "E": ["E", "F#", "G#", "A", "B", "C#", "D#"],
    "B": ["B", "C#", "D#", "E", "F#", "G#", "A#"],
    "F#": ["F#", "G#", "A#", "B", "C#", "D#", "E#"],
    "C#": ["C#", "D#", "E#", "F#", "G#", "A#", "B#"]
}

minorKeys = {
    "a": "ABCDEFG",
    "e": ["E", "F#", "G", "A", "B", "C", "D"],
    "b": ["B", "C#", "D", "E", "F#", "G", "A"],
    "f": ["F#", "G#", "A", "B", "C#", "D", "E"],
    "c": ["C#", "D#", "E", "F#", "G#", "A", "B"],
    "g": ["G#", "A#", "B", "C#", "D#", "E", "F#"],
    "d": [ "D#", "E#", "F#", "G#", "A#", "B", "C#"],
    "a#": ["A#", "B#", "C#", "D#", "E#", "F#", "G#"]
}

majorChordMap = {
    "I": 1,
    "ii": 2,
    "iii": 3,
    "IV": 4,
    "V": 5,
    "vi": 6,
    "vii": 7,
    "viiº": 7,
}

minorChordMap = {
    "i": 1,
    "ii": 2,
    "iiº": 2,
    "III": 3,
    "iv": 4,
    "v": 5,
    "VI": 6,
    "VII": 7
}

allNotes = "G2A2B2C3D3E3F3G3A3B3C4D4E4F4G4A4B4C5D5E5F5"

bassRange = [0, 16]
tenorRange = [6, 20]
altoRange = [16, 30]
supranoRange = [26, len(allNotes) - 2]

class PartWriter:
    def __init__(self, key="C", chordProgression="I"):
        self.key = key
        self.chordProgression = chordProgression.split(" ") # convert from "I I I" to ["I", "I", "I"]

    def isParallel5thOctave(self, line1, line2, startingPos, newNoteIndex, lower):
        if startingPos < 0:
            return False

        # check for stagnant motion
        if line1[startingPos][0:1] == line1[startingPos+1][0:1]:
            return False

        # check for octaves
        if line2[startingPos][0:1] == line1[startingPos][0:1] and allNotes[newNoteIndex] == line1[startingPos+1][0:1]:
            return True

        # check for 5th
        if lower: # if list 1 is below list 2 i.e. if we should look up a 4th or down a 4th from list 1
            if allNotes[allNotes.index(line1[startingPos][0:1]) + 8] == line2[startingPos][0:1] and allNotes[allNotes.index(line1[startingPos+1][0:1]) + 8] == allNotes[newNoteIndex]:
                return True
        else:
            if allNotes[allNotes.index(line1[startingPos][0:1]) + 10] == line2[startingPos][0:1] and allNotes[allNotes.index(line1[startingPos+1][0:1]) + 10] == allNotes[newNoteIndex]:
                return True

    def isVoiceCrossing(self, line1, startingPos, newNoteIndex, lower):
        if startingPos < 0:
            return False

        comparisonNote = allNotes.index(line1[startingPos][0:1])
        if lower: # if line 1 is supposed to be lower than line 2
            if newNoteIndex > comparisonNote:
                return True
        else:
            if newNoteIndex < comparisonNote:
                return True

        return False

    def generateKeystring(self):
        if self.key in majorKeys:
            self.keystring = majorKeys[self.key]
            self.quality = "major"
        else:
            self.keystring = minorKeys[self.key]
            self.quality = "minor"
        
    def setChordProgression(self):
        chords = []
        if self.quality == "major":
            for chord in self.chordProgression:
                chords.append(majorChordMap[chord])
        else:
            for chord in self.chordProgression:
                chords.append(minorChordMap[chord])
        self.chords = chords

    def writeBassLine(self):
        self.bassline = []
        lastNoteIndex = 0

        # setting first note to root
        for i in range(len(allNotes)):
            if allNotes[i] == self.keystring[self.chords[0]-1][0:1]:
                lastNoteIndex = i
                break
            else:
                i += 1

        # write rest of bassline
        for chord in self.chords:
            i, j = lastNoteIndex, lastNoteIndex
            while True:
                if allNotes[i] == self.keystring[chord-1][0:1]:
                    self.bassline.append(allNotes[i:i+2])
                    lastNoteIndex = i
                    break
                elif allNotes[j] == self.keystring[chord-1][0:1]:
                    self.bassline.append(allNotes[j:j+2])
                    lastNoteIndex = j
                    break

                # keeping pointers within range
                if i > bassRange[0]:
                    i -= 2
                if j < bassRange[1]:
                    j += 2
                if i <= bassRange[0] and j >= bassRange[1]:
                    print("shit") # this should never happen
                    break
        
    def writeSupranoLine(self):
        self.supranoLine = []
        i = supranoRange[1]

        # setting first note to bass
        while True:
            if allNotes[i] == self.keystring[self.chords[0]-1][0:1]:
                lastNoteIndex = i
                break
            else:
                i -= 2

        for num, chord in enumerate(self.chords):
            i, j = lastNoteIndex, lastNoteIndex
            while True:
                # check root
                if allNotes[j] == self.keystring[chord-1][0:1] and not self.isParallel5thOctave(self.bassline, self.supranoLine, num-1, j, True):
                        self.supranoLine.append(allNotes[j:j+2])
                        lastNoteIndex = j
                        break
                if allNotes[i] == self.keystring[chord-1][0:1] and not self.isParallel5thOctave(self.bassline, self.supranoLine, num-1, i, True):
                    self.supranoLine.append(allNotes[i:i+2])
                    lastNoteIndex = i
                    break

                # check 5th
                if chord >= 4:
                    if allNotes[j] == self.keystring[chord-1 + 4 - 7][0:1] and not self.isParallel5thOctave(self.bassline, self.supranoLine, num-1, j, True):
                        self.supranoLine.append(allNotes[j:j+2])
                        lastNoteIndex = j
                        break
                    elif allNotes[i] == self.keystring[chord-1 + 4 - 7][0:1] and not self.isParallel5thOctave(self.bassline, self.supranoLine, num-1, i, True):
                        self.supranoLine.append(allNotes[i:i+2])
                        lastNoteIndex = i
                        break
                elif allNotes[j] == self.keystring[chord-1 + 4][0:1] and not self.isParallel5thOctave(self.bassline, self.supranoLine, num-1, j, True):
                    self.supranoLine.append(allNotes[j:j+2])
                    lastNoteIndex = j
                    break     
                elif allNotes[i] == self.keystring[chord-1 + 4][0:1] and not self.isParallel5thOctave(self.bassline, self.supranoLine, num-1, i, True):
                    self.supranoLine.append(allNotes[i:i+2])
                    lastNoteIndex = i
                    break

                # check 3rd
                if chord >= 6:
                    if allNotes[j] == self.keystring[chord-1 + 2 - 7][0:1] and not self.isParallel5thOctave(self.bassline, self.supranoLine, num-1, j, True):
                        self.supranoLine.append(allNotes[j:j+2])
                        lastNoteIndex = j
                        break
                    elif allNotes[i] == self.keystring[chord-1 + 2 - 7][0:1] and not self.isParallel5thOctave(self.bassline, self.supranoLine, num-1, i, True):
                        self.supranoLine.append(allNotes[i:i+2])
                        lastNoteIndex = i
                        break
                elif allNotes[j] == self.keystring[chord-1 + 2][0:1] and not self.isParallel5thOctave(self.bassline, self.supranoLine, num-1, j, True):
                    self.supranoLine.append(allNotes[j:j+2])
                    lastNoteIndex = j
                    break
                elif allNotes[i] == self.keystring[chord-1 + 2][0:1] and not self.isParallel5thOctave(self.bassline, self.supranoLine, num-1, i, True):
                    self.supranoLine.append(allNotes[i:i+2])
                    lastNoteIndex = i
                    break

                # make sure the range is not being left
                if i > supranoRange[0]:
                    i -= 2
                if j < supranoRange[1]:
                    j += 2
                if i <= supranoRange[0] and j >= supranoRange[1]:
                    print("shit") # this should be physically impossible, but just in case
                    break

    def writeAltoAndTenor(self):
        self.altoLine = []
        self.tenorLine = []

        # good starting notes
        lastAlto = 22 
        lastTenor = 12

        for num, chord in enumerate(self.chords):
            print(self.altoLine)
            print(self.tenorLine)

            # see what note(s) is (are) missing eventually change [root, third, fifth]
            counts = [1, 0, 0]
            fifth = ""
            third = ""

            # just in case the third of fifth need to be doubled
            backUpThird, backUpFifth = "", ""

            # update counts of each chord member
            if self.supranoLine[num][0:1] == self.keystring[chord-1][0:1]:
                counts[0] = 2

            # fifth    
            if chord >= 4:
                if self.supranoLine[num][0:1] == self.keystring[chord-1 + 4 - 7][0:1]:
                    counts[2] = 1
                    fifth = self.keystring[chord-1 + 4 - 7][0:1]
            else:
                fifth = self.keystring[chord-1 + 4 - 7][0:1]
                if self.supranoLine[num][0:1] == self.keystring[chord-1 + 4][0:1]:
                    counts[2] = 1

            # third
            if chord >= 6:
                if self.supranoLine[num][0:1] == self.keystring[chord-1 + 2 - 7][0:1]:
                    counts[1] = 1
                    third = self.keystring[chord-1 + 2 - 7][0:1]
            else:
                third = self.keystring[chord-1 + 2 - 7][0:1]
                if self.supranoLine[num][0:1] == self.keystring[chord-1 + 2][0:1]:
                    counts[1] = 1
            
            # fill in the missing chord members
            i, j = lastAlto, lastAlto
            if counts[1] == 0:
                lookingFor = third
                lookingForIndex = 1
            else:
                lookingFor = fifth
                lookingForIndex = 2

            while True:
                if allNotes[j] == lookingFor and not self.isParallel5thOctave(self.bassline, self.altoLine, num-1, j, True) and not self.isParallel5thOctave(self.supranoLine, self.altoLine, num-1, j, False):
                    self.altoLine.append(allNotes[j:j+2])
                    counts[lookingForIndex] += 1
                    if counts[2] == 0:
                        lookingFor = allNotes[allNotes.index(self.keystring[chord-1][0:1]) + 8]
                        lookingForIndex = 2
                    else:
                        lookingFor = self.keystring[chord-1]
                        lookingForIndex = 0
                    lastAlto = j
                    break

                if allNotes[i] == lookingFor and not self.isParallel5thOctave(self.bassline, self.altoLine, num-1, i, True) and not self.isParallel5thOctave(self.supranoLine, self.altoLine, num-1, i, False):
                    self.altoLine.append(allNotes[i:i+2])
                    counts[lookingForIndex] += 1
                    if counts[2] == 0:
                        lookingFor = allNotes[allNotes.index(self.keystring[chord-1][0:1]) + 8]
                        lookingForIndex = 2
                    else:
                        lookingFor = self.keystring[chord-1]
                        lookingForIndex = 0
                    lastAlto = i
                    break

                # setup backups just in case they need to be doubled
                if backUpFifth == "":
                    if allNotes[i] == fifth and not self.isParallel5thOctave(self.bassline, self.altoLine, num-1, i, True) and not self.isParallel5thOctave(self.supranoLine, self.altoLine, num-1, i, False):
                        backUpFifth = allNotes[i:i+2]
                    elif allNotes[j] == fifth and not self.isParallel5thOctave(self.bassline, self.altoLine, num-1, j, True) and not self.isParallel5thOctave(self.supranoLine, self.altoLine, num-1, j, False):
                        backUpFifth = allNotes[j:j+2]
                if backUpThird == "":
                    if allNotes[i] == fifth and not self.isParallel5thOctave(self.bassline, self.altoLine, num-1, i, True) and not self.isParallel5thOctave(self.supranoLine, self.altoLine, num-1, i, False):
                        backUpThird = allNotes[i:i+2]
                    elif allNotes[j] == fifth and not self.isParallel5thOctave(self.bassline, self.altoLine, num-1, j, True) and not self.isParallel5thOctave(self.supranoLine, self.altoLine, num-1, j, False):
                        backUpThird = allNotes[j:j+2]

                # keep pointers within range
                if i > altoRange[0]:
                    i -= 2
                if j < altoRange[1]:
                    j += 2

                # use backups if neccessary, prioritizing the fifth over the third
                if i <= altoRange[0] and j >= altoRange[1]:
                    if counts[2] != 2 and backUpFifth != "":
                        self.altoLine.append(backUpFifth)
                        counts[2] += 1
                        print("doubled 5th in alto")
                    elif backUpThird != "":
                        self.altoLine.append(backUpThird)
                        counts[1] += 1
                        print("doubled 3rd in alto")
                    else:
                        print("fml") # this will happen in the case of a bad chord progression
                        print(counts)
                    break
            
            i, j = lastTenor, lastTenor
            backUpThird, backUpFifth = "", "" # reset to be used by tenor
            while True:
                if allNotes[i] == lookingFor and not self.isParallel5thOctave(self.bassline, self.tenorLine, num-1, i, True) and not self.isParallel5thOctave(self.supranoLine, self.tenorLine, num-1, i, False) and not self.isParallel5thOctave(self.altoLine, self.tenorLine, num-1, i, False):
                    self.tenorLine.append(allNotes[i:i+2])
                    lastTenor = i
                    break
                if allNotes[j] == lookingFor and not self.isParallel5thOctave(self.bassline, self.tenorLine, num-1, j, True) and not self.isParallel5thOctave(self.supranoLine, self.tenorLine, num-1, j, False) and not self.isParallel5thOctave(self.altoLine, self.tenorLine, num-1, j, False):
                    self.tenorLine.append(allNotes[j:j+2])
                    lastTenor = j
                    break

                # setup backups just in case they need to be doubled
                if backUpFifth == "":
                    if allNotes[i] == fifth and not self.isParallel5thOctave(self.bassline, self.tenorLine, num-1, i, True) and not self.isParallel5thOctave(self.supranoLine, self.tenorLine, num-1, i, False) and not self.isParallel5thOctave(self.altoLine, self.tenorLine, num-1, i, False):
                        backUpFifth = allNotes[i:i+2]
                    elif allNotes[j] == fifth and not self.isParallel5thOctave(self.bassline, self.tenorLine, num-1, j, True) and not self.isParallel5thOctave(self.supranoLine, self.tenorLine, num-1, j, False) and not self.isParallel5thOctave(self.altoLine, self.tenorLine, num-1, j, False):
                        backUpFifth = allNotes[j:j+2]
                if backUpThird == "":
                    if allNotes[i] == fifth and not self.isParallel5thOctave(self.bassline, self.tenorLine, num-1, i, True) and not self.isParallel5thOctave(self.supranoLine, self.tenorLine, num-1, i, False) and not self.isParallel5thOctave(self.altoLine, self.tenorLine, num-1, i, False):
                        backUpThird = allNotes[i:i+2]
                    elif allNotes[j] == fifth and not self.isParallel5thOctave(self.bassline, self.tenorLine, num-1, j, True) and not self.isParallel5thOctave(self.supranoLine, self.tenorLine, num-1, j, False) and not self.isParallel5thOctave(self.altoLine, self.tenorLine, num-1, j, False):
                        backUpThird = allNotes[j:j+2]

                # keep pointers within range
                if i > tenorRange[0]:
                    i -= 2
                if j < tenorRange[1]:
                    j += 2

                # use backups if neccessary, prioritizing the fifth over the third
                if i <= tenorRange[0] and j >= tenorRange[1]:
                    if counts[2] == 1 and backUpFifth != "":
                        self.tenorLine.append(backUpFifth)
                        counts[2] += 1
                        print("doubled 5th in tenor")
                    elif backUpThird != "":
                        self.tenorLine.append(backUpThird)
                        counts[1] += 1
                        print("doubled 3rd in tenor")
                    else:
                        print("fml") # this will happen in the case of a bad chord progression
                        print(counts)
                    break

    def printChords(self):
        for chord in self.chords:
            if chord >= 6:
                print(self.keystring[chord-1] + " " + self.keystring[chord-1 + 2 - 7] + " " + self.keystring[chord-1 + 4 - 7])
            elif chord >= 4:
                print(self.keystring[chord-1] + " " + self.keystring[chord-1 + 2] + " " + self.keystring[chord-1 + 4 - 7])
            else:
                print(self.keystring[chord-1] + " " + self.keystring[chord-1 + 2] + " " + self.keystring[chord-1 + 4])

    def main(self):
        if self.key == None:
            self.key = input("What is the key?: ")
        if self.chordProgression == None:
            self.chordProgression = input("Enter a chord progression (seperated by spaces): ").split(" ")
        self.generateKeystring()
        self.setChordProgression()
        self.printChords()
        self.writeBassLine()
        self.writeSupranoLine()
        self.writeAltoAndTenor()
        print(self.supranoLine)
        print(self.altoLine)
        print(self.tenorLine)
        print(self.bassline)

if __name__ == "__main__":
    PartWriterImpl = PartWriter("C", "I V vi IV")
    PartWriterImpl.main()

# edge cases: 
# I V vi IV
