import analyze

from find import find

# Bach
data, params = analyze.read_wav("../music/Beethoven.Seventh.wav")
find(data[20000:])