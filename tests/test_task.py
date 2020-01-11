import unittest
import json

from task_forge.task import Task, Note


class TaskTests(unittest.TestCase):
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

    def test_note_can_serialize_to_json(self):
        m = Note("JSON")
        j = m.to_json()
        s = json.dumps(j)
        self.assertEqual(j, json.loads(s))
        self.assertEqual(m, Note.from_dict(json.loads(s)))
