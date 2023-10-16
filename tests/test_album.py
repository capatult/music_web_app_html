from lib.album import Album

def test_can_construct_album():
    album = Album(0, "", 0, 0)

def test_album_constructs_correctly():
    album = Album(1, "A title", 2000, 2)
    assert album.id == 1
    assert album.title == "A title"
    assert album.release_year == 2000
    assert album.artist_id == 2

def test_new_from_form_data_constructs_correctly():
    album_1 = Album.new_from_form_data(
        "", "", ""
    )
    assert album_1 == Album(None, None, None, None)
    album_2 = Album.new_from_form_data(
        "A title", "2000", "2"
    )
    assert album_2 == Album(None, "A title", 2000, 2)
    album_3 = Album.new_from_form_data(
        None, "-1234", "not a number"
    )
    assert album_3 == Album(None, None, -1234, None)
    album_4 = Album.new_from_form_data(
        5, "also not a number", None
    )
    assert album_4 == Album(None, "5", None, None)

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
        "Album(1, \'A title\', 2000, 2)",
        "Album(2, \'A title\', 2000, 2)",
        "Album(1, \'A different title\', 2000, 2)",
        "Album(1, \'A title\', 2001, 2)",
        "Album(1, \'A title\', 2000, 3)",
    ]


def test_album_checked_as_valid_when_valid():
    assert Album(None, "Title", 0, 1).is_valid() == True
    assert Album(1, "Title", 0, 1).is_valid() == True


def test_album_checked_as_invalid_when_invalid():
    # `id` must be None or a positive int
    assert Album(0, "Title", 0, 1).is_valid() == False

    # `title` must be a non-empty string
    assert Album(None, "", 0, 1).is_valid() == False
    assert Album(None, None, 0, 1).is_valid() == False

    # `release_year` cannot be None
    assert Album(None, "Title", None, 1).is_valid() == False

    # `artist_id` must be a positive int
    assert Album(None, "Title", 0, 0).is_valid() == False
    assert Album(None, "Title", 0, None).is_valid() == False

def test_album_generates_correct_errors_in_right_order():
    # `id` must be None or a positive int
    assert Album(None, "Title", 0, 1).generate_errors() is None
    assert Album(1, "Title", 0, 1).generate_errors() is None
    assert Album(0, "Title", 0, 1).generate_errors() == "ID must be positive"

    # `title` must be a non-empty string
    assert Album(None, "", 0, 1).generate_errors() == "The title cannot be blank"
    assert Album(None, None, 0, 1).generate_errors() == "The title cannot be blank"

    # `release_year` cannot be None
    assert Album(None, "Title", None, 1).generate_errors() == "The release year cannot be blank"

    # `artist_id` must be a positive int
    assert Album(None, "Title", 0, 0).generate_errors() == "The artist must be selected"
    assert Album(None, "Title", 0, None).generate_errors() == "The artist must be selected"

    all_errors_msg = """\
The title cannot be blank; The release year cannot be blank; The artist must be selected"""
    assert Album(None, "", None, None).generate_errors() == all_errors_msg