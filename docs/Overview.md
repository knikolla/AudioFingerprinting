# Audio Fingerprinting Project

## Overview

I will use sliding windows to analyze the spectrum and create a spectrogram. Then I will find peaks, and record the time difference between peaks of the same frequency, and the offset from the start of the file. I will use a hashing function to create a unique identifier for this fingerprint (peak frequency, time difference) and store it in a database (using MySQL or MongoDB sounds convenient for this job, but I'm not there yet with the implementation). Each song will have a lot of fingerprints. 

To find a match. I will do the same process for the input, creating fingerprints and hashing them, and using that hash to access fingerprint in the database. Then I will need to align them, by subtracting the absolute offset of the fingerprint in the db with the relative offset from the start of the input sample. For a match, we return the song which has the biggest number of counts with the same difference. 

## References

* [Willdrevo - Audio Fingerprinting with Python and Numpy](http://willdrevo.com/fingerprinting-and-audio-recognition-with-python/)
