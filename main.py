import streamlit as st
import google.generativeai as genai
import matplotlib.pyplot as plt
import numpy as np
import os

# Load the API key from Streamlit secrets or environment variables
api_key = st.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")

# Initialize Gemini
if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.0-flash')
else:
    st.error("API key not found. Please set the GEMINI_API_KEY in Streamlit secrets or environment variables.")
    st.stop()

# Define conversion functions for all categories
def convert_length(value, from_unit, to_unit):
    length_conversions = {
        'meter': 1.0,
        'kilometer': 1000.0,
        'centimeter': 0.01,
        'millimeter': 0.001,
        'mile': 1609.34,
        'yard': 0.9144,
        'foot': 0.3048,
        'inch': 0.0254
    }
    return value * length_conversions[from_unit] / length_conversions[to_unit]

def convert_mass(value, from_unit, to_unit):
    mass_conversions = {
        'kilogram': 1.0,
        'gram': 0.001,
        'milligram': 0.000001,
        'pound': 0.453592,
        'ounce': 0.0283495
    }
    return value * mass_conversions[from_unit] / mass_conversions[to_unit]

def convert_temperature(value, from_unit, to_unit):
    if from_unit == 'celsius' and to_unit == 'fahrenheit':
        return (value * 9/5) + 32
    elif from_unit == 'fahrenheit' and to_unit == 'celsius':
        return (value - 32) * 5/9
    elif from_unit == 'celsius' and to_unit == 'kelvin':
        return value + 273.15
    elif from_unit == 'kelvin' and to_unit == 'celsius':
        return value - 273.15
    elif from_unit == 'fahrenheit' and to_unit == 'kelvin':
        return (value - 32) * 5/9 + 273.15
    elif from_unit == 'kelvin' and to_unit == 'fahrenheit':
        return (value - 273.15) * 9/5 + 32
    else:
        return value

def convert_time(value, from_unit, to_unit):
    time_conversions = {
        'second': 1.0,
        'millisecond': 0.001,
        'minute': 60.0,
        'hour': 3600.0,
        'day': 86400.0,
        'week': 604800.0,
        'month': 2629800.0,
        'year': 31557600.0
    }
    return value * time_conversions[from_unit] / time_conversions[to_unit]

def convert_volume(value, from_unit, to_unit):
    volume_conversions = {
        'liter': 1.0,
        'milliliter': 0.001,
        'gallon': 3.78541,
        'quart': 0.946353,
        'pint': 0.473176,
        'cup': 0.24,
        'tablespoon': 0.0147868,
        'teaspoon': 0.00492892
    }
    return value * volume_conversions[from_unit] / volume_conversions[to_unit]

def convert_data_transfer_rate(value, from_unit, to_unit):
    data_transfer_rate_conversions = {
        'bit per second': 1.0,
        'kilobit per second': 1000.0,
        'megabit per second': 1000000.0,
        'gigabit per second': 1000000000.0,
        'byte per second': 8.0,
        'kilobyte per second': 8000.0,
        'megabyte per second': 8000000.0,
        'gigabyte per second': 8000000000.0
    }
    return value * data_transfer_rate_conversions[from_unit] / data_transfer_rate_conversions[to_unit]

def convert_digital_storage(value, from_unit, to_unit):
    digital_storage_conversions = {
        'bit': 1.0,
        'byte': 8.0,
        'kilobyte': 8192.0,
        'megabyte': 8388608.0,
        'gigabyte': 8589934592.0,
        'terabyte': 8796093022208.0
    }
    return value * digital_storage_conversions[from_unit] / digital_storage_conversions[to_unit]

def convert_energy(value, from_unit, to_unit):
    energy_conversions = {
        'joule': 1.0,
        'kilojoule': 1000.0,
        'calorie': 4.184,
        'kilocalorie': 4184.0,
        'watt-hour': 3600.0,
        'kilowatt-hour': 3600000.0
    }
    return value * energy_conversions[from_unit] / energy_conversions[to_unit]

