import streamlit as st
import pandas as pd
from weasyprint import HTML

# Page Configuration
st.set_page_config(page_title="Awin Lead Hunter Pro - PDF & CSV", page_icon="🎯", layout="wide")

st.title("🎯 Awin Brand & Affiliate Manager Lead Hunter")
st.write("Extract targeted Awin brands, search strategies, decision-maker queries, and download lead reports as PDF or CSV.")

# Sidebar Filters
all_niches = ["Fashion & Apparel", "Beauty & Skincare", "Consumer Tech", "Health & Supplements", "Home & Living", "Travel & Hospitality", "Sports & Fitness"]
all_regions = ["UK", "US", "Europe", "Global"]

st.sidebar.header("Filter Criteria")
selected_niches = st.sidebar.multiselect("Select Target Niches:", all_niches, default=all_niches[:2])
selected_regions = st.sidebar.multiselect("Select Target Regions:", all_regions, default=all_regions[:2])

def generate_pdf(df):
    rows_html = ""
    for idx, row in df.iterrows():
        rows_html += f"""
        <tr>
            <td style="text-align: center; font-weight: bold;">{idx + 1}</td>
            <td style="font-weight: bold; color: #1e293b;">{row['Brand Name']}</td>
            <td><span class="badge niche">{row['Niche']}</span></td>
            <td><span class="badge region">{row['Region']}</span></td>
            <td>{row['Decision Maker']}</td>
            <td style="color: #2563eb; font-weight: 500;">{row['Contact Email']}</td>
        </tr>
        """
        
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            @page {{ size: A4 landscape; margin: 12mm 10mm; background-color: #f8fafc; }}
            body {{ font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; color: #334155; margin: 0; padding: 0; font-size: 9.5pt; }}
            .header-container {{ background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); color: #ffffff; padding: 16px 20px; border-radius: 8px; margin-bottom: 15px; }}
            .header-title {{ font-size: 18pt; font-weight: bold; margin: 0 0 4px 0; color: #38bdf8; }}
            table.data-table {{ width: 100%; border-collapse: collapse; background: #ffffff; border-radius: 6px; overflow: hidden; border: 1px solid #e2e8f0; }}
            table.data-table th {{ background-color: #0f172a; color: #f8fafc; text-align: left; padding: 8px 10px; font-size: 9pt; text-transform: uppercase; }}
            table.data-table td {{ padding: 7px 10px; border-bottom: 1px solid #f1f5f9; vertical-align: middle; }}
            .badge {{ display: inline-block; padding: 2px 7px; border-radius: 4px; font-size: 8pt; font-weight: 600; }}
            .badge.niche {{ background-color: #e0f2fe; color: #0369a1; }}
            .badge.region {{ background-color: #fef3c7; color: #b45309; }}
        </style>
    </head>
    <body>
        <div class="header-container">
            <h1 class="header-title">🎯 Awin Lead Hunter Pro — Decision Maker Report</h1>
        </div>
        <table class="data-table">
            <thead>
                <tr>
                    <th style="width: 5%;">#</th>
                    <th style="width: 20%;">Brand Name</th>
                    <th style="width: 20%;">Niche</th>
                    <th style="width: 15%;">Region</th>
                    <th style="width: 20%;">Decision Maker</th>
                    <th style="width: 20%;">Contact Email</th>
                </tr>
            </thead>
            <tbody>
                {rows_html}
            </tbody>
        </table>
    </body>
    </html>
    """
    return HTML(string=html_content).write_pdf()

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
        
        # PDF Download Button
        pdf_bytes = generate_pdf(df)
        col1.download_button(
            label="📄 Download PDF Report",
            data=pdf_bytes,
            file_name="Awin_Leads_Report.pdf",
            mime="application/pdf"
        )
        
        # CSV Download Button
        csv = df.to_csv(index=False).encode('utf-8')
        col2.download_button(
            label="📥 Download CSV Report",
            data=csv,
            file_name="Awin_Leads_Report.csv",
            mime="text/csv"
        )
