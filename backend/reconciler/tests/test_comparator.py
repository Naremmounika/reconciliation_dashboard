from django.test import SimpleTestCase

from reconciler.services.comparator import compare_records


class FakeRecord:
    def __init__(self, record_id, location_id, total_value):
        self.record_id = record_id
        self.location_id = location_id
        self.total_value = total_value


class FakeEntry:
    def __init__(self, entry_id, record_ref, location_id, value):
        self.entry_id = entry_id
        self.record_ref = record_ref
        self.location_id = location_id
        self.value = value


class ComparatorTests(SimpleTestCase):
    def test_missing_record_in_system_b(self):
        system_a = [
            FakeRecord("REC-1001", "LOC-201", "100.00"),
        ]

        system_b = []

        results = compare_records(system_a, system_b)

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["reason"], "MISSING_IN_B")

    def test_orphan_record_in_system_b(self):
        system_a = []

        system_b = [
            FakeEntry("ENT-1", "REC-9999", "LOC-201", "100.00"),
        ]

        results = compare_records(system_a, system_b)

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["reason"], "ORPHAN_IN_B")

    def test_duplicate_record_in_system_b(self):
        system_a = [
            FakeRecord("REC-1001", "LOC-201", "100.00"),
        ]

        system_b = [
            FakeEntry("ENT-1", "REC-1001", "LOC-201", "100.00"),
            FakeEntry("ENT-2", "REC-1001", "LOC-201", "100.00"),
        ]

        results = compare_records(system_a, system_b)

        reasons = [result["reason"] for result in results]

        self.assertIn("DUPLICATE_IN_B", reasons)

    def test_value_mismatch(self):
        system_a = [
            FakeRecord("REC-1001", "LOC-201", "100.00"),
        ]

        system_b = [
            FakeEntry("ENT-1", "REC-1001", "LOC-201", "150.00"),
        ]

        results = compare_records(system_a, system_b)

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["reason"], "VALUE_MISMATCH")