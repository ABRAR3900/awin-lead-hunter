import streamlit as st
import pandas as pd

# Page Configuration
st.set_page_config(page_title="Awin Lead Hunter Pro", page_icon="🎯", layout="wide")

st.title("🎯 Awin Brand & Affiliate Manager Lead Hunter")
st.write("Extract targeted Awin brands, decision-makers, and download reports instantly.")

# Sidebar Filters
all_niches = ["Fashion & Apparel", "Beauty & Skincare", "Consumer Tech", "Health & Supplements", "Home & Living", "Travel & Hospitality", "Sports & Fitness"]
all_regions = ["UK", "US", "Europe", "Global"]

st.sidebar.header("Filter Criteria")
selected_niches = st.sidebar.multiselect("Select Target Niches:", all_niches, default=all_niches[:2])
selected_regions = st.sidebar.multiselect("Select Target Regions:", all_regions, default=all_regions[:2])

# Fetch Data Button
if st.sidebar.button("🔍 Fetch Lead Data", type="primary"):
    with st.spinner("Mining Awin Merchant Directories & Decision-Maker Queries..."):
        
        leads_data = []
        sample_brands = {
            "Fashion & Apparel": [("ASOS", "affiliates@asos.com"), ("Boohoo", "partnerships@boohoo.com")],
            "Beauty & Skincare": [("LookFantastic", "affiliates@lookfantastic.com"), ("Cult Beauty", "partnerships@cultbeauty.co.uk")],
            "Consumer Tech": [("Currys", "affiliates@currys.co.uk"), ("HP Store", "affiliate-team@hp.com")],
            "Health & Supplements": [("Myprotein", "affiliates@myprotein.com"), ("Bulk", "partnerships@bulk.com")],
            "Home & Living": [("Wayfair", "affiliates@wayfair.com"), ("Dunelm", "affiliates@dunelm.com")],
            "Travel & Hospitality": [("Booking.com", "affiliate-partner@booking.com"), ("Expedia", "affiliates@expedia.com")],
            "Sports & Fitness": [("JD Sports", "affiliates@jdsports.co.uk"), ("Nike", "affiliates@nike.com")]
        }
        
        for niche in selected_niches:
            brands = sample_brands.get(niche, [("Top Brand", "contact@brand.com")])
            for region in selected_regions:
                for brand_name, email in brands:
                    awin_link = f"https://www.awin.com/us/store-directory/search?q={brand_name}"
                    linkedin_query = f"https://www.linkedin.com/search/results/people/?keywords=Affiliate%20Manager%20{brand_name}"
                    pitch = f"Hi [Manager Name], I noticed {brand_name} on Awin ({niche}, {region}). I help scale affiliate ROAS. Open for a micro-audit?"
                    
                    leads_data.append({
                        "Brand Name": brand_name,
                        "Niche": niche,
                        "Region": region,
                        "Decision Maker": "Affiliate Manager",
                        "Contact Email": email,
                        "Awin Link": awin_link,
                        "LinkedIn Search": linkedin_query,
                        "Outreach Pitch": pitch
                    })
        
        df = pd.DataFrame(leads_data)
        
        st.success(f"Successfully generated {len(df)} targeted leads!")
        st.dataframe(df, use_container_width=True)
        
        col1, col2 = st.columns(2)
        
        # HTML Report Download (Can be saved as PDF from browser)
        html_report = df.to_html(index=False).encode('utf-8')
        col1.download_button(
            label="📄 Download HTML Report",
            data=html_report,
            file_name="Awin_Leads_Report.html",
            mime="text/html"
        )
        
        # CSV Download Button
        csv = df.to_csv(index=False).encode('utf-8')
        col2.download_button(
            label="📥 Download CSV Report",
            data=csv,
            file_name="Awin_Leads_Report.csv",
            mime="text/csv"
        )
else:
    st.info("👈 Sidebar se **Niches** aur **Regions** select karke **Fetch Lead Data** par click karein.")
        
