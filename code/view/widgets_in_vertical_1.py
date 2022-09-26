

import tkinter as tk

import code.model.constants as CST
from code.view.menu_of_strategies import Menu_Of_Strategies

def setup_vertical_frame_1(view, super_frame):
    # Slide amount leverage
    view.frame_leverage = tk.Frame(super_frame, padx=5, pady=5)
    view.frame_leverage.pack()

    view.label_leverage = tk.Label(view.frame_leverage, text='Percent Leverage')
    view.label_leverage.pack()

    view.scale = tk.Scale(view.frame_leverage, from_=0, to=100, orient='horizontal', command=view.update_amount_leverage)
    view.scale.set(CST.DEFULT_PROPORTION_LEVERAGE*100)
    view.scale.pack()

    # Checkbox
    view.frame_Checkbox = tk.Frame(super_frame, padx=5, pady=5)
    view.frame_Checkbox.pack()
    view.checkbutton_fee_state = tk.IntVar()
    view.checkbutton_fee = tk.Checkbutton(view.frame_Checkbox,
                                          text="Include Fees",
                                          variable=view.checkbutton_fee_state,
                                          command=view.update_fee_status)
    view.checkbutton_fee.pack()

    # Horizontal with "Years" and "Loan"
    view.frame_group1 = tk.Frame(super_frame, padx=5, pady=5)
    view.frame_group1.pack()

    # Spinbox Years
    view.frame_years = tk.Frame(view.frame_group1, padx=5, pady=5)
    view.frame_years.pack(side=tk.LEFT)
    view.label_years = tk.Label(view.frame_years, text='Years\nInvesting')
    view.label_years.pack()
    view.spin_years = tk.Spinbox(view.frame_years, from_=0, to=100, width=5, command=view.update_years_histogram_interval)
    view.spin_years.delete(0)
    view.spin_years.insert(0, CST.DEFULT_YEARS_HISTOGRAM_INTERVAL)
    view.spin_years.pack()

    # Spinbox Loan
    view.frame_loan = tk.Frame(view.frame_group1, padx=5, pady=5)
    view.frame_loan.pack(side=tk.LEFT)
    view.label_loan = tk.Label(view.frame_loan, text='\nLoan')
    view.label_loan.pack()

    view.spin_loan = tk.Spinbox(view.frame_loan, from_=0, to=100, width=5, command=view.update_loan)
    view.spin_loan.delete(0)
    view.spin_loan.insert(0, CST.DEFULT_LOAN)
    view.spin_loan.pack()


    # Dropdown menu

    view.menu_of_strategies = Menu_Of_Strategies(super_frame, view)

    # Horizontal with "Harvest" and "Refill"
    view.frame_group2 = tk.Frame(super_frame, padx=5, pady=5)
    view.frame_group2.pack()

    # Spinbox harvest point
    view.frame_harvest_point = tk.Frame(view.frame_group2, padx=5, pady=5)
    view.frame_harvest_point.pack(side=tk.LEFT)
    view.label_harvest_point = tk.Label(view.frame_harvest_point, text='Harvest\nPoint %')
    view.label_harvest_point.pack()
    view.spin_harvest_point = tk.Spinbox(view.frame_harvest_point, from_=101, to=2000, width=5, command=view.update_harvest_point)
    view.spin_harvest_point.delete(0)
    view.spin_harvest_point.insert(0, CST.DEFULT_HARVEST_POINT)
    view.spin_harvest_point.pack()

    # Spinbox refill point
    view.frame_refill_point = tk.Frame(view.frame_group2, padx=5, pady=5)
    view.frame_refill_point.pack(side=tk.LEFT)
    view.label_refill_point = tk.Label(view.frame_refill_point, text='Refill\nPoint %')
    view.label_refill_point.pack()
    view.spin_refill_point = tk.Spinbox(view.frame_refill_point, from_=0, to=99, width=5, command=view.update_refill_point)
    view.spin_refill_point.delete(0)
    view.spin_refill_point.insert(0, CST.DEFULT_REFILL_POINT)
    view.spin_refill_point.pack()
