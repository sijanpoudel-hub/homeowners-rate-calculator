import streamlit as st

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(
    page_title="SecureHome Insurance Quote",
    page_icon="🏡",
    layout="centered"
)

# -------------------------------------------------
# ADVANCED CSS (VERY ATTRACTIVE)
# -------------------------------------------------
st.markdown("""
<style>

/* Background */
.stApp {
    background: linear-gradient(180deg, #eef3f9 0%, #ffffff 100%);
    font-family: 'Segoe UI', sans-serif;
}

/* Hero Section */
.hero {
    background: linear-gradient(120deg, #0b3c5d, #1d5c87);
    padding: 45px;
    border-radius: 20px;
    color: white;
    text-align: center;
    margin-bottom: 35px;
}
.hero h1 {
    font-size: 42px;
    margin-bottom: 10px;
}
.hero p {
    font-size: 18px;
    opacity: 0.9;
}

/* Glass Card */
.glass {
    background: rgba(255, 255, 255, 0.75);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border-radius: 18px;
    padding: 28px;
    box-shadow: 0 12px 30px rgba(0,0,0,0.08);
    margin-bottom: 28px;
}

/* Section Title */
.section-title {
    font-size: 22px;
    font-weight: 600;
    color: #0b3c5d;
    margin-bottom: 15px;
}

/* Button */
.stButton>button {
    width: 100%;
    background: linear-gradient(120deg, #0b3c5d, #1d5c87);
    color: white;
    font-size: 20px;
    padding: 16px;
    border-radius: 14px;
    border: none;
    transition: 0.3s;
}
.stButton>button:hover {
    transform: scale(1.02);
    background: linear-gradient(120deg, #1d5c87, #0b3c5d);
}

/* Quote Card */
.quote {
    background: linear-gradient(120deg, #e9f9ef, #ffffff);
    border-left: 8px solid #22a06b;
    border-radius: 18px;
    padding: 30px;
    text-align: center;
}
.quote h2 {
    color: #1f7a4d;
}
.quote h1 {
    font-size: 46px;
    margin-top: 10px;
}

/* Footer */
.footer {
    text-align: center;
    color: #777;
    font-size: 13px;
    margin-top: 40px;
}

</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# RATE MANUAL DATA
# -------------------------------------------------
BASE_RATE = 500
POLICY_FEE = 50

MIN_AMOUNT = 80_000
MAX_AMOUNT = 5_000_000

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
    "🏡 New Home": 0.20,
    "✅ Claim Free": 0.10,
    "📦 Multi-Policy": 0.07
}

PROTECTION_RELATIVITY = {
    "Frame": {1:1,2:1,3:1,4:1,5:1.05,6:1.1,7:1.15,8:1.25,9:2.1},
    "Masonry": {1:0.9,2:0.9,3:0.9,4:0.9,5:1,6:1.05,7:1.1,8:1.15,9:1.75}
}

# -------------------------------------------------
# FUNCTIONS
# -------------------------------------------------
def get_amount_relativity(amount):
    keys = sorted(AMOUNT_RELATIVITY.keys())
    if amount <= keys[0]:
        return AMOUNT_RELATIVITY[keys[0]]
    if amount > keys[-1]:
        return AMOUNT_RELATIVITY[keys[-1]] + 0.03 * ((amount - keys[-1]) / 15000)
    for i in range(len(keys)-1):
        if keys[i] <= amount <= keys[i+1]:
            r1, r2 = AMOUNT_RELATIVITY[keys[i]], AMOUNT_RELATIVITY[keys[i+1]]
            return r1 + (r2 - r1) * (amount - keys[i]) / (keys[i+1] - keys[i])

# -------------------------------------------------
# HERO
# -------------------------------------------------
st.markdown("""
<div class="hero">
<h1>SecureHome Insurance</h1>
<p>Instant • Transparent • Actuarially Accurate</p>
</div>
""", unsafe_allow_html=True)

# -------------------------------------------------
# INPUT CARD
# -------------------------------------------------
st.markdown('<div class="glass">', unsafe_allow_html=True)
st.markdown('<div class="section-title">🏠 Property Details</div>', unsafe_allow_html=True)

amount = st.number_input(
    "Amount of Insurance ($)",
    min_value=0,
    step=1,
    value=200000,
    help="Minimum $80,000 | Maximum $5,000,000"
)

col1, col2 = st.columns(2)
with col1:
    territory = st.selectbox("Territory", [1,2,3,4])
    protection = st.selectbox("Protection Class", list(range(1,10)))
    deductible = st.selectbox("Deductible ($)", [250,500,1000,5000])

with col2:
    construction = st.selectbox("Construction Type", ["Frame","Masonry"])
    tier = st.selectbox("Underwriting Tier", ["A","B","C","D"])
    jewelry = st.selectbox("Jewelry Coverage ($)", [2500,5000,10000],
                           help="$2,500 included at no cost")

liability = st.selectbox("Liability Limit ($)", [100000,300000,500000])
discounts = st.multiselect("Eligible Discounts", DISCOUNTS.keys())

st.markdown('</div>', unsafe_allow_html=True)

# -------------------------------------------------
# CTA
# -------------------------------------------------
if st.button("Get My Quote"):
    if amount < MIN_AMOUNT or amount > MAX_AMOUNT:
        st.markdown(
            f"""
            <div style="
            background-color:#fdecea;
            color:#611a15;
            padding:16px;
            border-radius:10px;
            font-size:16px;
            font-weight:500;
            ">
            ❌ Coverage amount must be between 
            <strong>${MIN_AMOUNT:,.0f}</strong> and 
            <strong>${MAX_AMOUNT:,.0f}</strong>.
            </div>
            """,
            unsafe_allow_html=True
            )

    else:
        premium = BASE_RATE
        premium *= get_amount_relativity(amount)
        premium *= TERRITORY_RELATIVITY[territory]
        premium *= PROTECTION_RELATIVITY[construction][protection]
        premium *= TIER_RELATIVITY[tier]
        premium *= DEDUCTIBLE_RELATIVITY[deductible]
        premium *= (1 - sum(DISCOUNTS[d] for d in discounts))
        premium += JEWELRY_ADDON[jewelry]
        premium += LIABILITY_ADDON[liability]
        premium += POLICY_FEE

        st.markdown(f"""
        <div class="quote">
            <h2>Your Estimated Annual Premium</h2>
            <h1>${premium:,.2f}</h1>
        </div>
        """, unsafe_allow_html=True)

# -------------------------------------------------
# FOOTER
# -------------------------------------------------
st.markdown("""
<div class="footer">
© 2026 SecureHome Insurance · Educational Rate Calculator · All values in USD
</div>
""", unsafe_allow_html=True)
