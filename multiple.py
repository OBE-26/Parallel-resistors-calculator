import random
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

# הגדרות דף רספונסיביות
st.set_page_config(page_title="לומדים את לוח הכפל!", page_icon="✏️", layout="wide")

# CSS מתקדם לתאימות למובייל ומראה משחקי
st.markdown(
    """
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Rubik:wght@400;600;700&display=swap');
    
    html, body, [class*="css"]  {
        font-family: 'Rubik', -apple-system, sans-serif;
        direction: rtl; text-align: right; user-select: none;
    }
    
    .stApp { background-color: #f4f7f6; }
    
    .main-title { font-size: 2.2rem; color: #2c3e50; text-align: center; font-weight: 700; }
    .subtitle { font-size: 1.1rem; color: #576574; text-align: center; margin-bottom: 1rem; }

    /* עיצוב המבוך 3D Top-Down */
    .forest-container {
        background: linear-gradient(135deg, #78e08f, #38ada9);
        padding: 20px; border-radius: 20px;
        box-shadow: 0 10px 20px rgba(0,0,0,0.2);
        text-align: center; margin-bottom: 20px; border: 4px solid #079992;
    }
    .forest-row { display: flex; justify-content: center; gap: 10px; margin-bottom: 5px; }
    .forest-cell {
        width: 55px; height: 55px; font-size: 35px;
        display: flex; align-items: center; justify-content: center;
        background: rgba(255,255,255,0.1); border-radius: 12px;
        box-shadow: inset 0 -3px 0 rgba(0,0,0,0.1);
    }
    .path-cell { background: #eccc68; box-shadow: 0 4px 0 #d1ccc0; }
    .player-cell {
        background: #ff7f50; transform: scale(1.1);
        box-shadow: 0 5px 10px rgba(0,0,0,0.3); z-index: 10;
        animation: bounce 1s infinite;
    }
    @keyframes bounce {
        0%, 100% { transform: translateY(0) scale(1.1); }
        50% { transform: translateY(-5px) scale(1.1); }
    }
    .stButton>button { width: 100%; border-radius: 12px; font-size: 1.1rem; font-weight: 600; background-color: #2e86de; color: white; padding: 10px; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">✨ לוּחַ הַכֶּפֶל הַקָּסוּם ✨</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">לומְדִים, מְתַרְגְּלִים וּמְשַׂחֲקִים בְּכֵף!</div>', unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["📊 לוּחַ כֶּפֶל", "⚡ תִּרְגּוּל מְהִיר", "📖 שְׁאֵלוֹת", "🌲 מִשְׂחָק הַיַּעַר"])

# ==========================================
# לשונית 1: לוח 10x10 אמיתי (בסגנון אקסל עם צביעה ירוק/אדום)
# ==========================================
with tab1:
  st.subheader("📊 עֲרִיכַת לוּחַ הַכֶּפֶל (כְּמוֹ אֶקְסֶל)")
  st.write("מַלֵּא/י אֶת הַתָּאִים, וְלַחַץ/י 'בְּדוֹק תְּשׁוּבוֹת'. תְּשׁוּבוֹת נְכוֹנוֹת יִצָּבְעוּ בְּיָרֹק, וּשְׁגוּיוֹת בְּאָדֹם!")

  if "table_data" not in st.session_state:
      st.session_state.table_data = pd.DataFrame("", index=[str(i) for i in range(1, 11)], columns=[str(i) for i in range(1, 11)])
      st.session_state.editor_key = 0
      st.session_state.check_table = False

  # פונקציית צביעת תאים
  def get_table_styles(df):
      styles = pd.DataFrame('', index=df.index, columns=df.columns)
      if not st.session_state.check_table:
          return styles
      for r in df.index:
          for c in df.columns:
              v = df.at[r, c]
              if v != "":
                  try:
                      if int(v) == int(r) * int(c):
                          styles.at[r, c] = 'background-color: #c8e6c9; color: #1b5e20; font-weight: bold;'
                      else:
                          styles.at[r, c] = 'background-color: #ffcdd2; color: #b71c1c; font-weight: bold;'
                  except:
                      styles.at[r, c] = 'background-color: #ffcdd2; color: #b71c1c; font-weight: bold;'
      return styles

  edited_df = st.data_editor(
      st.session_state.table_data.style.apply(get_table_styles, axis=None),
      key=f"editor_{st.session_state.editor_key}",
      use_container_width=True,
      height=400
  )

  c1, c2, c3 = st.columns(3)
  
  with c1:
      if st.button("🔍 בְּדוֹק/י תְּשׁוּבוֹת"):
          st.session_state.table_data = edited_df.copy()
          st.session_state.check_table = True
          
          correct = 0
          filled = 0
          for r in edited_df.index:
              for c in edited_df.columns:
                  v = edited_df.at[r, c]
                  if v != "":
                      filled += 1
                      try:
                          if int(v) == int(r)*int(c): correct += 1
                      except: pass
          
          if filled > 0 and correct == filled:
              st.balloons()
              st.success("🎉 מֻשְׁלָם! כָּל מַה שֶׁמִּלֵּאתָ/תּ נָכוֹן בְּמַדְעָן! תְּשׁוּבוֹתֶיךָ יְרֻקּוֹת!")
          elif filled > 0:
              st.warning(f"עָנִיתָ/תּ נָכוֹן עַל {correct} מִתּוֹךְ {filled}. סִמַּנְתִּי אֶת הַטָּעֻיּוֹת בְּאָדֹם.")
          else:
              st.info("עֲדַיִן לֹא מִלֵּאתָ/תּ אף תְּשׁוּבָה בַּטַּבְלָה 🙂")
          st.rerun()

  with c2:
      if st.button("🧹 נַקֵּה/י טָעֻיּוֹת (נִסָּיוֹן נוֹסָף)"):
          new_df = edited_df.copy()
          for r in new_df.index:
              for c in new_df.columns:
                  v = new_df.at[r, c]
                  if v != "":
                      try:
                          if int(v) != int(r)*int(c):
                              new_df.at[r, c] = "" # מנקה רק טעויות
                      except:
                          new_df.at[r, c] = ""
          st.session_state.table_data = new_df
          st.session_state.check_table = False
          st.session_state.editor_key += 1
          st.rerun()

  with c3:
      if st.button("🔄 נַקֵּה/י אֶת כָּל הַטַּבְלָה"):
          st.session_state.table_data = pd.DataFrame("", index=[str(i) for i in range(1, 11)], columns=[str(i) for i in range(1, 11)])
          st.session_state.check_table = False
          st.session_state.editor_key += 1
          st.rerun()

# ==========================================
# לשונית 2: תרגול מהיר
# ==========================================
with tab2:
  if "q_num1" not in st.session_state:
    st.session_state.q_num1, st.session_state.q_num2 = random.randint(2, 10), random.randint(2, 10)
    st.session_state.score = 0

  n1, n2 = st.session_state.q_num1, st.session_state.q_num2
  st.markdown(f'<div style="background:white; padding: 20px; border-radius:15px; text-align:center;"><h2>כַּמָּה זֶה?</h2><h1 style="font-size:3.5rem; color:#10ac84;">{n1} × {n2} = ?</h1></div><br>', unsafe_allow_html=True)
  
  user_quick_ans = st.text_input("כְּתֹב/י תְּשׁוּבָה כאן:", key="quick_ans")

  if st.button("בְּדוֹק/י תְּשׁוּבָה מְהִירָה"):
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
  WORDS = [
      {"q": "לְשָׁקֵד יֵשׁ 4 חֲבִילוֹת צְבָעִים. בְּכָל חֲבִילָה יֵשׁ 6 צְבָעִים. כַּמָּה צְבָעִים יֵשׁ בְּסַךְ הַכֹּל?", "ans": 24},
      {"q": "אִמָּא קָנְתָה 7 שַׂקִּיּוֹת תַּפּוּחִים. בְּכָל שַׂקִּית יֵשׁ 3 תַּפּוּחִים. כַּמָּה תַּפּוּחִים קָנְתָה אִמָּא?", "ans": 21},
  ]
  if "wp_idx" not in st.session_state: st.session_state.wp_idx = 0
  cp = WORDS[st.session_state.wp_idx]

  st.markdown(f'<div style="background:white; padding: 20px; border-radius:15px;"><h3>שאלה מס׳ {st.session_state.wp_idx + 1}:</h3><p style="font-size:1.2rem;">{cp["q"]}</p></div><br>', unsafe_allow_html=True)
  
  wp_ans = st.text_input("תְּשׁוּבָה מילולית:", key=f"wp_{st.session_state.wp_idx}")
  if st.button("בְּדוֹק/י אֶת הַשְּׁאֵלָה"):
    if wp_ans.strip().isdigit() and int(wp_ans.strip()) == cp["ans"]:
      st.balloons(); st.success("🎉 צָדַקְתָּ/תּ!")
    else:
      st.error(f"הַתְּשׁוּבָה הִיא {cp['ans']}.")
  if st.button("שְׁאֵלָה הַבָּאָה ⬅️"):
    st.session_state.wp_idx = (st.session_state.wp_idx + 1) % len(WORDS)
    st.rerun()

# ==========================================
# לשונית 4: משחק בחירה ביער (תלת ממד עם זיהוי החלקות Swipe)
# ==========================================
with tab4:
  st.subheader("🌲 מִשְׂחָק הַיַּעַר הַתְּלַת-מֵמַדִּי")
  st.write("מָה הַתְּשׁוּבָה לַתַּרְגִּיל? **הַחְלֵק/י יָמִינָה אוֹ שְׂמֹאלָה** עַל הַמָּסָךְ כְּדֵי שֶׁהַיֶּלֶד יִבְחַר כִּוּוּן!")

  # הזרקת קוד Javascript מאחורי הקלעים לזיהוי החלקות ומשיכות עכבר
  components.html("""
  <script>
  const doc = window.parent.document;
  let startX = 0; let isDragging = false;
  
  function triggerSwipe(direction) {
      const btns = doc.querySelectorAll('button');
      btns.forEach(b => {
          if (direction === 'left' && b.innerText.includes('הַחְלֵק שְׂמֹאלָה')) b.click();
          if (direction === 'right' && b.innerText.includes('הַחְלֵק יָמִינָה')) b.click();
      });
  }

  // תמיכה בהחלקת אצבע (טלפון/אייפד)
  doc.addEventListener('touchstart', e => { startX = e.changedTouches[0].screenX; }, {passive: true});
  doc.addEventListener('touchend', e => {
      let endX = e.changedTouches[0].screenX;
      if (startX - endX > 60) triggerSwipe('left');
      if (endX - startX > 60) triggerSwipe('right');
  }, {passive: true});

  // תמיכה במשיכת עכבר (מחשב)
  doc.addEventListener('mousedown', e => { startX = e.screenX; isDragging = true; });
  doc.addEventListener('mouseup', e => {
      if(!isDragging) return;
      let endX = e.screenX; isDragging = false;
      if (startX - endX > 60) triggerSwipe('left');
      if (endX - startX > 60) triggerSwipe('right');
  });
  </script>
  """, height=0, width=0)

  if "forest_step" not in st.session_state:
      st.session_state.forest_step = 1
      st.session_state.fq1, st.session_state.fq2 = random.randint(4, 9), random.randint(4, 9)

  step = st.session_state.forest_step

  if step <= 5:
      forest_html = f"""
      <div class="forest-container">
          <h4 style="color:white; margin-bottom:15px;">שָׁלָב {step} מִתּוֹךְ 5 - נְקֻדַּת פִּצּוּל</h4>
          <div class="forest-row"><div class="forest-cell">🌲</div><div class="forest-cell">🏰</div><div class="forest-cell">🌲</div></div>
          <div class="forest-row"><div class="forest-cell">🌲</div><div class="forest-cell path-cell">🟫</div><div class="forest-cell">🌲</div></div>
          <div class="forest-row"><div class="forest-cell path-cell">🟫</div><div class="forest-cell path-cell">🟫</div><div class="forest-cell path-cell">🟫</div></div>
          <div class="forest-row"><div class="forest-cell">🌲</div><div class="forest-cell player-cell">👦</div><div class="forest-cell">🌲</div></div>
      </div>
      """
      st.markdown(forest_html, unsafe_allow_html=True)

      n1, n2 = st.session_state.fq1, st.session_state.fq2
      correct_ans = n1 * n2
      wrong_ans = correct_ans + random.choice([-1, 1, 2, -2, n1, -n1])
      
      if "ans_left" not in st.session_state or st.session_state.get("last_step") != step:
          options = [correct_ans, wrong_ans]
          random.shuffle(options)
          st.session_state.ans_left = options[0]
          st.session_state.ans_right = options[1]
          st.session_state.last_step = step

      st.markdown(f"<h3 style='text-align:center;'>לְאַן פּוֹנִים? <span style='color:#e67e22;'>{n1} × {n2} = ?</span></h3>", unsafe_allow_html=True)

      col_right, col_left = st.columns(2)
      
      with col_right:
          # צד ימין (פיזית על המסך בעברית, לכן שמאלה)
          if st.button(f"⬅️ לַשְּׁבִיל הַשְּׂמָאלִי ({st.session_state.ans_left}) - הַחְלֵק שְׂמֹאלָה"):
              if st.session_state.ans_left == correct_ans:
                  st.success("נָכוֹן! הַיֶּלֶד מִתְקַדֵּם בַּיַּעַר 🏃")
                  st.session_state.forest_step += 1
                  st.session_state.fq1, st.session_state.fq2 = random.randint(4, 9), random.randint(4, 9)
                  st.rerun()
              else:
                  st.error("אוֹי! נִתְקַעְנוּ בְּעֵץ 🌲. זֶה הָיָה הַכִּוּוּן הַשֵּׁנִי.")

      with col_left:
          # צד שמאל
          if st.button(f"לַשְּׁבִיל הַיְּמָנִי ({st.session_state.ans_right}) ➡️ - הַחְלֵק יָמִינָה"):
              if st.session_state.ans_right == correct_ans:
                  st.success("נָכוֹן! הַיֶּלֶד מִתְקַדֵּם בַּיַּעַר 🏃")
                  st.session_state.forest_step += 1
                  st.session_state.fq1, st.session_state.fq2 = random.randint(4, 9), random.randint(4, 9)
                  st.rerun()
              else:
                  st.error("אוֹי! נִתְקַעְנוּ בְּעֵץ 🌲. זֶה הָיָה הַכִּוּוּן הַשֵּׁנִי.")

  else:
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
