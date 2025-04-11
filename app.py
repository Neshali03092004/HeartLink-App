import streamlit as st
import pandas as pd
import time
import base64
import random
from datetime import datetime

# ---------- LOAD CSV DATASETS ---------- #
health_df = pd.read_csv("health_monitoring.csv")
safety_df = pd.read_csv("safety_monitoring.csv")
reminder_df = pd.read_csv("daily_reminder.csv")

# Clean columns
for df in [health_df, safety_df, reminder_df]:
    df.columns = df.columns.str.strip()

health_df["Alert Triggered (Yes/No)"] = health_df["Alert Triggered (Yes/No)"].astype(str).str.lower().str.strip()
safety_df["Alert Triggered (Yes/No)"] = safety_df["Alert Triggered (Yes/No)"].astype(str).str.lower().str.strip()

if "Acknowledged" not in reminder_df.columns:
    reminder_df["Acknowledged"] = "No"

# Encode image as base64

def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Set paths
background_image_path = "background.jpg"
logo_image_path = "logo.jpg"
bg_base64 = get_base64_image(background_image_path)
logo_base64 = get_base64_image(logo_image_path)

st.set_page_config(page_title="HeartLink ❤️", page_icon="❤️", layout="wide")

# ---------- CUSTOM CSS ---------- #
st.markdown(f"""
<style>
html, body, [data-testid="stAppViewContainer"] {{ margin: 0; padding: 0; height: 100%; overflow: hidden; }}
.splash {{ height: 100vh; background-color: #E6E6FA; display: flex; flex-direction: column; justify-content: center; align-items: center; }}
.heartbeat {{ animation: heartbeat 1.5s infinite; }}
@keyframes heartbeat {{ 0% {{ transform: scale(1); }} 25% {{ transform: scale(1.1); }} 40% {{ transform: scale(0.95); }} 60% {{ transform: scale(1.05); }} 100% {{ transform: scale(1); }} }}
.title {{ font-size: 3.5rem; font-weight: bold; color: #8A2BE2; text-shadow: 1px 1px 3px #aaa; font-family: 'Algerian', sans-serif; }}
.subtitle {{ font-size: 1.5rem; font-style: italic; color: #4B0082; }}
.login-page {{
    height: 50vh;
    width: 50vw;
    background-image: url("data:image/png;base64,{bg_base64}");
    background-size: contain;
    background-position: center;
    background-repeat: no-repeat;
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
    margin: 0;
    padding: 0;
    overflow: hidden;
}}
.login-box {{ background: rgba(255,255,255,0.95); padding: 30px; border-radius: 15px; width: 350px; text-align: center; box-shadow: 0px 0px 20px rgba(0,0,0,0.2); }}
.welcome {{ font-size: 26px; color: #4B0082; font-family: 'Castellar', cursive; margin-bottom: 20px; font-weight: bold; }}
.quote-box {{ background-color: #f8f0ff; padding: 20px; border-radius: 10px; text-align: center; font-style: italic; color: #4a148c; margin-bottom: 40px; font-size: 18px; }}
.top-bar {{ display: flex; justify-content: space-between; margin-bottom: 20px; padding: 10px 30px; background-color: #f3e8ff; border-radius: 12px; font-size: 18px; }}
.top-bar span {{ font-weight: bold; }}
.stButton>button:hover {{ background-color: #ba68c8; }}
</style>
""", unsafe_allow_html=True)

# ---------- PAGES ---------- #
if "page" not in st.session_state:
    st.session_state.page = "splash"
if "login_time" not in st.session_state:
    st.session_state.login_time = ""

if st.session_state.page == "splash":
    st.markdown(f"""
    <div class="splash">
        <img src="data:image/png;base64,{logo_base64}" width="140">
        <div class="title heartbeat">HeartLink</div>
        <div class="subtitle">Connecting hearts, caring lives 💞</div>
    </div>
    """, unsafe_allow_html=True)
    time.sleep(3)
    st.session_state.page = "login"
    st.rerun()

