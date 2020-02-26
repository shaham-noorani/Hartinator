from constants import majorKeys, allNotes, voicesInOrder

def is7thResolved(voice, beat, newNoteIndex, key, voices):
    seventh = majorKeys[key][-1]
    newNoteIsTonic = key == allNotes[newNoteIndex]

    if beat == 0:
        return True

    if not newNoteIsTonic:
        if voice == "soprano" or voice == "bass":
            if voices[voice][beat-1][0:1] == seventh:
                return False

    return True

def isParallel5thOctave(voice, beat, newNoteIndex, voices): 
    if beat == 0:
        return False
    
    newNote = allNotes[newNoteIndex:newNoteIndex+1]
    priorNotes = dict()

    # define prior notes to be compared to later
    for i in voicesInOrder:
        priorNotes[i] = voices[i][beat-1][0:1]

    # check stagnant motion
    if priorNotes[voice] == newNote:
        return False

    # check against prior notes for parallel 5th/octaves
    for i in voicesInOrder:
        if i != voice:
            if priorNotes[i]:
                if priorNotes[i] == priorNotes[voice] and newNote == voices[i][0:1]:
                    return True
                if voicesInOrder.index(i) < voicesInOrder.index(voice):
                    if allNotes[allNotes.index(priorNotes[i][0:1]) + 6] == priorNotes[voice][0:1] and allNotes[allNotes.index(voices[i][beat][0:1]) + 6] == newNote[0:1]:
                        return True 
                elif allNotes[allNotes.index(priorNotes[i][0:1]) + 8] == priorNotes[voice][0:1] and allNotes[allNotes.index(voices[i][beat][0:1]) + 8] == newNote[0:1]:
                    return True 
        
    return False

def isVoiceCrossing(voice, beat, newNoteIndex, voices):
    if beat == 0:
        return False
    
    noteIndexes = {"soprano": "", "alto": "", "tenor": "", "bass": ""}

    # define prior notes dict to be compared to later
    for i in voicesInOrder:
        if i != voice:
            noteIndexes[i] = allNotes.index(voices[i][beat])

    if voice == "alto" and noteIndexes["soprano"]:
        if newNoteIndex > noteIndexes["soprano"]:
            return True

    if voice == "tenor" and noteIndexes["alto"]:
        if newNoteIndex > noteIndexes["alto"]:
            return True

    if voice == "tenor" and noteIndexes["bass"]:
        if newNoteIndex < noteIndexes["bass"]:
            return True

    return False

def isSpacingValid(voice, beat, newNoteIndex, voices):
    if voice == "alto":
        if voices["soprano"][beat] != "":
            if newNoteIndex + 14 < allNotes.index(voices["soprano"][beat]):
                return False
        if voices["tenor"][beat] != "":
            if newNoteIndex > allNotes.index(voices["tenor"][beat]) + 14:
                return False
    
    if voice == "tenor":
        if voices["alto"][beat] != "":
            if newNoteIndex + 14 < allNotes.index(voices["alto"][beat]):
                return False

    return True