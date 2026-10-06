import streamlit as st
import sqlite3
from datetime import datetime


# =====================================================
# DATABASE
# =====================================================

def create_database():

    conn = sqlite3.connect("incidents.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS incidents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            incident_id TEXT,
            username TEXT,
            name TEXT,
            email TEXT,
            incident_type TEXT,
            severity TEXT,
            description TEXT,
            status TEXT,
            date_time TEXT
        )
    """)

    conn.commit()
    conn.close()


create_database()


# =====================================================
# PAGE SETTINGS
# =====================================================

st.set_page_config(
    page_title="Cybersecurity Incident System",
    page_icon="🔐",
    layout="wide"
)


# =====================================================
# SESSION STATE
# =====================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""


# =====================================================
# LOGIN
# =====================================================

if not st.session_state.logged_in:

    st.title(
        "🔐 Cybersecurity Incident Reporting and Tracking System"
    )

    st.subheader("Login")

    username = st.text_input("Username")

    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("🔑 Login"):

        # ADMIN LOGIN
        if username == "admin" and password == "admin123":

            st.session_state.logged_in = True
            st.session_state.username = "admin"

            st.success("Admin login successful!")

            st.rerun()

        # USER LOGIN
        elif username == "user" and password == "user123":

            st.session_state.logged_in = True
            st.session_state.username = "user"

            st.success("User login successful!")

            st.rerun()

        else:

            st.error(
                "Invalid username or password."
            )

    st.info("Demo Login")

    st.write(
        "Admin → Username: `admin` | Password: `admin123`"
    )

    st.write(
        "User → Username: `user` | Password: `user123`"
    )

    st.stop()


# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.title("🔐 Cybersecurity System")

st.sidebar.write(
    f"Welcome, **{st.session_state.username}**!"
)


# ADMIN MENU
if st.session_state.username == "admin":

    menu = st.sidebar.radio(
        "Menu",
        [
            "📊 Dashboard",
            "📝 Report Incident",
            "📋 Incident Tracking"
        ]
    )


# USER MENU
else:

    menu = st.sidebar.radio(
        "Menu",
        [
            "📝 Report Incident",
            "🔎 My Incidents"
        ]
    )


# =====================================================
# LOGOUT
# =====================================================

if st.sidebar.button("🚪 Logout"):

    st.session_state.logged_in = False
    st.session_state.username = ""

    st.rerun()


# =====================================================
# ADMIN DASHBOARD
# =====================================================

if menu == "📊 Dashboard":

    st.title("📊 Admin Dashboard")

    conn = sqlite3.connect("incidents.db")
    cursor = conn.cursor()

    # Total
    cursor.execute(
        "SELECT COUNT(*) FROM incidents"
    )

    total = cursor.fetchone()[0]

    # Reported
    cursor.execute(
        """
        SELECT COUNT(*)
        FROM incidents
        WHERE status = 'Reported'
        """
    )

    reported = cursor.fetchone()[0]

    # Under Investigation
    cursor.execute(
        """
        SELECT COUNT(*)
        FROM incidents
        WHERE status = 'Under Investigation'
        """
    )

    investigation = cursor.fetchone()[0]

    # Resolved
    cursor.execute(
        """
        SELECT COUNT(*)
        FROM incidents
        WHERE status = 'Resolved'
        """
    )

    resolved = cursor.fetchone()[0]

    # Closed
    cursor.execute(
        """
        SELECT COUNT(*)
        FROM incidents
        WHERE status = 'Closed'
        """
    )

    closed = cursor.fetchone()[0]

    # Critical
    cursor.execute(
        """
        SELECT COUNT(*)
        FROM incidents
        WHERE severity = 'Critical'
        """
    )

    critical = cursor.fetchone()[0]

    conn.close()


    # Dashboard cards

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Total Incidents",
            total
        )

    with col2:

        st.metric(
            "Reported",
            reported
        )

    with col3:

        st.metric(
            "Under Investigation",
            investigation
        )


    col4, col5, col6 = st.columns(3)

    with col4:

        st.metric(
            "Resolved",
            resolved
        )

    with col5:

        st.metric(
            "Closed",
            closed
        )

    with col6:

        st.metric(
            "Critical",
            critical
        )


    st.divider()

    st.subheader(
        "📌 System Information"
    )

    st.write(
        "The administrator can monitor, investigate, "
        "resolve and close cybersecurity incidents."
    )


# =====================================================
# REPORT INCIDENT
# =====================================================

elif menu == "📝 Report Incident":

    st.title(
        "📝 Report Cybersecurity Incident"
    )

    st.write(
        "Report a suspected cybersecurity incident."
    )


    with st.form("incident_form"):

        name = st.text_input(
            "Your Name"
        )


        incident_type = st.selectbox(
            "Incident Type",
            [
                "Phishing",
                "Malware",
                "Unauthorized Access",
                "Data Breach",
                "Password Attack",
                "Suspicious Activity",
                "Other"
            ]
        )


        severity = st.selectbox(
            "Severity",
            [
                "Low",
                "Medium",
                "High",
                "Critical"
            ]
        )


        description = st.text_area(
            "Description",
            placeholder="Describe what happened..."
        )


        submit = st.form_submit_button(
            "🚨 Submit Incident"
        )


    if submit:

        if name == "":

            st.error(
                "Please enter your name."
            )

        elif description == "":

            st.error(
                "Please describe the incident."
            )

        else:

            conn = sqlite3.connect(
                "incidents.db"
            )

            cursor = conn.cursor()


            # Generate Incident ID

            cursor.execute(
                "SELECT COUNT(*) FROM incidents"
            )

            count = cursor.fetchone()[0] + 1001

            incident_id = f"INC-{count}"


            # Current date and time

            date_time = datetime.now().strftime(
                "%d-%m-%Y %H:%M:%S"
            )


            # Logged-in username

            username = st.session_state.username


            # Demo email

            if username == "user":

                email = "user@example.com"

            else:

                email = "admin@example.com"


            # Save incident

            cursor.execute(
                """
                INSERT INTO incidents
                (
                    incident_id,
                    username,
                    name,
                    email,
                    incident_type,
                    severity,
                    description,
                    status,
                    date_time
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    incident_id,
                    username,
                    name,
                    email,
                    incident_type,
                    severity,
                    description,
                    "Reported",
                    date_time
                )
            )


            conn.commit()

            conn.close()


            st.success(
                "Incident reported successfully!"
            )


            st.subheader(
                f"🚨 Your Incident ID is: {incident_id}"
            )


            st.info(
                "Status: Reported"
            )


