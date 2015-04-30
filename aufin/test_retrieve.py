import analyze

from find import find

# Bach
data, params = analyze.read_wav("../music/Beethoven.Ninth.wav")
find(data[500000:600000])