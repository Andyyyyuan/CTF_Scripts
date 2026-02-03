import mido

def extract_lsb_from_midi(midi_path):
    mid = mido.MidiFile(midi_path)
    binary_data = []

    for track in mid.tracks:
        for msg in track:
            if msg.type == 'note_on':
                velocity = msg.velocity
                lsb = velocity & 1
                binary_data.append(str(lsb))

    binary_str = ''.join(binary_data)
    bytes_list = [int(binary_str[i:i + 8], 2) for i in range(0, len(binary_str), 8)]
    m = bytes(bytes_list)
    return m


m = extract_lsb_from_midi('hide.mid')
print(m)