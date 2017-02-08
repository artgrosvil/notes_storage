import psycopg2
import config

conn = psycopg2.connect('host=' + config.db_host + ' dbname=' + config.db_name + ' user=' + config.db_user + ' password=' + config.db_password)
cur = conn.cursor()

def get_notes(user_id):
    cur.execute('SELECT * FROM notes WHERE user_id=%s ORDER BY date ASC;', [user_id])
    notes = cur.fetchall()
    return notes

def count_notes(user_id):
    cur.execute('SELECT COUNT(id) FROM notes WHERE user_id=%s;', [user_id])
    count = cur.fetchall()
    return count[0][0]

def insert_note(user_id, note_text):
    cur.execute('INSERT INTO notes (user_id, text_note) VALUES (%s, %s);', (user_id, str(note_text)))
    conn.commit()

def update_note(id_note, note_text):
    cur.execute('UPDATE notes SET text_note=%s WHERE id=%s', (str(note_text), id_note))
    conn.commit()

def delete_note(id_note):
    cur.execute('DELETE FROM notes WHERE id=%s', [id_note])
    conn.commit()