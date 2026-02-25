import random
from utils.karta import Karta
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
        self.broj_stiha = 0
        self.osvojeni_stihovi_mi = 0
        self.osvojeni_stihovi_vi = 0

        self.bodovi_mi = 0
        self.bodovi_vi = 0

        """self.prvi_koji_igra = prvi_na_redu
        self.drugi_koji_igra = (prvi_na_redu+1) % 4
        self.treci_koji_igra = (prvi_na_redu+2) % 4
        self.cetvrti_koji_igra = (prvi_na_redu+3) % 4"""

        #self.red_igranja = [prvi_na_redu, self.pomoca_za_red(prvi_na_redu+1),self.pomoca_za_red(prvi_na_redu+2), self.pomoca_za_red(prvi_na_redu+3)]
        
        


    #pomocna funkija za red igranja
    def pomoca_za_red(self, broj):
        if broj % 4 == 0:
            return 4
        else:
            return broj % 4



    #funkcija za mesanje karti
    #stavlja karte u ruke i talone
    def promjesaj_karte(self, prvi_na_redu):
        boje = ["H", "K", "P", "T"]
        brojevi = ["7", "8", "9", "c", "d", "b", "k", "a"]

        self.spil = []

        for b in boje:
            for br in brojevi:
                oznaka = b + br
                nova_karta = Karta(oznaka)
                self.spil.append(nova_karta)
        
        random.shuffle(self.spil)

        self.red_igranja = [prvi_na_redu, self.pomoca_za_red(prvi_na_redu+1),self.pomoca_za_red(prvi_na_redu+2), self.pomoca_za_red(prvi_na_redu+3)]
        red = self.red_igranja

        self.ruke[red[0]] = self.spil[0:3] + self.spil[12:15]
        self.ruke[red[1]] = self.spil[3:6] + self.spil[15:18]
        self.ruke[red[2]] = self.spil[6:9] + self.spil[18:21]
        self.ruke[red[3]] = self.spil[9:12] + self.spil[21:24]

        self.taloni[red[0]] = self.spil[24:26]
        self.taloni[red[1]] = self.spil[26:28]
        self.taloni[red[2]] = self.spil[28:30]
        self.taloni[red[3]] = self.spil[30:32]

    #ovo karte iz talona stavlja u ruke
    def otkrij_karte(self, br_igraca):
        self.ruke[br_igraca] = self.ruke[br_igraca] + self.taloni[br_igraca]
        self.taloni[br_igraca] = []

    
    def sortiraj_ruku(self, br_igraca):
        ruka = self.ruke[br_igraca]
        ruka.sort(key = lambda k: (k.boja, k.broj_za_zvanje))



    def ime_zvanja_4(self, tip_karti, rjecnik):
        rjecnik[tip_karti] = ["H"+ tip_karti, "K"+ tip_karti, "P"+ tip_karti, "T"+ tip_karti]

    def ime_zvanja_skala(self, duljina, prva_u_zvanju, rjecnik):
        broj_u_oznaku = {
            7: "7",
            8: "8",
            9: "9",
            10: "c",
            11: "d",
            12: "b",
            13: "k",
            14: "a"
        }

        boja = prva_u_zvanju.boja

        lista_karti_zvanja = []
        pocetni_broj = prva_u_zvanju.broj_za_zvanje

        for i in range(duljina):
            trenutni_broj = pocetni_broj + i
            if trenutni_broj in broj_u_oznaku:
                oznaka_broja = broj_u_oznaku[trenutni_broj]
                cijela_oznaka = boja + oznaka_broja
                lista_karti_zvanja.append(cijela_oznaka)
            
        indeks = 1
        kljuc = f"S{indeks}"
        while kljuc in rjecnik:
            indeks += 1
            kljuc = f"S{indeks}"
        rjecnik[kljuc] = lista_karti_zvanja



    def zvanja_karte(self, br_igraca):
        #prvo gledamo za 4 iste
        ruka = self.ruke[br_igraca]

        koja_zvanja = {}

        samo_brojevi = [k.broj for k in ruka]
        brojac = Counter(samo_brojevi)

        bodovi = 0

        temp_sva = {}

        for identitet, kolicina in brojac.items():
            if kolicina == 4:
                if identitet == "d":
                    bodovi += 200
                    self.ime_zvanja_4(identitet, temp_sva)
                if identitet == "9":
                    bodovi += 150
                    self.ime_zvanja_4(identitet, temp_sva)
                if identitet in ["a", "k", "b", "c"]:
                    bodovi += 100
                    self.ime_zvanja_4(identitet, temp_sva)
        

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
                    self.ime_zvanja_skala(duljina_niza, trenutna, temp_sva)
                elif duljina_niza == 4:
                    bodovi += 50
                    self.ime_zvanja_skala(duljina_niza, trenutna, temp_sva)
                elif duljina_niza >= 5 and duljina_niza < 8:
                    bodovi += 100
                    self.ime_zvanja_skala(duljina_niza, trenutna, temp_sva)
                elif duljina_niza == 8:
                    bodovi = 1001
                    self.ime_zvanja_skala(duljina_niza, trenutna, temp_sva)
                i += duljina_niza
            else:
                i += 1
        
        self.bodovi_zvanja[br_igraca] = bodovi
        self.popis_zvanja[br_igraca] = temp_sva



    def validna_zvanja(self):
        vrijednosti_za_zvanje_skala = {
            "7": 7,
            "8": 8,
            "9": 9,
            "c": 10,
            "d": 11,
            "b": 12,
            "k": 13,
            "a": 14
        }
        vrijednosti_za_zvanje_4 = {
            "7": 7,
            "8": 8,
            "9": 16,
            "c": 15,
            "d": 17,
            "b": 12,
            "k": 13,
            "a": 14
        }
                #tip zvanja (belot (3), cetiri (2) , skala (1), nullzvanje (0)), broj karte, duljina zvanja
                #znaci npr [cetiri, 12, 4] -> to su 4 kralja, jer je kralj "==" 12
                #[skala, 10, 4] -> to je 10, decko, baba, kralj
    
        najjace_od_svih_zvanja = [0,0,0,0]
        for id_igraca, lista_zvanja in self.popis_zvanja.items():
            for ime_zvanja, samo_zvanje in lista_zvanja.items():
                temp1 = 0
                temp2 = 0
                temp3 = len(samo_zvanje)
                temp4 = id_igraca
                if temp3 == 8:
                    temp1 = 3
                elif ime_zvanja in ["7","8","9","c","d","b","k","a"]:
                    temp1 = 2
                    temp2 = vrijednosti_za_zvanje_4[samo_zvanje[0][1]] #ovo je jer je samo_zvanje ["Hb","Kb","Pb","Tb"]
                elif "S" in ime_zvanja:
                    temp1 = 1
                    temp2 = vrijednosti_za_zvanje_skala[samo_zvanje[0][1]]
                
                if(temp1 > najjace_od_svih_zvanja[0]):
                    najjace_od_svih_zvanja = [temp1,temp2,temp3,temp4]
                elif(temp1 == najjace_od_svih_zvanja[0] and temp1 == 2):
                    if(temp2 > najjace_od_svih_zvanja[1]):
                        najjace_od_svih_zvanja = [temp1,temp2,temp3,temp4]
                elif(temp1 == najjace_od_svih_zvanja[0] and temp1 == 1):
                    if(temp3 > najjace_od_svih_zvanja[2]):
                        najjace_od_svih_zvanja = [temp1,temp2,temp3,temp4]
                    elif(temp3 == najjace_od_svih_zvanja[2]):
                        if(temp2 > najjace_od_svih_zvanja[1]):
                            najjace_od_svih_zvanja = [temp1,temp2,temp3,temp4]
                        elif(temp2 == najjace_od_svih_zvanja[1]):
                            if(self.red_igranja.index(temp4) < self.red_igranja.index(najjace_od_svih_zvanja[3])):
                                najjace_od_svih_zvanja = [temp1,temp2,temp3,temp4]
                elif(temp1 == najjace_od_svih_zvanja[0] and temp1 == 3):
                    if(self.red_igranja.index(temp4) < self.red_igranja.index(najjace_od_svih_zvanja[3])):
                                najjace_od_svih_zvanja = [temp1,temp2,temp3,temp4]

        if(najjace_od_svih_zvanja[3] % 2 == 1):
            self.popis_zvanja[2] = {}
            self.popis_zvanja[4] = {}
            self.bodovi_zvanja[2] = 0
            self.bodovi_zvanja[4] = 0
        else:
            self.popis_zvanja[1] = {}
            self.popis_zvanja[3] = {}
            self.bodovi_zvanja[1] = 0
            self.bodovi_zvanja[3] = 0
        
        self.drugi_format_popisa_zvanja()


    def jel_ima_belu(self, br_igraca, pokusna_karta):
        
        baba = Karta(self.adut + "b")
        kralj = Karta(self.adut + "k")
        if pokusna_karta == baba or pokusna_karta == kralj:
            if baba in self.ruke[br_igraca] and kralj in self.ruke[br_igraca]:
                self.bodovi_zvanja[br_igraca] += 20
                return True
        return False
        
        

    
    #gleda jel smo postivali boju (prvu bacenu ili aduta)
    def postivanje_boje(self, pokusana_karta, br_igraca):
        if(len(self.karte_na_stolu) == 0):
            return True
        else:
            #br_igraca = len(self.karte_na_stolu) + 1
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
            return None
        najjaca = self.karte_na_stolu[0]

        for k in self.karte_na_stolu:
            if k.jaca_od(najjaca, self.adut):
                najjaca = k

        return najjaca


    def postivanje_ibera(self, pokusana_karta, br_igraca):
        if(len(self.karte_na_stolu) == 0):
            return True
        else:
            najjaca = self.trenutna_najjaca()

            if pokusana_karta.jaca_od(najjaca, self.adut):
                return True
        
            temp_bool = True
            for k in self.ruke[br_igraca]:
                if k.boja == pokusana_karta.boja:
                    if k.jaca_od(najjaca, self.adut):
                        temp_bool = False
            return temp_bool
        
    def jel_na_redu(self, br_igraca):
        return self.red_igranja[len(self.karte_na_stolu)] == br_igraca



    #vraca jel se karta more baciti ili ne
    def baci_kartu(self, pokusana_karta, br_igraca):

        if self.postivanje_boje(pokusana_karta, br_igraca) and self.postivanje_ibera(pokusana_karta, br_igraca) and pokusana_karta in self.ruke[br_igraca] and self.jel_na_redu(br_igraca):
            bool_bela = self.jel_ima_belu(br_igraca, pokusana_karta)
            self.karte_na_stolu.append(pokusana_karta)
            self.bacene_karte[br_igraca].append(pokusana_karta)
            self.ruke[br_igraca].remove(pokusana_karta)
            return True, bool_bela
        
        return False, False
    


    def pokupi_stih(self):
        self.broj_stiha += 1
        najjaca = self.trenutna_najjaca()
        id_najjace = self.karte_na_stolu.index(najjaca)
        id_igraca = self.red_igranja[id_najjace]

        bodovi_stiha = sum(karta.bodovi(self.adut) for karta in self.karte_na_stolu)
        if self.broj_stiha == 8:
            bodovi_stiha += 10
            #self.broj_stiha = 0
        
        if id_igraca % 2 == 1:
            self.bodovi_mi += bodovi_stiha
            self.osvojeni_stihovi_mi += 1
        else:
            self.bodovi_vi += bodovi_stiha
            self.osvojeni_stihovi_vi += 1

        self.red_igranja = [id_igraca, self.pomoca_za_red(id_igraca+1),self.pomoca_za_red(id_igraca+2), self.pomoca_za_red(id_igraca+3)]  
        self.karte_na_stolu = []

    
    def konacni_bodovi(self):
        ukupna_igra = 162 + sum(self.bodovi_zvanja.values())

        potrebno = ukupna_igra / 2  + 1

        if(self.osvojeni_stihovi_vi == 0):
            self.bodovi_mi = ukupna_igra + 100
        elif(self.osvojeni_stihovi_mi == 0):
            self.bodovi_vi = ukupna_igra + 100
        else:
            if(self.igrac_koji_zove % 2 == 1):
                if(self.bodovi_mi < potrebno):
                    self.bodovi_mi = 0
                    self.bodovi_vi = ukupna_igra
            else:
                if(self.bodovi_vi < potrebno):
                    self.bodovi_mi = ukupna_igra
                    self.bodovi_vi = 0


    def zovi_aduta(self, adut, igrac_koji_zove):
        self.adut = adut
        self.igrac_koji_zove = igrac_koji_zove


    
    def postavi_stanje_iz_baze(self, adut, igrac_koji_zove, red_igranja, broj_stiha, 
                               bodovi_mi, bodovi_vi, bodovi_zvanja_mi, bodovi_zvanja_vi,
                               osvojeni_stihovi_mi, osvojeni_stihovi_vi,
                               zvanja_list):
        
        self.adut = adut if adut else ""
        self.igrac_koji_zove = igrac_koji_zove if igrac_koji_zove else 0
        self.red_igranja = red_igranja
        self.broj_stiha = broj_stiha
        
        self.bodovi_mi = bodovi_mi
        self.bodovi_vi = bodovi_vi
        
        #prvi i drugi su tu mi i vi
        self.bodovi_zvanja[1] = bodovi_zvanja_mi
        self.bodovi_zvanja[2] = bodovi_zvanja_vi
        self.bodovi_zvanja[3] = 0
        self.bodovi_zvanja[4] = 0
        
        self.osvojeni_stihovi_mi = osvojeni_stihovi_mi
        self.osvojeni_stihovi_vi = osvojeni_stihovi_vi
        
        if zvanja_list:
            self.novi_popis_zvanja = zvanja_list
        else:
            self.novi_popis_zvanja = {1: {}, 2: {}, 3: {}, 4: {}}
    


    def provjeri_belot(self):
        for red in self.red_igranja:
            if self.bodovi_zvanja[red] == 1001:
                return True
        return False
    
    def drugi_format_popisa_zvanja(self):
        self.novi_popis_zvanja = {
            1 : {},
            2 : {},
            3 : {},
            4 : {}
        }

        for tren_igrac, igraceva_zvanja in self.popis_zvanja.items():
            temp_pop = {}
            for ime_zvanja, zapis_zvanja in igraceva_zvanja.items():
                if "S" in ime_zvanja:
                    if len(zapis_zvanja) == 3:
                        bod = 20
                    elif len(zapis_zvanja) == 4:
                        bod = 50
                    elif len(zapis_zvanja) == 8:
                        bod = 1001
                    else:
                        bod = 100
                elif ime_zvanja in ["c","b","k","a"]:
                    bod = 100
                elif ime_zvanja == "9":
                    bod = 150
                elif ime_zvanja == "d":
                    bod = 200
                
                zap = ", ".join(zapis_zvanja)
                temp_pop[zap] = bod
  
            self.novi_popis_zvanja[tren_igrac] = temp_pop






