import pandas as pd
import streamlit as st

# הגדרת עיצוב הדף והתאמה למובייל
st.set_page_config(
    page_title="מחולל נגדים מקבילים שלמים", page_icon="⚡", layout="centered"
)

# הזרקת קוד HTML/JS תומך-Safari (תגיות מובייל ואייפון)
st.markdown(
    """
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <meta name="apple-mobile-web-app-title" content="נגדים מקבילים">
    <link rel="apple-touch-icon" href="https://cdn-icons-png.flaticon.com/512/2921/2921222.png">
    """,
    unsafe_allow_html=True,
)

st.title("⚡ מחולל נגדים מקבילים שלמים (2 עד 5 נגדים)")
st.markdown(
    "בחר את מספר הנגדים במעגל ואת ההתנגדות השקולה הרצויה ($R_{eq}$), "
    "והערכת תחשב עבורך קומבינציות נגדים בעלות ערכים שלמים בלבד!"
)

# תיבה ייעודית להסבר על שמירה במסך הבית באייפון (ספארי)
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
        
        זהו! האייקון יופיע על מסך הבית שלך כאפליקציה לכל דבר.
        """
  )

st.divider()

# בחירת פרמטרים על ידי המשתמש
col1, col2 = st.columns(2)

with col1:
  num_resistors = st.number_input(
      "כמות נגדים במעגל (2 עד 5):",
      min_value=2,
      max_value=5,
      value=3,
      step=1,
  )

with col2:
  r_eq = st.number_input(
      "התנגדות שקולה רצויה (Req באוהם):",
      min_value=1,
      max_value=10000,
      value=6,
      step=1,
  )

# מאגר דפוסים ליצירת נגדים שלמים (מקדמים המקיימים Sum(1/k_i) = 1)
PATTERNS = {
    2: [
        [2, 2],
        [3, 1.5],
        [4, 4 / 3],
    ],
    3: [
        [2, 3, 6],  # הדוגמה המפורסמת שלך!
        [3, 3, 3],
        [2, 4, 4],
        [4, 4, 2],
        [3, 6, 2],
    ],
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

# חישוב השילובים
results = []
patterns_for_n = PATTERNS.get(num_resistors, [])

for p_idx, pattern in enumerate(patterns_for_n, 1):
  resistors = [float(r_eq * k) for k in pattern]

  # בדיקה האם כל ערכי הנגדים המתקבלים הם מספרים שלמים
  if all(r.is_integer() for r in resistors):
    row = {"שילוב #": f"אופציה {p_idx}"}
    for i, r_val in enumerate(resistors, 1):
      row[f"נגד R{i} (Ω)"] = int(r_val)
    row["התנגדות שקולה (Req)"] = r_eq
    results.append(row)

# הצגת תוצאות
if results:
  st.success(
      f"מצאנו {len(results)} שילובים שונים של נגדים שלמים עבור מעגל של"
      f" {num_resistors} נגדים במקביל!"
  )
  df = pd.DataFrame(results)
  st.dataframe(df, use_container_width=True)
else:
  st.warning(
      f"עבור ערך Req = {r_eq}Ω לא נמצאו שילובים של נגדים שלמים בדפוסים הקימיים. נסה לבחור ערך Req זוגי או כפולה של 6/12."
  )