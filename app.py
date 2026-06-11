from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:adminadmin@database-1.cj6w02cuehgf.us-east-1.rds.amazonaws.com/taskdb'
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_pre_ping": True
}

db = SQLAlchemy(app)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(50), default='Pending')


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return {"message": "Task Manager API Running"}


@app.route("/tasks", methods=["POST"])
def create_task():
    data = request.json

    task = Task(
        task_name=data["task_name"]
    )

    db.session.add(task)
    db.session.commit()

    return jsonify({
        "message": "Task created"
    })


@app.route("/tasks", methods=["GET"])
def get_tasks():
    tasks = Task.query.all()

    result = []

    for task in tasks:
        result.append({
            "id": task.id,
            "task_name": task.task_name,
            "status": task.status
        })

    return jsonify(result)


@app.route("/tasks/<int:id>", methods=["PUT"])
def update_task(id):
    task = Task.query.get_or_404(id)

    data = request.json
    
    if data["status"] not in ["Pending", "Completed"]:
        return jsonify({
            "message": "Invalid status. Must be 'Pending' or 'Completed'."
        }), 400
    
    if not data["task_name"]:
        return jsonify({
            "message": "Task name cannot be empty."
        }), 400
    if not data["status"]:
        return jsonify({
            "message": "Status cannot be empty."
        }), 400
    
    task.status = data["status"]
    task.task_name = data["task_name"]
    task.id = id

    db.session.commit()

    return jsonify({
        "message": "Task updated"
    })


@app.route("/tasks/<int:id>", methods=["DELETE"])
def delete_task(id):
    task = Task.query.get_or_404(id)

    db.session.delete(task)
    db.session.commit()

    return jsonify({
        "message": "Task deleted"
    })


if __name__ == "__main__":
    app.run(debug=True)