import streamlit as st

# 초등학교 곱셈 학습 앱
# 이 앱은 사용자가 두 숫자를 입력하고 선택한 그림으로 곱셈 결과를 시각화한 뒤
# 사용자가 직접 계산 결과를 입력하여 정답 여부를 확인하도록 설계되었습니다.

st.set_page_config(page_title="초등 곱셈 학습", page_icon="✏️", layout="centered")

st.title("초등 곱셈 연습장")
st.markdown("간단한 곱셈을 그림으로 시각화하고 직접 답을 입력해보세요. (최대 12×12)")

# --- 입력 영역: 두 숫자와 그림 선택 ---
st.header("문제 설정")
# 숫자 입력: 1 ~ 12 범위로 제한하여 시각화가 과도하게 커지지 않도록 함
col_a, col_b = st.columns(2)
with col_a:
	a = st.number_input('첫 번째 수 (가로/행)', min_value=1, max_value=12, value=3, step=1, key='a')
with col_b:
	b = st.number_input('두 번째 수 (세로/열)', min_value=1, max_value=12, value=4, step=1, key='b')

# 그림 선택: 드롭다운 대신 그림을 직접 보고 선택할 수 있도록 구현
st.write('사용할 그림을 아래에서 직접 선택하세요:')
pics = [('사과', '🍎'), ('별', '⭐'), ('고양이', '🐱'), ('공', '⚽'), ('나비', '🦋')]

# 세션 상태에 선택값이 없으면 기본값 설정
if 'selected_pic' not in st.session_state:
	st.session_state.selected_pic = pics[0][1]

# 그림들을 가로로 배치하여 각 그림 아래에 선택 버튼을 둠
cols_pic = st.columns(len(pics))
for (name, emj), col in zip(pics, cols_pic):
	with col:
		# 이모지 크게 표시
		st.markdown(f"<div style='font-size:48px; text-align:center'>{emj}</div>", unsafe_allow_html=True)
		# 각 그림마다 별도의 버튼을 만들어 클릭 시 선택을 저장
		if st.button(f"선택\n{name}", key=f"select_{name}"):
			st.session_state.selected_pic = emj

st.write('선택한 그림:', next(f"{n} {e}" for n, e in pics if e == st.session_state.selected_pic))

# 버튼을 눌러 시각화 실행 — 사용자가 명시적으로 시각화를 실행하도록 함
if 'visualized' not in st.session_state:
	st.session_state.visualized = False

if st.button('시각화'):
	# 시각화 요청 시 세션 상태에 값 저장
	st.session_state.visualized = True
	st.session_state.rows = a
	st.session_state.cols = b
	# 선택된 그림(세션 상태)을 사용 — 기본값은 사과
	st.session_state.emoji = st.session_state.get('selected_pic', '🍎')
	# 정답 체크 결과 초기화
	st.session_state.checked = False
	st.session_state.last_result = None

# 초기화 버튼: 모든 학습 상태를 제거
if st.button('초기화'):
	for k in list(st.session_state.keys()):
		del st.session_state[k]
	st.experimental_rerun()

st.markdown('---')

# --- 시각화 영역: 그림으로 곱셈 결과 표시 ---
if st.session_state.get('visualized'):
	rows = st.session_state.rows
	cols = st.session_state.cols
	emoji = st.session_state.emoji

	st.header('시각화')
	st.write(f"문제: {rows} × {cols} = ?")
	st.write('아래 그림을 보며 곱셈의 의미(행 × 열)를 이해해보세요.')

	# 그림을 행/열 형태로 표시
	# 각 행마다 컬럼을 생성해서 가운데 정렬된 이모지를 표시
	for r in range(rows):
		cols_layout = st.columns(cols)
		for c_idx, col in enumerate(cols_layout):
			# HTML을 이용해 이모지 크기를 키워서 보기 쉽게 만듦
			col.markdown(f"<div style='font-size:36px; text-align:center'>{emoji}</div>", unsafe_allow_html=True)

	st.markdown('---')

	# --- 정답 입력 및 채점 ---
	st.subheader('정답 입력')
	# 사용자가 입력한 값으로 정답 확인 버튼을 눌러 채점
	user_answer = st.number_input('곱셈 결과를 입력하세요', min_value=0, max_value=200, value=0, step=1, key='user_answer')
	if st.button('정답 확인'):
		correct = rows * cols
		is_correct = (int(user_answer) == correct)
		st.session_state.checked = True
		st.session_state.last_result = is_correct
		if is_correct:
			st.success(f'정답입니다! {rows} × {cols} = {correct}')
		else:
			st.error(f'틀렸어요. 다시 시도해보세요. (힌트: {rows} × {cols} = {correct})')

	# 사용자가 채점 후 결과 확인 영역
	if st.session_state.get('checked'):
		if st.session_state.last_result:
			st.balloons()

	# 학습 팁 섹션: 왜 곱셈을 이렇게 시각화하는지 설명
	with st.expander('학습 팁: 왜 이렇게 시각화하나요?'):
		st.write('행×열로 배열을 그리면 곱셈이 덧셈의 반복임을 쉽게 이해할 수 있습니다.')

else:
	st.info('왼쪽에서 두 수를 입력하고 "시각화" 버튼을 눌러 시작하세요.')

# 하단 도움말: 간단한 사용 가이드
st.markdown('---')
st.caption('사용법: 숫자를 선택 → 그림 선택 → "시각화" → 결과 입력 → "정답 확인"')



