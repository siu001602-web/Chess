import streamlit as st
import chess
from streamlit_chess import chess_board

# 페이지 설정
st.set_page_config(
    page_title="Streamlit 체스 게임 (드래그 앤 드롭)",
    page_icon="♟️",
    layout="centered"
)

st.title("♟️ Streamlit 체스 게임")
st.write("마우스로 말을 드래그해서 놓으면 한 턴씩 자동으로 전환됩니다.")

# 1. 게임 상태 초기화
if "board" not in st.session_state:
    st.session_state.board = chess.Board()

# 2. 게임 리셋 함수
def reset_game():
    st.session_state.board = chess.Board()

# 사이드바 설정 (게임 상태 및 리셋 버튼)
st.sidebar.header("게임 설정 및 상태")
if st.sidebar.button("게임 새로 시작하기", on_click=reset_game):
    st.rerun()

current_turn = "백 (White)" if st.session_state.board.turn == chess.WHITE else "흑 (Black)"
st.sidebar.markdown(f"**현재 턴:** {current_turn}")

# 게임 종료 조건 및 상태 표시
if st.session_state.board.is_checkmate():
    winner = "흑 (Black)" if st.session_state.board.turn == chess.WHITE else "백 (White)"
    st.error(f"🎉 체크메이트! 승자: **{winner}**")
elif st.session_state.board.is_stalemate():
    st.warning("🤝 스테일메이트 (무승부)입니다!")
elif st.session_state.board.is_insufficient_material():
    st.warning("🤝 기물 부족으로 인한 무승부입니다!")
elif st.session_state.board.is_check():
    st.warning("⚠️ 체크 상태입니다!")

# 3. 드래그 앤 드롭 체스판 렌더링
# FEN(체스판의 현재 배치 상태 문자열)을 넘겨주어 상태를 유지합니다.
move_dict = chess_board(
    fen=st.session_state.board.fen(),
    key="interactive_chess_board"
)

# 4. 마우스 드래그로 수가 감지되었을 때 처리
if move_dict and move_dict.get("move"):
    move_uci = move_dict["move"]
    try:
        move = chess.Move.from_uci(move_uci)
        # 규칙에 맞는 수인 경우 board 상태 업데이트
        if move in st.session_state.board.legal_moves:
            st.session_state.board.push(move)
            st.rerun()
    except ValueError:
        pass

# 5. 둘 수 있는 수 목록 (도움말)
with st.expander("현재 둘 수 있는 모든 규칙적인 수 (Legal Moves)"):
    legal_moves = [m.uci() for m in st.session_state.board.legal_moves]
    st.write(", ".join(legal_moves))
