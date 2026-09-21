import streamlit as st
from datetime import datetime
import time

def wczytaj_protokol_txt(sciezka):
    kroki=[]
    with open(sciezka, 'r', encoding='utf-8') as plik:
        for i, linia in enumerate(plik):
            linia = linia.strip()
            if not linia:
                continue
            elementy = linia.split('|')

            if len(elementy) == 3:
                opis = elementy[0].strip()
                czy_timer = (elementy[1].strip().lower() == 'tak')
                czas = int(elementy[2].strip())

                kroki.append({
                    "id": i + 1,
                    "opis": opis,
                    "wymaga_timera": czy_timer,
                    "czas_sekundy": czas
                })
    return kroki
st.title("Laboratoryjna checklista")

wgrany_plik = st.sidebar.file_uploader("Wgraj swoj plik .txt", type=["txt"])
if wgrany_plik is not None:
    with open("nowy_protokol_tymczasowy.txt", "wb") as f:
        f.write(wgrany_plik.getvalue())
    sciezka_do_odczytu = "nowy_protokol_tymczasowy.txt"
    st.sidebar.success("Plik zaladowany")
else:
    sciezka_do_odczytu = "protokol.txt"

lista_krokow = wczytaj_protokol_txt(sciezka_do_odczytu)

if "znaczniki_czasu" not in st.session_state:
    st.session_state.znaczniki_czasu = {}
for krok in lista_krokow:
    col1, col2 = st.columns([3, 1])

    with col1:
        zaznaczony = st.checkbox(krok["opis"], key=f"krok_{krok['id']}")
        if zaznaczony:
            if krok["id"] not in st.session_state.znaczniki_czasu:
                st.session_state.znaczniki_czasu[krok["id"]] = datetime.now().strftime("%H:%M:%S")
            st.write(f"Wykonano: **{st.session_state.znaczniki_czasu[krok['id']]}**")
        else:
            if krok["id"] in st.session_state.znaczniki_czasu:
                del st.session_state.znaczniki_czasu[krok["id"]]

    with col2:
        if krok["wymaga_timera"]:
            if st.button(f"Start {krok['czas_sekundy']} s", key=f"timer_{krok['id']}"):
                okienko_timera = st.empty()
                for pozostalo in range(krok['czas_sekundy'], -1, -1):
                    minuty, sekundy = divmod(pozostalo, 60)
                    okienko_timera.metric("Czas do końca", f"{minuty:02d}:{sekundy:02d}")
                    time.sleep(1)
                okienko_timera.empty()
                st.success("Koniec czasu")
            


    
