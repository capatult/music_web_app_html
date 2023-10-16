from playwright.sync_api import Page, expect

# Tests for your routes go here

UTF_8 = "utf-8"

"""
When: we make a GET request to /albums
Then: it returns HTML with the following in the body:
    <h1>Albums</h1>

    <div class="album_info" data-testid="album_{{TEST_ID}}">
        <span>
            <a href="/albums/{{ALBUM_ID}} class="link_to_album_page">
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
Then: it returns HTML with the following in the body:
    <h1>{{TITLE}}</h1>

    <div class="album_info">
        <span class="album_release_year" data-testid="release_year">
            Release year: {{RELEASE_YEAR}}
        </span>
        <span class="album_artist" data-testid="artist">
            Artist: {{ARTIST}}
        </span>
    </div>
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
Then: it returns a 500 status code (Internal server error) or 404 status code
"""
def test_get_album_by_id_returns_500_or_404_error_if_id_invalid(db_connection, web_client):
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
    status_codes = [
        response.status_code
        for response in responses
    ]
    assert status_codes == [500, 500, 404, 404, 404]

"""
When: we make a GET request to /artists/<id>
And:  we provide a value for <id> which corresponds to an existing row in the `artists` table
Then: it returns HTML with the following in the body:
    <h1>{{NAME}}</h1>

    <div class="artist_info">
        <span class="artist_genre" data-testid="genre">
            Genre: {{GENRE}}
        </span>
    </div>
"""
def test_get_artist_by_id_returns_page_with_artist_info_if_id_valid(db_connection, page, test_web_address):
    db_connection.seed("seeds/music_web_app.sql")

    for artist_id, name, genre in zip(
        [1, 4],
        ["Pixies", "Nina Simone"],
        ["Rock", "Jazz"]
    ):
        page.goto(f"http://{test_web_address}/artists/{artist_id}")
        expect(page.locator("h1")).to_have_text(name)

        genre_locator = page.get_by_test_id("genre")

        expect(genre_locator).to_have_text(f"Genre: {genre}")

"""
When: we make a GET request to /artists/<id>
And:  we provide a value for <id> which does not correspond to an existing artist
Then: it returns a 500 status code (Internal server error) or 404 status code
"""
def test_get_artist_by_id_returns_500_or_404_error_if_id_invalid(db_connection, web_client):
    db_connection.seed("seeds/music_web_app.sql")
    responses = [
        web_client.get(f"/artists/{x}") for x in [
            "0",
            "5",
            "-1",
            "3.14",
            "hello",
        ]
    ]
    status_codes = [
        response.status_code
        for response in responses
    ]
    assert status_codes == [500, 500, 404, 404, 404]

"""
When: we make a GET request to /artists
Then: it returns HTML with the following in the body:
    <h1>Artists</h1>

    <div class="artist_info" data-testid="artist_{{TEST_ID}}">
        <span>
            <a href="/artists/{{ALBUM_ID}} class="link_to_artist_page>
                {{TITLE}}
            </a>
        </span>
    </div>

    <!-- (for each of the 4 artists in the seed data) -->
"""
def test_get_artists_returns_page_with_links_to_all_artists(db_connection, page, test_web_address):
    db_connection.seed("seeds/music_web_app.sql")

    page.goto(f"http://{test_web_address}/artists")
    expect(page.locator("h1")).to_have_text("Artists")

    artist_info_divs_locator = page.locator(".artist_info")
    expect(artist_info_divs_locator).to_have_count(4)

    names = [
        'Pixies',
        'ABBA',
        'Taylor Swift',
        'Nina Simone',
    ]
    genres = [
        'Rock',
        'Pop',
        'Pop',
        'Jazz',
    ]

    for i in range(4):
        page.goto(f"http://{test_web_address}/artists")
        artist_info_locator = page.get_by_test_id(f"artist_{i}")
        artist_info_locator.get_by_text(f"{names[i]}").click()

        # Now this section is the same as in the GET /artists/<id> test
        expect(page.locator("h1")).to_have_text(names[i])

        genre_locator = page.get_by_test_id("genre")

        expect(genre_locator).to_have_text(f"Genre: {genres[i]}")

"""
When: we make a GET request to /albums/new
Then: it returns a page with a form allowing the user to add a new album to the database
"""
def test_get_albums_new_returns_page_with_form_to_add_new_album(db_connection, page, test_web_address):
    db_connection.seed("seeds/music_web_app.sql")

    page.goto(f"http://{test_web_address}/albums/new")
    expect(page.locator("h1")).to_have_text("Create New Album")

    page.locator("input[name='title']").fill("Voyage")
    page.locator("input[name='release_year']").fill("2022")
    page.locator("select[name='artist_id']").select_option(label="ABBA")
    page.locator("text=Submit form").click()

    # Now we should be on the page for the new album
    expect(page.locator("h1")).to_have_text("Voyage")
    release_year_locator = page.get_by_test_id("release_year")
    artist_locator = page.get_by_test_id("artist")

    expect(release_year_locator).to_have_text(f"Release year: 2022")
    expect(artist_locator).to_have_text(f"Artist: ABBA")
