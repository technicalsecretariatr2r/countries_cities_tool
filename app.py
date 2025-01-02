import streamlit as st
import pycountry
from geonamescache import GeonamesCache
import pandas as pd
import io

# Initialize GeonamesCache for cities
gc = GeonamesCache()

# Generate a list of all country names using pycountry
countries = {country.alpha_2: country.name for country in pycountry.countries}

# Map of continents and their respective countries
continents = {
    "Africa": ["DZ", "EG", "LY", "MA", "SD", "TN", "AO", "BF", "BI", "BJ", "BW", "CD", "CF", "CG", "CI", "CM", "DJ", "ER", "ET", "GA", "GH", "GM", "GN", "GQ", "KE", "KM", "LR", "LS", "MG", "ML", "MR", "MU", "MW", "MZ", "NA", "NE", "NG", "RW", "SC", "SL", "SN", "SO", "SS", "ST", "SZ", "TD", "TG", "TZ", "UG", "ZA", "ZM", "ZW"],
    "Americas": ["AR", "BO", "BR", "CL", "CO", "CR", "CU", "DO", "EC", "GT", "HN", "HT", "JM", "MX", "NI", "PA", "PE", "PY", "SV", "TT", "UY", "VE", "CA", "US"],
    "Asia": ["KZ", "KG", "TJ", "TM", "UZ", "CN", "JP", "KP", "KR", "MN", "TW", "AF", "BD", "BT", "IN", "IR", "LK", "MV", "NP", "PK", "BN", "KH", "ID", "LA", "MY", "MM", "PH", "SG", "TH", "TL", "VN", "AM", "AZ", "BH", "CY", "GE", "IQ", "IL", "JO", "KW", "LB", "OM", "QA", "SA", "SY", "TR", "AE", "YE"],
    "Europe": ["BY", "BG", "CZ", "HU", "MD", "PL", "RO", "RU", "SK", "UA", "DK", "EE", "FI", "IS", "IE", "LV", "LT", "NO", "SE", "GB", "AL", "AD", "BA", "HR", "GR", "IT", "MT", "ME", "PT", "SM", "RS", "SI", "ES", "VA", "AT", "BE", "FR", "DE", "LI", "LU", "MC", "NL", "CH"],
    "Oceania": ["AU", "NZ", "FJ", "NC", "PG", "SB", "VU", "FM", "GU", "KI", "MH", "NR", "PW", "AS", "CK", "NU", "PF", "PN", "WS", "TO", "TV"]
}

regions_to_countries = {
    "Northern Africa": ["DZ", "EG", "LY", "MA", "SD", "TN"],
    "Sub-Saharan Africa": [
        "AO", "BF", "BI", "BJ", "BW", "CD", "CF", "CG", "CI", "CM", "DJ", "ER", "ET",
        "GA", "GH", "GM", "GN", "GQ", "KE", "KM", "LR", "LS", "MG", "ML", "MR", "MU",
        "MW", "MZ", "NA", "NE", "NG", "RW", "SC", "SL", "SN", "SO", "SS", "ST", "SZ",
        "TD", "TG", "TZ", "UG", "ZA", "ZM", "ZW"
    ],
    "Latin America and the Caribbean": [
        "AR", "BO", "BR", "CL", "CO", "CR", "CU", "DO", "EC", "GT", "HN", "HT", "JM", 
        "MX", "NI", "PA", "PE", "PY", "SV", "TT", "UY", "VE"
    ],
    "Northern America": ["CA", "US"],
    "Central Asia": ["KZ", "KG", "TJ", "TM", "UZ"],
    "Eastern Asia": ["CN", "JP", "KP", "KR", "MN", "TW"],
    "Southern Asia": ["AF", "BD", "BT", "IN", "IR", "LK", "MV", "NP", "PK"],
    "Southeastern Asia": ["BN", "KH", "ID", "LA", "MY", "MM", "PH", "SG", "TH", "TL", "VN"],
    "Western Asia": [
        "AM", "AZ", "BH", "CY", "GE", "IQ", "IL", "JO", "KW", "LB", "OM", "QA", "SA", 
        "SY", "TR", "AE", "YE"
    ],
    "Eastern Europe": ["BY", "BG", "CZ", "HU", "MD", "PL", "RO", "RU", "SK", "UA"],
    "Northern Europe": ["DK", "EE", "FI", "IS", "IE", "LV", "LT", "NO", "SE", "GB"],
    "Southern Europe": ["AL", "AD", "BA", "HR", "GR", "IT", "MT", "ME", "PT", "SM", "RS", "SI", "ES", "VA"],
    "Western Europe": ["AT", "BE", "FR", "DE", "LI", "LU", "MC", "NL", "CH"],
    "Australia and New Zealand": ["AU", "NZ"],
    "Melanesia": ["FJ", "NC", "PG", "SB", "VU"],
    "Micronesia": ["FM", "GU", "KI", "MH", "NR", "PW"],
    "Polynesia": ["AS", "CK", "NU", "PF", "PN", "WS", "TO", "TV"]
}


st.title("RtR Global Location Tool")
st.write("""##### Welcome to the RtR Global Location Tool! 
         
##### _This app helps you select geographical locations at various levels—continents, countries, regions, and cities._""")


