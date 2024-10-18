import math
from django.db import models
from django.utils import timezone
from datetime import date

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
    birth_date = models.DateField(null=True, blank=True)
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
    @property
    def bmi(self):
        return self.weight_kg / (self.height_cm / 100) ** 2

    # BMR - Basal Metabolic Rate
    @property
    def bmr(self):
        if self.gender == 'M':
            return 88.362 + (13.397 * float(self.weight_kg)) + (4.799 * float(self.height_cm)) - (5.677 * self.age)
        else:
            return 447.593 + (9.247 * float(self.weight_kg)) + (3.098 * float(self.height_cm)) - (4.330 * self.age)

    # LBM - Lean Body Mass
    @property
    def lbm(self):
        bf = self.body_fat_percentage if self.body_fat_percentage else self.calculate_body_fat_percentage()
        return float(self.weight_kg) * (1 - (bf / 100))

    # TDEE - Total Daily Energy Expenditure
    @property
    def tdee(self):
        activity_multiplier = {
            'sedentary': 1.2,
            'light': 1.375,
            'moderate': 1.55,
            'active': 1.725,
            'very_active': 1.9
        }
        return self.bmr * activity_multiplier[self.activity_level]

    # RMR - Resting Metabolic Rate
    @property
    def rmr(self):
        if self.gender == 'M':
            return (10 * float(self.weight_kg)) + (6.25 * float(self.height_cm)) - (5 * self.age) + 5
        else:
            return (10 * float(self.weight_kg)) + (6.25 * float(self.height_cm)) - (5 * self.age) - 161

    # FFMI - Fat-Free Mass Index
    @property
    def ffmi(self):
        return (self.lbm / 2.2) / ((float(self.height_cm) / 100) ** 2) + 6.1 * (1.8 - (float(self.height_cm) / 100))

    # IAC - Index of Central Adiposity
    @property
    def iac(self):
        return (float(self.hip_circumference) / (float(self.height_cm) ** 1.5)) - 18

    # Fat Mass
    @property
    def fat_mass(self):
        bf = self.body_fat_percentage if self.body_fat_percentage else self.calculate_body_fat_percentage()
        return float(self.weight_kg) * (bf / 100)

    # WHR - Waist-to-Hip Ratio
    @property
    def whr(self):
        return self.waist_circumference / self.hip_circumference

    # Heart Rate - Maximum
    @property
    def mhr(self):
        return 220 - self.age

    # BioType
    @property
    def biotype(self):
        bf = self.body_fat_percentage if self.body_fat_percentage else self.calculate_body_fat_percentage()

        if self.bmi < 18.5 and bf < 15 and self.whr < 0.42:
            return "Ectomorph"
        elif 18.5 <= self.bmi <= 24.9 and 15 <= bf <= 20 and 0.42 <= self.whr <= 0.49:
            return "Mesomorph"
        elif self.bmi > 24.9 or bf > 20 or self.whr > 0.49:
            return "Endomorph"
        else:
            return "Unknown"

    @property
    def age(self):
        today = date.today()
        return today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))

    # Strength - 1RM
    def calculate_1rm(self, exercise_weight, reps):
        return exercise_weight * (1 + (reps / 30))

    # VO2 Max
    def calculate_vo2max(self, distance_ran_in_meters):
        return (distance_ran_in_meters - 504.9) / 44.73

    # Fat Loss Goal
    def calculate_fat_loss_goal(self, target_body_fat_percentage):
        return self.lbm / (1 - (target_body_fat_percentage / 100)) - float(self.weight_kg)

    # Power - Newtons
    def calculate_power(self, weight_lifted, time_in_seconds):
        return weight_lifted * 9.81 / time_in_seconds

    # MET - Metabolic Equivalent of Task
    def calculate_met(self, exercise_duration_in_minutes):
        return 0.0175 * exercise_duration_in_minutes

    # Calories Burned
    def calculate_calories_burned(self, duration_in_minutes):
        return self.calculate_met(duration_in_minutes) * float(self.weight_kg) * 3.5 / 200

    # Body Fat Percentage
    def calculate_body_fat_percentage(self):
        if self.gender == 'M':
            body_fat = 86.010 * math.log10(self.waist_circumference - self.neck_circumference) - \
                       70.041 * math.log10(self.height_cm) + 36.76
        else:
            body_fat = 163.205 * math.log10(self.waist_circumference + self.hip_circumference - self.neck_circumference) - \
                       97.684 * math.log10(self.height_cm) - 78.387

        return round(body_fat, 2) if body_fat is not None else None
