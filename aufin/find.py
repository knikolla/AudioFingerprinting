import database
import pyaudio

from analyze import read_wav, get_spectrogram, get_peaks


def find(signal):
    x = get_spectrogram(signal)
    y = get_peaks(x)
    fingerprints = database.create_fingerprints(y)

    # Fingerprint alignment
    matches = {}
    best_song = 0
    best_diff = 0
    best_count = 0

    db = database.Database()
    for h, rel_time in fingerprints:
        match = db.get_fingerprint(h)

        # If the fingerprint exists in the database
        if match is not None:
            song_id, abs_time = match
            difference = abs_time - rel_time

            if song_id in matches:
                if difference in matches[song_id]:
                    matches[song_id][difference] += 1
                    candidate = matches[song_id][difference]

                    if candidate > best_count:
                        best_diff = difference
                        best_song = song_id
                        best_count = candidate

                else:
                    matches[song_id][difference] = 1
            else:
                matches[song_id] = {difference: 1}

    if best_song != 0:
        result = db.get_song(best_song)
        print("Title: " + result["title"] + "\tAuthor: " + result["author"] + "\tAlbum: " + result["album"] +
              "\t\t\t(" + str(best_count) + " fingerprint hits)")
    else:
        print("No confident match found...")


def from_file(file, start=0, end=0):
    data, params = read_wav(file)

    if end <= start:
        end = len(data)

    find(data[start:end])


def from_mic():
    audio = pyaudio.PyAudio()
    stream = audio.open(format=pyaudio.paInt16, channels=1,
                        rate=44100, input=True,
                        frames_per_buffer=1024)
    print("Listening...")

    frames = []
    for i in range(0, int(44100 / 1024 * 5)):
        data = stream.read(1024)
        frames.append(data)
    print("Searching...")

    find(frames)