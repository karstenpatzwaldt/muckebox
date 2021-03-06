from base import Base
from file import File
from artist import Artist
from album import Album

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

class Track(Base):
    __tablename__ = 'tracks'

    __private__ = set([
        'stringid',
        'directory',
        'bits_per_sample',
        'sample_rate',
        'file_id',
        'album_artist_id'
        ])

    id = Column(Integer, primary_key = True)
    stringid = Column(String, index = True, unique = True)
    directory = Column(String, index = True)

    file_id = Column(Integer, ForeignKey(File.id))

    title = Column(String)

    album_id = Column(Integer, ForeignKey(Album.id))

    artist_id = Column(Integer, ForeignKey(Artist.id))
    album_artist_id = Column(Integer, ForeignKey(Artist.id))

    artist = relationship(
        'Artist', primaryjoin = 'Artist.id == Track.artist_id',
        backref = 'tracks')
    album_artist = relationship(
        'Artist', primaryjoin = 'Artist.id == Track.album_artist_id')

    date = Column(String)

    tracknumber = Column(Integer)
    discnumber = Column(Integer)

    label = Column(String)
    catalognumber = Column(String)

    length = Column(Integer)
    bits_per_sample = Column(Integer)
    sample_rate = Column(Integer)
