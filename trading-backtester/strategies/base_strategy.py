class Strategy:
    def generate_signal(self, data, index):
        """
        Base method that ALL strategies must implement.

        Parameters:
        - data: list of prices
        - index: current position in the data

        Returns:
        - 1  -> BUY
        - -1 -> SELL
        - 0  -> HOLD
        """
        # This forces child classes to implement their own logic
        raise NotImplementedError