import analyze
import database

# Bach
data, params = analyze.read_wav("../music/Beethoven.Seventh.wav")

x = analyze.get_spectrogram(data[600000:800000], 4096, 2048)
y = analyze.get_peaks(x)
fingerprints = database.create_fingerprints(y)

db = database.Database()
for hash, rel_time in fingerprints:
    s = db.get(hash)
    if s is not None:
        song_id, abs_time = db.get(hash)
        print("SONG: " + str(song_id) + " ABS_TIME: " + str(abs_time) + " REL_TIME: " + str(rel_time))