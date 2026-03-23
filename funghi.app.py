import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pandas as pd
import datetime

# --- 1. Konfiguracja strony ---
st.set_page_config(
    page_title="Fungi Atelier | Grzyby Premium",
    page_icon="🍄",
    layout="centered"
)

# Inicjalizacja "bazy danych" w pamięci sesji (dla symulacji zamówień w panelu admina)
if 'zamowienia' not in st.session_state:
    st.session_state.zamowienia = []

# --- 2. UKRYTY PANEL ADMINISTRATORA ---
st.sidebar.markdown("🔒 **Strefa Fungi Atelier**")
haslo_admin = st.sidebar.text_input("Hasło dostępu", type="password")

# Jeśli wpisano poprawne hasło, pokazujemy tylko panel admina i zatrzymujemy resztę aplikacji
if haslo_admin == "Farma2026":  # W produkcji to hasło powinno być w st.secrets!
    st.title("🛠️ Panel Zarządzania Zamówieniami")
    st.write("Witaj w panelu sterowania Fungi Atelier. Poniżej znajduje się lista rezerwacji z obecnej sesji.")
    
    if len(st.session_state.zamowienia) > 0:
        # Konwersja listy słowników na ładną tabelę (DataFrame)
        df = pd.DataFrame(st.session_state.zamowienia)
        st.dataframe(df, use_container_width=True)
        
        # Opcja pobrania zamówień do Excela/CSV
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Pobierz bazę jako plik CSV", data=csv, file_name="zamowienia_grzyby.csv", mime="text/csv")
    else:
        st.info("Brak nowych zamówień w tej sesji.")
        
    st.stop() # Ta komenda ukrywa resztę strony dla klientów, jeśli jesteś zalogowany jako admin!


# --- 3. GŁÓWNA STRONA DLA KLIENTÓW ---

# Pasek FOMO (Fear Of Missing Out)
st.error("🔥 **Ostatnie sztuki!** Na najbliższy zbiór zostało nam tylko **1.5 kg Soplówki Jeżowatej**. Rezerwacje zamykamy w środę o 20:00!")

# Nagłówek
st.title("🍄 Fungi Atelier - Grzyby Premium")
st.markdown("### Świeże, rzemieślnicze grzyby egzotyczne ze Starogardu Gdańskiego.")
st.write("Nie sprzedajemy grzybów, które leżały tydzień w chłodni. Działamy w modelu **Pre-order** – ścinamy towar dokładnie wtedy, gdy złożysz zamówienie. Prosto z naszego mikroklimatu do Twojej kuchni.")

st.divider()

# Sekcja Oferty
st.header("🌿 Nasze Zbiory")
col1, col2 = st.columns(2)

with col1:
    st.subheader("🪵 Shiitake")
    st.write("Twardy, mięsisty kapelusz, potężna dawka umami. Idealny do ramenu, na masło lub do woka.")
    st.markdown("**Cena:** 40 zł / 1 kg")

with col2:
    st.subheader("☁️ Soplówka Jeżowata")
    st.write("Kulinarny rarytas przypominający mięso kraba. Naturalny nootropik (wspiera pracę mózgu).")
    st.markdown("**Cena:** 60 zł / 1 kg")

st.divider()

# --- 4. SEKCJA EDUKACYJNA (FAQ) ---
st.header("🧠 Często Zadawane Pytania")

with st.expander("Jak długo grzyby wytrzymają w lodówce?"):
    st.write("Dostarczamy grzyby w ciągu kilku godzin od ścięcia z kostki. Zapakowane w oddychającą, papierową torbę, w domowej lodówce zachowają idealną jędrność i aromat przez **7 do 10 dni**.")

with st.expander("Dlaczego wasze grzyby są inne niż te z marketu?"):
    st.write("Przemysłowe grzyby często podróżują setki kilometrów zamknięte w duszącym plastiku, przez co tracą teksturę i 'pocą się'. My ścinamy je specjalnie dla Ciebie, z gwarancją zachowania ciągłego łańcucha chłodniczego.")

