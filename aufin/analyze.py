import array
import contextlib
import matplotlib
import numpy
import wave

from matplotlib import pyplot, mlab

from scipy.ndimage.filters import maximum_filter
from scipy.ndimage.morphology import generate_binary_structure, binary_erosion, iterate_structure

def read_wav(file):
    """Read a Wave file into an array

    :param file: location of the Wave file
    :return: array containing the amplitude at each sample
    """
    with contextlib.closing(wave.open(file)) as f:
        params = f.getparams()
        frames = f.readframes(params[3])
    return array.array("h", frames), params


def get_spectrogram(signal, window_size, window_overlap):
    """Run FFT to get the spectrogram of a signal.

    :param signal: array of amplitudes
    :param window_size:
    :param window_overlap:
    :return: numpy 2D array x: time, y: frequency
    """
    result = matplotlib.mlab.specgram(
        signal,
        NFFT=window_size,
        Fs=44100,
        window=matplotlib.mlab.window_hanning,
        noverlap=window_overlap
    )[0]

    result = 10 * numpy.log10(result)
    result[result == -numpy.inf] = 0
    return result


def get_peaks(image):
    """Get the peaks from the 2D array, and do some filtering to reduce the number of peaks.

    :param image: 2D array representing the image
    :return: List of (x, y)
    """
    # http://stackoverflow.com/questions/3684484/peak-detection-in-a-2d-array
    structure = generate_binary_structure(2, 1)
    neighborhood = iterate_structure(structure, 20)

    local_max = maximum_filter(image, footprint=neighborhood)==image
    background = (image == 0)
    eroded_background = binary_erosion(background, structure=neighborhood, border_value=1)
    detected_peaks = local_max - eroded_background

    # detected_peaks is a 2D mask
    amplitudes = image[detected_peaks].flatten()
    freq, t = numpy.where(detected_peaks)

    # Filter all peaks with amplitude less then 10
    unfiltered_peaks = zip(t, freq, amplitudes)
    filtered_peaks = [x for x in unfiltered_peaks if x[2] > 10]

    # get indices for frequency and time
    time = [x[0] for x in filtered_peaks]
    frequency = [x[1] for x in filtered_peaks]

    # scatter of the peaks
    plot = False
    if plot:
        fig, ax = pyplot.subplots()
        ax.imshow(image)
        ax.scatter(time, frequency)
        ax.set_xlabel('Time')
        ax.set_ylabel('Frequency')
        ax.set_title("Spectrogram")
        pyplot.gca().invert_yaxis()
        pyplot.show()

    return list(zip(time, frequency))