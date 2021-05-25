from dataclasses import dataclass


@dataclass
class IMDBData:
    name: str
    id: str
    year: int
    director: str
    director_id: int
    release_day: str
    stars: list
    rating: float
    duration: int  # in minutes
    votes: int
    genres: list
    description: str
    cast: list
    budget: int

    def __str__(self):
        output = self.__class__.__name__ + "(\n"
        for (cnt, (key, value)) in enumerate(self.__dict__.items()):
            output += f'{key}={value.__str__()}'
            if cnt != len(self.__dict__.items()) - 1:
                output += ",\n"
        output += ")"
        return output