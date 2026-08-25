import streamlit as st

st.set_page_config(page_title="Movie Dubbing Studio", layout="centered")

# ==========================================
# 🔒 Password စစ်ဆေးသော Function (Password: 7818)
# ==========================================
def check_password():
    """Returns True if the user entered the correct password."""
    
    def password_entered():
        if st.session_state["password"] == "7818":
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Password ကို memory ထဲမှာ ဆက်မထားတော့ပါ
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show input for password.
        st.text_input(
            "🔒 ကျေးဇူးပြု၍ Password ထည့်ပါ။", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        # Password incorrect, show input + error.
        st.text_input(
            "🔒 ကျေးဇူးပြု၍ Password ထည့်ပါ။", type="password", on_change=password_entered, key="password"
        )
        st.error("😕 စကားဝှက် မှားယွင်းနေပါသည်။ ထပ်မံကြိုးစားပါ။")
        return False
    else:
        # Password correct.
        return True

# Password မှန်မှသာ အောက်ပါ App ကြီး ပွင့်မည်
if not check_password():
    st.stop()

# ==========================================
# 🎬 Movie Dubbing Studio App ၏ ပင်မ ကုဒ်များ
# ==========================================

st.title("🎬 Movie Dubbing Studio")
st.write("ဘာသာပြန်နဲ့ Edge TTS ဖြင့် အသံသွင်းကာ အလိုအလျောက် ပေါင်းစပ်ပေးမည့် App ဖြစ်ပါသည်။")

# API Keys ထည့်ရန် နေရာ
with st.expander("🔑 API Keys များ ထည့်ရန် (ဒီကိုနှိပ်ပါ)"):
    gemini_key = st.text_input("Gemini API Key", type="password")
    assemblyai_key = st.text_input("AssemblyAI API Key", type="password")

# 1. Video Uploader (Format အစုံနှင့် Size အကြီးအထိ လက်ခံရန်)
st.subheader("၁။ Video ရွေးချယ်ပါ")
uploaded_file = st.file_uploader(
    "Video တင်ရန် (MP4, MKV, AVI နှင့် အခြား Format များ)",
    type=["mp4", "mkv", "avi", "mov", "webm", "flv", "wmv"],
    help="200MB per file • Format အစုံ တင်နိုင်ပါသည်"
)

if uploaded_file is not None:
    st.success(f"ဗီဒီယိုဖိုင် အောင်မြင်စွာ တင်ပြီးပါပြီ: {uploaded_file.name}")
    st.video(uploaded_file)

# 2. မြန်မာအသံ ရွေးချယ်ရန်
st.subheader("၂။ မြန်မာအသံ ရွေးချယ်ရန်")
voice_option = st.selectbox(
    "အသံရွေးချယ်ရန်",
    ["my-MM-NilarNeural", "my-MM-ThihaNeural"]
)

# Start Dubbing Button
if st.button("🚀 Start Dubbing"):
    if uploaded_file is None:
        st.warning("ကျေးဇူးပြု၍ ဗီဒီယိုဖိုင် အရင်တင်ပေးပါ။")
    else:
        st.info("Dubbing လုပ်ဆောင်နေပါပြီ... ခဏစောင့်ဆိုင်းပေးပါ။")
