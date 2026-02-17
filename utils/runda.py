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

    def ime_zvanja_skala(self, duljina, boja, prva_u_zvanju, rjecnik):
        rjecnik[prva_u_zvanju.broj_za_zvanje] = []
       # for i in range(duljina):
          #  rjecnik[prva_u_zvanju.broj_za_zvanje].append() #ovo dalje treba se oznake karti tu napiseju

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
                    self.ime_zvanja_skala(duljina_niza, trenutna.boja, trenutna, temp_sva)
                elif duljina_niza == 4:
                    bodovi += 50
                    self.ime_zvanja_skala(duljina_niza, trenutna.boja, trenutna, temp_sva)
                elif duljina_niza >= 5 and duljina_niza < 8:
                    bodovi += 100
                    self.ime_zvanja_skala(duljina_niza, trenutna.boja, trenutna, temp_sva)
                elif duljina_niza == 8:
                    bodovi = 1001
                    self.ime_zvanja_skala(duljina_niza, trenutna.boja, trenutna, temp_sva)
                i += duljina_niza
            else:
                i += 1
        
        self.bodovi_zvanja[br_igraca] = bodovi

    def validna_zove(self):
        pass


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
        #br_igraca = self.red_igranja[len(self.karte_na_stolu) - 1] ovo valda ne treba

        if self.postivanje_boje(pokusana_karta, br_igraca) and self.postivanje_ibera(pokusana_karta, br_igraca) and pokusana_karta in self.ruke[br_igraca] and self.jel_na_redu(br_igraca):
            self.karte_na_stolu.append(pokusana_karta)
            self.bacene_karte[br_igraca].append(pokusana_karta)
            self.ruke[br_igraca].remove(pokusana_karta)
            return True
        
        return False
    


    def pokupi_stih(self):
        najjaca = self.trenutna_najjaca()
        id_najjace = self.karte_na_stolu.index(najjaca)
        id_igraca = self.red_igranja[id_najjace]

        bodovi_stiha = sum(karta.bodovi(self.adut) for karta in self.karte_na_stolu)

        if id_igraca % 2 == 1:
            self.bodovi_mi += bodovi_stiha
        else:
            self.bodovi_vi += bodovi_stiha

        self.red_igranja = [id_igraca, self.pomoca_za_red(id_igraca+1),self.pomoca_za_red(id_igraca+2), self.pomoca_za_red(id_igraca+3)]  
        self.karte_na_stolu = []

    
    def konacni_bodovi(self):
        ukupna_igra = 162 + sum(bodovi.value() for bodovi in self.bodovi_zvanja)

        potrebno = ukupna_igra // 2  + 1
        
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



    
    def tijek_runde(self, prvi_na_redu):
        pass



            
            
        

#jos treba dodati logiku za zvanja i za igranje


"""if __name__ == "__main__":
    print("=== POČETAK TESTA PODRAVSKE BELE ===")
    
    # 1. KREIRANJE RUNDE 
    # PROMJENA: Konstruktor je sada prazan ()
    runda = Runda()
    
    # 2. MIJEŠANJE
    # PROMJENA: Sada ovdje šaljemo tko je prvi na redu (npr. igrač 1)
    runda.promjesaj_karte(prvi_na_redu=1)
    print("Karte promiješane i red igranja postavljen.")

    # 3. ZVANJE ADUTA (Simulacija: Igrač 1 zove Pik)
    print("\n--- FAZA: ZVANJE ADUTA ---")
    odabrani_adut = "P"
    runda.zovi_aduta(odabrani_adut, igrac_koji_zove=1)
    print(f"Adut je: {runda.adut}")

    # 4. DIJELJENJE OSTATKA (TALONA)
    print("\n--- FAZA: UZIMANJE TALONA ---")
    
    # Simuliramo da svi uzimaju talone
    # Moramo paziti da su liste inicijalizirane u promjesaj_karte
    for i in range(1, 5):
        # Spajamo ruku i talon
        runda.ruke[i] = runda.ruke[i] + runda.taloni[i]
        runda.taloni[i] = [] # Praznimo talon
        
        # Sortiramo da vidimo ljepše
        runda.sortiraj_ruku(i)
        print(f"Ruka Igrač {i}: {runda.ruke[i]}")

    # 5. IGRANJE JEDNOG ŠTIHA
    print("\n--- FAZA: IGRANJE ŠTIHA (SIMULACIJA) ---")
    
    # Koristimo red_igranja koji je nastao u promjesaj_karte
    for igrac_na_potezu in runda.red_igranja:
        print(f"\nNa redu je Igrač {igrac_na_potezu}...")
        
        uspjesno_bacio = False
        
        # 1. POKUŠAJ PO PRAVILIMA
        # Kopiramo listu [:] da ne zbunimo petlju brisanjem elemenata
        for karta_u_ruci in runda.ruke[igrac_na_potezu][:]:
            # Tvoja nova funkcija baci_kartu sada koristi self.jel_na_redu unutar sebe
            # pa joj ne moramo ništa posebno slati osim karte i ID-a
            if runda.baci_kartu(karta_u_ruci, igrac_na_potezu):
                print(f"-> Igrač {igrac_na_potezu} baca (po pravilima): {karta_u_ruci}")
                uspjesno_bacio = True
                break 
        
        # 2. POKUŠAJ NA SILU (FALLBACK)
        # Ako logika ibera/boje ne dopušta ništa (npr. previše stroga pravila), bacamo prvu
        if not uspjesno_bacio:
            print(f"⚠️ Nema validne karte po trenutnoj logici! Forsiram prvu kartu...")
            
            if len(runda.ruke[igrac_na_potezu]) > 0:
                prva_karta = runda.ruke[igrac_na_potezu][0]
                
                # Ručno ažuriranje stanja (zaobilazimo baci_kartu provjere)
                runda.karte_na_stolu.append(prva_karta)
                runda.bacene_karte[igrac_na_potezu].append(prva_karta)
                runda.ruke[igrac_na_potezu].remove(prva_karta)
                
                print(f"-> Igrač {igrac_na_potezu} baca (prisilno): {prva_karta}")
            else:
                print("GREŠKA: Igrač nema karata u ruci!")

    # 6. KUPLJENJE ŠTIHA
    print(f"\nKarte na stolu: {runda.karte_na_stolu}")
    print("\n--- FAZA: KUPLJENJE ŠTIHA ---")
    
    try:
        runda.pokupi_stih()
        print(f"Bodovi MI: {runda.bodovi_mi}")
        print(f"Bodovi VI: {runda.bodovi_vi}")
        print(f"Novi red igranja za idući štih: {runda.red_igranja}")
    except Exception as e:
        print(f"Greška kod kupljenja štiha: {e}")
        print("(Vjerojatno greška u indeksiranju unutar pokupi_stih funkcije)")
    
    print("\n=== KRAJ TESTA ===")"""



