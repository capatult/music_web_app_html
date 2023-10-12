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

    def find(self, album_id):
        rows = self._connection.execute(
            'SELECT * FROM albums WHERE id = %s', (
                album_id,
            )
        )
        if len(rows) == 0:
            raise Exception("No album exists with the given id")
        if len(rows) > 1:
            raise Exception("More than 1 record was returned - CHECK QUERY CORRECTNESS NOW!")
        return self._convert_row_to_album(rows[0])