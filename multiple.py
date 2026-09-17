"""Shaked's Hebrew multiplication playground.

Run: streamlit run multiple.py
Only Streamlit is required. The complete responsive UI is embedded below.
Progress is stored in this browser's local storage (not shared across devices).
"""
from pathlib import Path
import tempfile
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="לוּחַ הַכֶּפֶל שֶׁל שָׁקֵד בֶּן עֶזְרָא", page_icon="🌱", layout="wide")
st.markdown("""<style>
.stApp { background: #f7f5ee; }
[data-testid="stAppViewContainer"] { background: #f7f5ee; }
[data-testid="stMainBlockContainer"], .block-container {
    max-width: 1100px; padding: 0.5rem 0.25rem 1rem;
}
[data-testid="stHeader"] { display: none; }
@media (max-width: 600px) {
    [data-testid="stMainBlockContainer"], .block-container {
        padding: 0.25rem 0 0.5rem;
    }
}
</style>""", unsafe_allow_html=True)

APP_HTML = r'''<!doctype html>
<html lang="he" dir="rtl">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover" />
    <meta name="theme-color" content="#f7f5ee" />
    <title>לוּחַ הַכֶּפֶל שֶׁל שָׁקֵד בֶּן עֶזְרָא</title>
    <style>
      :root {
        color-scheme: light;
        --ink: #243c3a;
        --muted: #627571;
        --paper: #f7f5ee;
        --white: #fffefa;
        --green: #187568;
        --line: #dce4dd;
        --violet: #7860aa;
        --good: #d0f0df;
        --bad: #ffdadd;
        --shadow: 0 8px 28px #243c3a09;
      }
      * {
        box-sizing: border-box;
      }
      html,
      body {
        margin: 0;
        padding: 0;
        background: var(--paper);
        color: var(--ink);
        font-family: Arial, "Noto Sans Hebrew", sans-serif;
        direction: rtl;
        text-align: right;
      }
      body {
        overflow-x: hidden;
      }
      button,
      input {
        font: inherit;
      }
      button {
        cursor: pointer;
        touch-action: manipulation;
      }
      button:disabled {
        cursor: default;
        opacity: 0.48;
      }
      button,
      input,
      a {
        -webkit-tap-highlight-color: transparent;
      }
      button:focus-visible,
      input:focus-visible,
      a:focus-visible {
        outline: 3px solid #e59f32;
        outline-offset: 3px;
      }
      button {
        border: 0;
      }
      h1,
      h2,
      h3,
      p {
        margin-top: 0;
      }
      h1,
      h2,
      h3 {
        line-height: 1.5;
        letter-spacing: -0.025em;
      }
      p {
        line-height: 1.8;
      }
      h2 {
        font-size: clamp(22px, 4vw, 30px);
        margin-bottom: 6px;
      }
      h3 {
        font-size: 20px;
      }
      bdi,
      .num,
      .math,
      input.numeric {
        direction: ltr;
        unicode-bidi: isolate;
        text-align: left;
        font-variant-numeric: tabular-nums;
      }
      bdi {
        display: inline-block;
      }
      .math {
        display: block;
        font-size: clamp(30px, 6vw, 48px);
        font-weight: 700;
        letter-spacing: 0.025em;
        line-height: 1.5;
      }
      .num {
        display: inline-block;
      }
      input.numeric {
        text-align: left !important;
      }
      input::-webkit-outer-spin-button,
      input::-webkit-inner-spin-button {
        -webkit-appearance: none;
        margin: 0;
      }
      input {
        font-size: 18px;
      }
      input.numeric {
        border: 2px solid var(--line);
        border-radius: 12px;
        background: white;
        padding: 12px;
        width: 100%;
        min-height: 50px;
        color: var(--ink);
      }
      input.numeric:focus {
        border-color: var(--green);
      }
      [hidden] {
        display: none !important;
      }
      .app {
        max-width: 1040px;
        margin: 0 auto;
        padding: 20px 24px 32px;
      }
      .brand-row {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 16px;
      }
      .brand-mark {
        width: 44px;
        height: 44px;
        border-radius: 15px;
        background: var(--green);
        color: white;
        display: grid;
        place-items: center;
        font-size: 30px;
        flex-shrink: 0;
      }
      .brand-name {
        font-size: 18px;
        font-weight: 700;
        line-height: 1.6;
      }
      .brand-note {
        font-size: 13px;
        color: var(--muted);
      }
      .tag {
        color: var(--green);
        font-size: 13px;
        font-weight: 700;
        letter-spacing: 0.04em;
      }
      .nav {
        display: flex;
        flex-wrap: wrap;
        gap: 6px;
        padding: 8px 0 16px;
        border-bottom: 1px solid var(--line);
        margin-bottom: 24px;
      }
      .nav button {
        background: transparent;
        color: var(--muted);
        padding: 10px 14px;
        border-radius: 24px;
        font-size: 15px;
        font-weight: 700;
        min-height: 42px;
        white-space: nowrap;
      }
      .nav button.active {
        background: var(--ink);
        color: #fff;
      }
      .nav button:hover:not(.active) {
        background: #e9eee7;
      }
      .hero {
        display: grid;
        grid-template-columns: 1.55fr 1fr;
        gap: 20px;
        align-items: center;
        padding: 22px 0 32px;
      }
      .hero h1 {
        font-size: clamp(30px, 5vw, 47px);
        margin: 12px 0 16px;
        max-width: 650px;
      }
      .hero p {
        max-width: 590px;
        font-size: 18px;
        color: var(--muted);
        margin-bottom: 0;
      }
      .hero-art {
        position: relative;
        height: 230px;
        display: grid;
        place-items: center;
      }
      .orb {
        width: 195px;
        height: 195px;
        border-radius: 50%;
        background: #e8eddc;
        display: grid;
        place-items: center;
        font-size: 70px;
      }
      .float {
        position: absolute;
        border: 1px solid #fff;
        border-radius: 16px;
        background: #fffefa;
        box-shadow: var(--shadow);
        padding: 14px 19px;
        font-size: 23px;
        font-weight: bold;
        transform: rotate(-8deg);
        direction: ltr;
        text-align: left;
      }
      .float.one {
        right: 6px;
        top: 35px;
        color: var(--green);
      }
      .float.two {
        left: 0;
        bottom: 30px;
        color: var(--violet);
        transform: rotate(7deg);
      }
      .section-kicker {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 10px;
        margin: 2px 0 14px;
      }
      .section-kicker h2 {
        font-size: 21px;
      }
      .section-kicker span {
        color: var(--muted);
        font-size: 13px;
      }
      .activities {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 14px;
      }
      .activity {
        background: var(--white);
        border: 1px solid var(--line);
        border-radius: 20px;
        padding: 23px;
        display: flex;
        flex-direction: column;
        align-items: flex-start;
        box-shadow: var(--shadow);
      }
      .activity-top {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 12px;
      }
      .activity-icon {
        width: 43px;
        height: 43px;
        border-radius: 14px;
        display: grid;
        place-items: center;
        font-size: 24px;
        background: #e9f1e6;
      }
      .activity:nth-child(2) .activity-icon {
        background: #fff1d0;
      }
      .activity:nth-child(3) .activity-icon {
        background: #eee8f8;
      }
      .activity:nth-child(4) .activity-icon {
        background: #e3f0ed;
      }
      .activity h3 {
        margin: 0;
      }
      .activity p {
        font-size: 16px;
        color: var(--muted);
        flex: 1;
        margin-bottom: 20px;
      }
      .btn {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        gap: 8px;
        background: var(--green);
        color: white;
        border: 1px solid transparent;
        border-radius: 12px;
        padding: 12px 18px;
        font-size: 16px;
        font-weight: 700;
        min-height: 48px;
        line-height: 1.5;
        text-align: right;
      }
      .btn.secondary {
        background: #edf1e9;
        color: var(--ink);
        border-color: #d9e2d8;
      }
      .btn.soft {
        background: white;
        color: var(--muted);
        border-color: var(--line);
      }
      .btn.danger {
        color: #983f4a;
        background: #fff4f2;
        border-color: #f0d8d9;
      }
      .activity .btn {
        width: 100%;
        justify-content: space-between;
      }
      .page-heading {
        margin-bottom: 20px;
      }
      .page-heading p {
        color: var(--muted);
        margin-bottom: 0;
      }
      .panel {
        border: 1px solid var(--line);
        border-radius: 20px;
        background: var(--white);
        padding: 22px;
        box-shadow: var(--shadow);
      }
      .toolbar {
        display: flex;
        flex-wrap: wrap;
        align-items: center;
        justify-content: space-between;
        gap: 10px;
        margin-bottom: 14px;
      }
      .subtle {
        font-size: 14px;
        color: var(--muted);
        line-height: 1.7;
      }
      .status {
        border-radius: 12px;
        padding: 12px 15px;
        line-height: 1.8;
        margin-top: 14px;
        background: #edf1e9;
      }
      .status.success {
        background: var(--good);
        color: #14553b;
      }
      .status.error {
        background: var(--bad);
        color: #8a2738;
      }
      .status.warning {
        background: #fff0cc;
        color: #7a5109;
      }
      .status:empty {
        display: none;
      }
      .actions {
        display: flex;
        gap: 10px;
        flex-wrap: wrap;
        margin-top: 16px;
      }
      .actions .btn {
        flex: 1;
      }
      .legend {
        display: flex;
        flex-wrap: wrap;
        gap: 15px;
        font-size: 13px;
        color: var(--muted);
        margin: 12px 0 0;
      }
      .legend span {
        display: inline-flex;
        align-items: center;
        gap: 5px;
      }
      .dot {
        width: 11px;
        height: 11px;
        border-radius: 4px;
        background: var(--good);
        border: 1px solid #60a881;
      }
      .dot.red {
        background: var(--bad);
        border-color: #d97d8c;
      }
      .dot.neutral {
        background: white;
        border-color: var(--line);
      }
      /* Eleven equal columns and square cells preserve the spreadsheet proportions.
   The optional large-cell view scrolls inside its own container, never the page. */
      .table-scroll {
        width: 100%;
        overflow-x: auto;
        border: 1px solid #bdcfc5;
        border-radius: 12px;
        direction: ltr;
        overscroll-behavior-x: contain;
        -webkit-overflow-scrolling: touch;
      }
      .times-table {
        display: grid;
        grid-template-columns: repeat(11, minmax(0, 1fr));
        width: 100%;
        direction: ltr;
        background: #cddcd2;
        gap: 1px;
      }
      .times-table.large {
        min-width: 610px;
      }
      .table-cell {
        aspect-ratio: 1;
        min-width: 0;
        position: relative;
        background: #fffefa;
        display: flex;
        align-items: stretch;
      }
      .table-cell.head {
        background: #e4eee6;
        color: var(--green);
        font-weight: 700;
        align-items: center;
        justify-content: flex-start;
        padding-left: clamp(2px, 1vw, 10px);
        font-size: clamp(14px, 2.6vw, 19px);
        direction: ltr;
        text-align: left;
      }
      .table-cell.corner {
        background: var(--green);
        color: white;
      }
      .table-cell input {
        border: 0;
        border-radius: 0;
        background: transparent;
        width: 100%;
        min-width: 0;
        min-height: 0;
        padding: 0 2px;
        font-size: clamp(16px, 2.7vw, 24px);
        letter-spacing: -0.045em;
        line-height: 1;
        direction: ltr;
        text-align: left;
        color: var(--ink);
        font-variant-numeric: tabular-nums;
        caret-color: var(--green);
      }
      .table-cell input:focus {
        outline: 3px solid var(--green);
        outline-offset: -3px;
        background: #f5fbf7;
      }
      .table-cell.correct {
        background: var(--good);
        box-shadow: inset 0 -3px #298055;
      }
      .table-cell.wrong {
        background: var(--bad);
        box-shadow: inset 0 -3px #ca5366;
      }
      .table-cell.correct input {
        color: #14553b;
      }
      .table-cell.wrong input {
        color: #8a2738;
      }
      .table-cell.correct:after,
      .table-cell.wrong:after {
        position: absolute;
        right: 2px;
        top: 1px;
        font-size: 9px;
        pointer-events: none;
      }
      .table-cell.correct:after {
        content: "✓";
        color: #14553b;
      }
      .table-cell.wrong:after {
        content: "×";
        color: #8a2738;
      }
      .selected-exercise {
        font-size: 18px;
        font-weight: 700;
        color: var(--green);
        min-width: 90px;
      }
      .score-pill {
        display: flex;
        gap: 8px;
        align-items: center;
        background: #fff2d4;
        border-radius: 25px;
        padding: 8px 14px;
        font-size: 14px;
      }
      .exercise-layout {
        display: grid;
        grid-template-columns: 1.3fr 0.7fr;
        gap: 18px;
      }
      .exercise-card .math {
        margin: 24px 0;
      }
      .answer-form {
        max-width: 460px;
      }
      .answer-form label {
        display: block;
        margin-bottom: 8px;
        font-weight: 700;
      }
      .answer-line {
        display: flex;
        gap: 10px;
        direction: ltr;
      }
      .answer-line input {
        min-width: 0;
        flex: 1;
      }
      .answer-line .btn {
        direction: rtl;
        flex-shrink: 0;
      }
      .note-panel {
        background: #eaf0e5;
        border: 0;
      }
      .note-panel h3 {
        margin-bottom: 10px;
      }
      .note-panel p {
        color: var(--muted);
      }
      .word-question {
        font-size: clamp(20px, 3vw, 27px);
        line-height: 2;
        margin: 22px 0;
      }
      .footer {
        color: var(--muted);
        font-size: 12px;
        line-height: 1.8;
        margin-top: 25px;
        padding-top: 16px;
        border-top: 1px solid var(--line);
      }
      .levels {
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 10px;
        margin: 18px 0;
      }
      .level {
        background: white;
        border: 1px solid var(--line);
        border-radius: 14px;
        padding: 13px 10px;
        min-height: 82px;
        color: var(--ink);
        text-align: right;
        line-height: 1.7;
      }
      .level strong {
        display: block;
        font-size: 17px;
      }
      .level small {
        font-size: 13px;
      }
      .level.active {
        border: 2px solid var(--green);
        background: #eaf4ec;
        padding: 12px 9px;
      }
      .maze-layout {
        display: grid;
        grid-template-columns: minmax(0, 1fr) 280px;
        gap: 20px;
        align-items: start;
      }
      .maze-stats {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 12px;
        flex-wrap: wrap;
        margin-bottom: 12px;
      }
      .hearts {
        font-size: 21px;
        letter-spacing: 2px;
        direction: ltr;
        display: block;
      }
      .progress-track {
        height: 7px;
        background: #e2e9df;
        border-radius: 8px;
        overflow: hidden;
        margin: 10px 0 16px;
        direction: ltr;
      }
      .progress-fill {
        height: 100%;
        background: var(--green);
        border-radius: 8px;
        transition: width 0.2s;
      }
      .maze-arena {
        position: relative;
        max-width: 600px;
        margin: auto;
      }
      .maze-board {
        display: grid;
        grid-template-columns: repeat(9, minmax(0, 1fr));
        gap: 2px;
        aspect-ratio: 1;
        direction: ltr;
        background: #c8dbc2;
        border: 7px solid #c8dbc2;
        border-radius: 18px;
        overflow: hidden;
      }
      .maze-cell {
        display: grid;
        place-items: center;
        position: relative;
        aspect-ratio: 1;
        min-width: 0;
        font-size: clamp(15px, 4vw, 30px);
        background: #efe4ba;
        border-radius: 4px;
      }
      .maze-cell.wall {
        background: #589773;
        box-shadow: inset 0 -3px #407c5c;
      }
      .maze-cell.wall:after {
        content: "♠";
        color: #c3d9b0;
        font-size: clamp(15px, 4vw, 28px);
      }
      .maze-cell.visited:not(.wall):not(.player):not(.goal):after {
        content: "·";
        font-size: 24px;
        color: #b4a362;
      }
      .maze-cell.player {
        background: #ffd27b;
        box-shadow: 0 0 0 2px #dfa747;
        z-index: 1;
      }
      .maze-cell.goal {
        background: #f6d987;
      }
      .maze-caption {
        font-size: 13px;
        color: var(--muted);
        margin-top: 10px;
      }
      .controls-panel {
        padding: 18px;
        background: #f0f3eb;
        border-radius: 18px;
      }
      .dpad {
        display: grid;
        grid-template: repeat(3, 56px) / repeat(3, 56px);
        gap: 8px;
        justify-content: center;
        direction: ltr;
        margin: 14px 0;
      }
      .dpad button {
        border-radius: 15px;
        background: white;
        color: var(--green);
        font-size: 29px;
        font-weight: bold;
        box-shadow: 0 3px 0 #cddace;
        min-width: 0;
      }
      .dpad button:active:not(:disabled) {
        transform: translateY(2px);
        box-shadow: 0 1px 0 #cddace;
      }
      .dpad [data-move="up"] {
        grid-area: 1/2;
      }
      .dpad [data-move="left"] {
        grid-area: 2/1;
      }
      .dpad [data-move="right"] {
        grid-area: 2/3;
      }
      .dpad [data-move="down"] {
        grid-area: 3/2;
      }
      .dpad-center {
        grid-area: 2/2;
        display: grid;
        place-items: center;
        color: #94a595;
        font-size: 24px;
      }
      .maze-overlay {
        position: absolute;
        inset: 0;
        z-index: 5;
        background: #183e35b8;
        backdrop-filter: blur(3px);
        border-radius: 18px;
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 12px;
      }
      .question-box {
        width: 100%;
        max-width: 370px;
        border-radius: 18px;
        background: #fffefa;
        padding: 20px;
        box-shadow: 0 14px 50px #0e332b40;
      }
      .question-box h3 {
        margin: 0 0 6px;
        font-size: 20px;
      }
      .question-box .math {
        font-size: 36px;
        margin: 6px 0 10px;
      }
      .question-box input {
        min-height: 44px;
        padding: 8px;
      }
      .question-box .btn {
        min-height: 44px;
        padding: 8px 12px;
      }
      .question-box .status {
        font-size: 14px;
        margin-top: 9px;
        padding: 8px 10px;
        line-height: 1.5;
      }
      .question-box label {
        font-size: 14px;
        display: block;
        margin-bottom: 5px;
      }
      .end-box {
        text-align: right;
      }
      .end-icon {
        font-size: 48px;
        margin-bottom: 3px;
      }
      .end-box h3 {
        margin-bottom: 5px;
      }
      .end-box p {
        font-size: 15px;
        line-height: 1.6;
        margin-bottom: 10px;
      }
      .end-box .btn {
        width: 100%;
        margin-top: 6px;
      }
      .dragon-stage {
        position: relative;
        height: 76px;
        overflow: hidden;
        direction: ltr;
      }
      .dragon-stage .dragon {
        position: absolute;
        left: 5%;
        top: 0;
        font-size: 57px;
        animation: dragon-catch 1.5s ease-out both;
      }
      .dragon-stage .kid {
        position: absolute;
        left: 70%;
        top: 17px;
        font-size: 37px;
        animation: kid-away 1.5s ease-out both;
      }
      @keyframes dragon-catch {
        0% {
          left: -30%;
        }
        65% {
          left: 55%;
          transform: scale(1.1);
        }
        100% {
          left: 110%;
          transform: translateY(-20px);
        }
      }
      @keyframes kid-away {
        0%,
        55% {
          opacity: 1;
          transform: none;
        }
        100% {
          opacity: 0;
          transform: translate(150px, -45px) scale(0.5);
        }
      }
      .fireworks {
        position: fixed;
        inset: 0;
        pointer-events: none;
        z-index: 80;
        overflow: hidden;
      }
      .spark {
        position: absolute;
        width: 7px;
        height: 7px;
        border-radius: 50%;
        background: var(--spark);
        animation: spark 1.1s ease-out var(--delay) both;
      }
      @keyframes spark {
        0% {
          opacity: 0;
          transform: translate(0, 0) scale(0.2);
        }
        10% {
          opacity: 1;
        }
        100% {
          opacity: 0;
          transform: translate(var(--dx), var(--dy)) scale(0.35);
        }
      }
      @media (min-width: 800px) {
        .table-panel {
          max-width: 790px;
          margin: auto;
        }
        .table-cell input {
          padding-left: 7px;
        }
        .table-cell.correct:after,
        .table-cell.wrong:after {
          font-size: 12px;
          right: 4px;
          top: 3px;
        }
      }
      @media (max-width: 760px) {
        .app {
          padding: 16px 14px 24px;
        }
        .hero {
          grid-template-columns: 1fr;
          padding: 8px 0 24px;
        }
        .hero-art {
          display: none;
        }
        .hero h1 {
          font-size: 34px;
          max-width: 540px;
        }
        .hero p {
          font-size: 17px;
        }
        .exercise-layout,
        .maze-layout {
          grid-template-columns: 1fr;
        }
        .controls-panel {
          padding: 14px;
        }
        .dpad {
          margin: 8px 0;
        }
        .controls-panel > p {
          margin-bottom: 8px;
        }
        .note-panel {
          display: none;
        }
        .maze-layout {
          gap: 14px;
        }
        .nav {
          margin-bottom: 20px;
        }
        .nav button {
          padding: 9px 11px;
        }
        .panel {
          padding: 16px;
        }
        .activities {
          gap: 12px;
        }
        .activity {
          padding: 18px;
        }
        .activity h3 {
          font-size: 18px;
        }
      }
      @media (max-width: 480px) {
        .app {
          padding: 12px 10px 24px;
        }
        .brand-note {
          font-size: 12px;
        }
        .brand-name {
          font-size: 16px;
        }
        .brand-row {
          gap: 9px;
        }
        .brand-mark {
          width: 38px;
          height: 38px;
          font-size: 25px;
        }
        .nav {
          gap: 3px;
          padding-top: 3px;
          padding-bottom: 12px;
        }
        .nav button {
          font-size: 13px;
          padding: 8px 9px;
          min-height: 39px;
        }
        .hero h1 {
          font-size: 31px;
        }
        .hero p {
          font-size: 16px;
        }
        .activities {
          grid-template-columns: 1fr;
        }
        .activity {
          padding: 19px;
        }
        .activity p {
          margin-bottom: 14px;
        }
        .section-kicker span {
          display: none;
        }
        .table-panel {
          padding: 8px;
          border-radius: 14px;
        }
        .toolbar {
          gap: 7px;
          margin: 4px 0 10px;
        }
        .toolbar .btn {
          font-size: 13px;
          padding: 8px 10px;
          min-height: 40px;
        }
        .toolbar .subtle {
          font-size: 12px;
        }
        .table-cell input {
          font-size: 16px;
          padding-left: 1px;
          letter-spacing: -0.065em;
        }
        .table-cell.head {
          font-size: 14px;
          padding-left: 2px;
        }
        .table-cell.correct:after,
        .table-cell.wrong:after {
          font-size: 7px;
          right: 1px;
          top: 0;
        }
        .legend {
          font-size: 12px;
          gap: 10px;
          margin-right: 3px;
        }
        .actions {
          gap: 7px;
        }
        .actions .btn {
          font-size: 14px;
          padding: 10px 8px;
          min-height: 48px;
        }
        .actions .btn.primary {
          flex-basis: 100%;
        }
        .table-panel .status {
          font-size: 14px;
        }
        .level {
          padding: 10px 7px;
        }
        .level.active {
          padding: 9px 6px;
        }
        .level strong {
          font-size: 16px;
        }
        .level small {
          font-size: 12px;
        }
        .levels {
          gap: 6px;
        }
        .maze-panel {
          padding: 9px;
        }
        .maze-board {
          border-width: 5px;
          gap: 2px;
        }
        .maze-overlay {
          padding: 9px;
        }
        .question-box {
          padding: 13px;
          border-radius: 14px;
        }
        .question-box h3 {
          font-size: 18px;
        }
        .question-box .math {
          font-size: 30px;
          margin: 4px 0 7px;
        }
        .question-box .status {
          font-size: 13px;
          padding: 6px 8px;
        }
        .question-box .btn {
          font-size: 14px;
        }
        .end-icon {
          font-size: 34px;
        }
        .end-box p {
          font-size: 13px;
        }
        .end-box h3 {
          font-size: 18px;
        }
        .dragon-stage {
          height: 60px;
        }
        .dragon-stage .dragon {
          font-size: 44px;
        }
        .dragon-stage .kid {
          font-size: 28px;
        }
        .answer-line {
          gap: 7px;
        }
        .score-pill {
          font-size: 13px;
          padding: 7px 11px;
        }
        .page-heading {
          margin-bottom: 14px;
        }
        .page-heading p {
          font-size: 15px;
        }
        .maze-stats {
          gap: 6px;
          font-size: 14px;
        }
      }
      @media (max-width: 360px) {
        .table-cell input {
          letter-spacing: -0.12em;
          padding: 0;
          font-size: 16px;
        }
      }
      @media (prefers-reduced-motion: reduce) {
        *,
        *:before,
        *:after {
          animation: none !important;
          transition: none !important;
          scroll-behavior: auto !important;
        }
        .spark {
          display: none;
        }
        .dragon-stage .dragon {
          left: 45%;
        }
        .dragon-stage .kid {
          left: 72%;
        }
      }
    </style>
  </head>
  <body>
    <main class="app" id="app">
      <header>
        <div class="brand-row">
          <div class="brand-mark" aria-hidden="true">×</div>
          <div>
            <div class="brand-name">לוּחַ הַכֶּפֶל שֶׁל שָׁקֵד בֶּן עֶזְרָא</div>
            <div class="brand-note">קוֹרְאִים, מְנַסִּים, מַצְלִיחִים.</div>
          </div>
        </div>
        <nav class="nav" aria-label="בְּחִירַת פְּעִילוּת">
          <button data-page="home" class="active" aria-current="page">הַבַּיִת</button>
          <button data-page="table">לוּחַ הַכֶּפֶל</button>
          <button data-page="quick">תִּרְגּוּל מָהִיר</button>
          <button data-page="words">שְׁאֵלוֹת מִלּוּלִיּוֹת</button>
          <button data-page="maze">הַמָּבוֹךְ</button>
        </nav>
      </header>
      <section id="page-home" class="page" aria-labelledby="home-title">
        <div class="hero">
          <div>
            <span class="tag">הַהַרְפַּתְקָה שֶׁל שָׁקֵד</span>
            <h1 id="home-title">לוּחַ הַכֶּפֶל שֶׁל<br />שָׁקֵד בֶּן עֶזְרָא</h1>
            <p>
              כָּאן לוֹמְדִים אֶת לוּחַ הַכֶּפֶל עַד <bdi>10</bdi>, בַּדֶּרֶךְ שֶׁהֲכִי אוֹהֲבִים:
              מְמַלְּאִים טַבְלָה, פּוֹתְרִים שְׁאֵלוֹת וְיוֹצְאִים לְהַרְפַּתְקָה בַּיַּעַר. כָּל
              נִסָּיוֹן הוּא הִזְדַּמְּנוּת לִלְמֹד!
            </p>
          </div>
          <div class="hero-art" aria-hidden="true">
            <div class="orb">🌱</div>
            <div class="float one">3 × 4 = 12</div>
            <div class="float two">7 × 8 = 56 ✨</div>
          </div>
        </div>
        <div class="section-kicker">
          <h2>בְּמָה נִרְצֶה לְשַׂחֵק הַיּוֹם?</h2>
          <span>אַרְבַּע דְּרָכִים לְתַרְגֵּל</span>
        </div>
        <div class="activities">
          <article class="activity">
            <div class="activity-top">
              <span class="activity-icon" aria-hidden="true">▦</span>
              <h3>לוּחַ הַכֶּפֶל</h3>
            </div>
            <p>
              מְמַלְּאִים כַּמָּה תָּאִים שֶׁרוֹצִים וּבוֹדְקִים. תְּשׁוּבָה נְכוֹנָה נִצְבַּעַת
              בְּיָרֹק, וְטָעוּת בְּאָדֹם. הַכֹּל נָכוֹן? חוֹגְגִים עִם זִקּוּקִים!
            </p>
            <button class="btn" data-page="table">
              לַטַּבְלָה <span aria-hidden="true">←</span>
            </button>
          </article>
          <article class="activity">
            <div class="activity-top">
              <span class="activity-icon" aria-hidden="true">⚡</span>
              <h3>תִּרְגּוּל מָהִיר</h3>
            </div>
            <p>
              תַּרְגִּיל אֶחָד בְּכָל פַּעַם, בְּלִי לַחַץ שֶׁל זְמַן. מַקְלִידִים תְּשׁוּבָה,
              מְקַבְּלִים מָשׁוֹב וְצוֹבְרִים נְקֻדּוֹת.
            </p>
            <button class="btn" data-page="quick">
              לַתִּרְגּוּל <span aria-hidden="true">←</span>
            </button>
          </article>
          <article class="activity">
            <div class="activity-top">
              <span class="activity-icon" aria-hidden="true">📖</span>
              <h3>שְׁאֵלוֹת מִלּוּלִיּוֹת</h3>
            </div>
            <p>
              מְגַלִּים אֵיפֹה מִסְתַּתֵּר הַכֶּפֶל בְּסִפּוּרִים קְצָרִים מֵחַיֵּי הַיּוֹם־יוֹם.
              קוֹרְאִים, חוֹשְׁבִים וּמַקְלִידִים אֶת הַתְּשׁוּבָה.
            </p>
            <button class="btn" data-page="words">
              לַסִּפּוּרִים <span aria-hidden="true">←</span>
            </button>
          </article>
          <article class="activity">
            <div class="activity-top">
              <span class="activity-icon" aria-hidden="true">🌲</span>
              <h3>הַמָּבוֹךְ הַקָּסוּם</h3>
            </div>
            <p>
              מִתְקַדְּמִים עִם הַחִצִּים. כָּל שְׁלוֹשָׁה צְעָדִים פּוֹתְרִים שְׁאֵלָה. שָׁלוֹשׁ
              רָמוֹת, שְׁלוֹשָׁה לְבָבוֹת וְדְרָקוֹן אֶחָד שׁוֹבָב!
            </p>
            <button class="btn" data-page="maze">
              לַהַרְפַּתְקָה <span aria-hidden="true">←</span>
            </button>
          </article>
        </div>
      </section>
      <section id="page-table" class="page" hidden aria-labelledby="table-title">
        <div class="page-heading">
          <span class="tag">מְתַרְגְּלִים בַּקֶּצֶב שֶׁלָּנוּ</span>
          <h2 id="table-title">לוּחַ הַכֶּפֶל</h2>
          <p>
            מְמַלְּאִים גַּם רַק חֵלֶק מֵהַטַּבְלָה, וְאָז לוֹחֲצִים עַל ״בְּדִיקַת תְּשׁוּבוֹת״.
          </p>
        </div>
        <div class="panel table-panel">
          <div class="toolbar">
            <div>
              <div class="subtle">הַתַּרְגִּיל שֶׁבָּחַרְנוּ</div>
              <div class="selected-exercise math" id="selected-exercise" aria-live="polite">
                1 × 1 = ?
              </div>
            </div>
            <button class="btn secondary" id="table-zoom" aria-pressed="false">
              הַגְדָּלַת הַתָּאִים ⤢
            </button>
          </div>
          <p id="zoom-hint" class="subtle" hidden>
            אֶפְשָׁר לְהַחְלִיק אֶת הַטַּבְלָה לַצְּדָדִים.
          </p>
          <div
            class="table-scroll"
            id="table-scroll"
            tabindex="0"
            role="region"
            aria-label="טַבְלַת כֶּפֶל עַד עֶשֶׂר"
          >
            <div
              class="times-table"
              id="times-table"
              role="group"
              aria-label="מִלּוּי לוּחַ הַכֶּפֶל"
            ></div>
          </div>
          <div class="legend">
            <span><i class="dot"></i>נָכוֹן ✓</span
            ><span><i class="dot red"></i>כְּדַאי לְנַסּוֹת שׁוּב ×</span
            ><span><i class="dot neutral"></i>עֲדַיִן לֹא נִבְדַּק</span>
          </div>
          <div class="actions">
            <button class="btn primary" id="check-table">בְּדִיקַת תְּשׁוּבוֹת ✓</button
            ><button class="btn secondary" id="clear-wrong">מְחִיקַת תְּשׁוּבוֹת שְׁגוּיוֹת</button
            ><button class="btn soft" id="clear-table">מְחִיקַת הַכֹּל</button>
          </div>
          <div class="status" id="table-status" role="status" aria-live="polite"></div>
        </div>
      </section>
      <section id="page-quick" class="page" hidden aria-labelledby="quick-title">
        <div class="page-heading">
          <span class="tag">תַּרְגִּיל קָטָן, הַצְלָחָה גְדוֹלָה</span>
          <h2 id="quick-title">תִּרְגּוּל מָהִיר</h2>
          <p>חוֹשְׁבִים, מַקְלִידִים וּבוֹדְקִים. אֶפְשָׁר לְנַסּוֹת שׁוּב!</p>
        </div>
        <div class="exercise-layout">
          <div class="panel exercise-card">
            <div class="toolbar">
              <strong>כַּמָּה זֶה?</strong>
              <div class="score-pill">⭐ נְקֻדּוֹת <bdi id="quick-score">0</bdi></div>
            </div>
            <div class="math" id="quick-exercise"></div>
            <form class="answer-form" id="quick-form" novalidate>
              <label for="quick-answer">הַתְּשׁוּבָה שֶׁלָּנוּ</label>
              <div class="answer-line">
                <input
                  id="quick-answer"
                  class="numeric"
                  type="text"
                  inputmode="numeric"
                  pattern="[0-9]*"
                  maxlength="3"
                  dir="ltr"
                  autocomplete="off"
                /><button class="btn" id="quick-submit" type="submit">בְּדִיקָה</button>
              </div>
            </form>
            <div class="status" id="quick-status" role="status"></div>
            <div class="actions">
              <button class="btn secondary" id="quick-next">הַתַּרְגִּיל הַבָּא ←</button>
            </div>
          </div>
          <aside class="panel note-panel">
            <h3>כָּל נִסָּיוֹן מְקַדֵּם אוֹתָנוּ 🌱</h3>
            <p>
              תְּשׁוּבָה נְכוֹנָה מוֹסִיפָה <bdi>10</bdi> נְקֻדּוֹת. הַתַּרְגִּיל נִשְׁאָר עַל
              הַמָּסָךְ עַד שֶׁבּוֹחֲרִים לְהַמְשִׁיךְ.
            </p>
          </aside>
        </div>
      </section>
      <section id="page-words" class="page" hidden aria-labelledby="words-title">
        <div class="page-heading">
          <span class="tag">כֶּפֶל בַּחַיִּים שֶׁלָּנוּ</span>
          <h2 id="words-title">שְׁאֵלוֹת מִלּוּלִיּוֹת</h2>
          <p>קוֹרְאִים אֶת הַסִּפּוּר וּמַקְלִידִים תְּשׁוּבָה בְּמִסְפָּר.</p>
        </div>
        <div class="panel exercise-card">
          <div class="toolbar">
            <span>הַסִּפּוּר שֶׁלָּנוּ <bdi id="word-number"></bdi></span
            ><span class="score-pill">⭐ נְקֻדּוֹת <bdi id="word-score">0</bdi></span>
          </div>
          <p id="word-question" class="word-question"></p>
          <form class="answer-form" id="word-form" novalidate>
            <label for="word-answer">הַתְּשׁוּבָה שֶׁלָּנוּ</label>
            <div class="answer-line">
              <input
                id="word-answer"
                class="numeric"
                type="text"
                inputmode="numeric"
                pattern="[0-9]*"
                maxlength="3"
                dir="ltr"
                autocomplete="off"
              /><button class="btn" id="word-submit" type="submit">בְּדִיקָה</button>
            </div>
          </form>
          <div class="status" id="word-status" role="status"></div>
          <div class="actions">
            <button class="btn secondary" id="word-next">הַסִּפּוּר הַבָּא ←</button>
          </div>
        </div>
      </section>
      <section id="page-maze" class="page" hidden aria-labelledby="maze-title">
        <div class="page-heading">
          <span class="tag">הַרְפַּתְקָה בֵּין הָעֵצִים</span>
          <h2 id="maze-title">הַמָּבוֹךְ הַקָּסוּם</h2>
          <p>כָּל שְׁלוֹשָׁה צְעָדִים — שְׁאֵלַת כֶּפֶל. פּוֹתְרִים וּמַמְשִׁיכִים לַדֶּגֶל!</p>
        </div>
        <div class="levels" id="levels" aria-label="רָמוֹת הַמִּשְׂחָק"></div>
        <div class="panel maze-panel">
          <div class="maze-stats">
            <span id="maze-stage"></span
            ><span class="hearts" id="maze-hearts" aria-live="polite"></span
            ><span class="score-pill">⭐ <bdi id="maze-score">0</bdi></span>
          </div>
          <div
            class="progress-track"
            role="progressbar"
            id="maze-progress"
            aria-label="הִתְקַדְּמוּת בָּרָמָה"
            aria-valuemin="0"
            aria-valuemax="10"
            aria-valuenow="0"
          >
            <div class="progress-fill" id="maze-progress-fill"></div>
          </div>
          <div class="maze-layout">
            <div>
              <div class="maze-arena" id="maze-arena">
                <div
                  class="maze-board"
                  id="maze-board"
                  role="img"
                  aria-label="מַפַּת הַמָּבוֹךְ"
                ></div>
                <div
                  class="maze-overlay"
                  id="maze-question"
                  hidden
                  role="dialog"
                  aria-labelledby="maze-question-title"
                >
                  <div class="question-box">
                    <h3 id="maze-question-title">עֲצִירָה לְשְׁאֵלָה ✨</h3>
                    <div class="math" id="maze-exercise"></div>
                    <form id="maze-form" novalidate>
                      <label for="maze-answer">מַקְלִידִים אֶת הַתְּשׁוּבָה</label>
                      <div class="answer-line">
                        <input
                          id="maze-answer"
                          class="numeric"
                          type="text"
                          inputmode="numeric"
                          pattern="[0-9]*"
                          maxlength="3"
                          dir="ltr"
                          autocomplete="off"
                        /><button class="btn" type="submit">בְּדִיקָה</button>
                      </div>
                    </form>
                    <div id="maze-answer-status" class="status" role="status"></div>
                  </div>
                </div>
                <div class="maze-overlay" id="maze-end" hidden>
                  <div class="question-box end-box" id="maze-end-content" role="status"></div>
                </div>
              </div>
              <div class="maze-caption" id="maze-caption"></div>
            </div>
            <div class="controls-panel">
              <strong>לְאָן מִתְקַדְּמִים?</strong>
              <div class="dpad" aria-label="כַּפְתּוֹרֵי תְּנוּעָה">
                <button data-move="up" aria-label="לְמַעְלָה">↑</button
                ><button data-move="left" aria-label="שְׂמֹאלָה">←</button
                ><span class="dpad-center" aria-hidden="true">✥</span
                ><button data-move="right" aria-label="יָמִינָה">→</button
                ><button data-move="down" aria-label="לְמַטָּה">↓</button>
              </div>
              <div class="status" id="maze-status" role="status"></div>
              <p class="subtle">
                כָּל טָעוּת מוֹרִידָה לֵב אֶחָד. אַחֲרֵי שָׁלוֹשׁ טָעֻיּוֹת, הַדְּרָקוֹן מַגִּיעַ —
                וְאֶפְשָׁר לְנַסּוֹת מֵחָדָשׁ.
              </p>
              <button class="btn soft" id="maze-restart">הַתְחָלַת הָרָמָה מֵחָדָשׁ ↻</button>
            </div>
          </div>
        </div>
        <p class="subtle" style="margin-top: 14px">
          כְּדֵי לִפְתֹּחַ אֶת הָרָמָה הַבָּאָה, מְסַיְּמִים אֶת הָרָמָה עִם לְפָחוֹת
          <bdi>80%</bdi> תְּשׁוּבוֹת נְכוֹנוֹת בַּנִּסָּיוֹן הָרִאשׁוֹן. כָּל תְּשׁוּבָה נְכוֹנָה
          מְזַכָּה בִּנְקֻדּוֹת.
        </p>
      </section>
      <footer class="footer">
        נִבְנָה בְּאַהֲבָה לְשָׁקֵד · הַהִתְקַדְּמוּת נִשְׁמֶרֶת בַּדַּפְדְּפָן הַזֶּה.<span
          id="storage-note"
          hidden
        >
          הַשְּׁמִירָה אֵינָהּ זְמִינָה כָּעֵת; אֶפְשָׁר לְהַמְשִׁיךְ לְשַׂחֵק.</span
        >
      </footer>
    </main>
    <div class="fireworks" id="fireworks" aria-hidden="true"></div>
    <script>
      "use strict";
      // All game state stays in this component: button presses never rerun Python.
      // No external scripts, fonts, trackers or parent-DOM access are required.
      const STORAGE_KEY = "shaked.multiplication.v3";
      const $ = (id) => document.getElementById(id);
      const TOTALS = [10, 15, 20],
        LEVEL_NAMES = ["א׳", "ב׳", "ג׳"];
      const randomInt = (min, max) => min + Math.floor(Math.random() * (max - min + 1));
      const newQuestion = (min = 1, max = 10) => ({
        a: randomInt(min, max),
        b: randomInt(1, 10),
        tries: 0,
        solved: false,
        input: "",
      });
      const newState = () => ({
        version: 3,
        table: Array(100).fill(""),
        marks: Array(100).fill(""),
        large: false,
        quick: { ...newQuestion(), score: 0 },
        wordIndex: 0,
        wordInputs: Array(12).fill(""),
        wordSolved: Array(12).fill(false),
        wordTries: Array(12).fill(0),
        unlocked: 0,
        best: [0, 0, 0],
        maze: null,
      });
      function loadState() {
        try {
          const raw = JSON.parse(localStorage.getItem(STORAGE_KEY));
          if (!raw || raw.version !== 3) return newState();
          const fresh = newState();
          Object.assign(fresh, raw);
          if (
            !Array.isArray(raw.table) ||
            raw.table.length !== 100 ||
            !raw.table.every((x) => typeof x === "string")
          )
            return newState();
          if (!Array.isArray(raw.marks) || raw.marks.length !== 100)
            fresh.marks = Array(100).fill("");
          fresh.marks = fresh.marks.map((x) => (["correct", "wrong"].includes(x) ? x : ""));
          if (!Number.isInteger(raw.unlocked) || raw.unlocked < 0 || raw.unlocked > 2)
            fresh.unlocked = 0;
          if (!Array.isArray(raw.best) || raw.best.length !== 3) fresh.best = [0, 0, 0];
          if (
            !raw.quick ||
            !Number.isInteger(raw.quick.a) ||
            raw.quick.a < 1 ||
            raw.quick.a > 10 ||
            !Number.isInteger(raw.quick.b) ||
            raw.quick.b < 1 ||
            raw.quick.b > 10
          )
            fresh.quick = { ...newQuestion(), score: 0 };
          for (const key of ["wordInputs", "wordSolved", "wordTries"])
            if (!Array.isArray(raw[key]) || raw[key].length !== 12) fresh[key] = newState()[key];
          if (!Number.isInteger(raw.wordIndex) || raw.wordIndex < 0 || raw.wordIndex >= 12)
            fresh.wordIndex = 0;
          if (!validMaze(raw.maze)) fresh.maze = null;
          return fresh;
        } catch {
          return newState();
        }
      }
      function validMaze(m) {
        return (
          m === null ||
          !!(
            m &&
            Number.isInteger(m.level) &&
            m.level >= 0 &&
            m.level < 3 &&
            Array.isArray(m.grid) &&
            m.grid.length === 9 &&
            m.grid.every((row) => Array.isArray(row) && row.length === 9) &&
            Number.isInteger(m.x) &&
            m.x >= 0 &&
            m.x < 9 &&
            Number.isInteger(m.y) &&
            m.y >= 0 &&
            m.y < 9 &&
            Number.isInteger(m.lives) &&
            m.lives >= 0 &&
            m.lives <= 3 &&
            Number.isInteger(m.completed) &&
            m.completed >= 0 &&
            m.completed <= TOTALS[m.level] &&
            Array.isArray(m.visited) &&
            m.visited.length === 81 &&
            m.question &&
            Number.isInteger(m.question.a) &&
            Number.isInteger(m.question.b) &&
            ["playing", "lost", "passed", "retry"].includes(m.status)
          )
        );
      }
      const state = loadState();
      let page = "home",
        fireworkTimer = null,
        restartPending = false;
      function save() {
        try {
          localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
          $("storage-note").hidden = true;
        } catch {
          $("storage-note").hidden = false;
        }
      }
      function status(id, text, kind = "") {
        const node = $(id);
        node.className = "status " + kind;
        node.textContent = text;
        resizeFrame();
      }
      function parseAnswer(value) {
        const text = value.trim();
        return /^\d{1,3}$/.test(text) ? Number(text) : null;
      }
      function numHTML(value) {
        return "<bdi>" + Number(value) + "</bdi>";
      }
      function ratioHTML(a, b) {
        return "<bdi>" + Number(a) + " / " + Number(b) + "</bdi>";
      }
      function percentHTML(value) {
        return "<bdi>" + Number(value) + "%</bdi>";
      }
      function normalizeDigits(value) {
        return value
          .replace(/[٠-٩]/g, (c) => String(c.charCodeAt(0) - 1632))
          .replace(/[۰-۹]/g, (c) => String(c.charCodeAt(0) - 1776));
      }
      document.addEventListener(
        "input",
        (event) => {
          if (event.target.matches('input[inputmode="numeric"]'))
            event.target.value = normalizeDigits(event.target.value);
        },
        true,
      );
      let lastHeight = 0,
        resizeQueued = false;
      function message(type, extra = {}) {
        if (window.parent !== window)
          window.parent.postMessage({ isStreamlitMessage: true, type, ...extra }, "*");
      }
      function resizeFrame() {
        if (resizeQueued) return;
        resizeQueued = true;
        requestAnimationFrame(() => {
          resizeQueued = false;
          const height = Math.ceil($("app").getBoundingClientRect().height) + 2;
          if (height !== lastHeight) {
            lastHeight = height;
            message("streamlit:setFrameHeight", { height });
          }
        });
      }
      window.addEventListener("message", (event) => {
        if (event.source === window.parent && event.data && event.data.type === "streamlit:render")
          resizeFrame();
      });
      function navigate(next) {
        if (!["home", "table", "quick", "words", "maze"].includes(next)) return;
        page = next;
        document.querySelectorAll(".page").forEach((el) => (el.hidden = el.id !== "page-" + next));
        document.querySelectorAll(".nav [data-page]").forEach((button) => {
          button.classList.toggle("active", button.dataset.page === next);
          if (button.dataset.page === next) button.setAttribute("aria-current", "page");
          else button.removeAttribute("aria-current");
        });
        if (next === "table") paintTable();
        if (next === "quick") renderQuick();
        if (next === "words") renderWords();
        if (next === "maze") {
          if (!state.maze) startMaze(0);
          else renderMaze();
        }
        $("app").scrollIntoView({ block: "start", behavior: "instant" });
        resizeFrame();
      }
      document
        .querySelectorAll("[data-page]")
        .forEach((button) => button.addEventListener("click", () => navigate(button.dataset.page)));
      function fireworks() {
        clearTimeout(fireworkTimer);
        const layer = $("fireworks");
        layer.replaceChildren();
        const colors = ["#1b947a", "#ffbf45", "#e9798c", "#8872c4", "#45a6cd"];
        for (let burst = 0; burst < 7; burst++) {
          const x = 12 + Math.random() * 76,
            y = 10 + Math.random() * 50;
          for (let i = 0; i < 22; i++) {
            const spark = document.createElement("i");
            spark.className = "spark";
            const angle = (i / 22) * Math.PI * 2,
              distance = 35 + Math.random() * 100;
            spark.style.cssText = `left:${x}%;top:${y}%;--spark:${colors[(i + burst) % colors.length]};--dx:${Math.cos(angle) * distance}px;--dy:${Math.sin(angle) * distance + 35}px;--delay:${burst * 0.24}s`;
            layer.append(spark);
          }
        }
        fireworkTimer = setTimeout(() => layer.replaceChildren(), 2900);
      }
      // Table: input, style and source of truth belong to the same cell.
      function createTable() {
        const grid = $("times-table");
        const frag = document.createDocumentFragment();
        for (let r = 0; r <= 10; r++)
          for (let c = 0; c <= 10; c++) {
            const cell = document.createElement("div");
            cell.className = "table-cell";
            if (!r || !c) {
              cell.classList.add("head");
              if (!r && !c) cell.classList.add("corner");
              cell.textContent = !r && !c ? "×" : String(r || c);
              cell.setAttribute("aria-hidden", "true");
            } else {
              const i = (r - 1) * 10 + c - 1;
              cell.id = "cell-" + i;
              const input = document.createElement("input");
              input.type = "text";
              input.inputMode = "numeric";
              input.pattern = "[0-9]*";
              input.maxLength = 3;
              input.autocomplete = "off";
              input.dir = "ltr";
              input.id = "table-" + i;
              input.dataset.index = i;
              input.setAttribute("aria-label", `${r} כָּפוּל ${c}`);
              input.value = state.table[i];
              input.addEventListener("focus", () => {
                $("selected-exercise").textContent = `${r} × ${c} = ?`;
              });
              input.addEventListener("input", () => {
                state.table[i] = input.value;
                state.marks[i] = "";
                paintCell(i);
                status("table-status", "");
                save();
              });
              input.addEventListener("keydown", (event) => {
                let target = i;
                const deltas = {
                  ArrowLeft: -1,
                  ArrowRight: 1,
                  ArrowUp: -10,
                  ArrowDown: 10,
                  Enter: 1,
                };
                if (event.key in deltas) {
                  target = i + deltas[event.key];
                  if (target >= 0 && target < 100) {
                    event.preventDefault();
                    $("table-" + target).focus();
                    $("table-" + target).select();
                  }
                }
              });
              cell.append(input);
            }
            frag.append(cell);
          }
        grid.replaceChildren(frag);
        paintTable();
      }
      function paintCell(i) {
        const node = $("cell-" + i),
          input = $("table-" + i);
        node.className = "table-cell" + (state.marks[i] ? " " + state.marks[i] : "");
        input.setAttribute("aria-invalid", state.marks[i] === "wrong" ? "true" : "false");
        const r = Math.floor(i / 10) + 1,
          c = (i % 10) + 1;
        input.setAttribute(
          "aria-label",
          `${r} כָּפוּל ${c}` +
            (state.marks[i] === "correct"
              ? " — נָכוֹן"
              : state.marks[i] === "wrong"
                ? " — תְּשׁוּבָה שְׁגוּיָה"
                : ""),
        );
        if (document.activeElement !== input) input.value = state.table[i];
      }
      function paintTable() {
        state.table.forEach((_, i) => paintCell(i));
        $("times-table").classList.toggle("large", !!state.large);
        $("table-zoom").setAttribute("aria-pressed", String(!!state.large));
        $("table-zoom").textContent = state.large
          ? "כָּל הַלּוּחַ בַּמָּסָךְ ⤡"
          : "הַגְדָּלַת הַתָּאִים ⤢";
        $("zoom-hint").hidden = !state.large;
        resizeFrame();
      }
      function checkTable() {
        let filled = 0,
          correct = 0;
        state.table.forEach((value, i) => {
          if (!value.trim()) {
            state.marks[i] = "";
            return;
          }
          filled++;
          const expected = (Math.floor(i / 10) + 1) * ((i % 10) + 1),
            good = parseAnswer(value) === expected;
          state.marks[i] = good ? "correct" : "wrong";
          if (good) correct++;
        });
        paintTable();
        save();
        if (!filled) {
          status("table-status", "עֲדַיִן לֹא מִלֵּאנוּ תְּשׁוּבוֹת. נַתְחִיל בְּתָא אֶחָד?");
          return;
        }
        if (correct === filled) {
          status(
            "table-status",
            `כָּל הַכָּבוֹד! כָּל ${filled} הַתְּשׁוּבוֹת שֶׁמִּלֵּאנוּ נְכוֹנוֹת! 🎆`,
            "success",
          );
          fireworks();
        } else
          status(
            "table-status",
            `${correct} תְּשׁוּבוֹת נְכוֹנוֹת מִתּוֹךְ ${filled}. אֶת הַתָּאִים הָאֲדֻמִּים אֶפְשָׁר לְתַקֵּן וְלִבְדֹּק שׁוּב.`,
            "warning",
          );
      }
      $("check-table").addEventListener("click", checkTable);
      $("clear-wrong").addEventListener("click", () => {
        let count = 0;
        state.table.forEach((value, i) => {
          if (value.trim() && parseAnswer(value) !== (Math.floor(i / 10) + 1) * ((i % 10) + 1)) {
            state.table[i] = "";
            state.marks[i] = "";
            count++;
          }
        });
        paintTable();
        save();
        status(
          "table-status",
          count
            ? `מָחַקְנוּ ${count} תְּשׁוּבוֹת שְׁגוּיוֹת. הַתְּשׁוּבוֹת הַנְּכוֹנוֹת נִשְׁאֲרוּ בַּטַּבְלָה.`
            : "אֵין תְּשׁוּבוֹת שְׁגוּיוֹת לִמְחִיקָה.",
        );
      });
      $("clear-table").addEventListener("click", () => {
        state.table.fill("");
        state.marks.fill("");
        paintTable();
        save();
        status("table-status", "הַטַּבְלָה נְקִיָּה. מוּכָנִים לְנִסָּיוֹן חָדָשׁ!");
      });
      $("table-zoom").addEventListener("click", () => {
        state.large = !state.large;
        paintTable();
        save();
      });
      // Practice retains the displayed question until Next is explicitly pressed.
      function renderQuick() {
        const q = state.quick;
        $("quick-exercise").textContent = `${q.a} × ${q.b} = ?`;
        $("quick-score").textContent = q.score;
        $("quick-answer").value = q.input || "";
        $("quick-answer").disabled = q.solved;
        $("quick-submit").disabled = q.solved;
        status(
          "quick-status",
          q.solved
            ? "נָכוֹן מְאֹד! אֶפְשָׁר לְהַמְשִׁיךְ לַתַּרְגִּיל הַבָּא."
            : q.tries
              ? "נְנַסֶּה שׁוּב. אֶפְשָׁר לַחְשֹׁב עַל חִבּוּר חוֹזֵר."
              : "",
          q.solved ? "success" : "",
        );
      }
      $("quick-answer").addEventListener("input", (event) => {
        state.quick.input = event.target.value;
        save();
      });
      $("quick-form").addEventListener("submit", (event) => {
        event.preventDefault();
        const q = state.quick;
        if (q.solved) return;
        const ans = parseAnswer($("quick-answer").value);
        if (ans === null) {
          status("quick-status", "נַקְלִיד מִסְפָּר שָׁלֵם כְּדֵי לִבְדֹּק.", "warning");
          return;
        }
        q.tries++;
        if (ans === q.a * q.b) {
          q.solved = true;
          q.score += 10;
          save();
          renderQuick();
          fireworks();
        } else {
          save();
          status(
            "quick-status",
            "כִּמְעַט! נְנַסֶּה שׁוּב. אֶפְשָׁר לְחַבֵּר קְבוּצוֹת שָׁווֹת.",
            "error",
          );
        }
      });
      $("quick-next").addEventListener("click", () => {
        const old = state.quick;
        let q;
        do {
          q = newQuestion();
        } while (q.a === old.a && q.b === old.b);
        state.quick = { ...q, score: old.score };
        save();
        renderQuick();
      });
      const STORIES = [
        [
          "לְשָׁקֵד יֵשׁ {a} חֲבִילוֹת צְבָעִים. בְּכָל חֲבִילָה יֵשׁ {b} צְבָעִים. כַּמָּה צְבָעִים יֵשׁ בְּסַךְ הַכֹּל?",
          4,
          6,
        ],
        [
          "אִמָּא קָנְתָה {a} שַׂקִּיּוֹת תַּפּוּחִים. בְּכָל שַׂקִּית יֵשׁ {b} תַּפּוּחִים. כַּמָּה תַּפּוּחִים קָנְתָה אִמָּא?",
          7,
          3,
        ],
        [
          "בַּגִּנָּה יֵשׁ {a} שׁוּרוֹת שֶׁל פְּרָחִים. בְּכָל שׁוּרָה יֵשׁ {b} פְּרָחִים. כַּמָּה פְּרָחִים יֵשׁ בַּגִּנָּה?",
          5,
          8,
        ],
        [
          "עַל הַשֻּׁלְחָן יֵשׁ {a} צַלָּחוֹת. בְּכָל צַלַּחַת יֵשׁ {b} עוּגִיּוֹת. כַּמָּה עוּגִיּוֹת יֵשׁ בְּסַךְ הַכֹּל?",
          3,
          7,
        ],
        [
          "לְשָׁקֵד יֵשׁ {a} דַּפִּים. עַל כָּל דַּף הוּא מַדְבִּיק {b} מַדְבֵּקוֹת. בְּכַמָּה מַדְבֵּקוֹת הוּא מִשְׁתַּמֵּשׁ?",
          6,
          4,
        ],
        [
          "בָּאוּלָם יֵשׁ {a} שׁוּרוֹת. בְּכָל שׁוּרָה יֵשׁ {b} כִּסְאוֹת. כַּמָּה כִּסְאוֹת יֵשׁ בָּאוּלָם?",
          8,
          9,
        ],
        [
          "בְּכָל קֻפְסָה יֵשׁ {b} קֻבִּיּוֹת. לְשָׁקֵד יֵשׁ {a} קֻפְסָאוֹת. כַּמָּה קֻבִּיּוֹת יֵשׁ לוֹ?",
          9,
          5,
        ],
        [
          "עַל כָּל מַדָּף יֵשׁ {b} סְפָרִים. בַּסִּפְרִיָּה יֵשׁ {a} מַדָּפִים כָּאֵלֶּה. כַּמָּה סְפָרִים יֵשׁ עַל הַמַּדָּפִים?",
          10,
          8,
        ],
        [
          "בַּחֲנָיָה יֵשׁ {a} מְכוֹנִיּוֹת. לְכָל מְכוֹנִית יֵשׁ {b} גַּלְגַּלִּים. כַּמָּה גַּלְגַּלִּים יֵשׁ לְכָל הַמְּכוֹנִיּוֹת יַחַד?",
          7,
          4,
        ],
        [
          "שָׁקֵד מֵכִין {a} שַׂקִּיּוֹת הַפְתָּעָה. בְּכָל שַׂקִּית יֵשׁ {b} סֻכָּרִיּוֹת. כַּמָּה סֻכָּרִיּוֹת צָרִיךְ לַהֲכָנַת הַשַּׂקִּיּוֹת?",
          6,
          6,
        ],
        [
          "בַּחֲצַר יֵשׁ {a} יְלָדִים. כָּל יֶלֶד מְקַבֵּל {b} בָּלוֹנִים. כַּמָּה בָּלוֹנִים מְקַבְּלִים כֻּלָּם יַחַד?",
          8,
          2,
        ],
        [
          "בְּכָל חֲבִילָה יֵשׁ {b} קְלָפִים. שָׁקֵד פּוֹתֵחַ {a} חֲבִילוֹת. כַּמָּה קְלָפִים יֵשׁ לוֹ?",
          10,
          10,
        ],
      ];
      function renderWords() {
        const i = state.wordIndex,
          [text, a, b] = STORIES[i];
        $("word-question").innerHTML = text.replace("{a}", numHTML(a)).replace("{b}", numHTML(b));
        $("word-number").textContent = `${i + 1} / ${STORIES.length}`;
        $("word-score").textContent = state.wordSolved.filter(Boolean).length * 10;
        $("word-answer").value = state.wordInputs[i];
        $("word-answer").disabled = state.wordSolved[i];
        $("word-submit").disabled = state.wordSolved[i];
        status(
          "word-status",
          state.wordSolved[i] ? "כָּל הַכָּבוֹד! פָּתַרְנוּ אֶת הַסִּפּוּר." : "",
          state.wordSolved[i] ? "success" : "",
        );
      }
      $("word-answer").addEventListener("input", (event) => {
        state.wordInputs[state.wordIndex] = event.target.value;
        save();
      });
      $("word-form").addEventListener("submit", (event) => {
        event.preventDefault();
        const i = state.wordIndex;
        if (state.wordSolved[i]) return;
        const ans = parseAnswer($("word-answer").value);
        if (ans === null) {
          status("word-status", "נַקְלִיד מִסְפָּר שָׁלֵם כְּדֵי לִבְדֹּק.", "warning");
          return;
        }
        state.wordTries[i]++;
        if (ans === STORIES[i][1] * STORIES[i][2]) {
          state.wordSolved[i] = true;
          save();
          renderWords();
          fireworks();
        } else {
          save();
          status(
            "word-status",
            "נְנַסֶּה שׁוּב: כַּמָּה קְבוּצוֹת יֵשׁ, וְכַמָּה פְּרִיטִים בְּכָל קְבוּצָה?",
            "error",
          );
        }
      });
      $("word-next").addEventListener("click", () => {
        state.wordIndex = (state.wordIndex + 1) % STORIES.length;
        save();
        renderWords();
      });
      // Generate a connected maze with a carved path between all odd-coordinate cells.
      // Each question stage has its own reachable flag. A question locks movement
      // after exactly three valid moves; wall presses do not count.
      function makeMaze() {
        const grid = Array.from({ length: 9 }, () => Array(9).fill(1));
        const stack = [[1, 1]];
        grid[1][1] = 0;
        while (stack.length) {
          const [x, y] = stack[stack.length - 1],
            options = [
              [2, 0],
              [-2, 0],
              [0, 2],
              [0, -2],
            ].filter(
              ([dx, dy]) =>
                x + dx > 0 && x + dx < 8 && y + dy > 0 && y + dy < 8 && grid[y + dy][x + dx] === 1,
            );
          if (!options.length) {
            stack.pop();
            continue;
          }
          const [dx, dy] = options[randomInt(0, options.length - 1)];
          grid[y + dy / 2][x + dx / 2] = 0;
          grid[y + dy][x + dx] = 0;
          stack.push([x + dx, y + dy]);
        }
        const distances = Array.from({ length: 9 }, () => Array(9).fill(-1)),
          queue = [[1, 1]];
        distances[1][1] = 0;
        let goal = { x: 1, y: 1 };
        for (let i = 0; i < queue.length; i++) {
          const [x, y] = queue[i];
          if (distances[y][x] > distances[goal.y][goal.x]) goal = { x, y };
          for (const [dx, dy] of [
            [1, 0],
            [-1, 0],
            [0, 1],
            [0, -1],
          ]) {
            const nx = x + dx,
              ny = y + dy;
            if (
              nx >= 0 &&
              nx < 9 &&
              ny >= 0 &&
              ny < 9 &&
              !grid[ny][nx] &&
              distances[ny][nx] === -1
            ) {
              distances[ny][nx] = distances[y][x] + 1;
              queue.push([nx, ny]);
            }
          }
        }
        return { grid, goal };
      }
      function mazeQuestion(level) {
        return level === 0
          ? newQuestion(1, 5)
          : level === 1
            ? newQuestion(2, 10)
            : newQuestion(6, 10);
      }
      function startMaze(level) {
        if (!Number.isInteger(level) || level < 0 || level > state.unlocked) return;
        const { grid, goal } = makeMaze();
        state.maze = {
          level,
          grid,
          goal,
          x: 1,
          y: 1,
          visited: Array(81).fill(false),
          lives: 3,
          completed: 0,
          firstCorrect: 0,
          score: 0,
          moves: 0,
          pending: false,
          question: mazeQuestion(level),
          status: "playing",
        };
        state.maze.visited[10] = true;
        restartPending = false;
        status("maze-status", "מוּכָנִים? מִתְקַדְּמִים עִם הַחִצִּים!");
        save();
        renderMaze();
      }
      function renderLevels() {
        const container = $("levels");
        container.replaceChildren();
        for (let level = 0; level < 3; level++) {
          const button = document.createElement("button");
          button.className = "level" + (state.maze && state.maze.level === level ? " active" : "");
          button.disabled = level > state.unlocked;
          button.dataset.level = level;
          button.innerHTML = `<strong>${button.disabled ? "🔒 " : ""}רָמָה ${LEVEL_NAMES[level]}</strong><small>${numHTML(TOTALS[level])} שְׁלָבִים${state.best[level] ? " · " + percentHTML(state.best[level]) : ""}</small>`;
          button.setAttribute("aria-pressed", String(!!state.maze && state.maze.level === level));
          button.addEventListener("click", () => {
            if (state.maze && state.maze.level === level) return;
            startMaze(level);
          });
          container.append(button);
        }
      }
      function renderMaze() {
        const m = state.maze;
        if (!m) return;
        renderLevels();
        $("maze-stage").innerHTML =
          `רָמָה ${LEVEL_NAMES[m.level]} · שָׁלָב ${ratioHTML(Math.min(m.completed + 1, TOTALS[m.level]), TOTALS[m.level])}`;
        $("maze-hearts").textContent = "❤️".repeat(m.lives) + "🤍".repeat(3 - m.lives);
        $("maze-hearts").setAttribute("aria-label", `נוֹתְרוּ ${m.lives} לְבָבוֹת`);
        $("maze-score").textContent = m.score;
        $("maze-progress").setAttribute("aria-valuemax", TOTALS[m.level]);
        $("maze-progress").setAttribute("aria-valuenow", m.completed);
        $("maze-progress-fill").style.width = (m.completed / TOTALS[m.level]) * 100 + "%";
        const board = $("maze-board");
        board.replaceChildren();
        for (let y = 0; y < 9; y++)
          for (let x = 0; x < 9; x++) {
            const cell = document.createElement("div");
            cell.className = "maze-cell";
            cell.dataset.x = x;
            cell.dataset.y = y;
            if (m.grid[y][x]) cell.classList.add("wall");
            if (m.visited[y * 9 + x]) cell.classList.add("visited");
            if (x === m.goal.x && y === m.goal.y) {
              cell.classList.add("goal");
              cell.textContent = "🚩";
            }
            if (x === m.x && y === m.y) {
              cell.classList.add("player");
              cell.textContent = "🧒";
            }
            board.append(cell);
          }
        board.setAttribute(
          "aria-label",
          `מַפַּת הַמָּבוֹךְ. הַשַּׂחְקָן בְּשׁוּרָה ${m.y}, עַמּוּדָה ${m.x}.`,
        );
        $("maze-caption").innerHTML =
          m.completed >= TOTALS[m.level]
            ? "כָּל הַשְּׁאֵלוֹת נִפְתְּרוּ. עַכְשָׁו מַגִּיעִים לַדֶּגֶל!"
            : `צְעָדִים עַד לַשְּׁאֵלָה הַבָּאָה: ${numHTML(3 - m.moves)} · לְחִיצָה עַל עֵץ לֹא נִסְפֶּרֶת.`;
        $("maze-question").hidden = !m.pending || m.status !== "playing";
        $("maze-end").hidden = m.status === "playing";
        document
          .querySelectorAll("[data-move]")
          .forEach((button) => (button.disabled = m.pending || m.status !== "playing"));
        $("maze-restart").textContent = restartPending
          ? "לְהַתְחִיל מֵחָדָשׁ? לְחִיצָה נוֹסֶפֶת לְאִשּׁוּר"
          : "הַתְחָלַת הָרָמָה מֵחָדָשׁ ↻";
        if (m.pending) {
          $("maze-exercise").textContent = `${m.question.a} × ${m.question.b} = ?`;
          $("maze-answer").value = m.question.input || "";
          status(
            "maze-answer-status",
            m.question.tries ? "נְנַסֶּה שׁוּב. יֵשׁ לָנוּ עוֹד הִזְדַּמְּנוּת!" : "",
            m.question.tries ? "error" : "",
          );
        }
        if (m.status !== "playing") renderMazeEnd();
        resizeFrame();
      }
      function move(direction) {
        const m = state.maze;
        if (!m || page !== "maze" || m.pending || m.status !== "playing") return;
        const delta = { up: [0, -1], down: [0, 1], left: [-1, 0], right: [1, 0] }[direction];
        if (!delta) return;
        const nx = m.x + delta[0],
          ny = m.y + delta[1];
        if (nx < 0 || nx >= 9 || ny < 0 || ny >= 9 || m.grid[ny][nx]) {
          status("maze-status", "כָּאן יֵשׁ עֵץ 🌲. נִבְחַר כִּוּוּן אַחֵר.");
          return;
        }
        m.x = nx;
        m.y = ny;
        m.visited[ny * 9 + nx] = true;
        restartPending = false;
        if (m.completed < TOTALS[m.level]) {
          m.moves++;
          if (m.moves === 3) {
            m.pending = true;
            m.question = mazeQuestion(m.level);
          }
        }
        status(
          "maze-status",
          m.x === m.goal.x && m.y === m.goal.y && m.completed < TOTALS[m.level]
            ? "הִגַּעְנוּ לַדֶּגֶל! נַמְשִׁיךְ לְטַיֵּל וּלְהַשְׁלִים אֶת הַשְּׁאֵלוֹת."
            : "",
        );
        maybeFinishMaze();
        save();
        renderMaze();
        if (m.pending) {
          $("maze-question").scrollIntoView({ block: "center", behavior: "instant" });
          $("maze-answer").focus({ preventScroll: true });
        }
      }
      document
        .querySelectorAll("[data-move]")
        .forEach((button) => button.addEventListener("click", () => move(button.dataset.move)));
      document.addEventListener("keydown", (event) => {
        if (
          page !== "maze" ||
          event.target.matches("input,textarea") ||
          event.altKey ||
          event.ctrlKey ||
          event.metaKey
        )
          return;
        const direction = {
          ArrowUp: "up",
          ArrowDown: "down",
          ArrowLeft: "left",
          ArrowRight: "right",
        }[event.key];
        if (direction) {
          event.preventDefault();
          move(direction);
        }
      });
      $("maze-answer").addEventListener("input", (event) => {
        if (state.maze && state.maze.pending) {
          state.maze.question.input = event.target.value;
          save();
        }
      });
      $("maze-form").addEventListener("submit", (event) => {
        event.preventDefault();
        const m = state.maze;
        if (!m || !m.pending || m.status !== "playing") return;
        const ans = parseAnswer($("maze-answer").value);
        if (ans === null) {
          status(
            "maze-answer-status",
            "נַקְלִיד מִסְפָּר שָׁלֵם. הַלְּבָבוֹת לֹא יֵרְדוּ.",
            "warning",
          );
          return;
        }
        if (ans === m.question.a * m.question.b) {
          if (m.question.tries === 0) m.firstCorrect++;
          m.score += m.question.tries === 0 ? 10 : 5;
          m.completed++;
          m.pending = false;
          m.moves = 0;
          status("maze-status", "נָכוֹן! עוֹד שְׁלָב הֻשְׁלַם. מַמְשִׁיכִים! ⭐", "success");
          maybeFinishMaze();
          save();
          renderMaze();
          $("maze-answer").blur();
        } else {
          m.question.tries++;
          m.lives--;
          if (m.lives === 0) {
            m.status = "lost";
            m.pending = false;
          }
          save();
          renderMaze();
          if (m.status === "playing") {
            $("maze-answer").select();
            status(
              "maze-answer-status",
              `לֹא נוֹרָא! נוֹתְרוּ ${m.lives} לְבָבוֹת. נְנַסֶּה שׁוּב.`,
              "error",
            );
          } else $("maze-end").scrollIntoView({ block: "center", behavior: "instant" });
        }
      });
      function maybeFinishMaze() {
        const m = state.maze;
        if (
          m.status !== "playing" ||
          m.pending ||
          m.completed < TOTALS[m.level] ||
          m.x !== m.goal.x ||
          m.y !== m.goal.y
        )
          return;
        const percent = Math.round((m.firstCorrect / TOTALS[m.level]) * 100);
        m.status = percent >= 80 ? "passed" : "retry";
        state.best[m.level] = Math.max(state.best[m.level], percent);
        if (m.status === "passed") {
          state.unlocked = Math.max(state.unlocked, Math.min(2, m.level + 1));
          fireworks();
        }
      }
      function renderMazeEnd() {
        const m = state.maze,
          box = $("maze-end-content"),
          percent = Math.round((m.firstCorrect / TOTALS[m.level]) * 100);
        box.replaceChildren();
        if (m.status === "lost") {
          box.innerHTML =
            '<div class="dragon-stage" aria-hidden="true"><span class="kid">🧒</span><span class="dragon">🐉</span></div><h3>הַדְּרָקוֹן הַשּׁוֹבָב הִגִּיעַ!</h3><p>הוּא לָקַח אֶת הַשַּׂחְקָן לַהַתְחָלָה. לֹא נוֹרָא — בַּנִּסָּיוֹן הַבָּא נַצְלִיחַ יוֹתֵר!</p>';
        } else if (m.status === "passed") {
          box.innerHTML = `<div class="end-icon" aria-hidden="true">🏆</div><h3>${m.level === 2 ? "סִיַּמְנוּ אֶת כָּל הָרָמוֹת!" : "רָמָה " + LEVEL_NAMES[m.level] + " הֻשְׁלְמָה!"}</h3><p>${percentHTML(percent)} הַצְלָחָה בַּנִּסָּיוֹן הָרִאשׁוֹן · ${numHTML(m.score)} נְקֻדּוֹת.</p>`;
          if (m.level < 2) {
            const next = document.createElement("button");
            next.className = "btn";
            next.textContent = "לָרָמָה הַבָּאָה ←";
            next.addEventListener("click", () => startMaze(m.level + 1));
            box.append(next);
          }
        } else {
          box.innerHTML = `<div class="end-icon" aria-hidden="true">🌱</div><h3>הִגַּעְנוּ לַסּוֹף!</h3><p>הַצְלָחָה בַּנִּסָּיוֹן הָרִאשׁוֹן: ${percentHTML(percent)}. נְנַסֶּה שׁוּב כְּדֵי לְהַגִּיעַ לְ־<bdi>80%</bdi> וְלִפְתֹּחַ אֶת הָרָמָה הַבָּאָה.</p>`;
        }
        const again = document.createElement("button");
        again.className = "btn secondary";
        again.textContent =
          m.status === "passed"
            ? "שׁוּב בְּאוֹתָהּ רָמָה"
            : "נִסָּיוֹן חָדָשׁ · שְׁלוֹשָׁה לְבָבוֹת ❤️";
        again.addEventListener("click", () => startMaze(m.level));
        box.append(again);
      }
      $("maze-restart").addEventListener("click", () => {
        if (!state.maze) return;
        if (restartPending || state.maze.status !== "playing") {
          startMaze(state.maze.level);
        } else {
          restartPending = true;
          $("maze-restart").textContent = "לְהַתְחִיל מֵחָדָשׁ? לְחִיצָה נוֹסֶפֶת לְאִשּׁוּר";
          resizeFrame();
        }
      });
      createTable();
      renderQuick();
      renderWords();
      save();
      message("streamlit:componentReady", { apiVersion: 1 });
      if ("ResizeObserver" in window) new ResizeObserver(resizeFrame).observe($("app"));
      window.addEventListener("resize", resizeFrame);
      window.addEventListener("pagehide", save);
      resizeFrame();
    </script>
  </body>
</html>
'''

@st.cache_resource
def _frontend_directory(html: str):
    # A stable directory for this server process; no writes into the git repo.
    directory = Path(tempfile.mkdtemp(prefix="shaked_multiplication_"))
    (directory / "index.html").write_text(html, encoding="utf-8")
    return str(directory)

playground = components.declare_component(
    "shaked_multiplication", path=_frontend_directory(APP_HTML)
)
playground(key="shaked_playground", default=None)