def convert_frequency(value, from_unit, to_unit):
    frequency_conversions = {
        'hertz': 1.0,
        'kilohertz': 1000.0,
        'megahertz': 1000000.0,
        'gigahertz': 1000000000.0
    }
    return value * frequency_conversions[from_unit] / frequency_conversions[to_unit]

def convert_fuel_economy(value, from_unit, to_unit):
    fuel_economy_conversions = {
        'miles per gallon': 1.0,
        'kilometers per liter': 0.425144,
        'liters per 100 kilometers': 235.214583
    }
    return value * fuel_economy_conversions[from_unit] / fuel_economy_conversions[to_unit]

def convert_plane_angle(value, from_unit, to_unit):
    plane_angle_conversions = {
        'degree': 1.0,
        'radian': 57.2958,
        'gradian': 0.9
    }
    return value * plane_angle_conversions[from_unit] / plane_angle_conversions[to_unit]

def convert_pressure(value, from_unit, to_unit):
    pressure_conversions = {
        'pascal': 1.0,
        'kilopascal': 1000.0,
        'bar': 100000.0,
        'psi': 6894.76
    }
    return value * pressure_conversions[from_unit] / pressure_conversions[to_unit]

def convert_speed(value, from_unit, to_unit):
    speed_conversions = {
        'meter per second': 1.0,
        'kilometer per hour': 0.277778,
        'mile per hour': 0.44704,
        'knot': 0.514444
    }
    return value * speed_conversions[from_unit] / speed_conversions[to_unit]

# Streamlit app
st.set_page_config(page_title="Unit Converter", page_icon="📏", layout="centered")

