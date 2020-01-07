# backtracking before falling back on doubling the third or fifth
# add flat keys
# add functionality for different amount of parts and optional starting notes
# add priority for whether to add the root, third, or fifth, especially in suprano
# BACKBURNER be able to play the music
# write unit tests

from constants import *

class PartWriter:
    def __init__(self, key="C", chordProgression="I"):
        self.key = key
        self.chordProgression = chordProgression.split(" ") # convert from "I I I" to ["I", "I", "I"]

    def printAllVoices(self):
        print("Suprano: " + str(self.supranoLine))
        print("Alto:    " + str(self.altoLine))
        print("Tenor:   " + str(self.tenorLine))
        print("Bass:    " + str(self.bassline))

    def isParallel5thOctave(self, line1, line2, startingPos, newNoteIndex, lower):
        if len(line1) > len(self.chords) or len(line2) > len(self.chords):
            print("Shit broke")
            self.printAllVoices()
            exit() # b/c I don't have a better place to put it

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
            if allNotes[allNotes.index(line1[startingPos][0:1]) - 8] == line2[startingPos][0:1] and allNotes[allNotes.index(line1[startingPos+1][0:1]) - 8] == allNotes[newNoteIndex]:
                return True

    def isVoiceCrossing(self, line1, startingPos, newNoteIndex, lower):
        # return False #QUICK FIX
        if startingPos < 0:
            return False

        comparisonNote = allNotes.index(line1[startingPos])

        if lower: # if line 1 is supposed to be lower than line 2
            if newNoteIndex < comparisonNote:
                return True
        else:
            if newNoteIndex > comparisonNote:
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

        # good starting note
        lastNoteIndex = int((bassRange[1] - bassRange[0]) / 2 + bassRange[0])

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

        # good starting note
        lastNoteIndex = int((supranoRange[1] - supranoRange[0]) / 2) + supranoRange[0]

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
        lastAlto = int((altoRange[1] - altoRange[0]) / 2 + altoRange[0])
        lastTenor = int((tenorRange[1] - tenorRange[0]) / 2 + tenorRange[0])

        # used to store notes in the alto that cause errors in the next mesure for backtracking
        # default to relevant empty values
        blacklist = []

        num = 0
        while num < len(self.chords):
            chord = self.chords[num]
            backtrack = False

            # frequency of each chord member
            counts = [0, 0, 0]
            fifth = ""
            third = ""
            root = self.keystring[chord-1][0:1]

            lookingFor = [True, True, True]

            # just in case the third of fifth need to be doubled
            backUpThird, backUpFifth = "", ""

            # update counts of each chord member
            if self.bassline[num][0:1] == root:
                counts[0] += 1
            
            if self.supranoLine[num][0:1] == root:
                counts[0] += 1

            # fifth    
            if chord >= 4:
                fifth = self.keystring[chord-1 + 4 - 7][0:1]
                if self.supranoLine[num][0:1] == fifth:
                    counts[2] = 1
            else:
                fifth = self.keystring[chord-1 + 4][0:1]
                if self.supranoLine[num][0:1] == fifth:
                    counts[2] = 1

            # third
            if chord >= 6:
                third = self.keystring[chord-1 + 2 - 7][0:1]
                if self.supranoLine[num][0:1] == third:
                    counts[1] = 1
            else:
                third = self.keystring[chord-1 + 2][0:1]
                if self.supranoLine[num][0:1] == third:
                    counts[1] = 1

            # set pointers
            i, j = lastAlto, lastAlto
            
            # update lookingFor to not look for anything that is present, unless it's the bass and hasn't already been doubled
            for k in range(len(counts)):
                if (counts[k] == 2 and k == 0) or (counts[k] == 1 and k != 0):
                    lookingFor[k] = False

            # alto
            while True:
                # check j
                if allNotes[j] == root and lookingFor[0] == True and not allNotes[j] in blacklist:
                    if not self.isParallel5thOctave(self.bassline, self.altoLine, num-1, j, True) and not self.isParallel5thOctave(self.supranoLine, self.altoLine, num-1, j, False):
                        if not self.isVoiceCrossing(self.supranoLine, num-1, j, False):
                            self.altoLine.append(allNotes[j:j+2])
                            counts[0] += 1
                            if counts[0] == 2:
                                lookingFor[0] = False
                            lastAlto = j
                            blacklist = []
                            backtrack = False
                            break

                if allNotes[j] == fifth and lookingFor[2] == True and not allNotes[j] in blacklist:
                    if not self.isParallel5thOctave(self.bassline, self.altoLine, num-1, j, True) and not self.isParallel5thOctave(self.supranoLine, self.altoLine, num-1, j, False):
                        if not self.isVoiceCrossing(self.supranoLine, num-1, j, False):
                            self.altoLine.append(allNotes[j:j+2])
                            lookingFor[2] = False
                            counts[2] += 1
                            lastAlto = j
                            blacklist = []
                            backtrack = False
                            break

                if allNotes[j] == third and lookingFor[1] == True and not allNotes[j] in blacklist:
                    if not self.isParallel5thOctave(self.bassline, self.altoLine, num-1, j, True) and not self.isParallel5thOctave(self.supranoLine, self.altoLine, num-1, j, False):
                        if not self.isVoiceCrossing(self.supranoLine, num-1, j, False):
                            self.altoLine.append(allNotes[j:j+2])
                            lookingFor[1] = False
                            counts[1] += 1
                            lastAlto = j
                            blacklist = []
                            backtrack = False
                            break

                # check i
                if allNotes[i] == root and lookingFor[0] == True and not allNotes[i] in blacklist:
                    if not self.isParallel5thOctave(self.bassline, self.altoLine, num-1, i, True) and not self.isParallel5thOctave(self.supranoLine, self.altoLine, num-1, i, False):
                        if not self.isVoiceCrossing(self.supranoLine, num-1, i, False):
                            self.altoLine.append(allNotes[i:i+2])
                            lookingFor[0] = False
                            counts[0] += 1
                            lastAlto = i
                            blacklist = []
                            backtrack = False
                            break

                if allNotes[i] == fifth and lookingFor[2] == True and not allNotes[i] in blacklist:
                    if not self.isParallel5thOctave(self.bassline, self.altoLine, num-1, i, True) and not self.isParallel5thOctave(self.supranoLine, self.altoLine, num-1, i, False):
                        if not self.isVoiceCrossing(self.supranoLine, num-1, i, False):
                            self.altoLine.append(allNotes[i:i+2])
                            lookingFor[2] = False
                            counts[2] += 1
                            lastAlto = i
                            blacklist = []
                            backtrack = False
                            break

                if allNotes[i] == third and lookingFor[1] == True and not allNotes[i] in blacklist:
                    if not self.isParallel5thOctave(self.bassline, self.altoLine, num-1, i, True) and not self.isParallel5thOctave(self.supranoLine, self.altoLine, num-1, i, False):
                        if not self.isVoiceCrossing(self.supranoLine, num-1, i, False):
                            self.altoLine.append(allNotes[i:i+2])
                            lookingFor[1] = False
                            counts[1] += 1
                            lastAlto = i
                            blacklist = []
                            backtrack = False
                            break

                # setup backups just in case they need to be doubled
                if backUpFifth == "":
                    if allNotes[i] == fifth and not self.isParallel5thOctave(self.bassline, self.altoLine, num-1, i, True) and not self.isParallel5thOctave(self.supranoLine, self.altoLine, num-1, i, False):
                        if not self.isVoiceCrossing(self.supranoLine, num-1, i, False):
                            backUpFifth = allNotes[i:i+2]
                    elif allNotes[j] == fifth and not self.isParallel5thOctave(self.bassline, self.altoLine, num-1, j, True) and not self.isParallel5thOctave(self.supranoLine, self.altoLine, num-1, j, False):
                        if not self.isVoiceCrossing(self.supranoLine, num-1, j, False):
                            backUpFifth = allNotes[j:j+2]
                if backUpThird == "":
                    if allNotes[i] == fifth and not self.isParallel5thOctave(self.bassline, self.altoLine, num-1, i, True) and not self.isParallel5thOctave(self.supranoLine, self.altoLine, num-1, i, False):
                        if not self.isVoiceCrossing(self.supranoLine, num-1, i, False):
                            backUpThird = allNotes[i:i+2]
                    elif allNotes[j] == fifth and not self.isParallel5thOctave(self.bassline, self.altoLine, num-1, j, True) and not self.isParallel5thOctave(self.supranoLine, self.altoLine, num-1, j, False):
                        if not self.isVoiceCrossing(self.supranoLine, num-1, j, False):
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
                        backtrack = False
                        counts[2] += 1
                        print("doubled 5th in alto")
                        break
                    elif backUpThird != "":
                        self.altoLine.append(backUpThird)
                        backtrack = False
                        counts[1] += 1
                        print("doubled 3rd in alto")
                        break
                    else:
                        # BACKTRACKING
                        blacklist.append(self.altoLine[-1][0:1])
                        del self.altoLine[-1]
                        del self.tenorLine[-1]
                        backtrack = True
                        num -= 1
                        break

            if backtrack:
                continue
        
            i, j = lastTenor, lastTenor

            backUpThird, backUpFifth = "", "" # reset to be used by tenor

            # tenor
            while True:
                # check i
                if allNotes[i] == root and lookingFor[0] == True:
                    if not self.isParallel5thOctave(self.bassline, self.tenorLine, num-1, i, True) and not self.isParallel5thOctave(self.supranoLine, self.tenorLine, num-1, i, False) and not self.isParallel5thOctave(self.altoLine, self.tenorLine, num-1, i, False):
                        if not self.isVoiceCrossing(self.bassline, num-1, i, True) and not self.isVoiceCrossing(self.altoLine, num-1, i, False):
                            self.tenorLine.append(allNotes[i:i+2])
                            lookingFor[0] = False
                            lastTenor = i
                            break

                if allNotes[i] == fifth and lookingFor[2] == True:
                    if not self.isParallel5thOctave(self.bassline, self.tenorLine, num-1, i, True) and not self.isParallel5thOctave(self.supranoLine, self.tenorLine, num-1, i, False) and not self.isParallel5thOctave(self.altoLine, self.tenorLine, num-1, i, False):
                        if not self.isVoiceCrossing(self.bassline, num-1, i, True) and not self.isVoiceCrossing(self.altoLine, num-1, i, False):
                            self.tenorLine.append(allNotes[i:i+2])
                            lookingFor[2] = False
                            lastTenor = i
                            break

                if allNotes[i] == third and lookingFor[1] == True:
                    if not self.isParallel5thOctave(self.bassline, self.tenorLine, num-1, i, True) and not self.isParallel5thOctave(self.supranoLine, self.tenorLine, num-1, i, False) and not self.isParallel5thOctave(self.altoLine, self.tenorLine, num-1, i, False):
                        if not self.isVoiceCrossing(self.bassline, num-1, i, True) and not self.isVoiceCrossing(self.altoLine, num-1, i, False):
                            self.tenorLine.append(allNotes[i:i+2])
                            lookingFor[1] = False
                            lastTenor = i
                            break

                # check j
                if allNotes[j] == root and lookingFor[0] == True:
                    if not self.isParallel5thOctave(self.bassline, self.tenorLine, num-1, j, True) and not self.isParallel5thOctave(self.supranoLine, self.tenorLine, num-1, j, False) and not self.isParallel5thOctave(self.altoLine, self.tenorLine, num-1, j, False):
                        if not self.isVoiceCrossing(self.bassline, num-1, j, True) and not self.isVoiceCrossing(self.altoLine, num-1, j, False):
                            self.tenorLine.append(allNotes[j:j+2])
                            lookingFor[0] = False
                            lastTenor = j
                            break

                if allNotes[j] == fifth and lookingFor[2] == True:
                    if not self.isParallel5thOctave(self.bassline, self.tenorLine, num-1, j, True) and not self.isParallel5thOctave(self.supranoLine, self.tenorLine, num-1, j, False) and not self.isParallel5thOctave(self.altoLine, self.tenorLine, num-1, j, False):
                        if not self.isVoiceCrossing(self.bassline, num-1, j, True) and not self.isVoiceCrossing(self.altoLine, num-1, j, False):
                            self.tenorLine.append(allNotes[j:j+2])
                            lookingFor[2] = False
                            lastTenor = j
                            break

                if allNotes[j] == third and lookingFor[1] == True:
                    if not self.isParallel5thOctave(self.bassline, self.tenorLine, num-1, j, True) and not self.isParallel5thOctave(self.supranoLine, self.tenorLine, num-1, j, False) and not self.isParallel5thOctave(self.altoLine, self.tenorLine, num-1, j, False):
                        if not self.isVoiceCrossing(self.bassline, num-1, j, True) and not self.isVoiceCrossing(self.altoLine, num-1, j, False):
                            self.tenorLine.append(allNotes[j:j+2])
                            lookingFor[1] = False
                            lastTenor = j
                            break

                # setup backups just in case they need to be doubled
                if backUpFifth == "":
                    if allNotes[i] == fifth and not self.isParallel5thOctave(self.bassline, self.tenorLine, num-1, i, True) and not self.isParallel5thOctave(self.supranoLine, self.tenorLine, num-1, i, False) and not self.isParallel5thOctave(self.altoLine, self.tenorLine, num-1, i, False):
                        if not self.isVoiceCrossing(self.bassline, num-1, i, True) and not self.isVoiceCrossing(self.altoLine, num-1, i, False):
                            backUpFifth = allNotes[i:i+2]
                    elif allNotes[j] == fifth and not self.isParallel5thOctave(self.bassline, self.tenorLine, num-1, j, True) and not self.isParallel5thOctave(self.supranoLine, self.tenorLine, num-1, j, False) and not self.isParallel5thOctave(self.altoLine, self.tenorLine, num-1, j, False):
                        if not self.isVoiceCrossing(self.bassline, num-1, j, True) and not self.isVoiceCrossing(self.altoLine, num-1, j, False):
                            backUpFifth = allNotes[j:j+2]
                if backUpThird == "":
                    if allNotes[i] == fifth and not self.isParallel5thOctave(self.bassline, self.tenorLine, num-1, i, True) and not self.isParallel5thOctave(self.supranoLine, self.tenorLine, num-1, i, False) and not self.isParallel5thOctave(self.altoLine, self.tenorLine, num-1, i, False):
                        if not self.isVoiceCrossing(self.bassline, num-1, i, True) and not self.isVoiceCrossing(self.altoLine, num-1, i, False):
                            backUpThird = allNotes[i:i+2]
                    elif allNotes[j] == fifth and not self.isParallel5thOctave(self.bassline, self.tenorLine, num-1, j, True) and not self.isParallel5thOctave(self.supranoLine, self.tenorLine, num-1, j, False) and not self.isParallel5thOctave(self.altoLine, self.tenorLine, num-1, j, False):
                        if not self.isVoiceCrossing(self.bassline, num-1, j, True) and not self.isVoiceCrossing(self.altoLine, num-1, j, False):
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
                        break
                    elif counts[1] == 1 and backUpThird != "":
                        self.tenorLine.append(backUpThird)
                        counts[1] += 1
                        print("doubled 3rd in tenor")
                        break
                    else:
                        # BACKTRACKING
                        blacklist.append(self.altoLine[-1][0:1])
                        del self.altoLine[-1]
                        num -= 1
                        break
            num += 1

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
        self.printAllVoices()

if __name__ == "__main__":
    PartWriterImpl = PartWriter("C", "I V vi IV")
    PartWriterImpl.main()

# edge cases: 
# I ii IV V
