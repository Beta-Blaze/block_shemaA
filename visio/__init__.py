FILE_DIRECTORY = '\\'.join(__file__.split("\\")[:-1]) + '\\'

SHAPE_TYPES = {
    "START": 2,
    "PROCESS": 4,
    "INPUT": 5,
    "IF": 6,
    "MODIFICATION": 7,
    "DEFINED_PROCESS": 8,
    "ONE_PAGE_CONNECTOR": 9,
    "MULTI_PAGE_CONNECTOR": 10,
    "POINT": 11
}

SHAPE_SIZE = {
    # Height Width
    "START": [0.3937007874015748, 1.181102362204724],
    "PROCESS": [0.7874015748031495, 1.181102362204724],
    "INPUT": [0.7874015748031495, 1.181102362204724],
    "IF": [0.7874015748031495, 1.181102362204724],
    "MODIFICATION": [0.7874015748031491, 1.181102362204724],
    "DEFINED_PROCESS": [0.7874015748031495, 1.181102362204724],
    "ONE_PAGE_CONNECTOR": [0.3937007874015748, 0.3937007874015748],
    "MULTI_PAGE_CONNECTOR": [0.4724409448818898, 0.3937007874015749],
    "POINT": [0.265625, 0.9999999349767528]
}