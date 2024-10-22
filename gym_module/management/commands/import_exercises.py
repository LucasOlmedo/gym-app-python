from django.core.management.base import BaseCommand
from gym_module.models import Exercise
import requests
import os
from django.db import connection

class Command(BaseCommand):
    help = 'Import exercises from an external API and save them to the database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--update',
            action='store_true',
            help='Update existing exercises if they exist, instead of just adding new ones.'
        )

    def handle(self, *args, **kwargs):
        update_existing = kwargs['update']

        self.stdout.write("Initializing...")
        connection.queries_log.clear()

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
        existing_exercises = Exercise.objects.in_bulk(field_name='ref_id')

        new_exercises = []
        updated_exercises = []
        total_imported = 0
        total_updated = 0

        for exercise_data in exercises:
            try:
                secondary_muscles_str = '||' . join(exercise_data.get('secondaryMuscles', []))
                instructions_str = '||' . join(exercise_data.get('instructions', []))

                existing_exercise = existing_exercises.get(exercise_data['id'])

                if existing_exercise:
                    if not update_existing:
                        continue
                    else:
                        existing_exercise.body_part = exercise_data['bodyPart']
                        existing_exercise.equipment = exercise_data['equipment']
                        existing_exercise.gif_url = exercise_data['gifUrl']
                        existing_exercise.name = exercise_data['name']
                        existing_exercise.target = exercise_data['target']
                        existing_exercise.secondary_muscles = secondary_muscles_str
                        existing_exercise.instructions = instructions_str

                        updated_exercises.append(existing_exercise)

                        total_updated += 1
                        self.stdout.write(self.style.WARNING(f"To Update: {exercise_data['name']}"))
                else:
                    exercise_to_create = Exercise(
                        body_part=exercise_data['bodyPart'],
                        equipment=exercise_data['equipment'],
                        gif_url=exercise_data['gifUrl'],
                        ref_id=exercise_data['id'],
                        name=exercise_data['name'],
                        target=exercise_data['target'],
                        secondary_muscles=secondary_muscles_str,
                        instructions=instructions_str,
                    )

                    new_exercises.append(exercise_to_create)

                    total_imported += 1
                    self.stdout.write(self.style.SUCCESS(f"To Create: {exercise_data['name']}"))

            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error importing - {exercise_data['name']}: {e}"))

        if new_exercises:
            self.stdout.write('Bulk creating new exercises...')
            Exercise.objects.bulk_create(new_exercises)

        if updated_exercises:
            self.stdout.write('Bulk updating existing exercises...')
            Exercise.objects.bulk_update(updated_exercises, [
                'body_part', 'equipment', 'gif_url', 'name', 'target', 
                'secondary_muscles', 'instructions'
            ])

        self.stdout.write(self.style.SUCCESS(f'Total imported: {total_imported}'))
        self.stdout.write(self.style.SUCCESS(f'Total updated: {total_updated}'))

        total_queries = len(connection.queries)
        self.stdout.write(f"Total Queries Executed: {total_queries}")

        self.stdout.write(self.style.SUCCESS('Done!'))
