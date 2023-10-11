from lib.album import Album

def test_can_construct_album():
    album = Album(0, "", 0, 0)

def test_album_constructs_correctly():
    album = Album(1, "A title", 2000, 2)
    assert album.id == 1
    assert album.title == "A title"
    assert album.release_year == 2000
    assert album.artist_id == 2

def test_identical_albums_compare_equal():
    album_1 = Album(1, "A title", 2000, 2)
    album_2 = Album(1, "A title", 2000, 2)
    assert album_1 == album_2

def test_non_identical_albums_compare_nonequal():
    album = Album(1, "A title", 2000, 2)
    others = [
        Album(2, "A title", 2000, 2),
        Album(1, "A different title", 2000, 2),
        Album(1, "A title", 2001, 2),
        Album(1, "A title", 2000, 3),
    ]
    for other in others:
        assert album != other

def test_album_string_formats_correctly():
    albums = [
        Album(1, "A title", 2000, 2),
        Album(2, "A title", 2000, 2),
        Album(1, "A different title", 2000, 2),
        Album(1, "A title", 2001, 2),
        Album(1, "A title", 2000, 3),
    ]
    representations = [
        str(album)
        for album in albums
    ]
    assert representations == [
        "Album(1, A title, 2000, 2)",
        "Album(2, A title, 2000, 2)",
        "Album(1, A different title, 2000, 2)",
        "Album(1, A title, 2001, 2)",
        "Album(1, A title, 2000, 3)",
    ]
