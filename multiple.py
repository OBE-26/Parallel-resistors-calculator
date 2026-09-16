import random
import streamlit as st

# הגדרות דף 
st.set_page_config(
    page_title="לומדים את לוח הכפל!", page_icon="✏️", layout="wide"
)

# CSS מתקדם: טבלה שלא נשברת במסכים קטנים ואנימציית מבוך
st.markdown(
    """
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Rubik:wght@400;600;700&display=swap');
    
    html, body, [class*="css"]  {
        font-family: 'Rubik', -apple-system, sans-serif;
        direction: rtl;
        text-align: right;
        -webkit-tap-highlight-color: transparent;
    }
    
    .stApp { background-color: #f4f7f6; }
    
    .main-title {
        font-size: 2rem; color: #2c3e50; text-align: center; font-weight: 700;
    }
    .subtitle {
        font-size: 1.1rem; color: #576574; text-align: center; margin-bottom: 1rem;
    }

    /* === קסם ה-CSS לטבלת 10x10 שלא נשברת לעולם באייפון === */
    /* מכריח את העמודות של Streamlit להישאר בשורה אחת עם גלילה רוחבית */
    div[data-testid="stHorizontalBlock"] {
        flex-wrap: nowrap !important;
        overflow-x: auto;
        -webkit-overflow-scrolling: touch;
        gap: 2px !important;
        padding-bottom: 5px;
    }
    
    div[data-testid="column"] {
        min-width: 32px !important; /* מספיק צר כדי להיכנס למסך, מספיק רחב להקלדה */
    }

    /* עיצוב שדות הטבלה - מונע זום בספארי ומקטין ריווח */
    .stTextInput input {
        text-align: center;
        font-weight: bold;
        font-size: 16px !important; 
        padding: 0px !important;
        height: 35px;
        border-radius: 6px;
    }

    /* === עיצוב המבוך המונפש === */
    .maze-track {
        position: relative;
        height: 70px;
        background: #e8f4f8;
        border-radius: 35px;
        border: 3px solid #b2bec3;
        margin: 30px 0;
        overflow: hidden;
        box-shadow: inset 0 3px 6px rgba(0,0,0,0.1);
    }
    
    .maze-character {
        position: absolute;
        top: 5px;
        font-size: 40px;
        transition: right 0.6s ease-in-out; /* אנימציית התנועה החלקה */
        z-index: 10;
    }

    .maze-gate {
        position: absolute;
        top: 10px;
        font-size: 35px;
        z-index: 5;
    }
    
    .maze-castle {
        position: absolute;
        left: 10px;
        top: 5px;
        font-size: 40px;
        z-index: 5;
    }

    .game-card {
        background: white; padding: 1rem; border-radius: 16px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05); margin-bottom: 1rem;
    }

    .stButton>button {
        width: 100%; border-radius: 12px; font-size: 1.1rem; font-weight: 600;
        background-color: #2e86de; color: white; border: none;
    }
    </style>
""",
    unsafe_allow_html=True,
)

