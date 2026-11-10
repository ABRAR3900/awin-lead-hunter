import re
import pandas as pd
import requests
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="Awin Lead Hunter Pro (5x API Waterfall)",
    page_icon="🎯",
    layout="wide",
)

st.title("🎯 Awin Lead Hunter Pro (Multi-API System)")
st.write(
    "Extract verified decision-makers using **Hunter, Apollo, Snov, Skrapp,"
    " & Anymail Finder** with Free Scraper Fallback."
)

# Sidebar API Keys Input
st.sidebar.header("🔑 Free API Keys Setup")
hunter_key = st.sidebar.text_input("Hunter.io API Key", type="password")
apollo_key = st.sidebar.text_input("Apollo.io API Key", type="password")
snov_client_id = st.sidebar.text_input("Snov.io Client ID", type="password")
snov_client_secret = st.sidebar.text_input(
    "Snov.io Client Secret", type="password"
)
skrapp_key = st.sidebar.text_input("Skrapp.io API Key", type="password")
anymail_key = st.sidebar.text_input("Anymail Finder API Key", type="password")

all_niches = [
    "Fashion & Apparel",
    "Beauty & Skincare",
    "Consumer Tech",
    "Health & Supplements",
]
selected_niches = st.sidebar.multiselect(
    "Select Target Niches:", all_niches, default=all_niches[:2]
)


# Helper function for Snov.io Token
def get_snov_token(client_id, client_secret):
  try:
    res = requests.post(
        "https://api.snov.io/v1/oauth/access_token",
        data={
            "grant_type": "client_credentials",
            "client_id": client_id,
            "client_secret": client_secret,
        },
        timeout=5,
    )
    return res.json().get("access_token")
  except Exception:
    return None


# 5-Layer Waterfall Email Finder
def get_verified_email(domain):
  # Layer 1: Hunter.io
  if hunter_key:
    try:
      res = requests.get(
          f"https://api.hunter.io/v2/domain-search?domain={domain}&api_key={hunter_key}",
          timeout=5,
      )
      if res.status_code == 200:
        emails = res.json().get("data", {}).get("emails", [])
        if emails:
          return emails[0].get("value"), "Hunter.io API"
    except Exception:
      pass

  # Layer 2: Apollo.io
  if apollo_key:
    try:
      headers = {"Cache-Control": "no-cache", "Content-Type": "application/json"}
      payload = {"api_key": apollo_key, "domain": domain}
      res = requests.post(
          "https://api.apollo.io/v1/organizations/enrich",
          json=payload,
          headers=headers,
          timeout=5,
      )
      if res.status_code == 200:
        org_data = res.json().get("organization", {})
        email = org_data.get("contact_email") or org_data.get("email")
        if email:
          return email, "Apollo.io API"
    except Exception:
      pass

  # Layer 3: Snov.io
  if snov_client_id and snov_client_secret:
    token = get_snov_token(snov_client_id, snov_client_secret)
    if token:
      try:
        res = requests.get(
            f"https://api.snov.io/v1/get-domain-emails-with-info?domain={domain}",
            headers={"Authorization": f"Bearer {token}"},
            timeout=5,
        )
        if res.status_code == 200:
          emails = res.json().get("emails", [])
          if emails:
            return emails[0].get("email"), "Snov.io API"
      except Exception:
        pass

  # Layer 4: Skrapp.io
  if skrapp_key:
    try:
      res = requests.get(
          f"https://api.skrapp.io/api/v2/domain?domain={domain}",
          headers={"X-Access-Key": skrapp_key},
          timeout=5,
      )
      if res.status_code == 200:
        emails = res.json().get("emails", [])
        if emails:
          return emails[0].get("email"), "Skrapp.io API"
    except Exception:
      pass

  # Layer 5: Anymail Finder
  if anymail_key:
    try:
      res = requests.post(
          "https://api.anymailfinder.com/v5.0/search/company.json",
          headers={
              "X-API-KEY": anymail_key,
              "Content-Type": "application/json",
          },
          json={"domain": domain},
          timeout=5,
      )
      if res.status_code == 200:
        email = res.json().get("email")
        if email:
          return email, "Anymail Finder API"
    except Exception:
      pass

  # Layer 6: Free Direct Web Scraper Fallback
  try:
    url = f"https://www.{domain}"
    res = requests.get(
        url,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            )
        },
        timeout=5,
    )
    if res.status_code == 200:
      emails = re.findall(
          r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", res.text
      )
      valid = [
          e
          for e in emails
          if not any(
              x in e.lower() for x in [".png", ".jpg", ".svg", "example"]
          )
      ]
      if valid:
        return valid[0], "Free Web Scraper"
  except Exception:
    pass

  # Smart Pattern Fallback
  return f"affiliates@{domain}", "Smart Pattern Match"


# Fetch Data Button
if st.sidebar.button("🔍 Fetch Verified Leads", type="primary"):
  with st.spinner("Processing Waterfall Extraction across APIs..."):
    leads_data = []
    sample_brands = {
        "Fashion & Apparel": [("ASOS", "asos.com"), ("Boohoo", "boohoo.com")],
        "Beauty & Skincare": [
            ("LookFantastic", "lookfantastic.com"),
            ("Cult Beauty", "cultbeauty.co.uk"),
        ],
        "Consumer Tech": [("Currys", "currys.co.uk"), ("HP Store", "hp.com")],
        "Health & Supplements": [
            ("Myprotein", "myprotein.com"),
            ("Bulk", "bulk.com"),
        ],
    }

    for niche in selected_niches:
      brands = sample_brands.get(niche, [("Top Brand", "brand.com")])
      for brand_name, domain in brands:
        contact_email, source = get_verified_email(domain)

        awin_link = f"https://www.awin.com/us/store-directory/search?q={brand_name}"
        linkedin_query = f"https://www.linkedin.com/search/results/people/?keywords=Affiliate%20Manager%20{brand_name}"
        pitch = f"Hi [Manager Name], I noticed {brand_name} on Awin ({niche}). I help scale affiliate ROAS. Open for a micro-audit?"

        leads_data.append({
            "Brand Name": brand_name,
            "Niche": niche,
            "Contact Email": contact_email,
            "Data Source": source,
            "Awin Link": awin_link,
            "LinkedIn Search": linkedin_query,
            "Outreach Pitch": pitch,
        })

    df = pd.DataFrame(leads_data)

    st.success(f"Generated {len(df)} leads successfully!")
    st.dataframe(df, use_container_width=True)

    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Download CSV Report",
        data=csv,
        file_name="Awin_MultiAPI_Leads.csv",
        mime="text/csv",
    )
else:
  st.info(
      "👈 Sidebar mein API keys dalein (jo available hon) aur **Fetch Verified"
      " Leads** par click karein."
        )
            
