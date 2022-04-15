

import tkinter as tk

import code.model.constants as CST

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

    self.checkbutton_rebalance_state = tk.IntVar()
    self.checkbutton_rebalance = tk.Checkbutton(self.frame_Checkbox,
                                                text="Rebalance",
                                                variable=self.checkbutton_rebalance_state,
                                                command=self.update_rebalance_status)
    self.checkbutton_rebalance.pack()

    # Horizontal with "Years" and "Loan"
    self.frame_group1 = tk.Frame(super_frame, padx=5, pady=5)
    self.frame_group1.pack()

    # Spinbox Years
    self.frame_years = tk.Frame(self.frame_group1, padx=5, pady=5)
    self.frame_years.pack(side=tk.LEFT)
    self.label_years = tk.Label(self.frame_years, text='Years')
    self.label_years.pack()
    self.spin_years = tk.Spinbox(self.frame_years, from_=0, to=100, width=5, command=self.update_years_investigating)
    self.spin_years.delete(0)
    self.spin_years.insert(0, CST.DEFULT_YEARS_INVESTIGATING)
    self.spin_years.pack()

    # Spinbox Loan
    self.frame_loan = tk.Frame(self.frame_group1, padx=5, pady=5)
    self.frame_loan.pack(side=tk.LEFT)
    self.label_loan = tk.Label(self.frame_loan, text='Loan')
    self.label_loan.pack()

    self.spin_loan = tk.Spinbox(self.frame_loan, from_=0, to=100, width=5, command=self.update_loan)
    self.spin_loan.pack()


    # Dropdown menu
    self.frame_dropdown = tk.Frame(super_frame, padx=5, pady=5)
    self.frame_dropdown.pack()

    self.label_dropdown = tk.Label(self.frame_dropdown, text='Strategy')
    self.label_dropdown.pack()

    self.options = ["Do Nothing",
                    "Harvest/Refill"]

    # datatype of menu text
    self.clicked = tk.StringVar()

    # initial menu text
    self.clicked.set(self.options[0])

    self.drop_menu = tk.OptionMenu(self.frame_dropdown, self.clicked, *self.options)
    self.drop_menu.pack()




