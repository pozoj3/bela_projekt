from runda import Runda
from karta import Karta
import random
import time

def ispisi_razdvajac(naslov):
    print(f"\n{'='*20} {naslov} {'='*20}")

if __name__ == "__main__":
    ispisi_razdvajac("POČETAK SIMULACIJE (ZVANJA + BELA)")

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

    # 3. UZIMANJE TALONA, SORTIRANJE I POČETNA ZVANJA
    print("\n--- OBRADA ZVANJA (PRIJE IGRE) ---")
    
    for i in range(1, 5):
        runda.otkrij_karte(i) 
        runda.sortiraj_ruku(i)
        runda.zvanja_karte(i) # Provjeri ima li nize ili 4 iste
        
        if runda.bodovi_zvanja[i] > 0:
            print(f"Igrač {i} prijavljuje: {runda.popis_zvanja[i]} ({runda.bodovi_zvanja[i]} bodova)")
    
    # Validacija zvanja (tko je jači)
    runda.validna_zvanja()
    
    print("\n--- PRIZNATA ZVANJA ---")
    ukupno_zvanja_mi = runda.bodovi_zvanja[1] + runda.bodovi_zvanja[3]
    ukupno_zvanja_vi = runda.bodovi_zvanja[2] + runda.bodovi_zvanja[4]
    print(f"MI: {ukupno_zvanja_mi} | VI: {ukupno_zvanja_vi}")

    # 4. IGRA (8 ŠTIHOVA)
    for broj_stiha in range(1, 9):
        ispisi_razdvajac(f"ŠTIH BROJ {broj_stiha}")
        
        # --- A) ISPIS RUKU ---
        print("   --- RUKU PRIJE ŠTIHA ---")
        for i in range(1, 5):
            ruka_str = [k.oznaka for k in runda.ruke[i]]
            oznaka = ">>" if i == runda.red_igranja[0] else "  "
            print(f"   {oznaka} Igrač {i}: {ruka_str}")
        print("   ------------------------\n")

        red_igranja = runda.red_igranja
        print(f"Redoslijed: {red_igranja}")

        # --- B) BACANJE KARATA ---
        for igrac_id in red_igranja:
            bacio_kartu = False
            
            # --- DETEKCIJA BELE (1. DIO) ---
            # Zapamtimo koliko bodova zvanja igrač ima PRIJE bacanja
            stari_bodovi_zvanja = runda.bodovi_zvanja[igrac_id]
            
            # 1. POKUŠAJ PO PRAVILIMA
            for karta in runda.ruke[igrac_id][:]:
                if runda.baci_kartu(karta, igrac_id):
                    print(f"✅ Igrač {igrac_id} baca: {karta}")
                    
                    # --- DETEKCIJA BELE (2. DIO) ---
                    # Provjerimo ima li sada više bodova nego prije
                    novi_bodovi_zvanja = runda.bodovi_zvanja[igrac_id]
                    if novi_bodovi_zvanja > stari_bodovi_zvanja:
                        # Ako su bodovi porasli, znači da je zvao Belu!
                        print(f"🔔 🔔 🔔 IGRAČ {igrac_id} ZOVE BELU! (+20) 🔔 🔔 🔔")
                    
                    bacio_kartu = True
                    break 
            
            # 2. POKUŠAJ NA SILU (Fallback)
            if not bacio_kartu:
                if len(runda.ruke[igrac_id]) > 0:
                    karta_na_silu = runda.ruke[igrac_id][0]
                    # Ovdje nema detekcije bele jer 'baci_kartu' nije uspio
                    runda.karte_na_stolu.append(karta_na_silu)
                    runda.bacene_karte[igrac_id].append(karta_na_silu)
                    runda.ruke[igrac_id].remove(karta_na_silu)
                    print(f"⚠️ FORCE -> Igrač {igrac_id} baca: {karta_na_silu}")

        # --- C) OBRADA ŠTIHA ---
        print(f"\nStol: {[k.oznaka for k in runda.karte_na_stolu]}")
        
        try:
            runda.pokupi_stih()
            pobjednik = runda.red_igranja[0]
            print(f"🏆 Štih nosi Igrač {pobjednik}")
            
            if broj_stiha == 8:
                print("🏁 ZADNJA (+10 bodova)")

            print(f"📊 BODOVI IGRE -> MI: {runda.bodovi_mi} | VI: {runda.bodovi_vi}")

        except Exception as e:
            print(f"❌ Greška u pokupi_stih: {e}")

    # 5. KONAČNI REZULTATI
    ispisi_razdvajac("KRAJ RUNDE")
    
    # Ponovno dohvaćamo zvanja jer se BELA naknadno dodala u runda.bodovi_zvanja
    ukupno_zvanja_mi = runda.bodovi_zvanja[1] + runda.bodovi_zvanja[3]
    ukupno_zvanja_vi = runda.bodovi_zvanja[2] + runda.bodovi_zvanja[4]

    konacni_mi = runda.bodovi_mi + ukupno_zvanja_mi
    konacni_vi = runda.bodovi_vi + ukupno_zvanja_vi
    
    print(f"Bodovi iz igre (MI): {runda.bodovi_mi}")
    print(f"Bodovi iz zvanja (MI): {ukupno_zvanja_mi} (Zvanja + Bela)")
    print(f"--- UKUPNO MI: {konacni_mi} ---")
    
    print("-" * 20)
    
    print(f"Bodovi iz igre (VI): {runda.bodovi_vi}")
    print(f"Bodovi iz zvanja (VI): {ukupno_zvanja_vi} (Zvanja + Bela)")
    print(f"--- UKUPNO VI: {konacni_vi} ---")
    
    print(f"\nSVEUKUPNO: {konacni_mi + konacni_vi}")