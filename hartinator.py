# add flat keys (only minor left)
# add functionality for different amount of parts and optional starting notes
# back track before doubling third or fifth
# if back track for a certain beat is 2 or 3 len then add 3rd or 5th

from constants import allNotes, bassRange, altoRange, tenorRange, sopranoRange, majorKeys, minorKeys
from chord import Chord

import os
import pygame
from random_words import RandomWords

class PartWriter:
    def __init__(self, key="C", chordProgression="I"):
        self.key = key
        self.chords = []

        self.chordProgression = chordProgression.split(" ") # convert from "I I I" to ["I", "I", "I"]
        for romanNumeral in self.chordProgression:
            self.chords.append(Chord(romanNumeral, self.key))
        self.sopranoLine = [""] * len(self.chords)
        self.altoLine = [""] * len(self.chords)
        self.tenorLine = [""] * len(self.chords)
        self.bassLine = []

    def printAllVoices(self):
        print("Soprano: " + str(self.sopranoLine))
        print("Alto:    " + str(self.altoLine))
        print("Tenor:   " + str(self.tenorLine))
        print("Bass:    " + str(self.bassLine))

    def printAllVoicesWithAccidentals(self):
        self.sopranoLineWithAccidentals = []
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

        self.sopranoLineWithAccidentals = line
        print("Soprano: " + str(line))

        self.altoLineWithAccidentals = []
        line = []

        for note in self.altoLine:
            if (note[0] + "#") in keystring:
                line.append(note[0] + "#" + note[1])
            elif (note[0] + "b") in keystring:
                line.append(note[0] + "b" + note[1])
            else:
                line.append(note)
        
        self.altoLineWithAccidentals = line
        print("Alto:    " + str(line))

        self.tenorLineWithAccidentals = []
        line = []

        for note in self.tenorLine:
            if (note[0] + "#") in keystring:
                line.append(note[0] + "#" + note[1])
            elif (note[0] + "b") in keystring:
                line.append(note[0] + "b" + note[1])
            else:
                line.append(note)

        self.tenorLineWithAccidentals = line                
        print("Tenor:   " + str(line))

        self.bassLineWithAccidentals = []
        line = []

        for note in self.bassLine:
            if (note[0] + "#") in keystring:
                line.append(note[0] + "#" + note[1])
            elif (note[0] + "b") in keystring:
                line.append(note[0] + "b" + note[1])
            else:
                line.append(note)

        self.bassLineWithAccidentals = line
        print("Bass:    " + str(line))

    def isParallel5thOctave(self, voice, otherVoices, beat, newNoteIndex):
        if beat < 0:
            return False

        newNote = allNotes[newNoteIndex:newNoteIndex+2]

        priorSoprano, priorAlto, priorTenor, priorBass = "", "", "", ""

        if len(self.sopranoLine) > beat:
            priorSoprano = self.sopranoLine[beat]
        if len(self.altoLine) > beat:
            priorAlto = self.altoLine[beat]
        if len(self.tenorLine) > beat:
            priorTenor = self.tenorLine[beat]
        if len(self.bassLine) > beat:
            priorBass = self.bassLine[beat]

        # check stagnant motion
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
                    if priorBass[0:1] == priorSoprano[0:1] and newNote[0:1] == self.sopranoLine[beat+1][0:1]:
                        return True
                    elif allNotes[allNotes.index(priorSoprano[0:1]) + 6] == priorBass[0:1] and allNotes[allNotes.index(self.sopranoLine[beat+1][0:1]) + 6] == newNote[0:1]:
                        return True

                elif otherVoice == "alto" and priorAlto:
                    if priorBass[0:1] == priorAlto[0:1] and newNote[0:1] == self.altoLine[beat+1][0:1]:
                        return True
                    elif allNotes[allNotes.index(priorAlto[0:1]) + 6] == priorBass[0:1] and allNotes[allNotes.index(self.altoLine[beat+1][0:1]) + 6] == newNote[0:1]:
                        return True

                elif priorTenor:
                    if priorBass[0:1] == priorTenor[0:1] and newNote[0:1] == self.tenorLine[beat+1][0:1]:
                        return True
                    elif allNotes[allNotes.index(priorTenor[0:1]) + 6] == priorBass[0:1] and allNotes[allNotes.index(self.tenorLine[beat+1][0:1]) + 6] == newNote[0:1]:
                        return True
            
            if voice == "tenor":
                if otherVoice == "soprano" and priorSoprano:
                    if priorTenor[0:1] == priorSoprano[0:1] and newNote[0:1] == self.sopranoLine[beat+1][0:1]:
                        return True
                elif allNotes[allNotes.index(priorSoprano[0:1]) + 6] == priorTenor[0:1] and allNotes[allNotes.index(self.sopranoLine[beat+1][0:1]) + 6] == newNote[0:1]:
                    return True

                elif otherVoice == "alto" and priorAlto:
                    if priorTenor[0:1] == priorAlto[0:1] and newNote[0:1] == self.altoLine[beat+1][0:1]:
                        return True
                    elif allNotes[allNotes.index(priorAlto[0:1]) + 6] == priorTenor[0:1] and allNotes[allNotes.index(self.altoLine[beat+1][0:1]) + 6] == newNote[0:1]:
                        return True

                elif priorBass:
                    if priorTenor[0:1] == priorBass[0:1] and newNote[0:1] == self.bassLine[beat+1][0:1]:
                        return True
                    elif allNotes[allNotes.index(priorBass[0:1]) + 8] == priorTenor[0:1] and allNotes[allNotes.index(self.bassLine[beat+1][0:1]) + 8] == newNote[0:1]:
                        return True
            
            if voice == "alto":
                if otherVoice == "soprano" and priorSoprano:
                    if priorAlto[0:1] == priorSoprano[0:1] and newNote[0:1] == self.sopranoLine[beat+1][0:1]:
                        return True
                elif allNotes[allNotes.index(priorSoprano[0:1]) + 6] == priorAlto[0:1] and allNotes[allNotes.index(self.sopranoLine[beat+1][0:1]) + 6] == newNote[0:1]:
                    return True

                elif otherVoice == "tenor" and priorTenor:
                    if priorAlto[0:1] == priorTenor[0:1] and newNote[0:1] == self.tenorLine[beat+1][0:1]:
                        return True
                    elif allNotes[allNotes.index(priorTenor[0:1]) + 8] == priorAlto[0:1] and allNotes[allNotes.index(self.tenorLine[beat+1][0:1]) + 8] == newNote[0:1]:
                        return True

                elif priorBass:
                    if priorAlto[0:1] == priorBass[0:1] and newNote[0:1] == self.bassLine[beat+1][0:1]:
                        return True
                    elif allNotes[allNotes.index(priorBass[0:1]) + 8] == priorAlto[0:1] and allNotes[allNotes.index(self.bassLine[beat+1][0:1]) + 8] == newNote[0:1]:
                        return True
            
            else: # soprano
                if otherVoice == "alto" and priorAlto:
                    if priorSoprano[0:1] == priorAlto[0:1] and newNote[0:1] == self.altoLine[beat+1][0:1]:
                        return True
                    elif allNotes[allNotes.index(priorAlto[0:1]) + 8] == priorSoprano[0:1] and allNotes[allNotes.index(self.altoLine[beat+1][0:1]) + 8] == newNote[0:1]:
                        return True

                elif otherVoice == "tenor" and priorTenor:
                    if priorSoprano[0:1] == priorTenor[0:1] and newNote[0:1] == self.tenorLine[beat+1][0:1]:
                        return True
                    elif allNotes[allNotes.index(priorTenor[0:1]) + 8] == priorSoprano[0:1] and allNotes[allNotes.index(self.tenorLine[beat+1][0:1]) + 8] == newNote[0:1]:
                        return True

                elif priorBass:
                    if priorSoprano[0:1] == priorBass[0:1] and newNote[0:1] == self.bassLine[beat+1][0:1]:
                        return True
                    elif allNotes[allNotes.index(priorBass[0:1]) + 8] == priorSoprano[0:1] and allNotes[allNotes.index(self.bassLine[beat+1][0:1]) + 8] == newNote[0:1]:
                        return True
            
        return False

    def isVoiceCrossing(self, voice, beat, newNoteIndex):
        if beat < 0:
            return False

        priorSoprano, priorAlto, priorTenor, priorBass = "", "", "", ""

        if self.sopranoLine[beat] != "":
            priorSoprano = allNotes.index(self.sopranoLine[beat])
        if self.altoLine[beat] != "":
            priorAlto = allNotes.index(self.altoLine[beat])
        if self.tenorLine[beat] != "":
            priorTenor = allNotes.index(self.tenorLine[beat])
        if self.bassLine[beat] != "":
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

    def isSpacingValid(self, voice, num, newNoteIndex):
        if voice == "soprano":
            if self.altoLine[num] != "":
                if newNoteIndex > allNotes.index(self.altoLine[num]) + 14:
                    return False

        if voice == "alto":
            if self.sopranoLine[num] != "":
                if newNoteIndex > allNotes.index(self.sopranoLine[num]) + 14:
                    return False
            if self.tenorLine[num] != "":
                if newNoteIndex > allNotes.index(self.tenorLine[num]) + 14:
                    return False
        
        if voice == "tenor":
            if self.altoLine[num] != "":
                if newNoteIndex > allNotes.index(self.altoLine[num]) + 14:
                    return False

        return True
        
    def writeBassLine(self):
        # good starting note
        lastNoteIndex = allNotes.index("C3")

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

    def writeLine(self, beat, voice):
        # this will properly unwind all of the pointless iterations
        if self.tenorLine[-1] != "":
            return
        chord = self.chords[beat]
        possibleValues = []
        counts = [0, 0, 0]

        if voice == "soprano":
            if self.bassLine[beat][0:1] == chord.root:
                counts[0] += 1
            i, j = allNotes.index("C5"), allNotes.index("C5")
            if beat != 0:
                i, j = allNotes.index(self.sopranoLine[beat-1]), allNotes.index(self.sopranoLine[beat-1])
            count = 0
            while count < 6:
                if not self.isParallel5thOctave("soprano", ["bass", "alto", "tenor"], beat-1, j) and not self.isVoiceCrossing("soprano", beat-1, j) and self.isSpacingValid("soprano", beat, j):
                    if allNotes[j] == chord.root[0:1] and counts[0] != 2:
                        possibleValues.append(allNotes[j:j+2])
                    if allNotes[j] == chord.third[0:1] and counts[1] == 0:
                        possibleValues.append(allNotes[j:j+2])
                    if allNotes[j] == chord.fifth[0:1] and counts[2] == 0:
                        possibleValues.append(allNotes[j:j+2])
                if not self.isParallel5thOctave("soprano", ["bass", "alto", "tenor"], beat-1, i) and not self.isVoiceCrossing("soprano", beat-1, i) and self.isSpacingValid("soprano", beat, i):
                    if allNotes[i] == chord.root[0:1] and counts[0] != 2:
                        possibleValues.append(allNotes[i:i+2])
                    if allNotes[i] == chord.third[0:1] and counts[1] == 0:
                        possibleValues.append(allNotes[i:i+2])
                    if allNotes[i] == chord.fifth[0:1] and counts[2] == 0:
                        possibleValues.append(allNotes[i:i+2])
                if i > sopranoRange[0]:
                    i -= 2
                if j < sopranoRange[1] + 2:
                    j += 2
                count += 1

            possibleValues = list(dict.fromkeys(possibleValues))
            for n in possibleValues:
                self.sopranoLine[beat] = n
                self.writeLine(beat, "alto")

        if voice == "alto":
            if self.bassLine[beat][0:1] == chord.root:
                counts[0] += 1
            if self.sopranoLine[beat][0:1] == chord.root:
                counts[0] += 1
            if self.sopranoLine[beat][0:1] == chord.third:
                counts[1] += 1
            elif self.sopranoLine[beat][0:1] == chord.fifth:
                counts[2] += 1
            i, j = allNotes.index("E4"), allNotes.index("E4")
            if beat != 0:
                i, j = allNotes.index(self.altoLine[beat-1]), allNotes.index(self.altoLine[beat-1])
            count = 0
            while count < 6:
                if not self.isParallel5thOctave("alto", ["bass", "soprano", "tenor"], beat-1, j) and not self.isVoiceCrossing("alto", beat-1, j) and self.isSpacingValid("alto", beat, j):
                    if allNotes[j] == chord.root[0:1] and counts[0] != 2:
                        possibleValues.append(allNotes[j:j+2])
                    if allNotes[j] == chord.third[0:1] and counts[1] == 0:
                        possibleValues.append(allNotes[j:j+2])
                    if allNotes[j] == chord.fifth[0:1] and counts[2] == 0:
                        possibleValues.append(allNotes[j:j+2])
                if not self.isParallel5thOctave("alto", ["bass", "soprano", "tenor"], beat-1, i) and not self.isVoiceCrossing("alto", beat-1, i) and self.isSpacingValid("alto", beat, i):
                    if allNotes[i] == chord.root[0:1] and counts[0] != 2:
                        possibleValues.append(allNotes[i:i+2])
                    if allNotes[i] == chord.third[0:1] and counts[1] == 0:
                        possibleValues.append(allNotes[i:i+2])
                    if allNotes[i] == chord.fifth[0:1] and counts[2] == 0:
                        possibleValues.append(allNotes[i:i+2])
                if i > altoRange[0]:
                    i -= 2
                if j < altoRange[1] + 2:
                    j += 2
                count += 1

            possibleValues = list(dict.fromkeys(possibleValues))
            for n in possibleValues:
                self.altoLine[beat] = n
                self.writeLine(beat, "tenor")

        if voice == "tenor":
            if self.bassLine[beat][0:1] == chord.root:
                counts[0] += 1
            if self.sopranoLine[beat][0:1] == chord.root:
                counts[0] += 1
            elif self.sopranoLine[beat][0:1] == chord.third:
                counts[1] += 1
            else:
                counts[2] += 1
            if self.altoLine[beat][0:1] == chord.root:
                counts[0] += 1
            elif self.altoLine[beat][0:1] == chord.third:
                counts[1] += 1
            else:
                counts[2] += 1

            i, j = allNotes.index("E4"), allNotes.index("E4")
            if beat != 0:
                i, j = allNotes.index(self.altoLine[beat-1]), allNotes.index(self.altoLine[beat-1])
            count = 0
            while count < 6:
                if not self.isParallel5thOctave("tenor", ["bass", "soprano", "alto"], beat-1, j) and not self.isVoiceCrossing("tenor", beat-1, j) and self.isSpacingValid("tenor", beat, j):
                    if allNotes[j] == chord.root[0:1] and counts[0] != 2:
                        possibleValues.append(allNotes[j:j+2])
                    if allNotes[j] == chord.third[0:1] and counts[1] == 0:
                        possibleValues.append(allNotes[j:j+2])
                    if allNotes[j] == chord.fifth[0:1] and counts[2] == 0:
                        possibleValues.append(allNotes[j:j+2])
                if not self.isParallel5thOctave("tenor", ["bass", "soprano", "alto"], beat-1, i) and not self.isVoiceCrossing("tenor", beat-1, i) and self.isSpacingValid("tenor", beat, i):
                    if allNotes[i] == chord.root[0:1] and counts[0] != 2:
                        possibleValues.append(allNotes[i:i+2])
                    if allNotes[i] == chord.third[0:1] and counts[1] == 0:
                        possibleValues.append(allNotes[i:i+2])
                    if allNotes[i] == chord.fifth[0:1] and counts[2] == 0:
                        possibleValues.append(allNotes[i:i+2])
                if i > tenorRange[0]:
                    i -= 2
                if j < tenorRange[1] + 2:
                    j += 2
                count += 1

            possibleValues = list(dict.fromkeys(possibleValues))
            for n in possibleValues:
                self.tenorLine[beat] = n
                if beat != len(self.chords) - 1:
                    self.writeLine(beat+1, "soprano")

    def writeAltoTenorAndSoprano(self):

        # good starting notes
        lastSoprano = allNotes.index("C5")
        lastAlto = allNotes.index("E4")
        lastTenor = allNotes.index("G3")

        # used to store notes in the soprano/alto that cause errors in the next beat (used for backtracking)
        sopranoBlacklist = []
        altoBlacklist = []

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

            i, j = lastSoprano, lastSoprano

            while True:
                backtrack = False

                # check j
                if not self.isParallel5thOctave("soprano", ["bass"], num-1, j) and not self.isVoiceCrossing("soprano", num-1, j) and self.isSpacingValid("soprano", num, j):

                    if allNotes[j] == chord.root[0:1] and lookingFor[0] == True and not allNotes[j] in sopranoBlacklist:
                        self.sopranoLine.append(allNotes[j:j+2])
                        counts[0] += 1
                        if counts[0] == 2:
                            lookingFor[0] = False
                        lastSoprano = j
                        break

                    if allNotes[j] == chord.third[0:1] and lookingFor[1] == True and not allNotes[j] in sopranoBlacklist:
                        self.sopranoLine.append(allNotes[j:j+2])
                        counts[1] += 1
                        lookingFor[1] = False
                        lastSoprano = j
                        break

                    if allNotes[j] == chord.fifth[0:1] and lookingFor[2] == True and not allNotes[j] in sopranoBlacklist:
                        self.sopranoLine.append(allNotes[j:j+2])
                        counts[2] += 1
                        lookingFor[2] = False
                        lastSoprano = j
                        break

                # check i
                if not self.isParallel5thOctave("soprano", ["bass"], num-1, i) and not self.isVoiceCrossing("soprano", num-1, i) and self.isSpacingValid("soprano", num, i):

                    if allNotes[i] == chord.root[0:1] and lookingFor[0] == True and not allNotes[i] in sopranoBlacklist:
                        self.sopranoLine.append(allNotes[i:i+2])
                        counts[0] += 1
                        if counts[0] == 2:
                            lookingFor[0] = False
                        lastSoprano = i
                        break

                    if allNotes[i] == chord.third[0:1] and lookingFor[1] == True and not allNotes[i] in sopranoBlacklist:
                        self.sopranoLine.append(allNotes[i:i+2])
                        counts[1] += 1
                        lookingFor[1] = False
                        lastSoprano = i
                        break

                    if allNotes[i] == chord.fifth[0:1] and lookingFor[2] == True and not allNotes[i] in sopranoBlacklist:
                        self.sopranoLine.append(allNotes[i:i+2])
                        counts[2] += 1
                        lookingFor[2] = False
                        lastSoprano = i
                        break

                if i > sopranoRange[0]:
                    i -= 2
                if j < sopranoRange[1] + 2:
                    j += 2
                if i <= sopranoRange[0] and j >= sopranoRange[1]:
                    sopranoBlacklist.append(self.sopranoLine[-1][0:1])
                    # altoBlacklist.append(self.altoLine[-1][0:1])
                    del self.altoLine[-1]
                    del self.sopranoLine[-1]
                    del self.tenorLine[-1]
                    backtrack = True
                    # print("backtrack: " + str(altoBlacklist) + " " + str(sopranoBlacklist) + " soprano " + str(num))
                    num -= 1
                    break

            if backtrack:
                continue

            # set pointers
            i, j = lastAlto, lastAlto

            # alto
            while True:
                backtrack = False

                # check j
                if not self.isVoiceCrossing("alto", num-1, j) and not self.isParallel5thOctave("alto", ["soprano", "bass"], num-1, j) and self.isSpacingValid("alto", num, j):

                    if allNotes[j] == chord.root[0:1] and lookingFor[0] == True and not allNotes[j] in altoBlacklist:
                        self.altoLine.append(allNotes[j:j+2])
                        counts[0] += 1
                        if counts[0] == 2:
                            lookingFor[0] = False
                        lastAlto = j
                        break

                    if allNotes[j] == chord.fifth[0:1] and not allNotes[j] in altoBlacklist:
                        if lookingFor[2] == True:
                            self.altoLine.append(allNotes[j:j+2])
                            lookingFor[2] = False
                            counts[2] += 1
                            lastAlto = j
                            break
                        elif not backUpFifth:
                            backUpFifth = allNotes[j:j+2]

                    if allNotes[j] == chord.third[0:1] and not allNotes[j] in altoBlacklist:
                        if lookingFor[1] == True:
                            self.altoLine.append(allNotes[j:j+2])
                            lookingFor[1] = False
                            counts[1] += 1
                            lastAlto = j
                            break
                        elif not backUpThird:
                            backUpThird = allNotes[j:j+2]

                # check i
                if not self.isVoiceCrossing("alto", num-1, i) and not self.isParallel5thOctave("alto", ["soprano", "bass"], num-1, i) and self.isSpacingValid("alto", num, i):

                    if allNotes[i] == chord.root[0:1] and lookingFor[0] == True and not allNotes[i] in altoBlacklist:
                        self.altoLine.append(allNotes[i:i+2])
                        lookingFor[0] = False
                        counts[0] += 1
                        lastAlto = i
                        break

                    if allNotes[i] == chord.fifth[0:1] and not allNotes[i] in altoBlacklist: 
                        if lookingFor[2] == True:
                            self.altoLine.append(allNotes[i:i+2])
                            lookingFor[2] = False
                            counts[2] += 1
                            lastAlto = i
                            break
                        elif not backUpFifth:
                            backUpFifth = allNotes[i:i+2]

                    if allNotes[i] == chord.third[0:1] and not allNotes[i] in altoBlacklist:
                        if lookingFor[1] == True:
                            self.altoLine.append(allNotes[i:i+2])
                            lookingFor[1] = False
                            counts[1] += 1
                            lastAlto = i
                            break
                        elif not backUpThird:
                            backUpThird = allNotes[i:i+2]

                # keep pointers within range
                if i > altoRange[0]:
                    i -= 2
                if j < altoRange[1] + 2:
                    j += 2

                # use backups if neccessary, prioritizing the fifth over the third
                if i <= altoRange[0] and j >= altoRange[1]:
                    if counts[2] != 2 and backUpFifth != "":
                        self.altoLine.append(backUpFifth)
                        counts[2] += 1
                        print("doubled 5th in alto on beat " + str(num+1))
                        altoBlacklist = []
                        break
                    elif backUpThird != "":
                        self.altoLine.append(backUpThird)
                        counts[1] += 1
                        print("doubled 3rd in alto on beat " + str(num+1))
                        altoBlacklist = []
                        break
                    else:
                    # BACKTRACKING
                        sopranoBlacklist.append(self.sopranoLine[-1][0:1])
                        del self.sopranoLine[-1]
                        backtrack = True
                        # print("backtrack: " + str(sopranoBlacklist) + " " + str(altoBlacklist) + " alto " + str(num))
                        break

            if backtrack: # this will proceed to re-write the soprano in this beat
                continue
        
            i, j = lastTenor, lastTenor

            backUpThird, backUpFifth = "", "" # reset to be used by tenor

            # tenor
            while True:
                backtrack = False

                # check i
                if not self.isVoiceCrossing("tenor", num-1, i) and not self.isParallel5thOctave("tenor", ["alto", "bass", "soprano"], num-1, i) and self.isSpacingValid("tenor", num, i):

                    if allNotes[i] == chord.root[0:1] and lookingFor[0] == True:
                        self.tenorLine.append(allNotes[i:i+2])
                        lookingFor[0] = False
                        counts[0] += 1
                        if counts[0] == 2:
                            lookingFor[0] = False
                        lastTenor = i
                        altoBlacklist, sopranoBlacklist = [], []
                        num += 1
                        break

                    if allNotes[i] == chord.fifth[0:1]:
                        if lookingFor[2] == True:
                            self.tenorLine.append(allNotes[i:i+2])
                            lookingFor[2] = False
                            counts[2] += 1
                            lastTenor = i
                            altoBlacklist, sopranoBlacklist = [], []
                            num += 1
                            break
                        elif not backUpFifth:
                            backUpFifth = allNotes[j:j+2]

                    if allNotes[i] == chord.third[0:1]:
                        if lookingFor[1] == True:
                            self.tenorLine.append(allNotes[i:i+2])
                            lookingFor[1] = False
                            counts[1] += 1
                            lastTenor = i
                            altoBlacklist, sopranoBlacklist = [], []
                            num += 1
                            break
                        elif not backUpThird:
                            backUpThird = allNotes[j:j+2]

                # check j
                if not self.isVoiceCrossing("tenor", num-1, j) and not self.isParallel5thOctave("tenor", ["alto", "bass", "soprano"], num-1, j) and self.isSpacingValid("tenor", num, j):

                    if allNotes[j] == chord.root[0:1] and lookingFor[0] == True:
                        self.tenorLine.append(allNotes[j:j+2])
                        lookingFor[0] = False
                        counts[0] += 1
                        if counts[0] == 2:
                            lookingFor[0] = False
                        lastTenor = j
                        altoBlacklist, sopranoBlacklist = [], []
                        num += 1
                        break

                    if allNotes[j] == chord.fifth[0:1]:
                        if lookingFor[2] == True:
                            self.tenorLine.append(allNotes[j:j+2])
                            lookingFor[2] = False
                            counts[2] += 1
                            lastTenor = j
                            altoBlacklist, sopranoBlacklist = [], []
                            num += 1
                            break
                        elif not backUpFifth:
                            backUpFifth = allNotes[j:j+2]
                            

                    if allNotes[j] == chord.third[0:1]:
                        if lookingFor[1] == True:
                            self.tenorLine.append(allNotes[j:j+2])
                            lookingFor[1] = False
                            counts[1] += 1
                            lastTenor = j
                            altoBlacklist, sopranoBlacklist = [], []
                            num += 1
                            break
                        elif not backUpThird:
                            backUpThird = allNotes[j:j+2]

                # keep pointers within range
                if i > tenorRange[0]:
                    i -= 2
                if j < tenorRange[1] + 2:
                    j += 2

                # use backups if neccessary, prioritizing the fifth over the third
                if i <= tenorRange[0] and j >= tenorRange[1]:
                    if backUpFifth:
                        self.tenorLine.append(backUpFifth)
                        counts[2] += 1
                        print("doubled 5th in tenor on beat " + str(num+1))
                        lastTenor = allNotes.index(backUpFifth)
                        altoBlacklist, sopranoBlacklist = [], []
                        num += 1
                        break
                    elif backUpThird:
                        self.tenorLine.append(backUpThird)
                        counts[1] += 1
                        print("doubled 3rd in tenor on beat " + str(num+1))
                        lastTenor = allNotes.index(backUpThird)
                        altoBlacklist, sopranoBlacklist = [], []
                        num += 1
                        break
                    else:
                        # BACKTRACKING
                        sopranoBlacklist.append(self.sopranoLine[-1][0:1])
                        altoBlacklist.append(self.altoLine[-1][0:1])
                        del self.altoLine[-1]
                        del self.sopranoLine[-1]
                        # print("backtrack: " + str(altoBlacklist) + " " + str(sopranoBlacklist) + " tenor " + str(num))
                        break

    def printChords(self):
        for chord in self.chords:
            print(chord.root + " " + chord.third + " " + chord.fifth)

    def addOctaveForLilypond(self, note):
        result = ""
        result += note[0]
        if "#" in note:
                result += "is"
        elif "b" in note:
            result += "es"
        if '2' in note:
            result += ","
        elif '4' in note:
            result += "\'"
        elif '5' in note:
            result += "\'\'"
        return result + " "

    def createSheetMusicPdf(self, createMidiFile):
        sopranoNotes, altoNotes, tenorNotes, bassNotes = "", "", "", ""

        for i in self.sopranoLineWithAccidentals:
            sopranoNotes += self.addOctaveForLilypond(i)
        for i in self.altoLineWithAccidentals:
            altoNotes += self.addOctaveForLilypond(i)
        for i in self.tenorLineWithAccidentals:
            tenorNotes += self.addOctaveForLilypond(i)
        for i in self.bassLineWithAccidentals:
            bassNotes += self.addOctaveForLilypond(i)

        self.fileName = RandomWords().random_word() + ".ly"

        fout = open("artifacts/" + self.fileName, "w")

        if self.key in majorKeys:
            quality = "\\major"
        else:
            quality = "\\minor"

        fileString = ""

        fileString += "global = { \\key " + self.key.lower() + " " + quality + " }" 
        fileString += "sopMusic = \\absolute { " + sopranoNotes.lower() + "}"
        fileString += "altoMusic = \\absolute { " + altoNotes.lower() + "}"
        fileString += "tenorMusic = \\absolute { " + tenorNotes.lower() + "}"
        fileString += "bassMusic = \\absolute { " + bassNotes.lower() + "}"
        fileString += "\\score { \\new ChoirStaff <<\\new Staff = \"women\" << \\new Voice = \"sopranos\" { \\voiceOne << \\global \\sopMusic >> }"
        fileString += "\\new Voice = \"altos\" { \\voiceTwo << \\global \\altoMusic >> } >>"
        fileString += "\\new Staff = \"men\" << \\clef bass \\new Voice = \"tenors\" { \\voiceOne << \\global \\tenorMusic >> }"
        fileString += "\\new Voice = \"basses\" { \\voiceTwo << \\global \\bassMusic >> } >> >> } \\version \"2.18.2\""
        
        fout.write(fileString)
        fout.close()

        os.system("lilypond --include /artifacts -o /artifacts " + self.fileName)
        os.system("open artifacts/" + self.fileName[0:-3] + ".pdf")
        print("Look for a file named \'" + self.fileName[0:-3] + ".pdf" + "\'!")
        if createMidiFile:
            fout = open("artifacts/" + self.fileName, "w")
            newFileString = fileString[0:fileString.index("score") + 8] + "\\midi { \\tempo 4 = 72 } " + fileString[fileString.index("score") + 8:-1] + fileString[-1]
            fout.write(newFileString)
            fout.close()
            os.system("lilypond --include /artifacts -o /artifacts " + self.fileName)
            print("The midi file will also have the same name!")

    def playMidiFile(self):
        midiFileName = self.fileName[0:-3] + ".midi"

        os.system("open -a GarageBand artifacts/" + midiFileName)

    def main(self):
        if self.key == None:
            self.key = input("What is the key?: ")
        if self.chordProgression == None:
            self.chordProgression = input("Enter a chord progression (seperated by spaces): ").split(" ")
        self.printChords()
        self.writeBassLine()
        # self.writeAltoTenorAndSoprano()
        self.writeLine(0, "soprano")
        print()
        self.printAllVoices()
        print()
        print("With accidentals: ")
        self.printAllVoicesWithAccidentals()
        self.createSheetMusicPdf(True)
        self.playMidiFile()

if __name__ == "__main__":
    PartWriterImpl = PartWriter("a", "i v VII v VI iv v v i iv VI v i VII v i")
    PartWriterImpl.main()

# edge cases: 
# I ii IV V key = C
# I IV vi V I IV V I

# meme cases
#I IV vi V I IV V I ii IV V vii vi IV ii V I IV vi IV vii vi V I


# IV - V