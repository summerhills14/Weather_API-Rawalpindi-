import streamlit as st
import requests
from datetime import datetime
from pathlib import Path


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Rawalpindi Weather Dashboard",
    page_icon="🌤️",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ==========================================
# CUSTOM CSS - PURPLE GLASS THEME
# ==========================================

st.markdown("""
<style>

/* Main Background */
.stApp {
    background: linear-gradient(
        135deg,
        #17103f 0%,
        #30215f 45%,
        #703e78 100%
    );
    color: white;
}

/* Remove default Streamlit spacing */
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1500px;
}

/* Hide Streamlit default menu */
#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    background: transparent !important;
}


/* ==========================================
   HEADER
========================================== */

.main-title {
    text-align: center;
    font-size: 3.2rem;
    font-weight: 800;
    color: #f5f3ff;
    margin-top: 10px;
    margin-bottom: 5px;
}

.subtitle {
    text-align: center;
    font-size: 1.1rem;
    color: #ddd6fe;
    margin-bottom: 35px;
}


/* ==========================================
   REFRESH BUTTON
========================================== */

.stButton > button {
    background: rgba(255, 255, 255, 0.95);
    color: #38275c;
    border: none;
    border-radius: 10px;
    padding: 12px 22px;
    font-size: 16px;
    font-weight: 600;
    transition: 0.3s;
    box-shadow: 0 4px 12px rgba(0,0,0,0.2);
}

.stButton > button:hover {
    background: #ffffff;
    transform: translateY(-2px);
    color: #6d3d7c;
}


/* ==========================================
   METRIC CARDS
========================================== */

.metric-card {
    background: linear-gradient(
        135deg,
        rgba(255,255,255,0.12),
        rgba(255,255,255,0.06)
    );

    border: 1px solid rgba(255,255,255,0.10);

    border-radius: 15px;

    padding: 30px 20px;

    text-align: center;

    min-height: 150px;

    backdrop-filter: blur(10px);

    box-shadow: 0 8px 25px rgba(0,0,0,0.15);

    transition: 0.3s;
}

.metric-card:hover {
    transform: translateY(-5px);

    background: linear-gradient(
        135deg,
        rgba(255,255,255,0.18),
        rgba(255,255,255,0.10)
    );
}

.metric-icon {
    font-size: 2.3rem;
    margin-bottom: 8px;
}

.metric-title {
    color: #f1eaff;
    font-size: 1.1rem;
    font-weight: 600;
    margin-bottom: 10px;
}

.metric-value {
    color: white;
    font-size: 2.4rem;
    font-weight: 700;
}


/* ==========================================
   INFORMATION CARDS
========================================== */

.info-card {
    background: linear-gradient(
        135deg,
        rgba(255,255,255,0.12),
        rgba(255,255,255,0.06)
    );

    border: 1px solid rgba(255,255,255,0.10);

    border-radius: 15px;

    padding: 30px;

    min-height: 280px;

    backdrop-filter: blur(10px);

    box-shadow: 0 8px 25px rgba(0,0,0,0.15);
}

.card-title {
    color: #f5f3ff;
    font-size: 1.5rem;
    font-weight: 700;
    margin-bottom: 25px;
}

.weather-description {
    text-align: center;
    font-size: 2rem;
    font-weight: 700;
    color: white;
    margin-top: 20px;
}

.big-weather-icon {
    text-align: center;
    font-size: 6rem;
    margin-top: 20px;
}


/* ==========================================
   ADDITIONAL INFORMATION
========================================== */

.info-text {
    font-size: 1.2rem;
    color: #f3e8ff;
    margin-top: 25px;
}

.info-text b {
    color: white;
}

.divider {
    border-top: 1px solid rgba(255,255,255,0.2);
    margin: 25px 0;
}


/* ==========================================
   HORIZONTAL LINE
========================================== */

hr {
    border: none;
    height: 1px;
    background: rgba(255,255,255,0.25);
    margin: 30px 0;
}


/* ==========================================
   FOOTER
========================================== */

.footer {
    text-align: center;
    color: #f1eaff;
    font-size: 1rem;
    font-weight: 500;
    padding: 10px;
}


/* Streamlit error styling */
.stAlert {
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)


# ==========================================
# LOAD API KEY
# ==========================================

def load_api_key():
    try:
        base_dir = Path(__file__).resolve().parent
        api_path = base_dir / "api_key.txt"

        with open("api_key.txt", "r") as file:
            return  file.read().strip()

    except FileNotFoundError:
        st.error("❌ API key file not found!")
        return None


API_KEY = load_api_key()


# ==========================================
# GET WEATHER DATA
# ==========================================

def get_weather():

    if not API_KEY:
        return None

    url = "https://api.openweathermap.org/data/2.5/weather"

    params = {
        "q": "Rawalpindi,PK",
        "appid": API_KEY,
        "units": "metric"
    }

    try:
        response = requests.get(
            url,
            params=params,
            timeout=10
        )

        if response.status_code == 200:
            return response.json()

        else:
            st.error(
                f"Unable to fetch weather data. "
                f"Status Code: {response.status_code}"
            )
            return None

    except requests.exceptions.RequestException as e:
        st.error(f"Connection Error: {e}")
        return None


# ==========================================
# HEADER
# ==========================================

st.markdown(
    """
    <div class="main-title">
        🌤️ Rawalpindi Weather Dashboard
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="subtitle">
        Live Weather Information using API
    </div>
    """,
    unsafe_allow_html=True
)


# ==========================================
# REFRESH BUTTON
# ==========================================

refresh = st.button("🔄 Refresh Weather")


# ==========================================
# FETCH WEATHER
# ==========================================

if API_KEY:

    with st.spinner("Fetching latest weather data..."):
        weather = get_weather()


    if weather:

        # Extract data
        temperature = weather["main"]["temp"]
        feels_like = weather["main"]["feels_like"]
        humidity = weather["main"]["humidity"]
        pressure = weather["main"]["pressure"]

        wind_speed = weather["wind"]["speed"]

        description = weather["weather"][0]["description"].title()

        icon = weather["weather"][0]["icon"]


        # ==========================================
        # WEATHER METRIC CARDS
        # ==========================================

        col1, col2, col3, col4 = st.columns(4)


        with col1:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-icon">🌡️</div>
                    <div class="metric-title">Temperature</div>
                    <div class="metric-value">{temperature:.1f} °C</div>
                </div>
                """,
                unsafe_allow_html=True
            )


        with col2:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-icon">🤔</div>
                    <div class="metric-title">Feels Like</div>
                    <div class="metric-value">{feels_like:.1f} °C</div>
                </div>
                """,
                unsafe_allow_html=True
            )


        with col3:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-icon">💧</div>
                    <div class="metric-title">Humidity</div>
                    <div class="metric-value">{humidity}%</div>
                </div>
                """,
                unsafe_allow_html=True
            )


        with col4:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-icon">💨</div>
                    <div class="metric-title">Wind Speed</div>
                    <div class="metric-value">{wind_speed:.1f} m/s</div>
                </div>
                """,
                unsafe_allow_html=True
            )


        # Divider
        st.markdown("<hr>", unsafe_allow_html=True)


        # ==========================================
        # BOTTOM INFORMATION CARDS
        # ==========================================

        left, right = st.columns(2)


        # WEATHER CONDITION CARD
        with left:
            weather_emoji = "🌤️"

            st.markdown(f"""
        <div class="info-card">

        <div class="card-title">
        🌤️ Weather Condition
        </div>

        <div class="weather-description">
        {description}
        </div>

        <div class="big-weather-icon">
        {weather_emoji}
        </div>

        </div>
        """, unsafe_allow_html=True)


        # ADDITIONAL INFORMATION
        with right:
            current_time = datetime.now().strftime(
                "%d %B %Y | %I:%M %p"
            )

            st.markdown(f"""
        <div class="info-card">

        <div class="card-title">
        📊 Additional Information
        </div>

        <div class="info-text">
        <b>Pressure:</b> {pressure} hPa
        </div>

        <div class="divider"></div>

        <div class="info-text">
        <b>Last Updated:</b> {current_time}
        </div>

        </div>
        """, unsafe_allow_html=True)

# ==========================================
# FOOTER
# ==========================================

st.markdown("<hr>", unsafe_allow_html=True)

st.markdown(
    """
    <div class="footer">
        Made with ❤️ using Streamlit | Rawalpindi Weather App
    </div>
    """,
    unsafe_allow_html=True
)