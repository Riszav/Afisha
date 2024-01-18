from django.db import models

class Director(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    @property
    def movies_count(self):
        count = 0
        for i in self.movies.all():
            count += 1
        return count


class Movie(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    duration = models.FloatField()
    director = models.ForeignKey(
        "movie_app.Director",
        on_delete=models.DO_NOTHING,
        related_name="movies"
    )

    def __str__(self):
        return self.title

    @property
    def director_name(self):
        return self.director.name

    @property
    def average_rating(self):
        summ = 0
        count = 0
        for i in self.reviews.all():
            summ += i.stars
            count += 1


        average = summ / count
        return average


STAR_CHOICES = (
    (i, '* ' * i) for i in range(1,6)
)
class Review(models.Model):
    text = models.TextField(null=True, blank=True)
    movie = models.ForeignKey(
        "movie_app.Movie",
        on_delete=models.CASCADE,
        related_name="reviews"
    )
    stars = models.IntegerField(choices=STAR_CHOICES, default=5)

    def __str__(self):
        return f'"{self.movie}" - {self.text}'

