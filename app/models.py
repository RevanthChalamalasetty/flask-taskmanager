from datetime import datetime, timezone
import uuid


class Task:
    def __init__(self, title: str, description: str = ""):
        self.id          = str(uuid.uuid4())
        self.title       = title
        self.description = description
        self.done        = False
        self.created_at  = datetime.now(timezone.utc).isoformat()

    def to_dict(self):
        return {
            "id":          self.id,
            "title":       self.title,
            "description": self.description,
            "done":        self.done,
            "created_at":  self.created_at,
        }


_store: dict[str, Task] = {}


def all_tasks():
    return [t.to_dict() for t in _store.values()]

def get_task(task_id: str):
    return _store.get(task_id)

def create_task(title: str, description: str = "") -> Task:
    t = Task(title, description)
    _store[t.id] = t
    return t

def update_task(task_id: str, **kwargs):
    t = _store.get(task_id)
    if not t:
        return None
    for k, v in kwargs.items():
        if hasattr(t, k):
            setattr(t, k, v)
    return t

def delete_task(task_id: str) -> bool:
    if task_id in _store:
        del _store[task_id]
        return True
    return False
