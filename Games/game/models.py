from django.db import models

class Game(models.Model):
    name = models.CharField(max_length=150, verbose_name="Название игры")
    description = models.TextField(max_length=500, verbose_name="Описание игры")
    stage_number = models.IntegerField(verbose_name="Номер этапа", default=1)
    end_date = models.DateField(verbose_name="Дата окончания этапа")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Игра"
        verbose_name_plural = "Игры"


class User(models.Model):
    name = models.CharField(max_length=150, verbose_name="Имя пользователя")
    stage1 = models.BooleanField(default=False)
    stage2 = models.BooleanField(default=False)
    game = models.ForeignKey(Game, on_delete=models.SET_NULL, null=True, verbose_name="Игра")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
