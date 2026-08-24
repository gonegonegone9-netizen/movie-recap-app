import streamlit as st
import os
import tempfile
import asyncio
import json
import assemblyai as aai
import google.generativeai as genai
import edge_tts
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.audio.CompositeAudioClip import CompositeAudioClip

st.set_page_config(page_title="Movie Dubbing App", page_icon="🎬")

st.title("One-Click Movie Dubbing App 🎬")
st.write("ဗီဒီယိုကို AssemblyAI ဖြင့် စာသားထုတ်၊ Gemini ဖြင့် ဘာသာပြန်၊ Edge TTS ဖြင့် အသံသွင်းကာ အလိုအလျောက် ပေါင်းစပ်ပေးမည့် App ဖြစ်ပါသည်။")

# API Keys များ ထည့်သွင်းခြင်း
with st.expander("🔑 API Keys များ ထည့်ရန် (ဒီကိုနှိပ်ပါ)"):
    aai_key = st.text_input("AssemblyAI API Key:", type="password")
    gemini_key = st.text_input("Gemini API Key:", type="password")

# Video Upload 
st.subheader("၁။ Video ရွေးချယ်ပါ")
uploaded_video = st.file_uploader("Video တင်ရန် (MP4 format)", type=["mp4"])

# အသံ ရွေးချယ်ခြင်း (Edge TTS)
st.subheader("၂။ မြန်မာအသံ ရွေးချယ်ပါ")
voice_choice = st.selectbox(
    "အသံရွေးချယ်ရန်", 
    ["my-MM-NilarNeural", "my-MM-ThihaNeural"]
)

async def generate_tts(text, voice, output_file):
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_file)

if st.button("🚀 Start Dubbing"):
    if uploaded_video and aai_key and gemini_key:
        
        try:
            # ယာယီဗီဒီယိုဖိုင် သိမ်းဆည်းရန်
            tfile = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
            tfile.write(uploaded_video.read())
            video_path = tfile.name

            # ၁။ AssemblyAI ဖြင့် စာသားနှင့် အချိန်ထုတ်ယူခြင်း
            st.info("⏳ ၁။ AssemblyAI ဖြင့် ဗီဒီယိုထဲမှ စာသားနှင့် အချိန်ကို ထုတ်ယူနေပါသည်...")
            aai.settings.api_key = aai_key
            transcriber = aai.Transcriber()
            transcript = transcriber.transcribe(video_path)
            
            if transcript.error:
                st.error(f"AssemblyAI Error: {transcript.error}")
                st.stop()

            segments = []
            if transcript.utterances:
                for u in transcript.utterances:
                    segments.append({
                        "start": u.start,
                        "end": u.end,
                        "text": u.text
                    })
            else:
                paragraphs = transcript.get_paragraphs()
                for p in paragraphs:
                    segments.append({
                        "start": p.start,
                        "end": p.end,
                        "text": p.text
                    })

            if not segments:
                st.warning("ဗီဒီယိုထဲတွင် စာသား (Transcript) မတွေ့ရှိရပါ။")
                st.stop()

            # ၂။ Gemini AI ဖြင့် ဘာသာပြန်ခြင်း
            st.info("⏳ ၂။ Gemini AI ဖြင့် အချိန်ကန့်သတ်ချက် (Max Limit) အတိုင်း မြန်မာလို ဘာသာပြန်နေပါသည်...")
            genai.configure(api_key=gemini_key)
            model = genai.GenerativeModel("gemini-1.5-flash")

            inputs_list = []
            for idx, seg in enumerate(segments):
                duration = (seg["end"] - seg["start"]) / 1000.0
                inputs_list.append(f'ID: {idx} | Time Frame: {seg["start"]/1000.0:.1f}s to {seg["end"]/1000.0:.1f}s (Max Limit: {duration:.1f}s) | Text: "{seg["text"]}"')
            
            prompt = f"""You are a professional video dubbing translator. You MUST translate the following source subtitles into natural spoken Burmese (Myanmar script ONLY, NO English, NO phonetic guides).
  
CRITICAL TIME LIMIT CONSTRAINT: For each subtitle, I have provided the exact Time Frame and the Max Limit in seconds. 
If your Burmese translation takes longer to speak than this time, the TTS audio will OVERLAP and ruin the video. 
You MUST provide a translation that fits perfectly within this time frame. If the time limit is very short, you MUST aggressively compress and summarize the Burmese translation (ချုံ့ပေးပါ) so it can be spoken very fast. Discard polite particles and unnecessary words. Do not translate word-for-word.

SUBTITLE SPLITTING RULE: After each natural sentence or phrase, add the Burmese period (။) to mark the boundary.

Return the result STRICTLY as a JSON object with a single key "translations" which contains an array of strings, where each string is the translated Burmese text corresponding to the input ID in order.

Inputs:
""" + "\n".join(inputs_list)

            response = model.generate_content(
                prompt,
                generation_config={"response_mime_type": "application/json"}
            )
            
            result_json = json.loads(response.text)
            translations = result_json.get("translations", [])

            if len(translations) != len(segments):
                while len(translations) < len(segments):
                    translations.append("")

            # ၃။ Edge TTS ဖြင့် အသံဖိုင်များ ဖန်တီးခြင်း
            st.info("⏳ ၃။ Edge TTS ဖြင့် မြန်မာအသံဖိုင်များ ဖန်တီးနေပါသည်...")
            audio_clips = []

            for idx, seg in enumerate(segments):
                trans_text = translations[idx]
                if not trans_text.strip():
                    continue
                
                audio_filename = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3').name
                
                # Async ဖြင့် အသံထုတ်ခြင်း
                asyncio.run(generate_tts(trans_text, voice_choice, audio_filename))
                
                start_sec = seg["start"] / 1000.0
                audio_clip = AudioFileClip(audio_filename).with_start(start_sec)
                audio_clips.append(audio_clip)

            # ၄။ ဗီဒီယိုနှင့် အသံ ပေါင်းစပ်ခြင်း
            st.info("⏳ ၄။ ဗီဒီယိုနှင့် အသံများကို ပေါင်းစပ်နေပါသည်...")
            video = VideoFileClip(video_path)
            original_audio = video.audio.with_volume_scaled(0.05) if video.audio else None

            if original_audio:
                final_audio = CompositeAudioClip([original_audio] + audio_clips)
            else:
                final_audio = CompositeAudioClip(audio_clips)

            final_video = video.with_audio(final_audio)
            output_video_path = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4').name
            final_video.write_videofile(output_video_path, codec="libx264", audio_codec="aac", fps=24)

            st.success("🎉 အောင်မြင်ပါသည်။ သင့်၏ မြန်မာ Dubbing Video အသစ် ရရှိပါပြီ!")
            st.video(output_video_path)

        except Exception as e:
            st.error(f"အမှားအယွင်း ဖြစ်ပေါ်သည်: {e}")
            
    else:
        st.warning("⚠️ ကျေးဇူးပြု၍ AssemblyAI Key, Gemini Key နှင့် Video ကို ထည့်ပေးပါ။")
