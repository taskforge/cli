import unittest
import json
from datetime import datetime

from task_forge.task import Task, Note, Model, date_to_string


class TaskTests(unittest.TestCase):
    def test_is_complete_and_completed(self):
        task = Task("task 1")
        self.assertEqual(task.is_complete(), False)
        self.assertEqual(task.is_complete(), task.is_completed())
        task.complete()
        self.assertEqual(task.is_complete(), True)
        self.assertEqual(task.is_complete(), task.is_completed())

    def test_unique_ids(self):
        task1 = Task("task 1")
        task2 = Task("task 2")
        task3 = Task("task 3")
        self.assertNotEqual(task1, task2)
        self.assertNotEqual(task1, task3)
        self.assertNotEqual(task2, task3)
        self.assertNotEqual(task1.created_date, task3.created_date)

    def test_sort_order(self):
        task1 = Task("task 1")
        task2 = Task("task 2")
        task3 = Task("task 3")

        listask1 = sorted([task3, task2, task1])

        self.assertEqual(listask1[0], task1)
        self.assertEqual(listask1[1], task2)
        self.assertEqual(listask1[2], task3)

        task1.priority = 3.0
        task2.priority = 1.0
        task3.priority = 2.0

        listask2 = sorted([task3, task2, task1])

        self.assertEqual(listask2[0], task1)
        self.assertEqual(listask2[1], task3)
        self.assertEqual(listask2[2], task2)


class ModelTests(unittest.TestCase):

    model_classes = [
        Task,
        Note,
    ]

    def test_task_can_serialize_to_json(self):
        m = Task("JSON")
        j = m.to_json()
        s = json.dumps(j)
        self.assertEqual(j, json.loads(s))
        self.assertEqual(m, Task.from_dict(json.loads(s)))
        # Test that completed_date can be de/serialized
        m = m.complete()
        j = m.to_json()
        s = json.dumps(j)
        self.assertEqual(j, json.loads(s))
        self.assertEqual(m, Task.from_dict(json.loads(s)))

    def test_note_can_serialize_to_json(self):
        m = Note("JSON")
        j = m.to_json()
        s = json.dumps(j)
        self.assertEqual(j, json.loads(s))
        self.assertEqual(m, Note.from_dict(json.loads(s)))

    def test_task_repr(self):
        m = Task("JSON")
        self.assertEqual(repr(m), "Task({})".format(str(m.id)))

    def test_note_repr(self):
        m = Note("JSON")
        self.assertEqual(repr(m), "Note({})".format(str(m.id)))

    def test_compare_non_model(self):
        self.assertNotEqual(Task("JSON"), 0)
        self.assertNotEqual(Note("JSON"), 0)

    def test_generic_model_to_dict(self):
        now = datetime.now()

        class GenericModel(Model):
            def __init__(self):
                self.__really_should_not_appear = 0
                self._should_not_appear = 0
                self.should_appear = 0
                self.second_attr = 1
                self.created_date = now

            def methods_should_be_ignored(self):
                pass

        m = GenericModel()
        self.assertEqual(
            m.to_dict(), {"should_appear": 0, "second_attr": 1, "created_date": now}
        )
        self.assertEqual(
            m.to_json(),
            {"should_appear": 0, "second_attr": 1, "created_date": date_to_string(now)},
        )

    def test_models_to_dict_contains_all_attributes(self):
        # Attributes that the classes inherit from Model but
        # shouldn't pass out with to_dict
        known_bad_attrs = [
            "dict_blacklist",
            "transforms",
        ]

        for model in [Task("task 1"), Note("note 1")]:
            self.assertEqual(
                sorted(list(model.to_dict().keys())),
                sorted(
                    [
                        a
                        for a in dir(model)
                        if not a.startswith("_")
                        and not callable(getattr(model, a))
                        and a not in known_bad_attrs
                    ]
                ),
            )
