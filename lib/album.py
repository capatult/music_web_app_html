import re

class Album:
    # Attributes needed:
    #   id: INTEGER -> int
    #   title: VARCHAR(255) -> str
    #   release_year: INTEGER -> int
    #   artist_id: INTEGER -> int
    def __init__(self, id, title, release_year, artist_id):
        self.id = id
        self.title = title
        self.release_year = release_year
        self.artist_id = artist_id

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __repr__(self):
        return f"""Album({", ".join(
            repr(x) for x in [
                self.id, self.title, self.release_year, self.artist_id
            ]
        )})"""

    @classmethod
    def new_from_form_data(cls, title, release_year, artist_id):
        new = cls(None, None, None, None)
        new.title = (
            None if title is None
            or str(title) == ""
            else str(title)
        )
        new.release_year = (
            None if release_year is None
            or not re.fullmatch(r"-?\d+", str(release_year))
            else int(str(release_year))
        )
        new.artist_id = (
            None if artist_id is None
            or not str(artist_id).isnumeric()
            else int(str(artist_id))
        )
        return new

    def _id_is_valid(self):
        return (isinstance(self.id, int) and self.id > 0) or (self.id == None)

    def _title_is_valid(self):
        if not isinstance(self.title, str):
            return False
        return len(self.title) > 0

    def _release_year_is_valid(self):
        return isinstance(self.release_year, int)

    def _artist_id_is_valid(self):
        return isinstance(self.artist_id, int) and self.artist_id > 0

    def is_valid(self):
        return all((
            self._id_is_valid(),
            self._title_is_valid(),
            self._release_year_is_valid(),
            self._artist_id_is_valid()
        ))

    def generate_errors(self):
        errors = []
        if not self._id_is_valid():
            errors.append("ID must be positive")
        if not self._title_is_valid():
            errors.append("The title cannot be blank")
        if not self._release_year_is_valid():
            errors.append("The release year cannot be blank")
        if not self._artist_id_is_valid():
            errors.append("The artist must be selected")
        return (
            None if len(errors) == 0
            else "; ".join(errors)
        )

    # def generate_errors(self):
    #     errors = []
    #     if self.id == 0:
    #         errors.append("ID must be positive")
    #     if (self.title is None) or (self.title == ""):
    #         errors.append("The title cannot be blank")
    #     if self.release_year is None:
    #         errors.append("The release year cannot be blank")
    #     if (self.artist_id is None) or (self.artist_id == 0):
    #         errors.append("The artist must be selected")
    #     return (
    #         None if len(errors) == 0
    #         else "; ".join(errors)
    #     )
