import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pandas as pd
import datetime

# --- 1. KONFIGURACJA STRONY ---
st.set_page_config(page_title="Fungi Atelier | Grzyby Premium", page_icon="🍄", layout="centered")

# --- 2. STYLIZACJA PREMIUM (CSS) ---
st.markdown("""
<style>
    /* Ukrycie technicznego menu Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Zmiana wyglądu głównego przycisku formularza */
    div.stButton > button:first-child {
        background-color: #2E402B; /* Głęboka, butelkowa zieleń */
        color: #F5F5F5;
        border: 1px solid #2E402B;
        border-radius: 5px;
        padding: 10px 24px;
        font-weight: bold;
        width: 100%;
        transition: all 0.3s ease-in-out;
    }
    div.stButton > button:first-child:hover {
        background-color: #1A2618;
        border: 1px solid #D4AF37; /* Złoty akcent */
        color: #D4AF37;
    }
</style>
""", unsafe_allow_html=True)

# Inicjalizacja bazy zamówień dla sesji
if 'zamowienia' not in st.session_state:
    st.session_state.zamowienia = []

# --- 3. UKRYTY PANEL ADMINISTRATORA ---
st.sidebar.markdown("🔒 **Strefa Fungi Atelier**")
haslo_admin = st.sidebar.text_input("Hasło dostępu", type="password")

if haslo_admin == "Farma2026":
    st.title("🛠️ Panel Zarządzania")
    st.write("Witaj w panelu sterowania. Poniżej znajduje się lista rezerwacji.")
    if len(st.session_state.zamowienia) > 0:
        df = pd.DataFrame(st.session_state.zamowienia)
        st.dataframe(df, use_container_width=True)
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Pobierz do Excela (CSV)", data=csv, file_name="zamowienia_grzyby.csv", mime="text/csv")
    else:
        st.info("Brak nowych zamówień w tej sesji.")
    st.stop()


# --- 4. STRONA GŁÓWNA DLA KLIENTÓW ---

# Pasek FOMO
st.error("🔥 **Ostatnie sztuki!** Na najbliższy zbiór zostało nam tylko **1.5 kg Soplówki Jeżowatej**.")

# Hero Image (Klimatyczne, ciemne zdjęcie rzemieślniczych grzybów)
st.image("https://images.unsplash.com/photo-1583337130417-3346a1be7dee?q=80&w=1200&auto=format&fit=crop", use_column_width=True)

# Nagłówek i podtytuł
st.markdown("<h1 style='text-align: center; font-family: serif;'>Fungi Atelier</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: gray; font-weight: normal;'>Rzemieślnicza uprawa grzybów egzotycznych</h4>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Ścinane na zamówienie. Dostarczane tego samego dnia w Starogardzie Gdańskim.</p>", unsafe_allow_html=True)

st.divider()

# Zakładki ofertowe
tab1, tab2 = st.tabs(["🌿 Nasze Zbiory", "🧠 Dlaczego my?"])

with tab1:
    col1, col2 = st.columns(2)
    with col1:
        st.image("https://images.unsplash.com/photo-1587314168485-3236d6710814?q=80&w=600&auto=format&fit=crop", caption="Shiitake (Twardnik Japoński)")
        st.markdown("**Cena:** 40 zł / 1 kg")
        st.write("Mięsisty kapelusz, potężna dawka umami. Niezastąpiony do ramenu, woka lub na palone masło.")
    with col2:
        st.image("https://images.unsplash.com/photo-1605807646983-377bc5a76445?q=80&w=600&auto=format&fit=crop", caption="Soplówka (Lion's Mane)")
        st.markdown("**Cena:** 60 zł / 1 kg")
        st.write("Kulinarny rarytas przypominający w strukturze mięso kraba. Smażona jak stek rozpływa się w ustach.")

