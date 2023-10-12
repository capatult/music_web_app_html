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

    def find(self, artist_id):
        rows = self._connection.execute(
            'SELECT * FROM artists WHERE id = %s', (
                artist_id,
            )
        )
        if len(rows) == 0:
            raise Exception("No artist exists with the given id")
        if len(rows) > 1:
            raise Exception("More than 1 record was returned - CHECK QUERY CORRECTNESS NOW!")
        return self._convert_row_to_artist(rows[0])