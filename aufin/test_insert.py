import analyze
import database

# Bach
data, params = analyze.read_wav("../music/ZA.Grazie.wav")

x = analyze.get_spectrogram(data)
y = analyze.get_peaks(x)

md = {'title': 'Grazie', 'author': 'Zero Assoluto', 'album': 'Sotto Una Pioggia Di Parole'}
database.insert_song(md, y)

