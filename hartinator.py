# add flat keys (only minor left)
# add functionality for different amount of parts and optional starting notes
# back track before doubling third or fifth
# make the blacklist a matrix
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

    def updateChordMemberFrequency(self, counts, beat, chord):
        lastBass = self.bassLine[beat][0:1]
        lastAlto = self.altoLine[beat][0:1]
        lastSoprano = self.sopranoLine[beat][0:1]
        if lastBass == chord.root:
            counts[0] += 1
        if lastSoprano == chord.root:
            counts[0] += 1
        if lastAlto == chord.root:
            counts[0] += 1
        if lastSoprano == chord.third:
            counts[1] += 1
        if lastBass == chord.third:
            counts[1] += 1
        if lastAlto == chord.third:
            counts[1] += 1
        if lastBass == chord.fifth:
            counts[2] += 1
        if lastSoprano == chord.fifth:
            counts[2] += 1
        if lastAlto == chord.fifth:
            counts[2] += 1
        
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
        self.updateChordMemberFrequency(counts, beat, chord)

        if voice == "soprano":
            i, j = allNotes.index("C5"), allNotes.index("C5")
            if beat != 0:
                i, j = allNotes.index(self.sopranoLine[beat-1]), allNotes.index(self.sopranoLine[beat-1])
            count = 0
            while count < 4:
                if not self.isParallel5thOctave("soprano", ["bass", "alto", "tenor"], beat-1, j) and not self.isVoiceCrossing("soprano", beat-1, j) and self.isSpacingValid("soprano", beat, j):
                    if allNotes[j] == chord.root[0:1] and counts[0] != 2:
                        possibleValues.append(allNotes[j:j+2])
                    if allNotes[j] == chord.third[0:1] and counts[1] != 2:
                        possibleValues.append(allNotes[j:j+2])
                    if allNotes[j] == chord.fifth[0:1] and counts[2] == 0:
                        possibleValues.append(allNotes[j:j+2])
                if not self.isParallel5thOctave("soprano", ["bass", "alto", "tenor"], beat-1, i) and not self.isVoiceCrossing("soprano", beat-1, i) and self.isSpacingValid("soprano", beat, i):
                    if allNotes[i] == chord.root[0:1] and counts[0] != 2:
                        possibleValues.append(allNotes[i:i+2])
                    if allNotes[i] == chord.third[0:1] and counts[1] != 2:
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
            i, j = allNotes.index("E4"), allNotes.index("E4")
            if beat != 0:
                i, j = allNotes.index(self.altoLine[beat-1]), allNotes.index(self.altoLine[beat-1])
            count = 0
            while count < 4:
                if not self.isParallel5thOctave("alto", ["bass", "soprano", "tenor"], beat-1, j) and not self.isVoiceCrossing("alto", beat-1, j) and self.isSpacingValid("alto", beat, j):
                    if allNotes[j] == chord.root[0:1] and counts[0] != 2:
                        possibleValues.append(allNotes[j:j+2])
                    if allNotes[j] == chord.third[0:1] and counts[1] != 2:
                        possibleValues.append(allNotes[j:j+2])
                    if allNotes[j] == chord.fifth[0:1] and counts[2] == 0:
                        possibleValues.append(allNotes[j:j+2])
                if not self.isParallel5thOctave("alto", ["bass", "soprano", "tenor"], beat-1, i) and not self.isVoiceCrossing("alto", beat-1, i) and self.isSpacingValid("alto", beat, i):
                    if allNotes[i] == chord.root[0:1] and counts[0] != 2:
                        possibleValues.append(allNotes[i:i+2])
                    if allNotes[i] == chord.third[0:1] and counts[1] != 2:
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
            i, j = allNotes.index("E4"), allNotes.index("E4")
            if beat != 0:
                i, j = allNotes.index(self.tenorLine[beat-1]), allNotes.index(self.tenorLine[beat-1])
            count = 0
            while count < 4:
                if not self.isParallel5thOctave("tenor", ["bass", "soprano", "alto"], beat-1, j) and not self.isVoiceCrossing("tenor", beat-1, j) and self.isSpacingValid("tenor", beat, j):
                    if allNotes[j] == chord.root[0:1] and counts[0] != 2:
                        possibleValues.append(allNotes[j:j+2])
                    if allNotes[j] == chord.third[0:1] and counts[1] != 2:
                        possibleValues.append(allNotes[j:j+2])
                    if allNotes[j] == chord.fifth[0:1] and counts[2] == 0:
                        possibleValues.append(allNotes[j:j+2])
                if not self.isParallel5thOctave("tenor", ["bass", "soprano", "alto"], beat-1, i) and not self.isVoiceCrossing("tenor", beat-1, i) and self.isSpacingValid("tenor", beat, i):
                    if allNotes[i] == chord.root[0:1] and counts[0] != 2:
                        possibleValues.append(allNotes[i:i+2])
                    if allNotes[i] == chord.third[0:1] and counts[1] != 2:
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
        self.writeLine(0, "soprano")
        print()
        self.printAllVoices()
        print()
        # print("With accidentals: ")
        self.printAllVoicesWithAccidentals()
        self.createSheetMusicPdf(True)
        self.playMidiFile()

if __name__ == "__main__":
    PartWriterImpl = PartWriter("C", "I IV vi V I IV V I ii IV V vii vi IV ii V I IV vi IV vii vi V I")
    PartWriterImpl.main()

# edge cases: 
# I ii IV V key = C
# I IV vi V I IV V I

# meme cases
#I IV vi V I IV V I ii IV V vii vi IV ii V I IV vi IV vii vi V I


# IV - V