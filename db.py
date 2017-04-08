import sqlite3

conn = sqlite3.connect('notes.db', check_same_thread = False)
cur = conn.cursor()

def get_notes(user_id):
    cur.execute('SELECT * FROM notes WHERE user_id=? ORDER BY date ASC;', [user_id])
    notes = cur.fetchall()
    return notes

def count_notes(user_id):
    cur.execute('SELECT COUNT(id) FROM notes WHERE user_id=?;', [user_id])
    count = cur.fetchall()
    return count[0][0]

def insert_note(user_id, note_text, date):
    cur.execute('INSERT INTO notes (user_id, text_note, date) VALUES (?, ?, ?);', (user_id, str(note_text), date))
    conn.commit()

def update_note(id_note, note_text):
    cur.execute('UPDATE notes SET text_note=? WHERE id=?', (str(note_text), id_note))
    conn.commit()

def delete_note(id_note):
    cur.execute('DELETE FROM notes WHERE id=?', [id_note])
    conn.commit()