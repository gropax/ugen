import unittest
from ugen import TraitStructure, TraitStructureList, TraitValue, MalformedStructure, trait_structure


class TestTraitStructures(unittest.TestCase):
    def test_union(self):
        malformed = MalformedStructure()
        self.assertEqual(malformed, malformed.union(malformed))

        value1 = TraitValue("1")
        value2 = TraitValue("2")

        self.assertEqual(malformed, malformed.union(value1))
        self.assertEqual(malformed, value1.union(malformed))
        self.assertEqual(value1, value1.union(value1))
        self.assertEqual(malformed, value1.union(value2))

        list1 = trait_structure(["1", "2", "3"])
        list2 = trait_structure(["1", "2", "4"])

        self.assertEqual(malformed, malformed.union(list1))
        self.assertEqual(malformed, list1.union(malformed))
        self.assertEqual(list1, list1.union(list1))
        self.assertEqual(malformed, list1.union(list2))

        struct1 = trait_structure({"a": "1", "b": "2"})
        struct2 = trait_structure({"a": "1", "b": "3"})

        self.assertEqual(malformed, malformed.union(struct1))
        self.assertEqual(malformed, struct1.union(malformed))
        self.assertEqual(struct1, struct1.union(struct1))
        self.assertEqual(malformed, struct1.union(struct2))

        struct3 = trait_structure({"a": "1", "c": "3"})
        struct4 = trait_structure({"a": "1", "b": "2", "c": "3"})

        self.assertEqual(struct4, struct1.union(struct3))

        struct5 = trait_structure({"a": "1", "b": [
            {"a": "1", "b": "2"},
            {"c": "3", "d": "4"},
        ]})
        struct6 = trait_structure({"c": "3", "b": [
            {"a": "1", "c": "3"},
            {"c": "3", "e": "5"},
        ]})
        struct7 = trait_structure({"a": "1", "c": "3", "b": [
            {"a": "1", "b": "2", "c": "3"},
            {"c": "3", "d": "4", "e": "5"},
        ]})

        self.assertEqual(struct7, struct5.union(struct6))

    def test_priority_union(self):
        malformed = MalformedStructure()
        self.assertEqual(malformed, malformed.priority_union(malformed))

        value1 = TraitValue("1")
        value2 = TraitValue("2")

        self.assertEqual(malformed, malformed.priority_union(value1))
        self.assertEqual(value1, value1.priority_union(malformed))
        self.assertEqual(value1, value1.priority_union(value1))
        self.assertEqual(value1, value1.priority_union(value2))

        list1 = trait_structure(["1", "2", "3"])
        list2 = trait_structure(["1", "2", "4"])

        self.assertEqual(list1, list1.priority_union(list1))
        self.assertEqual(list1, list1.priority_union(list2))

        struct1 = trait_structure({"a": "1", "b": "2"})
        struct2 = trait_structure({"a": "1", "b": "3"})

        self.assertEqual(malformed, malformed.priority_union(struct1))
        self.assertEqual(struct1, struct1.priority_union(malformed))
        self.assertEqual(struct1, struct1.priority_union(struct1))
        self.assertEqual(struct1, struct1.priority_union(struct2))

        struct3 = trait_structure({"a": "1", "c": "3"})
        struct4 = trait_structure({"a": "1", "b": "2", "c": "3"})

        self.assertEqual(struct4, struct1.priority_union(struct3))

        struct5 = trait_structure({"a": "1", "b": [
            {"a": "1", "b": "2"},
            {"c": "3", "d": "4"},
        ]})
        struct6 = trait_structure({"c": "3", "b": [
            {"a": "2", "c": "3"},
            {"c": "3", "e": "5", "d": "3"},
        ]})
        struct7 = trait_structure({"a": "1", "c": "3", "b": [
            {"a": "1", "b": "2", "c": "3"},
            {"c": "3", "d": "4", "e": "5"},
        ]})

        self.assertEqual(struct7, struct5.priority_union(struct6))
