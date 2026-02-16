import random
from karta import Karta
from collections import Counter

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

        self.bacene_karte = {
            1 : [], #tim mi
            2 : [], #tim vi
            3 : [], #tim mi
            4 : [] # tim vi
        }

        self.popis_zvanja = {
            1 : {},
            2 : {},
            3 : {},
            4 : {}  
        }
        #zvanja su to je rjecink koji zgleda ovak:
        # H20 : [H9, Hc, Hd], 4k : [H4, Kk, Pk, Tk]

        self.bodovi_zvanja = {
            1 : 0,
            2 : 0,
            3 : 0,
            4 : 0
        }

        self.karte_na_stolu = []
        self.adut = ""

        self.bodovi_mi = 0
        self.bodovi_vi = 0

        self.prvi_koji_igra = 1








    #funkcija za mesanje karti
    #stavlja karte u ruke i talone
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

    #ovo karte iz talona stavlja u ruke
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

        koja_zvanja = {}

        samo_brojevi = [k.broj for k in ruka]
        brojac = Counter(samo_brojevi)

        bodovi = 0

        for identitet, kolicina in brojac.items():
            if kolicina == 4:
                if identitet == "d":
                    bodovi += 200
                elif identitet == "9":
                    bodovi += 150
                elif identitet in ["a", "k", "b", "c"]:
                    bodovi += 100
        

        #sad idemo za normalna zvanja
        i = 0
        while i < len(ruka) - 2:
            trenutna = ruka[i]
            duljina_niza = 1
            j = i
            
            while j < len(ruka) - 1:
                karta_A = ruka[j]
                karta_B = ruka[j+1]
                
                if (karta_A.boja == karta_B.boja) and (karta_A.broj_za_zvanje + 1 == karta_B.broj_za_zvanje):
                    duljina_niza += 1
                    j += 1
                else:
                    break 
            
            if duljina_niza >= 3:
                if duljina_niza == 3:
                    bodovi += 20
                elif duljina_niza == 4:
                    bodovi += 50
                elif duljina_niza >= 5 and duljina_niza < 8:
                    bodovi += 100
                elif duljina_niza == 8:
                    bodovi = - 100
                i += duljina_niza
            else:
                i += 1
        
        self.bodovi_zvanja[br_igraca] = bodovi




    def jel_ima_belu(self, br_igraca):
        
        baba = Karta(self.adut + "b")
        kralj = Karta(self.adut + "k")
        if baba in self.ruke[br_igraca] and kralj in self.ruke[br_igraca]:
            return True
        return False
        
    

    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    #!!! ovo tu treba popraviti jer sad je redosled bacanja krivi !!!
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    
    #gleda jel smo postivali boju (prvu bacenu ili aduta)
    def postivanje_boje(self, pokusana_karta):
        if(len(self.karte_na_stolu) == 0):
            return True
        else:
            br_igraca = len(self.karte_na_stolu) + 1
            #prva_karta = Karta(self.karte_na_stolu[0])
            prva_karta = self.karte_na_stolu[0]
            
            if prva_karta.boja == pokusana_karta.boja:
                return True
            
            temp_bool1 = True
            temp_bool2 = True
            for k in self.ruke[br_igraca]:
                if k.boja == prva_karta.boja:
                    temp_bool1 = False
            
            if temp_bool1 == False:
                return False #nismo postivali samo
            
            if pokusana_karta.boja == self.adut:
                return True

            if temp_bool1 == True:
                for k in self.ruke[br_igraca]:
                    if k.boja == self.adut:
                        temp_bool2 = False
            
            return temp_bool2
        

    def trenutna_najjaca(self):
        if len(self.karte_na_stolu) == 0:
            return Karta("Nn")
        najjaca = self.karte_na_stolu[0]

        for k in self.karte_na_stolu:
            if k.jaca_od(najjaca, self.adut):
                najjaca = k

        return najjaca


    def postivanje_ibera(self, pokusana_karta):
        if(len(self.karte_na_stolu) == 0):
            return True
        else:
            najjaca = self.trenutna_najjaca()
            if pokusana_karta.jaca_od(najjaca, self.adut):
                return True
            return False



    #vraca jel se karta more baciti ili ne
    def baci_kartu(self, pokusana_karta):
        br_igraca = len(self.karte_na_stolu) + 1

        if self.postivanje_boje(pokusana_karta) and self.postivanje_ibera(pokusana_karta) and pokusana_karta in self.ruke[br_igraca]:
            self.karte_na_stolu.append(pokusana_karta)
            self.bacene_karte[br_igraca].append(pokusana_karta)
            self.ruke[br_igraca].remove(pokusana_karta)
            return True
        
        return False
    


    def pokupi_stih(self):
        najjaca = self.trenutna_najjaca()
        
        for i in range(1,5):
            if najjaca in self.bacene_karte[i]:
                if i % 2 == 1:
                    self.bodovi_mi += sum(karta.bodovi(self.adut) for karta in self.karte_na_stolu)
                else:
                    self.bodovi_vi += sum(karta.bodovi(self.adut) for karta in self.karte_na_stolu)
        
        self.karte_na_stolu = []


    def zovi_aduta(self, adut):
        self.adut = adut



    
    def tijek_runde(self, prvi_na_redu):
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