from playwright.sync_api import Page, expect

# Tests for your routes go here

UTF_8 = "utf-8"

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

    <div class="album_info" data-testid="album_{{TEST_ID}}">
        <span class="link_to_album_page">
            <a href="/albums/{{ALBUM_ID}}>
                {{TITLE}}
            </a>
        </span>
    </div>

    <!-- (for each of the 12 albums in the seed data) -->
"""
def test_get_albums_returns_page_with_links_to_all_albums(db_connection, page, test_web_address):
    db_connection.seed("seeds/music_web_app.sql")

    page.goto(f"http://{test_web_address}/albums")
    expect(page.locator("h1")).to_have_text("Albums")

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
    artist_ids = [
        1,
        1,
        2,
        2,
        1,
        3,
        3,
        4,
        4,
        4,
        4,
        2,
    ]
    artists = [
        (None, 'Pixies', 'ABBA', 'Taylor Swift', 'Nina Simone')[i]
        for i in artist_ids
    ]

    for i in range(12):
        page.goto(f"http://{test_web_address}/albums")
        album_info_locator = page.get_by_test_id(f"album_{i}")
        # link_locator = album_info_locator.locator(".link_to_album_page")
        # link_locator.click()
        album_info_locator.get_by_text(f"{titles[i]}").click()

        # Now this section is the same as in the GET /albums/<id> test
        expect(page.locator("h1")).to_have_text(titles[i])

        release_year_locator = page.get_by_test_id("release_year")
        artist_locator = page.get_by_test_id("artist")

        expect(release_year_locator).to_have_text(f"Release year: {release_years[i]}")
        expect(artist_locator).to_have_text(f"Artist: {artists[i]}")

"""
When: we make a GET request to /albums/<id>
And:  we provide a value for <id> which corresponds to an existing row in the `albums` table
Then: it returns HTML with the following in the body
"""
def test_get_album_by_id_returns_page_with_album_info_if_id_valid(db_connection, page, test_web_address):
    db_connection.seed("seeds/music_web_app.sql")

    for album_id, title, release_year, artist in zip(
        [1, 12],
        ["Doolittle", "Ring Ring"],
        ["1989", "1973"],
        ["Pixies", "ABBA"]
    ):
        page.goto(f"http://{test_web_address}/albums/{album_id}")
        expect(page.locator("h1")).to_have_text(title)

        release_year_locator = page.get_by_test_id("release_year")
        artist_locator = page.get_by_test_id("artist")

        expect(release_year_locator).to_have_text(f"Release year: {release_year}")
        expect(artist_locator).to_have_text(f"Artist: {artist}")

"""
When: we make a GET request to /albums/<id>
And:  we provide a value for <id> which does not correspond to an existing album
Then: it returns a 500 status code (Internal server error)
"""
def test_get_album_by_id_returns_404_error_if_id_invalid(db_connection, web_client):
    db_connection.seed("seeds/music_web_app.sql")
    responses = [
        web_client.get(f"/albums/{x}") for x in [
            "0",
            "13",
            "-1",
            "3.14",
            "hello",
        ]
    ]
    for response, expected_status_code in zip(
        responses, [
            500,
            500,
            404,
            404,
            404,
        ]
    ):
        assert response.status_code == expected_status_code
