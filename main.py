from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import db

app = Flask(__name__)


# Список вопросов для рефлексии
QUESTIONS = [
    "Что делает тебя счастливым прямо сейчас?",
    "Какая самая крутая вещь, которую ты можешь сделать? Почему ты её не делаешь?",
    "Что бы ты изменил в своей жизни, если бы не боялся?",
    "Что мешает тебе чувствовать себя живым сегодня?",
    "Чего ты боишься сейчас больше всего?",
    "Что тебе действительно важно, но ты откладываешь?",
    "Когда ты последний раз чувствовал вдохновение? Почему?",
    "Если бы ты исчез завтра, чего бы тебе не хватало?",
    "Что ты можешь сделать сегодня, чтобы стать чуть ближе к себе настоящему?"
]


@app.route('/')
def index():
    conn = db.get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT id, name, type, planted_by, growth_stage FROM plants ORDER BY id;')
    plants = cur.fetchall()
    return render_template('index.html', plants=plants)

@app.route('/plant', methods=['POST'])
def plant():
    name = request.form['name']
    ptype = request.form['type']
    planted_by = request.form['planted_by']

    conn = db.get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO plants (name, type, planted_by, growth_stage, last_watered, created_at)
        VALUES (%s, %s, %s, 0, %s, %s)
    ''', (name, ptype, planted_by, datetime.utcnow(), datetime.utcnow()))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route("/water/<int:bush_id>", methods=["GET", "POST"])
def water(bush_id):
    if request.method == "POST":
        conn = db.get_db_connection()
        cur = conn.cursor()
        now = datetime.now()

        # Сохраняем ответы на вопросы
        for i in range(len(QUESTIONS)):
            answer = request.form.get(f"q{i}")
            cur.execute("""
                INSERT INTO reflections (bush_id, question, answer, created_at)
                VALUES (%s, %s, %s, %s)
            """, (bush_id, QUESTIONS[i], answer, now))

        # Обновляем время последнего полива и при необходимости увеличиваем стадию
        cur.execute("""
            UPDATE plants
            SET last_watered = %s,
                growth_stage = LEAST(growth_stage + 1, 5)
            WHERE id = %s
        """, (now, bush_id))

        conn.commit()
        conn.close()
        return redirect(url_for("index"))

    return render_template("water.html", questions=QUESTIONS)

if __name__ == '__main__':
    app.run(debug=True)
