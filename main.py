import streamlit as st
import chess
import chess.svg

# 페이지 설정
st.set_page_config(
    page_title="Streamlit 체스 게임 (클릭 이동)",
    page_icon="♟️",
    layout="centered"
)

st.title("♟️ Streamlit 체스 게임")
st.write("직접 타이핑할 필요 없이, 클릭(선택)하여 출발지와 목적지를 지정해 이동하세요.")

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
board_svg = chess.svg.board(board=st.session_state.board, size=380)
st.components.v1.html(
    f'<div style="display: flex; justify-content: center;">{board_svg}</div>',
    height=400
)

# 클릭 기반(셀렉트박스) 이동 인터페이스
st.subheader("말 이동하기")

# 현재 둘 수 있는 합법적인 수들 추출
legal_moves = list(st.session_state.board.legal_moves)

# 출발지 목록 (현재 턴의 기물이 있는 칸들)
from_squares = sorted(list(set([move.from_square for move in legal_moves])))
from_square_names = [chess.square_name(sq) for sq in from_squares]

col1, col2 = st.columns(2)

with col1:
    selected_from = st.selectbox(
        "1단계: 이동할 말(출발지) 선택", 
        from_square_names if from_square_names else ["없음"]
    )

# 선택한 출발지에서 갈 수 있는 목적지 목록 자동 필터링
to_square_names = []
if selected_from and selected_from != "없음":
    from_sq_idx = chess.parse_square(selected_from)
    to_squares = [move.to_square for move in legal_moves if move.from_square == from_sq_idx]
    to_square_names = sorted([chess.square_name(sq) for sq in to_squares])

with col2:
    selected_to = st.selectbox(
        "2단계: 갈 곳(목적지) 선택", 
        to_square_names if to_square_names else ["먼저 출발지를 선택하세요"]
    )

if st.button("수 두기 실행", type="primary", use_container_width=True):
    if selected_from and selected_to and selected_to != "먼저 출발지를 선택하세요":
        move_str = selected_from + selected_to
        try:
            move = chess.Move.from_uci(move_str)
            if move in st.session_state.board.legal_moves:
                st.session_state.board.push(move)
                st.rerun()
            else:
                st.error("규칙에 어긋나는 수입니다.")
        except ValueError:
            st.error("올바르지 않은 이동입니다.")
    else:
        st.warning("출발지와 목적지를 모두 올바르게 선택해 주세요.")
