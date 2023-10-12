import os
from flask import Flask, request, render_template
from lib.database_connection import get_flask_database_connection
from lib.album_repository import AlbumRepository
from lib.album import Album
from lib.artist_repository import ArtistRepository
from lib.artist import Artist

# Create a new Flask app
app = Flask(__name__)

# == Your Routes Here ==
# @app.route('/albums', methods=['GET'])
# def get_albums():
#     connection = get_flask_database_connection(app)
#     repository = AlbumRepository(connection)
#     return "\n".join(
#         repr(album)
#         for album in repository.all()
#     )

@app.route('/artists', methods=['GET'])
def get_artists():
    connection = get_flask_database_connection(app)
    repository = ArtistRepository(connection)
    return "\n".join(
        repr(artist)
        for artist in repository.all()
    )

@app.route('/albums', methods=['GET'])
def get_albums():
    connection = get_flask_database_connection(app)
    repository = AlbumRepository(connection)
    all_albums = repository.all()
    return render_template(
        'albums/index.html',
        albums=all_albums
    )


# These lines start the server if you run this file directly
# They also start the server configured to use the test database
# if started in test mode.
if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get('PORT', 5001)))
