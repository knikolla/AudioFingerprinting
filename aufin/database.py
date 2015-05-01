import hashlib

from operator import itemgetter
from sqlalchemy import (create_engine, select, Table, Integer, String,
                        Column, MetaData, Sequence, ForeignKey, UniqueConstraint)
from sqlalchemy.exc import IntegrityError

class Database(object):
    def __init__(self):
        self._engine = create_engine('mysql+pymysql://root:root@localhost:8889/aufin')

        self._metadata = MetaData()
        self._songs = Table('songs', self._metadata,
                            Column('id', Integer, Sequence('user_id_seq'), primary_key=True),
                            Column('title', String(80)),
                            Column('author', String(80)),
                            Column('album', String(80)))

        self._fingerprints = Table('fingerprints', self._metadata,
                                   Column('hash', String(40), index=True),
                                   Column('time', Integer),
                                   Column('song_id', Integer, ForeignKey('songs.id')),
                                   UniqueConstraint('hash', 'time', 'song_id'))

        self._metadata.create_all(self._engine)

    def insert(self, metadata, fingerprints):
        title = metadata['title']
        author = metadata['author']
        album = metadata['album']

        s = self._songs.insert().values(title=title, author=author, album=album)
        res = self._engine.execute(s)

        i = self._fingerprints.insert()
        for f in fingerprints:
            h, t = f
            try:
                self._engine.execute(i, hash=h, time=str(t), song_id=res.inserted_primary_key)
            except IntegrityError:
                # Duplicate, do nothing
                continue

    def get_fingerprint(self, hash):
        s = select([self._fingerprints]).where(self._fingerprints.c.hash == hash)
        result = self._engine.execute(s)
        return result.fetchall()


    def get_song(self, id):
        s = select([self._songs]).where(self._songs.c.id == id)
        result = self._engine.execute(s)
        return result.fetchone()


def create_fingerprints(peaks):
    hashes = []
    for i in range(len(peaks)):
        for j in range(1, 15):
            if (i + j) < len(peaks):
                t1 = peaks[i][0]
                t2 = peaks[i + j][0]
                freq1 = peaks[i][1]
                freq2 = peaks[i + j][1]
                delta = t2 - t1

                hash = hashlib.sha1(str(str(freq1) + str(freq2) + str(delta)).encode('utf-8'))

                hashes.append((hash.hexdigest(), t1))

    return hashes


def insert_song(metadata, peaks):
    # Sort the peaks by time
    peaks.sort(key=itemgetter(0))
    f = create_fingerprints(peaks)

    # Connect to DB
    db = Database()
    db.insert(metadata, f)


