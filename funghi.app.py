import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pandas as pd
import datetime

# --- 1. Konfiguracja strony ---
st.set_page_config(page_title="Fungi Atelier | Grzyby Premium", page_icon="🍄", layout="centered")

# --- 2. MAGIA CSS (Stylizacja Premium) ---
st.markdown("""
<style>
    /* Ukrycie domyślnego menu i stopki Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Zmiana wyglądu głównego przycisku (Złoto/Zieleń) */
    div.stButton > button:first-child {
        background-color: #2E402B; /* Elegancka, głęboka zieleń */
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
        border: 1px solid #D4AF37; /* Złota ramka po najechaniu */
        color: #D4AF37;
    }
    
    /* Delikatne tło pod sekcjami */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Inicjalizacja bazy zamówień dla admina
if 'zamowienia' not in st.session_state:
    st.session_state.zamowienia = []

# --- 3. UKRYTY PANEL ADMINISTRATORA ---
st.sidebar.markdown("🔒 **Strefa Fungi Atelier**")
haslo_admin = st.sidebar.text_input("Hasło dostępu", type="password")

if haslo_admin == "Farma2026":
    st.title("🛠️ Panel Zarządzania")
    if len(st.session_state.zamowienia) > 0:
        df = pd.DataFrame(st.session_state.zamowienia)
        st.dataframe(df, use_container_width=True)
    else:
        st.info("Brak nowych zamówień w tej sesji.")
    st.stop()


# --- 4. GŁÓWNA STRONA DLA KLIENTÓW (PREMIUM) ---

# Pasek FOMO
st.error("🔥 **Ostatnie sztuki!** Na najbliższy zbiór zostało nam tylko **1.5 kg Soplówki Jeżowatej**.")

# Hero Image (Zdjęcie Główne z bazy Unsplash - potem podmienisz na swoje)
st.image("https://images.unsplash.com/photo-1542385151-efd9000785a0?q=80&w=1200&auto=format&fit=crop", use_column_width=True)

# Nagłówek
st.markdown("<h1 style='text-align: center;'>Fungi Atelier</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: gray;'>Rzemieślnicza uprawa grzybów egzotycznych</h4>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Ścinane na zamówienie. Dostarczane tego samego dnia w Starogardzie Gdańskim.</p>", unsafe_allow_html=True)

st.divider()

# Eleganckie zakładki zamiast zwykłego tekstu
tab1, tab2 = st.tabs(["🌿 Nasze Zbiory", "🧠 Dlaczego my?"])

with tab1:
    col1, col2 = st.columns(2)
    with col1:
        st.image("https://images.unsplash.com/photo-1633475027503-45a8df2410a6?q=80&w=600&auto=format&fit=crop", caption="Shiitake (Twardnik Japoński)")
        st.markdown("**Cena:** 40 zł / 1 kg")
        st.write("Mięsisty kapelusz, potężna dawka umami. Król azjatyckiej kuchni.")
    with col2:
        st.image("https://images.unsplash.com/photo-1605807646983-377bc5a76445?q=80&w=600&auto=format&fit=crop", caption="Soplówka (Lion's Mane)")
        st.markdown("**Cena:** 60 zł / 1 kg")
        st.write("Kulinarny rarytas przypominający mięso kraba. Ultra-świeża.")

with tab2:
    st.write("Przemysłowe grzyby często podróżują setki kilometrów zamknięte w duszącym plastiku, przez co tracą teksturę i 'pocą się'. My uprawiamy je w zautomatyzowanym mikroklimacie i ścinamy dopiero, gdy złożysz zamówienie. Otrzymujesz produkt najwyższej możliwej jakości, pachnący lasem.")

st.divider()

# --- 5. FORMULARZ ZAMÓWIEŃ ---
st.markdown("### 📦 Złóż rezerwację (bez zobowiązań)")

with st.form("preorder_form"):
    col_a, col_b = st.columns(2)
    with col_a:
        imie = st.text_input("Imię i Nazwisko / Nazwa Lokalu *")
        klient_typ = st.selectbox("Typ klienta", ["Osoba prywatna", "Restauracja"])
    with col_b:
        telefon = st.text_input("Numer telefonu *")
        produkt = st.selectbox("Wybierz zestaw", [
            "Zestaw MIX (Shiitake + Soplówka) - 500g",
            "Tylko Shiitake - 1 kg",
            "Tylko Soplówka - 500g",
            "Hurt B2B (kontakt telefoniczny)"
        ])
    
    uwagi = st.text_area("Dodatkowe uwagi (np. preferowane godziny odbioru)")
    
    submit_button = st.form_submit_button("ZAREZERWUJ ŚWIEŻE GRZYBY")

    if submit_button:
        if imie and telefon:
            st.session_state.zamowienia.append({"Data": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), "Klient": imie, "Telefon": telefon, "Produkt": produkt})
            st.success(f"Dziękujemy, {imie}! Rezerwacja przyjęta. Oddzwonimy na numer {telefon}.")
            st.balloons()
        else:
            st.error("Proszę wypełnić Imię i Telefon.")

# --- 6. STOPKA ---
st.markdown("<br><p style='text-align: center; color: gray; font-size: 12px;'>✉️ fungi.atelier@proton.me | 📞 +48 513-783-403</p>", unsafe_allow_html=True)
