import unittest
from ugen import TraitStructure, TraitStructureList, TraitValue, MalformedStructure, trait_structure


class TestTraitStructures(unittest.TestCase):
    def test_unification(self):
        malformed = MalformedStructure()
        self.assertEqual(malformed, malformed.unify(malformed))

        value1 = TraitValue("1")
        value2 = TraitValue("2")

        self.assertEqual(malformed, malformed.unify(value1))
        self.assertEqual(malformed, value1.unify(malformed))
        self.assertEqual(value1, value1.unify(value1))
        self.assertEqual(malformed, value1.unify(value2))

        list1 = trait_structure(["1", "2", "3"])
        list2 = trait_structure(["1", "2", "4"])

        self.assertEqual(malformed, malformed.unify(list1))
        self.assertEqual(malformed, list1.unify(malformed))
        self.assertEqual(list1, list1.unify(list1))
        self.assertEqual(malformed, list1.unify(list2))

        struct1 = trait_structure({"a": "1", "b": "2"})
        struct2 = trait_structure({"a": "1", "b": "3"})

        self.assertEqual(malformed, malformed.unify(struct1))
        self.assertEqual(malformed, struct1.unify(malformed))
        self.assertEqual(struct1, struct1.unify(struct1))
        self.assertEqual(malformed, struct1.unify(struct2))

        struct3 = trait_structure({"a": "1", "c": "3"})
        struct4 = trait_structure({"a": "1", "b": "2", "c": "3"})

        self.assertEqual(struct4, struct1.unify(struct3))

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

        self.assertEqual(struct7, struct5.unify(struct6))
