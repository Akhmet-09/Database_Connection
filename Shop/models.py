from django.db import models 
from django.core.validators import MinValueValidator
class Team(models.Model):
    name = models.CharField(max_length=100,unique=True)
    city = models.CharField(max_length=100)
    founded_year = models.PositiveBigIntegerField()

    def __str__(self):
        return f"{self.name} {self.city}"
    
class Player(models.Model):
    POSITION_CHOICES = [
        ('GK','GoalKeeper'),
        ('DF','Defender'),
        ('MF','MidFielder'),
        ('FW','Forward'),
    ]
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    jersey_number = models.PositiveBigIntegerField()
    position = models.CharField(max_length=2,choices=POSITION_CHOICES)
    team = models.ForeignKey(Team,on_delete=models.CASCADE,related_name='players')

    class Meta:
        unique_together = ('team','jersey_number')

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.jersey_number}"

class Match(models.Model):
    home_team = models.ForeignKey(Team,on_delete=models.CASCADE,related_name='home_matches')
    away_team = models.ForeignKey(Team,on_delete=models.CASCADE,related_name='away_matches')
    match_date = models.DateTimeField()
    home_team_score = models.PositiveBigIntegerField(default=0)
    away_team_score = models.PositiveIntegerField(default=0)
    def __str__(self):
        return f"{self.home_team} vs {self.away_team} ({self.match_date.strftime('%Y-%m-%d')})"

class Stat(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE,related_name='stats')
    match = models.ForeignKey(
        Match,
        on_delete=models.CASCADE,
        related_name='player_stats')
    goals = models.PositiveIntegerField(default=0)
    assists = models.PositiveIntegerField(default=0)
    yellow_cards = models.PositiveIntegerField(default=0)
    red_carda = models.PositiveIntegerField(default=0)
    class Meta:
        unique_together = ('player', 'match')
    def __str__(self):
        return f"{self.player} - {self.match}"



