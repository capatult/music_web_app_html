import os
from flask import Flask, request, render_template, redirect
from lib.database_connection import get_flask_database_connection
from lib.album_repository import AlbumRepository
from lib.album import Album
from lib.artist_repository import ArtistRepository
from lib.artist import Artist

# Create a new Flask app
app = Flask(__name__)


# @app.route('/psb', methods=['GET'])
# def psb():
#     conn = get_flask_database_connection(app)
#     repo = ArtistRepository(get_flask_database_connection(app))
#     psb = Artist(None, 'Pet Shop Boys', 'Pop')
#     repo.create(psb)
#     return "done"

@app.route('/artists', methods=['GET'])
def get_artists():
    connection = get_flask_database_connection(app)
    repository = ArtistRepository(connection)
    all_artists = repository.all()
    return render_template(
        'artists/index.html',
        artists=[
            {
                "test_id": i,
                "id": artist.id,
                "name": artist.name
            }
            for i, artist in enumerate(all_artists)
        ]
    )

@app.route('/artists/<int:artist_id>', methods=['GET'])
def get_artist_by_id(artist_id):
    connection = get_flask_database_connection(app)
    repository = ArtistRepository(connection)
    try:
        artist = repository.find(artist_id)
    except Exception:
        return render_template('error.html'), 500
    
    return render_template(
        'artists/show.html',
        artist=artist
    )

@app.route('/albums', methods=['GET'])
def get_albums():
    connection = get_flask_database_connection(app)
    repository = AlbumRepository(connection)
    all_albums = repository.all()
    return render_template(
        'albums/index.html',
        albums=[
            {
                "test_id": i,
                "id": album.id,
                "title": album.title
            }
            for i, album in enumerate(all_albums)
        ]
    )

@app.route('/albums/<int:album_id>', methods=['GET'])
def get_album_by_id(album_id):
    connection = get_flask_database_connection(app)
    album_repository = AlbumRepository(connection)
    artist_repository = ArtistRepository(connection)

    try:
        album = album_repository.find(album_id)
        artist = artist_repository.find(album.artist_id)
    except Exception:
        return render_template('error.html'), 500
    
    return render_template(
        'albums/show.html',
        album=album,
        artist=artist.name
    )

@app.route('/albums/new', methods=['GET'])
def get_new_album_creation_form():
    connection = get_flask_database_connection(app)
    artist_repository = ArtistRepository(connection)
    artists = artist_repository.all()
    return render_template(
        'albums/new.html',
        artists=artists
    )

@app.route('/albums', methods=['POST'])
def post_new_album_creation_form():
    connection = get_flask_database_connection(app)
    album_repository = AlbumRepository(connection)
    artist_repository = ArtistRepository(connection)

    # title = request.form['title']
    new_album = Album.new_from_form_data(
        request.form['title'],
        request.form['release_year'],
        request.form['artist_id']
    )

    if not new_album.is_valid():
        errors = new_album.generate_errors()
        if errors is None:
            errors = "no errors"
        # if new_album.artist_id not in
        return render_template(
            'albums/new.html',
            album=new_album,
            artists=artist_repository.all(),
            errors=errors
        ), 400

    album_repository.create(new_album)  # Side effect: set `new_album.id`
    return redirect(f"/albums/{new_album.id}")


# These lines start the server if you run this file directly
# They also start the server configured to use the test database
# if started in test mode.
if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get('PORT', 5001)))
