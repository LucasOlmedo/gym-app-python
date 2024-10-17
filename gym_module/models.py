import math
from django.db import models
from django.utils import timezone

class Exercise(models.Model):

    body_part = models.CharField(max_length=100)
    equipment = models.CharField(max_length=100)
    gif_url = models.CharField(max_length=100)
    ref_id = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    target = models.CharField(max_length=100)
    secondary_muscles = models.TextField()
    instructions = models.TextField()

    def __str__(self):
        return self.name


class PersonalInfo(models.Model):

    GENDER = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    
    ACTIVITY_LEVEL = [
        ('sedentary', 'Sedentary'),
        ('light', 'Lightly active'),
        ('moderate', 'Moderately active'),
        ('active', 'Active'),
        ('very_active', 'Very active'),
    ]

    # Personal Info
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=GENDER)
    age = models.PositiveIntegerField()
    height_cm = models.DecimalField(max_digits=5, decimal_places=2)
    weight_kg = models.DecimalField(max_digits=5, decimal_places=2)
    activity_level = models.CharField(max_length=20, choices=ACTIVITY_LEVEL)

    # Body Metrics - Upper Body
    neck_circumference = models.DecimalField(max_digits=5, decimal_places=2)
    shoulder_circumference = models.DecimalField(max_digits=5, decimal_places=2)
    chest_circumference = models.DecimalField(max_digits=5, decimal_places=2)

    arm_left_circumference = models.DecimalField(max_digits=5, decimal_places=2)
    arm_right_circumference = models.DecimalField(max_digits=5, decimal_places=2)

    forearm_left_circumference = models.DecimalField(max_digits=5, decimal_places=2)
    forearm_right_circumference = models.DecimalField(max_digits=5, decimal_places=2)

    # Body Metrics - Lower Body
    waist_circumference = models.DecimalField(max_digits=5, decimal_places=2)
    high_hip_circumference = models.DecimalField(max_digits=5, decimal_places=2)
    hip_circumference = models.DecimalField(max_digits=5, decimal_places=2)

    thigh_left_circumference = models.DecimalField(max_digits=5, decimal_places=2)
    thigh_left_lower_circumference = models.DecimalField(max_digits=5, decimal_places=2)
    thigh_right_circumference = models.DecimalField(max_digits=5, decimal_places=2)
    thigh_right_lower_circumference = models.DecimalField(max_digits=5, decimal_places=2)

    calf_left_circumference = models.DecimalField(max_digits=5, decimal_places=2)
    calf_right_circumference = models.DecimalField(max_digits=5, decimal_places=2)

    body_fat_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    measurement_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

    # BMI - Body Mass Index
    def calculate_bmi(self):
        return self.weight_kg / (self.height_cm / 100) ** 2

    # BMR - Basal Metabolic Rate
    def calculate_bmr(self):
        if self.gender == 'M':
            return 88.362 + (13.397 * self.weight_kg) + (4.799 * self.height_cm) - (5.677 * self.age)
        else:
            return 447.593 + (9.247 * self.weight) + (3.098 * self.height) - (4.330 * self.age)

    # LBM - Lean Body Mass
    def calculate_lbm(self):
        if self.body_fat_percentage:
            return self.weight * (1 - (self.body_fat_percentage / 100))
        return None

    # Strength - 1RM
    def calculate_1rm(self, exercise_weight, reps):
        return exercise_weight * (1 + (reps / 30))

    # TDEE - Total Daily Energy Expenditure
    def calculate_tdee(self):
        bmr = self.calculate_bmr()
        activity_multiplier = {
            'sedentary': 1.2,
            'light': 1.375,
            'moderate': 1.55,
            'active': 1.725,
            'very_active': 1.9
        }
        return bmr * activity_multiplier[self.activity_level]

    # RMR - Resting Metabolic Rate
    def calculate_rmr(self):
        if self.gender == 'M':
            return (10 * self.weight) + (6.25 * self.height) - (5 * self.age) + 5
        else:
            return (10 * self.weight) + (6.25 * self.height) - (5 * self.age) - 161

    # FFMI - Fat-Free Mass Index
    def calculate_ffmi(self):
        if self.body_fat_percentage:
            return (self.lbm / 2.2) / ((self.height / 100) ** 2) + 6.1 * (1.8 - (self.height / 100))
        return None

    # IAC - Index of Central Adiposity
    def calculate_iac(self):
        return (self.hip_circumference / (self.height ** 1.5)) - 18

    # Fat Mass
    def calculate_fat_mass(self):
        if self.body_fat_percentage:
            return self.weight * (self.body_fat_percentage / 100)
        return None

    # VO2 Max
    def calculate_vo2max(self, distance_ran_in_meters):
        return (distance_ran_in_meters - 504.9) / 44.73

    # Fat Loss Goal
    def calculate_fat_loss_goal(self, target_body_fat_percentage):
        lean_mass = self.calculate_lean_body_mass()
        return lean_mass / (1 - (target_body_fat_percentage / 100)) - self.weight

    # Power - Newtons
    def calculate_power(self, weight_lifted, time_in_seconds):
        return weight_lifted * 9.81 / time_in_seconds

    # WHR - Waist-to-Hip Ratio
    def calculate_whr(self):
        return self.waist_circumference / self.hip_circumference

    # MET - Metabolic Equivalent of Task
    def calculate_met(self, exercise_duration_in_minutes):
        return 0.0175 * exercise_duration_in_minutes

    # Calories Burned
    def calculate_calories_burned(self, duration_in_minutes):
        return self.calculate_met(duration_in_minutes) * self.weight * 3.5 / 200

    # Heart Rate - Maximum
    def calculate_max_heart_rate(self):
        return 220 - self.age

    # BioType
    def calculate_biotype(self):
        bmi = self.calculate_bmi()
        waist_height_ratio = self.calculate_whr()

        if bmi < 18.5 and self.body_fat_percentage < 15 and waist_height_ratio < 0.42:
            return "Ectomorph"
        elif 18.5 <= bmi <= 24.9 and 15 <= self.body_fat_percentage <= 20 and 0.42 <= waist_height_ratio <= 0.49:
            return "Mesomorph"
        elif bmi > 24.9 or self.body_fat_percentage > 20 or waist_height_ratio > 0.49:
            return "Endomorph"
        else:
            return "Unknown"

    # Body Fat Percentage
    def calculate_body_fat_percentage(self):
        if self.gender == 'M':
            body_fat = 86.010 * math.log10(self.waist_circumference - self.neck_circumference) - \
                       70.041 * math.log10(self.height_cm) + 36.76
        else:
            body_fat = 163.205 * math.log10(self.waist_circumference + self.hip_circumference - self.neck_circumference) - \
                       97.684 * math.log10(self.height_cm) - 78.387

        return round(body_fat, 2) if body_fat is not None else None

class WorkoutSession(models.Model):
    personal_info = models.ForeignKey(PersonalInfo, on_delete=models.CASCADE, related_name='workout_sessions')
    session_name = models.CharField(max_length=100, blank=True, null=True)
    date = models.DateTimeField(default=timezone.now)
    notes = models.TextField(blank=True, null=True)
    duration = models.DurationField(blank=True, null=True)

    def __str__(self):
        return f"Workout Session on {self.date} for {self.personal_info}"

class WorkoutHistory(models.Model):
    workout_session = models.ForeignKey(WorkoutSession, on_delete=models.CASCADE, related_name="workout_histories")
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    duration = models.DurationField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.personal_info} - {self.exercise} - {self.date}"

class WorkoutSet(models.Model):
    workout_history = models.ForeignKey(WorkoutHistory, on_delete=models.CASCADE, related_name="sets")
    set_number = models.IntegerField()
    weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    reps = models.IntegerField()
    notes = models.TextField(blank=True, null=True)
    rest_time = models.DurationField(blank=True, null=True)