from runda import Runda
from karta import Karta
import random
import time

def ispisi_razdvajac(naslov):
    print(f"\n{'='*20} {naslov} {'='*20}")

if __name__ == "__main__":
    ispisi_razdvajac("POČETAK SIMULACIJE")

    # 1. INICIJALIZACIJA
    runda = Runda()
    prvi_igrac = random.randint(1, 4)
    runda.promjesaj_karte(prvi_na_redu=prvi_igrac)
    
    # 2. RANDOM ADUT
    aduti = ["H", "K", "P", "T"]
    odabrani_adut = random.choice(aduti)
    runda.zovi_aduta(odabrani_adut, igrac_koji_zove=prvi_igrac)
    
    print(f"Prvi igra: Igrač {prvi_igrac}")
    print(f"Odabrani adut: {odabrani_adut}")

    # 3. UZIMANJE TALONA I SORTIRANJE
    for i in range(1, 5):
        runda.ruke[i] += runda.taloni[i]
        runda.taloni[i] = [] 
        runda.sortiraj_ruku(i)

    # 4. IGRA (8 ŠTIHOVA)
    for broj_stiha in range(1, 9):
        ispisi_razdvajac(f"ŠTIH BROJ {broj_stiha}")
        
        red_igranja = runda.red_igranja
        print(f"Redoslijed: {red_igranja}")

        # --- BACANJE KARATA (Svi bacaju) ---
        for igrac_id in red_igranja:
            print(f"\n🔵 Na redu: Igrač {igrac_id}")
            
            bacio_kartu = False
            
            # A) POKUŠAJ PO PRAVILIMA
            for karta in runda.ruke[igrac_id][:]:
                if runda.baci_kartu(karta, igrac_id):
                    print(f"✅ Igrač {igrac_id} baca: {karta}")
                    bacio_kartu = True
                    break 
            
            # B) POKUŠAJ NA SILU
            if not bacio_kartu:
                if len(runda.ruke[igrac_id]) > 0:
                    karta_na_silu = runda.ruke[igrac_id][0]
                    runda.karte_na_stolu.append(karta_na_silu)
                    runda.bacene_karte[igrac_id].append(karta_na_silu)
                    runda.ruke[igrac_id].remove(karta_na_silu)
                    print(f"⚠️ FORCE -> Igrač {igrac_id} baca: {karta_na_silu}")

        # --- ISPIS STANJA RUKU (SAD JE OVDJE, NAKON SVIH BACANJA) ---
        print("\n   --- STANJE RUKU NAKON ŠTIHA ---")
        for i in range(1, 5):
            ruka_str = [k.oznaka for k in runda.ruke[i]] 
            print(f"   Igrač {i}: {ruka_str}")
        print("   ------------------------------")

        # KRAJ ŠTIHA - KUPLJENJE
        print(f"\nStol: {[k.oznaka for k in runda.karte_na_stolu]}")
        
        try:
            runda.pokupi_stih()
            pobjednik = runda.red_igranja[0]
            print(f"🏆 Štih nosi Igrač {pobjednik}")
            
            # DODATAK: Bodovi za zadnji štih (Zadnja 10)
            # Ovo tvoja runda.py trenutno ne radi automatski, pa dodajem ručno ovdje
            if broj_stiha == 8:
                print("🏁 ZADNJA! (+10 bodova)")
                if pobjednik % 2 != 0:
                    runda.bodovi_mi += 10
                else:
                    runda.bodovi_vi += 10

        except Exception as e:
            print(f"❌ Greška: {e}")

    # 5. REZULTATI
    ispisi_razdvajac("KRAJ IGRE")
    print(f"Bodovi MI: {runda.bodovi_mi}")
    print(f"Bodovi VI: {runda.bodovi_vi}")
    print(f"Ukupno: {runda.bodovi_mi + runda.bodovi_vi} (Mora biti 162 ako nema zvanja)")