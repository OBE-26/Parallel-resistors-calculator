import random
import streamlit as st

# הגדרות דף מותאמות למובייל, אייפד ומחשב
st.set_page_config(
    page_title="לומדים את לוח הכפל!", page_icon="✏️", layout="wide"
)

# הזרקת עיצוב CSS לתמיכה בניקוד, פונטים קריאים ואנימציות
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Rubik:wght@400;600;700&display=swap');
    
    html, body, [class*="css"]  {
        font-family: 'Rubik', sans-serif;
        direction: rtl;
        text-align: right;
    }
    
    .stApp {
        background-color: #f7f9fc;
    }
    
    .main-title {
        font-size: 2.2rem;
        color: #2c3e50;
        text-align: center;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    .subtitle {
        font-size: 1.2rem;
        color: #7f8c8d;
        text-align: center;
        margin-bottom: 1.5rem;
    }
    
    /* עיצוב כפתורים גדולים ונוחים למגע באייפד ובמובייל */
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        font-size: 1.2rem;
        font-weight: 600;
        padding: 0.6rem 1rem;
        background-color: #4ea8de;
        color: white;
        border: none;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: all 0.2s ease;
    }
    
    .stButton>button:hover {
        background-color: #4895ef;
        transform: translateY(-2px);
    }
    
    /* עיצוב כרטיסיות משחק */
    .game-card {
        background: white;
        padding: 1.5rem;
        border-radius: 16px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        margin-bottom: 1rem;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# כותרת הראשית עם ניקוד
st.markdown(
    '<div class="main-title">✨ לוּחַ הַכֶּפֶל הַקָּסוּם ✨</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="subtitle">לומְדִים, מְתַרְגְּלִים וּמְשַׂחֲקִים בְּכֵף!</div>',
    unsafe_allow_html=True,
)

# יצירת לשוניות ניווט
tab1, tab2, tab3, tab4 = st.tabs([
    "🧩 לוּחַ כֶּפֶל לְהַשְׁלָמָה",
    "⚡ תִּרְגּוּל מְהִיר",
    "📖 שְׁאֵלוֹת מִלּוּלִיּוֹת",
    "🎮 מִשְׂחָק הַמַּבּוֹךְ",
])

# ==========================================
# לשונית 1: לוח כפל להשלמה ובדיקה
# ==========================================
with tab1:
  st.subheader("🧩 הַשְׁלָמַת לוּחַ הַכֶּפֶל")
  st.write(
      "מַלְאִי אֶת הַתְּשׁוּבוֹת שֶׁאַתְּ רוֹצָה בַּטַּבְלָה, וְלַחֲצִי עַל"
      ' **"בְּדוֹק אֶת הַתְּשׁוּבוֹת"** כְּדֵי לִרְאוֹת אִם צָדַקְתְּ!'
  )

  # גודל הטבלה (1 עד 10)
  cols_size = 10
  rows_size = 10

  # ניהול מצב הבדיקה
  if "checked_grid" not in st.session_state:
    st.session_state.checked_grid = False

  # יצירת מודול הטבלה באמצעות עמודות Streamlit
  header_cols = st.columns(cols_size + 1)
  header_cols[0].markdown("**X**")
  for j in range(1, cols_size + 1):
    header_cols[j].markdown(f"**{j}**")

  user_answers = {}
  for i in range(1, rows_size + 1):
    row_cols = st.columns(cols_size + 1)
    row_cols[0].markdown(f"**{i}**")
    for j in range(1, cols_size + 1):
      key = f"cell_{i}_{j}"
      val = row_cols[j].text_input(
          "", key=key, label_visibility="collapsed", placeholder=""
      )
      if val.strip().isdigit():
        user_answers[(i, j)] = int(val.strip())

  col_btn1, col_btn2 = st.columns([1, 1])
  with col_btn1:
    if st.button("🔍 בְּדוֹק אֶת הַתְּשׁוּבוֹת"):
      st.session_state.checked_grid = True

  with col_btn2:
    if st.button("🔄 נַקֵּה טַבְלָה"):
      for key in list(st.session_state.keys()):
        if key.startswith("cell_"):
          del st.session_state[key]
      st.session_state.checked_grid = False
      st.rerun()

  # הצגת תצאות הבדיקה
  if st.session_state.checked_grid:
    if not user_answers:
      st.info("עֲדַיִן לֹא מִלֵּאת אף תְּשׁוּבָה בַּטַּבְלָה 🙂")
    else:
      correct_count = 0
      wrong_details = []

      for (i, j), ans in user_answers.items():
        real_ans = i * j
        if ans == real_ans:
          correct_count += 1
        else:
          wrong_details.append(
              f"תרגיל **{i} × {j}**: כתבת **{ans}**, התשובה הנכונה היא"
              f" **{real_ans}**"
          )

      if len(wrong_details) == 0:
        st.balloons()
        st.success(
            f"🎉 כָּל הַכָּבוֹד! כָּל {correct_count} הַתְּשׁוּבוֹת שֶׁמִּלֵּאת"
            " נְכוֹנוֹת בְּמַדְעָן!"
        )
      else:
        st.warning(
            f"עָנִית עַל {correct_count} תְּשׁוּבוֹת נְכוֹנוֹת מִתּוֹךְ"
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
      f'<h1 style="font-size: 3.5rem; color: #3498db;">{n1} × {n2} = ?</h1>'
      f"</div>",
      unsafe_allow_html=True,
  )

  user_quick_ans = st.text_input(
      "כִּתְבִי אֶת הַתְּשׁוּבָה שֶׁלָּךְ כאן:", key="quick_ans"
  )

  if st.button("בִּדְקִי תְּשׁוּבָה"):
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
            f"לֹא נוֹרָא! {n1} × {n2} זה **{n1*n2}**. נַסִּי אֶת הַתַּרְגִּיל"
            " הַבָּא!"
        )
        st.session_state.q_num1 = random.randint(2, 10)
        st.session_state.q_num2 = random.randint(2, 10)
    else:
      st.warning("אנָּא כִּתְבִי מִסְפָּר.")

  st.metric("נְקֻדּוֹת שֶׁצָּבַרְתְּ", st.session_state.score)

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

  if st.button("בְּדוֹק שְׁאָלָה מִלּוּלִית"):
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
      st.warning("אנָּא כִּתְבִי מִסְפָּר.")

  if st.button("הַשְּׁאָלָה הַבָּאָה ⬅️"):
    st.session_state.wp_idx = (st.session_state.wp_idx + 1) % len(
        WORD_PROBLEMS
    )
    st.rerun()

