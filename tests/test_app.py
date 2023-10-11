from playwright.sync_api import Page, expect

# Tests for your routes go here

UTF_8 = "utf-8"

"""
When: we make a GET request to /albums
Then: we should get a list of all albums in the database
"""
def test_get_albums_returns_one_album_per_line_listing(db_connection, web_client):
    db_connection.seed("seeds/music_web_app.sql")
    response = web_client.get('/albums')
    assert response.status_code == 200
    assert response.data.decode(UTF_8) == """\
Album(1, \'Doolittle\', 1989, 1)
Album(2, \'Surfer Rosa\', 1988, 1)
Album(3, \'Waterloo\', 1974, 2)
Album(4, \'Super Trouper\', 1980, 2)
Album(5, \'Bossanova\', 1990, 1)
Album(6, \'Lover\', 2019, 3)
Album(7, \'Folklore\', 2020, 3)
Album(8, \'I Put a Spell on You\', 1965, 4)
Album(9, \'Baltimore\', 1978, 4)
Album(10, \'Here Comes the Sun\', 1971, 4)
Album(11, \'Fodder on My Wings\', 1982, 4)
Album(12, \'Ring Ring\', 1973, 2)\
"""

"""
When: we make a GET request to /artists
Then: we should get a list of all artists in the database
"""
def test_get_artists_returns_list_of_artists(db_connection, web_client):
    db_connection.seed("seeds/music_web_app.sql")
    response = web_client.get('/artists')
    assert response.status_code == 200
    assert response.data.decode(UTF_8) == """[\
Artist(1, Pixies, Rock), \
Artist(2, ABBA, Pop), \
Artist(3, Taylor Swift, Pop), \
Artist(4, Nina Simone, Jazz)\
]\
"""