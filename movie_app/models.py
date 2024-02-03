from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Director(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:  # Мета класс - Это класс, который содержит дополнительную информацию о модели
        db_table = 'directors'  # Название таблицы в базе данных (по умолчанию appname_classname (post_postinfo))
        verbose_name = 'Директор'  # Название модели в единственном числе
        verbose_name_plural = 'Директоры'  # Название модели во множественном числе

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
        on_delete=models.CASCADE,
        related_name="movies",
    )
    category = models.ForeignKey(
        "movie_app.Category",
        on_delete=models.CASCADE,
        related_name="movies",
        null=True)
    tags = models.ManyToManyField(Tag, blank=True)


    def __str__(self):
        return self.title

    class Meta:  # Мета класс - Это класс, который содержит дополнительную информацию о модели
        db_table = 'movies'  # Название таблицы в базе данных (по умолчанию appname_classname (post_postinfo))
        verbose_name = 'Кино'  # Название модели в единственном числе
        verbose_name_plural = 'Кино'  # Название модели во множественном числе


    @property
    def director_name(self):
        return self.director.name

    @property
    def average_rating(self):
        summ = 0
        count = 0
        if self.reviews.all():
            for i in self.reviews.all():
                summ += i.stars
                count += 1
            average = summ / count
            return average
        return 0


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

    class Meta:  # Мета класс - Это класс, который содержит дополнительную информацию о модели
        db_table = 'reviews'  # Название таблицы в базе данных (по умолчанию appname_classname (post_postinfo))
        verbose_name = 'Отзыв'  # Название модели в единственном числе
        verbose_name_plural = 'Отзывы'  # Название модели во множественном числе


    def __str__(self):
        return f'"{self.movie}" - {self.text}'

