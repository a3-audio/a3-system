class InputAdapterOSC:

    # maybe pass port/ip
    def __init__(self, mocDisplay):
        self.mocDisplay = mocDisplay

        # open osc server
        # dispatch osc inputs to mocDisplay callbacks
        # as in InputAdapterUI.
