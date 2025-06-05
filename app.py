import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
import re

st.set_page_config(page_title="유튜브 자막 복사기", layout="centered")
st.title("📋 유튜브 자막 추출 및 복사기")

video_url = st.text_input("유튜브 영상 링크:")

def extract_video_id(url):
    match = re.search(r"(?:v=|youtu\.be/)([a-zA-Z0-9_-]{11})", url)
    return match.group(1) if match else None

def get_transcript(video_id):
    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        transcript = transcript_list.find_transcript(['ko', 'ko-Hans', 'en', 'en-US'])
        fetched = transcript.fetch()
        texts = [entry.text for entry in fetched]
        return "\n".join(texts)
    except Exception as e:
        return f"[❌ 오류] 자막을 가져오는 중 문제가 발생했습니다:\n{e}"

if st.button("자막 추출"):
    if not video_url:
        st.warning("링크를 입력해 주세요.")
    else:
        video_id = extract_video_id(video_url)
        if not video_id:
            st.error("잘못된 유튜브 링크입니다.")
        else:
            with st.spinner("자막을 추출 중입니다..."):
                transcript = get_transcript(video_id)
                st.subheader("📖 추출된 자막")
                
                # 자막 텍스트 박스 (id를 직접 줘야 JS에서 찾을 수 있음)
                st.text_area("자막", transcript, height=300, key="transcript_box")

                # 복사 버튼 + JS 직접 삽입
                st.markdown(
                    """
                    <script>
                    function copyToClipboard() {
                        const textArea = document.querySelector('textarea');
                        textArea.select();
                        document.execCommand('copy');
                        alert('📋 자막이 복사되었습니다!');
                    }
                    </script>
                    <button onclick="copyToClipboard()" style="padding:0.5em 1em;background:#4CAF50;border:none;border-radius:5px;color:white;cursor:pointer;margin-top:10px;">
                    📋 자막 복사하기
                    </button>
                    """,
                    unsafe_allow_html=True
                )
