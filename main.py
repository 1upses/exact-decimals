class decimal:
    
    def __init__(self, value: int = 0, decimal = "00", precision: int = 2):
        self.precision = precision
        self.value = value
        self.decimal = str(decimal)

        if len(self.decimal) < self.precision:
            while len(self.decimal) < self.precision:
                self.decimal += "0"
        elif len(self.decimal) > self.precision:
            while len(self.decimal) > self.precision:
                self.decimal = self.decimal[:-1]
    
    def __str__(self):
        return str(self.value) + "." + self.decimal

    def __add__(self, other):
        if type(other) == decimal:
            value = self.value + other.value
            decim = str(int(self.decimal) + int(other.decimal))
            if len(decim) > self.precision:
                decim = decim[1:]
                value += 1
            elif len(decim) < self.precision:
                while len(decim) < self.precision:
                    decim = "0" + decim
            return decimal(value, decim, self.precision)
        elif type(other) == int:
            return decimal(self.value + other, self.decimal, self.precision)
        elif type(other) == float:
            return self + float_to_decimal(other)
    
def float_to_decimal(number: float, precision: int = 2):
    return decimal(int(number), str(number - int(number))[2:], precision)
