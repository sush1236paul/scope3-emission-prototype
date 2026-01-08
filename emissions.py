EMISSION_FACTORS = {
    'diesel': 2.68,       # kgCO2e per liter
    'electricity': 0.42,  # kgCO2e per kWh
    'natural_gas': 5.3    # kgCO2e per therm
}

def normalize_and_calculate(qty, unit, fuel_type):
    # Convert gallons to liters for diesel if necessary
    norm_qty = qty * 3.78541 if unit.lower() == 'gallons' else qty
    
    # Get factor and calculate
    factor = EMISSION_FACTORS.get(fuel_type.lower(), 0.0)
    return round(norm_qty * factor, 2)
