import cherrypy

from sqlalchemy import func

from models.track import Track
from models.artist import Artist
from models.album import Album
from utils.db import Db
from utils.threadmanager import ThreadManager

class StatusAPI(object):
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def default(self):
        session = Db().get_session()

        artist_count = session.query(func.count(Artist.id)).one()[0]
        track_count = session.query(func.count(Track.id)).one()[0]
        album_count = session.query(func.count(Album.id)).one()[0]

        total_length = session.query(func.sum(Track.length)).one()[0]

        return {
            'library': {
                'artist_count': artist_count,
                'track_count': track_count,
                'album_count': album_count,
                'total_length': total_length,
                },
            'threads': [ s._asdict() for s in ThreadManager.get_all() ]
            }
