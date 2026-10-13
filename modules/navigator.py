import streamlit as st
from collections import deque

GRAPH = {
    "Main Gate": ["Admin Block", "Library"],
    "Admin Block": ["Main Gate", "Canteen", "Auditorium"],
    "Library": ["Main Gate", "Lab", "Placement Cell"],
    "Canteen": ["Admin Block"],
    "Auditorium": ["Admin Block"],
    "Lab": ["Library"],
    "Placement Cell": ["Library"],
}

def bfs(start: str, goal: str) -> list[str]:
    """Find the shortest path between start and goal using Breadth-First Search."""
    queue, visited = deque([[start]]), {start}
    while queue:
        path = queue.popleft()
        if path[-1] == goal:
            return path
        for nbr in GRAPH.get(path[-1], []):
            if nbr not in visited:
                visited.add(nbr)
                queue.append(path + [nbr])
    return []

def dfs(start: str, goal: str) -> list[str]:
    """Find a path between start and goal using Depth-First Search."""
    stack, visited = [[start]], set()
    while stack:
        path = stack.pop()
        node = path[-1]
        if node == goal:
            return path
        if node not in visited:
            visited.add(node)
            for nbr in reversed(GRAPH.get(node, [])):
                if nbr not in visited:
                    stack.append(path + [nbr])
    return []

def run():
    """Render the campus navigator interface comparing BFS and DFS traversal."""
    st.markdown('<div class="campus-card">'
                '<div class="card-title">🧭 Practical 3: Campus Route Navigator</div>'
                '<div class="card-subtitle">Graph Search Traversal: Breadth-First Search vs Depth-First Search</div>',
                unsafe_allow_html=True)
    nodes = list(GRAPH.keys())
    c1, c2, c3 = st.columns([1, 1, 1])
    start = c1.selectbox("Start Location", nodes, index=0)
    goal = c2.selectbox("Goal Location", nodes, index=3)
    algo = c3.radio("Search Strategy", ["BFS (Shortest)", "DFS (Depth-First)"])
    find = st.button("Find Route", type="primary")
    st.markdown('</div>', unsafe_allow_html=True)

    if find or "nav_path" in st.session_state:
        if find:
            st.session_state.nav_path = bfs(start, goal) if "BFS" in algo else dfs(start, goal)
            st.session_state.nav_algo = algo
        path = st.session_state.get("nav_path", [])
        st.markdown(f'<div class="campus-card"><div class="card-title">📍 Path Result: {st.session_state.get("nav_algo", "")}</div>', unsafe_allow_html=True)
        if path:
            chips = " ".join(f'<span class="chip chip-indigo">{node}</span>' + ('<span class="arrow-separator">➔</span>' if i < len(path)-1 else '') for i, node in enumerate(path))
            st.markdown(f'<div class="route-container">{chips}</div>', unsafe_allow_html=True)
            st.write(f"✨ **Total Steps:** `{len(path) - 1} hops` ({len(path)} landmarks visited)")
        else:
            st.markdown('<span class="chip chip-amber">⚠️ No path found between selected locations</span>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
