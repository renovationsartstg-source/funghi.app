import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pandas as pd
import datetime

# --- 1. KONFIGURACJA STRONY ---
st.set_page_config(
    page_title="Fungi Atelier | Grzyby Premium", 
    page_icon="🍄", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- 2. AGRESYWNY CSS ---
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    [data-testid="collapsedControl"] {display: none;} 
    
    .block-container {
        padding-top: 1rem;
        padding-bottom: 2rem;
    }
    
    div.stButton > button:first-child {
        background-color: #121212; 
        color: #D4AF37;
        border: 1px solid #D4AF37;
        border-radius: 4px;
        padding: 12px 24px;
        font-weight: 600;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        width: 100%;
        transition: all 0.3s ease-in-out;
    }
    div.stButton > button:first-child:hover {
        background-color: #D4AF37;
        color: #121212;
        border: 1px solid #121212;
        box-shadow: 0px 4px 15px rgba(212, 175, 55, 0.3);
    }
    
    /* Ukrycie tła dla rozwijanego panelu logowania, żeby był dyskretny */
    .streamlit-expanderHeader {
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. INICJALIZACJA SESJI I BAZY DANYCH ---
if 'zamowienia' not in st.session_state:
    st.session_state.zamowienia = []

if 'is_admin' not in st.session_state:
    st.session_state.is_admin = False

# Dynamiczny pasek ogłoszeń (FOMO) w pamięci sesji
if 'fomo_text' not in st.session_state:
    st.session_state.fomo_text = "🔥 **Ostatnie sztuki!** Ze względu na rzemieślniczy proces, na najbliższy zbiór zostało nam tylko **1.5 kg Soplówki**."

if 'show_fomo' not in st.session_state:
    st.session_state.show_fomo = True


# --- 4. BEZPIECZNY PANEL ADMINISTRATORA (WIDOK PO ZALOGOWANIU) ---
if st.session_state.is_admin:
    st.title("🛠️ Fungi Atelier - Centrum Dowodzenia")
    st.success("Zabezpieczona sesja. Zalogowano pomyślnie.")
    
    # Przycisk wylogowania
    if st.button("🚪 Wyloguj i wróć do sklepu"):
        st.session_state.is_admin = False
        st.rerun()
        
    st.divider()
    
    # --- NOWOŚĆ: Edycja paska ogłoszeń ---
    st.subheader("📢 Zarządzanie ogłoszeniami (Pasek na górze strony)")
    nowy_tekst_fomo = st.text_area("Treść ogłoszenia (możesz używać gwiazdek **tekst** do pogrubienia):", value=st.session_state.fomo_text)
    pokaz_fomo = st.checkbox("Wyświetlaj pasek ogłoszeń klientom", value=st.session_state.show_fomo)
    
    if st.button("💾 Zapisz zmiany na stronie"):
        st.session_state.fomo_text = nowy_tekst_fomo
        st.session_state.show_fomo = pokaz_fomo
        st.success("Strona główna zaktualizowana!")
        
    st.divider()
    
    # --- Baza zamówień ---
    st.subheader("📦 Baza Zamówień")
    
    if len(st.session_state.zamowienia) > 0:
        df = pd.DataFrame(st.session_state.zamowienia)
        st.dataframe(df, use_container_width=True)
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Pobierz listę rezerwacji (CSV)", data=csv, file_name="zamowienia_grzyby.csv", mime="text/csv")
    else:
        st.info("Brak nowych zamówień. Klienci jeszcze śpią.")
        
    st.stop() # Zatrzymuje kod, żeby zalogowany admin nie widział na dole strony dla klientów

# =====================================================================
# --- 5. STRONA GŁÓWNA DLA KLIENTA (WIDOK PRZED ZALOGOWANIEM) ---
# =====================================================================

# Wyświetlanie dynamicznego paska FOMO, jeśli jest włączony w panelu Admina
if st.session_state.show_fomo and st.session_state.fomo_text.strip() != "":
    st.error(st.session_state.fomo_text)

try:
    st.image("image_hero.png", use_column_width=True)
except:
    pass

st.markdown("<h1 style='text-align: center; font-family: serif; margin-bottom: 0;'>Fungi Atelier</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: #a3a3a3; font-weight: 400; margin-top: 5px;'>Ekskluzywna uprawa grzybów egzotycznych</h4>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 14px;'>Ścinane na zamówienie. Gwarancja pełnego łańcucha chłodniczego z dostawą w Starogardzie.</p>", unsafe_allow_html=True)

st.divider()

tab1, tab2 = st.tabs(["🌿 Oferta (Pre-order)", "🧠 Nasza Filozofia"])

with tab1:
    col1, col2 = st.columns(2)
    with col1:
        try: st.image("image_shiitake.png")
        except: pass
        st.markdown("**🪵 Shiitake Premium**")
        st.markdown("*Cena: 40 zł / 1 kg (Świeże)*")
        st.caption("Mięsisty, jędrny kapelusz. Tłocznia umami dla Twoich dań.")
    with col2:
        try: st.image("image_lions_mane.png")
        except: pass
        st.markdown("**☁️ Soplówka Jeżowata**")
        st.markdown("*Cena: 60 zł / 1 kg (Świeże)*")
        st.caption("Kulinarny rarytas. Struktura przypominająca mięso homara.")

with tab2:
    st.markdown("### Koniec z zaparzonymi grzybami z marketu.")
    st.write("Większość grzybów w dystrybucji przemysłowej traci 50% swoich walorów przez złą temperaturę i duszący plastik. My uprawiamy je w zautomatyzowanym mikroklimacie i **ścinamy dopiero, gdy klikniesz przycisk**.")
    st.markdown("### 🍂 Esencja Smaku (Nasze Susze)")
    st.write("Część naszych najpiękniejszych zbiorów powoli suszymy w niskich temperaturach. Dzięki temu pozbywamy się wody, zamykając 100% aromatu i właściwości prozdrowotnych w wygodnej formie, idealnej do wywarów, sosów i ramenu.")

st.divider()

st.markdown("### 📦 Rezerwacja na najbliższy zbiór")

with st.form("preorder_form", clear_on_submit=True):
    col_a, col_b = st.columns(2)
    with col_a:
        imie = st.text_input("Imię i Nazwisko / Nazwa Lokalu *")
        telefon = st.text_input("Numer telefonu *")
        klient_typ = st.selectbox("Typ klienta", ["Osoba prywatna", "Restauracja / Szef Kuchni"])
    with col_b:
        produkt = st.selectbox("Wybierz produkt", [
            "🌿 ŚWIEŻE: Zestaw MIX Degustacyjny (Shiitake + Soplówka) - 500g",
            "🌿 ŚWIEŻE: Zestaw MIX Kulinarny - 1 kg",
            "🌿 ŚWIEŻE: Tylko Shiitake Premium - 500g",
            "🌿 ŚWIEŻE: Tylko Soplówka Jeżowata - 500g",
            "🍂 SUSZONE: Shiitake (Intensywne Umami) - 50g",
            "🍂 SUSZONE: Soplówka Jeżowata (Ekstrakt Nootropowy) - 50g",
            "🍂 SUSZONE: Zestaw MIX Suszony - 100g",
            "🔄 SUBSKRYPCJA: Świeży MIX co tydzień (4x 500g / miesiąc)",
            "👨‍🍳 GASTRONOMIA: Pakiet Testowy B2B (Darmowa próbka)",
            "🏢 GASTRONOMIA: Zamówienie Hurtowe (powyżej 3 kg)"
        ])
    
    uwagi = st.text_area("Uwagi do zamówienia (np. preferowany dzień odbioru / dane do wysyłki Paczkomatem)")
    
    submit_button = st.form_submit_button("Potwierdź rezerwację (bez płatności)")

    if submit_button:
        if imie and telefon:
            st.session_state.zamowienia.append({
                "Data": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), 
                "Klient": imie, 
                "Telefon": telefon, 
                "Produkt": produkt,
                "Typ": klient_typ,
                "Uwagi": uwagi
            })
            
            try:
                if "EMAIL_SENDER" in st.secrets:
                    nadawca_email = st.secrets["EMAIL_SENDER"]
                    haslo_email = st.secrets["EMAIL_PASSWORD"]
                    odbiorca_email = "fungi.atelier@proton.me"

                    msg = MIMEMultipart()
                    msg['From'] = nadawca_email
                    msg['To'] = odbiorca_email
                    msg['Subject'] = f"🍄 ZAMÓWIENIE: {imie} ({produkt})"

                    tresc = f"Nowa rezerwacja z Fungi Atelier!\n\nData: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\nTyp: {klient_typ}\nKlient: {imie}\nTelefon: {telefon}\nProdukt: {produkt}\nUwagi: {uwagi if uwagi else 'Brak'}"
                    msg.attach(MIMEText(tresc, 'plain'))

                    server = smtplib.SMTP('smtp.gmail.com', 587)
                    server.starttls()
                    server.login(nadawca_email, haslo_email)
                    server.send_message(msg)
                    server.quit()
            except Exception:
                pass 
            
            st.toast(f"Sukces! Rezerwacja na {produkt} została zapisana.", icon="🥂")
            st.balloons()
        else:
            st.error("Wypełnij wymagane pola: Imię oraz Telefon.")

st.divider()

# --- 6. UKRYTA SEKCJA LOGOWANIA W STOPCE ---
st.markdown("<p style='text-align: center; color: #555; font-size: 12px;'>Fungi Atelier © 2026 | fungi.atelier@proton.me | +48 513-783-403</p>", unsafe_allow_html=True)

with st.expander("🔒"):
    haslo_wejsciowe = st.text_input("Zarządzanie", type="password", help="Wpisz hasło administratora")
    if haslo_wejsciowe == "Farma2026":
        st.session_state.is_admin = True
        st.rerun()
    elif haslo_wejsciowe != "":
        st.error("Błędne hasło.")
