import math
import pandas as pd
import streamlit as st

# הגדרת עיצוב הדף והתאמה למובייל
st.set_page_config(
    page_title="מחולל נגדים וזרמים שלמים",
    page_icon="https://cdn-icons-png.flaticon.com/512/3463/3463930.png",
    layout="centered",
)

# הזרקת קוד HTML/JS תומך-Safari עם האייקון החדש שבחרת
st.markdown(
    """
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <meta name="apple-mobile-web-app-title" content="נגדים וזרמים">
    <link rel="apple-touch-icon" href="https://cdn-icons-png.flaticon.com/512/3463/3463930.png">
    """,
    unsafe_allow_html=True,
)
st.title("⚡ מחולל נגדים, מתחים וזרמים שלמים ")
st.markdown(
    "הזן את ההתנגדות השקולה ($R_t$), מספר הנגדים ומכפיל המתח לקבלת זרמים"
    " גדולים ושלמים יותר בכל ענף."
)

with st.expander(
    "📱 טיפ: איך להוסיף את האפליקציה למסך הבית באייפון (Safari)",
    expanded=False,
):
  st.markdown(
      """
        1. פתח את הקישור הזה בדפדפן **Safari** באייפון שלך.
        2. לחץ על כפתור ה**שיתוף (Share - המלבן עם החץ כלפי מעלה)** בתחתית המסך.
        3. גלול למטה בתפריט שנפתח ובחר **"הוסף למסך הבית" (Add to Home Screen)**.
        4. לחץ על **הוסף (Add)** בפינה הימנית/שמאלית העליונה.
        """
  )

st.divider()

col1, col2, col3 = st.columns(3)

with col1:
  num_resistors = st.number_input(
      "כמות נגדים (2-5):", min_value=2, max_value=5, value=3, step=1
  )

with col2:
  r_eq = st.number_input(
      "התנגדות שקולה Rt (Ω):", min_value=1, max_value=10000, value=6, step=1
  )

with col3:
  voltage_multiplier = st.selectbox(
      "מכפיל מתח (שליטה בזרמים):", [1, 2, 3, 4, 5, 6], index=0
  )

# מאגר דפוסים ליצירת נגדים שלמים
PATTERNS = {
    2: [[2, 2], [3, 1.5], [4, 4 / 3]],
    3: [[2, 3, 6], [3, 3, 3], [2, 4, 4], [4, 4, 2], [3, 6, 2]],
    4: [
        [4, 4, 4, 4],
        [2, 4, 8, 8],
        [3, 3, 6, 6],
        [2, 6, 6, 6],
        [2, 4, 6, 12],
    ],
    5: [
        [5, 5, 5, 5, 5],
        [2, 6, 12, 20, 30],
        [3, 4, 6, 12, 12],
        [2, 4, 8, 16, 16],
        [4, 4, 4, 8, 8],
    ],
}


def calc_lcm_list(numbers):
  lcm_val = numbers[0]
  for n in numbers[1:]:
    lcm_val = (lcm_val * n) // math.gcd(lcm_val, n)
  return lcm_val


resistor_results = []
current_results = []
patterns_for_n = PATTERNS.get(num_resistors, [])

for p_idx, pattern in enumerate(patterns_for_n, 1):
  resistors = [float(r_eq * k) for k in pattern]

  if all(r.is_integer() for r in resistors):
    r_ints = [int(r) for r in resistors]

    # חישוב מתח בסיס מינימלי ואז כפל במכפיל שבחר המשתמש
    lcm_val = calc_lcm_list(r_ints)
    base_voltage = (
        lcm_val / 2.0 if (lcm_val / 2.0).is_integer() else float(lcm_val)
    )
    v_total = base_voltage * voltage_multiplier

    v_formatted = int(v_total) if v_total.is_integer() else round(v_total, 1)

    # 1. טבלת נגדים ומתח
    res_row = {
        "אופציה": f"#{p_idx}",
        "Vt (V)": str(v_formatted),
        "Rt (Ω)": str(r_eq),
    }
    for i, r_val in enumerate(r_ints, 1):
      res_row[f"R{i} (Ω)"] = str(r_val)
    resistor_results.append(res_row)

    # 2. טבלת זרמים
    cur_row = {"אופציה": f"#{p_idx}"}
    temp_currents = {}
    total_current = 0
    for i, r_val in enumerate(r_ints, 1):
      i_val = v_total / r_val
      i_formatted = (
          int(i_val) if i_val.is_integer() else round(i_val, 1)
      )
      temp_currents[f"I{i} (A)"] = str(i_formatted)
      total_current += i_val

    it_formatted = (
        int(total_current)
        if total_current.is_integer()
        else round(total_current, 1)
    )
    cur_row["Itotal (A)"] = str(it_formatted)
    cur_row.update(temp_currents)
    current_results.append(cur_row)

# הצגת התוצאות
if resistor_results:
  st.success(f"מצאנו {len(resistor_results)} שילובים תואמים!")

  st.subheader("📐 טבלת התנגדויות ומתח")
  df_resistors = pd.DataFrame(resistor_results).astype(str)
  st.dataframe(df_resistors, use_container_width=True, hide_index=True)

  st.subheader("⚡ טבלת זרמים במעגל")
  df_currents = pd.DataFrame(current_results).astype(str)
  st.dataframe(df_currents, use_container_width=True, hide_index=True)
else:
  st.warning(
      f"עבור ערך Rt = {r_eq}Ω לא נמצאו שילובים של נגדים שלמים. נסה לבחור ערך Rt זוגי או כפולה של 6/12."
  )
