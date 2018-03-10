from ugen import MalformedStructure, TraitStructure
import random


class MusicalStructure(TraitStructure):
    def children_defined(self):
        return "_children" in self.traits

    @property
    def children(self):
        return self.traits["_children"]

    @children.setter
    def children(self, value):
        self.traits["_children"] = value

    def successor_defined(self):
        return "_successor" in self.traits

    @property
    def successor(self):
        return self.traits["_successor"]

    @successor.setter
    def successor(self, value):
        self.traits["_successor"] = value


class Rule(object):
    def __init__(self, head, tail, weight):
        self.head = head
        self.tail = tail
        self.weight = weight


class Generator(object):
    def __init__(self, rules):
        self.rules = rules

    def generate(self, struct):
        if not struct.children_defined():
            rule = self.pick_rule(struct)
            children = []
            succ = struct.successor
            for traits in rule.tail[::-1]:
                child = traits.priority_union(struct)
                child.successor = succ
                children.insert(0, child)
                succ = child
            struct.children = children

        for child in struct.children[::-1]:
            self.generate(child)
    
    def pick_rule(self, traits):
        return random.choice(r for r in self.rules
                             if r.head.unify(traits) != MalformedStructure())
