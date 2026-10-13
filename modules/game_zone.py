import streamlit as st
import heapq

GOAL = (1, 2, 3, 4, 5, 6, 7, 8, 0)
LINES = [(0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6)]

def a_star_hint(state: tuple) -> str:
    """Compute the next optimal move for 8-puzzle using A* with Manhattan distance."""
    pos = {v: (i // 3, i % 3) for i, v in enumerate(GOAL)}
    h = lambda s: sum(abs(i // 3 - pos[v][0]) + abs(i % 3 - pos[v][1]) for i, v in enumerate(s) if v)
    pq, visited = [(h(state), 0, state, [])], {state: 0}
    while pq:
        _, g, s, path = heapq.heappop(pq)
        if s == GOAL:
            return f"Slide Tile {path[0][0]} {path[0][1]}" if path else "Puzzle Solved!"
        idx = s.index(0)
        r, c = idx // 3, idx % 3
        for dr, dc, m in [(-1,0,"Down"), (1,0,"Up"), (0,-1,"Right"), (0,1,"Left")]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < 3 and 0 <= nc < 3:
                nidx = nr * 3 + nc
                ns = list(s)
                ns[idx], ns[nidx] = ns[nidx], ns[idx]
                t = tuple(ns)
                if t not in visited or g + 1 < visited[t]:
                    visited[t] = g + 1
                    heapq.heappush(pq, (g + 1 + h(t), g + 1, t, path + [(s[nidx], m)]))
    return "No solution found."

def minimax(b: list, is_ai: bool) -> int:
    """Evaluate game tree states recursively with Minimax for Tic-Tac-Toe."""
    if any(all(b[i] == 'O' for i in ln) for ln in LINES): return 10
    if any(all(b[i] == 'X' for i in ln) for ln in LINES): return -10
    if ' ' not in b: return 0
    scores = [minimax(b[:i] + ['O' if is_ai else 'X'] + b[i+1:], not is_ai) for i in range(9) if b[i] == ' ']
    return max(scores) if is_ai else min(scores)

def ai_move(b: list) -> int:
    """Determine the optimal move index for the AI player using Minimax."""
    moves = [(minimax(b[:i] + ['O'] + b[i+1:], False), i) for i in range(9) if b[i] == ' ']
    return max(moves)[1] if moves else -1

def run():
    """Render the Game Zone featuring 8-puzzle (A*) and Tic-Tac-Toe (Minimax)."""
    c_puz, c_ttt = st.columns(2)
    with c_puz:
        st.markdown('<div class="campus-card"><div class="card-title">🧩 Practical 4: 8-Puzzle (A* Search)</div>'
                    '<div class="card-subtitle">Heuristic: Manhattan Distance</div>', unsafe_allow_html=True)
        if "puzzle_s" not in st.session_state: st.session_state.puzzle_s = (1, 2, 3, 4, 0, 5, 7, 8, 6)
        s = st.session_state.puzzle_s
        for r in range(3):
            cols = st.columns(3)
            for c in range(3):
                v = s[r * 3 + c]
                cols[c].markdown(f'<div class="{"tile-box" if v else "tile-empty"}">{v if v else ""}</div>', unsafe_allow_html=True)
        h1, h2 = st.columns(2)
        if h1.button("💡 Hint (A*)", type="primary"):
            st.markdown(f'<span class="chip chip-teal">● {a_star_hint(s)}</span>', unsafe_allow_html=True)
        if h2.button("🔄 Reset Puzzle"):
            st.session_state.puzzle_s = (1, 2, 3, 4, 0, 5, 7, 8, 6)
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with c_ttt:
        st.markdown('<div class="campus-card"><div class="card-title">⭕ Practical 5: Tic-Tac-Toe (Minimax)</div>'
                    '<div class="card-subtitle">Unbeatable AI: You (X) vs AI (O)</div>', unsafe_allow_html=True)
        if "ttt_b" not in st.session_state: st.session_state.ttt_b = [' '] * 9
        b = st.session_state.ttt_b
        winner = 'O' if any(all(b[i]=='O' for i in ln) for ln in LINES) else ('X' if any(all(b[i]=='X' for i in ln) for ln in LINES) else ('Draw' if ' ' not in b else None))
        for r in range(3):
            cols = st.columns(3)
            for c in range(3):
                i = r * 3 + c
                if cols[c].button(b[i], key=f"t_{i}", disabled=(b[i] != ' ' or winner is not None)):
                    b[i] = 'X'
                    if not any(all(b[k]=='X' for k in ln) for ln in LINES) and ' ' in b:
                        m = ai_move(b)
                        if m != -1: b[m] = 'O'
                    st.rerun()
        status = '<span class="chip chip-red">● AI Won!</span>' if winner == 'O' else ('<span class="chip chip-amber">● Draw Game!</span>' if winner == 'Draw' else '<span class="chip chip-indigo">● Status: AI ready (Your turn X)</span>')
        st.markdown(status, unsafe_allow_html=True)
        if st.button("🔄 Reset Game"):
            st.session_state.ttt_b = [' '] * 9
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
