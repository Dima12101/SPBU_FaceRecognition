DATA_DIR = './data'

ALL_METHODS = [
    'scale', 'hist', 'grad',
    'spec_dft', 'spec_dct']

METHODS_PARAM = {
    'scale': {'name': 'l', 'default': '2'},
    'hist': {'name': 'BIN', 'default': '32'},
    'grad': {'name': 'W', 'default': '10'},
    'spec_dft': {'name': 'P', 'default': '20'},
    'spec_dct': {'name': 'P', 'default': '20'}
}

ALL_DATABASES = ['ORL', 'Yale_faces']

DATABASE_CONF = {
    'ORL': {
        'number_group': 40,
        'number_img': 10,
        'img_path': './data/ORL/s{g}/{im}.pgm'
    },
    'Yale_faces': {
        'number_group': 15,
        'number_img': 11,
        'img_path': './data/Yale_faces/subject{g}.*'
    },
}
