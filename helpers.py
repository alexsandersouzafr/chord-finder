

NOTES = {
    '1':['B#', 'C'],
    '2':['C#', 'Db'],
    '3':['D'],
    '4':['D#', 'Eb'],
    '5':['E', 'Fb'],
    '6':['E#', 'F'],
    '7':['F#','Gb'],
    '8':['G'],
    '9':['G#', 'Ab'],
    '10':['A'],
    '11':['A#', 'Bb'],
    '12':['B','Cb'],
    '13':['B#', 'C'],
    '14':['C#', 'Db'],
    '15':['D'],
    '16':['D#', 'Eb'],
    '17':['E', 'Fb'],
    '18':['E#', 'F'],
    '19':['F#','Gb'],
    '20':['G'],
    '21':['G#', 'Ab'],
    '22':['A'],
    '23':['A#', 'Bb'],
    '24':['B','Cb']
}

COLOR = {
    # Triads
    '': [4, 3],
    'm': [3, 4],
    'aug': [4, 4],
    'm5b': [3, 3],
    'sus2': [2, 5],
    'sus4': [5, 2],

    # Tetrachords
    '6': [4, 3, 2],
    'Maj7': [4, 3, 4],
    '7': [4, 3, 3],
    'm7': [3, 4, 3],
    'mMaj7': [3, 4, 4],
    'add9': [2, 2, 3],
    '°': [3, 3, 4],
    '7(sus2)': [2, 5, 3],
    '7(sus4)': [5, 2, 3]
}

INV = {
    # Tetrachord Inversions
    'MajorM7B3': [3, 4, 1], #Maj7/3rd OK
    'MajorM7B5': [4, 1, 4], #Maj7/5th OK
    'MajorM7B7': [1, 4, 3], #Maj7/7th
    'Minorm7B5': [3, 2, 3], #7/5th
    'Minorm7B7': [2, 3, 4], #7/7th
    'Majorm7B3': [3, 3, 2], #7/3rd
    'Majorm7B5': [3, 2, 4], #7/5th
    'Majorm7B7': [2, 4, 3], #/7

    # Triad Inversions
    'MajorB3': [3, 5], #terça no baixo (intervalo: )
    'MajorB5': [5, 4], #quinta np baixo
    'MinorB3': [4, 5], 
    'MinorB5': [5, 3]
}   

# Finds note position in NOTES.
def note_index(note, root: bool):
    for number in NOTES:
        if note in NOTES[number] and root == True:
            return int(number)
        elif note in NOTES[number] and root == False:
            return int(number) + 12
    # return print("Invalid Note") #DEBUG PRINT

# Find interval between two notes.
# Usage: asc: True for ascendent and asc: False for descendent. Return number of semitones.
# a and b are index numbers
def interval(a, b, asc: bool):
    interval = 0
    # Get ascendente interval
    if asc == True:
        if a < b:
            interval = (a - b)
        else:
            interval = ((b - a) + 12)
        return interval

    # Get descendente interval
    else:
        if a > b:
            interval = (a - b)
        else:
            interval = ((b + a) - 12)
        return interval

# Stack chord's notes ascendently by 3rds or above. start from root
def stack(notes):
    stacked = []
    # print(f"Notes: {notes}") #DEBUG PRINT
    root = notes[0]
    stacked.append(root)
    stacks = [] # Other notes
    
    #populate stacks
    for i in range(1, len(notes)):
        if notes[i] - 12 < root:
            stacks.append(notes[i])
        else:
            stacks.append(notes[i] - 12)
    stacks.sort()

    # Populate stacked
    for i in range(len(stacks)):
        stacked.append(stacks[i])
    # print(f"Stacked: {stacked}") #DEBUG PRINT

    # TODO: Find dissonances and rearrange the stack in thirds to get a triad. Find 2nds (1 or 2 semitones),

    return stacked

#  Get interval pattern from 
def pattern(notes):
    pattern = []
    for i in range(len(notes)):
        if i >= len(notes) - 1: break
        leap = interval(notes[i], notes[i + 1], True)
        if leap < 0:
            leap *= -1
        pattern.append(leap)
    # print(f"Pattern: {pattern}") #DEBUG PRINT
    return pattern

# Define chord color and root
def color(pattern):
    for color in COLOR:
        if pattern == COLOR[color]:
            return color
    
    # In case it is an inversion. The root will become the BASS and the name of the chord will change.
    for inversion in INV:
        if pattern == INV[inversion]:
            return inversion

def print_chord(prename):
    # Check if not inversions
    inversions = ['B5', 'B7', 'B3', 'B7']
    color = ""
    match = False
    correction = 0

    for item in inversions:
        if item in prename:
            match = True
    # If not inversion, return name normally
    if not match:
        return prename

    #In case of inversion:
    else:
        # Get root note and add # or b if needed
        root = prename[0]
        # print(root)
        if prename[1] == '#' or prename[1] == 'b':
            root += prename[1]
        bass = f"/{root}"
        # print(root)
        # print(f"Prename: {prename}")
        # Check if chord is major or minor and set the correction value so you get new root
        if 'B3' in prename: # for 3rd in bass
            if 'Minor' in prename:
                correction = 3
                color = 'm'
            else:
                correction = 4
        elif 'B5' in prename: # for 5th in bass
            correction = 7
            if 'Minor' in prename:
                color = 'm'
        elif 'B7' in prename: # for 7th in bass
            if 'M7' in prename:
                correction = -1
            if 'm7' in prename:
                correction = -2
        
        # Adds maj7th to color if not in the bass
        if correction != -1:
            if 'M7' in prename: # for minor 7th
                color += 'Maj7'
            if 'm7' in prename: # for minor 7th
                color += '7'
        
        # Get root index
        for index in NOTES:
            if root in NOTES[index]:
                root = int(index) - correction
                if root < 0:
                    root += 12                
                
        # print(root)
        # print(f"Correction: {correction}")
        # print(f"bass: {bass}")

        # Get new root
        root = str(root)
        for note in NOTES:
            if root in note:
                if 'b' in bass:
                    root = NOTES[note][1]
                elif '#' in bass:
                    root = NOTES[note][0]
                else:
                    root = NOTES[note][1]

    final_name = f"{root}{color}{bass}"
    return final_name

# input list > note_index > stack > pattern > color> inversion? > print
def chordfinder(root,b,c,d):
    note_input = [root, b, c]
    if d:
        note_input.append(d)
    notas = []
    index = 0

    # Populate notas with note indexes
    for i in range(len(note_input)):
        if i == 0:
            index = note_index(note_input[i], True)
        else:
            index = note_index(note_input[i], False)
        notas.append(index)

    chord_color = color(pattern(stack(notas)))
    return print_chord(f"{root}{chord_color}")
    
    
# chordfinder(input("Root: "), input(), input(), input())