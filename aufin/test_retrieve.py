import find

from analyze import get_spectrogram, get_peaks, read_wav

#data, params = read_wav("../music/WATIC.ComeBackHome.wav")

#x = get_spectrogram(data)
#y = get_peaks(x, plot=True)

#find.from_file("../music/WATIC.ComeBackHome.wav", start=500000, end=800000)
#find.from_file("../recordings/Grazie.wav")
find.from_mic()