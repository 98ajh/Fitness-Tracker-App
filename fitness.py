"""This programme will function as a fitness tracker, allowing the user to
input details on exercises and workouts, and track goals.
The user will be provided with a menu, with options to create an exercise
and add it to the database. They will also be able to view or delete an
exercise by category.
Users can create a workout routine, made up of each exercise, as well as to
track their progress for each movement.
Finally, they will be able to choose from a pre-determined fitness goal, and
can track this by entering their distance travelled/weight lifted."""

# First import libraries we will use, sqlite3 and tabulate.
import sqlite3
from tabulate import tabulate

"""Create initial table within try statement to catch exceptions, using
db rollback"""
try:
    # Connect to database.
    db = sqlite3.connect('ftracker.db')

    # Create cursor object.
    cursor = db.cursor()

    cursor.execute('''
                   PRAGMA foreign_keys = ON
                   ''')

    # Create initial table of exercises that can be added to by user.
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS exercises(id INTEGER PRIMARY KEY,
                    exercises TEXT, category TEXT)
                   ''')


except Exception as e:
    db.rollback()
    raise e


def add_exercise():
    """Create function to allow user to add new exercise to the table, taking
    in exercise name, id and category. Inputs within try except
    statement to catch user error."""
    view_exercises()
    try:

        ex_id = int(input('Please enter the exercise id: '))
        ex_name = input('Enter exercise name: ')
        ex_cat = input('Please enter the exercise category: ')
        cursor.execute('''
                        INSERT OR REPLACE INTO exercises(id, exercises,
                        category)
                        VALUES(?,?,?)''', (ex_id, ex_name, ex_cat,))
        db.commit()
        print('Exercise added successfully!')
    except ValueError:
        print('Error. Please try again.')


def view_ex_cat():
    """Create function to view exercises within table, using tabulate
    function to print in table format, showing the exercise id and name."""

    view_cat = input('Please enter the category of'
                     'exercise you wish to view: ')
    cursor.execute('''
                   SELECT id, exercises FROM exercises WHERE category LIKE '%'
                    || ? || '%' ''', (view_cat,))
    exercises = cursor.fetchall()
    print(tabulate(exercises, headers=["ID", "Exercises"]))


def delete_cat():
    """Create function allowing user to delete a
      category of exercise from table."""
    view_exercises()

    del_cat = input('Please select the category you wish to delete: ')
    cursor.execute('''
                   DELETE FROM exercises WHERE
                    category = ? ''', (del_cat,))
    db.commit()
    print('Category successfully deleted!')


def view_exercises():
    """Function to view all exercises within exercise table, printed in table
    format. This function will be called within the create routine function
    so users be presented with exercises to choose from. """
    cursor.execute('''
                   SELECT * FROM exercises''')
    ex = cursor.fetchall()
    print(tabulate(ex, headers=["ID", "Exercises"]))


"""Execute statement to create workout table, using a workout id as a primary
key, as well as a workout name(ie Upper body 1)"""

cursor.execute('''
               CREATE TABLE IF NOT EXISTS workout_routines(workout_id
                INTEGER PRIMARY KEY, routine_name TEXT)
               ''')

"""Execute statement to create routine exercise table. This will use the
workout id from the table above as the foreign key, whilst having its own
routine id as a primary key."""


cursor.execute('''
               CREATE TABLE IF NOT EXISTS route_exercises
               (r_ex_id INTEGER PRIMARY KEY, routine_ex TEXT,
                routine_id INTEGER,
               FOREIGN KEY (routine_id)
                REFERENCES workout_routines(workout_id))
               ''')


def create_routine():
    """Function to create a workout routine using exercises
      from exercise table.
    User gives exercise a name(e.g Upper body 1), and can choose what exercises
    they want."""
    view_exercises()
    try:
        work_id = int(input('Please create/enter the workout ID: '))
        name_routine = input('Please enter the name of the routine: ')
        cursor.execute('''
                   INSERT OR REPLACE INTO workout_routines
                   (workout_id, routine_name)
                   VALUES(?,?)''', (work_id, name_routine))
        db.commit()

        route_id = int(input('Please create the exercise ID: '))
        route_ex = input('Please enter the name of the exercise '
                         'you want to add: ')
        cursor.execute('''
                   INSERT OR REPLACE into route_exercises
                       (r_ex_id, routine_ex, routine_id)
                   VALUES(?,?,?)''', (route_id, route_ex, work_id))
        db.commit()
    except ValueError:
        print('Error. Please try again.')


def view_routine():
    """Function to allow user to view a specific routine
    User will enter which routine to view(ie Upper body 1),
    and will be presented with the exercises within the
    routine in table format"""
    try:
        view_route = input('Please enter the routine you want to view: ')
        cursor.execute('''
                   SELECT workout_routines.workout_id,
                    workout_routines.routine_name, route_exercises.r_ex_id,
                   route_exercises.routine_ex FROM workout_routines JOIN
                    route_exercises ON
                    (workout_routines.workout_id = route_exercises.routine_id)
                   WHERE routine_name LIKE '%' || ? || '%' ''', (view_route,))
        routine = cursor.fetchall()
        print(tabulate(routine, headers=["Workout ID", "Workout name",
                                         "Exercise number", "Exercise name"]))
    except ValueError:
        print('Error. Please try again.')


# Execute statement to create table for goals.
cursor.execute('''
               CREATE TABLE IF NOT EXISTS goal
               (g_id INTEGER PRIMARY KEY, g_achieve TEXT)
               ''')


# Execute statement for progress table.
cursor.execute('''
               CREATE TABLE IF NOT EXISTS progression
               (exercise TEXT PRIMARY KEY,
                weight_distance INTEGER)
               ''')


def set_goals():
    """Function to add a fitness goal to the table. User can choose from 3
    pre-determined goals. This can then be tracked using the progress to
    goal function."""
    try:
        goal_menu = int(input('Please select a fitness goal,'
                              'press 1, 2 or 3:\n 1)Lose weight\n'
                              '2)Run/Row/Cycle for 25 km\n'
                              '3)Bench press 100kg\n: '))
        if goal_menu == 1:
            goal_weight = int(input('How much weight do you want to lose?: '))
            cursor.execute('''
                       INSERT OR REPLACE INTO goal(g_id, g_achieve)
                       VALUES(?,?)''', (goal_menu, goal_weight))
            db.commit()

        elif goal_menu == 2:
            goal_ex = input('Which exercise do you want to set this '
                            'goal for?: ')
            cursor.execute('''
                       INSERT OR REPLACE INTO goal(g_id, g_achieve)
                       VALUES(?,?)'''), (goal_menu, goal_ex)
            db.commit()

        elif goal_menu == 3:
            rep_goal = int(input('How many reps do you want to do this '
                                 'weight for?: '))
            cursor.execute('''
                       INSERT OR REPLACE INTO goal(g_id, g_achieve)
                       VALUES(?,?)'''), (goal_menu, rep_goal)
            db.commit()
        else:
            print('Error. Please try again.')
    except ValueError:
        print('Error. Please try again.')


# Function to view all goals within the table so user can keep track.
def view_goals():
    cursor.execute('''
                   SELECT * FROM goal''')
    goals = cursor.fetchall()
    print(tabulate(goals, headers=["Goal", "Exercise"]))


def set_ex_progress():
    """Function where user can track progress for each exercise.
    If user enters either Run/Row/Cycle they will be asked for kilometres
    any other exercise asked for weight."""
    view_exercises()
    try:
        prog_ex = input('Please enter the exercise: ')
        if prog_ex == 'Run':
            k_m = int(input('Please enter how many kilometres you can do: '))
            cursor.execute('''
                       INSERT OR REPLACE INTO progression
                       (exercise, weight_distance)
                       VALUES(?,?)''', (prog_ex, k_m))
        elif prog_ex == 'Cycle':
            k_m = int(input('Please enter how many kilometres you can do: '))
            cursor.execute('''
                       INSERT OR REPLACE INTO progression
                       (exercise, weight_distance)
                       VALUES(?,?)''', (prog_ex, k_m))
        elif prog_ex == 'Row':
            k_m = int(input('Please enter how many kilometres you can do: '))
            cursor.execute('''
                       INSERT OR REPLACE INTO progression
                       (exercise, weight_distance)
                       VALUES(?,?)''', (prog_ex, k_m))
            db.commit()
        else:
            weight_ex = int(input('Please enter how much weight'
                                  'you can use: '))
            cursor.execute('''
                       INSERT OR REPLACE INTO progression
                       (exercise, weight_distance)
                       VALUES(?,?)''', (prog_ex, weight_ex))
            db.commit()
    except ValueError:
        print('Error. Please try again.')


def view_ex_progress():
    """Function whereby a user can see their progress for each exercise,
    printed in table format, showing the exercise name and the
      weight/distance."""
    cursor.execute('''
                   SELECT * FROM progression''')
    progress = cursor.fetchall()
    print(tabulate(progress, headers=["Exercise", "KG/Kilometres"]))


"""Create function to  track whether user has met their pre-determined goal.
User can enter how much weight they have lost/how far travelled in cardio/how
much they can perform on bench press. If they have met their goal, they will
be informed of achievement."""


def progress_to_goals():
    """Create function to  track whether user has met their
      pre-determined goal.
    User can enter how much weight they have lost/how far
      travelled in cardio/how
    much they can perform on bench press. If they have met their
      goal, they will
    be informed of achievement."""
    try:
        choose_goal = int(input('Please select the goal id'
                                'to track progress: '))
        if choose_goal == 1:
            weight_progress = int(input('How much weight have you'
                                        'currently lost?: '))
            if weight_progress >= 10:
                print('Congratulations! You have met your goal to lose 10KG!')
            else:
                print('Well done! You are on your way to your goal!')
        elif choose_goal == 2:
            cardio_progress = int(input('Please enter how far you'
                                        'have travelled in kilometres: '))
            if cardio_progress >= 25:
                print('Congratulations! You have met your goal to'
                      'Run/Row/Cycle for 25KM!')
            else:
                print('Well done! You are on your way to your goal!')
        elif choose_goal == 3:
            bench_progress = int(input('How much were you able to'
                                       'bench press in your latest session?:'
                                       ''))
            if bench_progress >= 100:
                print('Congratulations! You have met your goal'
                      'to bench press 100KG!')
        else:
            print('Well done! You are on your way to your goal!')
    except ValueError:
        print('Error. Please try again.')


while True:
    print('\nMENU')
    print('1) Add exercise')
    print('2) View exercise category')
    print('3) Delete exercise category')
    print('4) Create workout routine')
    print('5) View routine')
    print('6) Set fitness goal')
    print('7) View fitness goals')
    print('8) Set exercise progress')
    print('9) View exercise progress')
    print('10) View progress to fitness goals')
    print('11) Quit')
    menu = int(input('Please choose from the menu option above: '))
    if menu == 1:
        add_exercise()
    elif menu == 2:
        view_ex_cat()
    elif menu == 3:
        delete_cat()
    elif menu == 4:
        create_routine()
    elif menu == 5:
        view_routine()
    elif menu == 6:
        set_goals()
    elif menu == 7:
        view_goals()
    elif menu == 8:
        set_ex_progress()
    elif menu == 9:
        view_ex_progress()
    elif menu == 10:
        progress_to_goals()
    elif menu == 11:
        db.close()
        exit()
    else:
        print('Error. Please try again.')