# ==========================================
# לשונית 4: משחק המבוך
# ==========================================
with tab4:
  st.subheader("🎮 מִשְׂחָק הַמַּבּוֹךְ – הַמַּסָּע לָאַרְמוֹן")
  st.write(
      "הַיֶּלֶד רוֹצֶה לְהַגִּיעַ לָאַרְמוֹן! עַזְרִי לוֹ לִפְתֹּחַ אֶת"
      " הַשְּׁעָרִים עַל יְדֵי פִּתְרוֹן תַּרְגִּילֵי כֶּפֶל."
  )

  if "maze_step" not in st.session_state:
    st.session_state.maze_step = 0

  steps = [
      {"gate": "🚪 שַׁעַר 1: יַעַר הַמִּסְפָּרִים", "n1": 3, "n2": 4},
      {"gate": "🚪 שַׁעַר 2: גֶּשֶׁר הַקְּסָמִים", "n1": 6, "n2": 7},
      {"gate": "🚪 שַׁעַר 3: מְעָרַת הַזָּהָב", "n1": 8, "n2": 9},
      {"gate": "🏰 שַׁעַר הָאַרְמוֹן הַנֶּאֱצָל", "n1": 7, "n2": 8},
  ]

  curr_step = st.session_state.maze_step

  if curr_step < len(steps):
    st.info(f"שלב {curr_step + 1} מתוך {len(steps)}: {steps[curr_step]['gate']}")

    # תצוגת המבוך וההתקדמות
    progress_icons = ""
    for idx in range(len(steps)):
      if idx < curr_step:
        progress_icons += " ✅ "
      elif idx == curr_step:
        progress_icons += " 👦 (כאן הילד) "
      else:
        progress_icons += " 🔒 "
    progress_icons += " 🏰"

    st.markdown(
        f'<div class="game-card" style="text-align:center; font-size:1.5rem;">'
        f"{progress_icons}"
        f"</div>",
        unsafe_allow_html=True,
    )

    n1 = steps[curr_step]["n1"]
    n2 = steps[curr_step]["n2"]

    st.write(
        f"כְּדֵי לפְתֹּחַ אֶת {steps[curr_step]['gate']}, פִּתְרִי אֶת"
        f" הַתַּרְגִּיל: **{n1} × {n2}**"
    )
    maze_ans = st.text_input("תְּשׁוּבָה לִפְתִיחַת הַשַּׁעַר:", key=f"maze_{curr_step}")

    if st.button("פְּתַח אֶת הַשַּׁעַר!"):
      if maze_ans.strip().isdigit() and int(maze_ans.strip()) == n1 * n2:
        st.balloons()
        st.success("🔓 הַשַּׁעַר נִפְתַּח! הַיֶּלֶד מַמְשִׁיךְ קָדִימָה!")
        st.session_state.maze_step += 1
        st.rerun()
      else:
        st.error("הַשַּׁעַר נִשְׁאַר נָעוּל... נַסִּי שוּב!")
  else:
    st.balloons()
    st.markdown(
        '<div class="game-card" style="text-align:center;">'
        "<h2>👑 כָּל הַכָּבוֹד! הִגַּעְתְּ לָאַרְמוֹן! 👑</h2>"
        "<p>פָּתַחְתְּ אֶת כָּל הַשְּׁעָרִים בְּהַצְלָחָה!</p>"
        "</div>",
        unsafe_allow_html=True,
    )
    if st.button("הַתְחֵל מִשְׂחָק חָדָשׁ 🔄"):
      st.session_state.maze_step = 0
      st.rerun()
