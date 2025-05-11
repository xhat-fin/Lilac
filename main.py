from flask import Flask, render_template, request, redirect, url_for, jsonify
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
    plants = db.get_all_plants()
    return render_template('index.html', plants=plants)


@app.route('/plant', methods=['POST'])
def plant():
    name = request.form['name']
    ptype = request.form['type']
    planted_by = request.form['planted_by']
    db.plant(name, ptype, planted_by)
    return redirect(url_for('index'))


@app.route("/water/<int:id>", methods=["GET", "POST"])
def water(id):
    if request.method == "POST":
        # Сохраняем ответы на вопросы
        for i in range(len(QUESTIONS)):
            answer = request.form.get(f"q{i}")
            db.insert_quest(id, QUESTIONS[i], answer)

        # Обновляем время последнего полива и при необходимости увеличиваем стадию
        db.update_stage(id)
        return redirect(url_for("index"))
    return render_template("water.html", questions=QUESTIONS)



@app.route("/delete/<int:id>", methods=["DELETE"])
def delete_plant(id):
    db.delete_plant(id)
    return jsonify(success=True)


@app.route("/plant/<int:id>/history")
def plant_history(id):
    plant = db.get_plant(id)
    reflections = db.get_reflections(id)
    return render_template("history.html", plant=plant, reflections=reflections)



if __name__ == '__main__':
    app.run(debug=True)
