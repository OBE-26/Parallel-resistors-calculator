import random
import streamlit as st

# הגדרות דף מותאמות למובייל, אייפד ומחשב
st.set_page_config(
    page_title="לומדים את לוח הכפל!", page_icon="✏️", layout="wide"
)

# הזרקת קוד HTML/CSS מותאם במיוחד ל-Safari באייפון ובאייפד
st.markdown(
    """
    <!-- הגדרות תאימות ל-Safari באייפון/אייפד -->
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <meta name="apple-mobile-web-app-title" content="לוח הכפל">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <link rel="apple-touch-icon" href="https://cdn-icons-png.flaticon.com/512/3426/3426653.png">

    <style>
    @import url('https://fonts.googleapis.com/css2?family=Rubik:wght@400;600;700&display=swap');
    
    html, body, [class*="css"]  {
        font-family: 'Rubik', -apple-system, BlinkMacSystemFont, sans-serif;
        direction: rtl;
        text-align: right;
        -webkit-tap-highlight-color: transparent;
    }
    
    .stApp {
        background-color: #f0f4f8;
    }
    
    .main-title {
        font-size: 2.3rem;
        color: #2c3e50;
        text-align: center;
        font-weight: 700;
        margin-bottom: 0.2rem;
    }
    
    .subtitle {
        font-size: 1.2rem;
        color: #576574;
        text-align: center;
        margin-bottom: 1.5rem;
    }
    
    /* עיצוב כפתורים נגישים ונוחים למגע באייפון/אייפד */
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        font-size: 1.2rem;
        font-weight: 600;
        padding: 0.6rem 1rem;
        background-color: #2e86de;
        color: white;
        border: none;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: all 0.2s ease;
        -webkit-appearance: none;
    }
    
    .stButton>button:hover, .stButton>button:active {
        background-color: #10ac84;
        transform: translateY(-2px);
    }
    
    /* קופסאות משחק */
    .game-card {
        background: white;
        padding: 1.5rem;
        border-radius: 16px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.06);
        margin-bottom: 1rem;
    }

    /* עיצוב שדות קלט בטבלה - גודל 16px מונע זום אוטומטי ב-Safari במיקוד */
    .stTextInput input {
        text-align: center;
        font-weight: bold;
        font-size: 16px !important;
        padding: 4px;
        border-radius: 8px;
        -webkit-appearance: none;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# כותרת ראשית מנוקדת
st.markdown(
    '<div class="main-title">✨ לוּחַ הַכֶּפֶל הַקָּסוּם ✨</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="subtitle">לומְדִים, מְתַרְגְּלִים וּמְשַׂחֲקִים בְּכֵף!</div>',
    unsafe_allow_html=True,
)

# הסבר קצר להוספה למסך הבית באייפון
with st.expander(
    "📱 טיפ: איך להוסיף את האפליקציה למסך הבית באייפון / באייפד (Safari)",
    expanded=False,
):
  st.markdown(
      """
        1. פתח/י את הקישור הזה בדפדפן **Safari**.
        2. לחץ/צי עַל כַּפְתּוֹר הַ**שִׁיתּוּף (Share - המלבן עם החץ כלפי מעלה)**.
        3. גְּלֹל/י לְמַטָּה וּבְחַר/י **"הוֹסֵף לְמָסָךְ הַבַּיִת" (Add to Home Screen)**.
        4. לַחַץ/צי עַל **הוֹסֵף (Add)**.
        """
  )

# לשוניות הניווט
tab1, tab2, tab3, tab4 = st.tabs([
    "🧩 לוּחַ כֶּפֶל לְהַשְׁלָמָה",
    "⚡ תִּרְגּוּל מְהִיר",
    "📖 שְׁאֵלוֹת מִלּוּלִיּוֹת",
    "🏃‍♂️ מִשְׂחָק הַמַּבּוֹךְ (10 שְׁלָבִים)",
])

# ==========================================
# לשונית 1: לוח כפל להשלמה ובדיקה (טבלאי)
# ==========================================
with tab1:
  st.subheader("🧩 הַשְׁלָמַת לוּחַ הַכֶּפֶל")
  st.write(
      "מַלֵּא/י אֶת הַתְּשׁוּבוֹת שֶׁבִּרְצוֹנְךָ/ךְ בַּטַּבְלָה,"
      ' וְלַחַץ/צי עַל **"בְּדוֹק/י אֶת הַתְּשׁוּבוֹת"** כְּדֵי'
      " לִרְאוֹת אִם צָדַקְתָּ/תּ!"
  )

  cols_size = 10
  rows_size = 10

  if "checked_grid" not in st.session_state:
    st.session_state.checked_grid = False

  # כותרת עליונה של הטבלה
  header_cols = st.columns([0.6] + [1] * cols_size)
  header_cols[0].markdown(
      "<h4 style='text-align:center; color:#2e86de;'>✕</h4>",
      unsafe_allow_html=True,
  )
  for j in range(1, cols_size + 1):
    header_cols[j].markdown(
        f"<h4 style='text-align:center;'>{j}</h4>", unsafe_allow_html=True
    )

  user_answers = {}

  # יצירת שורות הטבלה
  for i in range(1, rows_size + 1):
    row_cols = st.columns([0.6] + [1] * cols_size)
    row_cols[0].markdown(
        f"<h4 style='text-align:center; margin-top:5px;'>{i}</h4>",
        unsafe_allow_html=True,
    )
    for j in range(1, cols_size + 1):
      key = f"cell_{i}_{j}"
      val = row_cols[j].text_input(
          "", key=key, label_visibility="collapsed", placeholder=""
      )
      if val.strip().isdigit():
        user_answers[(i, j)] = int(val.strip())

  st.write("")
  col_btn1, col_btn2 = st.columns([1, 1])
  with col_btn1:
    if st.button("🔍 בְּדוֹק/י אֶת הַתְּשׁוּבוֹת"):
      st.session_state.checked_grid = True

  with col_btn2:
    if st.button("🔄 נַקֵּה/י טַבְלָה"):
      for key in list(st.session_state.keys()):
        if key.startswith("cell_"):
          del st.session_state[key]
      st.session_state.checked_grid = False
      st.rerun()

  # הצגת תוצאות הבדיקה
  if st.session_state.checked_grid:
    if not user_answers:
      st.info("עֲדַיִן לֹא מִלֵּאתָ/תּ אף תְּשׁוּבָה בַּטַּבְלָה 🙂")
    else:
      correct_count = 0
      wrong_details = []

      for (i, j), ans in user_answers.items():
        real_ans = i * j
        if ans == real_ans:
          correct_count += 1
        else:
          wrong_details.append(
              f"תרגיל **{i} × {j}**: כָּתַבְתָּ/תּ **{ans}**, הַתְּשׁוּבָה"
              f" הַנְּכוֹנָה הִיא **{real_ans}**"
          )

      if len(wrong_details) == 0:
        st.balloons()
        st.success(
            f"🎉 כָּל הַכָּבוֹד! כָּל {correct_count} הַתְּשׁוּבוֹת שֶׁמִּלֵּאתָ/תּ"
            " נְכוֹנוֹת בְּמַדְעָן!"
        )
      else:
        st.warning(
            f"עָנִיתָ/תּ עַל {correct_count} תְּשׁוּבוֹת נְכוֹנוֹת מִתּוֹךְ"
            f" {len(user_answers)}."
        )
        st.error("הִנֵּה הַמְּקוֹמוֹת שֶׁכְּדַאי לְתַקֵּן:")
        for w in wrong_details:
          st.write(f"• {w}")

# ==========================================
# לשונית 2: תרגול מהיר
# ==========================================
with tab2:
  st.subheader("⚡ תִּרְגּוּל מְהִיר")

  if "q_num1" not in st.session_state:
    st.session_state.q_num1 = random.randint(2, 10)
    st.session_state.q_num2 = random.randint(2, 10)
    st.session_state.score = 0

  n1 = st.session_state.q_num1
  n2 = st.session_state.q_num2

  st.markdown(
      f'<div class="game-card" style="text-align: center;">'
      f"<h2>כַּמָּה זֶה?</h2>"
      f'<h1 style="font-size: 3.5rem; color: #10ac84;">{n1} × {n2} = ?</h1>'
      f"</div>",
      unsafe_allow_html=True,
  )

  user_quick_ans = st.text_input(
      "כְּתֹב/י אֶת הַתְּשׁוּבָה שֶׁלְּךָ/ךְ כאן:", key="quick_ans"
  )

  if st.button("בְּדוֹק/י תְּשׁוּבָה"):
    if user_quick_ans.strip().isdigit():
      ans = int(user_quick_ans.strip())
      if ans == n1 * n2:
        st.balloons()
        st.success("🎉 נָכוֹן מְאֹד! כָּל הַכָּבוֹד!")
        st.session_state.score += 1
        st.session_state.q_num1 = random.randint(2, 10)
        st.session_state.q_num2 = random.randint(2, 10)
      else:
        st.error(
            f"לֹא נוֹרָא! {n1} × {n2} זה **{n1*n2}**. נַסֵּה/י אֶת הַתַּרְגִּיל"
            " הַבָּאָה!"
        )
        st.session_state.q_num1 = random.randint(2, 10)
        st.session_state.q_num2 = random.randint(2, 10)
    else:
      st.warning("אָנָּא כְּתֹב/י מִסְפָּר.")

  st.metric("נְקֻדּוֹת שֶׁצָּבַרְתָּ/תּ", st.session_state.score)

# ==========================================
# לשונית 3: שאלות מילוליות
# ==========================================
with tab3:
  st.subheader("📖 שְׁאֵלוֹת מִלּוּלִיּוֹת")

  WORD_PROBLEMS = [
      {
          "q": (
              "לְשָׁקֵד יֵשׁ 4 חֲבִילוֹת שֶׁל צְבָעִים. בְּכָל חֲבִילָה יֵשׁ 6"
              " צְבָעִים. כַּמָּה צְבָעִים יֵשׁ לְשָׁקֵד בְּסַךְ הַכֹּל?"
          ),
          "n1": 4,
          "n2": 6,
          "ans": 24,
      },
      {
          "q": (
              "בַּגִּנָּה יֵשׁ 5 עֲרוּגוֹת. בְּכָל עֲרוּגָה שְׁתוּלִים 8"
              " פְּרָחִים. כַּמָּה פְּרָחִים יֵשׁ בַּגִּנָּה?"
          ),
          "n1": 5,
          "n2": 8,
          "ans": 40,
      },
      {
          "q": (
              "אִמָּא קָנְתָה 7 שַׂקִּיּוֹת תַּפּוּחִים. בְּכָל שַׂקִּית יֵשׁ"
              " 3 תַּפּוּחִים. כַּמָּה תַּפּוּחִים יֵשׁ בְּסַךְ הַכֹּל?"
          ),
          "n1": 7,
          "n2": 3,
          "ans": 21,
      },
      {
          "q": (
              "בְּכִתָּה יֵשׁ 9 שֻׁלְחָנוֹת. סְבִיב כָּל שֻׁלְחָן יוֹשְׁבִים 4"
              " יְלָדִים. כַּמָּה יְלָדִים יוֹשְׁבִים בַּכִּתָּה?"
          ),
          "n1": 9,
          "n2": 4,
          "ans": 36,
      },
      {
          "q": (
              "דָּנִי קָנָה 8 מַחְבָּרוֹת. כָּל מַחְבֶּרֶת עוֹלָה 5 שְׁקָלִים."
              " כַּמָּה שִׁלֵּם דָּנִי בְּסַךְ הַכֹּל?"
          ),
          "n1": 8,
          "n2": 5,
          "ans": 40,
      },
  ]

  if "wp_idx" not in st.session_state:
    st.session_state.wp_idx = 0

  current_p = WORD_PROBLEMS[st.session_state.wp_idx]

  st.markdown(
      f'<div class="game-card">'
      f"<h3>שאלה מס׳ {st.session_state.wp_idx + 1}:</h3>"
      f'<p style="font-size: 1.3rem;">{current_p["q"]}</p>'
      f"</div>",
      unsafe_allow_html=True,
  )

  wp_ans = st.text_input("תְּשׁוּבָה:", key=f"wp_{st.session_state.wp_idx}")

  if st.button("בְּדוֹק/י שְׁאָלָה מִלּוּלִית"):
    if wp_ans.strip().isdigit():
      if int(wp_ans.strip()) == current_p["ans"]:
        st.balloons()
        st.success(
            f"🎉 נָכוֹן מְאֹד! הַתַּרְגִּיל הוּא {current_p['n1']} ×"
            f" {current_p['n2']} = {current_p['ans']}"
        )
      else:
        st.error(
            f"לֹא מְדֻיָּק. הַתַּרְגִּיל הוּא {current_p['n1']} ×"
            f" {current_p['n2']} = {current_p['ans']}."
        )
    else:
      st.warning("אָנָּא כְּתֹב/י מִסְפָּר.")

  if st.button("הַשְּׁאָלָה הַבָּאָה ⬅️"):
    st.session_state.wp_idx = (st.session_state.wp_idx + 1) % len(
        WORD_PROBLEMS
    )
    st.rerun()

# ==========================================
# לשונית 4: משחק המבוך (10 שלבים עם אנימציית הליכה)
# ==========================================
with tab4:
  st.subheader("🏃‍♂️ מִשְׂחָק הַמַּבּוֹךְ – הַמַּסָּע לָאַרְמוֹן (10 שְׁלָבִים)")
  st.write(
      "הַזֵּז/י אֶת הַיֶּלֶד צַעַד אַחַר צַעַד עַל יְדֵי פִּתְרוֹן"
      " תַּרְגִּילֵי כֶּפֶל עד לְהַגָּעָה לָאַרְמוֹן!"
  )

  # 10 שלבים מובנים
  MAZE_STEPS = [
      {"n1": 2, "n2": 3, "name": "שַׁעַר 1"},
      {"n1": 3, "n2": 4, "name": "שַׁעַר 2"},
      {"n1": 4, "n2": 5, "name": "שַׁעַר 3"},
      {"n1": 5, "n2": 6, "name": "שַׁעַר 4"},
      {"n1": 6, "n2": 7, "name": "שַׁעַר 5"},
      {"n1": 7, "n2": 7, "name": "שַׁעַר 6"},
      {"n1": 8, "n2": 6, "name": "שַׁעַר 7"},
      {"n1": 9, "n2": 5, "name": "שַׁעַר 8"},
      {"n1": 8, "n2": 9, "name": "שַׁעַר 9"},
      {"n1": 9, "n2": 9, "name": "שַׁעַר 10 – הָאַרְמוֹן!"},
  ]

  if "maze_step" not in st.session_state:
    st.session_state.maze_step = 0

  curr_step = st.session_state.maze_step
  total_steps = len(MAZE_STEPS)

  # תצוגת מסלול ההליכה (מותאמת לרזולוציות מובייל ו-Safari)
  path_html = "<div style='display:flex; justify-content:space-between; align-items:center; background:white; padding:15px; border-radius:15px; font-size:1.3rem; border:2px solid #e0e0e0; margin-bottom:15px; overflow-x:auto; -webkit-overflow-scrolling: touch;'>"

  for idx in range(total_steps):
    if idx < curr_step:
      path_html += "<span style='opacity:0.6;'>🟢</span>"
    elif idx == curr_step:
      path_html += (
          "<span style='font-size:2rem; transform:scale(1.2);"
          " display:inline-block;'>👦</span>"
      )
    else:
      path_html += "<span style='opacity:0.3;'>⚪</span>"

  path_html += "<span>🏰</span></div>"
  st.markdown(path_html, unsafe_allow_html=True)

  if curr_step < total_steps:
    step_data = MAZE_STEPS[curr_step]
    n1, n2 = step_data["n1"], step_data["n2"]

    st.info(f"📍 שְׁלָב {curr_step + 1} מִתּוֹךְ {total_steps}: {step_data['name']}")

    st.markdown(
        f'<div class="game-card" style="text-align:center;">'
        f'<h2>כְּדֵי לִצְעֹד צַעַד קָדִימָה, פְּתֹר/י:</h2>'
        f'<h1 style="font-size:3rem; color:#e67e22;">{n1} × {n2} = ?</h1>'
        f'</div>',
        unsafe_allow_html=True,
    )

    maze_ans = st.text_input("תְּשׁוּבָה:", key=f"maze_ans_{curr_step}")

    if st.button("צְעַד/י קָדִימָה! 🚶‍♂️"):
      if maze_ans.strip().isdigit() and int(maze_ans.strip()) == n1 * n2:
        st.balloons()
        st.success("🔓 נָכוֹן מְאֹד! הַיֶּלֶד צָעַד צַעַד קָדִימָה!")
        st.session_state.maze_step += 1
        st.rerun()
      else:
        st.error("הַתְּשׁוּבָה לֹא מְדֻיֶּקֶת... נַסֵּה/י שוּב!")
  else:
    st.balloons()
    st.markdown(
        '<div class="game-card" style="text-align:center;">'
        '<h2>👑 כָּל הַכָּבוֹד! הַיֶּלֶד הִגִּיעַ לָאַרְמוֹן! 👑</h2>'
        '<p style="font-size:1.3rem;">פָּתַחְתָּ/תּ אֶת כָּל 10 הַשְּׁעָרִים'
        ' בְּהַצְלָחָה רַבָּה!</p>'
        '</div>',
        unsafe_allow_html=True,
    )
    if st.button("הַתְחֵל/י מִשְׂחָק חָדָשׁ 🔄"):
      st.session_state.maze_step = 0
      st.rerun()
