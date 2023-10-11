from lib.album import Album

class AlbumRepository:
    def __init__(self, connection):
        self._connection = connection

    @staticmethod
    def _convert_row_to_album(row):
        return Album(
            row["id"], row["title"], row["release_year"], row["artist_id"]
        )

    def all(self):
        rows = self._connection.execute('SELECT * FROM albums')
        return [self._convert_row_to_album(row) for row in rows]

    def create(self, album):
        self._connection.execute(
            'INSERT INTO albums (title, release_year, artist_id) VALUES (%s, %s, %s)',
            [
                album.title, album.release_year, album.artist_id
            ]
        )
        return None