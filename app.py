import streamlit as st
import pycountry
import io
from PIL import Image


# --- SETUP PAGE ---
st.set_page_config(page_title="RtR Geographical Presence Tool", layout="centered")


def apply_custom_style():
    st.markdown("""
    <style>
       

        /* HEADER and TEXT COLORS */
        h1, h2, h3, h4, h5, h6 {
            color: #112E4D;
        }

      

        /* PRIMARY BUTTON */
        .stButton>button {
            background-color: #FF37D5;
            color: white;
            border-radius: 6px;
            font-weight: bold;
        }
        .stButton>button:hover {
            background-color: #e126b9;
            color: white;
        }

        /* DOWNLOAD BUTTON */
        .stDownloadButton>button {
            background-color: #112E4D;
            color: white;
            border-radius: 6px;
        }
        .stDownloadButton>button:hover {
            background-color: #0a1d33;
        }

        /* TEXTAREA */
        textarea {
            background-color: #ffffff;
            border: 1px solid #112E4D;
        }

    

        /* RADIO BUTTONS */
        .stRadio label {
            font-weight: bold;
            color: #112E4D;
        }
    </style>
    """, unsafe_allow_html=True)

# Apply the style
apply_custom_style()






# --- COUNTRY DATA ---
countries = {country.alpha_2: country.name for country in pycountry.countries}
country_list = sorted(countries.values())

# --- CONTINENT → COUNTRY CODES ---
continents = {
    "Africa": ["DZ", "EG", "LY", "MA", "SD", "TN", "AO", "BF", "BI", "BJ", "BW", "CD", "CF", "CG", "CI", "CM", "DJ", "ER", "ET", "GA", "GH", "GM", "GN", "GQ", "KE", "KM", "LR", "LS", "MG", "ML", "MR", "MU", "MW", "MZ", "NA", "NE", "NG", "RW", "SC", "SL", "SN", "SO", "SS", "ST", "SZ", "TD", "TG", "TZ", "UG", "ZA", "ZM", "ZW"],
    "Americas": ["AR", "BO", "BR", "CL", "CO", "CR", "CU", "DO", "EC", "GT", "HN", "HT", "JM", "MX", "NI", "PA", "PE", "PY", "SV", "TT", "UY", "VE", "CA", "US", "BS", "DM"],
    "Asia": ["KZ", "KG", "TJ", "TM", "UZ", "CN", "JP", "KP", "KR", "MN", "TW", "AF", "BD", "BT", "IN", "IR", "LK", "MV", "NP", "PK", "BN", "KH", "ID", "LA", "MY", "MM", "PH", "SG", "TH", "TL", "VN", "AM", "AZ", "BH", "CY", "GE", "IQ", "IL", "JO", "KW", "LB", "OM", "QA", "SA", "SY", "TR", "AE", "YE"],
    "Europe": ["BY", "BG", "CZ", "HU", "MD", "PL", "RO", "RU", "SK", "UA", "DK", "EE", "FI", "IS", "IE", "LV", "LT", "NO", "SE", "GB", "AL", "AD", "BA", "HR", "GR", "IT", "MT", "ME", "PT", "SM", "RS", "SI", "ES", "VA", "AT", "BE", "FR", "DE", "LI", "LU", "MC", "NL", "CH"],
    "Oceania": ["AU", "NZ", "FJ", "NC", "PG", "SB", "VU", "FM", "GU", "KI", "MH", "NR", "PW", "AS", "CK", "NU", "PF", "PN", "WS", "TO", "TV"]
}

logo = Image.open("images/logo_web.png")

col1, col2 = st.columns([1, 5])
with col1:
    st.image(logo, use_container_width=False, width=100)
with col2:
    st.markdown(
        "<h1 style='color: #112E4D; padding-top: 15px;'>RtR GEOGRAPHICAL PRESENCE TOOL</h1>",
        unsafe_allow_html=True
    )

apply_custom_style()

st.info("""
Use this tool to report the countries where your initiative is active.

**Two ways to select countries:**
- Select by **continent** (guided)
- Select by **typing country names** directly

Paste your final list into the RtR reporting tool, following the instructions provided.
""")

# --- MODE SWITCH ---
mode = st.radio("How do you want to select countries?", ["By continent", "By country name directly"])

selected_country_names = []

# --- MODE 1: BY CONTINENT ---
if mode == "By continent":
    selected_continents = st.multiselect("🌍 Select continents:", options=list(continents.keys()))
    for continent in selected_continents:
        st.subheader(f"🌐 {continent}")
        codes = continents.get(continent, [])
        names = [countries[code] for code in codes if code in countries]
        selected = st.multiselect(f"Select countries in {continent}:", options=names, key=continent)
        selected_country_names.extend(selected)

# --- MODE 2: DIRECT COUNTRY SELECTION ---
else:
    selected_country_names = st.multiselect("🔎 Type to select countries:", options=country_list)

# --- OUTPUT ---
if selected_country_names:
    unique_sorted = sorted(set(selected_country_names))
    result_string = ";".join(unique_sorted)

    st.success("✅ Copy this line and paste it into the RtR reporting tool:")
    st.text_area("Your country list:", result_string, height=100)

    txt_data = io.StringIO(result_string)
    st.download_button(
        label="💾 Download as .txt",
        data=txt_data.getvalue(),
        file_name="geographical_presence.txt",
        mime="text/plain"
    )
else:
    st.warning("Please select at least one country.")

# --- FOOTER ---
# st.markdown("---")
# st.markdown(
#     "<small>Need help? Contact:<br>"
#     "**Francis Mason** (francismason@climatechampions.team)<br>"
#     "**Laura Ramajo** (lauraramajo@climatechampions.team)</small>",
#     unsafe_allow_html=True
# )
