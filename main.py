import streamlit as st
import google.generativeai as genai
import matplotlib.pyplot as plt
import numpy as np
import os

# Load API key
api_key = st.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")

# Initialize Gemini
if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.0-flash')
else:
    st.error("API key not found. Please set the GEMINI_API_KEY in Streamlit secrets or environment variables.")
    st.stop()

# Conversion functions
def convert_length(value, from_unit, to_unit):
    units = {'meter': 1.0, 'kilometer': 1000.0, 'centimeter': 0.01, 'millimeter': 0.001, 'mile': 1609.34, 'yard': 0.9144, 'foot': 0.3048, 'inch': 0.0254}
    return value * units[from_unit] / units[to_unit]

def convert_mass(value, from_unit, to_unit):
    units = {'kilogram': 1.0, 'gram': 0.001, 'milligram': 0.000001, 'pound': 0.453592, 'ounce': 0.0283495}
    return value * units[from_unit] / units[to_unit]

def convert_temperature(value, from_unit, to_unit):
    if from_unit == 'celsius' and to_unit == 'fahrenheit': return (value * 9/5) + 32
    elif from_unit == 'fahrenheit' and to_unit == 'celsius': return (value - 32) * 5/9
    elif from_unit == 'celsius' and to_unit == 'kelvin': return value + 273.15
    elif from_unit == 'kelvin' and to_unit == 'celsius': return value - 273.15
    elif from_unit == 'fahrenheit' and to_unit == 'kelvin': return (value - 32) * 5/9 + 273.15
    elif from_unit == 'kelvin' and to_unit == 'fahrenheit': return (value - 273.15) * 9/5 + 32
    else: return value

def convert_time(value, from_unit, to_unit):
    units = {'second': 1.0, 'millisecond': 0.001, 'minute': 60.0, 'hour': 3600.0, 'day': 86400.0, 'week': 604800.0, 'month': 2629800.0, 'year': 31557600.0}
    return value * units[from_unit] / units[to_unit]

def convert_volume(value, from_unit, to_unit):
    units = {'liter': 1.0, 'milliliter': 0.001, 'gallon': 3.78541, 'quart': 0.946353, 'pint': 0.473176, 'cup': 0.24, 'tablespoon': 0.0147868, 'teaspoon': 0.00492892}
    return value * units[from_unit] / units[to_unit]

def convert_data_transfer_rate(value, from_unit, to_unit):
    units = {'bit per second': 1.0, 'kilobit per second': 1000.0, 'megabit per second': 1000000.0, 'gigabit per second': 1000000000.0, 'byte per second': 8.0, 'kilobyte per second': 8000.0, 'megabyte per second': 8000000.0, 'gigabyte per second': 8000000000.0}
    return value * units[from_unit] / units[to_unit]

def convert_digital_storage(value, from_unit, to_unit):
    units = {'bit': 1.0, 'byte': 8.0, 'kilobyte': 8192.0, 'megabyte': 8388608.0, 'gigabyte': 8589934592.0, 'terabyte': 8796093022208.0}
    return value * units[from_unit] / units[to_unit]

def convert_energy(value, from_unit, to_unit):
    units = {'joule': 1.0, 'kilojoule': 1000.0, 'calorie': 4.184, 'kilocalorie': 4184.0, 'watt-hour': 3600.0, 'kilowatt-hour': 3600000.0}
    return value * units[from_unit] / units[to_unit]

def convert_frequency(value, from_unit, to_unit):
    units = {'hertz': 1.0, 'kilohertz': 1000.0, 'megahertz': 1000000.0, 'gigahertz': 1000000000.0}
    return value * units[from_unit] / units[to_unit]

def convert_fuel_economy(value, from_unit, to_unit):
    units = {'miles per gallon': 1.0, 'kilometers per liter': 0.425144, 'liters per 100 kilometers': 235.214583}
    return value * units[from_unit] / units[to_unit]

def convert_plane_angle(value, from_unit, to_unit):
    units = {'degree': 1.0, 'radian': 57.2958, 'gradian': 0.9}
    return value * units[from_unit] / units[to_unit]

def convert_pressure(value, from_unit, to_unit):
    units = {'pascal': 1.0, 'kilopascal': 1000.0, 'bar': 100000.0, 'psi': 6894.76}
    return value * units[from_unit] / units[to_unit]

