import streamlit as st
import requests

def fetch_country_data(country_name):
    url = f"https://restcountries.com/v3.1/name/{country_name}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        country_data = data[0]
        name = country_data["name"]["common"]
        capital = country_data["capital"][0]
        population = country_data["population"]
        area = country_data["area"]
        currency = country_data["currencies"]
        region = country_data["region"]
        return name, capital, population, area, currency, region
    else:
        return None
    
def main():
    # Set page config
    st.set_page_config(page_title="🌍 Country Explorer", page_icon="🌍", layout="centered")
    
    # Title and header
    st.title("🌍 Country Explorer")
    st.markdown("Discover interesting facts about countries around the world")
    
    # Search input
    country_name = st.text_input("🔍 Enter a country name:", placeholder="e.g., France, Japan, Brazil...")
    
    if country_name:
        country_info = fetch_country_data(country_name)
        if country_info:
            name, capital, population, area, currency, region = country_info
            
            # Format currency
            currency_info = ""
            for curr_code, curr_data in currency.items():
                currency_info += f"{curr_data['name']} ({curr_code}) - {curr_data['symbol']}"
            
            # Create columns for better layout
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader(name)
                st.write(f"🏛️Capital:{capital}")
                st.write(f"🌍 Region:{region}")
                st.write(f"👥 Population: {population:,}")
            
            with col2:
                st.write(f"📏 Area: {area:,} km²")
                st.write(f"💰 Currency:{currency_info}")
        else:
            st.error("❌ Country not found. Please check the spelling and try again.")

if __name__ == "__main__":
    main()