# Custom CSS with dark theme
st.markdown(
    """
    <style>
    /* Dark background for the entire app */
    body {
        background-color: 	#000000;
        color: #000000;
        font-family: 'Arial', sans-serif;
    }

    /* Main container */
    .main {
        max-width: 800px;
        margin: auto;
        padding: 2rem;
        border-radius: 1rem;
        background: rgba(18, 18, 18, 0.9);
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        border: 1px solid rgba(255, 255, 255, 0.18);
    }

    /* Title */
    .title {
        font-size: 2.5rem;
        font-weight: 700;
        color: #000000;
        text-align: center;
        margin-bottom: 1.5rem;
    }

    /* Description */
    .description {
        font-size: 1.1rem;
        color: rgba(0, 0, 0, 0.8);
;
        text-align: center;
        margin-bottom: 2rem;
    }

    /* Input fields */
    .stNumberInput, .stSelectbox {
        width: 100% !important;
        margin-bottom: 1rem;
        background: rgba(255, 255, 255, 0.1);
        border: none;
        border-radius: 0.5rem;
        padding: 0.75rem;
        color: black;
    }

    /* Button */
    .stButton button {
        width: 100%;
        background: linear-gradient(135deg, #6a11cb, #2575fc);
        color: black;
        font-size: 1rem;
        font-weight: 600;
        padding: 0.75rem;
        border-radius: 0.5rem;
        border: none;
        transition: background 0.3s ease;
    }
    .stButton button:hover {
        background: linear-gradient(135deg, #2575fc, #6a11cb);
    }

    /* Result display */
    .result {
        font-size: 2.5rem;
        font-weight: 700;
        color: black;
        text-align: center;
        margin-top: 2rem;
        margin-bottom: 2rem;
    }

    /* Explanation box */
    .explanation {
        font-size: 1rem;
        color: black;
        margin-top: 1.5rem;
        padding: 1.5rem;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 0.5rem;
        backdrop-filter: blur(10px);
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.18);
    }

    /* Footer */
    .footer {
        font-size: 0.875rem;
        color: color: rgba(0, 0, 0, 0.8);
;
        text-align: center;
        margin-top: 2rem;
    }

    /* Graph container */
    .graph-container {
        margin-top: 2rem;
        padding: 1.5rem;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 0.5rem;
        backdrop-filter: blur(10px);
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.18);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Main container
st.markdown('<div class="main">', unsafe_allow_html=True)

# Title and description
st.markdown('<div class="title">📏 Advanced Unit Converter</div>', unsafe_allow_html=True)
st.markdown('<div class="description">Convert units instantly with a clean and modern design!</div>', unsafe_allow_html=True)

# Input fields in a clean layout
col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    value = st.number_input("Enter value", value=1.0, step=0.1, format="%.2f")

with col2:
    category = st.selectbox("Category", [
        "Data Transfer Rate", "Digital Storage", "Energy", "Frequency", "Fuel Economy",
        "Length", "Mass", "Plane Angle", "Pressure", "Speed", "Temperature", "Time", "Volume"
    ])
    if category == "Data Transfer Rate":
        units = ["bit per second", "kilobit per second", "megabit per second", "gigabit per second",
                 "byte per second", "kilobyte per second", "megabyte per second", "gigabyte per second"]
    elif category == "Digital Storage":
        units = ["bit", "byte", "kilobyte", "megabyte", "gigabyte", "terabyte"]
    elif category == "Energy":
        units = ["joule", "kilojoule", "calorie", "kilocalorie", "watt-hour", "kilowatt-hour"]
    elif category == "Frequency":
        units = ["hertz", "kilohertz", "megahertz", "gigahertz"]
    elif category == "Fuel Economy":
        units = ["miles per gallon", "kilometers per liter", "liters per 100 kilometers"]
    elif category == "Length":
        units = ["meter", "kilometer", "centimeter", "millimeter", "mile", "yard", "foot", "inch"]
    elif category == "Mass":
        units = ["kilogram", "gram", "milligram", "pound", "ounce"]
    elif category == "Plane Angle":
        units = ["degree", "radian", "gradian"]
    elif category == "Pressure":
        units = ["pascal", "kilopascal", "bar", "psi"]
    elif category == "Speed":
        units = ["meter per second", "kilometer per hour", "mile per hour", "knot"]
    elif category == "Temperature":
        units = ["celsius", "fahrenheit", "kelvin"]
    elif category == "Time":
        units = ["second", "millisecond", "minute", "hour", "day", "week", "month", "year"]
    elif category == "Volume":
        units = ["liter", "milliliter", "gallon", "quart", "pint", "cup", "tablespoon", "teaspoon"]

with col3:
    from_unit = st.selectbox("From", units)
    to_unit = st.selectbox("To", units)

# Perform conversion
if category == "Data Transfer Rate":
    result = convert_data_transfer_rate(value, from_unit, to_unit)
elif category == "Digital Storage":
    result = convert_digital_storage(value, from_unit, to_unit)
elif category == "Energy":
    result = convert_energy(value, from_unit, to_unit)
elif category == "Frequency":
    result = convert_frequency(value, from_unit, to_unit)
elif category == "Fuel Economy":
    result = convert_fuel_economy(value, from_unit, to_unit)
elif category == "Length":
    result = convert_length(value, from_unit, to_unit)
elif category == "Mass":
    result = convert_mass(value, from_unit, to_unit)
elif category == "Plane Angle":
    result = convert_plane_angle(value, from_unit, to_unit)
elif category == "Pressure":
    result = convert_pressure(value, from_unit, to_unit)
elif category == "Speed":
    result = convert_speed(value, from_unit, to_unit)
elif category == "Temperature":
    result = convert_temperature(value, from_unit, to_unit)
elif category == "Time":
    result = convert_time(value, from_unit, to_unit)
elif category == "Volume":
    result = convert_volume(value, from_unit, to_unit)
else:
    result = "Unsupported conversion"

# Display the result in a large and prominent way
st.markdown(f'<div class="result">Converted value: <strong>{result:.2f}</strong></div>', unsafe_allow_html=True)

# Use Gemini to generate a response
if st.button("Explain Conversion"):
    prompt = f"Explain the conversion of {value} {from_unit} to {to_unit}. The result is {result}."
    response = model.generate_content(prompt)
    st.markdown(f'<div class="explanation"><strong>Gemini Explanation:</strong><br>{response.text}</div>', unsafe_allow_html=True)

# Add a graph for visualization
st.markdown('<div class="graph-container">', unsafe_allow_html=True)
st.markdown("### 📊 Conversion Visualization")

# Generate graph based on category
x = np.linspace(0, 100, 100)  # X-axis range
if category == "Temperature":
    if from_unit == "celsius" and to_unit == "fahrenheit":
        y = (x * 9/5) + 32
    elif from_unit == "fahrenheit" and to_unit == "celsius":
        y = (x - 32) * 5/9
    elif from_unit == "celsius" and to_unit == "kelvin":
        y = x + 273.15
    elif from_unit == "kelvin" and to_unit == "celsius":
        y = x - 273.15
    elif from_unit == "fahrenheit" and to_unit == "kelvin":
        y = (x - 32) * 5/9 + 273.15
    elif from_unit == "kelvin" and to_unit == "fahrenheit":
        y = (x - 273.15) * 9/5 + 32
    else:
        y = x
elif category == "Length":
    y = convert_length(x, from_unit, to_unit)
elif category == "Mass":
    y = convert_mass(x, from_unit, to_unit)
elif category == "Time":
    y = convert_time(x, from_unit, to_unit)
elif category == "Volume":
    y = convert_volume(x, from_unit, to_unit)
elif category == "Data Transfer Rate":
    y = convert_data_transfer_rate(x, from_unit, to_unit)
elif category == "Digital Storage":
    y = convert_digital_storage(x, from_unit, to_unit)
elif category == "Energy":
    y = convert_energy(x, from_unit, to_unit)
elif category == "Frequency":
    y = convert_frequency(x, from_unit, to_unit)
elif category == "Fuel Economy":
    y = convert_fuel_economy(x, from_unit, to_unit)
elif category == "Plane Angle":
    y = convert_plane_angle(x, from_unit, to_unit)
elif category == "Pressure":
    y = convert_pressure(x, from_unit, to_unit)
elif category == "Speed":
    y = convert_speed(x, from_unit, to_unit)
else:
    y = x

# Plot the graph with advanced styling
fig, ax = plt.subplots(figsize=(10, 6))

# Plot the main line
ax.plot(x, y, label=f"{from_unit} to {to_unit}", color='#6a11cb', linewidth=2.5)

# Highlight the converted value
ax.scatter(value, result, color="red", s=100, label="Converted Value", zorder=5)

# Add grid lines
ax.grid(True, linestyle='--', alpha=0.7)

# Add annotations
ax.annotate(f'{result:.2f} {to_unit}', xy=(value, result), xytext=(value + 5, result + 5),
            arrowprops=dict(facecolor='red', shrink=0.05), fontsize=12, color='red')

# Set labels and title with better styling
ax.set_xlabel(f"{from_unit}", fontsize=14, fontweight='bold', color='#000000')
ax.set_ylabel(f"{to_unit}", fontsize=14, fontweight='bold', color='#000000')
ax.set_title(f"{from_unit} to {to_unit} Conversion", fontsize=16, fontweight='bold', color='#000000')

# Customize the legend
ax.legend(loc='upper left', fontsize=12, framealpha=0.9)

# Customize the ticks
ax.tick_params(axis='both', which='major', labelsize=12, colors='#000000')

# Add a background color to the plot
ax.set_facecolor('#1e1e1e')

# Remove top and right spines
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# Add a subtle shadow to the plot
for spine in ax.spines.values():
    spine.set_edgecolor('#000000')
    spine.set_linewidth(1.5)

# Display the plot in Streamlit
st.pyplot(fig)

st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown('<div class="footer">Made by ❤️ Muhammad Hamza</div>', unsafe_allow_html=True)

# Close main container
st.markdown('</div>', unsafe_allow_html=True)