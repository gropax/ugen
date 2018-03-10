from ugen import Rule, trait_structure


Rule(
    trait_structure({
        "duration": 4,
        "origin": 0,
        "_successor": {
            "origin": 0,
        },
    }), [
        trait_structure({
            "duration": 4,
            "_successor": 0,
        }),
    ])
