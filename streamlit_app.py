import streamlit as st
import random

# --- 設定とデータ準備 ---
st.set_page_config(page_title="高校物理クイズ", layout="centered")

# 問題データ（本来はCSVやJSONから読み込むのが理想的です）
if 'questions' not in st.session_state:
    st.session_state.questions = [
        {"id": 1, "q": "重力加速度 $g$ の値はおよそいくら？", "a": "9.8", "unit": "m/s^2"},
        {"id": 2, "q": "オームの法則の式は？", "a": "V=RI", "unit": ""},
        {"id": 3, "q": "運動方程式の基本形は？", "a": "F=ma", "unit": ""},
        {"id": 4, "q": "密度を $\rho$、体積を $V$ としたとき、浮力の大きさは？", "a": "ρVg", "unit": "N"},
        {"id": 5, "q": "理想気体の状態方程式は？", "a": "PV=nRT", "unit": ""},
    ]

# --- セッション状態の初期化 ---
if 'history' not in st.session_state:
    st.session_state.history = []  # 解答履歴
if 'current_idx' not in st.session_state:
    st.session_state.current_idx = 0
if 'mode' not in st.session_state:
    st.session_state.mode = "通常"

# --- ヘルパー関数 ---
def get_wrong_questions():
    """間違えた問題のIDを重複なしで抽出"""
    wrong_ids = {h['id'] for h in st.session_state.history if not h['is_correct']}
    return [q for q in st.session_state.questions if q['id'] in wrong_ids]

# --- UI レイアウト ---
st.title("🚀 高校物理 公式クイズ")

# サイドバーでモード切り替え
st.sidebar.header("メニュー")
mode_choice = st.sidebar.radio("モード選択", ["通常モード", "復習モード（ミスのみ）"])

if mode_choice == "通常モード":
    active_questions = st.session_state.questions
    st.session_state.mode = "通常"
else:
    active_questions = get_wrong_questions()
    st.session_state.mode = "復習"

# クイズの進行管理
if not active_questions:
    st.info("間違えた問題はありません！素晴らしい！")
else:
    # 範囲外エラー防止
    if st.session_state.current_idx >= len(active_questions):
        st.session_state.current_idx = 0

    q_data = active_questions[st.session_state.current_idx]

    # 問題表示
    st.subheader(f"問題 {st.session_state.current_idx + 1}")
    st.write(q_data['q'])

    with st.form(key=f"quiz_form_{q_data['id']}"):
        user_answer = st.text_input("答えを入力してください")
        submit = st.form_submit_button("回答する")

        if submit:
            is_correct = (user_answer.strip().lower() == q_data['a'].lower())
            
            # 履歴に追加
            st.session_state.history.append({
                "id": q_data['id'],
                "question": q_data['q'],
                "your_answer": user_answer,
                "correct_answer": q_data['a'],
                "is_correct": is_correct
            })

            if is_correct:
                st.success("正解！")
            else:
                st.error(f"不正解... 答えは {q_data['a']} です。")
            
            # 次の問題へ進むためのボタンを促す
            st.write("下のボタンを押して次の問題へ進んでください。")

    if st.button("次の問題へ ➡️"):
        st.session_state.current_idx = (st.session_state.current_idx + 1) % len(active_questions)
        st.rerun()

# --- 履歴の表示 ---
st.divider()
st.subheader("📊 学習データ")
if st.session_state.history:
    wrong_only = st.checkbox("間違えた問題のみ表示")
    
    display_data = st.session_state.history
    if wrong_only:
        display_data = [h for h in st.session_state.history if not h['is_correct']]
    
    st.table(display_data)
else:
    st.caption("まだ回答データがありません。")

if st.button("履歴をリセット"):
    st.session_state.history = []
    st.rerun()
