def get_names(values):
    """
    :param values:
    :return:
    """
    unique_names = set()  # avoid duplicates
    data_results = values['data']['results']
    for char in data_results:
        print(char['name'])
        unique_names.add(char['name'])
    return unique_names

def get_comics_character(characters, values):
    """

    :param characters:
    :param values:
    :return:
    """
