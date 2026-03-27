from typing import Dict, List

# per-session in-memory history store
sessions: Dict[str, List[Dict[str, str]]] = {}


def save_context(session_id: str, user: str, bot: str):
    if session_id not in sessions:
        sessions[session_id] = []
    sessions[session_id].append({"user": user, "bot": bot})


def get_history(session_id: str) -> str:
    if session_id not in sessions or not sessions[session_id]:
        return ""
    history_lines = []
    for item in sessions[session_id]:
        history_lines.append(f"User: {item['user']}\nAssistant: {item['bot']}")
    return "\n".join(history_lines)


def reset_session(session_id: str):
    sessions.pop(session_id, None)