with st.expander("Jak najlepiej przyrządzić Soplówkę? (Kulinarny tip)"):
    st.write("Potraktuj ją jak owoce morza! Pokrój kule w grube na 1,5 cm plastry. Wrzuć na suchą patelnię, żeby odparować trochę wody, a następnie dodaj solidną łyżkę masła, ząbek czosnku i smaż na złoty kolor z obu stron. Na koniec oprósz solą. Proste i genialne.")

st.divider()

# --- 5. FORMULARZ ZAMÓWIEŃ ---
st.header("📦 Zapisz się na najbliższy zbiór!")
st.write("Wypełnij formularz. Odezwiemy się do Ciebie z informacją o dokładnym terminie odbioru (zazwyczaj czwartek/piątek).")

with st.form("preorder_form"):
    klient_typ = st.radio("Jesteś klientem indywidualnym czy reprezentujesz restaurację?", ["Osoba prywatna", "Restauracja / Szef Kuchni"])
    
    imie = st.text_input("Imię i Nazwisko / Nazwa Lokalu *")
    telefon = st.text_input("Numer telefonu *")
    
    produkt = st.selectbox("Co chcesz zarezerwować?", [
        "Zestaw Degustacyjny MIX (Shiitake + Soplówka) - 500g",
        "Tylko Shiitake - 500g",
        "Tylko Shiitake - 1 kg",
        "Tylko Soplówka - 500g",
        "Zamówienie Hurtowe (ustalimy przez telefon)"
    ])
    
    uwagi = st.text_area("Dodatkowe uwagi (np. preferowane godziny odbioru)")
    
    submit_button = st.form_submit_button("Złóż rezerwację (bez zobowiązań)")

    if submit_button:
        if imie and telefon:
            # 1. Zapis do wewnętrznej bazy danych (Dla panelu admina)
            st.session_state.zamowienia.append({
                "Data": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                "Klient": imie,
                "Telefon": telefon,
                "Typ": klient_typ,
                "Produkt": produkt,
                "Uwagi": uwagi
            })
            
            # 2. Mechanizm wysyłania e-maila
            try:
                # W wersji lokalnej możesz wpisać hasło w st.secrets.
                # Jeśli jeszcze tego nie masz, aplikacja po prostu zapisze to w panelu i pokaże błąd maila.
                if "EMAIL_SENDER" in st.secrets:
                    nadawca_email = st.secrets["EMAIL_SENDER"]
                    haslo_email = st.secrets["EMAIL_PASSWORD"]
                    odbiorca_email = "fungi.atelier@proton.me"

                    msg = MIMEMultipart()
                    msg['From'] = nadawca_email
                    msg['To'] = odbiorca_email
                    msg['Subject'] = f"🍄 NOWE ZAMÓWIENIE: {imie} ({produkt})"

                    tresc = f"""
                    Nowe zamówienie z Fungi Atelier!
                    
                    Data: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}
                    Typ klienta: {klient_typ}
                    Imię/Nazwa: {imie}
                    Telefon: {telefon}
                    Zamówienie: {produkt}
                    Uwagi: {uwagi if uwagi else 'Brak'}
                    """
                    msg.attach(MIMEText(tresc, 'plain'))

                    server = smtplib.SMTP('smtp.gmail.com', 587)
                    server.starttls()
                    server.login(nadawca_email, haslo_email)
                    server.send_message(msg)
                    server.quit()

                st.success(f"Dziękujemy, {imie}! Twoja rezerwacja została przyjęta. Zadzwonimy na numer {telefon}!")
                st.balloons()
                
            except Exception as e:
                # Nawet jak mail nie wyjdzie (brak konfiguracji), to zapisze się w panelu admina!
                st.warning("Rezerwacja zapisana w systemie! (Uwaga: powiadomienie e-mail nie zostało skonfigurowane).")
        else:
            st.error("Proszę wypełnić pola oznaczone gwiazdką (Imię i Telefon).")

# --- 6. STOPKA ---
st.divider()
st.markdown("### Kontakt z Fungi Atelier")
st.markdown("✉️ **E-mail:** fungi.atelier@proton.me")
st.markdown("📞 **Telefon:** +48 513-783-403")