elif st.session_state.page == "login":
    st.markdown('<div class="login-page">', unsafe_allow_html=True)
    st.markdown('<div class="login-box">', unsafe_allow_html=True)
    st.markdown('<div class="welcome">Welcome to HeartLink❤️ Senior Buddies 👵👴</div>', unsafe_allow_html=True)
    name = st.text_input("👤 Name")
    phone_email = st.text_input("📧 User-ID")
    password = st.text_input("🔒 Password", type="password")
    if st.button("Login"):
        valid_ids = health_df["Device-ID/User-ID"].astype(str).unique()
        if phone_email in valid_ids:
            st.session_state.user_id = phone_email
            st.session_state.user_name = name
            st.session_state.login_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            st.session_state.page = "dashboard"
            st.success(f"Welcome {name}, your data is loading!")
            st.rerun()
        else:
            st.error("Invalid ID. Please enter a valid user ID from the dataset.")
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.page == "dashboard":
    st.markdown("<div class='top-bar'>"
                f"<span>👵 Welcome, {st.session_state.user_name}!</span>"
                f"<span>🕒 Last Login: {st.session_state.login_time}</span>"
                "</div>", unsafe_allow_html=True)
    st.markdown('<h2 style="color:#7b2cbf;text-align:center;">Welcome back, dear senior buddy! 💗</h2>', unsafe_allow_html=True)
    quote = random.choice([
    "🍎 Eat an apple a day — keep that doctor away!",
    "💧 Stay hydrated — your body loves you for it!",
    "😄 A good laugh is sunshine for the soul.",
    "☀️ Mornings are miracles, enjoy every one!",
    "🧠 A sharp mind starts with a peaceful heart.",
    "🧁 Life is short — enjoy the cupcake!",
    "📖 Read something joyful today — it’s brain candy!",
    "🚶‍♂️ A walk a day keeps the worries away.",
    "🎵 Music is the vitamin for your mood.",
    "💬 Talk to someone you love today.",
    "🍵 Tea time is healing time.",
    "🌻 Just like a flower, bloom in your time.",
    "📺 Watch your favorite show and smile wider.",
    "🍲 Good food, good mood — cook your joy!",
    "📞 A call to a friend is the best medicine.",
    "💊 Take your medicine like a superhero takes their power!",
    "🎨 Be creative — paint your day with color!",
    "🧩 Keep your brain buzzing — try a puzzle!",
    "📸 Look at your favorite memory and smile.",
    "🎂 Your age is just the icing — you're the cake!",
    "🐦 Listen to birds — they sing just for you.",
    "🪴 Water your plants and your soul.",
    "🛌 Rest well — it's how warriors recover!",
    "🌈 Every wrinkle tells a story — yours is beautiful.",
    "🕯️ Light a candle, not just the room but your heart.",
    "💃 Dance in your kitchen — nobody’s watching!",
    "🧘‍♂️ Breathe in calm, breathe out smiles.",
    "🎁 Today is a gift — unwrap it slowly.",
    "😇 You are wise, wonderful, and deeply loved.",
    "👟 Comfortable shoes and a happy soul go together.",
    "🧦 Cozy socks, warm tea, happy heart!",
    "📚 Learn something new — age is no barrier.",
    "🎤 Sing in the shower — your voice is golden!",
    "🎒 Life’s an adventure — keep packing joy.",
    "🌼 You are someone’s sunshine today.",
    "📅 One happy moment daily keeps gloom away.",
    "🥗 Healthy food = happy heart!",
    "🌟 You’re the sparkle in someone’s life.",
    "🍞 Break bread, build bonds.",
    "🐶 Pet a dog. Hug a human. Laugh loud.",
    "🎈 Add one smile to the world every day.",
    "👓 You’ve seen decades — you are wisdom!",
    "📍 Wherever you are, peace can follow.",
    "🏡 Home is where kindness lives — and so do you.",
    "🪞 Mirror says: You're amazing today too!",
    "💬 A kind word heals more than medicine.",
    "☕ Sip slowly. Love loudly.",
    "🎶 Old songs never fade — neither do you.",
    "🪙 Gratitude is gold for your heart.",
    "💖 Your heart is full of love — share it today."
])

    st.markdown(f'<div class="quote-box">{quote}</div>', unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("🩺 Health Monitoring"):
            st.session_state.page = "health"
            st.rerun()
    with col2:
        if st.button("🛟 Safety Alerts"):
            st.session_state.page = "safety"
            st.rerun()
    with col3:
        if st.button("⏰ Daily Reminders"):
            st.session_state.page = "reminders"
            st.rerun()
    with col4:
        if st.button("🚪 Logout"):
            st.session_state.page = "login"
            st.rerun()
    st.markdown("---")
    if st.button("💬 Chat with Buddy"):
        st.info("Coming soon: Your friendly chat buddy!")
        st.session_state.page = "chat"
        st.rerun()
    if st.button("❤ Call for Help"):
        st.warning("Emergency request sent to caregiver!")
    if st.button("📋 Health Tips"):
        st.success("Stay hydrated, walk daily, eat colorful foods!")            
                   
elif st.session_state.page == "health":
    st.title("🩺 Health Monitoring")
    uid = st.session_state.get("user_id", "")
    df = health_df[health_df["Device-ID/User-ID"] == uid]
    if not df.empty:
        for _, row in df.iterrows():
            st.markdown("---")
            st.write(f"**🆔 User:** {row['Device-ID/User-ID']}")
            st.write(f"🕒 Time: {row['Timestamp']}")
            st.write(f"❤️ Heart Rate: {row['Heart Rate']} ({row['Heart Rate Below/Above Threshold (Yes/No)']})")
            st.write(f"🩸 BP: {row['Blood Pressure']} ({row['Blood Pressure Below/Above Threshold (Yes/No)']})")
            st.write(f"🍬 Sugar: {row['Glucose Levels']} ({row['Glucose Levels Below/Above Threshold (Yes/No)']})")
            st.write(f"🔴 Alert Triggered: {row['Alert Triggered (Yes/No)']}")
            st.write(f"📩 Caregiver Notified: {row['Caregiver Notified (Yes/No)']}")
    else:
        st.warning("No health data available for this user.")
    if st.button("⬅️ Back"):
        st.session_state.page = "dashboard"
        st.rerun()

elif st.session_state.page == "safety":
    st.title("🛟 Safety Monitoring")
    uid = st.session_state.get("user_id", "")
    df = safety_df[safety_df["Device-ID/User-ID"] == uid]
    if not df.empty:
        for _, row in df.iterrows():
            st.markdown("---")
            st.write(f"**🆔 User:** {row['Device-ID/User-ID']}")
            st.write(f"🕒 Time: {row['Timestamp']}")
            st.write(f"📍 Location: {row['Location']}")
            st.write(f"💤 Activity: {row['Movement Activity']}")
            st.write(f"🧊 Impact: {row['Impact Force Level']} | Inactivity: {row['Post-Fall Inactivity Duration (Seconds)']}s")
            st.write(f"🚨 Alert Triggered: {row['Alert Triggered (Yes/No)']} | Caregiver Notified: {row['Caregiver Notified (Yes/No)']}")
    else:
        st.warning("No safety data found for this user.")
    if st.button("⬅️ Back"):
        st.session_state.page = "dashboard"
        st.rerun()

elif st.session_state.page == "reminders":
    st.title("⏰ Daily Reminders")
    uid = st.session_state.get("user_id", "")
    df = reminder_df[reminder_df["Device-ID/User-ID"] == uid]
    if not df.empty:
        for _, row in df.iterrows():
            st.markdown("---")
            st.write(f"📆 Time: {row['Timestamp']} | Reminder: {row['Reminder Type']}")
            st.write(f"⏰ Scheduled: {row['Scheduled Time']} | Sent: {row['Reminder Sent (Yes/No)']}")
            st.write(f"✅ Acknowledged: {row['Acknowledged (Yes/No)']}")
    else:
        st.warning("No reminders found for this user.")
    if st.button("⬅️ Back"):
        st.session_state.page = "dashboard"
        st.rerun()
elif st.session_state.page == "chat":
    st.title("💬 Chat with Your HeartLink Buddy")
    st.markdown("Say hi to your friendly companion!")
     
    # Store chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Get user input
    user_input = st.text_input("Type your message here:")
    if st.button("Send"):
        if user_input:
            # Add to chat history
            st.session_state.chat_history.append(("You", user_input))

            # Simple responses (you can expand!)
            if "hello" in user_input.lower():
                reply = "Hello buddy! How are you feeling today? 💖"
            elif "medicine" in user_input.lower():
                reply = "Don’t forget to take your medicine after food! 💊"
            elif "joke" in user_input.lower():
                reply = "Why did the raisin go to the doctor? It felt dried out! 😄"
            else:
                reply = "That’s interesting! I’m here to chat with you anytime."

            st.session_state.chat_history.append(("HeartBuddy", reply))

    # Display chat history
    for sender, message in st.session_state.chat_history:
        st.markdown(f"{sender}:** {message}")

    if st.button("⬅️ Back"):
        st.session_state.page = "dashboard"
        st.rerun()
        