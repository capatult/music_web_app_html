from lib.album_repository import AlbumRepository
from lib.album import Album
import pytest

"""
When: we call AlbumRepository.all
Then: we get a list of Album objects reflecting the seed data.
"""
def test_get_all_records(db_connection):
    db_connection.seed("seeds/music_web_app.sql")
    repository = AlbumRepository(db_connection)

    albums = repository.all()

    assert albums == [
        Album(1, 'Doolittle', 1989, 1),
        Album(2, 'Surfer Rosa', 1988, 1),
        Album(3, 'Waterloo', 1974, 2),
        Album(4, 'Super Trouper', 1980, 2),
        Album(5, 'Bossanova', 1990, 1),
        Album(6, 'Lover', 2019, 3),
        Album(7, 'Folklore', 2020, 3),
        Album(8, 'I Put a Spell on You', 1965, 4),
        Album(9, 'Baltimore', 1978, 4),
        Album(10, 'Here Comes the Sun', 1971, 4),
        Album(11, 'Fodder on My Wings', 1982, 4),
        Album(12, 'Ring Ring', 1973, 2),
    ]

"""
When: we call AlbumRepository.create
And:  we provide an Album object with values in all columns except `id`
    (`id` will be autoassigned)
Then: we create a new record in the `albums` table in the database
    (it returns None)
"""
def test_create_record(db_connection):
    db_connection.seed("seeds/music_web_app.sql")
    repository = AlbumRepository(db_connection)

    repository.create(Album(None, "Voyage", 2022, 2))

    result = repository.all()
    assert result == [
        Album(1, 'Doolittle', 1989, 1),
        Album(2, 'Surfer Rosa', 1988, 1),
        Album(3, 'Waterloo', 1974, 2),
        Album(4, 'Super Trouper', 1980, 2),
        Album(5, 'Bossanova', 1990, 1),
        Album(6, 'Lover', 2019, 3),
        Album(7, 'Folklore', 2020, 3),
        Album(8, 'I Put a Spell on You', 1965, 4),
        Album(9, 'Baltimore', 1978, 4),
        Album(10, 'Here Comes the Sun', 1971, 4),
        Album(11, 'Fodder on My Wings', 1982, 4),
        Album(12, 'Ring Ring', 1973, 2),
        Album(13, 'Voyage', 2022, 2),
    ]

"""
When: we call AlbumRepository.find
And:  we provide a value for `id` which corresponds to
    a record in the `albums` table in the database
Then: it returns an Album object corresponding to that record
"""
def test_get_single_record(db_connection):
    db_connection.seed("seeds/music_web_app.sql")
    repository = AlbumRepository(db_connection)

    all_albums = repository.all()

    for album in all_albums:
        result = repository.find(album.id)
        assert result == album


"""
When: we call AlbumRepository.find
And:  we provide a value for `id` which does not correspond to
    a record in the `albums` table in the database
Then: it raises an exception
"""
def test_attempt_get_nonexistent_record(db_connection):
    db_connection.seed("seeds/music_web_app.sql")
    repository = AlbumRepository(db_connection)

    nonexistent_ids = [0, 13, -1]

    for nonexistent_id in nonexistent_ids:
        with pytest.raises(Exception) as e:
            repository.find(nonexistent_id)
        error_message = str(e.value)
        assert error_message == "No album exists with the given id"
