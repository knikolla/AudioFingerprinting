import database
import pyaudio
import numpy

from analyze import read_wav, get_spectrogram, get_peaks


def find(signal):
    x = get_spectrogram(signal)
    y = get_peaks(x)
    fingerprints = database.create_fingerprints(y)

    # Fingerprint alignment
    matches = {}
    best_song = 0
    best_count = 0

    db = database.Database()
    for h, rel_time in fingerprints:
        match = db.get_fingerprint(h)

        # If the fingerprint exists in the database
        if len(match) > 1:
            print(match)

        for f in match:
            song_id = f["song_id"]
            abs_time = f["time"]
            difference = abs_time - rel_time

            #print("Song ID: " + str(song_id))

            if song_id in matches:
                if difference in matches[song_id]:
                    matches[song_id][difference] += 1
                    candidate = matches[song_id][difference]

                    if candidate > best_count:
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
    # Based on sound_recorder.py from mabdrabo
    # https://gist.github.com/mabdrabo/8678538
    audio = pyaudio.PyAudio()
    stream = audio.open(format=pyaudio.paInt16, channels=1,
                        rate=44100, input=True,
                        frames_per_buffer=1024)
    print("Listening...")

    frames = []
    for i in range(0, int((44100 * 8) / 1024)):
        data = stream.read(1024)
        decoded = numpy.fromstring(data, 'int16')
        frames.extend(decoded)

    print("Searching...")

    find(frames)