st.write("##### 1) READ INSTRUCTIONS")
with st.expander("How to Use the RtR Global Location Tool"):

    # Create tabs
    tab1, tab2, tab3 = st.tabs(["Instructions", "Features", "Data Sources"])

    # Tab 1: Instructions
    with tab1:
        st.subheader("How to Use the RtR Global Location Tool")
        st.markdown("""
        Welcome to the **RtR Global Location Tool**! This app helps you select geographical locations at various levels—continents, countries, regions, and cities.

        ### How to Use the App
        1. **Select Continents**: 
        - Use the multiselect dropdown to choose one or more continents.
        2. **Refine by Countries**:
        - Pick specific countries within the selected continents.
        3. **Include City-Level Data (Optional)**:
        - Choose whether to include cities for selected countries. If selected, a list of cities will be available for filtering.
        4. **View Results**:
        - View your selections in a table with a summary of unique continents, regions, countries, and cities.
        5. **Download the Data**:
        - Use the "Download Results as Excel" button to save your selections for further use.
        """)

    # Tab 2: Features
    with tab2:
        st.subheader("Features of the RtR Global Location Tool")
        st.markdown("""
        ### Key Features
        - **Explore Locations**: 
            - Select continents to start exploring.
            - Drill down into specific countries within those continents.
            - Optionally, include cities for a more detailed view.
        - **View Summaries**:
            - Automatically generates a summary of selected locations, including:
                - Unique continents
                - Regions
                - Countries
                - Cities
        - **Download Results**:
            - Save the results as an Excel file with detailed breakdowns and summaries.
        """)

    # Tab 3: Data Sources
    with tab3:
        st.subheader("Data Sources")
        st.markdown("""
        The app utilizes reliable geographical datasets:
        - **Continents and Countries**: Data sourced from [PyCountry](https://pypi.org/project/pycountry/), ensuring up-to-date country codes and names.
        - **Regions**: Defined based on the UN geoscheme for grouping countries by regions.
        - **Cities**: Retrieved from the [GeonamesCache](https://pypi.org/project/geonamescache/) library, which provides a global database of cities.
        """)


# Continent selection
st.write("##### 2) USE SELECTION TOOL ")
selected_continents = st.multiselect("Select all continents:", options=list(continents.keys()))


data = []  # To store the results

if selected_continents:
    # Country selection based on selected continents
    for continent in selected_continents:
        st.write(f"### {continent}")
        available_countries = [countries[code] for code in continents[continent] if code in countries]
        selected_countries = st.multiselect(f"Select countries in {continent}:", options=available_countries)

        # Map selected country names back to alpha-2 codes
        selected_country_codes = [code for code, name in countries.items() if name in selected_countries]

        if selected_countries:
            # Determine the regions for selected countries
            country_to_region = {
                code: region for region, codes in regions_to_countries.items() for code in codes
            }
            selected_regions = [country_to_region.get(code, "Unknown Region") for code in selected_country_codes]

            # Ask if the user wants to add city-level information
            add_city_info = st.radio(f"Do you want to add city-level information for the selected countries in {continent}?", ("Yes", "No"))

            if add_city_info == "Yes":
                # City selection based on selected countries
                def get_cities_for_countries(country_codes):
                    cities = []
                    for city_data in gc.get_cities().values():
                        if city_data["countrycode"] in country_codes:
                            cities.append(city_data["name"])
                    return sorted(set(cities))  # Remove duplicates and sort

                city_options = get_cities_for_countries(selected_country_codes)
                selected_cities = st.multiselect(f"Select cities in the selected countries in {continent}:", options=city_options)

                # Add selected data to the results table
                for country, region in zip(selected_countries, selected_regions):
                    if selected_cities:
                        for city in selected_cities:
                            data.append([continent, region, country, city])
                    else:
                        data.append([continent, region, country, "No Cities Reported"])
            else:
                # Add data without city-level information
                for country, region in zip(selected_countries, selected_regions):
                    data.append([continent, region, country, "No Cities Reported"])





# Display the results as a table
if data:
    df = pd.DataFrame(data, columns=["Continent", "Regions", "Country", "City"])

    # Generate summary data
    summary_data = {
        "Location": [
            "N° Continents", 
            "N° Regions", 
            "N° Countries", 
            "N° Cities"
        ],
        "N°": [
            len(df["Continent"].unique()),  # Number of unique continents
            len(df["Regions"].unique()),   # Number of unique regions
            len(df["Country"].unique()),   # Number of unique countries
            len(df[df["City"] != "No Cities Reported"]["City"].unique())  # Number of unique cities excluding "No Cities Reported"
        ],
        "List": [
            ", ".join(df["Continent"].unique()),  # List of unique continents
            ", ".join(df["Regions"].unique()),    # List of unique regions
            ", ".join(df["Country"].unique()),    # List of unique countries
            ", ".join(df[df["City"] != "No Cities Reported"]["City"].unique())  # List of unique cities excluding "No Cities Reported"
        ]
    }

    summary_df = pd.DataFrame(summary_data, columns=["Location", "N°", "List"])

    # Generate narrative markdown
    st.write("##### 3) Results")
    narrative = f"""
    The initiative includes:
    - **{summary_data['N°'][0]} continents**: {summary_data['List'][0]}.
    - **{summary_data['N°'][1]} regions**: {summary_data['List'][1]}.
    - **{summary_data['N°'][2]} countries**: {summary_data['List'][2]}.
    - **{summary_data['N°'][3]} cities**: {summary_data['List'][3]}.
    """
    st.info(narrative)
    
    # Add functionality to download the results as an Excel file
    def to_excel(summary_df, df):
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            summary_df.to_excel(writer, sheet_name="Summary", index=False)
            df.to_excel(writer, sheet_name="Locations", index=False)
        return output.getvalue()

    excel_data = to_excel(summary_df, df)

    st.download_button(
        label="Download Results as Excel",
        data=excel_data,
        file_name="results.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    
    st.write("#### Summary Table")
    st.dataframe(summary_df)

    st.write("#### Selected Locations")
    st.dataframe(df)
    
else:
    st.write("No selections made yet.")
