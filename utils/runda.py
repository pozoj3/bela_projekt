import random
from karta import Karta

class Runda:
    def __init__(self):
        self.spil = []

        self.ruke = {
            1 : [], #tim mi
            2 : [], #tim vi
            3 : [], #tim mi
            4 : [] # tim vi
        }

        self.taloni = {
            1 : [], #tim mi
            2 : [], #tim vi
            3 : [], #tim mi
            4 : [] # tim vi
        }



    def promjesaj_karte(self):
        boje = ["H", "K", "P", "T"]
        brojevi = ["7", "8", "9", "c", "d", "b", "k", "a"]

        self.spil = []

        for b in boje:
            for br in brojevi:
                oznaka = b + br
                nova_karta = Karta(oznaka)
                self.spil.append(nova_karta)
        
        random.shuffle(self.spil)

        self.ruke[1] = self.spil[0:3] + self.spil[12:15]
        self.ruke[2] = self.spil[3:6] + self.spil[15:18]
        self.ruke[3] = self.spil[6:9] + self.spil[18:21]
        self.ruke[4] = self.spil[9:12] + self.spil[21:24]

        self.taloni[1] = self.spil[24:26]
        self.taloni[2] = self.spil[26:28]
        self.taloni[3] = self.spil[28:30]
        self.taloni[4] = self.spil[30:32]

    
    def otkrij_karte(self, br_igraca):
        self.ruke[br_igraca] = self.ruke[br_igraca] + self.taloni[br_igraca]
        self.taloni[br_igraca] = []

    
    def sortiraj_ruku(self, br_igraca):
        ruka = self.ruke[br_igraca]
        ruka.sort(key = lambda k: (k.boja, k.broj_za_zvanje))

    #def sortiraj_sve_ruke(self):
        #for ruka in self.ruka:
           # ruka.sortiraj_ruku()

    def zvanja_karte(self, br_igraca):
        #prvo gledamo za 4 iste
        ruka = self.ruke[br_igraca]
        for karta in ruka:
            pass
            
        

#jos treba dodati logiku za zvanja i za igranje


if __name__ == "__main__":
    runda = Runda()
    
    print("Stvaram i miješam špil...")
    runda.promjesaj_karte()
    
    print(f"Broj karata u špilu: {len(runda.spil)}") # Mora biti 32
    
    print("\nPrvih 5 karata nakon miješanja:")
    # Ovo ispisuje prvih 5 karata iz liste (slicing)
    print(runda.spil[:5])