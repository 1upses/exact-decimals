class decimal:
    
    def __init__(self, value = 0, decimal = "0", precision: int = 0):
        """precision can be manually defined if needed, but will automatically be if not"""
        self.__cut = not bool(precision) #définis la variable qui tronquera le résultat si nécéssaire
        
        if (len(str(decimal)) > precision) and not precision and (type(value) != float): #définis la précision si non précisée
            precision = len(str(decimal))

        if type(value) == float: #gestion des nombres flottants
            self.value = int(value)
            strip = 2 if value >= 0 else 3 #on retire le moins si c'est négatif
            self.decimal = str(value - int(value))[strip:]
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
        if self.__cut: #enlève les 0 inutiles
            while (self.precision >= 2) and (not int(self.decimal[-1])):
                self.decimal = pop_last_str(self.decimal)[1]
                self.precision -= 1
        
        return f"{self.value}.{self.decimal}"

    def __add__(self, other):
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
            #on multiplie d'abord les entiers, puis les parties décimales
            #entre elles comme si c'était des entier, et on rajoute les
            #caractères en trop à la partie entière
            value = self.value * other
            decim = str(int(self.decimal) * other)

            to_add = ""
            while len(decim) != len(self.decimal):
                temp = pop_first_str(decim)
                to_add += temp[0]
                decim = temp[1]
            value += int(to_add)

            return decimal(value, decim, self.precision)

        if type(other) == decimal:
            #on supprime la virgule, on multiplie les 2 nombres
            #ensemble comme pour des entiers, puis on replace la
            #virgule selon le nombre de chiffres décimales des deux nombres
            premier = int(str(self.value) + self.decimal)
            dernier = int(str(other.value) + other.decimal)
            space = len(self.decimal) + len(other.decimal)
            resultat = str(premier * dernier)
            to_add = ""
            for _ in range(space):
                temp = pop_last_str(resultat)
                to_add = temp[0] + to_add
                resultat = temp[1]
            return decimal(int(resultat), to_add)

        if type(other) == float:
            return self * decimal(other)

        else:
            raise TypeError(f"wrong type, only variables of type decimal, int, and floats are supported, but type {type(other)} was input")

def pop_first_str(string: str):
    temp = ""
    for i in range(1, len(string)):
        temp += string[i]
    return (string[0], temp)

def pop_last_str(string: str):
    temp = pop_first_str(string[::-1])
    return temp[0], temp[1][::-1]
 
print(decimal(5,"0200"))