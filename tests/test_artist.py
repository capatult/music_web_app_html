from lib.artist import Artist

def test_can_construct_artist():
    artist = Artist(0, "", "")

def test_artist_constructs_correctly():
    artist = Artist(1, "A name", "A genre")
    assert artist.id == 1
    assert artist.name == "A name"
    assert artist.genre == "A genre"

def test_identical_artists_compare_equal():
    artist_1 = Artist(1, "A name", "A genre")
    artist_2 = Artist(1, "A name", "A genre")
    assert artist_1 == artist_2

def test_non_identical_artists_compare_nonequal():
    artist = Artist(1, "A name", "A genre")
    others = [
        Artist(2, "A name", "A genre"),
        Artist(1, "A different name", "A genre"),
        Artist(1, "A name", "A different genre"),
    ]
    for other in others:
        assert artist != other

def test_artist_string_formats_correctly():
    artists = [
        Artist(1, "A name", "A genre"),
        Artist(2, "A name", "A genre"),
        Artist(1, "A different name", "A genre"),
        Artist(1, "A name", "A different genre"),
    ]
    representations = [
        str(artist)
        for artist in artists
    ]
    assert representations == [
        "Artist(1, A name, A genre)",
        "Artist(2, A name, A genre)",
        "Artist(1, A different name, A genre)",
        "Artist(1, A name, A different genre)",
    ]
