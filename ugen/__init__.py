def singleton(class_):
    instances = {}

    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]

    return getinstance


@singleton
class MalformedStructure(object):
    def unify(self, other):
        return MalformedStructure()


class TraitStructure(object):
    def __init__(self, traits):
        self.traits = traits

    def __eq__(self, other):
        return isinstance(other, TraitStructure) and self.traits == other.traits

    def unify(self, other):
        if not isinstance(other, TraitStructure):
            return MalformedStructure()

        s = {}
        labels = list(self.traits.keys()) + list(other.traits.keys())

        for label in labels:
            if label in self.traits and label in other.traits:
                unified = self.traits[label].unify(other.traits[label])
                if unified == MalformedStructure():
                    return MalformedStructure()
                else:
                    s[label] = unified
            elif label in self.traits:
                s[label] = self.traits[label]
            else:
                s[label] = other.traits[label]

        return TraitStructure(s)


class TraitValue(object):
    def __init__(self, value):
        self.value = value

    def __eq__(self, other):
        return isinstance(other, TraitValue) and self.value == other.value

    def unify(self, other):
        if isinstance(other, TraitValue) and self.value == other.value:
            return TraitValue(self.value)
        else:
            return MalformedStructure()


class TraitStructureList(object):
    def __init__(self, structs):
        self.structs = structs

    def __eq__(self, other):
        return isinstance(other, TraitStructureList) and self.structs == other.structs

    def unify(self, other):
        if not isinstance(other, TraitStructureList):
            return MalformedStructure()

        if len(self.structs) != len(other.structs):
            return MalformedStructure()

        s = []
        for s1, s2 in zip(self.structs, other.structs):
            unified = s1.unify(s2)
            if unified == MalformedStructure():
                return MalformedStructure()
            else:
                s.append(unified)

        return TraitStructureList(s)


def trait_structure(obj):
    if isinstance(obj, dict):
        return TraitStructure({t: trait_structure(obj[t]) for t in obj})
    elif isinstance(obj, list):
        return TraitStructureList([trait_structure(x) for x in obj])
    else:
        return TraitValue(obj)
