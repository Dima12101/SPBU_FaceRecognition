from collections import Counter

import numpy as np

from src.core.base import dist
from src.core import features
from src.configs import ALL_DATABASES, METHODS_PARAM, ALL_METHODS, DATABASE_CONF

def recognition(img, method, param, database_data, g_range, i_range):
    print(f"START 'Recognition'. Method '{method}'[{param}]")
    img_features, img_vec = features.HANDLER[method](img, param)

    rec_img = None
    rec_img_features = None
    d_min = float("inf")
    for g_i in range(*g_range):
        for im_i in range(*i_range):
            tmp_img = database_data[g_i][im_i]
            tmp_img_features, tmp_img_vec = features.HANDLER[method](tmp_img, param)
            if (d := dist(img_vec, tmp_img_vec)) < d_min:
                d_min = d ; rec_img = (g_i, im_i) ; rec_img_features = tmp_img_features
    print('END')
    return img_features, rec_img, rec_img_features


def _search(templates, test):
    '''Поиск эталона для теста по КМР'''
    test_vec = test[0]
    d_min = float("inf")
    template_min = None
    for template in templates:
        template_vec = template[0]
        if (d := dist(template_vec, test_vec)) < d_min:
            d_min = d ; template_min = template
    return template_min

def classifiers(templates, tests):
    '''Расчёт качества классификации'''
    number_true = 0
    for test in tests:
        template_search = _search(templates, test)
        class_test = test[1]
        class_search  = template_search[1]
        if class_test == class_search: number_true += 1
    score = (number_true / len(tests)) * 100 # %
    return score

def parallel_classifiers(templates, tests, number_tests):
    number_true = 0
    for i in range(number_tests):
        class_test = tests[ALL_METHODS[0]][i][1]
        class_search = Counter()
        for method in ALL_METHODS:
            test = tests[method][i]
            template_search = _search(templates[method], test)
            class_search[template_search[1]] += 1
        class_voting = class_search.most_common(1)[0][0]
        if class_test == class_voting: number_true += 1
    score = (number_true / number_tests) * 100 # %
    return score

def database_to_vec(data, database, method, param):
    number_gr = DATABASE_CONF[database]['number_group']
    number_img = DATABASE_CONF[database]['number_img']
    data_vec = []
    for gr in range(number_gr):
        group_vec = []
        for im in range(number_img):
            group_vec.append(features.HANDLER[method](data[gr][im], param)[1])
        data_vec.append(group_vec)
    return data_vec

def research_1_N(database_data, database, method):
    print(f'{database=} ; {method=}')
    # Settings
    range_param = METHODS_PARAM[method]['range']
    number_classes = DATABASE_CONF[database]['number_group']
    number_img = DATABASE_CONF[database]['number_img']

    param_CV_scores = []
    param_mean_scores = []
    for param in range(*range_param):
        data_vec = database_to_vec(database_data, database, method, param)
        # CV
        param_scores = []
        for i in range(number_img):
            # Create template/test
            templates = []
            tests = []
            for cl in range(number_classes):
                templates.append((data_vec[cl][i], cl))
                for im in range(number_img):
                    if im != i: tests.append((data_vec[cl][im], cl))
            # Compute score
            score = classifiers(templates, tests)
            param_scores.append(score)
        score_mean = sum(param_scores) / len(param_scores)
        param_mean_scores.append(score_mean)
        param_CV_scores.append(param_scores)
        print(f'{param=} ; {score_mean=}')
    return param_mean_scores, param_CV_scores

def research_L_NL(database_data, database, method, param):
    print(f'{database=} ; {method=}; {param=}')
    # Settings
    number_classes = DATABASE_CONF[database]['number_group']
    number_img = DATABASE_CONF[database]['number_img']

    data_vec = database_to_vec(database_data, database, method, param)

    scores = []
    for L in range(1, number_img):
        # Create template/test
        templates = [(data_vec[cl][im], cl) for cl in range(number_classes) for im in range(L)]
        tests = [(data_vec[cl][im], cl) for cl in range(number_classes) for im in range(L,number_img)]            
            
        # Compute score
        score = classifiers(templates, tests)
        scores.append(score)
        print(f'{L=} ; {score=}')
    return scores


def research_parallel_system(database_data, database, params):
    print(f'{database=} ; {params=}')
    # Settings
    number_classes = DATABASE_CONF[database]['number_group']
    number_img = DATABASE_CONF[database]['number_img']

    data_vec = {}
    for method in ALL_METHODS:
        data_vec[method] = database_to_vec(database_data, database, method, params[method])

    scores = []
    for L in range(1, number_img):
        # Create template/test
        templates = {} ; tests = {}
        for method in ALL_METHODS:
            templates[method] = [(data_vec[method][cl][im], cl) for cl in range(number_classes) for im in range(L)]
            tests[method] = [(data_vec[method][cl][im], cl) for cl in range(number_classes) for im in range(L,number_img)]            
            
        # Compute score
        score = parallel_classifiers(templates, tests, number_img-L)
        scores.append(score)
        print(f'{L=} ; {score=}')
    return scores



def research_parallel_system_new(database_data, database, params, L):
    print(f'{database=} ; {params=}; {L=}')
    # Settings
    number_classes = DATABASE_CONF[database]['number_group']
    number_img = DATABASE_CONF[database]['number_img']

    data_vec = {}
    for method in ALL_METHODS:
        data_vec[method] = database_to_vec(database_data, database, method, params[method])

    templates = {}
    for method in ALL_METHODS:
        templates[method] = [(data_vec[method][cl][im], cl) for cl in range(number_classes) for im in range(L)]

    scores = []

    tests = {}
    for method in ALL_METHODS:
        tests[method] = []


    for i_num in range(number_img-L):
        for i_cl in range(number_classes):
            for method in ALL_METHODS:
                tests[method].append((data_vec[method][i_cl][L+i_num], i_cl))
                test_num = len(tests[method])
        
            # Compute score
            score = parallel_classifiers(templates, tests, test_num)
            scores.append(score)
            print(f'num={test_num} {score=}')
    return scores
