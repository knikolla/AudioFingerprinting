import analyze
import database

# Bach
data, params = analyze.read_wav("../music/Bach.wav")

x = analyze.get_spectrogram(data)
y = analyze.get_peaks(x)

md = {'title': 'Bach', 'author': 'Bach', 'album': 'Test'}
database.insert_song(md, y)

# Beethoven Seventh
data, params = analyze.read_wav("../music/Beethoven.Ninth.wav")

x = analyze.get_spectrogram(data)
y = analyze.get_peaks(x)

md = {'title': 'Beethoven Seventh', 'author': 'Beethoven', 'album': 'Test'}
database.insert_song(md, y)

# Beethoven Ninth
data, params = analyze.read_wav("../music/Beethoven.Seventh.wav")

x = analyze.get_spectrogram(data)
y = analyze.get_peaks(x)

md = {'title': 'Beethoven Ninth', 'author': 'Beethoven', 'album': 'Test'}
database.insert_song(md, y)