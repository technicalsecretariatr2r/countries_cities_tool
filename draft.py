
def country_selector():
# Generate a list of all country names using pycountry
    countries = [country.name for country in pycountry.countries]

    # Streamlit Multiselect for Countries
    st.title("Country Selector")
    selected_countries = st.multiselect(
        "Select countries:",
        options=countries,
        default=[]
    )

    # Display Selected Countries
    if selected_countries:
        st.subheader("You selected:")
        st.write(", ".join(selected_countries))
    else:
        st.write("No countries selected.")
country_selector()
