async def mock_extract_data(filename):
    fname = filename.lower()
    if "invoice" in fname:
        return {
            "supplier": "Shell Global",
            "fuel_type": "diesel",
            "quantity": 500.0,
            "unit": "gallons",
            "evidence": "Detected: 500 gallons of Diesel Fuel"
        }
    elif "shipping" in fname:
        return {
            "supplier": "Maersk",
            "fuel_type": "diesel",
            "quantity": 1200.0,
            "unit": "liters",
            "evidence": "Manifest lists 1200L marine diesel"
        }
    return {
        "supplier": "Generic Corp",
        "fuel_type": "electricity",
        "quantity": 100.0,
        "unit": "kwh",
        "evidence": "Default power usage detected"
    }