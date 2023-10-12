from lib.artist_repository import ArtistRepository
from lib.artist import Artist
import pytest

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

"""
When: we call ArtistRepository.find
And:  we provide a value for `id` which corresponds to
    a record in the `artists` table in the database
Then: it returns an Artist object corresponding to that record
"""
def test_get_single_record(db_connection):
    db_connection.seed("seeds/music_web_app.sql")
    repository = ArtistRepository(db_connection)

    all_artists = repository.all()

    for artist in all_artists:
        result = repository.find(artist.id)
        assert result == artist


"""
When: we call ArtistRepository.find
And:  we provide a value for `id` which does not correspond to
    a record in the `artists` table in the database
Then: it raises an exception
"""
def test_attempt_get_nonexistent_record(db_connection):
    db_connection.seed("seeds/music_web_app.sql")
    repository = ArtistRepository(db_connection)

    nonexistent_ids = [0, 13, -1]

    for nonexistent_id in nonexistent_ids:
        with pytest.raises(Exception) as e:
            repository.find(nonexistent_id)
        error_message = str(e.value)
        assert error_message == "No artist exists with the given id"
