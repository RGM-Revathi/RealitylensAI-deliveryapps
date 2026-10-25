

import streamlit as st
import pandas as pd
from collections import Counter
from datetime import date
import json
import urllib.request
import urllib.error

# =========================================================
# FACT CHECK ✓ WITH REALITYLENSAI
# Andhra Pradesh hotels, restaurants & residential projects
# =========================================================

st.set_page_config(
    page_title="FACT CHECK | RealityLensAI",
    page_icon="✓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -------------------- PROFESSIONAL LIGHT THEME --------------------

st.markdown("""
<style>
/* ===== COLORFUL, HIGH-CONTRAST THEME ===== */
:root { color-scheme: light !important; }
html, body, .stApp,
[data-testid="stAppViewContainer"], [data-testid="stMain"],
[data-testid="stMainBlockContainer"], [data-testid="stHeader"],
[data-testid="stBottom"], [data-testid="stVerticalBlock"],
[data-testid="stHorizontalBlock"] {
    background: linear-gradient(135deg, #F1F5FF 0%, #F7F0FF 48%, #E9FAF7 100%) !important;
    color: #17233D !important;
}
[data-testid="stMainBlockContainer"] { padding-top: 1.4rem !important; }
.stApp, .stApp p, .stApp span, .stApp label, .stApp li,
.stApp small, .stApp strong, .stApp div,
[data-testid="stMarkdownContainer"], [data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] li {
    color: #17233D;
}
.stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6 {
    color: #18264A !important; font-weight: 800 !important;
}
/* Inputs and dropdowns */
.stApp input, .stApp textarea, .stApp select,
[data-baseweb="select"], [data-baseweb="select"] *,
[data-baseweb="input"], [data-baseweb="input"] *,
[data-baseweb="textarea"], [data-baseweb="textarea"] *, [data-baseweb="tag"] {
    background-color: #FFFFFF !important; color: #17233D !important;
    -webkit-text-fill-color: #17233D !important; border-color: #AABBE0 !important;
}
[data-baseweb="popover"], [data-baseweb="popover"] *, [role="listbox"], [role="option"] { color: #17233D !important; }
[role="option"] { background: #FFFFFF !important; }
[role="option"]:hover { background: #E7E9FF !important; }
/* Navigation tabs */
.stTabs [data-baseweb="tab-list"] { background: #E2E8FA !important; border-radius: 13px !important; gap: 6px !important; padding: 5px !important; }
.stTabs [data-baseweb="tab"] { background: transparent !important; color: #27375E !important; border-radius: 9px !important; }
.stTabs [data-baseweb="tab"] *, .stTabs button p { color: #27375E !important; -webkit-text-fill-color: #27375E !important; font-weight: 700 !important; }
.stTabs [aria-selected="true"] { background: linear-gradient(135deg, #D5F5EB, #E6E5FF) !important; border-bottom: 3px solid #6554C0 !important; }
.stTabs [aria-selected="true"] *, .stTabs [aria-selected="true"] p { color: #26316B !important; -webkit-text-fill-color: #26316B !important; font-weight: 800 !important; }
/* Buttons */
.stApp .stButton > button, .stApp button[kind="primary"], .stApp button[kind="secondary"], .stApp [data-testid="stDownloadButton"] button, .stApp a[kind="secondary"] {
    background: linear-gradient(135deg, #D7F5EC, #E4E2FF) !important; color: #202C59 !important;
    border: 1px solid #9B9BE0 !important; border-radius: 10px !important; font-weight: 750 !important;
}
.stApp .stButton > button *, .stApp button[kind="primary"] *, .stApp button[kind="secondary"] *, .stApp [data-testid="stDownloadButton"] button * { color: #202C59 !important; -webkit-text-fill-color: #202C59 !important; }
.stApp .stButton > button:hover, .stApp [data-testid="stDownloadButton"] button:hover { background: linear-gradient(135deg, #BCEBDD, #CBC8FF) !important; border-color: #5C55B7 !important; }
/* Cards, metrics, alerts and data panels */
[data-testid="stVerticalBlockBorderWrapper"], [data-testid="stExpander"], [data-testid="stMetric"], [data-testid="stAlert"], .stApp [data-testid="stDataFrame"], .stApp [data-testid="stTable"] {
    background: #FFFFFF !important; border: 1px solid #D0D8F0 !important; border-radius: 13px !important; color: #17233D !important;
}
[data-testid="stMetricLabel"], [data-testid="stMetricLabel"] *, [data-testid="stMetricValue"], [data-testid="stMetricValue"] *, [data-testid="stMetricDelta"], [data-testid="stMetricDelta"] * { color: #17233D !important; -webkit-text-fill-color: #17233D !important; }
/* Data tables */
.stApp table { background: #FFFFFF !important; color: #17233D !important; border-collapse: collapse !important; }
.stApp th { background: #DDE7FF !important; color: #1D2D5A !important; font-weight: 800 !important; }
.stApp td { background: #FFFFFF !important; color: #17233D !important; }
.stApp th, .stApp td { border-color: #D2DDF2 !important; }
/* Expanders */
[data-testid="stExpander"] { border: 1px solid #BCC9EC !important; background: #FFFFFF !important; overflow: hidden; }
[data-testid="stExpander"] summary { background: linear-gradient(90deg, #E2F6F0, #E9E5FF) !important; padding: 12px 14px !important; border-radius: 10px !important; color: #1D2D5A !important; font-weight: 800 !important; }
[data-testid="stExpander"] summary span, [data-testid="stExpander"] summary p, [data-testid="stExpander"] summary div, [data-testid="stExpander"] summary svg { color: #1D2D5A !important; fill: #1D2D5A !important; -webkit-text-fill-color: #1D2D5A !important; font-weight: 800 !important; }
[data-testid="stExpander"] summary:hover { background: #D8D5FF !important; }
[data-testid="stMarkdownContainer"] h2, [data-testid="stMarkdownContainer"] h3 { padding-bottom: 6px; border-bottom: 1px solid #D2DDF2; }
/* Sidebar */
[data-testid="stSidebar"], [data-testid="stSidebar"] > div { background: linear-gradient(180deg, #E0F5F0 0%, #E7E7FF 100%) !important; }
[data-testid="stSidebar"] *, [data-testid="stSidebar"] p, [data-testid="stSidebar"] label { color: #17233D !important; }
.stApp a { color: #4C3DA8 !important; text-decoration: underline; font-weight: 650; }
.stApp [data-testid="stCheckbox"] *, .stApp [data-testid="stRadio"] * { color: #17233D !important; }
.stApp [data-testid="stProgress"] > div { background: #DCE4F8 !important; }
.stApp [data-testid="stProgress"] [role="progressbar"] { background: linear-gradient(90deg, #0D9B83, #6554C0) !important; }
.stApp .stCaption, .stApp [data-testid="stCaptionContainer"], .stApp [data-testid="stCaptionContainer"] * { color: #4B5878 !important; }
.stApp input:disabled, .stApp textarea:disabled { color: #596580 !important; -webkit-text-fill-color: #596580 !important; opacity: 1 !important; }
[data-testid="stDecoration"] { background: linear-gradient(90deg, #0D9B83, #6554C0, #D14D83) !important; }
hr { border-color: #D0D8F0 !important; }
/* Centered hero title with rich color and strong contrast */
.hero { background: linear-gradient(120deg, #D8F7EE 0%, #E4E4FF 48%, #FFE4EF 100%); border: 1px solid #B6C4EB; border-top: 5px solid #6554C0; border-radius: 20px; padding: 30px 24px 25px; margin: 0 auto 24px auto; text-align: center; box-shadow: 0 10px 28px rgba(43, 50, 105, 0.13); }
.hero-title { color: #18264A !important; font-size: clamp(2rem, 4vw, 3.1rem); line-height: 1.15; font-weight: 950; letter-spacing: 0.5px; text-align: center; }
.hero-subtitle { color: #4B3198 !important; font-size: clamp(1.1rem, 2vw, 1.55rem); font-weight: 900; letter-spacing: 2px; text-align: center; margin-top: 7px; }
.hero-caption { color: #26375D !important; font-size: 1rem; font-weight: 650; text-align: center; margin-top: 13px; }

/* ===== LIGHTEN DARK/BLACK WIDGET BOXES + FORCE READABLE TEXT ===== */
/* All common Streamlit content surfaces */
[data-testid="stAppViewContainer"], [data-testid="stMain"],
[data-testid="stMainBlockContainer"], [data-testid="stVerticalBlockBorderWrapper"],
[data-testid="stElementContainer"], [data-testid="stExpander"],
[data-testid="stPopover"], [data-testid="stDialog"], [role="dialog"],
[data-testid="stNotificationContent"] {
    color: #17233D !important;
}
/* Code blocks, JSON/text output, terminal-like black panels */
.stApp pre, .stApp code, [data-testid="stCode"],
[data-testid="stCodeBlock"], [data-testid="stJson"],
.stApp [data-testid="stText"] {
    background: #F3F6FC !important;
    color: #17233D !important;
    border: 1px solid #D5DDF0 !important;
    border-radius: 10px !important;
}
.stApp pre *, .stApp code *, [data-testid="stCode"] *,
[data-testid="stCodeBlock"] *, [data-testid="stJson"] * {
    background-color: transparent !important;
    color: #17233D !important;
    -webkit-text-fill-color: #17233D !important;
    text-shadow: none !important;
}
/* Charts and chart canvases: light canvas with dark labels */
.stApp [data-testid="stPlotlyChart"], .stApp [data-testid="stVegaLiteChart"],
.stApp [data-testid="stArrowVegaLiteChart"], .stApp [data-testid="stDeckGlChart"],
.stApp [data-testid="stGraphvizChart"] {
    background: #FFFFFF !important;
    border: 1px solid #D5DDF0 !important;
    border-radius: 12px !important;
    padding: 6px !important;
}
/* Tables and dataframe toolbars */
.stApp [data-testid="stDataFrame"] *, .stApp [data-testid="stTable"] *,
.stApp [data-testid="stDataFrameResizable"] *,
.stApp [data-testid="stToolbar"] * {
    color: #17233D !important;
}
.stApp [data-testid="stDataFrame"] button,
.stApp [data-testid="stDataFrameResizable"] button,
.stApp [data-testid="stToolbar"] button {
    background: #EEF2FC !important;
    color: #17233D !important;
    border-color: #C9D3EA !important;
}
/* Alerts, status boxes, and messages */
.stApp [data-testid="stAlert"], .stApp [data-testid="stStatusWidget"],
.stApp [data-testid="stToast"], .stApp [data-testid="stNotificationContent"] {
    background: #F7F9FF !important;
    color: #17233D !important;
    border: 1px solid #D3DDF0 !important;
}
.stApp [data-testid="stAlert"] *, .stApp [data-testid="stStatusWidget"] *,
.stApp [data-testid="stToast"] * {
    color: #17233D !important;
    -webkit-text-fill-color: #17233D !important;
}
/* Form fields, multiselect chips, selected values, and dropdown menu */
[data-baseweb="select"] > div, [data-baseweb="input"] > div,
[data-baseweb="textarea"] > div, [data-baseweb="tag"] {
    background: #FFFFFF !important;
    color: #17233D !important;
    border-color: #B8C6E2 !important;
}
[data-baseweb="select"] *, [data-baseweb="input"] *,
[data-baseweb="textarea"] *, [data-baseweb="tag"] * {
    color: #17233D !important;
    -webkit-text-fill-color: #17233D !important;
}
/* Any nested panels that inherit a dark theme */
.stApp [data-testid="stVerticalBlockBorderWrapper"],
.stApp [data-testid="stHorizontalBlock"] > div,
.stApp [data-testid="stColumn"] > div,
.stApp [data-testid="stMetric"] > div {
    background-color: #FFFFFF !important;
}
.stApp [data-testid="stMarkdownContainer"] p,
.stApp [data-testid="stMarkdownContainer"] li,
.stApp [data-testid="stMarkdownContainer"] span,
.stApp label, .stApp p, .stApp li, .stApp small,
.stApp [data-testid="stCaptionContainer"] * {
    color: #17233D !important;
    -webkit-text-fill-color: #17233D !important;
}
.stApp input::placeholder, .stApp textarea::placeholder {
    color: #687692 !important;
    -webkit-text-fill-color: #687692 !important;
    opacity: 1 !important;
}


/* ===== FIX: "Open reference website" LINK BUTTON ===== */
.stApp [data-testid="stLinkButton"] a,
.stApp [data-testid="stLinkButton"] a:link,
.stApp [data-testid="stLinkButton"] a:visited,
.stApp a[data-testid="stLinkButton"],
.stApp a[kind="secondary"] {
    background: #FFFFFF !important;
    background-color: #FFFFFF !important;
    color: #17233D !important;
    -webkit-text-fill-color: #17233D !important;
    border: 1px solid #AABBE0 !important;
    border-radius: 10px !important;
    box-shadow: 0 2px 7px rgba(35, 48, 85, 0.08) !important;
    text-decoration: none !important;
    font-weight: 750 !important;
}
.stApp [data-testid="stLinkButton"] a *,
.stApp [data-testid="stLinkButton"] a p,
.stApp [data-testid="stLinkButton"] a span,
.stApp a[data-testid="stLinkButton"] * {
    color: #17233D !important;
    -webkit-text-fill-color: #17233D !important;
}
.stApp [data-testid="stLinkButton"] a:hover,
.stApp a[data-testid="stLinkButton"]:hover,
.stApp a[kind="secondary"]:hover {
    background: #EEF2FF !important;
    background-color: #EEF2FF !important;
    border-color: #6554C0 !important;
    color: #17233D !important;
    -webkit-text-fill-color: #17233D !important;
}

</style>
""", unsafe_allow_html=True)

# -------------------- DELIVERY PLATFORM CATALOGUE --------------------
# IMPORTANT: The reviews below are illustrative demo text, not genuine customer reviews.
# Scores and analysis are heuristic demonstrations, not independently verified findings.

places = {
    "Amazon": {
        "image": "https://www.google.com/s2/favicons?domain=amazon.in&sz=128",
        "category": "Online Shopping", "city": "India", "price": "Varies by product",
        "source": "https://www.amazon.in/",
        "description": "Review product information, seller reliability, delivery, returns, refunds and support.",
        "reviews": [
            ("Family shopper", "The order arrived on time and tracking updates were helpful.", 4),
            ("Student", "The refund process took longer than expected.", 2),
            ("Online seller", "Resolving a support issue took several steps.", 3),
            ("First-time buyer", "The product page clearly listed the main features.", 4),
        ],
    },
    "Flipkart": {
        "image": "https://www.google.com/s2/favicons?domain=flipkart.com&sz=128",
        "category": "Online Shopping", "city": "India", "price": "Varies by product",
        "source": "https://www.flipkart.com/",
        "description": "Review listing accuracy, delivery, replacements, returns and customer support.",
        "reviews": [
            ("Student", "Price comparison was easy and the parcel arrived in good condition.", 4),
            ("Family shopper", "The replacement status was unclear.", 2),
            ("First-time buyer", "The product description could explain included accessories more clearly.", 3),
            ("Working professional", "Order tracking was useful throughout delivery.", 4),
        ],
    },
    "Swiggy": {
        "image": "https://www.google.com/s2/favicons?domain=swiggy.com&sz=128",
        "category": "Food Delivery", "city": "India", "price": "Varies by order",
        "source": "https://www.swiggy.com/",
        "description": "Review delivery estimates, order accuracy, food condition, cancellations, fees and support.",
        "reviews": [
            ("Family customer", "The order arrived later than estimated and the food was not warm.", 2),
            ("Student", "Tracking was useful and the order was packed neatly.", 4),
            ("Busy professional", "Getting help for a missing item took too long.", 2),
            ("Regular customer", "Reordering a previous meal was quick and convenient.", 4),
        ],
    },
    "Zomato": {
        "image": "https://www.google.com/s2/favicons?domain=zomato.com&sz=128",
        "category": "Food Delivery", "city": "India", "price": "Varies by order",
        "source": "https://www.zomato.com/",
        "description": "Review restaurant listings, delivery estimates, packaging, fees, refunds and issue resolution.",
        "reviews": [
            ("Family customer", "Restaurant options were easy to compare.", 4),
            ("Student", "The delivery was delayed and the arrival time kept changing.", 2),
            ("Busy professional", "The meal was correct, but resolving a spilled item was unclear.", 3),
            ("Regular customer", "The menu photos helped me choose what to order.", 4),
        ],
    },
    "Blinkit": {
        "image": "https://www.google.com/s2/favicons?domain=blinkit.com&sz=128",
        "category": "Quick Commerce", "city": "India", "price": "Varies by order",
        "source": "https://blinkit.com/",
        "description": "Review stock accuracy, substitutions, missing products, delivery reliability and refunds.",
        "reviews": [
            ("Family shopper", "An unavailable item was substituted without clear communication.", 2),
            ("Student", "Finding daily essentials and checking prices was convenient.", 4),
            ("Working professional", "The missing-item refund was not explained clearly.", 2),
            ("Regular customer", "The order arrived quickly and the items were packed neatly.", 4),
        ],
    },
    "Zepto": {
        "image": "https://www.google.com/s2/favicons?domain=zeptonow.com&sz=128",
        "category": "Quick Commerce", "city": "India", "price": "Varies by order",
        "source": "https://www.zeptonow.com/",
        "description": "Review delivery speed, stock accuracy, item condition, substitutions, fees and support.",
        "reviews": [
            ("Student", "Repeat ordering was convenient and delivery was quick.", 4),
            ("Family shopper", "Some items were unavailable after checkout and alternatives were unclear.", 2),
            ("Working professional", "An item was damaged and the support steps were unclear.", 2),
            ("Regular customer", "The app made it easy to find common grocery items.", 4),
        ],
    },
    "BigBasket": {
        "image": "https://www.google.com/s2/favicons?domain=bigbasket.com&sz=128",
        "category": "Grocery Delivery", "city": "India", "price": "Varies by order",
        "source": "https://www.bigbasket.com/",
        "description": "Review grocery freshness, missing items, delivery slots, substitutions and refunds.",
        "reviews": [
            ("Family shopper", "The delivery slot was convenient and most groceries arrived in good condition.", 4),
            ("Senior customer", "Some fresh items were not in the expected condition.", 2),
            ("Busy professional", "Refund status for an unavailable item needed clearer updates.", 2),
            ("Regular customer", "The scheduled slot made weekly grocery shopping easier.", 4),
        ],
    },
}

# -------------------- ANALYSIS RULES --------------------

# Keep place lists in a consistent category -> city -> name order.
places = dict(sorted(
    places.items(),
    key=lambda pair: (pair[1]["category"], pair[1]["city"], pair[0].casefold())
))

# Add clearly labelled illustrative positive examples so the prototype can
# demonstrate both positive and negative perspectives for every selected place.
# These are synthetic demo examples, not genuine public reviews.
for _place_name, _place in places.items():
    _cat = _place["category"]
    if _cat == "Hotel":
        _positive = [
            ("Family", "The room was clean and the staff helped us promptly.", 5),
            ("Professional", "Check-in was smooth and the location was convenient.", 4),
        ]
    elif _cat == "Restaurant":
        _positive = [
            ("Family", "The food was tasty and the staff were welcoming.", 5),
            ("Student", "The meal was satisfying and service was quick.", 4),
        ]
    elif _cat == "Apartment / House":
        _positive = [
            ("Homebuyer", "The layout looked practical during the illustrative site visit.", 4),
            ("Family", "The location seemed convenient for nearby daily needs.", 4),
        ]
    elif _cat == "Museum":
        _positive = [
            ("Student", "The exhibits made the history easier to understand.", 5),
            ("Family", "The visit was informative and enjoyable.", 4),
        ]
    elif _cat == "Park":
        _positive = [
            ("Family", "The outdoor visit was enjoyable and scenic.", 5),
            ("Student", "The place was pleasant to explore with friends.", 4),
        ]
    else:
        _positive = [
            ("Family", "The place was enjoyable and facilities were easy to access.", 5),
            ("Student", "The visit was pleasant and the area was easy to explore.", 4),
        ]
    _place["reviews"] = list(_place["reviews"]) + _positive

ISSUE_RULES = {
    "Delivery Time / Reliability": [
        "late", "delayed", "delivery time", "arrived later", "arrival time",
        "tracking", "delivery slot", "on time", "quickly", "delivery was quick",
    ],
    "Order Accuracy / Availability": [
        "missing item", "missing product", "wrong item", "unavailable", "out of stock",
        "substituted", "substitution", "replacement", "order was correct", "order accuracy",
    ],
    "Product / Food Condition": [
        "not warm", "cold food", "spilled", "damaged", "fresh", "freshness",
        "packed neatly", "packaging", "condition", "spoiled", "broken",
    ],
    "Price / Fees / Value": [
        "expensive", "overpriced", "costly", "extra charges", "delivery fee",
        "platform fee", "surge fee", "price", "refund", "refund process", "refund status",
    ],
    "App / Support / Transparency": [
        "customer support", "support issue", "support steps", "clearer", "unclear",
        "communication", "help", "tracking updates", "product description", "menu photos",
        "easy to compare", "convenient", "reordering",
    ],
}

IMPROVEMENTS = {
    "Delivery Time / Reliability": (
        "Show realistic delivery windows, communicate delays promptly, and explain how estimates are calculated."
    ),
    "Order Accuracy / Availability": (
        "Improve inventory synchronisation, confirm substitutions with customers, and simplify missing-item reporting."
    ),
    "Product / Food Condition": (
        "Strengthen packaging and handling checks, record condition-related complaints, and make replacement options clear."
    ),
    "Price / Fees / Value": (
        "Show item totals, delivery/platform fees, discounts and refund rules clearly before checkout."
    ),
    "App / Support / Transparency": (
        "Make order status easier to understand and provide a clear, trackable path to human support."
    ),
    "General dissatisfaction": (
        "Collect more detail and check the original order record before drawing a conclusion."
    ),
}

def analyze_reviews(reviews):
    findings = []
    counts = Counter()

    for perspective, text, rating in reviews:
        lowered = text.lower()
        issues = [
            issue for issue, keywords in ISSUE_RULES.items()
            if any(word in lowered for word in keywords)
        ]

        if rating <= 2 and not issues:
            issues = ["General dissatisfaction"]

        if issues:
            findings.append({
                "Perspective": perspective,
                "Rating": rating,
                "Review": text,
                "Issues": issues,
            })
            counts.update(issues)

    average = (
        sum(item[2] for item in reviews) / len(reviews)
        if reviews else 0
    )

    return {
        "findings": findings,
        "counts": counts,
        "average": average,
        "total": len(reviews),
    }

def demo_score(place, analysis):
    # Demonstration formula only; not a real-world verified score.
    score = 70 + (analysis["average"] - 3) * 8
    score -= min(15, len(analysis["findings"]) * 1.5)
    if place["category"] in ("Quick Commerce", "Food Delivery") and analysis["average"] < 3:
        score -= 2
    return max(0, min(100, round(score)))

def label(name):
    item = places[name]
    return f"{name}  |  {item['category']}  |  {item['city']}"

# -------------------- HEADER --------------------
st.markdown("""
<div class="hero">
    <div class="hero-title">FACT CHECK ✓</div>
    <div class="hero-subtitle">WITH REALITYLENS AI</div>
    <div class="hero-caption">Delivery App Reviews · Claim Checks · Evidence Signals · Trust Score</div>
</div>
""", unsafe_allow_html=True)

st.warning(
    "DEMO DATA NOTICE: The reviews shown here are illustrative examples created "
    "to demonstrate the analysis. They are not genuine customer reviews, live ratings, "
    "or verified allegations. The analysis does not independently authenticate evidence."
)

# -------------------- SIDEBAR FILTERS --------------------
st.sidebar.title("Explore Delivery Apps")
st.sidebar.caption("Food delivery • Quick commerce • Online shopping • Groceries")

category = st.sidebar.selectbox(
    "Category",
    ["All categories", "Food Delivery", "Quick Commerce", "Grocery Delivery", "Online Shopping"],
)
city_options = ["All cities"] + sorted({p["city"] for p in places.values()})
city = st.sidebar.selectbox("City", city_options)

filtered_places = [
    name for name, item in places.items()
    if (category == "All categories" or item["category"] == category)
    and (city == "All cities" or item["city"] == city)
]
st.sidebar.caption(f"{len(filtered_places)} platforms in this demo catalogue")
st.sidebar.markdown("---")
st.sidebar.caption("Always verify current details through official sources.")
st.sidebar.markdown("---")
st.sidebar.markdown("**Optional LLM review assistant**")
llm_api_key = st.sidebar.text_input(
    "OpenAI API key (optional)",
    type="password",
    help="Only used when you press the LLM analysis button. It is not saved by this app.",
    key="llm_api_key_input",
)
st.sidebar.caption("Without an API key, the prototype still runs its local review rules.")

# -------------------- NAVIGATION --------------------
explore_tab, report_tab, compare_tab, saved_tab, submit_tab, feed_tab, about_tab = st.tabs([
    "Explore Apps",
    "App Reviews & Reality Report",
    "Compare",
    "Saved",
    "Submit a Claim",
    "Ranked Feed",
    "About",
])

# -------------------- EXPLORE --------------------
with explore_tab:
    st.subheader("Explore delivery and shopping platforms")
    st.write(
        "Browse delivery, grocery and online-shopping platforms. "
        "Choose a platform to view its review analysis."
    )

    if filtered_places:
        columns = st.columns(3)
        for index, name in enumerate(filtered_places):
            item = places[name]
            with columns[index % 3]:
                # Platform logo/favicons are loaded from the platform domain.
                st.image(item["image"], width=76)
                st.markdown(f"### {name}")
                st.markdown(f"**Category:** {item['category']}")
                st.markdown(f"**City:** {item['city']}")
                st.markdown(f"**Price range:** {item['price']}")
                st.write(item["description"])

                st.link_button(
                    "Open reference website",
                    item["source"],
                    use_container_width=True,
                )
                if st.button("Analyze this app", key=f"pick_{name}"):
                    st.session_state["report_place_select"] = name
                    st.toast("Platform selected. Open App Reviews & Reality Report.")
    else:
        st.info("No places match those filters.")

    st.caption(
        "A listing or external link is not an endorsement. Confirm current details independently."
    )

# -------------------- REPORT --------------------
with report_tab:
    st.subheader("Reviews & Reality Report")

    all_names = list(places.keys())
    default_name = st.session_state.get("report_place_select", st.session_state.get("report_place", all_names[0]))
    if default_name not in places:
        default_name = all_names[0]

    selected = st.selectbox(
        "Select a platform to analyze",
        all_names,
        index=all_names.index(default_name),
        format_func=label,
        key="report_place_select",
    )

    place = places[selected]
    analysis = analyze_reviews(place["reviews"])
    score = demo_score(place, analysis)

    st.markdown(f"## {selected}")
    st.write(place["description"])

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Demo score", f"{score}/100")
    m2.metric("Review examples", analysis["total"])
    m3.metric("Flagged examples", len(analysis["findings"]))
    m4.metric("Issue categories", len(analysis["counts"]))

    st.caption(
        "This score is generated by a simple demonstration formula. "
        "It is not a verified quality rating or a trained ML prediction."
    )

    # Perspective and sentiment are shown as review outputs; the five TruthLens
    # measures below follow the uploaded pitch deck: Authenticity, Credibility,
    # Trust, Confidence Score (0-100), and Rank.
    def review_sentiment(review_row):
        perspective, review_text, rating = review_row
        if rating >= 4:
            return "Positive"
        if rating <= 2:
            return "Negative"
        return "Mixed / Neutral"

    sentiment_rows = []
    for _perspective, _review_text, _rating in place["reviews"]:
        _matches = [
            issue for issue, keywords in ISSUE_RULES.items()
            if any(word in _review_text.lower() for word in keywords)
        ]
        sentiment_rows.append({
            "Perspective": _perspective,
            "Sentiment": review_sentiment((_perspective, _review_text, _rating)),
            "Rating": _rating,
            "Review": _review_text,
            "Topic detected": ", ".join(_matches) if _matches else "General experience",
            "Evidence status": "Not independently verified",
        })
    sentiment_df = pd.DataFrame(sentiment_rows)

    st.markdown("## Review signals by person perspective")
    st.caption("See the positive, negative and mixed experiences that feed into the analysis. Demo examples only.")
    sentiment_counts = sentiment_df["Sentiment"].value_counts()
    q1, q2, q3 = st.columns(3)
    q1.metric("Positive reviews", int(sentiment_counts.get("Positive", 0)))
    q2.metric("Negative reviews", int(sentiment_counts.get("Negative", 0)))
    q3.metric("Mixed / neutral", int(sentiment_counts.get("Mixed / Neutral", 0)))
    st.dataframe(
        sentiment_df[["Perspective", "Sentiment", "Rating", "Review", "Topic detected"]],
        use_container_width=True,
        hide_index=True,
    )

    st.markdown("## TruthLens: Five Trust Measures")
    st.caption("Outputs are based on this prototype's illustrative review data and heuristic rules. They are not verified real-world findings.")

    # Conservative demo-only indicators. Authenticity cannot be confirmed without
    # original evidence; credibility is a heuristic signal, not a source certification.
    ratings = [r[2] for r in place["reviews"]]
    avg_rating = (sum(ratings) / len(ratings)) if ratings else 0
    n_reviews = len(place["reviews"])
    matched_issue_count = len(analysis["findings"])
    authenticity = max(20, min(95, 48 + (sum(1 for r in place["reviews"] if len(r[1]) > 20) * 3) - min(20, matched_issue_count)))
    credibility = max(20, min(95, round(35 + avg_rating * 10 + min(10, n_reviews))))
    verified_backing = 0  # no verified-user connector in this demo
    trust = max(10, min(95, round((authenticity * 0.35) + (credibility * 0.35) + (verified_backing * 0.30))))
    confidence_score = max(0, min(100, round((authenticity * 0.30) + (credibility * 0.35) + (trust * 0.35))))

    if confidence_score >= 75 and matched_issue_count <= max(1, n_reviews // 3):
        verdict = "Genuine-like signal"
    elif authenticity < 40 or matched_issue_count >= max(5, n_reviews // 2):
        verdict = "Suspicious signal"
    elif avg_rating < 2.8:
        verdict = "Potentially misleading / needs review"
    else:
        verdict = "Unverified"

    # Rank is within the current demo catalogue and should never be read as an
    # official or live ranking.
    ranking_values = []
    for _name, _item in places.items():
        _a = analyze_reviews(_item["reviews"])
        _avg = _a["average"]
        _score = round(max(0, min(100, 30 + (_avg * 10) - min(20, len(_a["findings"]) * 1.5))))
        ranking_values.append((_name, _score))
    ranking_values.sort(key=lambda x: x[1], reverse=True)
    demo_rank = next((i for i, (nm, _) in enumerate(ranking_values, start=1) if nm == selected), None)

    score_cols = st.columns(5)
    score_cols[0].metric("Authenticity", f"{authenticity}/100")
    score_cols[1].metric("Credibility", f"{credibility}/100")
    score_cols[2].metric("Trust", f"{trust}/100")
    score_cols[3].metric("Confidence score", f"{confidence_score}/100")
    score_cols[4].metric("Demo rank", f"#{demo_rank}" if demo_rank else "—")
    st.markdown(f"### Provisional verdict: **{verdict}**")
    st.progress(confidence_score / 100)
    st.caption(
        "Authenticity and credibility are heuristic demo signals. No verified identity, receipt/photo OCR, "
        "independent source checks, or verified-crowd votes are connected in this version. "
        "Therefore the verdict remains provisional and all claims require human review."
    )

    with st.expander("1. Authenticity — review/evidence integrity signals", expanded=True):
        st.metric("Demo authenticity indicator", f"{authenticity}/100")
        st.dataframe(
            sentiment_df[["Perspective", "Rating", "Review", "Evidence status"]],
            use_container_width=True, hide_index=True,
        )
        st.write("Evidence to collect: original photo or receipt, date/time, source URL, metadata and an unedited copy. This prototype does not perform image forensics or prove a review is authentic.")

    with st.expander("2. Credibility — source reliability signals", expanded=True):
        st.metric("Demo credibility indicator", f"{credibility}/100")
        st.dataframe(
            sentiment_df[["Perspective", "Sentiment", "Rating", "Review"]],
            use_container_width=True, hide_index=True,
        )
        st.write("Source checks to record: who published the claim, whether the visit/transaction is supported, whether the source is independent, and whether the date/context matches. Source credibility is not verified automatically.")

    with st.expander("3. Trust — independent backing", expanded=True):
        st.metric("Verified independent backing", "0 connected votes")
        st.write("The pitch deck proposes verified visitors/customers and trust-weighted votes. No OTP/device verification or verified-user voting service is connected in this prototype, so this measure is intentionally not presented as confirmed crowd support.")
        st.dataframe(
            sentiment_df[["Perspective", "Sentiment", "Review", "Evidence status"]],
            use_container_width=True, hide_index=True,
        )

    with st.expander("4. Confidence Score — 0 to 100", expanded=True):
        st.metric("Provisional confidence score", f"{confidence_score}/100")
        st.write(f"**Current provisional verdict:** {verdict}")
        st.write("The score combines the demo authenticity, credibility and trust indicators. It is a prototype calculation, not a calibrated probability that a claim is true.")
        st.dataframe(
            pd.DataFrame([{
                "Measure": "Authenticity", "Score": authenticity,
            }, {
                "Measure": "Credibility", "Score": credibility,
            }, {
                "Measure": "Trust", "Score": trust,
            }, {
                "Measure": "Combined confidence score", "Score": confidence_score,
            }]),
            use_container_width=True, hide_index=True,
        )

    with st.expander("5. Rank — comparison with similar selected delivery platforms", expanded=True):
        st.metric("Demo catalogue rank", f"#{demo_rank} of {len(ranking_values)}")
        rank_df = pd.DataFrame([
            {"Rank": i, "Platform": nm, "Demo score": sc}
            for i, (nm, sc) in enumerate(ranking_values, start=1)
        ])
        st.dataframe(rank_df, use_container_width=True, hide_index=True)
        st.caption("Ranks are calculated from illustrative examples in this local catalogue only—not live reviews, verified facts, or an official recommendation.")

    st.markdown("## Claim → Evidence → Verdict")
    with st.form("claim_check_form"):
        claim_text = st.text_area(
            "Paste a claim or review about this place",
            placeholder="Example: The visitor area was closed on the date of my visit.",
        )
        evidence_text = st.text_area(
            "Evidence or source details (optional)",
            placeholder="Add an official URL, receipt details, photo/date description, document reference, or say what evidence is missing.",
        )
        claim_submitted = st.form_submit_button("Check claim")
    if claim_submitted:
        if not claim_text.strip():
            st.warning("Enter a claim first.")
        else:
            claim_lower = claim_text.lower()
            claim_hits = [topic for topic, words in ISSUE_RULES.items() if any(w in claim_lower for w in words)]
            st.markdown("### Extracted checkable claim")
            st.write(claim_text.strip())
            st.markdown("### Initial claim assessment")
            if evidence_text.strip():
                st.info("UNVERIFIED — evidence details supplied, but this prototype has not authenticated them or checked independent sources.")
            else:
                st.warning("UNVERIFIED — no supporting evidence details supplied yet.")
            st.write("**Possible topics detected:** " + (", ".join(claim_hits) if claim_hits else "No specific topic matched by the demo rules"))
            st.write("**Next checks:** validate source credibility, evidence date and authenticity; compare with independent sources; seek verified visitor/customer confirmation; escalate serious or disputed cases for human review.")
            st.caption("The app does not automatically declare a claim genuine, suspicious or misleading from text alone.")

    st.markdown("## Negative Review Intelligence")

    if not analysis["findings"]:
        st.success(
            "No examples matched the current rules. This does not prove that "
            "there are no negative reviews."
        )
    else:
        a, b, c = st.columns(3)
        a.metric("Flagged examples", len(analysis["findings"]))
        b.metric(
            "Perspectives",
            len({x["Perspective"] for x in analysis["findings"]}),
        )
        c.metric("Issue types", len(analysis["counts"]))

        st.markdown("### Recurring issue categories")
        issue_table = pd.DataFrame([
            {"Issue": issue, "Mentions": count}
            for issue, count in analysis["counts"].most_common()
        ])
        st.dataframe(issue_table, use_container_width=True, hide_index=True)

        st.markdown("### Findings by perspective")
        perspectives = sorted({
            item["Perspective"] for item in analysis["findings"]
        })

        for perspective in perspectives:
            group = [
                item for item in analysis["findings"]
                if item["Perspective"] == perspective
            ]

            with st.expander(
                f"{perspective} — {len(group)} flagged example(s)",
                expanded=True,
            ):
                for number, item in enumerate(group, start=1):
                    st.markdown(
                        f"**Example {number} · Rating: {item['Rating']}/5**"
                    )
                    st.write(item["Review"])
                    st.write("**Detected topics:** " + ", ".join(item["Issues"]))

                    for issue in item["Issues"]:
                        suggestion = IMPROVEMENTS.get(
                            issue,
                            "Review the complaint and investigate before taking action.",
                        )
                        st.info(f"**Suggested action — {issue}:** {suggestion}")

                    evidence = st.text_area(
                        "Required evidence / source details",
                        key=f"evidence_{selected}_{perspective}_{number}",
                        placeholder=(
                            "Enter a source name, document date, receipt details, "
                            "official URL, or description of relevant evidence."
                        ),
                    )

                    evidence_key = f"{selected}|{perspective}|{number}"
                    if not evidence.strip():
                        st.warning("Evidence required: add a source, dated record, URL, receipt, photo/document description, or write what evidence still needs to be collected. This finding cannot be marked ready yet.")
                    else:
                        st.success("Evidence note recorded for human verification — not independently authenticated.")
                        st.caption(
                            "Next check: source credibility, date, authenticity, context, "
                            "and whether the evidence directly supports or contradicts the review claim."
                        )
                        st.session_state.setdefault("evidence_notes", {})[evidence_key] = evidence.strip()
                    st.divider()

        st.markdown("### Improvement priorities")
        for issue, count in analysis["counts"].most_common(3):
            st.markdown(
                f"- **{issue} ({count} mention(s)):** "
                f"{IMPROVEMENTS.get(issue, 'Investigate the complaint and document corrective action.')}"
            )

    # Machine-learning topic grouping (TF-IDF + KMeans) when scikit-learn is installed.
    st.markdown("## AI / ML Review Intelligence")
    st.caption("Local ML groups similar review wording; the rule-based issue detector above flags specific complaint topics. Both are decision-support signals, not verified facts.")
    review_texts = [row[1] for row in place["reviews"]]
    if len(review_texts) >= 3:
        try:
            from sklearn.feature_extraction.text import TfidfVectorizer
            from sklearn.cluster import KMeans
            vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
            matrix = vectorizer.fit_transform(review_texts)
            cluster_count = min(3, len(review_texts))
            model = KMeans(n_clusters=cluster_count, random_state=42, n_init=10)
            cluster_ids = model.fit_predict(matrix)
            cluster_df = pd.DataFrame({
                "ML topic group": [f"Group {int(cid) + 1}" for cid in cluster_ids],
                "Perspective": [row[0] for row in place["reviews"]],
                "Review example": review_texts,
            }).sort_values(["ML topic group", "Perspective"])
            st.dataframe(cluster_df, use_container_width=True, hide_index=True)
            st.caption("Model: TF-IDF text features + KMeans clustering. These are automatically grouped text patterns, not trained truth labels.")
        except ImportError:
            st.info("Optional ML package missing. Install it with: python -m pip install scikit-learn")
        except ValueError as exc:
            st.info(f"ML grouping could not run on this small sample: {exc}")

    st.markdown("## LLM-assisted improvement suggestions")
    st.write("An LLM can draft practical improvements from the currently selected platform's flagged examples. Evidence and recommendations still need human verification.")
    if st.button("Generate improvement plan with LLM", key="llm_improvement_plan"):
        if not llm_api_key.strip():
            st.warning("Enter your OpenAI API key in the sidebar first. You can still use the local analysis without it.")
        else:
            flagged_payload = [
                {"perspective": x["Perspective"], "rating": x["Rating"], "review_example": x["Review"], "issues": x["Issues"]}
                for x in analysis["findings"]
            ]
            prompt = (
                "You are a careful customer-experience improvement assistant. Analyze these illustrative review examples for "
                + selected + ". Identify recurring negative experiences, separate evidence from assumptions, and propose a concise prioritized action plan. "
                "Do not claim these are real reviews or state allegations as facts. Mention what evidence should be collected. Data: "
                + json.dumps(flagged_payload, ensure_ascii=False)
            )
            request_body = json.dumps({
                "model": "gpt-4o-mini",
                "messages": [
                    {"role": "system", "content": "Be evidence-aware, concise, and explicit about uncertainty."},
                    {"role": "user", "content": prompt},
                ],
                "temperature": 0.2,
            }).encode("utf-8")
            req = urllib.request.Request(
                "https://api.openai.com/v1/chat/completions",
                data=request_body,
                headers={"Authorization": "Bearer " + llm_api_key.strip(), "Content-Type": "application/json"},
                method="POST",
            )
            try:
                with urllib.request.urlopen(req, timeout=45) as response:
                    result_json = json.loads(response.read().decode("utf-8"))
                llm_text = result_json["choices"][0]["message"]["content"]
                st.markdown("### Suggested action plan")
                st.write(llm_text)
                st.caption("Generated by gpt-4o-mini using demo review examples. Check all recommendations and gather real evidence before acting.")
            except urllib.error.HTTPError as exc:
                st.error(f"LLM request failed (HTTP {exc.code}). Check API key, API access and billing, then try again.")
            except Exception as exc:
                st.error(f"Could not reach the LLM service: {exc}")

    st.markdown("## Review examples used in this demo")
    review_df = pd.DataFrame([
        {
            "Perspective": perspective,
            "Rating": rating,
            "Review text": text,
            "Data status": "Illustrative demo text",
        }
        for perspective, text, rating in place["reviews"]
    ])
    st.dataframe(review_df, use_container_width=True, hide_index=True)

    st.download_button(
        "Download review examples as CSV",
        data=review_df.to_csv(index=False).encode("utf-8"),
        file_name="realitylens_demo_reviews.csv",
        mime="text/csv",
    )

# -------------------- COMPARE --------------------
with compare_tab:
    st.subheader("Compare delivery apps")

    compare_names = st.multiselect(
        "Choose platforms to compare",
        all_names if "all_names" in globals() else list(places.keys()),
        default=list(places.keys())[:2],
        format_func=label,
    )

    if compare_names:
        rows = []
        for name in compare_names:
            item = places[name]
            result = analyze_reviews(item["reviews"])
            most_common = (
                result["counts"].most_common(1)[0][0]
                if result["counts"] else "No match"
            )
            rows.append({
                "Platform": name,
                "Category": item["category"],
                "City": item["city"],
                "Price": item["price"],
                "Demo score /100": demo_score(item, result),
                "Review examples": result["total"],
                "Flagged examples": len(result["findings"]),
                "Most common issue": most_common,
            })

        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
        st.caption(
            "This comparison uses illustrative demo examples only; it is not a ranking of actual platform performance."
        )
    else:
        st.info("Select at least one place to compare.")

# -------------------- SAVED --------------------
with saved_tab:
    st.subheader("Saved platforms")
    save_name = st.selectbox(
        "Choose a platform",
        list(places.keys()),
        format_func=label,
        key="save_name",
    )

    if st.button("Save platform"):
        saved = st.session_state.get("saved_places", [])
        if save_name not in saved:
            saved.append(save_name)
        st.session_state["saved_places"] = saved
        st.success("Platform saved for this session.")

    saved = st.session_state.get("saved_places", [])
    if saved:
        for name in saved:
            st.markdown(f"- **{name}** — {places[name]['category']}, {places[name]['city']}")
    else:
        st.info("No saved platforms yet. Saved items last for this session.")

# -------------------- SUBMIT CLAIM --------------------
with submit_tab:
    st.subheader("Submit a claim about a delivery app")
    st.write("Submit a checkable claim about delivery time, order accuracy, item condition, fees, refunds, app listings or customer support.")
    with st.form("submit_claim_tab_form"):
        submit_place = st.selectbox("Place", list(places.keys()), format_func=label, key="submit_claim_place")
        submit_claim = st.text_area("Paste any review, post or claim", placeholder="Example: The app charged a fee that was not shown before checkout.")
        submit_proof = st.text_area("Add proof or source details", placeholder="Official URL, receipt/document details, photo and visit date, or other source information.")
        submit_button = st.form_submit_button("Extract claim and assess")
    if submit_button:
        if not submit_claim.strip():
            st.warning("Please enter a claim or review.")
        else:
            lowered = submit_claim.lower()
            matched_topics = [topic for topic, words in ISSUE_RULES.items() if any(word in lowered for word in words)]
            st.markdown("### 1. Input")
            st.write(f"**Place:** {submit_place}")
            st.write(submit_claim.strip())
            st.markdown("### 2. Extract")
            st.write("**Candidate claim:** " + submit_claim.strip())
            st.write("**Topics detected:** " + (", ".join(matched_topics) if matched_topics else "No rule-based topic match"))
            st.markdown("### 3. Verify")
            if submit_proof.strip():
                st.write("**Evidence supplied:** " + submit_proof.strip())
                st.warning("Evidence provided but not independently authenticated.")
            else:
                st.warning("No evidence supplied yet. Add an independent source, dated record, receipt, photo/document or verified visitor confirmation.")
            st.markdown("### 4. Verdict")
            st.info("UNVERIFIED — a human must review evidence and independent sources before assigning a final verdict.")
            st.markdown("### 5. Share")
            verdict_card = (
                f"TRUTHLENS — PROVISIONAL CLAIM CARD\nPlatform: {submit_place}\n"
                f"Claim: {submit_claim.strip()}\nStatus: UNVERIFIED\n"
                "Note: Evidence has not been independently authenticated."
            )
            st.code(verdict_card)
            st.download_button("Download provisional verdict card", verdict_card, file_name="truthlens_verdict_card.txt", mime="text/plain")

# -------------------- RANKED FEED --------------------
with feed_tab:
    st.subheader("Ranked feed — delivery platforms and claims")
    st.caption("Illustrative catalogue ranking, not a ranking of real-time public opinion.")
    feed_rows = []
    for _name, _item in places.items():
        _analysis = analyze_reviews(_item["reviews"])
        _score = round(max(0, min(100, 30 + (_analysis["average"] * 10) - min(20, len(_analysis["findings"]) * 1.5))))
        _verdict = "Unverified"
        if _score >= 70 and len(_analysis["findings"]) <= 3:
            _verdict = "Genuine-like signal (demo)"
        elif len(_analysis["findings"]) >= 6:
            _verdict = "Suspicious signal (demo)"
        feed_rows.append({
            "Platform": _name,
            "Category": _item["category"],
            "City": _item["city"],
            "Demo score": _score,
            "Sample reviews": _analysis["total"],
            "Flagged examples": len(_analysis["findings"]),
            "Status": _verdict,
        })
    feed_df = pd.DataFrame(feed_rows).sort_values(["Demo score", "Platform"], ascending=[False, True])
    feed_df.insert(0, "Rank", range(1, len(feed_df) + 1))
    st.dataframe(feed_df, use_container_width=True, hide_index=True)
    st.caption("The deck's final verdict options are Genuine, Suspicious, Misleading and Unverified. Here they are represented only as provisional demo signals; verified verdicts require evidence and human review.")

# -------------------- ABOUT --------------------
with about_tab:
    st.subheader("About TruthLens / RealityLensAI")
    st.write(
        "A fact-check layer for claims about delivery and shopping apps—not another review platform. "
        "Reviews are raw input; the prototype organises claims, highlights evidence gaps, "
        "compares perspectives and displays a provisional Trust Score."
    )

    st.markdown("### Core workflow")
    st.markdown("""
    1. **Input:** paste a review, post or claim and optionally add proof.
    2. **Extract:** identify a checkable claim and likely topic.
    3. **Verify:** review evidence, source reliability, independent signals and verified-user confirmation.
    4. **Verdict:** Genuine, Suspicious, Misleading or Unverified—final decisions require evidence and human review.
    5. **Share:** download a provisional verdict card.
    """)

    st.markdown("### Five TrustLens measures")
    st.markdown("""
    - **Authenticity:** whether content or evidence appears genuine.
    - **Credibility:** whether the source is reliable.
    - **Trust:** whether independent sources and verified visitors/customers support the claim.
    - **Confidence Score (0–100):** one weighted, explainable confidence indicator.
    - **Rank:** position among similar claims/places in the demo catalogue.
    """)

    st.markdown("### Intelligence under the hood — planned / prototype components")
    st.markdown("""
    - **Graph and anomaly ML:** detect suspicious account clusters and possible review rings.
    - **Vision and OCR:** inspect receipts, photos, reused images and available metadata.
    - **LLM with retrieval-augmented generation (RAG):** extract claims and compare them with source material.
    - **Time-series analysis:** flag sudden bursts and coordinated posting times.
    - **Ensemble scoring:** combine signals into one explainable confidence score.
    - **Human in the loop:** review edge cases, appeals and serious verdicts; use reviewed cases to improve the system.
    """)

    st.markdown("### Anti-faking controls — planned")
    st.markdown("""
    - Verified identity through OTP/device checks and one person per account.
    - Proof of experience so verified customers/visitors have stronger voting weight.
    - Image authenticity checks using metadata and edit/reuse detection.
    - Vote-ring defence that discounts coordinated accounts.
    - Trust-weighted votes where accurate contributions earn influence.
    - Human review and appeal for serious or disputed verdicts.
    """)

    st.markdown("### Participation and business value — planned")
    st.markdown("""
    - Low-friction participation through one-tap, voice, WhatsApp and regional-language flows.
    - Privacy-aware participation: anonymous to the business, verified by the service.
    - Status updates when a business responds or fixes an issue.
    - Recognition through badges and trust levels, not cash for claims.
    - Businesses could check suspicious claims, appeal a verdict and earn a fact-verified badge when evidence supports it.
    """)

    st.markdown("### Roadmap and success metrics")
    st.markdown("""
    - **Week 1:** choose one niche and city, define verdict labels.
    - **Week 2:** build submit, verdict and ranked-feed screens with claim scoring.
    - **Week 3:** add crowd voting and trust scores.
    - **Week 4:** test with 20–50 real users.
    - **Phase 2:** public issues, location and authority routing.
    - **Success metrics:** verdict accuracy, share of users who vote, verdict cards shared, and repeat usage.
    """)

    st.markdown("### Current prototype limitations")
    st.markdown("""
    - Catalogue review text is illustrative, not genuine customer/visitor feedback.
    - No OTP identity verification, verified-user voting, image-forensics service, live source retrieval or authority-routing integration is connected.
    - The numeric measures and ranking are heuristic demo outputs, not trained or calibrated truth probabilities.
    - Official source links are reference starting points; they do not verify individual claims.
    """)

    st.markdown("### Delivery platform categories")
    st.write("Food Delivery • Quick Commerce • Grocery Delivery • Online Shopping")

