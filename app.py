import streamlit as st
import time

st.set_page_config(layout='wide')



# ============================== CSS ========================
# Custom CSS for button effects
st.markdown("""
    <style>
    /* Button Styling */
    .stButton > button {
        transition: transform 0.2s ease-in-out, background 0.3s ease-in-out, box-shadow 0.2s;
    }
    
    /* Click Effect: Impact Shockwave */
    .stButton > button:active {
        transform: scale(0.9);
    }

    </style>
""", unsafe_allow_html=True)


# Custom cursor
st.markdown(
    """
    <style>
        * {cursor: url(https://cur.cursors-4u.net/cursors/cur-11/cur1054.cur), auto !important;}
    </style>
    """,
    unsafe_allow_html=True
)



# Dynamic Effect when user click ai insight button
def progress_ai():
    progress_bar = st.progress(0)
    status_text = st.empty()  # Placeholder for status updates

    steps = 3  # Number of steps in progress
    for i in range(steps + 1):
        percent_complete = int((i / steps) * 100)  # Calculate percentage
        progress_bar.progress(percent_complete)

        if percent_complete < 100:
            status_text.text(f"Analysing... {percent_complete}% ⏳")
        else:
            status_text.text("Fetching data...")

        time.sleep(0.5)  # Smooth delay







# ================ User-defined modules ===============
from frontend.dashboard import dashboard
from frontend.report_analysis import report_analysis_page
from frontend.transactions import transactions_page
from frontend.categories import categories_page
from frontend.settings import settings_page, get_details_from_profiles_table
from frontend.budget import budget_page
from frontend.notifications import get_notifications
from frontend.contact_us import contact_us_page
from frontend.ai import ai
from backend.auth import *






# ======================== Sidebar ==========================
# ========= Logged user info ===========


# Setting session state for Login 
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.email = ""
    st.session_state.uid = None


if st.session_state.logged_in:
    user_data = get_details_from_profiles_table(st.session_state.uid)
    name = user_data["name"]
    profile_photo = user_data["profile_photo"]

    # Creating two column inside sidebar
    # - one for loggen user's image
    # - another for loggen in username
    col1, col2 = st.sidebar.columns([1, 3])

    with col1:
        st.image(profile_photo, width=200)

    with col2:
        st.write("Logged in as:")
        st.markdown(f" ### {name}")

    # Seperator for styling
    st.sidebar.markdown("---")

    #  ========== Navigation Bar===========
    st.sidebar.title("🏠 Main Menu")
    menu = [
        '🏠 Dashboard (Home)',  
        '📊 Report & Analysis',  
        '💰 Manage Transactions',  
        '📂 Manage Categories',  
        '📉 Manage Budgets',  
        '🔔 Notifications',  
        '🤖 AI Insights',  
        '⚙️ Settings',  
        '📞 Contact Us'  
    ]


    with st.sidebar.container(border=True):
        selected_page = st.radio("Select a section:", menu,index=0)

    # =========== Opening page to display based on selection ================
    if selected_page == '🏠 Dashboard (Home)':
        dashboard(st.session_state.uid)

    elif selected_page == '📊 Report & Analysis':
        report_analysis_page(st.session_state.uid)

    elif selected_page == '💰 Manage Transactions':
        transactions_page(st.session_state.uid)
        
    elif selected_page == '📂 Manage Categories':
        categories_page(st.session_state.uid)


    elif selected_page == '📉 Manage Budgets':
        budget_page(st.session_state.uid)

    elif selected_page == '🔔 Notifications':
        notifications = get_notifications(st.session_state.uid)

        st.subheader("🔔 Notifications")
        if notifications:
            for n in notifications:
                st.warning(n)
        else:
            st.success("🎉 No alerts! You're managing your finances well.")

    elif selected_page == '🤖 AI Insights':
        if st.button("Get AI 🤖 insights"):
            progress_ai()
            if not ai(st.session_state.uid):  # If `ai()` returns False, show warning
                st.warning("You don't have sufficient data to use this feature")

    elif selected_page == '⚙️ Settings':
        settings_page(st.session_state.uid)
        
    elif selected_page == '📞 Contact Us':
        contact_us_page()

    # Seperator for styling
    st.sidebar.markdown("---")

    # ====== Logout Button =====
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()



else:
    # Initialize session state variable to track if GIF was shown
    if "gif_shown" not in st.session_state:
        st.session_state.gif_shown = False  # Initially False

    # Show GIF only if it hasn't been displayed before
    if not st.session_state.gif_shown:
        gif_placeholder = st.empty()
        
        with gif_placeholder:
            st.markdown(
                """
                <div style="display: flex; justify-content: center; align-items: center; height: 80vh;">
                    <img src="https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExenB1amNuNzdpZmk1cGw0MmtmY2JkMmV1Z3QyZ2MyN3VxdXo1OWJzMyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9cw/gkbppgFMYr908R1ZfA/giphy.gif" width="400">
                </div>
                """,
                unsafe_allow_html=True
            )

        time.sleep(2)  # Pause for effect
        gif_placeholder.empty()  # Remove the GIF
        
        st.session_state.gif_shown = True  # Set flag so GIF doesn't show again

    
    with st.container(border=True):
        st.markdown("<h3 style='text-align: center; color: #4CAF50;'>🌟 Welcome to your</h3>", unsafe_allow_html=True)
        st.markdown("<h1 style='text-align: center; color: #FFD700;'>💰 Smart Expense Tracker App</h1>", unsafe_allow_html=True)
        st.divider()
        
        
        # Initialize session state for navigation
        if "page" not in st.session_state:
            st.session_state.page = "Login"

        # Pill-style navigation using segmented control
        page_map = {
            "Login": "🔑 Login",
            "Register": "📝 Register",
        }

        selection = st.segmented_control(
            "Select Page",
            options=list(page_map.keys()),
            format_func=lambda option: page_map[option],
            selection_mode="single",
        )

        # Update session state based on selection
        if selection:
            st.session_state.page = selection
        
        with st.container( border=True):
            # Display the selected page content
            if st.session_state.page == "Login":
                login()
            else:
                register()








