from django.db   import models
from django.core import exceptions

NAME_LENGTH = 140
""" Maximum length of name fields in various models. This value should be
    long enough to hold any reasonable personal name, university name, district
    name, or other things like these. """

TEXT_LENGTH = 1024
""" Maximum length of descriptions fields in models below. This value should be
    long enough to hold an average paragraph of descriptive text. Maybe,
    a thousand or two of characters. """

GRADE_LENGTH = 20
""" Maximum length of the `grade` field. This value should be long enough to
    hold a number plus possible brief one-word explanation. """


class TeamOrigin(models.Model):
    name = models.CharField(max_length=NAME_LENGTH)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Team origin"


class Team(models.Model):
    name = models.CharField(max_length=NAME_LENGTH)
    description = models.TextField(max_length=TEXT_LENGTH, blank=True)
    origin = models.ForeignKey(TeamOrigin, null=True, blank=True)

    def __str__(self):
        return self.name


class CommonOrigin(models.Model):
    name = models.CharField(max_length=NAME_LENGTH)

    def __str__(self):
        return self.name


class Participant(models.Model):
    short_name  = models.CharField(max_length=NAME_LENGTH)
    full_name   = models.CharField(max_length=NAME_LENGTH, blank=True)
    origin      = models.ForeignKey(CommonOrigin, null=True, blank=True)
    grade       = models.CharField(max_length=GRADE_LENGTH, blank=True)
    team        = models.ForeignKey(Team)
    is_capitan  = models.BooleanField()

    def __str__(self):
        return self.short_name


class Leader(models.Model):
    short_name  = models.CharField(max_length=NAME_LENGTH)
    full_name   = models.CharField(max_length=NAME_LENGTH, blank=True)
    origin      = models.ForeignKey(CommonOrigin, null=True, blank=True)
    team        = models.ForeignKey(Team)

    def __str__(self):
        return self.short_name


class Jury(models.Model):
    short_name  = models.CharField(max_length=NAME_LENGTH)
    full_name   = models.CharField(max_length=NAME_LENGTH, blank=True)
    origin      = models.ForeignKey(CommonOrigin, null=True, blank=True)

    def __str__(self):
        return self.short_name


class Room(models.Model):
    name        = models.CharField(max_length=NAME_LENGTH)

    def __str__(self):
        return self.name


class Problem(models.Model):
    problem_num = models.IntegerField(primary_key=True)
    name        = models.CharField(max_length=NAME_LENGTH)
    description = models.TextField(max_length=TEXT_LENGTH, blank=True)

    def __str__(self):
        return "#{0}. {1}".format(self.problem_num, self.name)


class Fight(models.Model):

    # Python lacks proper enums and constants, so use these static
    # variables to refer to 'status' values from Python code.
    NOT_STARTED = 0
    IN_PROGRESS = 1
    COMPLETED   = 2

    STATUS_CHOICES = [
        (NOT_STARTED, "Not started"),
        (IN_PROGRESS, "In progress"),
        (COMPLETED,   "Completed")
    ]

    room        = models.ForeignKey(Room)
    fight_num   = models.IntegerField()
    start_time  = models.DateTimeField(null=True, blank=True)
    stop_time   = models.DateTimeField(null=True, blank=True)
    status      = models.PositiveSmallIntegerField(default=NOT_STARTED, choices=STATUS_CHOICES)
    team1       = models.ForeignKey(Team, related_name="team1")
    team2       = models.ForeignKey(Team, related_name="team2")
    team3       = models.ForeignKey(Team, related_name="team3", null=True, blank=True)
    team4       = models.ForeignKey(Team, related_name="team4", null=True, blank=True)
    juries      = models.ManyToManyField(Jury, blank=True)

    def clean(self):
        super().clean()

        bad = (self.start_time is not None and
               self.stop_time  is not None and
               self.start_time >= self.stop_time)
        if bad:
            raise exceptions.ValidationError({"stop_time":
                "Fight is completed before being started"})

        if self.team3 is None and self.team4 is not None:
            raise exceptions.ValidationError({"team3":
                "Team 3 must be given when team 4 is given"})

        teams = [self.team1, self.team2, self.team3, self.team4]
        teams_uniq = set(teams) - {None}
        if len(teams_uniq) < 2 or len(teams_uniq) + teams.count(None) != 4:
            raise exceptions.ValidationError(
                "Participating teams are not unigue")

    def __str__(self):
        return "Fight {0} at {1}".format(self.fight_num, self.room.name)

    class Meta:
        unique_together = ("room", "fight_num")


class FightStage(models.Model):
    fight       = models.ForeignKey(Fight)
    action_num  = models.IntegerField()
    problem     = models.ForeignKey(Problem)
    reporter    = models.ForeignKey(Participant, related_name="reporter")
    opponent    = models.ForeignKey(Participant, related_name="opponent")
    reviewer    = models.ForeignKey(Participant, related_name="reviewer", null=True, blank=True)

    def clean(self):
        super().clean()

        guys = [self.reporter, self.opponent, self.reviewer]
        guys_uniq = set(guys) - {None}
        if len(guys_uniq) < 2 or len(guys_uniq) + guys.count(None) != 3:
            raise exceptions.ValidationError(
                "Single person is assigned for two or more roles")

    class Meta:
        unique_together = ("fight", "action_num")

    def __str__(self):
        return 'Fight #{0}, stage #{1} at {2}'.format(self.fight.fight_num, self.action_num, self.fight.room.name)


class Refusal(models.Model):
    fight_stage = models.ForeignKey(FightStage)
    problem     = models.ForeignKey(Problem)

    class Meta:
        unique_together = ("fight_stage", "problem")


class JuryPoints(models.Model):
    fight_stage   = models.ForeignKey(FightStage)
    jury          = models.ForeignKey(Jury)
    reporter_mark = models.IntegerField(null=True, blank=True)
    opponent_mark = models.IntegerField(null=True, blank=True)
    reviewer_mark = models.IntegerField(null=True, blank=True)

    def clean_fields(self, exclude=None):
        super().clean_fields(exclude)

        exclude_set = set()
        if exclude is not None:
            exclude_set = set(exclude)

        if "reviewer_mark" not in exclude_set:
            bad = (self.reviewer_mark is None and
                   self.fight_stage.fight.team3 is not None)
            if bad:
                raise exceptions.ValidationError({"reviewer_mark":
                    "Reviewer mark must be set, because there is a " +
                    "reviewing team in this fight"})

        if "jury" not in exclude_set:
            juries_set = set(self.fight_stage.fight.juries.all())
            if self.jury not in juries_set:
                raise exceptions.ValidationError({"jury":
                    "Selected jury doesn't take part in the fight"})

    class Meta:
        unique_together = ("fight_stage", "jury")


class LeaderToJury(models.Model):
    leader = models.ForeignKey(Leader)
    jury = models.ForeignKey(Jury)

    class Meta:
        unique_together = ("leader", "jury")

    def __str__(self):
        return "{0} -> {1}".format(self.leader, self.jury)