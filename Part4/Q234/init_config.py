images = {
    "dedup": "anakli/cca:parsec_dedup",
    "blackscholes": "anakli/cca:parsec_blackscholes",
    "canneal": "anakli/cca:parsec_canneal",
    "ferret": "anakli/cca:parsec_ferret",
    "freqmine": "anakli/cca:parsec_freqmine",
    "radix": "anakli/cca:splash2x_radix",
    "vips": "anakli/cca:parsec_vips"
}

threads = {
    "dedup": 3,
    "blackscholes": 3,
    "canneal": 3,
    "ferret": 3,
    "freqmine": 3,
    "radix": 2,
    "vips": 3,
}

cores = {
    "dedup": "2,3",
    "blackscholes": "2,3",
    "canneal": "2,3",
    "ferret": "2,3",
    "freqmine": "2,3",
    "radix": "2,3",
    "vips": "2,3"
}

weights = {
    "dedup": 10,
    "blackscholes": 10,
    "canneal": 10,
    "ferret": 10,
    "freqmine": 10,
    "radix": 10,
    "vips": 10
}

MAX_MEMORY = 7.636
