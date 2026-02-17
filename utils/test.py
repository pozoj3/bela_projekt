from runda import Runda
from karta import Karta

# Pomoćna funkcija za ljepši ispis
def run_test(naziv, ocekivano, rezultat):
    status = "✅ PROŠLO" if ocekivano == rezultat else "❌ PALO"
    print(f"{status} | {naziv}")
    print(f"   -> Očekivano: {ocekivano}, Dobiveno: {rezultat}\n")

if __name__ == "__main__":
    print("=== TESTIRANJE PRAVILA (NOVA KLASA) ===\n")

    # 1. INICIJALIZACIJA (Prilagođeno novoj klasi)
    runda = Runda()
    runda.promjesaj_karte(prvi_na_redu=1) # Bitno da se kreiraju liste u rječnicima
    
    # Postavljamo aduta za test (Herc)
    runda.adut = "H" 
    print(f"Postavljen adut: {runda.adut} (Herc)\n")

    # ==========================================
    # 1. TESTIRANJE: POŠTIVANJE BOJE
    # ==========================================
    print("---------------------------------------")
    print("--- 1. TESTIRANJE POŠTIVANJA BOJE ---")
    print("---------------------------------------\n")

    # SCENARIO 1: Imaš boju i baciš je -> TRUE
    # Stol: Pik 10
    # Ruka: Pik 7, Tref 8
    # Potez: Pik 7
    runda.karte_na_stolu = [Karta("Pc")] 
    runda.ruke[1] = [Karta("P7"), Karta("T8")] 
    rezultat = runda.postivanje_boje(Karta("P7"), br_igraca=1)
    run_test("Igrač ima boju i poštuje ju", True, rezultat)

    # SCENARIO 2: Imaš boju, ali bacaš drugu (Renons) -> FALSE
    # Stol: Pik 10
    # Ruka: Pik 7, Tref 8
    # Potez: Tref 8
    runda.karte_na_stolu = [Karta("Pc")] 
    runda.ruke[1] = [Karta("P7"), Karta("T8")] 
    rezultat = runda.postivanje_boje(Karta("T8"), br_igraca=1)
    run_test("Igrač ima boju ali baca drugu", False, rezultat)

    # SCENARIO 3: Nemaš boju, imaš aduta, sječeš adutom -> TRUE
    # Stol: Pik 10
    # Ruka: Herc 8 (Adut), Tref 8
    # Potez: Herc 8
    runda.karte_na_stolu = [Karta("Pc")] 
    runda.ruke[1] = [Karta("H8"), Karta("T8")] 
    rezultat = runda.postivanje_boje(Karta("H8"), br_igraca=1)
    run_test("Igrač nema boju, sječe adutom", True, rezultat)

    # SCENARIO 4: Nemaš boju, imaš aduta, ALI bacaš škart -> FALSE
    # Stol: Pik 10
    # Ruka: Herc 8 (Adut), Tref 8
    # Potez: Tref 8
    runda.karte_na_stolu = [Karta("Pc")] 
    runda.ruke[1] = [Karta("H8"), Karta("T8")] 
    rezultat = runda.postivanje_boje(Karta("T8"), br_igraca=1)
    run_test("Igrač ne sječe iako ima aduta", False, rezultat)

    # SCENARIO 5: Nemaš boju, NEMAŠ aduta, bacaš bilo što -> TRUE
    # Stol: Pik 10
    # Ruka: Karo 9, Tref 8
    # Potez: Tref 8
    runda.karte_na_stolu = [Karta("Pc")] 
    runda.ruke[1] = [Karta("K9"), Karta("T8")] 
    rezultat = runda.postivanje_boje(Karta("T8"), br_igraca=1)
    run_test("Igrač nema ni boju ni aduta (škart)", True, rezultat)


    # ==========================================
    # 2. TESTIRANJE: POŠTIVANJE IBERA
    # ==========================================
    print("---------------------------------------")
    print("--- 2. TESTIRANJE POŠTIVANJA IBERA ---")
    print("---------------------------------------\n")

    # SCENARIO 1: Prva karta na stolu (prazan stol) -> TRUE
    runda.karte_na_stolu = []
    rezultat = runda.postivanje_ibera(Karta("H8"))
    run_test("Prva karta na stolu", True, rezultat)

    # SCENARIO 2: Bacaš jaču kartu od one na stolu -> TRUE
    # Stol: Pik 9
    # Potez: Pik 10 (c)
    runda.karte_na_stolu = [Karta("P9")]
    rezultat = runda.postivanje_ibera(Karta("Pc"))
    run_test("Igrač baca jaču kartu (ibera)", True, rezultat)

    # SCENARIO 3: Bacaš slabiju kartu od one na stolu -> FALSE (Po tvojoj logici)
    # Stol: Pik 10 (c)
    # Potez: Pik 7
    runda.karte_na_stolu = [Karta("Pc")]
    rezultat = runda.postivanje_ibera(Karta("P7"))
    run_test("Igrač baca slabiju kartu (zabranjeno u tvojoj logici)", False, rezultat)

    # SCENARIO 4: Adut na ne-aduta (Mora biti jače) -> TRUE
    # Stol: Pik 10
    # Potez: Herc 7 (Adut)
    runda.karte_na_stolu = [Karta("Pc")]
    rezultat = runda.postivanje_ibera(Karta("H7"))
    run_test("Rezanje adutom je 'iber'", True, rezultat)

    # SCENARIO 5: Adut na slabiji adut -> TRUE
    # Stol: Herc 9 (14)
    # Potez: Herc Dečko (20)
    runda.karte_na_stolu = [Karta("H9")]
    rezultat = runda.postivanje_ibera(Karta("Hd"))
    run_test("Iber u adutu (Dečko na 9)", True, rezultat)