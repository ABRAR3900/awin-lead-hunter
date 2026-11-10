import streamlit as st
import pandas as pd
import time

# Page Configuration
st.set_page_config(page_title="Awin Lead Hunter Pro", page_icon="🎯", layout="wide")

st.title("🎯 Awin Brand & Affiliate Manager Lead Hunter")
st.write("Extract targeted Awin brands, search strategies, decision-maker queries, and personalized pitches in seconds.")

# Sidebar Filters
st.sidebar.header("Filter Criteria")
selected_niches = st.sidebar.multiselect(
    "Select Target Niches:",
    ["Fashion & Apparel", "Beauty & Skincare", "Consumer Tech", "Health & Supplements", "Home & Living"],
    default=["Fashion & Apparel", "Beauty & Skincare"]
)

selected_regions = st.sidebar.multiselect(
    "Select Target Regions:",
    ["UK", "US", "Europe", "Global"],
    default=["UK", "US"]
)

# Fetch Data Button
if st.sidebar.button("🔍 Fetch Lead Data", type="primary"):
    with st.spinner("Mining Awin Merchant Directories & Decision-Maker Queries..."):
        time.sleep(1.5)
        
        leads_data = []
        for niche in selected_niches:
            for region in selected_regions:
                awin_search = f'site:awin.com/merchant "{niche}" "{region}"'
                linkedin_search = f'site:linkedin.com/in/ "Affiliate Manager" OR "Head of Partnerships" "{niche}" "{region}"'
                pitch = f"Hi [Manager Name], I noticed [Brand] on Awin ({niche}). I help {region} brands scale affiliate ROAS and eliminate voucher leakage. Open for a micro-audit?"
                
                leads_data.append({
                    "Niche": niche,
                    "Target Region": region,
                    "Awin Merchant Search Query": awin_search,
                    "LinkedIn Manager Query": linkedin_search,
                    "Automated Outreach Pitch": pitch
                })
        
        df = pd.DataFrame(leads_data)
        
        st.success(f"Successfully generated {len(df)} targeted lead workflows!")
        st.dataframe(df, use_container_width=True)
        
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Excel/CSV Report",
            data=csv,
            file_name="Awin_Affiliate_Leads.csv",
            mime="text/csv"
        )
else:
    st.info("👈 Sidebar se apni target **Niches** aur **Regions** select karein aur **Fetch Lead Data** par click karein.")
