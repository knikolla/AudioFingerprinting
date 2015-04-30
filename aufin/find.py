import database

from analyze import get_spectrogram, get_peaks

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
        match = db.get(h)

        # If the fingerprint exists in the database
        if match is not None:
            song_id, abs_time = match
            difference = abs_time - rel_time

            #print("SONG: " + str(song_id) + " ABS_TIME: " + str(abs_time) + " REL_TIME: " + str(rel_time))

            if song_id in matches:
                if difference in matches[song_id]:
                    matches[song_id][difference] += 1
                    candidate = matches[song_id][difference]

                    if candidate > best_diff:
                        best_diff = difference
                        best_song = song_id
                        best_count = candidate

                else:
                    matches[song_id][difference] = 1
            else:
                matches[song_id] = {difference: 1}


    print("SONG_ID: " + str(best_song) + "\tBEST_DIFF: " + str(best_diff) + "\tBEST_COUNT: " + str(best_count))