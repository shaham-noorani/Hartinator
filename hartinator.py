# add flat keys (only minor left)
# add functionality for different amount of parts and optional starting notes
# BACKBURNER be able to play the music
# BACKBURNER produce sheet music
# once tenor and alto break, back track soprano
# back track before doubling third or fifth
# write soprano, alto, and tenor at the same time

from constants import allNotes, bassRange, altoRange, tenorRange, sopranoRange, majorKeys, minorKeys
from chord import Chord

class PartWriter:
    def __init__(self, key="C", chordProgression="I"):
        self.key = key
        self.chords = []
        self.sopranoLine = []
        self.altoLine = []
        self.tenorLine = []
        self.bassLine = []

        self.chordProgression = chordProgression.split(" ") # convert from "I I I" to ["I", "I", "I"]
        for romanNumeral in self.chordProgression:
            self.chords.append(Chord(romanNumeral, self.key))

    def printAllVoices(self):
        print("Soprano: " + str(self.sopranoLine))
        print("Alto:    " + str(self.altoLine))
        print("Tenor:   " + str(self.tenorLine))
        print("Bass:    " + str(self.bassLine))

    def printAllVoicesWithAccidentals(self):
        line = []

        if self.key in majorKeys:
            keystring = majorKeys[self.key]
        else:
            keystring = minorKeys[self.key]

        for note in self.sopranoLine:
            if (note[0] + "#") in keystring:
                line.append(note[0] + "#" + note[1])
            elif (note[0] + "b") in keystring:
                line.append(note[0] + "b" + note[1])
            else:
                line.append(note)

        print("Soprano: " + str(line))

        line = []

        for note in self.altoLine:
            if (note[0] + "#") in keystring:
                line.append(note[0] + "#" + note[1])
            elif (note[0] + "b") in keystring:
                line.append(note[0] + "b" + note[1])
            else:
                line.append(note)
                
        print("Alto:    " + str(line))

        line = []

        for note in self.tenorLine:
            if (note[0] + "#") in keystring:
                line.append(note[0] + "#" + note[1])
            elif (note[0] + "b") in keystring:
                line.append(note[0] + "b" + note[1])
            else:
                line.append(note)
                
        print("Tenor:   " + str(line))

        line = []

        for note in self.bassLine:
            if (note[0] + "#") in keystring:
                line.append(note[0] + "#" + note[1])
            elif (note[0] + "b") in keystring:
                line.append(note[0] + "b" + note[1])
            else:
                line.append(note)
                
        print("Bass:    " + str(line))

    def isParallel5thOctave(self, voice, otherVoices, beat, newNoteIndex):
        if beat < 0:
            return False

        newNote = allNotes[newNoteIndex:newNoteIndex+2]

        priorSoprano, priorAlto, priorTenor, priorBass = "", "", "", ""

        if len(self.sopranoLine) > beat:
            priorSoprano = self.sopranoLine[beat-1]
        if len(self.altoLine) > beat:
            priorAlto = self.altoLine[beat-1]
        if len(self.tenorLine) > beat:
            priorTenor = self.tenorLine[beat-1]
        if len(self.bassLine) > beat:
            priorBass = self.bassLine[beat-1]

        if voice == "bass":
            if priorBass == newNote:
                return False
        if voice == "tenor":
            if priorTenor == newNote:
                return False
        if voice == "alto":
            if priorAlto == newNote:
                return False
        if voice == "soprano":
            if priorSoprano == newNote:
                return False

        for otherVoice in otherVoices:
            if voice == "bass":
                if otherVoice == "soprano" and priorSoprano:
                    if priorBass[0:1] == priorSoprano[0:1] and newNote[0:1] == self.sopranoLine[beat][0:1]:
                        return True
                    elif allNotes[allNotes.index(priorSoprano) + 6] == priorBass[0:1] and allNotes[allNotes.index(self.sopranoLine[beat]) + 6] == newNote[0:1]:
                        return True

                elif otherVoice == "alto" and priorAlto:
                    if priorBass[0:1] == priorAlto[0:1] and newNote[0:1] == self.altoLine[beat][0:1]:
                        return True
                    elif allNotes[allNotes.index(priorAlto) + 6] == priorBass[0:1] and allNotes[allNotes.index(self.altoLine[beat]) + 6] == newNote[0:1]:
                        return True

                elif priorTenor:
                    if priorBass[0:1] == priorTenor[0:1] and newNote[0:1] == self.tenorLine[beat][0:1]:
                        return True
                    elif allNotes[allNotes.index(priorTenor) + 6] == priorBass[0:1] and allNotes[allNotes.index(self.tenorLine[beat]) + 6] == newNote[0:1]:
                        return True
            
            if voice == "tenor":
                if otherVoice == "soprano" and priorSoprano:
                    if priorTenor[0:1] == priorSoprano[0:1] and newNote[0:1] == self.sopranoLine[beat][0:1]:
                        return True
                elif allNotes[allNotes.index(priorSoprano) + 6] == priorTenor[0:1] and allNotes[allNotes.index(self.sopranoLine[beat]) + 6] == newNote[0:1]:
                    return True

                elif otherVoice == "alto" and priorAlto:
                    if priorTenor[0:1] == priorAlto[0:1] and newNote[0:1] == self.altoLine[beat][0:1]:
                        return True
                    elif allNotes[allNotes.index(priorAlto) + 6] == priorTenor[0:1] and allNotes[allNotes.index(self.altoLine[beat]) + 6] == newNote[0:1]:
                        return True

                elif priorBass:
                    if priorTenor[0:1] == priorBass[0:1] and newNote[0:1] == self.bassLine[beat][0:1]:
                        return True
                    elif allNotes[allNotes.index(priorBass) + 8] == priorTenor[0:1] and allNotes[allNotes.index(self.bassLine[beat]) + 8] == newNote[0:1]:
                        return True
            
            if voice == "alto":
                if otherVoice == "soprano" and priorSoprano:
                    if priorAlto[0:1] == priorSoprano[0:1] and newNote[0:1] == self.sopranoLine[beat][0:1]:
                        return True
                elif allNotes[allNotes.index(priorSoprano) + 6] == priorAlto[0:1] and allNotes[allNotes.index(self.sopranoLine[beat]) + 6] == newNote[0:1]:
                    return True

                elif otherVoice == "alto" and priorTenor:
                    if priorAlto[0:1] == priorTenor[0:1] and newNote[0:1] == self.tenorLine[beat][0:1]:
                        return True
                    elif allNotes[allNotes.index(priorTenor) + 8] == priorAlto[0:1] and allNotes[allNotes.index(self.tenorLine[beat]) + 8] == newNote[0:1]:
                        return True

                elif priorBass:
                    if priorAlto[0:1] == priorBass[0:1] and newNote[0:1] == self.bassLine[beat][0:1]:
                        return True
                    elif allNotes[allNotes.index(priorBass) + 8] == priorAlto[0:1] and allNotes[allNotes.index(self.bassLine[beat]) + 8] == newNote[0:1]:
                        return True
            
            else: # soprano
                if otherVoice == "alto" and priorAlto:
                    if priorSoprano[0:1] == priorAlto[0:1] and newNote[0:1] == self.altoLine[beat][0:1]:
                        return True
                    elif allNotes[allNotes.index(priorAlto) + 8] == priorSoprano[0:1] and allNotes[allNotes.index(self.altoLine[beat]) + 8] == newNote[0:1]:
                        return True

                elif otherVoice == "alto" and priorTenor:
                    if priorSoprano[0:1] == priorTenor[0:1] and newNote[0:1] == self.tenorLine[beat][0:1]:
                        return True
                    elif allNotes[allNotes.index(priorTenor) + 8] == priorSoprano[0:1] and allNotes[allNotes.index(self.tenorLine[beat]) + 8] == newNote[0:1]:
                        return True

                elif priorBass:
                    if priorSoprano[0:1] == priorBass[0:1] and newNote[0:1] == self.bassLine[beat][0:1]:
                        return True
                    elif allNotes[allNotes.index(priorBass) + 8] == priorSoprano[0:1] and allNotes[allNotes.index(self.bassLine[beat]) + 8] == newNote[0:1]:
                        return True
            
        return False

    def isVoiceCrossing(self, voice, beat, newNoteIndex):
        if beat < 0:
            return False

        priorSoprano, priorAlto, priorTenor, priorBass = "", "", "", ""

        if len(self.sopranoLine) > beat+1:
            priorSoprano = allNotes.index(self.sopranoLine[beat])
        if len(self.altoLine) > beat+1:
            priorAlto = allNotes.index(self.altoLine[beat])
        if len(self.tenorLine) > beat+1:
            priorTenor = allNotes.index(self.tenorLine[beat])
        if len(self.bassLine) > beat+1:
            priorBass = allNotes.index(self.bassLine[beat])

        if voice == "soprano" and priorAlto:
            if newNoteIndex < priorAlto:
                return True

        if voice == "alto" and priorSoprano:
            if newNoteIndex > priorSoprano:
                return True

        if voice == "alto" and priorTenor:
            if newNoteIndex < priorTenor:
                return True

        if voice == "tenor" and priorAlto:
            if newNoteIndex > priorAlto:
                return True

        if voice == "tenor" and priorBass:
            if newNoteIndex < priorBass:
                return True

        if voice == "bass" and priorTenor:
            if newNoteIndex > priorTenor:
                return True

        return False

    def writeBassLine(self):
        # good starting note
        lastNoteIndex = int((bassRange[1] - bassRange[0]) / 2 + bassRange[0])

        # write rest of bassLine
        for chord in self.chords:
            i, j = lastNoteIndex, lastNoteIndex
            while True:
                if allNotes[i] == chord.root[0:1]:
                    self.bassLine.append(allNotes[i:i+2])
                    lastNoteIndex = i
                    break
                elif allNotes[j] == chord.root[0:1]:
                    self.bassLine.append(allNotes[j:j+2])
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
        
    def writeSopranoLine(self):

        # good starting note
        lastNoteIndex = int((sopranoRange[1] - sopranoRange[0]) / 2) + sopranoRange[0]

        for num, chord in enumerate(self.chords):
            i, j = lastNoteIndex, lastNoteIndex

            while True:
                if not self.isParallel5thOctave("soprano", ["bass"], num-1, j):

                    if allNotes[j] == chord.root[0:1]:
                            self.sopranoLine.append(allNotes[j:j+2])
                            lastNoteIndex = j
                            break
                    if allNotes[i] == chord.root[0:1]:
                        self.sopranoLine.append(allNotes[i:i+2])
                        lastNoteIndex = i
                        break

                    if allNotes[j] == chord.fifth[0:1]:
                        self.sopranoLine.append(allNotes[j:j+2])
                        lastNoteIndex = j
                        break     
                    elif allNotes[i] == chord.fifth[0:1]:
                        self.sopranoLine.append(allNotes[i:i+2])
                        lastNoteIndex = i
                        break

                    if allNotes[j] == chord.third[0:1]:
                        self.sopranoLine.append(allNotes[j:j+2])
                        lastNoteIndex = j
                        break
                    elif allNotes[i] == chord.third[0:1]:
                        self.sopranoLine.append(allNotes[i:i+2])
                        lastNoteIndex = i
                        break

                # make sure the range is not being left
                if i > sopranoRange[0]:
                    i -= 2
                if j < sopranoRange[1]:
                    j += 2
                if i <= sopranoRange[0] and j >= sopranoRange[1]:
                    print("shit") # this should never happen
                    break

    def writeAltoAndTenor(self):

        # good starting notes
        lastAlto = int((altoRange[1] - altoRange[0]) / 2 + altoRange[0])
        lastTenor = int((tenorRange[1] - tenorRange[0]) / 2 + tenorRange[0])

        # used to store notes in the alto that cause errors in the next mesure for backtracking
        blacklist = []

        num = 0
        while num < len(self.chords):
            chord = self.chords[num]
            backtrack = False

            # frequency of each chord member
            counts = [0, 0, 0]

            lookingFor = [True, True, True]

            # just in case the third of fifth need to be doubled
            backUpThird, backUpFifth = "", ""

            # update counts of each chord member
            if self.bassLine[num][0:1] == chord.root[0:1]:
                counts[0] += 1
            
            if self.sopranoLine[num][0:1] == chord.root[0:1]:
                counts[0] += 1

            if self.sopranoLine[num][0:1] == chord.fifth[0:1]:
                counts[2] = 1

            if self.sopranoLine[num][0:1] == chord.third[0:1]:
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
                if not self.isVoiceCrossing("alto", num-1, j) and not self.isParallel5thOctave("alto", ["suprano"], num-1, j):

                    if allNotes[j] == chord.root[0:1] and lookingFor[0] == True and not allNotes[j] in blacklist:
                        self.altoLine.append(allNotes[j:j+2])
                        counts[0] += 1
                        if counts[0] == 2:
                            lookingFor[0] = False
                        lastAlto = j
                        blacklist = []
                        backtrack = False
                        break

                    if allNotes[j] == chord.fifth[0:1] and not allNotes[j] in blacklist:
                        if lookingFor[2] == True:
                            self.altoLine.append(allNotes[j:j+2])
                            lookingFor[2] = False
                            counts[2] += 1
                            lastAlto = j
                            blacklist = []
                            backtrack = False
                            break
                        elif not backUpFifth:
                            backUpFifth = allNotes[j:j+2]

                    if allNotes[j] == chord.third[0:1] and not allNotes[j] in blacklist:
                        if lookingFor[1] == True:
                            self.altoLine.append(allNotes[j:j+2])
                            lookingFor[1] = False
                            counts[1] += 1
                            lastAlto = j
                            blacklist = []
                            backtrack = False
                            break
                        elif not backUpThird:
                            backUpThird = allNotes[j:j+2]

                # check i
                if not self.isVoiceCrossing("alto", num-1, i) and not self.isParallel5thOctave("alto", ["suprano"], num-1, i):

                    if allNotes[i] == chord.root[0:1] and lookingFor[0] == True and not allNotes[i] in blacklist:
                        self.altoLine.append(allNotes[i:i+2])
                        lookingFor[0] = False
                        counts[0] += 1
                        lastAlto = i
                        blacklist = []
                        backtrack = False
                        break

                    if allNotes[i] == chord.fifth[0:1] and not allNotes[i] in blacklist: 
                        if lookingFor[2] == True:
                            self.altoLine.append(allNotes[i:i+2])
                            lookingFor[2] = False
                            counts[2] += 1
                            lastAlto = i
                            blacklist = []
                            backtrack = False
                            break
                        elif not backUpFifth:
                            backUpFifth = allNotes[i:i+2]

                    if allNotes[i] == chord.third[0:1] and not allNotes[i] in blacklist:
                        if lookingFor[1] == True:
                            self.altoLine.append(allNotes[i:i+2])
                            lookingFor[1] = False
                            counts[1] += 1
                            lastAlto = i
                            blacklist = []
                            backtrack = False
                            break
                        elif not backUpThird:
                            backUpThird = allNotes[i:i+2]

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
                        print("doubled 5th in alto on beat " + str(num+1))
                        break
                    elif backUpThird != "":
                        self.altoLine.append(backUpThird)
                        backtrack = False
                        counts[1] += 1
                        print("doubled 3rd in alto on beat" + str(num+1))
                        break
                    else:
                        # BACKTRACKING
                        blacklist.append(self.altoLine[-1][0:1])
                        del self.altoLine[-1]
                        del self.tenorLine[-1]
                        backtrack = True
                        num -= 1
                        break

            if backtrack: # so the something isn't added to the tenor
                continue
        
            i, j = lastTenor, lastTenor

            backUpThird, backUpFifth = "", "" # reset to be used by tenor

            # tenor
            while True:

                # check i
                if not self.isVoiceCrossing("tenor", num-1, i) and not self.isParallel5thOctave("tenor", ["alto", "bass"], num-1, i):

                    if allNotes[i] == chord.root[0:1] and lookingFor[0] == True:
                        self.tenorLine.append(allNotes[i:i+2])
                        lookingFor[0] = False
                        lastTenor = i
                        break

                    if allNotes[i] == chord.fifth[0:1] and lookingFor[2] == True:
                        self.tenorLine.append(allNotes[i:i+2])
                        lookingFor[2] = False
                        lastTenor = i
                        break

                    if allNotes[i] == chord.third[0:1] and lookingFor[1] == True:
                        self.tenorLine.append(allNotes[i:i+2])
                        lookingFor[1] = False
                        lastTenor = i
                        break

                # check j
                if not self.isVoiceCrossing("tenor", num-1, j) and not self.isParallel5thOctave("tenor", ["alto", "bass"], num-1, j):

                    if allNotes[j] == chord.root[0:1] and lookingFor[0] == True:
                        self.tenorLine.append(allNotes[j:j+2])
                        lookingFor[0] = False
                        lastTenor = j
                        break

                    if allNotes[j] == chord.fifth[0:1]:
                        if lookingFor[2] == True:
                            self.tenorLine.append(allNotes[j:j+2])
                            lookingFor[2] = False
                            lastTenor = j
                            break
                        elif not backUpFifth:
                            backUpFifth = allNotes[j:j+2]
                            

                    if allNotes[j] == chord.third[0:1]:
                        if lookingFor[1] == True:
                            self.tenorLine.append(allNotes[j:j+2])
                            lookingFor[1] = False
                            lastTenor = j
                            break
                        elif not backUpThird:
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
                        print("doubled 5th in tenor on beat " + str(num+1))
                        break
                    elif counts[1] == 1 and backUpThird != "":
                        self.tenorLine.append(backUpThird)
                        counts[1] += 1
                        print("doubled 3rd in tenor on beat " + str(num+1))
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
            print(chord.root + " " + chord.third + " " + chord.fifth)


    def main(self):
        if self.key == None:
            self.key = input("What is the key?: ")
        if self.chordProgression == None:
            self.chordProgression = input("Enter a chord progression (seperated by spaces): ").split(" ")
        self.printChords()
        self.writeBassLine()
        self.writeSopranoLine()
        self.writeAltoAndTenor()
        self.printAllVoices()
        # self.printAllVoicesWithAccidentals()

if __name__ == "__main__":
    PartWriterImpl = PartWriter("E", "I V I")
    PartWriterImpl.main()

# edge cases: 
# I ii IV V
# I IV vi V I IV V I