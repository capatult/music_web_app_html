from playwright.sync_api import Page, expect

# Tests for your routes go here

UTF_8 = "utf-8"

# """
# When: we make a GET request to /albums
# Then: we should get a list of all albums in the database
# """
# def test_get_albums_returns_one_album_per_line_listing(db_connection, web_client):
#     db_connection.seed("seeds/music_web_app.sql")
#     response = web_client.get('/albums')
#     assert response.status_code == 200
#     assert response.data.decode(UTF_8) == """\
# Album(1, \'Doolittle\', 1989, 1)
# Album(2, \'Surfer Rosa\', 1988, 1)
# Album(3, \'Waterloo\', 1974, 2)
# Album(4, \'Super Trouper\', 1980, 2)
# Album(5, \'Bossanova\', 1990, 1)
# Album(6, \'Lover\', 2019, 3)
# Album(7, \'Folklore\', 2020, 3)
# Album(8, \'I Put a Spell on You\', 1965, 4)
# Album(9, \'Baltimore\', 1978, 4)
# Album(10, \'Here Comes the Sun\', 1971, 4)
# Album(11, \'Fodder on My Wings\', 1982, 4)
# Album(12, \'Ring Ring\', 1973, 2)\
# """

"""
When: we make a GET request to /artists
Then: we should get a list of all artists in the database
"""
def test_get_artists_returns_one_artist_per_line_listing(db_connection, web_client):
    db_connection.seed("seeds/music_web_app.sql")
    response = web_client.get('/artists')
    assert response.status_code == 200
    assert response.data.decode(UTF_8) == """\
Artist(1, \'Pixies\', \'Rock\')
Artist(2, \'ABBA\', \'Pop\')
Artist(3, \'Taylor Swift\', \'Pop\')
Artist(4, \'Nina Simone\', \'Jazz\')\
"""

"""
When: we make a GET request to /albums
Then: it returns HTML with the following in the body:
    <h1>Albums</h1>

    <div>
        Title: {{TITLE}}
        Released: {{RELEASE_YEAR}}
    </div>

    <!-- (for each of the 12 albums in the seed data) -->
"""
def test_get_albums_returns_page_with_all_albums(db_connection, page, test_web_address):
    db_connection.seed("seeds/music_web_app.sql")

    page.goto(f"http://{test_web_address}/albums")

    album_info_divs_locator = page.locator(".album_info")
    expect(album_info_divs_locator).to_have_count(12)

    titles = [
        'Doolittle',
        'Surfer Rosa',
        'Waterloo',
        'Super Trouper',
        'Bossanova',
        'Lover',
        'Folklore',
        'I Put a Spell on You',
        'Baltimore',
        'Here Comes the Sun',
        'Fodder on My Wings',
        'Ring Ring',
    ]
    release_years = [
        "1989",
        "1988",
        "1974",
        "1980",
        "1990",
        "2019",
        "2020",
        "1965",
        "1978",
        "1971",
        "1982",
        "1973",
    ]

    for i in range(12):
        album_info_locator = page.get_by_test_id(f"album_{i}")

        title_locator = album_info_locator.locator(".album_title")
        release_year_locator = album_info_locator.locator(".album_release_year")

        expect(title_locator).to_have_text(f"Title: {titles[i]}")
        expect(release_year_locator).to_have_text(f"Released: {release_years[i]}")
