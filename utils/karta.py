# boje: "H" - herc, "K" - karo, "P" - pik, "T" -tref
# brojevi: "7", "8",. "9", "c", "d", "b", "k", "a"
# jelAdut
# za zvanja 1,2,3,4,5,6,7,8
# bodovi: 0, 0, 0/14, 10, 2/20, 3, 4, 11  


class Karta:
    def __init__(self, oznaka): #oznaka je npr. "K7" ili "Pb"
        self.oznaka = oznaka
        self.boja = oznaka[0]
        self.broj = oznaka[1]

        vrijednosti_za_zvanje = {
            "7": 7,
            "8": 8,
            "9": 9,
            "c": 10,
            "d": 11,
            "b": 12,
            "k": 13,
            "a": 14
        }

        self.broj_za_zvanje = vrijednosti_za_zvanje[self.broj]
        


    def __repr__(self):
        #return f"Karta(boja = '{self.boja}', broj = '{self.broj}')"
        return f"{self.boja}{self.broj}"
    
    def __eq__(self, druga_karta):
        if isinstance(druga_karta, Karta):
            return self.oznaka == druga_karta.oznaka
        return False
        

    def bodovi(self, adut):
        bodovi_za_karte = {
            "7": 0,
            "8": 0,
            "9": 0,
            "c": 10,
            "d":  2,
            "b": 3,
            "k": 4,
            "a": 11
        }

        if adut == self.boja:
            if self.broj == "d":
                return 20
            elif self.broj == "9":
                return 14
        
        return bodovi_za_karte[self.broj]
    
    def jaca_od(self, druga_karta, adut):
        jacina ={
            "7": 1,
            "8": 2,
            "9": 3,
            "c": 7,
            "d":  4,
            "b": 5,
            "k": 6,
            "a": 8
        }
        jacina_adut ={
            "7": 1,
            "8": 2,
            "9": 7,
            "c": 5,
            "d":  8,
            "b": 3,
            "k": 4,
            "a": 6
        }
        if self.boja == adut and druga_karta.boja != adut:
            return True
        elif self.boja != adut and druga_karta.boja == adut:
            return False
        elif self.boja == adut and druga_karta.boja == adut:
            return jacina_adut[self.broj] > jacina_adut[druga_karta.broj]
        else:
            if self.boja == druga_karta.boja:
                return jacina[self.broj] > jacina[druga_karta.broj]
            else:
                return False #tu je pretpostavka da nemres baciti kartu druge boje


    


if __name__ == "__main__":
    # Probamo napraviti kartu Devetku Herc
    k1 = Karta("H9")
    print(f"Oznaka: {k1.oznaka}")
    print(f"Boja: {k1.boja}")
    print(f"Rang: {k1.broj}")
    print(f"Broj za zvanje: {k1.broj_za_zvanje}") # Treba ispisati 9
    
    print("-" * 20)
    
    # Probamo napraviti Desetku Tref (testiramo dvoznamenkasti broj)
    k2 = Karta("Kc")
    print(f"Oznaka: {k2.oznaka}")
    print(f"Boja: {k2.boja}")
    print(f"Rang: {k2.broj}")       # Treba ispisati 10
    print(f"Broj za zvanje: {k2.broj_za_zvanje}") # Treba ispisati 10
    
    print("-" * 20)

    # Probamo Kralja (testiramo slova)
    k3 = Karta("Pk")
    print(f"Broj za zvanje (Kralj): {k3.broj_za_zvanje}") # Treba ispisati 13