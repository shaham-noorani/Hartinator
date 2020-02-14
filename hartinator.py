# add flat keys (only minor left)
# correct doubling with inversions

from constants import allNotes, bassRange, altoRange, tenorRange, sopranoRange, majorKeys, minorKeys, voicesInOrder, goodStartingNotes, ranges
from chord import Chord

import os
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

    def updateVoicesDictionary(self):
        self.voices = {"soprano": self.sopranoLine, "alto": self.altoLine, "tenor": self.tenorLine, "bass": self.bassLine}

    def printAllVoices(self):
        print("Soprano: " + str(self.sopranoLine))
        print("Alto:    " + str(self.altoLine))
        print("Tenor:   " + str(self.tenorLine))
        print("Bass:    " + str(self.bassLine))

    def printAllVoicesWithAccidentals(self):
        self.updateVoicesDictionary()
        i = 0
        for voice in voicesInOrder:
            line = []

            if self.key in majorKeys:
                keystring = majorKeys[self.key]
            else:
                keystring = minorKeys[self.key]

            for note in self.voices[voice]:
                if (note[0] + "#") in keystring:
                    line.append(note[0] + "#" + note[1])
                elif (note[0] + "b") in keystring:
                    line.append(note[0] + "b" + note[1])
                else:
                    line.append(note)

            if i == 0:
                self.sopranoLineWithAccidentals = line
            if i == 1:
                self.altoLineWithAccidentals = line
            if i == 2:
                self.tenorLineWithAccidentals = line
            if i == 3:
                self.bassLineWithAccidentals = line
            print(voicesInOrder[i] + ": " + str(line))
            i += 1

    def is7thResolved(self, voice, beat, newNoteIndex):
        seventh = majorKeys[self.key][-2]
        newNoteIsTonic = self.key == allNotes[newNoteIndex][0:1]
        if beat == 0:
            return True
        if voice == "soprano":
            if self.sopranoLine[beat-1][0:1] == seventh:
                if not newNoteIsTonic:
                    return False
        if voice == "bass":
            if self.bassLine[beat-1][0:1] == seventh:
                if not newNoteIsTonic:
                    return False
        return True

    def isParallel5thOctave(self, voice, beat, newNoteIndex): 
        if beat == 0:
            return False
        
        self.updateVoicesDictionary()
        newNote = allNotes[newNoteIndex:newNoteIndex+1]
        priorNotes = dict()

        # define prior notes to be compared to later
        for i in voicesInOrder:
            priorNotes[i] = self.voices[i][beat-1][0:1]

        # check stagnant motion
        if priorNotes[voice] == newNote:
            return False

        # check against prior notes for parallel 5th/octaves
        for i in voicesInOrder:
            if i != voice:
                if priorNotes[i]:
                    if priorNotes[i] == priorNotes[voice] and newNote == self.voices[i][beat][0:1]:
                        return True
                    if voicesInOrder.index(i) > voicesInOrder.index(voice):
                        if allNotes[allNotes.index(priorNotes[i][0:1]) + 6] == priorNotes[voice][0:1] and allNotes[allNotes.index(self.voices[i][beat][0:1]) + 6] == newNote[0:1]:
                            return True 
                    elif allNotes[allNotes.index(priorNotes[i][0:1]) + 8] == priorNotes[voice][0:1] and allNotes[allNotes.index(self.voices[i][beat][0:1]) + 8] == newNote[0:1]:
                        return True 
            
        return False

    def isVoiceCrossing(self, voice, beat, newNoteIndex):
        if beat < 0:
            return False
        
        self.updateVoicesDictionary()
        priorNoteIndexes = dict()

        # define prior notes dict to be compared to later
        for i in voicesInOrder:
            priorNoteIndexes[i] = allNotes.index(self.voices[i][beat])

        if voice == "soprano" and priorNoteIndexes["alto"]:
            if newNoteIndex < priorNoteIndexes["alto"]:
                return True

        if voice == "alto" and priorNoteIndexes["soprano"]:
            if newNoteIndex > priorNoteIndexes["soprano"]:
                return True

        if voice == "alto" and priorNoteIndexes["tenor"]:
            if newNoteIndex < priorNoteIndexes["tenor"]:
                return True

        if voice == "tenor" and priorNoteIndexes["alto"]:
            if newNoteIndex > priorNoteIndexes["alto"]:
                return True

        if voice == "tenor" and priorNoteIndexes["bass"]:
            if newNoteIndex < priorNoteIndexes["bass"]:
                return True

        if voice == "bass" and priorNoteIndexes["tenor"]:
            if newNoteIndex > priorNoteIndexes["tenor"]:
                return True

        return False

    def isSpacingValid(self, voice, beat, newNoteIndex):
        if voice == "soprano":
            if self.altoLine[beat] != "":
                if newNoteIndex > allNotes.index(self.altoLine[beat]) + 14:
                    return False

        if voice == "alto":
            if self.sopranoLine[beat] != "":
                if newNoteIndex > allNotes.index(self.sopranoLine[beat]) + 14:
                    return False
            if self.tenorLine[beat] != "":
                if newNoteIndex > allNotes.index(self.tenorLine[beat]) + 14:
                    return False
        
        if voice == "tenor":
            if self.altoLine[beat] != "":
                if newNoteIndex > allNotes.index(self.altoLine[beat]) + 14:
                    return False

        return True

    def followsAllVoiceLeading(self, voice, beat, newNoteIndex):
        return self.is7thResolved(voice, beat, newNoteIndex) and not self.isParallel5thOctave(voice, beat, newNoteIndex) and not self.isVoiceCrossing(voice, beat, newNoteIndex) and self.isSpacingValid(voice, beat, newNoteIndex)

    def removeBadNotes(self, possibleNotes, counts, voice, chord):
        for n in possibleNotes:
            if voice == "tenor":
                if n[0] == chord.fifth and counts[1] == 0:
                    possibleNotes.remove(n)
                if n[0] == chord.third and counts[1] == 1:
                    possibleNotes.remove(n)
                if n[0] == chord.third and (counts[1] == 0 or counts[2] == 0):
                    possibleNotes.remove(n)
            if voice == "alto":
                if n[0] == chord.root and counts[0] == 2:
                    possibleNotes.remove(n)

    def updateChordMemberFrequency(self, counts, beat, chord):
        self.updateVoicesDictionary()

        for i in voicesInOrder:
            curr = self.voices[i][beat][0:1]
            if curr == chord.root:
                counts[0] += 1
            elif curr == chord.third:
                counts[1] += 1
            elif curr == chord.fifth:
                counts[2] += 1
        
    def writeBassLine(self):
        # good starting note
        lastNoteIndex = allNotes.index(goodStartingNotes["bass"])

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
                    break

    def writeLine(self, beat, voice, note=""):
        # this will properly unwind all of the pointless recursions
        if not "" in self.tenorLine:
            return
        
        chord = self.chords[beat]
        possibleNotes = []
        counts = [0, 0, 0]
        
        # new stuff
        i, j = allNotes.index(goodStartingNotes[voice]), allNotes.index(goodStartingNotes[voice])
        if beat != 0:
            i, j = allNotes.index(self.voices[voice][beat-1]), allNotes.index(self.voices[voice][beat-1])
        if voice == "soprano":
            self.tenorLine[beat-1] = note

        count = 0
        self.updateChordMemberFrequency(counts, beat, chord)

        while count < 4:
            if self.followsAllVoiceLeading(voice, beat, j):
                if allNotes[j] in [chord.root[0:1], chord.third[0:1], chord.fifth[0:1]]:
                    possibleNotes.append(allNotes[j:j+2])
            if self.followsAllVoiceLeading(voice, beat, i):
                if allNotes[i] in [chord.root[0:1], chord.third[0:1], chord.fifth[0:1]]:
                    possibleNotes.append(allNotes[i:i+2])
            if i > ranges[voice][0]:
                i -= 2
            if j < ranges[voice][1]:
                j += 2
            count += 1

        possibleNotes = list(dict.fromkeys(possibleNotes)) # removes duplicates
        self.removeBadNotes(possibleNotes, counts, voice, chord)
        for n in possibleNotes:
            self.updateVoicesDictionary()
            if voice != "tenor":
                nextVoice = voicesInOrder[voicesInOrder.index(voice) + 1]
            else:
                beat += 1
                nextVoice = "soprano"
            self.writeLine(beat, nextVoice, n)

        # old stuff
        # if voice == "soprano":
        #     i, j = goodStartingNotes["soprano"], goodStartingNotes["soprano"]
        #     if beat != 0:
        #         i, j = allNotes.index(self.voices["soprano"][beat-1]), allNotes.index(self.voices["soprano"][beat-1])
        #         self.tenorLine[beat-1] = note
        #     count = 0
        #     self.updateChordMemberFrequency(counts, beat, chord)
        #     while count < 4:
        #         if not self.isParallel5thOctave("soprano", beat-1, j) and not self.isVoiceCrossing("soprano", beat-1, j) and self.isSpacingValid("soprano", beat, j) and self.is7thResolved("soprano", beat, j):
        #             if allNotes[j] == chord.root[0:1] or allNotes[j] == chord.third[0:1] or allNotes[j] == chord.fifth[0:1]:
        #                 possibleNotes.append(allNotes[j:j+2])
        #         if not self.isParallel5thOctave("soprano", beat-1, i) and not self.isVoiceCrossing("soprano", beat-1, i) and self.isSpacingValid("soprano", beat, i) and self.is7thResolved("soprano", beat, i):
        #             if allNotes[i] == chord.root[0:1] or allNotes[i] == chord.third[0:1] or allNotes[i] == chord.fifth[0:1]:
        #                 possibleNotes.append(allNotes[i:i+2])
        #         if i > sopranoRange[0]:
        #             i -= 2
        #         if j < sopranoRange[1]:
        #             j += 2
        #         count += 1

        #     possibleNotes = list(dict.fromkeys(possibleNotes))
        #     for n in possibleNotes:
        #         self.updateVoicesDictionary()
        #         self.writeLine(beat, "alto", n)

        # if voice == "alto":
        #     self.sopranoLine[beat] = note
        #     i, j = goodStartingNotes["alto"], goodStartingNotes["alto"]
        #     if beat != 0:
        #         i, j = allNotes.index(self.voices["alto"][beat-1]), allNotes.index(self.voices["alto"][beat-1])
        #     count = 0
        #     self.updateChordMemberFrequency(counts, beat, chord)
        #     while count < 4:
        #         if not self.isParallel5thOctave("alto", beat-1, j) and not self.isVoiceCrossing("alto", beat-1, j) and self.isSpacingValid("alto", beat, j):
        #             if allNotes[j] == chord.root[0:1] and counts[0] < 2:
        #                 possibleNotes.append(allNotes[j:j+2])
        #             if allNotes[j] == chord.third[0:1]:
        #                 if counts[1] == 0:
        #                     possibleNotes.append(allNotes[j:j+2])
        #                 elif backupThird == "":
        #                     backupThird = allNotes[j:j+2]
        #             if allNotes[j] == chord.fifth[0:1] and counts[2] < 2:
        #                 possibleNotes.append(allNotes[j:j+2])
        #         if not self.isParallel5thOctave("alto", beat-1, i) and not self.isVoiceCrossing("alto", beat-1, i) and self.isSpacingValid("alto", beat, i):
        #             if allNotes[i] == chord.root[0:1] and counts[0] < 2:
        #                 possibleNotes.append(allNotes[i:i+2])
        #             if allNotes[i] == chord.third[0:1]:
        #                 if counts[1] == 0:
        #                     possibleNotes.append(allNotes[i:i+2])
        #                 elif backupThird == "":
        #                     backupThird = allNotes[i:i+2]
        #             if allNotes[i] == chord.fifth[0:1] and counts[2] < 2:
        #                 possibleNotes.append(allNotes[i:i+2])
        #         if i > altoRange[0]:
        #             i -= 2
        #         if j < altoRange[1]:
        #             j += 2
        #         count += 1

        #     possibleNotes = list(dict.fromkeys(possibleNotes))
        #     for n in possibleNotes:
        #         self.updateVoicesDictionary()
        #         self.writeLine(beat, "tenor", n)

        # if voice == "tenor":
        #     self.altoLine[beat] = note
        #     i, j = goodStartingNotes["tenor"], goodStartingNotes["tenor"]
        #     if beat != 0:
        #         i, j = allNotes.index(self.voices["tenor"][beat-1]), allNotes.index(self.voices["tenor"][beat-1])
        #     count = 0
        #     self.updateChordMemberFrequency(counts, beat, chord)
        #     while count < 4:
        #         if not self.isParallel5thOctave("tenor", beat-1, j) and not self.isVoiceCrossing("tenor", beat-1, j) and self.isSpacingValid("tenor", beat, j):
        #             if allNotes[j] == chord.root[0:1] and counts[0] <= 1:
        #                 possibleNotes.append(allNotes[j:j+2])
        #             if allNotes[j] == chord.third[0:1]:
        #                 if counts[1] == 0:
        #                     possibleNotes.append(allNotes[j:j+2])
        #                 elif backupThird == "":
        #                     backupThird = allNotes[j:j+2]
        #             if allNotes[j] == chord.fifth[0:1] and counts[2] <= 1:
        #                 if counts[0] != 2 and counts[1] == 1 or (counts[2] == 0):
        #                     possibleNotes.append(allNotes[j:j+2])
        #         if not self.isParallel5thOctave("tenor", beat-1, i) and not self.isVoiceCrossing("tenor", beat-1, i) and self.isSpacingValid("tenor", beat, i):
        #             if allNotes[i] == chord.root[0:1] and counts[0] <= 1:
        #                 possibleNotes.append(allNotes[i:i+2])
        #             if allNotes[i] == chord.third[0:1]:
        #                 if counts[1] == 0:
        #                     possibleNotes.append(allNotes[i:i+2])
        #                 elif backupThird == "":
        #                     backupThird = allNotes[i:i+2]
        #             if allNotes[i] == chord.fifth[0:1] and counts[2] <= 1:
        #                 if counts[0] != 2 and counts[1] == 1 or (counts[2] == 0):
        #                     possibleNotes.append(allNotes[i:i+2])
        #         if i > tenorRange[0]:
        #             i -= 2
        #         if j < tenorRange[1]:
        #             j += 2
        #         count += 1

        #     possibleNotes = list(dict.fromkeys(possibleNotes))
        #     if backupThird and counts[1] != 0 and counts[2] != 0:
        #         possibleNotes.append(backupThird)
        #     for n in possibleNotes:
        #         if n[0] == chord.fifth and counts[1] == 0:
        #             None
        #         elif n[0] == chord.root and (0 in [counts[0], counts[1]]):
        #             None
        #         elif beat < len(self.chords) - 1:
        #             self.updateVoicesDictionary()
        #             self.writeLine(beat + 1, "soprano", n)
        #         else:
        #             self.voices["tenor"][beat] = n

    def printChords(self):
        for chord in self.chords:
            print(chord.root + " " + chord.third + " " + chord.fifth)

    def addOctaveForLilypond(self, note):
        result = note[0]
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

    def createSheetMusicPdf(self):
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
        keyAccidental = ""
        if "#" in self.key:
            keyAccidental = "is"
        if "b" in self.key:
            keyAccidental = "es"

        fileString = ""

        fileString += "global = { \\key " + self.key.lower()[0] + keyAccidental + " " + quality + " }" 
        fileString += "sopMusic = \\absolute { " + sopranoNotes.lower() + "}"
        fileString += "altoMusic = \\absolute { " + altoNotes.lower() + "}"
        fileString += "tenorMusic = \\absolute { " + tenorNotes.lower() + "}"
        fileString += "bassMusic = \\absolute { " + bassNotes.lower() + "}"
        fileString += "\\score { \\new ChoirStaff <<\\new Staff = \"women\" << \\new Voice = \"sopranos\" { \\voiceOne << \\global \\sopMusic >> }"
        fileString += "\\new Voice = \"altos\" { \\voiceTwo << \\global \\altoMusic >> } >>"
        fileString += "\\new Staff = \"men\" << \\clef bass \\new Voice = \"tenors\" { \\voiceOne << \\global \\tenorMusic >> }"
        fileString += "\\new Voice = \"basses\" { \\voiceTwo << \\global \\bassMusic >> } >> >> } \\version \"2.18.2\""
        self.fileString = fileString
        
        fout.write(fileString)
        fout.close()

        os.system("lilypond --include /artifacts -o /artifacts " + self.fileName)
        os.system("open artifacts/" + self.fileName[0:-3] + ".pdf")
        print("Look for a file named \'" + self.fileName[0:-3] + ".pdf" + "\'!")

    def playMidiFile(self):
        midiFileName = self.fileName[0:-3] + ".midi"
        fout = open("artifacts/" + self.fileName, "w")
        newFileString = self.fileString[0:self.fileString.index("score") + 8] + "\\midi { \\tempo 4 = 72 } " + self.fileString[self.fileString.index("score") + 8:-1] + self.fileString[-1]
        fout.write(newFileString)
        fout.close()
        os.system("lilypond --include /artifacts -o /artifacts " + self.fileName)
        os.system("open -a GarageBand artifacts/" + midiFileName)

    def main(self):
        if self.key == None:
            self.key = input("What is the key?: ")
        if self.chordProgression == None:
            self.chordProgression = input("Enter a chord progression (seperated by spaces): ").split(" ")
        # self.printChords()
        self.writeBassLine()
        self.writeLine(0, "soprano", [self.sopranoLine, self.altoLine, self.tenorLine, self.bassLine])
        print()
        self.printAllVoices()
        print()
        print("With accidentals: ")
        self.printAllVoicesWithAccidentals()
        self.createSheetMusicPdf()
        self.playMidiFile()

if __name__ == "__main__":
    PartWriterImpl = PartWriter("C", "I vi IV ii V vii I V I IV V64 I I6 I64 V I")
    PartWriterImpl.main()

# meme cases
#I IV vi V I IV V I ii IV V vii vi IV ii V I IV vi IV vii vi V I