import streamlit as st

def length_converter(value, from_unit, to_unit):
    # Conversion factors relative to meters
    conversion_factors = {
        'mm': 0.001,
        'cm': 0.01,
        'm': 1,
        'km': 1000,
        'in': 0.0254,
        'ft': 0.3048,
        'yd': 0.9144,
        'mi': 1609.34
    }
    
    try:
        return value * conversion_factors[from_unit] / conversion_factors[to_unit]
    except KeyError:
        return None

def weight_converter(value, from_unit, to_unit):
    conversion_factors = {
        'mg': 0.001, 'g': 1, 'kg': 1000, 'ton': 1000000,
        'oz': 28.3495, 'lb': 453.592
    }
    try:
        return value * conversion_factors[from_unit] / conversion_factors[to_unit]
    except KeyError:
        return None

def temperature_converter(value, from_unit, to_unit):
    try:
        if from_unit == to_unit:
            return value
        # Convert to Celsius first
        if from_unit == '°F':
            celsius = (value - 32) * 5/9
        elif from_unit == 'K':
            celsius = value - 273.15
        else:
            celsius = value
        # Convert to target unit
        if to_unit == '°F':
            return celsius * 9/5 + 32
        elif to_unit == 'K':
            return celsius + 273.15
        return celsius
    except:
        return None

def time_converter(value, from_unit, to_unit):
    conversion_factors = {
        'ms': 0.001, 's': 1, 'min': 60, 'hr': 3600,
        'day': 86400, 'week': 604800, 'year': 31536000
    }
    try:
        return value * conversion_factors[from_unit] / conversion_factors[to_unit]
    except KeyError:
        return None

def volume_converter(value, from_unit, to_unit):
    conversion_factors = {
        'ml': 0.001, 'l': 1, 'm³': 1000,
        'tsp': 0.00492892, 'tbsp': 0.0147868,
        'fl oz': 0.0295735, 'cup': 0.24,
        'pt': 0.473176, 'qt': 0.946353, 'gal': 3.78541
    }
    try:
        return value * conversion_factors[from_unit] / conversion_factors[to_unit]
    except KeyError:
        return None

# Streamlit app
st.set_page_config(page_title="Universal Unit Converter", layout="wide")
st.title("🌐 Universal Unit Converter")
st.write("Convert between different units of measurement")

# Sidebar for conversion type
conversion_type = st.sidebar.selectbox(
    "Select Conversion Type",
    ["Length", "Weight", "Temperature", "Time", "Volume"]
)

# Unit options based on conversion type
unit_options = {
    "Length": ['mm', 'cm', 'm', 'km', 'in', 'ft', 'yd', 'mi'],
    "Weight": ['mg', 'g', 'kg', 'ton', 'oz', 'lb'],
    "Temperature": ['°C', '°F', 'K'],
    "Time": ['ms', 's', 'min', 'hr', 'day', 'week', 'year'],
    "Volume": ['ml', 'l', 'm³', 'tsp', 'tbsp', 'fl oz', 'cup', 'pt', 'qt', 'gal']
}

# Main content
col1, col2, col3 = st.columns(3)

with col1:
    value = st.number_input("Enter value", value=1.0, step=0.1)

with col2:
    from_unit = st.selectbox("From unit", unit_options[conversion_type])

with col3:
    to_unit = st.selectbox("To unit", unit_options[conversion_type])

# Convert button and result
if st.button("Convert"):
    if conversion_type == "Length":
        result = length_converter(value, from_unit, to_unit)
    elif conversion_type == "Weight":
        result = weight_converter(value, from_unit, to_unit)
    elif conversion_type == "Temperature":
        result = temperature_converter(value, from_unit, to_unit)
    elif conversion_type == "Time":
        result = time_converter(value, from_unit, to_unit)
    elif conversion_type == "Volume":
        result = volume_converter(value, from_unit, to_unit)
    
    if result is not None:
        st.success(f"**Result:** {value:.2f} {from_unit} = {result:.4f} {to_unit}")
    else:
        st.error("Error: Invalid conversion")

# Additional information
st.markdown("---")
st.markdown("""
### Supported Conversions:
- **Length:** Millimeters, Centimeters, Meters, Kilometers, Inches, Feet, Yards, Miles
- **Weight:** Milligrams, Grams, Kilograms, Tons, Ounces, Pounds
- **Temperature:** Celsius, Fahrenheit, Kelvin
- **Time:** Milliseconds, Seconds, Minutes, Hours, Days, Weeks, Years
- **Volume:** Milliliters, Liters, Cubic Meters, Teaspoons, Tablespoons, Fluid Ounces, Cups, Pints, Quarts, Gallons
""")