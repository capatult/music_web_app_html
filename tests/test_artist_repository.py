from lib.artist_repository import ArtistRepository
from lib.artist import Artist

"""
When: we call ArtistRepository._convert_row_to_artist
And: we provide a dict for row with values for keys "id", "name", and "genre"
Then: we get an Artist object reflecting the values in the passed-in dictionary.
"""
def test_convert_row_to_artist():
    dicts = [
        {"id": 1, "name": "A name", "genre": "A genre"},
        {"id": 2, "name": "Another name", "genre": "Another genre"},
    ]
    artists = [
        ArtistRepository._convert_row_to_artist(mock_row)
        for mock_row in dicts
    ]
    assert artists == [
        Artist(1, "A name", "A genre"),
        Artist(2, "Another name", "Another genre"),
    ]



"""
When: we call ArtistRepository.all
Then: we get a list of Artist objects reflecting the seed data.
"""
def test_get_all_records(db_connection):
    db_connection.seed("seeds/music_web_app.sql")
    repository = ArtistRepository(db_connection)

    artists = repository.all()

    assert artists == [
        Artist(1, 'Pixies', 'Rock'),
        Artist(2, 'ABBA', 'Pop'),
        Artist(3, 'Taylor Swift', 'Pop'),
        Artist(4, 'Nina Simone', 'Jazz'),
    ]

"""
When: we call ArtistRepository.create
And: we provide an Artist object with values in all columns except `id`
    (`id` will be autoassigned)
Then: we create a new record in the `artists` table in the database
    (it returns None)
"""
def test_create_record(db_connection):
    db_connection.seed("seeds/music_web_app.sql")
    repository = ArtistRepository(db_connection)

    repository.create(Artist(None, "Wild nothing", "Indie"))

    result = repository.all()
    assert result == [
        Artist(1, 'Pixies', 'Rock'),
        Artist(2, 'ABBA', 'Pop'),
        Artist(3, 'Taylor Swift', 'Pop'),
        Artist(4, 'Nina Simone', 'Jazz'),
        Artist(5, 'Wild nothing', 'Indie'),
    ]