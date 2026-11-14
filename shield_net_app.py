import streamlit as st
import pandas as pd
from html import escape
import math

st.set_page_config(page_title="Shield-Net | Matching Demo", page_icon="S", layout="wide")
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@500;600;700;800&display=swap');
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
.stApp { background: #f3f6f5; color: #1b2b37; }
[data-testid="stHeader"] { background: rgba(243,246,245,.88); }
[data-testid="stSidebar"] { background: #edf2f0; border-right: 1px solid #dce5e1; }
[data-testid="stSidebar"] h2 { color: #155e56; font-family: 'Manrope',sans-serif; }
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
[data-testid="stSidebar"] [data-testid="stCaptionContainer"],
[data-testid="stSidebar"] [data-testid="stWidgetLabel"],
[data-testid="stSidebar"] [data-testid="stWidgetLabel"] p,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] label p { color:#344b50 !important; opacity:1 !important; }
[data-testid="stSidebar"] [data-testid="stSlider"] [data-testid="stThumbValue"] { color:#155e56 !important; font-weight:700 !important; }
h1, h2, h3, h4 { font-family: 'Manrope', sans-serif; letter-spacing: -.035em; color: #173142; }
h2 { padding-top: 4px; }
.block-container { max-width: 1440px; padding-top: 1.6rem; padding-bottom: 2rem; }
.hero { background: radial-gradient(circle at 88% 12%,rgba(120,207,177,.24),transparent 27%), linear-gradient(115deg,#102b3a,#174c55); color: white; padding: 30px 34px; border-radius: 20px; margin: 0 0 24px; box-shadow: 0 12px 30px rgba(19,58,65,.12); }
.hero h1 { color: white; margin: 7px 0 6px; font-size: 34px; }
.hero p { color: #d0e1e1; margin: 0; font-size: 15px; }
.kicker { color:#a9d8c8; text-transform:uppercase; letter-spacing:.15em; font-weight:700; font-size:11px; }
.note { background:#e9f3f0; border:1px solid #d4e8e0; border-left:4px solid #168474; padding:14px 17px; border-radius:10px; color:#294a4d; font-size:13px; }
.decision-card { background:#e8f4f0; border:1px solid #cbe4da; border-left:5px solid #168474; border-radius:13px; padding:17px 20px; color:#243b3d !important; }
.decision-card.attention { background:#fff4d8; border-color:#f0dfb2; border-left-color:#d39128; }
.decision-card p { color:#243b3d !important; margin:0; font-size:15px; line-height:1.55; font-weight:600; }
.decision-card.attention p { color:#493a20 !important; }
[data-testid="stMetric"] { background:#fff; border:1px solid #e2eae6; border-radius:14px; padding:16px 18px; box-shadow:0 4px 14px rgba(26,56,50,.045); }
[data-testid="stMetricLabel"] { color:#617181; font-size:12px; font-weight:600; }
[data-testid="stMetricValue"] { color:#173c43; font-family:'Manrope',sans-serif; }
[data-testid="stTabs"] [role="tablist"] { gap:8px; border-bottom:1px solid #dce5e1; }
[data-testid="stTabs"] button[role="tab"],
[data-testid="stTabs"] button[role="tab"] p,
[data-testid="stTabs"] [data-baseweb="tab"] { border-radius:10px 10px 0 0; padding:10px 16px; color:#40575d !important; opacity:1 !important; }
[data-testid="stTabs"] button[role="tab"][aria-selected="true"],
[data-testid="stTabs"] button[role="tab"][aria-selected="true"] p,
[data-testid="stTabs"] [data-baseweb="tab"][aria-selected="true"] { color:#126b60 !important; border-bottom:3px solid #168474; font-weight:700; }
[data-testid="stDataFrame"] { border:1px solid #e2eae6; border-radius:12px; overflow:hidden; }
div.stButton > button[kind="primary"] { background:linear-gradient(100deg,#16796c,#209780); border:0; border-radius:10px; min-height:48px; font-weight:700; box-shadow:0 5px 14px rgba(22,121,108,.17); }
div.stButton > button[kind="primary"]:hover { background:linear-gradient(100deg,#12685d,#188570); border:0; }
hr { border-color:#dce5e1; }
</style>
""", unsafe_allow_html=True)

DEMAND_A = pd.DataFrame([
    {"Request ID":"H-101", "Organization":"Harborview Medical", "Location":"Seattle", "Latitude":47.598, "Longitude":-122.325, "Demand Quantity":120, "Urgency":1, "Product Preference":"Fully assembled", "Organization Type":"Hospital"},
    {"Request ID":"H-102", "Organization":"Northgate Clinic", "Location":"Seattle", "Latitude":47.707, "Longitude":-122.325, "Demand Quantity":80, "Urgency":2, "Product Preference":"Fully assembled", "Organization Type":"Clinic"},
    {"Request ID":"H-103", "Organization":"Rainier Community Care", "Location":"Tacoma", "Latitude":47.252, "Longitude":-122.444, "Demand Quantity":60, "Urgency":2, "Product Preference":"Kit", "Organization Type":"Community care"},
    {"Request ID":"H-104", "Organization":"Soundview Urgent Care", "Location":"Tacoma", "Latitude":47.240, "Longitude":-122.433, "Demand Quantity":50, "Urgency":3, "Product Preference":"Fully assembled", "Organization Type":"Urgent care"},
])
SUPPLY_A = pd.DataFrame([
    {"Supplier ID":"S-01", "Supplier":"Evergreen Plastics", "Location":"Seattle", "Latitude":47.560, "Longitude":-122.315, "Daily Capacity":150, "Product Type":"Fully assembled", "Contact Information":"ops@evergreen.example"},
    {"Supplier ID":"S-02", "Supplier":"Cascadia Makers", "Location":"Tacoma", "Latitude":47.268, "Longitude":-122.430, "Daily Capacity":75, "Product Type":"Kit", "Contact Information":"hello@cascadia.example"},
    {"Supplier ID":"S-03", "Supplier":"Puget Safety Works", "Location":"Seattle", "Latitude":47.680, "Longitude":-122.210, "Daily Capacity":90, "Product Type":"Fully assembled", "Contact Information":"supply@puget.example"},
    {"Supplier ID":"S-04", "Supplier":"Tacoma Shield Collective", "Location":"Tacoma", "Latitude":47.252, "Longitude":-122.450, "Daily Capacity":45, "Product Type":"Fully assembled", "Contact Information":"orders@tacoma.example"},
])
DEMAND_B = pd.DataFrame([
    {"Request ID":"H-201", "Organization":"Metro General", "Location":"Chicago", "Latitude":41.880, "Longitude":-87.640, "Demand Quantity":200, "Urgency":1, "Product Preference":"Fully assembled", "Organization Type":"Hospital"},
    {"Request ID":"H-202", "Organization":"Westside Pediatrics", "Location":"Chicago", "Latitude":41.920, "Longitude":-87.750, "Demand Quantity":90, "Urgency":2, "Product Preference":"Kit", "Organization Type":"Hospital"},
    {"Request ID":"H-203", "Organization":"Lake County Health", "Location":"Evanston", "Latitude":42.040, "Longitude":-87.690, "Demand Quantity":100, "Urgency":2, "Product Preference":"Fully assembled", "Organization Type":"Healthcare facility"},
])
SUPPLY_B = pd.DataFrame([
    {"Supplier ID":"S-11", "Supplier":"Midwest Fabrication", "Location":"Chicago", "Latitude":41.890, "Longitude":-87.620, "Daily Capacity":180, "Product Type":"Fully assembled", "Contact Information":"team@midwest.example"},
    {"Supplier ID":"S-12", "Supplier":"Lakeshore 3D Lab", "Location":"Evanston", "Latitude":42.050, "Longitude":-87.680, "Daily Capacity":80, "Product Type":"Kit", "Contact Information":"info@lakeshore.example"},
    {"Supplier ID":"S-13", "Supplier":"Civic Shield Co-op", "Location":"Chicago", "Latitude":41.810, "Longitude":-87.600, "Daily Capacity":100, "Product Type":"Fully assembled", "Contact Information":"civic@shield.example"},
    {"Supplier ID":"S-14", "Supplier":"North Shore Shield Works", "Location":"Evanston", "Latitude":42.030, "Longitude":-87.690, "Daily Capacity":60, "Product Type":"Fully assembled", "Contact Information":"dispatch@northshore.example"},
])

URGENCY_WEIGHTS = {1: 3, 2: 2, 3: 1}

def demo_matches(demand, supply, distance_weight=1.5):
    """Greedy approximation of weighted shortage and transport-distance costs."""
    remaining = dict(zip(supply["Supplier ID"], supply["Daily Capacity"].astype(int)))
    suppliers = supply.to_dict("records")
    rows = []
    def distance_km(supplier, requester):
        lat1, lon1 = math.radians(float(supplier["Latitude"])), math.radians(float(supplier["Longitude"]))
        lat2, lon2 = math.radians(float(requester["Latitude"])), math.radians(float(requester["Longitude"]))
        dlat, dlon = lat2-lat1, lon2-lon1
        hav = math.sin(dlat/2)**2 + math.cos(lat1)*math.cos(lat2)*math.sin(dlon/2)**2
        return 6371 * 2 * math.atan2(math.sqrt(hav), math.sqrt(1-hav))

    requests = demand.to_dict("records")
    candidates = []
    for req in requests:
        urgency = int(req["Urgency"])
        for sup in suppliers:
            if str(sup["Product Type"]).strip().casefold() != str(req["Product Preference"]).strip().casefold():
                continue
            distance = distance_km(sup, req)
            # Objective change from allocating one unit: avoid weighted shortfall, pay distance cost.
            benefit = 100 * URGENCY_WEIGHTS[urgency] - distance_weight * distance
            candidates.append((benefit, distance, urgency, str(req["Request ID"]), sup["Supplier"], req, sup))

    # Greedily take the pair with the largest positive objective improvement first.
    candidates.sort(key=lambda item: (-item[0], item[1], item[2], item[3], item[4]))
    left_demand = {str(req["Request ID"]): int(req["Demand Quantity"]) for req in requests}
    for benefit, distance, urgency, request_id, _, req, sup in candidates:
        if benefit <= 0:
            break
        qty = min(left_demand[request_id], remaining[sup["Supplier ID"]])
        if qty <= 0:
            continue
        rows.append({"Request ID":req["Request ID"], "Requester":req["Organization"], "Requester Location":req["Location"], "Supplier":sup["Supplier"], "Supplier Location":sup["Location"], "Product Type":req["Product Preference"], "Units":qty, "Urgency":urgency, "Distance (km)":round(distance, 1)})
        remaining[sup["Supplier ID"]] -= qty
        left_demand[request_id] -= qty

    for req in requests:
        need = left_demand[str(req["Request ID"])]
        if need > 0:
            rows.append({"Request ID":req["Request ID"], "Requester":req["Organization"], "Requester Location":req["Location"], "Supplier":"Unfilled demand", "Supplier Location":"-", "Product Type":req["Product Preference"], "Units":need, "Urgency":req["Urgency"], "Distance (km)":"-"})
    columns = ["Request ID", "Requester", "Requester Location", "Supplier", "Supplier Location", "Product Type", "Units", "Urgency", "Distance (km)"]
    return pd.DataFrame(rows, columns=columns)

def validate_inputs(demand, supply):
    errors = []
    if demand.empty:
        errors.append("Add at least one healthcare request.")
    if supply.empty:
        errors.append("Add at least one supplier.")
    demand_required = ["Request ID", "Organization", "Location", "Latitude", "Longitude", "Demand Quantity", "Urgency", "Product Preference", "Organization Type"]
    supply_required = ["Supplier ID", "Supplier", "Location", "Latitude", "Longitude", "Daily Capacity", "Product Type", "Contact Information"]
    for label, frame, columns in [("Requester", demand, demand_required), ("Supplier", supply, supply_required)]:
        for column in columns:
            if column not in frame.columns:
                errors.append(f"{label} data is missing the {column} field.")
            elif frame[column].isna().any() or frame[column].astype(str).str.strip().eq("").any():
                errors.append(f"Fill in all {column} values in the {label.lower()} table.")
    if "Request ID" in demand and demand["Request ID"].duplicated().any():
        errors.append("Each Request ID must be unique.")
    if "Supplier ID" in supply and supply["Supplier ID"].duplicated().any():
        errors.append("Each Supplier ID must be unique.")
    for frame, column, label in [(demand, "Demand Quantity", "Demand Quantity"), (supply, "Daily Capacity", "Daily Capacity")]:
        if column in frame:
            values = pd.to_numeric(frame[column], errors="coerce")
            if values.isna().any() or not values.map(math.isfinite).all() or (values < 0).any() or (values % 1 != 0).any():
                errors.append(f"{label} must contain finite, non-negative whole numbers.")
    for label, frame in [("Requester", demand), ("Supplier", supply)]:
        for coordinate, lower, upper in [("Latitude", -90, 90), ("Longitude", -180, 180)]:
            if coordinate in frame:
                values = pd.to_numeric(frame[coordinate], errors="coerce")
                if values.isna().any() or not values.map(math.isfinite).all() or (values < lower).any() or (values > upper).any():
                    errors.append(f"{label} {coordinate.lower()} values must be valid coordinates ({lower} to {upper}).")
    if "Urgency" in demand:
        urgency = pd.to_numeric(demand["Urgency"], errors="coerce")
        if urgency.isna().any() or not urgency.isin([1, 2, 3]).all():
            errors.append("Urgency must be 1, 2, or 3 (1 is highest priority).")
    if "Product Preference" in demand and not demand["Product Preference"].isin(["Fully assembled", "Kit"]).all():
        errors.append("Product Preference must be Fully assembled or Kit.")
    if "Product Type" in supply and not supply["Product Type"].isin(["Fully assembled", "Kit"]).all():
        errors.append("Supplier Product Type must be Fully assembled or Kit.")
    return errors

def build_decision_recommendations(demand, supply, result):
    """Turn the illustrative allocation into coordinator-friendly decision notes."""
    allocated_rows = result[result["Supplier"] != "Unfilled demand"]
    shortfall_rows = result[result["Supplier"] == "Unfilled demand"]
    total_requested = int(demand["Demand Quantity"].sum())
    total_allocated = int(allocated_rows["Units"].sum()) if not allocated_rows.empty else 0
    total_shortfall = total_requested - total_allocated
    shortfall_by_request = shortfall_rows.set_index("Request ID")["Units"].to_dict() if not shortfall_rows.empty else {}
    allocated_by_supplier = allocated_rows.groupby("Supplier")["Units"].sum().to_dict() if not allocated_rows.empty else {}
    recommendations = []

    for req in demand.sort_values("Urgency").to_dict("records"):
        request_id = req["Request ID"]
        assigned = allocated_rows[allocated_rows["Request ID"] == request_id]
        shipped = int(assigned["Units"].sum()) if not assigned.empty else 0
        unmet = int(shortfall_by_request.get(request_id, 0))
        demand_qty = int(req["Demand Quantity"])
        if demand_qty == 0:
            detail = "No shipment is needed because requested quantity is zero."
        elif not assigned.empty:
            sources = "; ".join(
                f'{int(row["Units"]):,} from {escape(str(row["Supplier"]))} ({float(row["Distance (km)"]):.1f} km)'
                for _, row in assigned.iterrows()
            )
            detail = f"Recommend allocating {shipped:,} of {demand_qty:,} requested units: {sources}."
            if unmet:
                detail += f" {unmet:,} units remain unmet; seek additional compatible supply at urgency level {int(req['Urgency'])}."
            else:
                detail += " Request is fully covered; approve the proposed allocation."
        elif unmet:
            compatible = supply[(supply["Product Type"] == req["Product Preference"]) & (supply["Daily Capacity"] > 0)]
            if compatible.empty:
                detail = f"No compatible supplier capacity is available for the {req['Product Preference']} preference. Source compatible stock for all {unmet:,} units."
            else:
                detail = f"No allocation was selected for the {unmet:,} units. Review compatible capacity, location coordinates, and the distance penalty."
        else:
            detail = "No shipment is needed."
        recommendations.append({"Request ID":request_id, "Organization":req["Organization"], "Urgency":int(req["Urgency"]), "Recommendation":detail})

    utilization = []
    for sup in supply.to_dict("records"):
        used = int(allocated_by_supplier.get(sup["Supplier"], 0))
        capacity = int(sup["Daily Capacity"])
        remaining = max(0, capacity - used)
        compatible_open = demand[
            (demand["Product Preference"] == sup["Product Type"])
            & (demand["Request ID"].map(shortfall_by_request).fillna(0).astype(int) > 0)
        ]
        if capacity == 0:
            reason = "No daily capacity was entered."
        elif remaining == 0:
            reason = "All listed capacity is allocated."
        elif compatible_open.empty:
            reason = "No remaining open demand for this product; retain the balance as reserve."
        else:
            reason = "Capacity remains while compatible demand is open; review the distance penalty and score-ranked matches."
        utilization.append({"Supplier":sup["Supplier"], "Product Type":sup["Product Type"], "Daily Capacity":capacity, "Allocated":used, "Unallocated":remaining, "Why capacity remains":reason})

    if total_shortfall == 0:
        summary = f"Recommend approving the proposed plan: all {total_requested:,} requested face shields are covered across {len(allocated_rows)} supplier-requester allocations."
    else:
        priority_open = demand[demand["Request ID"].isin(shortfall_by_request)].sort_values("Urgency")
        focus = ", ".join(escape(str(name)) for name in priority_open["Organization"].tolist())
        summary = f"Approve the {total_allocated:,} suggested allocations, then prioritize sourcing the remaining {total_shortfall:,} shields for {focus}. Review the supplier utilization table for compatible unused capacity."
    return summary, recommendations, pd.DataFrame(utilization)

def build_flow_svg(flows):
    """Build a dependency-free, styled Sankey diagram for suggested matches."""
    suppliers = flows["Supplier"].drop_duplicates().tolist()
    facilities = flows["Requester"].drop_duplicates().tolist()
    width, node_w, node_h = 1120, 250, 58
    height = max(390, 94 * max(len(suppliers), len(facilities)) + 100)
    source_x, target_x = 28, width - node_w - 28
    top, usable = 88, height - 124
    source_y = {name: top + (i + 0.5) * usable / len(suppliers) for i, name in enumerate(suppliers)}
    target_y = {name: top + (i + 0.5) * usable / len(facilities) for i, name in enumerate(facilities)}
    supplier_totals = flows.groupby("Supplier")["Units"].sum().to_dict()
    facility_totals = flows.groupby("Requester")["Units"].sum().to_dict()
    max_units = max(int(value) for value in flows["Units"])
    pieces = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="{height}px">']
    pieces.append('<defs><linearGradient id="flowRibbon" x1="0" x2="1"><stop offset="0%" stop-color="#168779"/><stop offset="52%" stop-color="#53ae91"/><stop offset="100%" stop-color="#e0a34b"/></linearGradient><linearGradient id="canvas" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#ffffff"/><stop offset="100%" stop-color="#f6faf8"/></linearGradient></defs>')
    pieces.append(f'<rect x="0" y="0" width="{width}" height="100%" rx="22" fill="url(#canvas)" stroke="#e2ebe7"/>')
    pieces.append(f'<text x="{source_x}" y="34" fill="#18796f" font-family="Arial,sans-serif" font-size="11" font-weight="700" letter-spacing="1.5">SUPPLY PARTNERS</text><text x="{source_x}" y="54" fill="#7d8d8d" font-family="Arial,sans-serif" font-size="11">{len(suppliers)} suppliers</text>')
    pieces.append(f'<text x="{target_x}" y="34" fill="#b27a2b" font-family="Arial,sans-serif" font-size="11" font-weight="700" letter-spacing="1.5">HEALTHCARE RECIPIENTS</text><text x="{target_x}" y="54" fill="#7d8d8d" font-family="Arial,sans-serif" font-size="11">{len(facilities)} facilities</text>')
    for row in flows.to_dict("records"):
        sy, ty = source_y[row["Supplier"]], target_y[row["Requester"]]
        amount = int(row["Units"])
        stroke_width = max(4, 38 * amount / max_units)
        distance = row.get("Distance (km)", "Unavailable")
        title = escape(f'{row["Supplier"]} to {row["Requester"]}: {amount:,} shields; {distance} km')
        path = f'M {source_x + node_w} {sy} C {width * .38} {sy}, {width * .62} {ty}, {target_x} {ty}'
        pieces.append(f'<path d="{path}" fill="none" stroke="#ffffff" stroke-opacity=".8" stroke-width="{stroke_width + 5:.1f}" stroke-linecap="round"/>')
        pieces.append(f'<path d="{path}" fill="none" stroke="url(#flowRibbon)" stroke-opacity=".48" stroke-width="{stroke_width:.1f}" stroke-linecap="round"><title>{title}</title></path>')
    for name, cy in source_y.items():
        label = escape(name if len(name) <= 25 else name[:22] + "...")
        pieces.append(f'<rect x="{source_x}" y="{cy-node_h/2}" width="{node_w}" height="{node_h}" rx="14" fill="#ffffff" stroke="#d8e9e3"/>')
        pieces.append(f'<rect x="{source_x}" y="{cy-node_h/2}" width="7" height="{node_h}" rx="3.5" fill="#188576"/>')
        pieces.append(f'<text x="{source_x+20}" y="{cy-3}" fill="#24434a" font-family="Arial,sans-serif" font-size="13" font-weight="700"><title>{escape(name)}</title>{label}</text>')
        pieces.append(f'<text x="{source_x+20}" y="{cy+17}" fill="#82918f" font-family="Arial,sans-serif" font-size="10">{supplier_totals[name]:,} shields allocated</text>')
    for name, cy in target_y.items():
        label = escape(name if len(name) <= 25 else name[:22] + "...")
        pieces.append(f'<rect x="{target_x}" y="{cy-node_h/2}" width="{node_w}" height="{node_h}" rx="14" fill="#ffffff" stroke="#f0e2c9"/>')
        pieces.append(f'<rect x="{target_x+node_w-7}" y="{cy-node_h/2}" width="7" height="{node_h}" rx="3.5" fill="#e3a64a"/>')
        pieces.append(f'<text x="{target_x+16}" y="{cy-3}" fill="#4e4434" font-family="Arial,sans-serif" font-size="13" font-weight="700"><title>{escape(name)}</title>{label}</text>')
        pieces.append(f'<text x="{target_x+16}" y="{cy+17}" fill="#9b8c75" font-family="Arial,sans-serif" font-size="10">{facility_totals[name]:,} shields suggested</text>')
    pieces.append('</svg>')
    return "".join(pieces), height

with st.sidebar:
    st.markdown("## Shield-Net")
    st.caption("Face-shield supply and demand matching")
    scenario = st.selectbox("Choose a sample case", ["Pacific Northwest", "Chicago region"])
    distance_weight = 1.5  # Fixed default; slider removed for a simpler interface.
    st.caption("All organizations and sample quantities are illustrative.")

required_demand_columns = {"Request ID", "Organization", "Location", "Latitude", "Longitude", "Demand Quantity", "Urgency", "Product Preference", "Organization Type"}
required_supply_columns = {"Supplier ID", "Supplier", "Location", "Latitude", "Longitude", "Daily Capacity", "Product Type", "Contact Information"}
schema_changed = (
    "demand" not in st.session_state or "supply" not in st.session_state
    or not required_demand_columns.issubset(st.session_state.demand.columns)
    or not required_supply_columns.issubset(st.session_state.supply.columns)
)
if schema_changed or "scenario" not in st.session_state or st.session_state.scenario != scenario:
    if scenario == "Pacific Northwest":
        st.session_state.demand, st.session_state.supply = DEMAND_A.copy(), SUPPLY_A.copy()
    else:
        st.session_state.demand, st.session_state.supply = DEMAND_B.copy(), SUPPLY_B.copy()
    st.session_state.scenario = scenario
    st.session_state.matches = demo_matches(st.session_state.demand, st.session_state.supply, distance_weight)
    st.session_state.matches_distance_weight = distance_weight
    st.session_state.validation_errors = []

if st.session_state.matches is None and not st.session_state.get("validation_errors"):
    st.session_state.matches = demo_matches(st.session_state.demand, st.session_state.supply, distance_weight)
    st.session_state.matches_distance_weight = distance_weight

st.markdown('<div class="hero"><div class="kicker">PPE coordination dashboard / supply network</div><h1>Match face-shield supply to need</h1><p>Review requests and supplier capacity, then generate an illustrative allocation for coordinator review.</p></div>', unsafe_allow_html=True)
demo_tab, history_tab = st.tabs(["Matching dashboard", "Historical case results"])

with demo_tab:
    st.subheader(f"{scenario}: inputs")
    st.caption("A sample plan is shown on load. Edit the tables, then click Generate matches. Latitude and longitude provide point-to-point distances; sample coordinates are illustrative approximations.")
    demand_tab, supply_tab = st.tabs(["Healthcare requests", "Supplier capacity"])
    with demand_tab:
        st.markdown("#### Healthcare requests")
        st.caption("Urgency uses 1 (highest priority) through 3 (lowest priority). Coordinates determine point-to-point distances; sample coordinates are illustrative, not exact addresses.")
        demand = st.data_editor(
            st.session_state.demand, hide_index=True, use_container_width=True,
            height=min(800, max(180, 36 * (len(st.session_state.demand) + 2) + 12)),
            num_rows="dynamic", key=f"demand_v3_{scenario}",
            column_config={
                "Request ID": st.column_config.TextColumn("Request ID", width="small", required=True),
                "Organization": st.column_config.TextColumn("Organization", width="medium", required=True),
                "Location": st.column_config.TextColumn("Location", width="small", required=True),
                "Latitude": st.column_config.NumberColumn("Latitude", min_value=-90, max_value=90, step=0.001, format="%.3f", width="small", required=True),
                "Longitude": st.column_config.NumberColumn("Longitude", min_value=-180, max_value=180, step=0.001, format="%.3f", width="small", required=True),
                "Demand Quantity": st.column_config.NumberColumn("Demand Quantity", min_value=0, step=1, format="plain", width="small", required=True),
                "Urgency": st.column_config.NumberColumn("Urgency (1-3)", min_value=1, max_value=3, step=1, format="plain", width="small", required=True),
                "Product Preference": st.column_config.SelectboxColumn("Product Preference", options=["Fully assembled", "Kit"], width="medium", required=True),
                "Organization Type": st.column_config.SelectboxColumn("Organization Type", options=["Hospital", "Nursing home", "Healthcare facility", "Clinic", "Urgent care", "Community care"], width="medium", required=True),
            },
        )
        st.session_state.demand = demand
    with supply_tab:
        st.markdown("#### Supplier capacity")
        supply = st.data_editor(
            st.session_state.supply, hide_index=True, use_container_width=True,
            height=min(800, max(180, 36 * (len(st.session_state.supply) + 2) + 12)),
            num_rows="dynamic", key=f"supply_v3_{scenario}",
            column_config={
                "Supplier ID": st.column_config.TextColumn("Supplier ID", width="small", required=True),
                "Supplier": st.column_config.TextColumn("Supplier", width="medium", required=True),
                "Location": st.column_config.TextColumn("Location", width="small", required=True),
                "Latitude": st.column_config.NumberColumn("Latitude", min_value=-90, max_value=90, step=0.001, format="%.3f", width="small", required=True),
                "Longitude": st.column_config.NumberColumn("Longitude", min_value=-180, max_value=180, step=0.001, format="%.3f", width="small", required=True),
                "Daily Capacity": st.column_config.NumberColumn("Daily Capacity", min_value=0, step=1, format="plain", width="small", required=True),
                "Product Type": st.column_config.SelectboxColumn("Product Type", options=["Fully assembled", "Kit"], width="medium", required=True),
                "Contact Information": st.column_config.TextColumn("Contact Information", width="medium", required=True),
            },
        )
        st.session_state.supply = supply

    if st.button("Generate illustrative matches", type="primary", use_container_width=True):
        errors = validate_inputs(demand, supply)
        st.session_state.validation_errors = errors
        st.session_state.matches = None if errors else demo_matches(demand, supply, distance_weight)
        if not errors:
            st.session_state.matches_distance_weight = distance_weight

    if st.session_state.get("validation_errors"):
        st.error("Please correct the input data before generating matches.")
        for error in st.session_state.validation_errors:
            st.write(f"- {error}")

    result = st.session_state.matches
    if result is not None:
        st.divider()
        st.subheader("Matching results")
        requested = int(demand["Demand Quantity"].sum())
        allocated = int(result.loc[result["Supplier"] != "Unfilled demand", "Units"].sum()) if not result.empty else 0
        unmatched = requested - allocated
        fill_rate = 100 * allocated / requested if requested else 0
        distance_values = pd.to_numeric(result.loc[result["Supplier"] != "Unfilled demand", "Distance (km)"], errors="coerce")
        distance_units = result.loc[distance_values.index, "Units"].astype(float)
        average_distance = (distance_values * distance_units).sum() / distance_units[distance_values.notna()].sum() if distance_values.notna().any() else None
        shortfall_rows = result[result["Supplier"] == "Unfilled demand"]
        weighted_shortfall = sum(int(row["Units"]) * URGENCY_WEIGHTS[int(row["Urgency"])] for _, row in shortfall_rows.iterrows())
        unit_km = float((distance_values * distance_units).sum())
        run_distance_weight = st.session_state.get("matches_distance_weight", distance_weight)
        shortfall_cost = 100 * weighted_shortfall
        distance_cost = run_distance_weight * unit_km
        objective_score = shortfall_cost + distance_cost
        if run_distance_weight != distance_weight:
            st.info("Distance penalty changed. Click Generate matches to refresh the allocation using the new weight.")
        k1,k2,k3,k4,k5,k6 = st.columns(6)
        k1.metric("Requests", f"{len(demand)}")
        k2.metric("Units requested", f"{requested:,}")
        k3.metric("Units allocated", f"{allocated:,}")
        k4.metric("Unfilled demand", f"{unmatched:,}", f"{fill_rate:.1f}% covered")
        k5.metric("Avg. distance", f"{average_distance:.1f} km" if average_distance is not None else "N/A", help="Shipment-weighted average distance from matched suppliers to requesters.")
        k6.metric("Weighted shortfall", f"{weighted_shortfall:,}", help="Unfilled units weighted by urgency: level 1 = 3, level 2 = 2, level 3 = 1.")
        st.caption(f"Greedy objective score: {objective_score:,.1f} = 100 x weighted shortfall ({shortfall_cost:,}) + distance weight {run_distance_weight:.1f} x unit-km ({unit_km:,.1f}). Lower is preferred by the heuristic.")
        st.markdown("#### Allocation plan by requester")
        st.caption("One row per requester. Supplier quantities and distances are written together so each recommendation is easy to trace.")
        allocation_plan_rows = []
        for req in demand.sort_values("Urgency").to_dict("records"):
            request_rows = result[result["Request ID"] == req["Request ID"]]
            matches_for_request = request_rows[request_rows["Supplier"] != "Unfilled demand"]
            unmet_for_request = int(request_rows.loc[request_rows["Supplier"] == "Unfilled demand", "Units"].sum())
            allocated_for_request = int(matches_for_request["Units"].sum()) if not matches_for_request.empty else 0
            if matches_for_request.empty:
                supplier_plan = "No compatible allocation"
            else:
                supplier_plan = "; ".join(
                    f'{row["Supplier"]}: {int(row["Units"]):,} units ({float(row["Distance (km)"]):.1f} km)'
                    for _, row in matches_for_request.iterrows()
                )
            action = f"Approve {allocated_for_request:,} units"
            if unmet_for_request:
                action += f"; source {unmet_for_request:,} more"
            elif int(req["Demand Quantity"]) == 0:
                action = "No shipment required"
            allocation_plan_rows.append({
                "Urgency":int(req["Urgency"]), "Requester":req["Organization"],
                "Demand":int(req["Demand Quantity"]), "Product":req["Product Preference"],
                "Supplier allocation(s)":supplier_plan, "Unfilled":unmet_for_request,
                "Recommended action":action,
            })
        allocation_plan = pd.DataFrame(allocation_plan_rows)
        st.dataframe(allocation_plan, hide_index=True, use_container_width=True, height=min(560, max(160, 40 * (len(allocation_plan) + 1) + 8)))

        recommendation, requester_notes, supplier_utilization = build_decision_recommendations(demand, supply, result)
        st.markdown("#### Recommended decision")
        with st.container(border=True):
            card_class = "decision-card attention" if unmatched else "decision-card"
            st.markdown(f'<div class="{card_class}"><p>{escape(recommendation)}</p></div>', unsafe_allow_html=True)
            st.markdown("**Action by requester**")
            for note in requester_notes:
                st.markdown(f'- **{escape(str(note["Organization"]))}** (urgency {note["Urgency"]}): {note["Recommendation"]}')
            st.markdown("**Supplier capacity review**")
            st.dataframe(supplier_utilization, hide_index=True, use_container_width=True, height=min(420, max(150, 36 * (len(supplier_utilization) + 2))))

        st.markdown('<div class="note"><b>Decision logic:</b> the demo greedily assigns the compatible supplier-requester pair with the largest positive reduction in the combined score, using urgency weights and distance penalty. The distance penalty uses a fixed default weight of 1.5 to balance shortfall and shipment distance. This is a heuristic demonstration, not the original Shield-Net optimization model.</div>', unsafe_allow_html=True)
    else:
        st.info("Edit the inputs if you like, then select Generate illustrative matches to see the dashboard output.")

with history_tab:
    st.subheader("Reported Shield-Net service outcomes")
    st.caption("Historical implementation period: March-September 2020")
    h1,h2,h3,h4 = st.columns(4)
    h1.metric("Supplier-requester matches", "390")
    h2.metric("Face shields shipped", "50,925")
    h3.metric("Organizations receiving shields", "68")
    h4.metric("Suppliers in matching service", "373")
    st.markdown('<div class="note"><b>Historical reported results.</b> These figures describe the real service and are separate from the sample inputs and illustrative allocations in the matching dashboard.</div>', unsafe_allow_html=True)
    st.markdown("Source: Alcock, Rebecca, Justin J. Boutilier, and Auyon Siddiq. [Shield-Net: Matching Supply with Demand for Face Shields During the COVID-19 Pandemic](https://doi.org/10.1287/inte.2021.1112), *INFORMS Journal on Applied Analytics*, 52(6), 485-507 (2022).")
    st.caption("The historical totals are presented as reported case-study results. The prototype does not calculate them from historical transaction records.")

st.divider()
st.caption("SHIELD-NET | Streamlit prototype | Sample matching results are illustrative")

