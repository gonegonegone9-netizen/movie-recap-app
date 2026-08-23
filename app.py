import streamlit as st

st.set_page_config(page_title="Movie Dubbing App", page_icon="🎬")

st.title("One-Click Movie Dubbing App 🎬")
st.write("Video ကို အလိုအလျောက် မြန်မာလို ဘာသာပြန်ပြီး အသံထည့်ပေးမည့် App ဖြစ်ပါသည်။")

# API Keys တောင်းခံခြင်း
with st.expander("API Keys များ ထည့်ရန် (ဒီကိုနှိပ်ပါ)"):
    aai_key = st.text_input("AssemblyAI API Key:", type="password")
    gemini_key = st.text_input("Gemini API Key:", type="password")
    azure_key = st.text_input("Azure TTS Key:", type="password")

# Video Upload
uploaded_video = st.file_uploader("Video တင်ရန် (MP4)", type=["mp4"])
voice_choice = st.selectbox("အသံရွေးချယ်ရန်", ["my-MM-NilarNeural (Female - နီလာ)", "my-MM-ThihaNeural (Male - သီဟ)"])

if st.button("Start Dubbing"):
    if uploaded_video and aai_key and gemini_key and azure_key:
        st.info("၁။ AssemblyAI ဖြင့် စာသားနှင့် အချိန် ထုတ်ယူနေပါသည်...")
        # API ချိတ်ဆက်ရန် နေရာ
        
        st.info("၂။ Gemini AI ဖြင့် မြန်မာလို ဘာသာပြန်နေပါသည်...")
        # API ချိတ်ဆက်ရန် နေရာ
        
        st.info("၃။ Microsoft Azure ဖြင့် အသံထွက် (TTS) ဖန်တီးနေပါသည်...")
        # API ချိတ်ဆက်ရန် နေရာ
        
        st.info("၄။ FFmpeg ဖြင့် Video နှင့် Audio ပေါင်းနေပါသည်...")
        
        st.success("လုပ်ငန်းစဉ်ပြီးဆုံးပါသည်။ (မှတ်ချက် - ယခုအဆင့်သည် UI စမ်းသပ်ခြင်းသာဖြစ်ပြီး API အစစ်ချိတ်ဆက်ရန် ကျန်ပါသေးသည်)")
    else:
        st.warning("ကျေးဇူးပြု၍ API Keys အားလုံးနှင့် Video ကို ထည့်ပေးပါ။")
