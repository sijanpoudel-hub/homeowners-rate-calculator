import streamlit as st

# -------------------------
# RATE MANUAL DATA
# -------------------------

BASE_RATE = 500
POLICY_FEE = 50

AMOUNT_RELATIVITY = {
    80000: 0.56, 95000: 0.63, 110000: 0.69, 125000: 0.75,
    140000: 0.81, 155000: 0.86, 170000: 0.91, 185000: 0.96,
    200000: 1.00, 215000: 1.04, 230000: 1.08, 245000: 1.12,
    260000: 1.16, 275000: 1.20, 290000: 1.24, 305000: 1.28,
    320000: 1.32, 335000: 1.36, 350000: 1.39, 365000: 1.42,
    380000: 1.45
}

TERRITORY_RELATIVITY = {1: 0.80, 2: 0.90, 3: 1.00, 4: 1.10}
TIER_RELATIVITY = {"A": 0.80, "B": 0.95, "C": 1.00, "D": 1.45}
DEDUCTIBLE_RELATIVITY = {250: 1.00, 500: 0.95, 1000: 0.85, 5000: 0.70}

JEWELRY_ADDON = {2500: 0, 5000: 35, 10000: 60}
LIABILITY_ADDON = {100000: 0, 300000: 25, 500000: 45}

DISCOUNTS = {
    "New Home (20%)": 0.20,
    "Claim Free (10%)": 0.10,
    "Multi-Policy (7%)": 0.07
}

PROTECTION_RELATIVITY = {
    "Frame": {1: 1.00, 2: 1.00, 3: 1.00, 4: 1.00, 5: 1.05, 6: 1.10, 7: 1.15, 8: 1.25, 9: 2.10},
    "Masonry": {1: 0.90, 2: 0.90, 3: 0.90, 4: 0.90, 5: 1.00, 6: 1.05, 7: 1.10, 8: 1.15, 9: 1.75}
}

# -------------------------
# APP UI
# -------------------------

st.title("Homeowners Insurance Rate Calculator")
st.write("All calculations strictly follow the rate manual.")
st.write("All dollar amounts are in USD ($).")

amount = st.selectbox("Amount of Insurance ($)", sorted(AMOUNT_RELATIVITY.keys()))
territory = st.selectbox("Territory", list(TERRITORY_RELATIVITY.keys()))
construction = st.selectbox("Construction Type", ["Frame", "Masonry"])
protection = st.selectbox("Protection Class", list(range(1, 10)))
tier = st.selectbox("Underwriting Tier", list(TIER_RELATIVITY.keys()))
deductible = st.selectbox("Deductible ($)", list(DEDUCTIBLE_RELATIVITY.keys()))
jewelry = st.selectbox("Jewelry Coverage ($)", list(JEWELRY_ADDON.keys()))
liability = st.selectbox("Liability Limit ($)", list(LIABILITY_ADDON.keys()))

st.subheader("Discounts")
selected_discounts = st.multiselect("Select applicable discounts", DISCOUNTS.keys())

# -------------------------
# CALCULATION
# -------------------------

if st.button("Calculate Premium"):
    discount_factor = sum(DISCOUNTS[d] for d in selected_discounts)

    premium = BASE_RATE
    premium *= AMOUNT_RELATIVITY[amount]
    premium *= TERRITORY_RELATIVITY[territory]
    premium *= PROTECTION_RELATIVITY[construction][protection]
    premium *= TIER_RELATIVITY[tier]
    premium *= DEDUCTIBLE_RELATIVITY[deductible]
    premium *= (1 - discount_factor)
    premium += JEWELRY_ADDON[jewelry]
    premium += LIABILITY_ADDON[liability]
    premium += POLICY_FEE

    st.success(f"Final Annual Premium: ${premium:,.2f}")
