import analyze
import find
import database
import sys


def main(argv):
    if len(argv) == 0:
        print_help()
    else:
        operation = argv[0].lower()
        if operation == "insert":
            source = argv[1]
            title = input("Title: ")
            author = input("Author: ")
            album = input("Album: ")
            metadata = {'title': title, 'author': author, 'album': album}
            data, params = analyze.read_wav(source)
            database.insert_song(metadata, analyze.get_peaks(analyze.get_spectrogram(data)))
        elif operation == "find":
            source = argv[1].lower()
            if source == "mic":
                find.from_mic()
            elif source == "file":
                file = argv[2]
                try:
                    start = int(argv[3])
                    end = int(argv[4])
                except IndexError:
                    start = 0
                    end = 0
                find.from_file(file, start, end)

def print_help():
    print("Help!")

if __name__ == '__main__':
    main(sys.argv[1:])