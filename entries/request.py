import sqlite3
import json
from models import Entry, Mood

# This function is used to look up a single animal, 
# The id of the animal has to be passed as an argument.
# It iterates the entire list with a for..in loop. 
# For each animal, it checks if its id property is the same
# as the id that was passed into the function as a parameter.
# Finally, it returns the value of requested_animal

# function that gets list of animals, does not contain self
def get_all_entries():
    # Open a connection to the database
    with sqlite3.connect("./dailyjournal.db") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
        e.id,
        e.concept,
        e.entry,
        e.date,
        e.mood_id,
        m.label mood_label
        FROM Entry e
        JOIN Mood m
        ON m.id = e.mood_id
        """)

        # Initialize an empty list to hold all entry representations
        entries = []

        # returns everything that matches the query
        # Convert rows of data into a Python list
        # fetchall() returning a easier version of the rows that come back
        # appending entry dictionary to entry list
        # fetchall() fetches all the data
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            # Create an entry instance from the current row.
            # The database fields are specified in
            # exact order of the parameters defined in the Entry class.
            # use bracket notation to get the value of the keys, pass in parameters for class
            entry = Entry(row['id'], row['concept'], row['entry'], row['date'], row['mood_id'])
            
            # Create a Mood instance from the current row
            mood = Mood(row['mood_id'], row['mood_label'])
            
            # .__dict__ : is a dictionary or other mapping object used to store an object’s (writable) attributes.
            # Add the dictionary representation of the mood and customer to the animal
            entry.mood = mood.__dict__
            # Adds the dictionary representation of the entry to the list
            entries.append(entry.__dict__)

    # Use `json` package to properly serialize list as JSON
    # pass dumps a list of dictionaries
    return json.dumps(entries)   


def get_single_entry(id):
    with sqlite3.connect("./dailyjournal.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Use a ? parameter to inject a variable's value
        # into the SQL statement.
        # tables to grab FROM
        db_cursor.execute("""
        SELECT
        e.id,
        e.concept,
        e.entry,
        e.date,
        e.mood_id,
        m.label mood_label
        FROM Entry e
        JOIN Mood m
        ON m.id = e.mood_id
        WHERE e.id = ?
        """, ( id, ))

        # Load the single result into memory
        data = db_cursor.fetchone()

        # Create an entry instance from the current row
        entry = Entry(data['id'], data['concept'], data['entry'], data['date'], data['mood_id'])

        # Create a mood instance from the current row
        mood = Mood(data['mood_id'], data['mood_label'])
        
        # .__dict__ : is a dictionary or other mapping object used to store an object’s (writable) attributes.
        # Add the dictionary representation of the location to the entry
        entry.mood = mood.__dict__
        

    return json.dumps(entry.__dict__)    