def convert_speed(value, from_unit, to_unit):
    units = {'meter per second': 1.0, 'kilometer per hour': 0.277778, 'mile per hour': 0.44704, 'knot': 0.514444}
    return value * units[from_unit] / units[to_unit]

# Streamlit app
st.set_page_config(page_title="Unit Converter", page_icon="📏", layout="centered")

# Title and description
st.title("📏 Advanced Unit Converter")
st.write("Convert units instantly with a clean and modern design!")

# Input fields
col1, col2, col3 = st.columns([2, 1, 1])
with col1: value = st.number_input("Enter value", value=1.0, step=0.1, format="%.2f")
with col2:
    category = st.selectbox("Category", ["Data Transfer Rate", "Digital Storage", "Energy", "Frequency", "Fuel Economy", "Length", "Mass", "Plane Angle", "Pressure", "Speed", "Temperature", "Time", "Volume"])
    units = {
        "Data Transfer Rate": ["bit per second", "kilobit per second", "megabit per second", "gigabit per second", "byte per second", "kilobyte per second", "megabyte per second", "gigabyte per second"],
        "Digital Storage": ["bit", "byte", "kilobyte", "megabyte", "gigabyte", "terabyte"],
        "Energy": ["joule", "kilojoule", "calorie", "kilocalorie", "watt-hour", "kilowatt-hour"],
        "Frequency": ["hertz", "kilohertz", "megahertz", "gigahertz"],
        "Fuel Economy": ["miles per gallon", "kilometers per liter", "liters per 100 kilometers"],
        "Length": ["meter", "kilometer", "centimeter", "millimeter", "mile", "yard", "foot", "inch"],
        "Mass": ["kilogram", "gram", "milligram", "pound", "ounce"],
        "Plane Angle": ["degree", "radian", "gradian"],
        "Pressure": ["pascal", "kilopascal", "bar", "psi"],
        "Speed": ["meter per second", "kilometer per hour", "mile per hour", "knot"],
        "Temperature": ["celsius", "fahrenheit", "kelvin"],
        "Time": ["second", "millisecond", "minute", "hour", "day", "week", "month", "year"],
        "Volume": ["liter", "milliliter", "gallon", "quart", "pint", "cup", "tablespoon", "teaspoon"]
    }[category]
with col3:
    from_unit = st.selectbox("From", units)
    to_unit = st.selectbox("To", units)

# Perform conversion
conversion_functions = {
    "Data Transfer Rate": convert_data_transfer_rate,
    "Digital Storage": convert_digital_storage,
    "Energy": convert_energy,
    "Frequency": convert_frequency,
    "Fuel Economy": convert_fuel_economy,
    "Length": convert_length,
    "Mass": convert_mass,
    "Plane Angle": convert_plane_angle,
    "Pressure": convert_pressure,
    "Speed": convert_speed,
    "Temperature": convert_temperature,
    "Time": convert_time,
    "Volume": convert_volume
}
result = conversion_functions[category](value, from_unit, to_unit)

# Display result
st.markdown(f"**Converted value:** {result:.2f}")

# Gemini explanation
if st.button("Explain Conversion"):
    prompt = f"Explain the conversion of {value} {from_unit} to {to_unit}. The result is {result}."
    response = model.generate_content(prompt)
    st.write(f"**Gemini Explanation:**\n{response.text}")

# Graph visualization
st.write("### 📊 Conversion Visualization")
x = np.linspace(0, 100, 100)
y = conversion_functions[category](x, from_unit, to_unit)

fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(x, y, label=f"{from_unit} to {to_unit}", color='blue', linewidth=2.5)
ax.scatter(value, result, color="red", s=100, label="Converted Value", zorder=5)
ax.grid(True, linestyle='--', alpha=0.7)
ax.annotate(f'{result:.2f} {to_unit}', xy=(value, result), xytext=(value + 5, result + 5), arrowprops=dict(facecolor='red', shrink=0.05), fontsize=12, color='red')
ax.set_xlabel(f"{from_unit}", fontsize=14, fontweight='bold')
ax.set_ylabel(f"{to_unit}", fontsize=14, fontweight='bold')
ax.set_title(f"{from_unit} to {to_unit} Conversion", fontsize=16, fontweight='bold')
ax.legend(loc='upper left', fontsize=12, framealpha=0.9)
ax.tick_params(axis='both', which='major', labelsize=12)
st.pyplot(fig)

# Footer
st.write("Made by ❤️ Muhammad Hamza")
