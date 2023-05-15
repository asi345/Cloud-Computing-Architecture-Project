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
    "dedup": 1,
    "blackscholes": 2,
    "canneal": 2,
    "ferret": 4,
    "freqmine": 4,
    "radix": 4,
    "vips": 4,
}

cores = {
    "dedup": "0,1,2,3",
    "blackscholes": "0,1,2,3",
    "canneal": "0,1,2,3",
    "ferret": "0,1,2,3",
    "freqmine": "0,1,2,3",
    "radix": "0,1,2,3",
    "vips": "0,1,2,3"
}

MAX_MEMORY = 7.636
