from code.model.market_class import Market

def market_dict_to_market_class(market_name ,market_dict):

    market_class = Market(market_name, market_dict['index_value'], market_dict['time'])
    market_class.set_daily_change(market_dict['daily_change'])

    return market_class


def market_class_to_dict_market(market_class):

    key = market_class.get_name()
    market_dict = {}

    market_dict['index_value'] = market_class.get_values()
    market_dict['time'] = market_class.get_time_span()
    market_dict['daily_change'] = market_class.get_daily_change()

    return [key, market_dict]


def dict_of_market_dicts_to_dict_of_market_classes(dict_of_dicts):
    new_dict = {}

    for key in dict_of_dicts.keys():
        new_dict[key] = market_dict_to_market_class(key, dict_of_dicts[key])

    return new_dict

def dict_of_market_classes_to_dict_of_market_dicts(dict_of_classes):
    new_dict = {}

    for key in dict_of_classes.keys():
        new_dict[key] = market_class_to_dict_market(dict_of_classes[key])[1]

    return new_dict
