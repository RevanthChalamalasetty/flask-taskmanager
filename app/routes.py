from flask import Blueprint, jsonify, request
from . import models

tasks_bp = Blueprint("tasks", __name__)


def _err(msg, code):
    return jsonify({"error": msg}), code


@tasks_bp.get("/tasks")
def list_tasks():
    return jsonify(models.all_tasks()), 200


@tasks_bp.post("/tasks")
def create_task():
    body  = request.get_json(silent=True) or {}
    title = body.get("title", "").strip()
    if not title:
        return _err("title is required", 400)
    task = models.create_task(title, body.get("description", ""))
    return jsonify(task.to_dict()), 201


@tasks_bp.get("/tasks/<task_id>")
def get_task(task_id):
    task = models.get_task(task_id)
    if not task:
        return _err("task not found", 404)
    return jsonify(task.to_dict()), 200


@tasks_bp.patch("/tasks/<task_id>")
def update_task(task_id):
    body    = request.get_json(silent=True) or {}
    allowed = {"title", "description", "done"}
    updates = {k: v for k, v in body.items() if k in allowed}
    if not updates:
        return _err("no valid fields to update", 400)
    task = models.update_task(task_id, **updates)
    if not task:
        return _err("task not found", 404)
    return jsonify(task.to_dict()), 200


@tasks_bp.delete("/tasks/<task_id>")
def delete_task(task_id):
    if not models.delete_task(task_id):
        return _err("task not found", 404)
    return jsonify({"deleted": task_id}), 200
