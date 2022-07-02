

import tkinter as tk

import code.model.constants as CST
from code.view.menu_of_strategies import Menu_Of_Strategies

def setup_vertical_frame_1(self, super_frame):
    # Slide amount leverage
    self.frame_leverage = tk.Frame(super_frame, padx=5, pady=5)
    self.frame_leverage.pack()

    self.label_leverage = tk.Label(self.frame_leverage, text='Percent Leverage')
    self.label_leverage.pack()

    self.scale = tk.Scale(self.frame_leverage, from_=0, to=100, orient='horizontal', command=self.update_amount_leverage)
    self.scale.set(CST.DEFULT_PROPORTION_LEVERAGE*100)
    self.scale.pack()

    # Checkbox
    self.frame_Checkbox = tk.Frame(super_frame, padx=5, pady=5)
    self.frame_Checkbox.pack()
    self.checkbutton_fee_state = tk.IntVar()
    self.checkbutton_fee = tk.Checkbutton(self.frame_Checkbox,
                                          text="Include Fees",
                                          variable=self.checkbutton_fee_state,
                                          command=self.update_fee_status)
    self.checkbutton_fee.pack()

    # Horizontal with "Years" and "Loan"
    self.frame_group1 = tk.Frame(super_frame, padx=5, pady=5)
    self.frame_group1.pack()

    # Spinbox Years
    self.frame_years = tk.Frame(self.frame_group1, padx=5, pady=5)
    self.frame_years.pack(side=tk.LEFT)
    self.label_years = tk.Label(self.frame_years, text='Years\nInvesting')
    self.label_years.pack()
    self.spin_years = tk.Spinbox(self.frame_years, from_=0, to=100, width=5, command=self.update_years_investigating)
    self.spin_years.delete(0)
    self.spin_years.insert(0, CST.DEFULT_YEARS_INVESTIGATING)
    self.spin_years.pack()

    # Spinbox Loan
    self.frame_loan = tk.Frame(self.frame_group1, padx=5, pady=5)
    self.frame_loan.pack(side=tk.LEFT)
    self.label_loan = tk.Label(self.frame_loan, text='\nLoan')
    self.label_loan.pack()

    self.spin_loan = tk.Spinbox(self.frame_loan, from_=0, to=100, width=5, command=self.update_loan)
    self.spin_loan.delete(0)
    self.spin_loan.insert(0, CST.DEFULT_LOAN)
    self.spin_loan.pack()


    # Dropdown menu

    self.menu_of_strategies = Menu_Of_Strategies(super_frame, self)

    # Horizontal with "Harvest" and "Refill"
    self.frame_group2 = tk.Frame(super_frame, padx=5, pady=5)
    self.frame_group2.pack()

    # Spinbox harvest point
    self.frame_harvest_point = tk.Frame(self.frame_group2, padx=5, pady=5)
    self.frame_harvest_point.pack(side=tk.LEFT)
    self.label_harvest_point = tk.Label(self.frame_harvest_point, text='Harvest\nPoint %')
    self.label_harvest_point.pack()
    self.spin_harvest_point = tk.Spinbox(self.frame_harvest_point, from_=101, to=2000, width=5, command=self.update_harvest_point)
    self.spin_harvest_point.delete(0)
    self.spin_harvest_point.insert(0, CST.DEFULT_HARVEST_POINT)
    self.spin_harvest_point.pack()

    # Spinbox refill point
    self.frame_refill_point = tk.Frame(self.frame_group2, padx=5, pady=5)
    self.frame_refill_point.pack(side=tk.LEFT)
    self.label_refill_point = tk.Label(self.frame_refill_point, text='Refill\nPoint %')
    self.label_refill_point.pack()
    self.spin_refill_point = tk.Spinbox(self.frame_refill_point, from_=0, to=99, width=5, command=self.update_refill_point)
    self.spin_refill_point.delete(0)
    self.spin_refill_point.insert(0, CST.DEFULT_REFILL_POINT)
    self.spin_refill_point.pack()
