import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from datetime import datetime

# 페이지 구성(제목, 아이콘 등) 설정
st.set_page_config(page_title="Streamlit 요소 예제", page_icon="✨", layout="wide")

# 상단 타이틀
st.title("Streamlit: 단일 페이지 요소 모음")
# 간단한 설명(마크다운) - 마크다운을 사용하면 리치 텍스트를 쓸 수 있습니다.
st.markdown("이 페이지는 Streamlit에서 단일 페이지에 넣을 수 있는 주요 요소들의 예시와 사용법을 보여줍니다.")

# --- 레이아웃 데모: 사이드바, 컬럼, 컨테이너 ---
st.sidebar.header("사이드바 예제")
st.sidebar.write("입력 위젯이나 설정을 사이드바에 놓을 수 있습니다.")

# 컬럼을 사용해 가로 레이아웃을 만들기
col1, col2, col3 = st.columns([1, 2, 1])

with col1:
	st.header("컬럼 1")
	st.write("간단한 텍스트와 값")

with col2:
	st.header("컬럼 2: 폼과 입력")
	# 폼 예제: 여러 입력을 모아 한 번에 제출
	with st.form(key='my_form'):
		name = st.text_input('이름 입력', value='홍길동')  # 텍스트 입력
		age = st.number_input('나이', min_value=0, max_value=120, value=30)
		agree = st.checkbox('약관에 동의합니다')
		submitted = st.form_submit_button('제출')
		if submitted:
			# 폼 제출 후 동작
			st.success(f"제출 완료: {name} ({age}세), 동의: {agree}")

with col3:
	st.header("컬럼 3")
	st.metric(label='매출', value='₩1,200,000', delta='5%')  # 메트릭 위젯

st.markdown('---')

# --- 텍스트와 코드 표현 ---
st.subheader('텍스트, 마크다운, 코드, 수식')
st.write('일반 텍스트: write()는 여러 타입을 자동 포맷합니다.')
st.markdown('`st.markdown()` 으로 **굵은 글씨**, _기울임_ 등을 쓸 수 있습니다.')
st.code('''# 예시 코드
for i in range(3):
	print(i)
''')
st.latex(r"E = mc^2")  # 수식

# --- 인터랙티브 위젯 모음 ---
st.subheader('입력 위젯 예시')
# 텍스트 입력
txt = st.text_input('텍스트 입력', placeholder='여기에 입력하세요')
# 텍스트 영역(여러 줄)
memo = st.text_area('메모', value='여러 줄 텍스트를 입력하세요')
# 숫자 입력
num = st.number_input('숫자 입력', value=10)
# 슬라이더
slider_val = st.slider('슬라이더', min_value=0, max_value=100, value=25)
# 선택 박스
option = st.selectbox('선택박스', ['옵션 A', '옵션 B', '옵션 C'])
# 다중 선택
multi = st.multiselect('다중 선택', ['사과', '배', '바나나'], default=['사과'])
# 라디오 버튼
choice = st.radio('라디오', ['하나', '둘', '셋'])
# 체크박스
check = st.checkbox('체크박스 예')
# 버튼
if st.button('버튼 클릭'):
	st.info('버튼이 클릭되었습니다')

# 날짜/시간 입력
date = st.date_input('날짜 선택', value=datetime.today())
time = st.time_input('시간 선택', value=datetime.now().time())

# 파일 업로드
uploaded = st.file_uploader('파일 업로드', type=['csv', 'txt'])
if uploaded is not None:
	st.write('업로드된 파일 이름:', uploaded.name)
	# 판다스로 읽어 화면에 출력 (CSV 가정)
	try:
		df_up = pd.read_csv(uploaded)
		st.dataframe(df_up.head())
	except Exception:
		st.write('CSV가 아닌 파일입니다. 파일 내용을 텍스트로 표시합니다.')
		st.text(uploaded.getvalue().decode('utf-8'))

# 색상 선택기
color = st.color_picker('색상 선택', '#00f900')

st.markdown('---')

# --- 데이터 표시 및 차트 ---
st.subheader('데이터와 차트')
# 예제 데이터프레임 생성
df = pd.DataFrame({
	'x': np.arange(1, 11),
	'y': np.random.randn(10).cumsum(),
	'category': ['A', 'B'] * 5
})

st.dataframe(df)  # 인터랙티브한 데이터프레임
st.table(df.head())  # 정적 테이블

# 간단한 내장 차트
st.line_chart(df[['x', 'y']].set_index('x'))
st.area_chart(df[['x', 'y']].set_index('x'))
st.bar_chart(pd.DataFrame({'a': np.random.randint(0, 10, 5)}))

# Altair 예제: 더 복잡한 차트
chart = alt.Chart(df).mark_circle(size=60).encode(x='x', y='y', color='category')
st.altair_chart(chart, use_container_width=True)

st.markdown('---')

# --- 미디어: 이미지/오디오/비디오/맵 ---
st.subheader('미디어')
st.image('https://placekitten.com/400/200', caption='예시 이미지')
st.audio('https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3')
st.video('https://www.w3schools.com/html/mov_bbb.mp4')

# 지도 예제: 위도/경도 컬럼을 가진 데이터프레임 필요
map_df = pd.DataFrame({
	'lat': [37.5665, 37.5651, 37.5700],
	'lon': [126.9780, 126.9895, 126.9768]
})
st.map(map_df)

st.markdown('---')

# --- 상태/피드백 위젯 ---
st.subheader('상태 표시 및 진행')
with st.spinner('작업 중... 잠시 기다려주세요'):
	# 가벼운 연산 시뮬레이션
	np.random.seed(0)
	_ = np.random.randn(1000).sum()
st.success('완료!')

progress = st.progress(0)
for i in range(100):
	progress.progress(i + 1)

st.balloons()  # 축하 애니메이션

st.info('정보 메시지 예')
st.warning('경고 메시지 예')
st.error('에러 메시지 예')

st.markdown('---')

# --- 확장 가능한 섹션(Expander)과 탭(Tabs) ---
with st.expander('추가 설명 (펼치기)'):
	st.write('여기에 상세 설명이나 옵션을 넣을 수 있습니다.')

tab1, tab2 = st.tabs(['탭 1', '탭 2'])
with tab1:
	st.write('탭 1 내용')
with tab2:
	st.write('탭 2 내용')

st.markdown('---')

# --- 외부 데이터 불러오기(작업 예시) ---
st.subheader('로컬 CSV 불러오기 예시')
try:
	# workspace 내 data/gdp_data.csv 파일이 있으면 읽어서 차트 출력
	gdp = pd.read_csv('data/gdp_data.csv')
	st.write('`data/gdp_data.csv`에서 일부 데이터:')
	st.dataframe(gdp.head())
except FileNotFoundError:
	st.write('데이터 파일이 없습니다: data/gdp_data.csv')

# 하단 메모: 학습용 각주(주석은 코드에 남겨놨습니다)
st.caption('이 파일의 주석을 읽어보면 각 위젯의 사용법을 배울 수 있습니다.')


