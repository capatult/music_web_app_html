from lib.artist import Artist

class ArtistRepository:
    def __init__(self, connection):
        self._connection = connection

    @staticmethod
    def _convert_row_to_artist(row):
        return Artist(
            row["id"], row["name"], row["genre"]
        )

    def all(self):
        rows = self._connection.execute(
            'SELECT * FROM artists'
        )
        return [self._convert_row_to_artist(row) for row in rows]

    def create(self, artist):
        self._connection.execute(
            'INSERT INTO artists (name, genre) VALUES (%s, %s)',
            [
                artist.name, artist.genre
            ]
        )
        return None
