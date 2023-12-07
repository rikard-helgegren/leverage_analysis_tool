#!/usr/bin/env python3
#
# Copyright (C) 2023 Rikard Helgegren <rikard.helgegren@gmail.com>
#
# This software is only allowed for private use. As a private user you are allowed to copy,
# modify, use, and compile the software. You are NOT however allowed to publish, sell, or
# distribute this software, either in source code form or as a compiled binary, for any purpose,
# commercial or non-commercial, by any means.

from kivy.logger import logging

class Buy_sell_singelton(object):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Buy_sell_singelton, cls).__new__(cls)
        else:
            return cls.instance
        
        cls.log = {}
        """ Logg all buys and sells in this dict
        """

        cls.current_date = ''
        """ Date that might be added to logg if an event happened
        """

        cls.current_events = []
        """ Populated if buy or sell of a certificate is made
        """

        return cls.instance
    
    def create_log_event_from_parts(cls):
        logging.debug("Buy_sell_singelton: create_log_from_parts")

        if cls.current_date != '' and cls.current_events != []:
            cls.log[cls.current_date] = cls.current_events
            logging.debug("Buy_sell_singelton: event added to log")
            cls.clear_sub_parts()

    def clear_sub_parts(cls):
        logging.debug("Buy_sell_singelton: clear_sub_parts")
        cls.current_date = ''
        cls.current_events = []
    
    def get_log(cls):
        logging.debug("Buy_sell_singelton: get_log")
        return cls.log
        
    def clear_log(cls):
        logging.debug("Buy_sell_singelton: clear_log")
        cls.log = {}


    def get_current_date(cls):
        logging.debug("Buy_sell_singelton: get_current_date")
        return cls.current_date
    def set_current_date(cls, current_date):
        logging.debug("Buy_sell_singelton: set_current_date")
        cls.current_date = current_date
    def clear_current_date(cls):
        logging.debug("Buy_sell_singelton: clear_current_date")
        cls.current_date = ''

    def get_current_events(cls):
        logging.debug("Buy_sell_singelton: get_current_events")
        return cls.current_events
    def append_current_events(cls, activity):
        logging.debug("Buy_sell_singelton: append_current_events")
        event = {'Activity': activity}
        cls.current_events.append(event) 
    def clear_current_events(cls):
        logging.debug("Buy_sell_singelton: clear_current_events")
        cls.current_events = [] 

    