# =====================================================
# ADMIN INCIDENT TRACKING
# =====================================================

elif menu == "📋 Incident Tracking":

    st.title(
        "📋 Incident Tracking"
    )

    st.write(
        "View and manage all reported cybersecurity incidents."
    )


    # SEARCH

    search = st.text_input(
        "🔍 Search Incident",
        placeholder=(
            "Search by Incident ID, name or incident type..."
        )
    )


    # FILTERS

    col1, col2 = st.columns(2)


    with col1:

        severity_filter = st.selectbox(
            "Filter by Severity",
            [
                "All",
                "Low",
                "Medium",
                "High",
                "Critical"
            ]
        )


    with col2:

        status_filter = st.selectbox(
            "Filter by Status",
            [
                "All",
                "Reported",
                "Under Investigation",
                "Resolved",
                "Closed"
            ]
        )


    # GET DATABASE DATA

    conn = sqlite3.connect(
        "incidents.db"
    )

    cursor = conn.cursor()


    cursor.execute(
        "SELECT * FROM incidents ORDER BY id DESC"
    )


    incidents = cursor.fetchall()

    conn.close()


    # FILTER INCIDENTS

    filtered_incidents = []


    for incident in incidents:

        (
            database_id,
            incident_id,
            username,
            name,
            email,
            incident_type,
            severity,
            description,
            status,
            date_time
        ) = incident


        # Search filter

        search_text = (
            incident_id
            + " "
            + name
            + " "
            + incident_type
        ).lower()


        if (
            search
            and search.lower() not in search_text
        ):

            continue


        # Severity filter

        if (
            severity_filter != "All"
            and severity != severity_filter
        ):

            continue


        # Status filter

        if (
            status_filter != "All"
            and status != status_filter
        ):

            continue


        filtered_incidents.append(
            incident
        )


    # DISPLAY RESULTS

    if not filtered_incidents:

        st.info(
            "No matching incidents found."
        )


    else:

        st.write(
            f"Showing {len(filtered_incidents)} incident(s)"
        )


        for incident in filtered_incidents:

            (
                database_id,
                incident_id,
                username,
                name,
                email,
                incident_type,
                severity,
                description,
                status,
                date_time
            ) = incident


            with st.expander(
                f"🚨 {incident_id} | "
                f"{incident_type} | "
                f"{severity}"
            ):


                st.write(
                    f"**Reported By:** {name}"
                )


                st.write(
                    f"**Username:** {username}"
                )


                st.write(
                    f"**Email:** {email}"
                )


                st.write(
                    f"**Incident Type:** {incident_type}"
                )


                st.write(
                    f"**Severity:** {severity}"
                )


                st.write(
                    f"**Description:** {description}"
                )


                st.write(
                    f"**Current Status:** {status}"
                )


                st.write(
                    f"**Date:** {date_time}"
                )


                # STATUS UPDATE

                status_options = [
                    "Reported",
                    "Under Investigation",
                    "Resolved",
                    "Closed"
                ]


                new_status = st.selectbox(
                    "Update Status",
                    status_options,
                    index=status_options.index(
                        status
                    ),
                    key=f"status_{database_id}"
                )


                if st.button(
                    "Update Status",
                    key=f"update_{database_id}"
                ):


                    conn = sqlite3.connect(
                        "incidents.db"
                    )

                    cursor = conn.cursor()


                    cursor.execute(
                        """
                        UPDATE incidents
                        SET status = ?
                        WHERE id = ?
                        """,
                        (
                            new_status,
                            database_id
                        )
                    )


                    conn.commit()

                    conn.close()


                    st.success(
                        f"Status updated to {new_status}"
                    )


                    st.rerun()


# =====================================================
# USER MY INCIDENTS
# =====================================================

elif menu == "🔎 My Incidents":

    st.title(
        "📋 My Reported Incidents"
    )

    st.write(
        "View the incidents you have reported."
    )


    current_user = (
        st.session_state.username
    )


    conn = sqlite3.connect(
        "incidents.db"
    )

    cursor = conn.cursor()


    cursor.execute(
        """
        SELECT *
        FROM incidents
        WHERE username = ?
        ORDER BY id DESC
        """,
        (current_user,)
    )


    incidents = cursor.fetchall()

    conn.close()


    if incidents:


        for incident in incidents:

            (
                database_id,
                incident_id,
                username,
                name,
                email,
                incident_type,
                severity,
                description,
                status,
                date_time
            ) = incident


            st.subheader(
                f"🚨 {incident_id} | {incident_type}"
            )


            st.write(
                f"**Name:** {name}"
            )


            st.write(
                f"**Severity:** {severity}"
            )


            st.write(
                f"**Description:** {description}"
            )


            st.write(
                f"**Status:** {status}"
            )


            st.write(
                f"**Date:** {date_time}"
            )


            st.divider()


    else:

        st.info(
            "No incidents reported by you yet."
        )