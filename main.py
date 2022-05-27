class decimal:
    
    def __init__(self, value = 0, decimal = "0", precision: int = 0):
        """precision can be manually defined if needed, but will automatically be if not"""
        if (len(str(decimal)) > precision) and not precision and (type(value) != float): #définis la précision si non précisée
            precision = len(str(decimal))

        if type(value) == float: #gestion des nombres flottants
            self.value = int(value)
            self.decimal = str(value - int(value))[2:]
            if (len(self.decimal) > precision) and not precision:
                precision = len(self.decimal)
            self.precision = precision
        else: #gestion normale de l'objet
            if precision:
                self.precision = precision
            else:
                self.precision = len(decimal)
            self.value = value
            self.decimal = str(decimal)

        if len(self.decimal) < self.precision: #rajoute des 0 si précision plus grande
            while len(self.decimal) < self.precision:
                self.decimal += "0"
        elif len(self.decimal) > self.precision: #tronque si précision plus petite
            while len(self.decimal) > self.precision:
                self.decimal = self.decimal[:-1]
    
    def __str__(self):
        return f"{self.value}.{self.decimal}"

    def __add__(self, other):
        """adding negative numbers may lead to some strange behaviors (bugs I'm too lazy to fix),
        I advise you to use the substracting operator instead"""
        if type(other) == decimal:
            
            while len(self.decimal) != len(other.decimal): #set la même précision pour chaque nombre
                if self.decimal > other.decimal:
                    other.decimal += "0"
                    other.precision += 1
                    precision = other.precision
                elif self.decimal < other.decimal:
                    self.decimal += "0"
                    self.precision += 1
                    precision = self.precision

            value = self.value + other.value #set les valeurs
            if other.value < 0:
                decim = str(int(self.decimal) - int(other.decimal))
            else:
                decim = str(int(self.decimal) + int(other.decimal))
            
            if "-" in decim: #pour gérer les nombres négatifs
                decim = str(10**precision + int(decim))
                value -= 1

            if len(decim) > self.precision: #si la décimale dépasse 1
                decim = decim[1:]
                value += 1
            elif len(decim) < self.precision: #remet à la bonne précision après le calcul
                while len(decim) < self.precision:
                    decim = "0" + decim
            return decimal(value, decim, self.precision)

        elif type(other) == int:
            return decimal(self.value + other, self.decimal, self.precision)

        elif type(other) == float:
            return self + decimal(other)

        else:
            raise TypeError(f"wrong type, only variables of type decimal, int, and floats are supported, but type {type(other)} was input")

    def __sub__(self, other):
        if type(other) == decimal:
            return self + decimal(-other.value, other.decimal, other.precision)
        elif (type(other) == int) or (type(other) == float):
            return self + decimal(-other)
        else:
            raise TypeError(f"wrong type, only variables of type decimal, int, and floats are supported, but type {type(other)} was input")

    def __mul__(self, other):
        if type(other) == int:
            
            value = self.value * other
            decim = str(int(self.decimal) * other)

            to_add = ""
            while len(decim) != len(self.decimal):
                temp = pop_first_str(decim)
                to_add += temp[0]
                decim = temp[1]
            value += int(to_add)

            return decimal(value, decim, self.precision)

def pop_first_str(string: str):
    temp = ""
    for i in range(1, len(string)):
        temp += string[i]
    return (string[0], temp)

print(decimal(4,25) * -5)