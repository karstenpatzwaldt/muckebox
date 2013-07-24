import cherrypy
import Queue

from models.track import Track
from db import Db
from transcoder.autotranscoder import AutoTranscoder

class StreamAPI(object):
    BLOCK_SIZE = 32 * 1024
    QUALITY_STRINGS = {
        'lowest':       AutoTranscoder.Quality.LOWEST,
        'low':          AutoTranscoder.Quality.LOW,
        'medium':       AutoTranscoder.Quality.MEDIUM,
        'high':         AutoTranscoder.Quality.HIGH,
        'highest':      AutoTranscoder.Quality.HIGHEST,
        }

    @cherrypy.expose
    def default(self, trackid, format = False, quality = 'high', max_bits_per_sample = 16, max_sample_rate = 48000):
        if not (trackid and trackid.isdigit()):
            raise cherrypy.HTTPError(400)

        if quality not in self.QUALITY_STRINGS:
            raise cherrypy.HTTPError(400)

        if not str(max_bits_per_sample).isdigit():
            raise cherrypy.HTTPError(400)

        if not str(max_sample_rate).isdigit():
            raise cherrypy.HTTPError(400)

        session = Db.get_session()
        track = self.get_track(int(trackid), session)

        queue = Queue.Queue()
        transcoder = AutoTranscoder(track,
                                    { 'format': format,
                                      'quality': self.QUALITY_STRINGS[quality],
                                      'bits_per_sample': max_bits_per_sample,
                                      'sample_rate': max_sample_rate },
                                    queue)

        cherrypy.response.headers["Content-Type"] = transcoder.get_mime_type()

        transcoder.start()

        return self.stream(transcoder, queue)

    @staticmethod
    def stream(transcoder, queue):
        while True:
            block = queue.get()

            if not block:
                break

            try:
                yield block
            except GeneratorExit:
                transcoder.abort()
                raise

    @staticmethod
    def get_track(trackid, session):
        return session.query(Track).filter(Track.id == trackid).one()

    default._cp_config = { 'response.stream': True }
