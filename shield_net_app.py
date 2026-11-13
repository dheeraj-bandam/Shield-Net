import streamlit as st
import pandas as pd

st.set_page_config(page_title="Shield-Net | Matching Demo", page_icon="S", layout="wide")
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@500;600;700;800&display=swap');
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
.stApp { background: #f5f7f8; color: #182a3a; }
h1, h2, h3 { font-family: 'Manrope', sans-serif; letter-spacing: -.03em; }
.hero { background: linear-gradient(115deg,#102b3a,#174c55); color: white; padding: 26px 30px; border-radius: 16px; margin: 0 0 22px; }
.hero h1 { color: white; margin: 4px 0; font-size: 30px; }
.hero p { color: #d0e1e1; margin: 0; }
.kicker { color:#a9d8c8; text-transform:uppercase; letter-spacing:.13em; font-weight:700; font-size:11px; }
.note { background:#e9f3f0; border-left:4px solid #168474; padding:12px 16px; border-radius:7px; color:#294a4d; font-size:13px; }
</style>
""", unsafe_allow_html=True)

DEMAND_A = pd.DataFrame([
    {"Request ID":"H-101", "Facility":"Harborview Medical", "City":"Seattle", "Shield type":"Adult", "Units requested":120, "Urgency":"Critical", "Need by":"Today"},
    {"Request ID":"H-102", "Facility":"Northgate Clinic", "City":"Seattle", "Shield type":"Adult", "Units requested":80, "Urgency":"High", "Need by":"Today"},
    {"Request ID":"H-103", "Facility":"Rainier Community Care", "City":"Tacoma", "Shield type":"Pediatric", "Units requested":60, "Urgency":"High", "Need by":"Tomorrow"},
    {"Request ID":"H-104", "Facility":"Soundview Urgent Care", "City":"Tacoma", "Shield type":"Adult", "Units requested":50, "Urgency":"Standard", "Need by":"Tomorrow"},
])
SUPPLY_A = pd.DataFrame([
    {"Supplier ID":"S-01", "Supplier":"Evergreen Plastics", "City":"Seattle", "Shield type":"Adult", "Units available":150, "Ready in":"Today"},
    {"Supplier ID":"S-02", "Supplier":"Cascadia Makers", "City":"Tacoma", "Shield type":"Pediatric", "Units available":75, "Ready in":"Today"},
    {"Supplier ID":"S-03", "Supplier":"Puget Safety Works", "City":"Seattle", "Shield type":"Adult", "Units available":90, "Ready in":"Tomorrow"},
])
DEMAND_B = pd.DataFrame([
    {"Request ID":"H-201", "Facility":"Metro General", "City":"Chicago", "Shield type":"Adult", "Units requested":200, "Urgency":"Critical", "Need by":"Today"},
    {"Request ID":"H-202", "Facility":"Westside Pediatrics", "City":"Chicago", "Shield type":"Pediatric", "Units requested":90, "Urgency":"High", "Need by":"Today"},
    {"Request ID":"H-203", "Facility":"Lake County Health", "City":"Evanston", "Shield type":"Adult", "Units requested":100, "Urgency":"High", "Need by":"Tomorrow"},
])
SUPPLY_B = pd.DataFrame([
    {"Supplier ID":"S-11", "Supplier":"Midwest Fabrication", "City":"Chicago", "Shield type":"Adult", "Units available":180, "Ready in":"Today"},
    {"Supplier ID":"S-12", "Supplier":"Lakeshore 3D Lab", "City":"Evanston", "Shield type":"Pediatric", "Units available":80, "Ready in":"Today"},
    {"Supplier ID":"S-13", "Supplier":"Civic Shield Co-op", "City":"Chicago", "Shield type":"Adult", "Units available":100, "Ready in":"Tomorrow"},
])

def demo_matches(demand, supply):
    """Transparent sample allocation; not the paper's optimization model."""
    remaining = dict(zip(supply["Supplier ID"], supply["Units available"].astype(int)))
    suppliers = supply.to_dict("records")
    rank = {"Critical":0, "High":1, "Standard":2}
    rows = []
    for req in sorted(demand.to_dict("records"), key=lambda x: (rank.get(x["Urgency"], 3), x["Need by"])):
        compatible = [s for s in suppliers if s["Shield type"] == req["Shield type"]]
        compatible.sort(key=lambda s: (s["City"] != req["City"], s["Ready in"] != "Today", s["Supplier"]))
        need = int(req["Units requested"])
        for sup in compatible:
            qty = min(need, remaining[sup["Supplier ID"]])
            if qty <= 0:
                continue
            rows.append({"Request ID":req["Request ID"], "Facility":req["Facility"], "Supplier":sup["Supplier"], "Supplier city":sup["City"], "Shield type":req["Shield type"], "Units":qty, "Urgency":req["Urgency"], "Ready":sup["Ready in"]})
            remaining[sup["Supplier ID"]] -= qty
            need -= qty
            if need == 0:
                break
        if need:
            rows.append({"Request ID":req["Request ID"], "Facility":req["Facility"], "Supplier":"Unfilled demand", "Supplier city":"-", "Shield type":req["Shield type"], "Units":need, "Urgency":req["Urgency"], "Ready":"Needs sourcing"})
    return pd.DataFrame(rows)

with st.sidebar:
    st.markdown("## Shield-Net")
    st.caption("Face-shield supply and demand matching")
    scenario = st.selectbox("Choose a sample case", ["Pacific Northwest", "Chicago region"])
    st.caption("All organizations and sample quantities are illustrative.")

if "scenario" not in st.session_state or st.session_state.scenario != scenario:
    if scenario == "Pacific Northwest":
        st.session_state.demand, st.session_state.supply = DEMAND_A.copy(), SUPPLY_A.copy()
    else:
        st.session_state.demand, st.session_state.supply = DEMAND_B.copy(), SUPPLY_B.copy()
    st.session_state.scenario = scenario
    st.session_state.matches = None

st.markdown('<div class="hero"><div class="kicker">PPE coordination dashboard</div><h1>Match face-shield supply to need</h1><p>Review requests and supplier capacity, then generate an illustrative allocation for coordinator review.</p></div>', unsafe_allow_html=True)

demo_tab, history_tab = st.tabs(["Matching dashboard", "Historical case results"])
with demo_tab:
    st.subheader(f"{scenario}: inputs")
    st.caption("Edit the tables, then click Generate matches. Requests and supply must use the same shield type to be compatible.")
    input_a, input_b = st.columns(2)
    with input_a:
        st.markdown("#### Healthcare requests")
        demand = st.data_editor(st.session_state.demand, hide_index=True, use_container_width=True, num_rows="dynamic", key=f"demand_{scenario}")
        st.session_state.demand = demand
    with input_b:
        st.markdown("#### Supplier capacity")
        supply = st.data_editor(st.session_state.supply, hide_index=True, use_container_width=True, num_rows="dynamic", key=f"supply_{scenario}")
        st.session_state.supply = supply

    if st.button("Generate illustrative matches", type="primary", use_container_width=True):
        st.session_state.matches = demo_matches(demand, supply)

    result = st.session_state.matches
    if result is not None:
        st.divider()
        st.subheader("Matching results")
        requested = int(demand["Units requested"].sum())
        supplied = int(supply["Units available"].sum())
        allocated = int(result.loc[result["Supplier"] != "Unfilled demand", "Units"].sum()) if not result.empty else 0
        unmatched = requested - allocated
        fill_rate = 100 * allocated / requested if requested else 0
        k1,k2,k3,k4 = st.columns(4)
        k1.metric("Requests", f"{len(demand)}")
        k2.metric("Units requested", f"{requested:,}")
        k3.metric("Units allocated", f"{allocated:,}")
        k4.metric("Unfilled demand", f"{unmatched:,}", f"{fill_rate:.1f}% covered")
        result_left, result_right = st.columns([1.25, 1])
        with result_left:
            st.markdown("#### Suggested matches")
            st.dataframe(result, hide_index=True, use_container_width=True)
        with result_right:
            st.markdown("#### Units by facility")
            chart_data = result[result["Supplier"] != "Unfilled demand"].groupby("Facility", as_index=False)["Units"].sum()
            if chart_data.empty:
                st.info("No compatible supplier capacity is available for these requests.")
            else:
                st.bar_chart(chart_data.set_index("Facility"), color="#168474", height=300)
        st.markdown('<div class="note"><b>Demo only:</b> requests are considered in urgency order, then compatible stock is assigned with nearby and ready-today suppliers preferred. This simple rule is not the original Shield-Net optimization model.</div>', unsafe_allow_html=True)
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
