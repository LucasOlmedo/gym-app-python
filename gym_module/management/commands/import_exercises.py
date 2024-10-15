from django.core.management.base import BaseCommand
from gym_module.models import Exercise
import requests
import os

class Command(BaseCommand):
    help = 'Import exercises from an external API and save them to the database'

    def handle(self, *args, **kwargs):

        self.stdout.write("Initializing...")

        api_url = os.environ.get('API_GYM') + '/exercises'
        params = {"limit": '-1', "offset": '0'}
        headers = {
            "x-rapidapi-key": os.environ.get('API_KEY'),
        }

        response = requests.get(api_url, headers=headers, params=params)

        if response.status_code != 200:
            self.stdout.write(self.style.ERROR('Failed to fetch data from API'))
            return

        exercises = response.json()

        total_imported = 0
        total_updated = 0

        for exercise_data in exercises:
            try:
                secondary_muscles_str = '||' . join(exercise_data.get('secondaryMuscles', []))
                instructions_str = '||' . join(exercise_data.get('instructions', []))

                exercise, created = Exercise.objects.update_or_create(
                    ref_id=exercise_data['id'],
                    defaults={
                        'body_part': exercise_data['bodyPart'],
                        'equipment': exercise_data['equipment'],
                        'gif_url': exercise_data['gifUrl'],
                        'ref_id': exercise_data['id'],
                        'name': exercise_data['name'],
                        'target': exercise_data['target'],
                        'secondary_muscles': secondary_muscles_str,
                        'instructions': instructions_str,
                    }
                )
                
                if created:
                    total_imported += 1
                    self.stdout.write(self.style.SUCCESS(f"Imported: {exercise_data['name']}"))
                else:
                    total_updated += 1
                    self.stdout.write(self.style.WARNING(f"Updated: {exercise_data['name']}"))

            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error importing - {exercise_data['name']}: {e}"))

        self.stdout.write(self.style.SUCCESS(f'Total imported: {total_imported}'))
        self.stdout.write(self.style.SUCCESS(f'Total updated: {total_updated}'))