with tab2:
    st.write("Przemysłowe grzyby często podróżują setki kilometrów zamknięte w duszącym plastiku, przez co tracą teksturę, aromat i 'pocą się'.")
    st.write("My uprawiamy je lokalnie, w rygorystycznie kontrolowanym mikroklimacie i **ścinamy dopiero, gdy złożysz zamówienie**. Otrzymujesz produkt najwyższej jakości restauracyjnej, pachnący czystym lasem, zachowując pełen łańcuch chłodniczy.")

st.divider()

# --- 5. FORMULARZ ZAMÓWIEŃ ---
st.markdown("### 📦 Złóż rezerwację (bez zobowiązań)")
st.write("Wypełnij poniższy formularz. Odezwiemy się do Ciebie z informacją o dokładnym terminie zbioru i dostawy (zazwyczaj czwartek/piątek).")

with st.form("preorder_form"):
    col_a, col_b = st.columns(2)
    with col_a:
        imie = st.text_input("Imię i Nazwisko / Nazwa Lokalu *")
        klient_typ = st.selectbox("Typ klienta", ["Osoba prywatna", "Restauracja / B2B"])
    with col_b:
        telefon = st.text_input("Numer telefonu *")
        produkt = st.selectbox("Wybierz zestaw", [
            "Zestaw MIX (Shiitake + Soplówka) - 500g",
            "Tylko Shiitake - 1 kg",
            "Tylko Shiitake - 500g",
            "Tylko Soplówka - 500g",
            "Hurt Gastronomia (ustalimy telefonicznie)"
        ])
    
    uwagi = st.text_area("Dodatkowe uwagi (np. preferowane godziny odbioru)")
    
    submit_button = st.form_submit_button("ZAREZERWUJ ŚWIEŻE GRZYBY")

    if submit_button:
        if imie and telefon:
            # Zapis do ukrytego panelu administratora
            st.session_state.zamowienia.append({
                "Data": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), 
                "Klient": imie, 
                "Telefon": telefon, 
                "Produkt": produkt,
                "Typ": klient_typ
            })
            
            # Próba wysłania powiadomienia e-mail (jeśli skonfigurowano st.secrets)
            try:
                if "EMAIL_SENDER" in st.secrets:
                    nadawca_email = st.secrets["EMAIL_SENDER"]
                    haslo_email = st.secrets["EMAIL_PASSWORD"]
                    odbiorca_email = "fungi.atelier@proton.me"

                    msg = MIMEMultipart()
                    msg['From'] = nadawca_email
                    msg['To'] = odbiorca_email
                    msg['Subject'] = f"🍄 NOWE ZAMÓWIENIE: {imie} ({produkt})"

                    tresc = f"Nowe zamówienie z Fungi Atelier!\n\nData: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\nTyp: {klient_typ}\nKlient: {imie}\nTelefon: {telefon}\nProdukt: {produkt}\nUwagi: {uwagi if uwagi else 'Brak'}"
                    msg.attach(MIMEText(tresc, 'plain'))

                    server = smtplib.SMTP('smtp.gmail.com', 587)
                    server.starttls()
                    server.login(nadawca_email, haslo_email)
                    server.send_message(msg)
                    server.quit()

                st.success(f"Dziękujemy, {imie}! Rezerwacja przyjęta. Oczekuj na kontakt z naszej strony pod numerem {telefon}.")
                st.balloons()
            except Exception as e:
                # Jeśli e-mail nie wyjdzie (bo brak konfiguracji w chmurze), klient i tak widzi sukces, a zamówienie wpada do panelu Admina.
                st.success(f"Dziękujemy, {imie}! Rezerwacja zapisana w systemie. Oddzwonimy!")
                st.balloons()
        else:
            st.error("Proszę wypełnić pola oznaczone gwiazdką (Imię i Telefon).")

# --- 6. STOPKA KONTAKTOWA ---
st.markdown("<br><p style='text-align: center; color: gray; font-size: 13px;'>✉️ fungi.atelier@proton.me | 📞 +48 513-783-403</p>", unsafe_allow_html=True)
