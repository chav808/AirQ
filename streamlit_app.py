import streamlit as st
import requests
from streamlit_folium import folium_static
import folium
import plotly.express as px

api_key = "3841c728-6af6-4ad7-8036-6b1c48ebe288"

st.title("Weather and Air Quality Web App")
st.header("Streamlit and AirVisual API")

@st.cache
def generate_list_of_countries():
    countries_url = f"https://api.airvisual.com/v2/countries?key={api_key}"
    countries_dict = requests.get(countries_url).json()
    return countries_dict

@st.cache
def generate_list_of_states(country_selected):
    states_url = f"https://api.airvisual.com/v2/states?country={country_selected}&key={api_key}"
    states_dict = requests.get(states_url).json()
    return states_dict

@st.cache
def generate_list_of_cities(state_selected, country_selected):
    cities_url = f"https://api.airvisual.com/v2/cities?state={state_selected}&country={country_selected}&key={api_key}"
    cities_dict = requests.get(cities_url).json()
    return cities_dict

@st.cache
def fetch_weather_and_air_quality(city_selected, state_selected, country_selected):
    aqi_data_url = f"https://api.airvisual.com/v2/city?city={city_selected}&state={state_selected}&country={country_selected}&key={api_key}"
    aqi_data_dict = requests.get(aqi_data_url).json()
    return aqi_data_dict

def display_map(latitude, longitude):
    m = folium.Map(location=[latitude, longitude], zoom_start=10)
    folium.Marker([latitude, longitude], popup="Selected Location", tooltip="Selected Location").add_to(m)
    folium_static(m)

# Sidebar selection for location method
category = st.selectbox("Select Location Method", ["By City, State, and Country", "By Nearest City (IP Address)", "By Latitude and Longitude"])

if category == "By City, State, and Country":
    countries_dict = generate_list_of_countries()
    if countries_dict["status"] == "success":
        countries_list = [country["country"] for country in countries_dict["data"]]
        countries_list.insert(0, "")

        country_selected = st.selectbox("Select a country", countries_list)
        if country_selected:
            states_dict = generate_list_of_states(country_selected)
            if states_dict["status"] == "success":
                states_list = [state["state"] for state in states_dict["data"]]
                states_list.insert(0, "")

                state_selected = st.selectbox("Select a state", states_list)
                if state_selected:
                    cities_dict = generate_list_of_cities(state_selected, country_selected)
                    if cities_dict["status"] == "success":
                        cities_list = [city["city"] for city in cities_dict["data"]]
                        cities_list.insert(0, "")

                        city_selected = st.selectbox("Select a city", cities_list)
                        if city_selected:
                            aqi_data = fetch_weather_and_air_quality(city_selected, state_selected, country_selected)
                            if aqi_data["status"] == "success":
                                st.subheader(f"Weather and Air Quality Information for {city_selected}, {state_selected}, {country_selected}")
                                st.write(f"Temperature: {aqi_data['data']['current']['weather']['tp']} °C")
                                st.write(f"Humidity: {aqi_data['data']['current']['weather']['hu']} %")
                                st.write(f"AQI (Air Quality Index): {aqi_data['data']['current']['pollution']['aqius']}")
                                st.write(f"Main Pollutant: {aqi_data['data']['current']['pollution']['mainus']}")
                                st.write(f"Pollutant Concentration: {aqi_data['data']['current']['pollution']['concus']}")
                                st.write(f"Time of Measurement: {aqi_data['data']['current']['pollution']['ts']}")
                                st.write("Location on Map:")
                                display_map(aqi_data['data']['location']['coordinates'][1], aqi_data['data']['location']['coordinates'][0])
                            else:
                                st.warning("No data available for this location.")
                    else:
                        st.warning("No cities available for the selected state and country.")
            else:
                st.warning("No states available for the selected country.")
    else:
        st.error("Failed to fetch countries. Please try again later.")

elif category == "By Nearest City (IP Address)":
    nearest_city_url = f"https://api.airvisual.com/v2/nearest_city?key={api_key}"
    nearest_city_data = requests.get(nearest_city_url).json()
    if nearest_city_data["status"] == "success":
        st.subheader("Weather and Air Quality Information for Nearest City")
        st.write(f"City: {nearest_city_data['data']['city']}")
        st.write(f"State: {nearest_city_data['data']['state']}")
        st.write(f"Country: {nearest_city_data['data']['country']}")
        st.write(f"Temperature: {nearest_city_data['data']['current']['weather']['tp']} °C")
        st.write(f"Humidity: {nearest_city_data['data']['current']['weather']['hu']} %")
        st.write(f"AQI (Air Quality Index): {nearest_city_data['data']['current']['pollution']['aqius']}")
        st.write(f"Main Pollutant: {nearest_city_data['data']['current']['pollution']['mainus']}")
        st.write(f"Pollutant Concentration: {nearest_city_data['data']['current']['pollution']['concus']}")
        st.write(f"Time of Measurement: {nearest_city_data['data']['current']['pollution']['ts']}")
        st.write("Location on Map:")
        display_map(nearest_city_data['data']['location']['coordinates'][1], nearest_city_data['data']['location']['coordinates'][0])
    else:
        st.warning("No data available for the nearest city.")

elif category == "By Latitude and Longitude":
    latitude = st.text_input("Enter Latitude")
    longitude = st.text_input("Enter Longitude")
    if latitude and longitude:
        lat = float(latitude)
        lon = float(longitude)
        lat_lon_url = f"https://api.airvisual.com/v2/nearest_city?lat={lat}&lon={lon}&key={api_key}"
        lat_lon_data = requests.get(lat_lon_url).json()
        if lat_lon_data["status"] == "success":
            st.subheader("Weather and Air Quality Information for Specified Coordinates")
            st.write(f"Latitude: {lat}")
            st.write(f"Longitude: {lon}")
            st.write(f"City: {lat_lon_data['data']['city']}")
            st.write(f"State: {lat_lon_data['data']['state']}")
            st.write(f"Country: {lat_lon_data['data']['country']}")
            st.write(f"Temperature: {lat_lon_data['data']['current']['weather']['tp']} °C")
            st.write(f"Humidity: {lat_lon_data['data']['current']['weather']['hu']} %")
            st.write(f"AQI (Air Quality Index): {lat_lon_data['data']['current']['pollution']['aqius']}")
            st.write(f"Main Pollutant: {lat_lon_data['data']['current']['pollution']['mainus']}")
            st.write(f"Pollutant Concentration: {lat_lon_data['data']['current']['pollution']['concus']}")
            st.write(f"Time of Measurement: {lat_lon_data['data']['current']['pollution']['ts']}")
            st.write("Location on Map:")
            display_map(lat_lon_data['data']['location']['coordinates'][1], lat_lon_data['data']['location']['coordinates'][0])
        else:
            st.warning("No data available for the specified coordinates.")
