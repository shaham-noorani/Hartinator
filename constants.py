majorKeys = {
    "C": "CDEFGAB",
    "G": ["G", "A", "B", "C", "D", "E", "F#"],
    "D": ["D", "E", "F#", "G", "A", "B", "C#"],
    "A": ["A", "B", "C#", "D", "E", "F#", "G#"],
    "E": ["E", "F#", "G#", "A", "B", "C#", "D#"],
    "B": ["B", "C#", "D#", "E", "F#", "G#", "A#"],
    "F#": ["F#", "G#", "A#", "B", "C#", "D#", "E#"],
    "C#": ["C#", "D#", "E#", "F#", "G#", "A#", "B#"],
    "F": ["F", "G", "A", "Bb", "C", "D", "E"],
    "Bb": ["Bb", "C", "D", "Eb", "F", "G", "A"],
    "Eb": ["Eb", "F", "G", "A", "Bb", "C", "D"],
    "Ab": ["Ab", "Bb", "C", "Db", "Eb", "F", "G"],
    "Db": ["Db", "Eb", "F", "Gb", "Ab", "Bb", "C"],
    "Gb": ["Gb", "Ab", "Bb", "Cb", "Db", "Eb", "F"],
    "Cb": ["Cb", "Db", "Eb", "Fb", "Gb", "Ab", "Bb"],
}

minorKeys = {
    "a": "ABCDEFG",
    "e": ["E", "F#", "G", "A", "B", "C", "D"],
    "b": ["B", "C#", "D", "E", "F#", "G", "A"],
    "f#": ["F#", "G#", "A", "B", "C#", "D", "E"],
    "c#": ["C#", "D#", "E", "F#", "G#", "A", "B"],
    "g#": ["G#", "A#", "B", "C#", "D#", "E", "F#"],
    "d#": [ "D#", "E#", "F#", "G#", "A#", "B", "C#"],
    "a#": ["A#", "B#", "C#", "D#", "E#", "F#", "G#"],
    "d": ["D", "F", "G", "A", "Bb", "C", "D"],
    "g": ["G", "A", "Bb", "C", "D", "Eb", "F", "G"],
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

allNotes = "F2G2A2B2C3D3E3F3G3A3B3C4D4E4F4G4A4B4C5D5E5F5G5A5B5C6"

bassRange = [0, allNotes.index("A3")]
tenorRange = [allNotes.index("C3"), allNotes.index("E4")]
altoRange = [allNotes.index("B3"), allNotes.index("D5")]
sopranoRange = [allNotes.index("F4"), allNotes.index("F5")]