st.markdown('<div class="main-title">✨ לוּחַ הַכֶּפֶל הַקָּסוּם ✨</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">לומְדִים, מְתַרְגְּלִים וּמְשַׂחֲקִים בְּכֵף!</div>', unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs([
    "🧩 לוּחַ כֶּפֶל", "⚡ תִּרְגּוּל מְהִיר", "📖 שְׁאֵלוֹת", "🏃 מִשְׂחָק הַמַּסְלוּל"
])

# ==========================================
# לשונית 1: לוח כפל 10x10 (גלילה אופקית מותאמת אישית)
# ==========================================
with tab1:
  st.subheader("🧩 הַשְׁלָמַת לוּחַ הַכֶּפֶל מָלֵא (10x10)")
  st.write("מַלֵּא/י אֶת הַמִּשְׁבְּצוֹת, גְּלֹל/י הַצִּדָּה אִם הַמָּסָךְ קָטָן, וּבְדוֹק/י!")

  if "checked_grid" not in st.session_state:
    st.session_state.checked_grid = False

  # כותרות (1-10)
  header_cols = st.columns(11)
  header_cols[0].markdown("<h5 style='text-align:center; color:#2e86de;'>✕</h5>", unsafe_allow_html=True)
  for j in range(1, 11):
    header_cols[j].markdown(f"<h5 style='text-align:center;'>{j}</h5>", unsafe_allow_html=True)

  user_answers = {}

  # תוכן הטבלה
  for i in range(1, 11):
    row_cols = st.columns(11)
    row_cols[0].markdown(f"<h5 style='text-align:center; margin-top:6px;'>{i}</h5>", unsafe_allow_html=True)
    for j in range(1, 11):
      val = row_cols[j].text_input("", key=f"cell_{i}_{j}", label_visibility="collapsed")
      if val.strip().isdigit():
        user_answers[(i, j)] = int(val.strip())

  st.write("")
  c_btn1, c_btn2 = st.columns(2)
  with c_btn1:
    if st.button("🔍 בְּדוֹק/י תְּשׁוּבוֹת"): st.session_state.checked_grid = True
  with c_btn2:
    if st.button("🔄 נַקֵּה/י טַבְלָה"):
      for key in list(st.session_state.keys()):
        if key.startswith("cell_"): del st.session_state[key]
      st.session_state.checked_grid = False
      st.rerun()

  if st.session_state.checked_grid:
    if not user_answers:
      st.info("עֲדַיִן לֹא מִלֵּאתָ/תּ אף תְּשׁוּבָה 🙂")
    else:
      correct = sum(1 for (i, j), ans in user_answers.items() if ans == i * j)
      if correct == len(user_answers):
        st.balloons()
        st.success(f"🎉 מֻשְׁלָם! עָנִיתָ/תּ עַל {correct} תְּשׁוּבוֹת נְכוֹנָה!")
      else:
        st.warning(f"עָנִיתָ/תּ עַל {correct} תְּשׁוּבוֹת נְכוֹנוֹת מִתּוֹךְ {len(user_answers)}.")
        for (i, j), ans in user_answers.items():
          if ans != i * j:
            st.write(f"• תרגיל **{i} × {j}**: כָּתַבְתָּ/תּ **{ans}**, התשובה היא **{i*j}**")

# ==========================================
# לשונית 2: תרגול מהיר
# ==========================================
with tab2:
  st.subheader("⚡ תִּרְגּוּל מְהִיר")
  if "q_num1" not in st.session_state:
    st.session_state.q_num1 = random.randint(2, 10)
    st.session_state.q_num2 = random.randint(2, 10)
    st.session_state.score = 0

  n1, n2 = st.session_state.q_num1, st.session_state.q_num2
  st.markdown(f'<div class="game-card" style="text-align:center;"><h2>כַּמָּה זֶה?</h2><h1 style="font-size:3.5rem; color:#10ac84;">{n1} × {n2} = ?</h1></div>', unsafe_allow_html=True)
  
  user_quick_ans = st.text_input("כְּתֹב/י אֶת הַתְּשׁוּבָה שֶׁלְּךָ/ךְ כאן:", key="quick_ans")

  if st.button("בְּדוֹק/י תְּשׁוּבָה"):
    if user_quick_ans.strip().isdigit() and int(user_quick_ans.strip()) == n1 * n2:
      st.balloons()
      st.success("🎉 נָכוֹן מְאֹד!")
      st.session_state.score += 1
      st.session_state.q_num1 = random.randint(2, 10)
      st.session_state.q_num2 = random.randint(2, 10)
    else:
      st.error(f"לֹא נוֹרָא! {n1} × {n2} זה **{n1*n2}**. נַסֵּה/י שוּב בַּתַּרְגִּיל הַבָּא!")
      st.session_state.q_num1 = random.randint(2, 10)
      st.session_state.q_num2 = random.randint(2, 10)
  st.metric("נְקֻדּוֹת שֶׁצָּבַרְתָּ/תּ", st.session_state.score)

# ==========================================
# לשונית 3: שאלות מילוליות
# ==========================================
with tab3:
  st.subheader("📖 שְׁאֵלוֹת מִלּוּלִיּוֹת")
  WORDS = [
      {"q": "לְשָׁקֵד יֵשׁ 4 חֲבִילוֹת שֶׁל צְבָעִים. בְּכָל חֲבִילָה יֵשׁ 6 צְבָעִים. כַּמָּה צְבָעִים יֵשׁ לְשָׁקֵד?", "ans": 24},
      {"q": "בַּגִּנָּה יֵשׁ 5 עֲרוּגוֹת. בְּכָל עֲרוּגָה שְׁתוּלִים 8 פְּרָחִים. כַּמָּה פְּרָחִים יֵשׁ בַּגִּנָּה?", "ans": 40},
  ]
  if "wp_idx" not in st.session_state: st.session_state.wp_idx = 0
  cp = WORDS[st.session_state.wp_idx]

  st.markdown(f'<div class="game-card"><h3>שאלה מס׳ {st.session_state.wp_idx + 1}:</h3><p style="font-size:1.2rem;">{cp["q"]}</p></div>', unsafe_allow_html=True)
  
  wp_ans = st.text_input("תְּשׁוּבָה:", key=f"wp_{st.session_state.wp_idx}")
  if st.button("בְּדוֹק/י"):
    if wp_ans.strip().isdigit() and int(wp_ans.strip()) == cp["ans"]:
      st.balloons(); st.success("🎉 צָדַקְתָּ/תּ!")
    else:
      st.error(f"הַתְּשׁוּבָה הִיא {cp['ans']}.")
  if st.button("שְׁאֵלָה הַבָּאָה ⬅️"):
    st.session_state.wp_idx = (st.session_state.wp_idx + 1) % len(WORDS)
    st.rerun()

# ==========================================
# לשונית 4: משחק המסלול (Side-Scroller Animation)
# ==========================================
with tab4:
  st.subheader("🏃 מִשְׂחָק הַמַּסְלוּל – הַדֶּרֶךְ לָאַרְמוֹן")
  
  if "pos" not in st.session_state:
    st.session_state.pos = 0          # מיקום הדמות (0 עד 10)
    st.session_state.gates = {3: False, 7: False} # שערים נעולים במיקומים 3 ו-7
    st.session_state.q_gate1 = (random.randint(3, 7), random.randint(4, 9))
    st.session_state.q_gate2 = (random.randint(6, 9), random.randint(6, 9))

  pos = st.session_state.pos
  gates = st.session_state.gates

  # ציור מסלול האנימציה (Track)
  # אחוז ההתקדמות (מימין לשמאל: pos=0 זה 0%, pos=10 זה 90% בערך כדי לא לדרוס את הארמון)
  progress_percent = pos * 9 
  
  gate1_icon = "🔓" if gates[3] else "🚪"
  gate2_icon = "🔓" if gates[7] else "🚪"

  st.markdown(f"""
    <div class="maze-track">
        <!-- השחקנית מתקדמת מימין לשמאל -->
        <div class="maze-character" style="right: {progress_percent}%;">👧</div>
        <!-- שער 1 (מיקום 30%) -->
        <div class="maze-gate" style="right: 27%; filter: grayscale({'0' if gates[3] else '1'});">{gate1_icon}</div>
        <!-- שער 2 (מיקום 70%) -->
        <div class="maze-gate" style="right: 63%; filter: grayscale({'0' if gates[7] else '1'});">{gate2_icon}</div>
        <!-- היעד (הארמון) -->
        <div class="maze-castle">🏰</div>
    </div>
  """, unsafe_allow_html=True)

  # מערכת התנועה
  col_btn_r, col_btn_l = st.columns(2)
  
  with col_btn_r:
    if st.button("➡️ זְוּז/י אָחוֹרָה (יָמִינָה)"):
      if pos > 0:
        st.session_state.pos -= 1
        st.rerun()
  
  with col_btn_l:
    if st.button("⬅️ זְוּז/י קָדִימָה (שְׂמֹאלָה)"):
      # בדיקה אם יש שער נעול לפני שזזים קדימה
      if pos == 2 and not gates[3]:
        st.warning("עֲצֹר/רִי! יֵשׁ שַׁעַר נָעוּל לְפָנֶיךָ/ךְ. עֲנֵה/י עַל הַחִידָה לְמַטָּה כְּדֵי לִפְתֹּחַ אוֹתוֹ.")
      elif pos == 6 and not gates[7]:
        st.warning("עֲצֹר/רִי! יֵשׁ עוֹד שַׁעַר נָעוּל. עֲנֵה/י עַל הַחִידָה לְמַטָּה.")
      elif pos < 10:
        st.session_state.pos += 1
        st.rerun()

  # הצגת שאלות כפל לפני שערים
  if pos == 2 and not gates[3]:
    n1, n2 = st.session_state.q_gate1
    st.markdown(f'<div class="game-card" style="text-align:center;"><h3>🔑 חִידָה לִפְתִיחַת הַשַּׁעַר הָרִאשׁוֹן:</h3><h2 style="color:#e67e22;">{n1} × {n2} = ?</h2></div>', unsafe_allow_html=True)
    ans1 = st.text_input("תְּשׁוּבָה:", key="ans_g1")
    if st.button("פְּתַח/י שַׁעַר"):
      if ans1.strip().isdigit() and int(ans1.strip()) == n1 * n2:
        st.session_state.gates[3] = True
        st.session_state.pos += 1
        st.rerun()
      else:
        st.error("טָעוּת! נַסֵּה/י שוּב.")

  if pos == 6 and not gates[7]:
    n1, n2 = st.session_state.q_gate2
    st.markdown(f'<div class="game-card" style="text-align:center;"><h3>🔑 חִידָה לִפְתִיחַת הַשַּׁעַר הַשֵּׁנִי:</h3><h2 style="color:#e67e22;">{n1} × {n2} = ?</h2></div>', unsafe_allow_html=True)
    ans2 = st.text_input("תְּשׁוּבָה:", key="ans_g2")
    if st.button("פְּתַח/י שַׁעַר"):
      if ans2.strip().isdigit() and int(ans2.strip()) == n1 * n2:
        st.session_state.gates[7] = True
        st.session_state.pos += 1
        st.rerun()
      else:
        st.error("טָעוּת! נַסֵּה/י שוּב.")

  # מסך ניצחון
  if pos == 10:
    st.balloons()
    st.success("👑 כָּל הַכָּבוֹד! הִגַּעְתָּ/תּ לָאַרְמוֹן בְּהַצְלָחָה!")
    if st.button("שַׂחֵק/י שׁוּב 🔄"):
      del st.session_state.pos
      st.rerun()
