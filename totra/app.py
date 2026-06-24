import streamlit as st
import uuid
from api_handler import create_report, get_valid_reports, submit_verification

if "user_id" not in st.session_state:
    st.session_state.user_id = str(uuid.uuid4())

st.title("TOTRA")
st.caption("Traffic On The Road App")

st.subheader("Report an Incident")

report_type = st.selectbox(
    "What are you reporting?",
    ["police", "roadblock", "accident", "roadwork"]
)

lat = st.number_input("Latitude", value=10.6549, format="%.4f")
lon = st.number_input("Longitude", value=-61.5019, format="%.4f")

if st.button("Submit Report"):
    report = create_report(
        user_id=st.session_state.user_id,
        report_type=report_type,
        lat=lat,
        lon=lon
    )
    st.success("Report submitted! ID: " + report.report_id[:8])

st.subheader("Active Reports")
reports = get_valid_reports()

if not reports:
    st.info("No active reports right now.")
else:
    for r in reports:
        if r.is_credible:
            status = "Verified"
        else:
            status = "Pending verification"
        st.write("**" + r.report_type.upper() + "** — " + status)
        st.write("Location: " + str(r.lat) + ", " + str(r.lon))
        if not r.is_credible and r.user_id != st.session_state.user_id:
            if st.button("Verify this report", key=r.report_id):
                submit_verification(r.report_id, st.session_state.user_id)
                st.success("Verification submitted!")
        st.divider()
