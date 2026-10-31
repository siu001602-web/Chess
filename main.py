import streamlit as st
import chess
import chess.svg

# 페이지 설정
st.set_page_config(
    page_title="Streamlit 체스 게임",
    page_icon="♟️",
    layout="centered"
)

st.title("♟️ Streamlit 체스 게임")
st.write("흑과 백이 한 턴씩 번갈아 가며 좌표를 입력해 진행하는 체스 게임입니다.")

# 게임 상태 초기화
if "board" not in st.session_state:
    st.session_state.board = chess.Board()

def reset_game():
    st.session_state.board = chess.Board()

# 사이드바 설정
st.sidebar.header("게임 설정 및 상태")
if st.sidebar.button("게임 새로 시작하기", on_click=reset_game):
    st.rerun()

current_turn = "백 (White)" if st.session_state.board.turn == chess.WHITE else "흑 (Black)"
st.sidebar.markdown(f"**현재 턴:** {current_turn}")

# 게임 상태 표시
if st.session_state.board.is_checkmate():
    winner = "흑 (Black)" if st.session_state.board.turn == chess.WHITE else "백 (White)"
    st.error(f"🎉 체크메이트! 승자: **{winner}**")
elif st.session_state.board.is_stalemate():
    st.warning("🤝 스테일메이트 (무승부)입니다!")
elif st.session_state.board.is_check():
    st.warning("⚠️ 체크 상태입니다!")

# 체스판 화면 출력 (SVG 렌더링)
board_svg = chess.svg.board(board=st.session_state.board, size=400)
st.components.v1.html(
    f'<div style="display: flex; justify-content: center;">{board_svg}</div>',
    height=420
)

# 수 입력 폼 (예: e2e4)
st.subheader("수의 이동 입력")
with st.form(key="move_form", clear_on_submit=True):
    move_input = st.text_input("이동할 좌표를 입력하세요 (예: e2e4)", max_chars=5, placeholder="e2e4")
    submit_button = st.form_submit_button(label="수 두기")

if submit_button:
    move_str = move_input.strip().lower()
    try:
        move = chess.Move.from_uci(move_str)
        if move in st.session_state.board.legal_moves:
            st.session_state.board.push(move)
            st.rerun()
        else:
            st.error("규칙에 어긋나는 수입니다. 다시 시도해 주세요.")
    except ValueError:
        st.error("올바른 좌표 형식(UCI)이 아닙니다. (예: e2e4)")

# 현재 둘 수 있는 수 목록
with st.expander("현재 둘 수 있는 가능한 수 (Legal Moves)"):
    legal_moves = [m.uci() for m in st.session_state.board.legal_moves]
    st.write(", ".join(legal_moves))
