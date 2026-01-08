import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Scope-3 Auditor", layout="wide")
st.title("🌱 Scope-3 Supply Chain Auditor")

# 1. Batch Selection
batch_name = st.text_input("Current Batch Name", value="Batch-01")

uploaded_file = st.file_uploader("Upload Invoice", type=["pdf", "png", "jpg"])

if uploaded_file:
    if st.button("Run Audit"):
        with st.spinner("Processing..."):
            # Prepare file and batch parameter
            files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
            params = {"batch_name": batch_name}
            
            try:
                # API Call
                res = requests.post("http://localhost:8000/process", params=params, files=files)
                result = res.json()
                
                # Display Results
                st.metric("Estimated CO2e", f"{result['total_emissions_kgco2e']} kg")
                st.info(f"Evidence: {result['extracted_data']['evidence']}")
            except Exception as e:
                st.error(f"Error: {e}")

# 2. History & Charts Section
st.divider()
st.header("📊 Batch Comparison & History")

# Fetch full history
h_res = requests.get("http://localhost:8000/history")
if h_res.status_code == 200 and h_res.json():
    df = pd.DataFrame(h_res.json())
    
    # Chart: Compare Batches
    st.subheader("Emissions by Batch")
    batch_chart_data = df.groupby("batch")["total_emissions_kgco2e"].sum()
    st.bar_chart(batch_chart_data)
    
    # Table: Raw History
    st.subheader("Audit History")
    st.dataframe(df[["timestamp", "supplier", "batch", "total_emissions_kgco2e"]], use_container_width=True)
else:
    st.write("No history available yet. Upload a document to see analytics.")