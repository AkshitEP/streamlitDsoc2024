import pandas as pd
import streamlit as st

# Snowflake Animation CSS
SNOWFLAKE_CSS = """
<style>
body {
    background: linear-gradient(to bottom, #a0c4ff, #d0f0ff);
    color: #1c1c1c;
    font-family: 'Arial', sans-serif;
}

table {
    margin: auto;
    border: 1px solid #cccccc;
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
    background-color: #ffffff;
}

th, td {
    padding: 10px;
    text-align: center;
}

th {
    background-color: #004d99;
    color: white;
}

td {
    font-size: 14px;
    background-color: #e6f7ff;
    color: black;  /* Set text color inside the table to black */
}

# Snowflake animations
.snowflake {
    position: absolute;
    top: 0;
    width: 30px;
    height: 30px;
    background: white;
    border-radius: 50%;
    opacity: 0.8;
    animation: fall 5s linear infinite;
}

@keyframes fall {
    to {
        transform: translateY(100vh);
        opacity: 0;
    }
}
</style>
<div class="snowflake">❄</div>
"""


# Inject snowflake animation
st.markdown(SNOWFLAKE_CSS, unsafe_allow_html=True)

@st.cache_data
def load_data():
    # Load your CSV file
    data = pd.read_csv("main.csv")
    
    def calculate_total_score(score):
        try:
            if pd.isna(score):
                return 0  # Handle missing values
            
            # Extract the base score and bonus
            parts = score.split("+")  # Split into base score and bonus part
            base_score = eval(parts[0].strip())  # Base score
            
            bonus = 0
            if len(parts) > 1 and "bonus" in parts[1]:
                bonus = int(parts[1].split("(")[0].strip())  # Extract bonus count
            
            return base_score + bonus * 5  # Calculate total score
        except Exception as e:
            st.warning(f"Error processing score: {score}. Setting it to 0. Error: {e}")
            return 0
    
    data['Total Score'] = data['Score (Out of 100) bonus tasks - 5 each'].apply(calculate_total_score)
    
    return data

data = load_data()

# Sidebar - Entry no. input
st.sidebar.header("Search Your Marks")
entry_no = st.sidebar.text_input("Enter your Entry Number:")

# Main header
st.title("❄️ Winter: Dev Summer of Code Leaderboard ❄️")

# Display top 10 leaderboards
st.subheader("Top 10 Leaderboard")
leaderboard = data.sort_values(by="Total Score", ascending=False).head(10)
st.table(leaderboard[["Name", "Entry no.", "Hostel", "Vertical", "Total Score"]])

# Search functionality
if entry_no:
    st.subheader("Your Details")
    user_data = data[data["Entry no."].str.strip() == entry_no.strip()]
    if not user_data.empty:
        st.table(user_data[[  # Adjust the table columns
            "Name", "Entry no.", "Phone no.", "Hostel",
            "Vertical", "Score (Out of 100) bonus tasks - 5 each", "Review", "Total Score"
        ]])
    else:
        st.warning("No records found for the provided Entry Number.")
