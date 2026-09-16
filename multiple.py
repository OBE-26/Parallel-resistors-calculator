import random
import pandas as pd
import streamlit as st

# הגדרות דף רספונסיביות
st.set_page_config(
    page_title="לומדים את לוח הכפל!", page_icon="✏️", layout="wide"
)

# CSS מותאם למראה משחקי ואקסל
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
    }
    
    .stApp { background-color: #f4f7f6; }
    
    .main-title {
        font-size: 2.2rem; color: #2c3e50; text-align: center; font-weight: 700;
    }
    .subtitle {
        font-size: 1.1rem; color: #576574; text-align: center; margin-bottom: 1rem;
    }

    /* עיצוב משחק המבוך (סגנון תלת ממד איזומטרי / משחק טלפון) */
    .forest-container {
        background: linear-gradient(135deg, #78e08f, #38ada9);
        padding: 20px;
        border-radius: 20px;
        box-shadow: 0 10px 20px rgba(0,0,0,0.2);
        text-align: center;
        margin-bottom: 20px;
        border: 4px solid #079992;
    }

    .forest-row {
        display: flex;
        justify-content: center;
        gap: 10px;
        margin-bottom: 5px;
    }

    .forest-cell {
        width: 50px;
        height: 50px;
        font-size: 30px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: rgba(255,255,255,0.1);
        border-radius: 10px;
        box-shadow: inset 0 -3px 0 rgba(0,0,0,0.1);
    }
    
    .path-cell {
        background: #eccc68;
        box-shadow: 0 4px 0 #d1ccc0;
    }

    .player-cell {
        background: #ff7f50;
        transform: scale(1.1);
        box-shadow: 0 5px 10px rgba(0,0,0,0.3);
        z-index: 10;
        animation: bounce 1s infinite;
    }

    @keyframes bounce {
        0%, 100% { transform: translateY(0) scale(1.1); }
        50% { transform: translateY(-5px) scale(1.1); }
    }

    .stButton>button {
        width: 100%; border-radius: 12px; font-size: 1.1rem; font-weight: 600;
        background-color: #2e86de; color: white; border: none; padding: 10px;
    }
    </style>
""",
    unsafe_allow_html=True,
)

st.markdown('<div class="main-title">✨ לוּחַ הַכֶּפֶל הַקָּסוּם ✨</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">לומְדִים, מְתַרְגְּלִים וּמְשַׂחֲקִים בְּכֵף!</div>', unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs([
    "📊 לוח אקסל (10x10)", "⚡ תִּרְגּוּל מְהִיר", "📖 שְׁאֵלוֹת", "🌲 מִשְׂחָק הַיַּעַר"
])

# ==========================================
# לשונית 1: לוח 10x10 אמיתי (כמו אקסל - Data Editor)
# ==========================================
with tab1:
  st.subheader("📊 עֲרִיכַת לוּחַ הַכֶּפֶל (כְּמוֹ אֶקְסֶל)")
  st.write("מַלֵּא/י אֶת הַתָּאִים הָאֲפוֹרִים שֶׁבַּטַּבְלָה מַמָּשׁ כְּמוֹ קוֹבֶץ אֶקְסֶל, וְלַחַץ/י 'בְּדוֹק תְּשׁוּבוֹת'.")

  # אתחול טבלת הפנדס רק בפעם הראשונה
  if "excel_board" not in st.session_state:
      # יוצרים טבלה של 10 על 10, עמודות ושורות 1 עד 10, עם ערך ריק
      df = pd.DataFrame(index=[str(i) for i in range(1, 11)], columns=[str(i) for i in range(1, 11)])
      df.fillna("", inplace=True)
      st.session_state.excel_board = df

  # הצגת הטבלה לעריכה (משתמשים ב-data_editor)
  edited_df = st.data_editor(
      st.session_state.excel_board,
      use_container_width=True,
      height=400
  )

  c_btn1, c_btn2 = st.columns(2)
  with c_btn1:
      check_btn = st.button("🔍 בְּדוֹק/י תְּשׁוּבוֹת")
  with c_btn2:
      if st.button("🔄 נַקֵּה/י טַבְלָה"):
          del st.session_state.excel_board
          st.rerun()

  if check_btn:
      correct_answers = 0
      wrong_answers = []
      total_filled = 0

      # מעבר על כל התאים בטבלה ששקד מילאה
      for row in range(1, 11):
          for col in range(1, 11):
              val = edited_df.at[str(row), str(col)]
              if val != "":
                  total_filled += 1
                  try:
                      user_val = int(val)
                      if user_val == row * col:
                          correct_answers += 1
                      else:
                          wrong_answers.append(f"תרגיל **{row} × {col}**: כָּתַבְתָּ/תּ **{user_val}**, התשובה היא **{row*col}**.")
                  except ValueError:
                      wrong_answers.append(f"תרגיל **{row} × {col}**: הקלדת ערך לא חוקי ('{val}').")
      
      if total_filled == 0:
          st.info("עֲדַיִן לֹא מִלֵּאתָ/תּ אף תְּשׁוּבָה 🙂")
      elif correct_answers == total_filled:
          st.balloons()
          st.success(f"🎉 מֻשְׁלָם! כָּל הַ-{total_filled} תְּשׁוּבוֹת שֶׁמִּלֵּאת נְכוֹנוֹת בְּמַדְעָן!")
      else:
          st.warning(f"עָנִיתָ/תּ נָכוֹן עַל {correct_answers} מִתּוֹךְ {total_filled} שֶׁמִּלֵּאת.")
          for w in wrong_answers:
              st.write(f"• {w}")

# ==========================================
# לשונית 2: תרגול מהיר
# ==========================================
with tab2:
  st.subheader("⚡ תִּרְגּוּל מְהִיר")
  if "q_num1" not in st.session_state:
    st.session_state.q_num1, st.session_state.q_num2 = random.randint(2, 10), random.randint(2, 10)
    st.session_state.score = 0

  n1, n2 = st.session_state.q_num1, st.session_state.q_num2
  st.markdown(f'<div style="background:white; padding: 20px; border-radius:15px; text-align:center;"><h2>כַּמָּה זֶה?</h2><h1 style="font-size:3.5rem; color:#10ac84;">{n1} × {n2} = ?</h1></div><br>', unsafe_allow_html=True)
  
  user_quick_ans = st.text_input("כְּתֹב/י תְּשׁוּבָה:", key="quick_ans")

  if st.button("בְּדוֹק/י תְּשׁוּבָה"):
    if user_quick_ans.strip().isdigit() and int(user_quick_ans.strip()) == n1 * n2:
      st.balloons(); st.success("🎉 נָכוֹן מְאֹד!")
      st.session_state.score += 1
    else:
      st.error(f"לֹא נוֹרָא! {n1} × {n2} = **{n1*n2}**.")
    st.session_state.q_num1, st.session_state.q_num2 = random.randint(2, 10), random.randint(2, 10)
  st.metric("נְקֻדּוֹת שֶׁצָּבַרְתָּ/תּ", st.session_state.score)

# ==========================================
# לשונית 3: שאלות מילוליות
# ==========================================
with tab3:
  st.subheader("📖 שְׁאֵלוֹת מִלּוּלִיּוֹת")
  WORDS = [
      {"q": "לְשָׁקֵד יֵשׁ 4 חֲבִילוֹת צְבָעִים. בְּכָל חֲבִילָה יֵשׁ 6 צְבָעִים. כַּמָּה צְבָעִים יֵשׁ בְּסַךְ הַכֹּל?", "ans": 24},
      {"q": "אִמָּא קָנְתָה 7 שַׂקִּיּוֹת תַּפּוּחִים. בְּכָל שַׂקִּית יֵשׁ 3 תַּפּוּחִים. כַּמָּה תַּפּוּחִים קָנְתָה אִמָּא?", "ans": 21},
  ]
  if "wp_idx" not in st.session_state: st.session_state.wp_idx = 0
  cp = WORDS[st.session_state.wp_idx]

  st.markdown(f'<div style="background:white; padding: 20px; border-radius:15px;"><h3>שאלה מס׳ {st.session_state.wp_idx + 1}:</h3><p style="font-size:1.2rem;">{cp["q"]}</p></div><br>', unsafe_allow_html=True)
  
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
# לשונית 4: משחק בחירה ביער (מראה טלפון תלת-ממד מדמה)
# ==========================================
with tab4:
  st.subheader("🌲 מִשְׂחָק הַיַּעַר – יָמִינָה אוֹ שְׂמֹאלָה?")
  st.write("הַיֶּלֶד בַּיַּעַר וְצָרִיךְ לִבְחֹר אֶת הַדֶּרֶךְ לָאַרְמוֹן! לְאַן מַמְשִׁיכִים? (בְּחַר/י בַּתְּשׁוּבָה הַנְּכוֹנָה)")

  if "forest_step" not in st.session_state:
      st.session_state.forest_step = 1
      st.session_state.fq1, st.session_state.fq2 = random.randint(4, 9), random.randint(4, 9)

  step = st.session_state.forest_step

  if step <= 5:
      # בניית תצוגת היער הקסום - סימולציה ויזואלית של מבוך יער
      forest_html = f"""
      <div class="forest-container">
          <h4 style="color:white; margin-bottom:15px;">שָׁלָב {step} מִתּוֹךְ 5</h4>
          <div class="forest-row">
              <div class="forest-cell">🌲</div>
              <div class="forest-cell">🏰</div>
              <div class="forest-cell">🌲</div>
          </div>
          <div class="forest-row">
              <div class="forest-cell">🌲</div>
              <div class="forest-cell path-cell">🟫</div>
              <div class="forest-cell">🌲</div>
          </div>
          <div class="forest-row">
              <div class="forest-cell path-cell">🟫</div>
              <div class="forest-cell path-cell">🟫</div>
              <div class="forest-cell path-cell">🟫</div>
          </div>
          <div class="forest-row">
              <div class="forest-cell">🌲</div>
              <div class="forest-cell player-cell">👦</div>
              <div class="forest-cell">🌲</div>
          </div>
      </div>
      """
      st.markdown(forest_html, unsafe_allow_html=True)

      n1, n2 = st.session_state.fq1, st.session_state.fq2
      correct_ans = n1 * n2
      wrong_ans = correct_ans + random.choice([-1, 1, 2, -2, n1, -n1])
      
      # מערבבים את התשובות (שמאל או ימין)
      if "ans_left" not in st.session_state or st.session_state.get("last_step") != step:
          options = [correct_ans, wrong_ans]
          random.shuffle(options)
          st.session_state.ans_left = options[0]
          st.session_state.ans_right = options[1]
          st.session_state.last_step = step

      st.markdown(f"<h3 style='text-align:center;'>כְּדֵי לְהַמְשִׁיךְ, עֲנֵה/י: <span style='color:#e67e22;'>{n1} × {n2} = ?</span></h3>", unsafe_allow_html=True)
      st.write("")

      col_left, col_right = st.columns(2)
      
      with col_right: # ימינה
          if st.button(f"⬅️ שְׂמֹאלָה ({st.session_state.ans_left})"): # בגלל RTL ימין ושמאל הפוכים ויזואלית בכפתורים
              if st.session_state.ans_left == correct_ans:
                  st.success("נָכוֹן! הַיֶּלֶד מִתְקַדֵּם 🏃")
                  st.session_state.forest_step += 1
                  st.session_state.fq1, st.session_state.fq2 = random.randint(4, 9), random.randint(4, 9)
                  st.rerun()
              else:
                  st.error("אוֹי! נִתְקַעְנוּ בְּעֵץ 🌲. נַסֵּה/י אֶת הַכִּוּוּן הַשֵּׁנִי.")

      with col_left: # שמאלה
          if st.button(f"יָמִינָה ({st.session_state.ans_right}) ➡️"):
              if st.session_state.ans_right == correct_ans:
                  st.success("נָכוֹן! הַיֶּלֶד מִתְקַדֵּם 🏃")
                  st.session_state.forest_step += 1
                  st.session_state.fq1, st.session_state.fq2 = random.randint(4, 9), random.randint(4, 9)
                  st.rerun()
              else:
                  st.error("אוֹי! נִתְקַעְנוּ בְּעֵץ 🌲. נַסֵּה/י אֶת הַכִּוּוּן הַשֵּׁנִי.")

  else:
      # מסך ניצחון והגעה לארמון
      st.balloons()
      st.markdown("""
      <div class="forest-container" style="background: linear-gradient(135deg, #f1c40f, #f39c12);">
          <div style="font-size: 80px;">🏰</div>
          <h2 style="color:white;">כָּל הַכָּבוֹד! הִגַּעְתָּ/תּ לָאַרְמוֹן!</h2>
      </div>
      """, unsafe_allow_html=True)
      
      if st.button("שַׂחֵק/י מֵחָדָשׁ 🔄"):
          st.session_state.forest_step = 1
          st.rerun()
