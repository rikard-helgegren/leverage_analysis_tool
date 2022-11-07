
import csv
from src.model.market_class import Market


def read_and_manage_raw_data(data_file_path, markets_file_name_list):
    
    country_data_and_sattistics = {}

    for market_file_name in markets_file_name_list:

        time  = []
        value = []

        #read data, exclude first row of describing text
        results = []
        with open(data_file_path+"/"+market_file_name) as csvfile:
            first_row = next(csvfile)
            reader = csv.reader(csvfile,)
            for row in reader: # each row is a list
                time.append(int(row[0]))
                value.append(float(row[2]))

        #Reverse, since data is backwards
        time  = time[::-1]
        value = value[::-1]

        #save data in dict of market objects
        [name, country] = market_file_name.split()

        market = Market(name, value, time)
        market.set_country(country[:-4]) # add country but remove ".csv"
        country_data_and_sattistics[name] = market


    return country_data_and_sattistics
