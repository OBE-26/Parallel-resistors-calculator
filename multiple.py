"""Personal multiplication game for Shaked, version 5.
Run with: streamlit run multiple.py
All progress stays in the current browser; there are no accounts or database settings.
"""
from pathlib import Path
import tempfile
import streamlit as st
import streamlit.components.v1 as components

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


.session-heading{display:flex;flex-wrap:wrap;justify-content:space-between;align-items:center;gap:12px;margin-bottom:14px}.quiz-meta{font-size:15px;color:var(--muted);line-height:1.8}.quiz-progress{height:7px;background:#e5eae0;border-radius:7px;overflow:hidden;direction:ltr;margin:14px 0}.quiz-progress>div{height:100%;background:var(--green);transition:width .2s}.revealed-answer{background:#fff1ca;border:1px solid #efd18f;border-radius:14px;padding:14px;margin-top:15px;line-height:1.8}.revealed-answer .math{margin:6px 0!important}.result-card{padding:16px;background:#edf4e9;border-radius:15px;margin-top:16px}.result-card .result-number{font-size:42px;font-weight:700;color:var(--green);display:block;direction:ltr;text-align:left}.result-card p{margin:8px 0 12px}.busy button[data-move]{opacity:.55}.table-panel .toolbar{direction:ltr}.table-panel .toolbar>div,.table-panel .toolbar>button{direction:rtl}.draft-note{font-size:12px;color:var(--muted);min-height:18px;margin-top:8px}.start-prompt{padding:22px;border:1px dashed #9fbdab;border-radius:16px;margin-top:16px;line-height:1.8}.section-error{margin-bottom:14px}.quiz-card .word-question{margin:16px 0}.quiz-card .math{margin:18px 0}.quiz-end-actions{display:flex;gap:10px;flex-wrap:wrap}.quiz-end-actions .btn{flex:1}.score-aside{font-size:13px;line-height:1.8;color:var(--muted)}
@media(max-width:480px){.session-heading{gap:8px}.quiz-card{padding:15px}.result-card .result-number{font-size:36px}}
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
      <p id="storage-note" class="status warning" hidden role="status">הַדַּפְדְּפָן לֹא מְאַפְשֵׁר שְׁמִירָה. אֶפְשָׁר לְשַׂחֵק, אֲבָל הַהִתְקַדְּמוּת לֹא תִּשָּׁמֵר אַחֲרֵי סְגִירַת הַדַּף.</p><div id="global-status" class="status section-error" role="status"></div>
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
              רָמוֹת וּשְׁלוֹשָׁה נִסְיוֹנוֹת לְכָל שְׁאֵלָה!
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
          <div id="table-draft-note" class="draft-note" role="status"></div><div class="status" id="table-status" role="status" aria-live="polite"></div>
        </div>
      </section>
<section class="page" id="page-quick" hidden aria-labelledby="quick-title"><div class="page-heading"><span class="tag">עֶשְׂרִים צְעָדִים שֶׁל הַצְלָחָה</span><h2 id="quick-title">תִּרְגּוּל מָהִיר</h2><p>בְּכָל רָמָה <bdi>20</bdi> שְׁאֵלוֹת. עוֹנִים נָכוֹן וּמַמְשִׁיכִים, בַּקֶּצֶב שֶׁלָּנוּ.</p></div>
    <div class="levels" id="quick-levels"></div>
    <div class="start-prompt" id="quick-start">בּוֹחֲרִים רָמָה פְּתוּחָה וּמַתְחִילִים סֶבֶב שֶׁל <bdi>20</bdi> שְׁאֵלוֹת.</div>
    <div class="panel quiz-card" id="quick-card" hidden><div class="session-heading"><span class="quiz-meta" id="quick-progress-label"></span><span class="score-pill">נָכוֹן בַּפַּעַם הָרִאשׁוֹנָה <bdi id="quick-first">0</bdi></span></div>
    <div class="quiz-progress"><div id="quick-progress-fill"></div></div><div id="quick-question-area"><div class="math" id="quick-exercise"></div>
    <form class="answer-form" id="quick-form" novalidate><label for="quick-answer">הַתְּשׁוּבָה שֶׁלָּנוּ</label><div class="answer-line"><input id="quick-answer" class="numeric" type="text" inputmode="numeric" pattern="[0-9]*" maxlength="3" dir="ltr" autocomplete="off"><button class="btn" id="quick-submit" type="submit">בְּדִיקָה</button></div></form>
    <div class="status" id="quick-status" role="status"></div><div class="revealed-answer" id="quick-reveal" hidden><strong>נִלְמַד יַחַד אֶת הַתְּשׁוּבָה:</strong><div class="math" id="quick-solution"></div><span>נַקְלִיד אֶת הַתְּשׁוּבָה הַנְּכוֹנָה בַּשָּׂדֶה כְּדֵי לְהַמְשִׁיךְ.</span></div>
    <div class="actions"><button class="btn secondary" id="quick-next" disabled>לַשְּׁאֵלָה הַבָּאָה ←</button></div></div><div id="quick-result" class="result-card" hidden></div></div>
    </section><section class="page" id="page-words" hidden aria-labelledby="words-title"><div class="page-heading"><span class="tag">מָאתַיִם סִפּוּרִים, שָׁלוֹשׁ רָמוֹת</span><h2 id="words-title">שְׁאֵלוֹת מִלּוּלִיּוֹת</h2><p>בְּכָל רָמָה <bdi>20</bdi> שְׁאֵלוֹת. עוֹנִים נָכוֹן וּמַמְשִׁיכִים, בַּקֶּצֶב שֶׁלָּנוּ.</p></div>
    <div class="levels" id="words-levels"></div>
    <div class="start-prompt" id="words-start">בּוֹחֲרִים רָמָה פְּתוּחָה וּמַתְחִילִים סֶבֶב שֶׁל <bdi>20</bdi> שְׁאֵלוֹת.</div>
    <div class="panel quiz-card" id="words-card" hidden><div class="session-heading"><span class="quiz-meta" id="words-progress-label"></span><span class="score-pill">נָכוֹן בַּפַּעַם הָרִאשׁוֹנָה <bdi id="words-first">0</bdi></span></div>
    <div class="quiz-progress"><div id="words-progress-fill"></div></div><div id="words-question-area"><p class="word-question" id="words-question"></p>
    <form class="answer-form" id="words-form" novalidate><label for="words-answer">הַתְּשׁוּבָה שֶׁלָּנוּ</label><div class="answer-line"><input id="words-answer" class="numeric" type="text" inputmode="numeric" pattern="[0-9]*" maxlength="3" dir="ltr" autocomplete="off"><button class="btn" id="words-submit" type="submit">בְּדִיקָה</button></div></form>
    <div class="status" id="words-status" role="status"></div><div class="revealed-answer" id="words-reveal" hidden><strong>נִלְמַד יַחַד אֶת הַתְּשׁוּבָה:</strong><div class="math" id="words-solution"></div><span>נַקְלִיד אֶת הַתְּשׁוּבָה הַנְּכוֹנָה בַּשָּׂדֶה כְּדֵי לְהַמְשִׁיךְ.</span></div>
    <div class="actions"><button class="btn secondary" id="words-next" disabled>לַשְּׁאֵלָה הַבָּאָה ←</button></div></div><div id="words-result" class="result-card" hidden></div></div>
    </section>      <section id="page-maze" class="page" hidden aria-labelledby="maze-title">
        <div class="page-heading">
          <span class="tag">הַרְפַּתְקָה בֵּין הָעֵצִים</span>
          <h2 id="maze-title">הַמָּבוֹךְ הַקָּסוּם</h2>
          <p>כָּל שְׁלוֹשָׁה צְעָדִים — שְׁאֵלַת כֶּפֶל. פּוֹתְרִים וּמַמְשִׁיכִים לַדֶּגֶל!</p>
        </div>
        <div class="levels" id="levels" aria-label="רָמוֹת הַמִּשְׂחָק"></div>
        <div class="start-prompt" id="maze-start">בּוֹחֲרִים רָמָה וְיוֹצְאִים לַהַרְפַּתְקָה!</div><div class="panel maze-panel" id="maze-panel" hidden>
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
                    <div id="maze-reveal" hidden><p class="subtle" style="margin:8px 0 12px">מַמְשִׁיכִים לַהַרְפַּתְקָה! הַשְּׁאֵלָה הַזֹּאת לֹא מוֹסִיפָה נְקֻדּוֹת.</p><button class="btn" id="maze-continue" type="button">מַמְשִׁיכִים ←</button></div>
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
<footer class="footer">נבנה באהבה לשקד בן עזרא</footer>
    </main>
    <div class="fireworks" id="fireworks" aria-hidden="true"></div>

<script>
const WORD_BANK = [{"id":"w001","level":0,"text":"יֵשׁ 2 שַׂקִּיּוֹת. בְּכָל שַׂקִּית 2 תַּפּוּחִים. כַּמָּה תַּפּוּחִים יֵשׁ בְּסַךְ הַכֹּל?","a":2,"b":2},{"id":"w002","level":0,"text":"יֵשׁ 2 שַׂקִּיּוֹת. בְּכָל שַׂקִּית 5 תַּפּוּחִים. כַּמָּה תַּפּוּחִים יֵשׁ בְּסַךְ הַכֹּל?","a":2,"b":5},{"id":"w003","level":0,"text":"יֵשׁ 3 שַׂקִּיּוֹת. בְּכָל שַׂקִּית 4 תַּפּוּחִים. כַּמָּה תַּפּוּחִים יֵשׁ בְּסַךְ הַכֹּל?","a":3,"b":4},{"id":"w004","level":0,"text":"יֵשׁ 4 שַׂקִּיּוֹת. בְּכָל שַׂקִּית 3 תַּפּוּחִים. כַּמָּה תַּפּוּחִים יֵשׁ בְּסַךְ הַכֹּל?","a":4,"b":3},{"id":"w005","level":0,"text":"יֵשׁ 5 שַׂקִּיּוֹת. בְּכָל שַׂקִּית 2 תַּפּוּחִים. כַּמָּה תַּפּוּחִים יֵשׁ בְּסַךְ הַכֹּל?","a":5,"b":2},{"id":"w006","level":0,"text":"עַל הַשֻּׁלְחָן 3 צַלָּחוֹת. בְּכָל צַלַּחַת 5 עוּגִיּוֹת. כַּמָּה עוּגִיּוֹת יֵשׁ בְּסַךְ הַכֹּל?","a":3,"b":5},{"id":"w007","level":0,"text":"עַל הַשֻּׁלְחָן 4 צַלָּחוֹת. בְּכָל צַלַּחַת 4 עוּגִיּוֹת. כַּמָּה עוּגִיּוֹת יֵשׁ בְּסַךְ הַכֹּל?","a":4,"b":4},{"id":"w008","level":0,"text":"עַל הַשֻּׁלְחָן 5 צַלָּחוֹת. בְּכָל צַלַּחַת 3 עוּגִיּוֹת. כַּמָּה עוּגִיּוֹת יֵשׁ בְּסַךְ הַכֹּל?","a":5,"b":3},{"id":"w009","level":0,"text":"עַל הַשֻּׁלְחָן 2 צַלָּחוֹת. בְּכָל צַלַּחַת 2 עוּגִיּוֹת. כַּמָּה עוּגִיּוֹת יֵשׁ בְּסַךְ הַכֹּל?","a":2,"b":2},{"id":"w010","level":0,"text":"עַל הַשֻּׁלְחָן 2 צַלָּחוֹת. בְּכָל צַלַּחַת 5 עוּגִיּוֹת. כַּמָּה עוּגִיּוֹת יֵשׁ בְּסַךְ הַכֹּל?","a":2,"b":5},{"id":"w011","level":0,"text":"בַּגִּנָּה 5 שׁוּרוֹת. בְּכָל שׁוּרָה 4 פְּרָחִים. כַּמָּה פְּרָחִים יֵשׁ בַּגִּנָּה?","a":5,"b":4},{"id":"w012","level":0,"text":"בַּגִּנָּה 2 שׁוּרוֹת. בְּכָל שׁוּרָה 3 פְּרָחִים. כַּמָּה פְּרָחִים יֵשׁ בַּגִּנָּה?","a":2,"b":3},{"id":"w013","level":0,"text":"בַּגִּנָּה 3 שׁוּרוֹת. בְּכָל שׁוּרָה 2 פְּרָחִים. כַּמָּה פְּרָחִים יֵשׁ בַּגִּנָּה?","a":3,"b":2},{"id":"w014","level":0,"text":"בַּגִּנָּה 3 שׁוּרוֹת. בְּכָל שׁוּרָה 5 פְּרָחִים. כַּמָּה פְּרָחִים יֵשׁ בַּגִּנָּה?","a":3,"b":5},{"id":"w015","level":0,"text":"בַּגִּנָּה 4 שׁוּרוֹת. בְּכָל שׁוּרָה 4 פְּרָחִים. כַּמָּה פְּרָחִים יֵשׁ בַּגִּנָּה?","a":4,"b":4},{"id":"w016","level":0,"text":"יֵשׁ 3 קֻפְסָאוֹת. בְּכָל קֻפְסָה 3 עֶפְרוֹנוֹת. כַּמָּה עֶפְרוֹנוֹת יֵשׁ בְּסַךְ הַכֹּל?","a":3,"b":3},{"id":"w017","level":0,"text":"יֵשׁ 4 קֻפְסָאוֹת. בְּכָל קֻפְסָה 2 עֶפְרוֹנוֹת. כַּמָּה עֶפְרוֹנוֹת יֵשׁ בְּסַךְ הַכֹּל?","a":4,"b":2},{"id":"w018","level":0,"text":"יֵשׁ 4 קֻפְסָאוֹת. בְּכָל קֻפְסָה 5 עֶפְרוֹנוֹת. כַּמָּה עֶפְרוֹנוֹת יֵשׁ בְּסַךְ הַכֹּל?","a":4,"b":5},{"id":"w019","level":0,"text":"יֵשׁ 5 קֻפְסָאוֹת. בְּכָל קֻפְסָה 4 עֶפְרוֹנוֹת. כַּמָּה עֶפְרוֹנוֹת יֵשׁ בְּסַךְ הַכֹּל?","a":5,"b":4},{"id":"w020","level":0,"text":"יֵשׁ 2 קֻפְסָאוֹת. בְּכָל קֻפְסָה 3 עֶפְרוֹנוֹת. כַּמָּה עֶפְרוֹנוֹת יֵשׁ בְּסַךְ הַכֹּל?","a":2,"b":3},{"id":"w021","level":0,"text":"יֵשׁ 5 יְלָדִים. כָּל יֶלֶד מְקַבֵּל 2 בָּלוֹנִים. כַּמָּה בָּלוֹנִים צָרִיךְ לְכֻלָּם?","a":5,"b":2},{"id":"w022","level":0,"text":"יֵשׁ 5 יְלָדִים. כָּל יֶלֶד מְקַבֵּל 5 בָּלוֹנִים. כַּמָּה בָּלוֹנִים צָרִיךְ לְכֻלָּם?","a":5,"b":5},{"id":"w023","level":0,"text":"יֵשׁ 2 יְלָדִים. כָּל יֶלֶד מְקַבֵּל 4 בָּלוֹנִים. כַּמָּה בָּלוֹנִים צָרִיךְ לְכֻלָּם?","a":2,"b":4},{"id":"w024","level":0,"text":"יֵשׁ 3 יְלָדִים. כָּל יֶלֶד מְקַבֵּל 3 בָּלוֹנִים. כַּמָּה בָּלוֹנִים צָרִיךְ לְכֻלָּם?","a":3,"b":3},{"id":"w025","level":0,"text":"יֵשׁ 4 יְלָדִים. כָּל יֶלֶד מְקַבֵּל 2 בָּלוֹנִים. כַּמָּה בָּלוֹנִים צָרִיךְ לְכֻלָּם?","a":4,"b":2},{"id":"w026","level":0,"text":"בַּסַּל 2 חֲבִילוֹת. בְּכָל חֲבִילָה 5 לַחְמָנִיּוֹת. כַּמָּה לַחְמָנִיּוֹת יֵשׁ בַּסַּל?","a":2,"b":5},{"id":"w027","level":0,"text":"בַּסַּל 3 חֲבִילוֹת. בְּכָל חֲבִילָה 4 לַחְמָנִיּוֹת. כַּמָּה לַחְמָנִיּוֹת יֵשׁ בַּסַּל?","a":3,"b":4},{"id":"w028","level":0,"text":"בַּסַּל 4 חֲבִילוֹת. בְּכָל חֲבִילָה 3 לַחְמָנִיּוֹת. כַּמָּה לַחְמָנִיּוֹת יֵשׁ בַּסַּל?","a":4,"b":3},{"id":"w029","level":0,"text":"בַּסַּל 5 חֲבִילוֹת. בְּכָל חֲבִילָה 2 לַחְמָנִיּוֹת. כַּמָּה לַחְמָנִיּוֹת יֵשׁ בַּסַּל?","a":5,"b":2},{"id":"w030","level":0,"text":"בַּסַּל 5 חֲבִילוֹת. בְּכָל חֲבִילָה 5 לַחְמָנִיּוֹת. כַּמָּה לַחְמָנִיּוֹת יֵשׁ בַּסַּל?","a":5,"b":5},{"id":"w031","level":0,"text":"יֵשׁ 4 דַּפִּים. עַל כָּל דַּף 4 מַדְבֵּקוֹת. כַּמָּה מַדְבֵּקוֹת יֵשׁ בְּסַךְ הַכֹּל?","a":4,"b":4},{"id":"w032","level":0,"text":"יֵשׁ 5 דַּפִּים. עַל כָּל דַּף 3 מַדְבֵּקוֹת. כַּמָּה מַדְבֵּקוֹת יֵשׁ בְּסַךְ הַכֹּל?","a":5,"b":3},{"id":"w033","level":0,"text":"יֵשׁ 2 דַּפִּים. עַל כָּל דַּף 2 מַדְבֵּקוֹת. כַּמָּה מַדְבֵּקוֹת יֵשׁ בְּסַךְ הַכֹּל?","a":2,"b":2},{"id":"w034","level":0,"text":"יֵשׁ 2 דַּפִּים. עַל כָּל דַּף 5 מַדְבֵּקוֹת. כַּמָּה מַדְבֵּקוֹת יֵשׁ בְּסַךְ הַכֹּל?","a":2,"b":5},{"id":"w035","level":0,"text":"יֵשׁ 3 דַּפִּים. עַל כָּל דַּף 4 מַדְבֵּקוֹת. כַּמָּה מַדְבֵּקוֹת יֵשׁ בְּסַךְ הַכֹּל?","a":3,"b":4},{"id":"w036","level":0,"text":"יֵשׁ 2 סַלִּים. בְּכָל סַל 3 כַּדּוּרִים. כַּמָּה כַּדּוּרִים יֵשׁ בְּכָל הַסַּלִּים יַחַד?","a":2,"b":3},{"id":"w037","level":0,"text":"יֵשׁ 3 סַלִּים. בְּכָל סַל 2 כַּדּוּרִים. כַּמָּה כַּדּוּרִים יֵשׁ בְּכָל הַסַּלִּים יַחַד?","a":3,"b":2},{"id":"w038","level":0,"text":"יֵשׁ 3 סַלִּים. בְּכָל סַל 5 כַּדּוּרִים. כַּמָּה כַּדּוּרִים יֵשׁ בְּכָל הַסַּלִּים יַחַד?","a":3,"b":5},{"id":"w039","level":0,"text":"יֵשׁ 4 סַלִּים. בְּכָל סַל 4 כַּדּוּרִים. כַּמָּה כַּדּוּרִים יֵשׁ בְּכָל הַסַּלִּים יַחַד?","a":4,"b":4},{"id":"w040","level":0,"text":"יֵשׁ 5 סַלִּים. בְּכָל סַל 3 כַּדּוּרִים. כַּמָּה כַּדּוּרִים יֵשׁ בְּכָל הַסַּלִּים יַחַד?","a":5,"b":3},{"id":"w041","level":0,"text":"בַּסִּפְרִיָּה 4 מַדָּפִים. עַל כָּל מַדָּף 2 סְפָרִים. כַּמָּה סְפָרִים יֵשׁ עַל הַמַּדָּפִים?","a":4,"b":2},{"id":"w042","level":0,"text":"בַּסִּפְרִיָּה 4 מַדָּפִים. עַל כָּל מַדָּף 5 סְפָרִים. כַּמָּה סְפָרִים יֵשׁ עַל הַמַּדָּפִים?","a":4,"b":5},{"id":"w043","level":0,"text":"בַּסִּפְרִיָּה 5 מַדָּפִים. עַל כָּל מַדָּף 4 סְפָרִים. כַּמָּה סְפָרִים יֵשׁ עַל הַמַּדָּפִים?","a":5,"b":4},{"id":"w044","level":0,"text":"בַּסִּפְרִיָּה 2 מַדָּפִים. עַל כָּל מַדָּף 3 סְפָרִים. כַּמָּה סְפָרִים יֵשׁ עַל הַמַּדָּפִים?","a":2,"b":3},{"id":"w045","level":0,"text":"בַּסִּפְרִיָּה 3 מַדָּפִים. עַל כָּל מַדָּף 2 סְפָרִים. כַּמָּה סְפָרִים יֵשׁ עַל הַמַּדָּפִים?","a":3,"b":2},{"id":"w046","level":0,"text":"בַּיַּעַר 5 עֵצִים. עַל כָּל עֵץ 5 צִפּוֹרִים. כַּמָּה צִפּוֹרִים יֵשׁ עַל הָעֵצִים?","a":5,"b":5},{"id":"w047","level":0,"text":"בַּיַּעַר 2 עֵצִים. עַל כָּל עֵץ 4 צִפּוֹרִים. כַּמָּה צִפּוֹרִים יֵשׁ עַל הָעֵצִים?","a":2,"b":4},{"id":"w048","level":0,"text":"בַּיַּעַר 3 עֵצִים. עַל כָּל עֵץ 3 צִפּוֹרִים. כַּמָּה צִפּוֹרִים יֵשׁ עַל הָעֵצִים?","a":3,"b":3},{"id":"w049","level":0,"text":"בַּיַּעַר 4 עֵצִים. עַל כָּל עֵץ 2 צִפּוֹרִים. כַּמָּה צִפּוֹרִים יֵשׁ עַל הָעֵצִים?","a":4,"b":2},{"id":"w050","level":0,"text":"בַּיַּעַר 4 עֵצִים. עַל כָּל עֵץ 5 צִפּוֹרִים. כַּמָּה צִפּוֹרִים יֵשׁ עַל הָעֵצִים?","a":4,"b":5},{"id":"w051","level":0,"text":"יֵשׁ 3 שֻׁלְחָנוֹת. לְיַד כָּל שֻׁלְחָן 4 כִּסְאוֹת. כַּמָּה כִּסְאוֹת יֵשׁ בְּסַךְ הַכֹּל?","a":3,"b":4},{"id":"w052","level":0,"text":"יֵשׁ 4 שֻׁלְחָנוֹת. לְיַד כָּל שֻׁלְחָן 3 כִּסְאוֹת. כַּמָּה כִּסְאוֹת יֵשׁ בְּסַךְ הַכֹּל?","a":4,"b":3},{"id":"w053","level":0,"text":"יֵשׁ 5 שֻׁלְחָנוֹת. לְיַד כָּל שֻׁלְחָן 2 כִּסְאוֹת. כַּמָּה כִּסְאוֹת יֵשׁ בְּסַךְ הַכֹּל?","a":5,"b":2},{"id":"w054","level":0,"text":"יֵשׁ 5 שֻׁלְחָנוֹת. לְיַד כָּל שֻׁלְחָן 5 כִּסְאוֹת. כַּמָּה כִּסְאוֹת יֵשׁ בְּסַךְ הַכֹּל?","a":5,"b":5},{"id":"w055","level":0,"text":"יֵשׁ 2 שֻׁלְחָנוֹת. לְיַד כָּל שֻׁלְחָן 4 כִּסְאוֹת. כַּמָּה כִּסְאוֹת יֵשׁ בְּסַךְ הַכֹּל?","a":2,"b":4},{"id":"w056","level":0,"text":"יֵשׁ 5 צְמִידִים. בְּכָל צָמִיד 3 חָרוּזִים. כַּמָּה חָרוּזִים יֵשׁ בְּכָל הַצְּמִידִים?","a":5,"b":3},{"id":"w057","level":0,"text":"יֵשׁ 2 צְמִידִים. בְּכָל צָמִיד 2 חָרוּזִים. כַּמָּה חָרוּזִים יֵשׁ בְּכָל הַצְּמִידִים?","a":2,"b":2},{"id":"w058","level":0,"text":"יֵשׁ 2 צְמִידִים. בְּכָל צָמִיד 5 חָרוּזִים. כַּמָּה חָרוּזִים יֵשׁ בְּכָל הַצְּמִידִים?","a":2,"b":5},{"id":"w059","level":0,"text":"יֵשׁ 3 צְמִידִים. בְּכָל צָמִיד 4 חָרוּזִים. כַּמָּה חָרוּזִים יֵשׁ בְּכָל הַצְּמִידִים?","a":3,"b":4},{"id":"w060","level":0,"text":"יֵשׁ 4 צְמִידִים. בְּכָל צָמִיד 3 חָרוּזִים. כַּמָּה חָרוּזִים יֵשׁ בְּכָל הַצְּמִידִים?","a":4,"b":3},{"id":"w061","level":0,"text":"יֵשׁ 3 קַרְטוֹנִים. בְּכָל קַרְטוֹן 2 בַּקְבּוּקִים. כַּמָּה בַּקְבּוּקִים יֵשׁ בְּסַךְ הַכֹּל?","a":3,"b":2},{"id":"w062","level":0,"text":"יֵשׁ 3 קַרְטוֹנִים. בְּכָל קַרְטוֹן 5 בַּקְבּוּקִים. כַּמָּה בַּקְבּוּקִים יֵשׁ בְּסַךְ הַכֹּל?","a":3,"b":5},{"id":"w063","level":0,"text":"יֵשׁ 4 קַרְטוֹנִים. בְּכָל קַרְטוֹן 4 בַּקְבּוּקִים. כַּמָּה בַּקְבּוּקִים יֵשׁ בְּסַךְ הַכֹּל?","a":4,"b":4},{"id":"w064","level":0,"text":"יֵשׁ 5 קַרְטוֹנִים. בְּכָל קַרְטוֹן 3 בַּקְבּוּקִים. כַּמָּה בַּקְבּוּקִים יֵשׁ בְּסַךְ הַכֹּל?","a":5,"b":3},{"id":"w065","level":0,"text":"יֵשׁ 2 קַרְטוֹנִים. בְּכָל קַרְטוֹן 2 בַּקְבּוּקִים. כַּמָּה בַּקְבּוּקִים יֵשׁ בְּסַךְ הַכֹּל?","a":2,"b":2},{"id":"w066","level":0,"text":"בַּמִּשְׂחָק 4 מִגְדָּלִים. בְּכָל מִגְדָּל 5 קֻבִּיּוֹת. כַּמָּה קֻבִּיּוֹת יֵשׁ בְּסַךְ הַכֹּל?","a":4,"b":5},{"id":"w067","level":0,"text":"בַּמִּשְׂחָק 5 מִגְדָּלִים. בְּכָל מִגְדָּל 4 קֻבִּיּוֹת. כַּמָּה קֻבִּיּוֹת יֵשׁ בְּסַךְ הַכֹּל?","a":5,"b":4},{"id":"w068","level":0,"text":"בַּמִּשְׂחָק 2 מִגְדָּלִים. בְּכָל מִגְדָּל 3 קֻבִּיּוֹת. כַּמָּה קֻבִּיּוֹת יֵשׁ בְּסַךְ הַכֹּל?","a":2,"b":3},{"id":"w069","level":0,"text":"בַּמִּשְׂחָק 3 מִגְדָּלִים. בְּכָל מִגְדָּל 2 קֻבִּיּוֹת. כַּמָּה קֻבִּיּוֹת יֵשׁ בְּסַךְ הַכֹּל?","a":3,"b":2},{"id":"w070","level":0,"text":"בַּמִּשְׂחָק 3 מִגְדָּלִים. בְּכָל מִגְדָּל 5 קֻבִּיּוֹת. כַּמָּה קֻבִּיּוֹת יֵשׁ בְּסַךְ הַכֹּל?","a":3,"b":5},{"id":"w071","level":0,"text":"יֵשׁ 2 זֵרִים. בְּכָל זֵר 4 פְּרָחִים. כַּמָּה פְּרָחִים יֵשׁ בְּכָל הַזֵּרִים?","a":2,"b":4},{"id":"w072","level":0,"text":"יֵשׁ 3 זֵרִים. בְּכָל זֵר 3 פְּרָחִים. כַּמָּה פְּרָחִים יֵשׁ בְּכָל הַזֵּרִים?","a":3,"b":3},{"id":"w073","level":0,"text":"יֵשׁ 4 זֵרִים. בְּכָל זֵר 2 פְּרָחִים. כַּמָּה פְּרָחִים יֵשׁ בְּכָל הַזֵּרִים?","a":4,"b":2},{"id":"w074","level":0,"text":"יֵשׁ 4 זֵרִים. בְּכָל זֵר 5 פְּרָחִים. כַּמָּה פְּרָחִים יֵשׁ בְּכָל הַזֵּרִים?","a":4,"b":5},{"id":"w075","level":0,"text":"יֵשׁ 5 זֵרִים. בְּכָל זֵר 4 פְּרָחִים. כַּמָּה פְּרָחִים יֵשׁ בְּכָל הַזֵּרִים?","a":5,"b":4},{"id":"w076","level":0,"text":"יֵשׁ 4 אֲרִיזוֹת. בְּכָל אֲרִיזָה 3 קְלָפִים. כַּמָּה קְלָפִים יֵשׁ בְּסַךְ הַכֹּל?","a":4,"b":3},{"id":"w077","level":0,"text":"יֵשׁ 5 אֲרִיזוֹת. בְּכָל אֲרִיזָה 2 קְלָפִים. כַּמָּה קְלָפִים יֵשׁ בְּסַךְ הַכֹּל?","a":5,"b":2},{"id":"w078","level":0,"text":"יֵשׁ 5 אֲרִיזוֹת. בְּכָל אֲרִיזָה 5 קְלָפִים. כַּמָּה קְלָפִים יֵשׁ בְּסַךְ הַכֹּל?","a":5,"b":5},{"id":"w079","level":0,"text":"יֵשׁ 2 אֲרִיזוֹת. בְּכָל אֲרִיזָה 4 קְלָפִים. כַּמָּה קְלָפִים יֵשׁ בְּסַךְ הַכֹּל?","a":2,"b":4},{"id":"w080","level":0,"text":"יֵשׁ 3 אֲרִיזוֹת. בְּכָל אֲרִיזָה 3 קְלָפִים. כַּמָּה קְלָפִים יֵשׁ בְּסַךְ הַכֹּל?","a":3,"b":3},{"id":"w081","level":1,"text":"לַהַצָּגָה הֵכִינוּ 5 שׁוּרוֹת שֶׁל כִּסְאוֹת, וּבְכָל שׁוּרָה 6 כִּסְאוֹת. כַּמָּה אֲנָשִׁים יוּכְלוּ לָשֶׁבֶת?","a":5,"b":6},{"id":"w082","level":1,"text":"לַהַצָּגָה הֵכִינוּ 5 שׁוּרוֹת שֶׁל כִּסְאוֹת, וּבְכָל שׁוּרָה 9 כִּסְאוֹת. כַּמָּה אֲנָשִׁים יוּכְלוּ לָשֶׁבֶת?","a":5,"b":9},{"id":"w083","level":1,"text":"לַהַצָּגָה הֵכִינוּ 6 שׁוּרוֹת שֶׁל כִּסְאוֹת, וּבְכָל שׁוּרָה 3 כִּסְאוֹת. כַּמָּה אֲנָשִׁים יוּכְלוּ לָשֶׁבֶת?","a":6,"b":3},{"id":"w084","level":1,"text":"לַהַצָּגָה הֵכִינוּ 6 שׁוּרוֹת שֶׁל כִּסְאוֹת, וּבְכָל שׁוּרָה 6 כִּסְאוֹת. כַּמָּה אֲנָשִׁים יוּכְלוּ לָשֶׁבֶת?","a":6,"b":6},{"id":"w085","level":1,"text":"לַהַצָּגָה הֵכִינוּ 6 שׁוּרוֹת שֶׁל כִּסְאוֹת, וּבְכָל שׁוּרָה 9 כִּסְאוֹת. כַּמָּה אֲנָשִׁים יוּכְלוּ לָשֶׁבֶת?","a":6,"b":9},{"id":"w086","level":1,"text":"בְּכָל עַמּוּד בָּאַלְבּוֹם יֵשׁ מָקוֹם לְ־4 תְּמוּנוֹת. מִלְּאוּ 6 עַמּוּדִים. כַּמָּה תְּמוּנוֹת הִכְנִיסוּ?","a":6,"b":4},{"id":"w087","level":1,"text":"בְּכָל עַמּוּד בָּאַלְבּוֹם יֵשׁ מָקוֹם לְ־7 תְּמוּנוֹת. מִלְּאוּ 6 עַמּוּדִים. כַּמָּה תְּמוּנוֹת הִכְנִיסוּ?","a":6,"b":7},{"id":"w088","level":1,"text":"בְּכָל עַמּוּד בָּאַלְבּוֹם יֵשׁ מָקוֹם לְ־10 תְּמוּנוֹת. מִלְּאוּ 6 עַמּוּדִים. כַּמָּה תְּמוּנוֹת הִכְנִיסוּ?","a":6,"b":10},{"id":"w089","level":1,"text":"בְּכָל עַמּוּד בָּאַלְבּוֹם יֵשׁ מָקוֹם לְ־4 תְּמוּנוֹת. מִלְּאוּ 7 עַמּוּדִים. כַּמָּה תְּמוּנוֹת הִכְנִיסוּ?","a":7,"b":4},{"id":"w090","level":1,"text":"בְּכָל עַמּוּד בָּאַלְבּוֹם יֵשׁ מָקוֹם לְ־7 תְּמוּנוֹת. מִלְּאוּ 7 עַמּוּדִים. כַּמָּה תְּמוּנוֹת הִכְנִיסוּ?","a":7,"b":7},{"id":"w091","level":1,"text":"בְּמֶשֶׁךְ 7 יָמִים קָרְאוּ בְּכָל יוֹם 2 עַמּוּדִים. כַּמָּה עַמּוּדִים קָרְאוּ בְּכָל הַיָּמִים יַחַד?","a":7,"b":2},{"id":"w092","level":1,"text":"בְּמֶשֶׁךְ 7 יָמִים קָרְאוּ בְּכָל יוֹם 5 עַמּוּדִים. כַּמָּה עַמּוּדִים קָרְאוּ בְּכָל הַיָּמִים יַחַד?","a":7,"b":5},{"id":"w093","level":1,"text":"בְּמֶשֶׁךְ 7 יָמִים קָרְאוּ בְּכָל יוֹם 8 עַמּוּדִים. כַּמָּה עַמּוּדִים קָרְאוּ בְּכָל הַיָּמִים יַחַד?","a":7,"b":8},{"id":"w094","level":1,"text":"בְּמֶשֶׁךְ 8 יָמִים קָרְאוּ בְּכָל יוֹם 2 עַמּוּדִים. כַּמָּה עַמּוּדִים קָרְאוּ בְּכָל הַיָּמִים יַחַד?","a":8,"b":2},{"id":"w095","level":1,"text":"בְּמֶשֶׁךְ 8 יָמִים קָרְאוּ בְּכָל יוֹם 5 עַמּוּדִים. כַּמָּה עַמּוּדִים קָרְאוּ בְּכָל הַיָּמִים יַחַד?","a":8,"b":5},{"id":"w096","level":1,"text":"לְכָל קְבוּצָה מְחַלְּקִים 9 כַּרְטִיסִים. בַּכִּתָּה יֵשׁ 7 קְבוּצוֹת. כַּמָּה כַּרְטִיסִים צָרִיךְ לְחַלֵּק?","a":7,"b":9},{"id":"w097","level":1,"text":"לְכָל קְבוּצָה מְחַלְּקִים 3 כַּרְטִיסִים. בַּכִּתָּה יֵשׁ 8 קְבוּצוֹת. כַּמָּה כַּרְטִיסִים צָרִיךְ לְחַלֵּק?","a":8,"b":3},{"id":"w098","level":1,"text":"לְכָל קְבוּצָה מְחַלְּקִים 6 כַּרְטִיסִים. בַּכִּתָּה יֵשׁ 8 קְבוּצוֹת. כַּמָּה כַּרְטִיסִים צָרִיךְ לְחַלֵּק?","a":8,"b":6},{"id":"w099","level":1,"text":"לְכָל קְבוּצָה מְחַלְּקִים 9 כַּרְטִיסִים. בַּכִּתָּה יֵשׁ 8 קְבוּצוֹת. כַּמָּה כַּרְטִיסִים צָרִיךְ לְחַלֵּק?","a":8,"b":9},{"id":"w100","level":1,"text":"לְכָל קְבוּצָה מְחַלְּקִים 3 כַּרְטִיסִים. בַּכִּתָּה יֵשׁ 9 קְבוּצוֹת. כַּמָּה כַּרְטִיסִים צָרִיךְ לְחַלֵּק?","a":9,"b":3},{"id":"w101","level":1,"text":"בַּמַּאֲפִיָּה אוֹפִים 8 מַגָּשִׁים. עַל כָּל מַגָּשׁ 7 מַאֲפִים. כַּמָּה מַאֲפִים אוֹפִים בְּסַךְ הַכֹּל?","a":8,"b":7},{"id":"w102","level":1,"text":"בַּמַּאֲפִיָּה אוֹפִים 8 מַגָּשִׁים. עַל כָּל מַגָּשׁ 10 מַאֲפִים. כַּמָּה מַאֲפִים אוֹפִים בְּסַךְ הַכֹּל?","a":8,"b":10},{"id":"w103","level":1,"text":"בַּמַּאֲפִיָּה אוֹפִים 9 מַגָּשִׁים. עַל כָּל מַגָּשׁ 4 מַאֲפִים. כַּמָּה מַאֲפִים אוֹפִים בְּסַךְ הַכֹּל?","a":9,"b":4},{"id":"w104","level":1,"text":"בַּמַּאֲפִיָּה אוֹפִים 9 מַגָּשִׁים. עַל כָּל מַגָּשׁ 7 מַאֲפִים. כַּמָּה מַאֲפִים אוֹפִים בְּסַךְ הַכֹּל?","a":9,"b":7},{"id":"w105","level":1,"text":"בַּמַּאֲפִיָּה אוֹפִים 9 מַגָּשִׁים. עַל כָּל מַגָּשׁ 10 מַאֲפִים. כַּמָּה מַאֲפִים אוֹפִים בְּסַךְ הַכֹּל?","a":9,"b":10},{"id":"w106","level":1,"text":"לְכָל מִשְׁתַּתֵּף בַּחֻג נוֹתְנִים 5 דַּפִּים. בַּחֻג 9 מִשְׁתַּתְּפִים. כַּמָּה דַּפִּים צָרִיךְ לְהָכִין?","a":9,"b":5},{"id":"w107","level":1,"text":"לְכָל מִשְׁתַּתֵּף בַּחֻג נוֹתְנִים 8 דַּפִּים. בַּחֻג 9 מִשְׁתַּתְּפִים. כַּמָּה דַּפִּים צָרִיךְ לְהָכִין?","a":9,"b":8},{"id":"w108","level":1,"text":"לְכָל מִשְׁתַּתֵּף בַּחֻג נוֹתְנִים 2 דַּפִּים. בַּחֻג 10 מִשְׁתַּתְּפִים. כַּמָּה דַּפִּים צָרִיךְ לְהָכִין?","a":10,"b":2},{"id":"w109","level":1,"text":"לְכָל מִשְׁתַּתֵּף בַּחֻג נוֹתְנִים 5 דַּפִּים. בַּחֻג 10 מִשְׁתַּתְּפִים. כַּמָּה דַּפִּים צָרִיךְ לְהָכִין?","a":10,"b":5},{"id":"w110","level":1,"text":"לְכָל מִשְׁתַּתֵּף בַּחֻג נוֹתְנִים 8 דַּפִּים. בַּחֻג 10 מִשְׁתַּתְּפִים. כַּמָּה דַּפִּים צָרִיךְ לְהָכִין?","a":10,"b":8},{"id":"w111","level":1,"text":"בַּחֲנוּת יֵשׁ 10 מַדָּפִים שֶׁל צַעֲצוּעִים. עַל כָּל מַדָּף 3 צַעֲצוּעִים. כַּמָּה צַעֲצוּעִים יֵשׁ עַל הַמַּדָּפִים?","a":10,"b":3},{"id":"w112","level":1,"text":"בַּחֲנוּת יֵשׁ 10 מַדָּפִים שֶׁל צַעֲצוּעִים. עַל כָּל מַדָּף 6 צַעֲצוּעִים. כַּמָּה צַעֲצוּעִים יֵשׁ עַל הַמַּדָּפִים?","a":10,"b":6},{"id":"w113","level":1,"text":"בַּחֲנוּת יֵשׁ 10 מַדָּפִים שֶׁל צַעֲצוּעִים. עַל כָּל מַדָּף 9 צַעֲצוּעִים. כַּמָּה צַעֲצוּעִים יֵשׁ עַל הַמַּדָּפִים?","a":10,"b":9},{"id":"w114","level":1,"text":"בַּחֲנוּת יֵשׁ 2 מַדָּפִים שֶׁל צַעֲצוּעִים. עַל כָּל מַדָּף 3 צַעֲצוּעִים. כַּמָּה צַעֲצוּעִים יֵשׁ עַל הַמַּדָּפִים?","a":2,"b":3},{"id":"w115","level":1,"text":"בַּחֲנוּת יֵשׁ 2 מַדָּפִים שֶׁל צַעֲצוּעִים. עַל כָּל מַדָּף 6 צַעֲצוּעִים. כַּמָּה צַעֲצוּעִים יֵשׁ עַל הַמַּדָּפִים?","a":2,"b":6},{"id":"w116","level":1,"text":"בְּכָל מַסְלוּל בַּמִּשְׂחָק יֵשׁ 10 תַּחֲנוֹת. בָּנוּ 10 מַסְלוּלִים נִפְרָדִים. כַּמָּה תַּחֲנוֹת יֵשׁ בְּסַךְ הַכֹּל?","a":10,"b":10},{"id":"w117","level":1,"text":"בְּכָל מַסְלוּל בַּמִּשְׂחָק יֵשׁ 4 תַּחֲנוֹת. בָּנוּ 2 מַסְלוּלִים נִפְרָדִים. כַּמָּה תַּחֲנוֹת יֵשׁ בְּסַךְ הַכֹּל?","a":2,"b":4},{"id":"w118","level":1,"text":"בְּכָל מַסְלוּל בַּמִּשְׂחָק יֵשׁ 7 תַּחֲנוֹת. בָּנוּ 2 מַסְלוּלִים נִפְרָדִים. כַּמָּה תַּחֲנוֹת יֵשׁ בְּסַךְ הַכֹּל?","a":2,"b":7},{"id":"w119","level":1,"text":"בְּכָל מַסְלוּל בַּמִּשְׂחָק יֵשׁ 10 תַּחֲנוֹת. בָּנוּ 2 מַסְלוּלִים נִפְרָדִים. כַּמָּה תַּחֲנוֹת יֵשׁ בְּסַךְ הַכֹּל?","a":2,"b":10},{"id":"w120","level":1,"text":"בְּכָל מַסְלוּל בַּמִּשְׂחָק יֵשׁ 4 תַּחֲנוֹת. בָּנוּ 3 מַסְלוּלִים נִפְרָדִים. כַּמָּה תַּחֲנוֹת יֵשׁ בְּסַךְ הַכֹּל?","a":3,"b":4},{"id":"w121","level":1,"text":"בְּכָל קֻפְסַת יְצִירָה יֵשׁ 8 מִכְחוֹלִים. הֵבִיאוּ 2 קֻפְסָאוֹת לַכִּתָּה. כַּמָּה מִכְחוֹלִים הֵבִיאוּ?","a":2,"b":8},{"id":"w122","level":1,"text":"בְּכָל קֻפְסַת יְצִירָה יֵשׁ 2 מִכְחוֹלִים. הֵבִיאוּ 3 קֻפְסָאוֹת לַכִּתָּה. כַּמָּה מִכְחוֹלִים הֵבִיאוּ?","a":3,"b":2},{"id":"w123","level":1,"text":"בְּכָל קֻפְסַת יְצִירָה יֵשׁ 5 מִכְחוֹלִים. הֵבִיאוּ 3 קֻפְסָאוֹת לַכִּתָּה. כַּמָּה מִכְחוֹלִים הֵבִיאוּ?","a":3,"b":5},{"id":"w124","level":1,"text":"בְּכָל קֻפְסַת יְצִירָה יֵשׁ 8 מִכְחוֹלִים. הֵבִיאוּ 3 קֻפְסָאוֹת לַכִּתָּה. כַּמָּה מִכְחוֹלִים הֵבִיאוּ?","a":3,"b":8},{"id":"w125","level":1,"text":"בְּכָל קֻפְסַת יְצִירָה יֵשׁ 2 מִכְחוֹלִים. הֵבִיאוּ 4 קֻפְסָאוֹת לַכִּתָּה. כַּמָּה מִכְחוֹלִים הֵבִיאוּ?","a":4,"b":2},{"id":"w126","level":1,"text":"לְכָל שֻׁלְחָן מְכִינִים 6 מַפִּיּוֹת. בָּאוּלָם 3 שֻׁלְחָנוֹת. כַּמָּה מַפִּיּוֹת יֵשׁ לְהָכִין?","a":3,"b":6},{"id":"w127","level":1,"text":"לְכָל שֻׁלְחָן מְכִינִים 9 מַפִּיּוֹת. בָּאוּלָם 3 שֻׁלְחָנוֹת. כַּמָּה מַפִּיּוֹת יֵשׁ לְהָכִין?","a":3,"b":9},{"id":"w128","level":1,"text":"לְכָל שֻׁלְחָן מְכִינִים 3 מַפִּיּוֹת. בָּאוּלָם 4 שֻׁלְחָנוֹת. כַּמָּה מַפִּיּוֹת יֵשׁ לְהָכִין?","a":4,"b":3},{"id":"w129","level":1,"text":"לְכָל שֻׁלְחָן מְכִינִים 6 מַפִּיּוֹת. בָּאוּלָם 4 שֻׁלְחָנוֹת. כַּמָּה מַפִּיּוֹת יֵשׁ לְהָכִין?","a":4,"b":6},{"id":"w130","level":1,"text":"לְכָל שֻׁלְחָן מְכִינִים 9 מַפִּיּוֹת. בָּאוּלָם 4 שֻׁלְחָנוֹת. כַּמָּה מַפִּיּוֹת יֵשׁ לְהָכִין?","a":4,"b":9},{"id":"w131","level":1,"text":"הַגַּנָּן שָׁתַל 4 שׁוּרוֹת שֶׁל שְׁתִילִים. בְּכָל שׁוּרָה 4 שְׁתִילִים. כַּמָּה שְׁתִילִים שָׁתַל?","a":4,"b":4},{"id":"w132","level":1,"text":"הַגַּנָּן שָׁתַל 4 שׁוּרוֹת שֶׁל שְׁתִילִים. בְּכָל שׁוּרָה 7 שְׁתִילִים. כַּמָּה שְׁתִילִים שָׁתַל?","a":4,"b":7},{"id":"w133","level":1,"text":"הַגַּנָּן שָׁתַל 4 שׁוּרוֹת שֶׁל שְׁתִילִים. בְּכָל שׁוּרָה 10 שְׁתִילִים. כַּמָּה שְׁתִילִים שָׁתַל?","a":4,"b":10},{"id":"w134","level":1,"text":"הַגַּנָּן שָׁתַל 5 שׁוּרוֹת שֶׁל שְׁתִילִים. בְּכָל שׁוּרָה 4 שְׁתִילִים. כַּמָּה שְׁתִילִים שָׁתַל?","a":5,"b":4},{"id":"w135","level":1,"text":"הַגַּנָּן שָׁתַל 5 שׁוּרוֹת שֶׁל שְׁתִילִים. בְּכָל שׁוּרָה 7 שְׁתִילִים. כַּמָּה שְׁתִילִים שָׁתַל?","a":5,"b":7},{"id":"w136","level":1,"text":"בְּכָל תֵּבָה יֵשׁ 2 אוֹצָרוֹת. בַּמִּשְׂחָק מָצְאוּ 5 תֵּבוֹת. כַּמָּה אוֹצָרוֹת מָצְאוּ בְּסַךְ הַכֹּל?","a":5,"b":2},{"id":"w137","level":1,"text":"בְּכָל תֵּבָה יֵשׁ 5 אוֹצָרוֹת. בַּמִּשְׂחָק מָצְאוּ 5 תֵּבוֹת. כַּמָּה אוֹצָרוֹת מָצְאוּ בְּסַךְ הַכֹּל?","a":5,"b":5},{"id":"w138","level":1,"text":"בְּכָל תֵּבָה יֵשׁ 8 אוֹצָרוֹת. בַּמִּשְׂחָק מָצְאוּ 5 תֵּבוֹת. כַּמָּה אוֹצָרוֹת מָצְאוּ בְּסַךְ הַכֹּל?","a":5,"b":8},{"id":"w139","level":1,"text":"בְּכָל תֵּבָה יֵשׁ 2 אוֹצָרוֹת. בַּמִּשְׂחָק מָצְאוּ 6 תֵּבוֹת. כַּמָּה אוֹצָרוֹת מָצְאוּ בְּסַךְ הַכֹּל?","a":6,"b":2},{"id":"w140","level":1,"text":"בְּכָל תֵּבָה יֵשׁ 5 אוֹצָרוֹת. בַּמִּשְׂחָק מָצְאוּ 6 תֵּבוֹת. כַּמָּה אוֹצָרוֹת מָצְאוּ בְּסַךְ הַכֹּל?","a":6,"b":5},{"id":"w141","level":2,"text":"לְקִשּׁוּט הַכִּתָּה מְכִינִים שַׁרְשְׁרוֹת זֵהוֹת. כָּל שַׁרְשֶׁרֶת מֻרְכֶּבֶת מִ־7 טַבָּעוֹת נְיָר. רוֹצִים לִתְלוֹת 10 שַׁרְשְׁרוֹת. כַּמָּה טַבָּעוֹת צָרִיךְ לְהָכִין?","a":10,"b":7},{"id":"w142","level":2,"text":"לְקִשּׁוּט הַכִּתָּה מְכִינִים שַׁרְשְׁרוֹת זֵהוֹת. כָּל שַׁרְשֶׁרֶת מֻרְכֶּבֶת מִ־10 טַבָּעוֹת נְיָר. רוֹצִים לִתְלוֹת 10 שַׁרְשְׁרוֹת. כַּמָּה טַבָּעוֹת צָרִיךְ לְהָכִין?","a":10,"b":10},{"id":"w143","level":2,"text":"לְקִשּׁוּט הַכִּתָּה מְכִינִים שַׁרְשְׁרוֹת זֵהוֹת. כָּל שַׁרְשֶׁרֶת מֻרְכֶּבֶת מִ־5 טַבָּעוֹת נְיָר. רוֹצִים לִתְלוֹת 6 שַׁרְשְׁרוֹת. כַּמָּה טַבָּעוֹת צָרִיךְ לְהָכִין?","a":6,"b":5},{"id":"w144","level":2,"text":"לְקִשּׁוּט הַכִּתָּה מְכִינִים שַׁרְשְׁרוֹת זֵהוֹת. כָּל שַׁרְשֶׁרֶת מֻרְכֶּבֶת מִ־8 טַבָּעוֹת נְיָר. רוֹצִים לִתְלוֹת 6 שַׁרְשְׁרוֹת. כַּמָּה טַבָּעוֹת צָרִיךְ לְהָכִין?","a":6,"b":8},{"id":"w145","level":2,"text":"לְקִשּׁוּט הַכִּתָּה מְכִינִים שַׁרְשְׁרוֹת זֵהוֹת. כָּל שַׁרְשֶׁרֶת מֻרְכֶּבֶת מִ־3 טַבָּעוֹת נְיָר. רוֹצִים לִתְלוֹת 7 שַׁרְשְׁרוֹת. כַּמָּה טַבָּעוֹת צָרִיךְ לְהָכִין?","a":7,"b":3},{"id":"w146","level":2,"text":"בְּמִשְׂחַק הָאוֹצָר כָּל הַצְלָחָה מְזַכָּה בְּ־6 נְקֻדּוֹת. שָׁקֵד הִצְלִיחָה בְּ־6 מְשִׂימוֹת, וְלֹא קִבְּלָה נְקֻדּוֹת נוֹסָפוֹת. כַּמָּה נְקֻדּוֹת צָבְרָה?","a":6,"b":6},{"id":"w147","level":2,"text":"בְּמִשְׂחַק הָאוֹצָר כָּל הַצְלָחָה מְזַכָּה בְּ־9 נְקֻדּוֹת. שָׁקֵד הִצְלִיחָה בְּ־6 מְשִׂימוֹת, וְלֹא קִבְּלָה נְקֻדּוֹת נוֹסָפוֹת. כַּמָּה נְקֻדּוֹת צָבְרָה?","a":6,"b":9},{"id":"w148","level":2,"text":"בְּמִשְׂחַק הָאוֹצָר כָּל הַצְלָחָה מְזַכָּה בְּ־4 נְקֻדּוֹת. שָׁקֵד הִצְלִיחָה בְּ־7 מְשִׂימוֹת, וְלֹא קִבְּלָה נְקֻדּוֹת נוֹסָפוֹת. כַּמָּה נְקֻדּוֹת צָבְרָה?","a":7,"b":4},{"id":"w149","level":2,"text":"בְּמִשְׂחַק הָאוֹצָר כָּל הַצְלָחָה מְזַכָּה בְּ־7 נְקֻדּוֹת. שָׁקֵד הִצְלִיחָה בְּ־7 מְשִׂימוֹת, וְלֹא קִבְּלָה נְקֻדּוֹת נוֹסָפוֹת. כַּמָּה נְקֻדּוֹת צָבְרָה?","a":7,"b":7},{"id":"w150","level":2,"text":"בְּמִשְׂחַק הָאוֹצָר כָּל הַצְלָחָה מְזַכָּה בְּ־10 נְקֻדּוֹת. שָׁקֵד הִצְלִיחָה בְּ־7 מְשִׂימוֹת, וְלֹא קִבְּלָה נְקֻדּוֹת נוֹסָפוֹת. כַּמָּה נְקֻדּוֹת צָבְרָה?","a":7,"b":10},{"id":"w151","level":2,"text":"מוֹכְרִים כַּרְטִיסִים בַּחֲבִילוֹת שֶׁל 5 כַּרְטִיסִים. הַמּוֹרָה קָנְתָה 7 חֲבִילוֹת שְׁלֵמוֹת. לְכַמָּה יְלָדִים יֵשׁ כַּרְטִיס, אִם כָּל יֶלֶד מְקַבֵּל אֶחָד?","a":7,"b":5},{"id":"w152","level":2,"text":"מוֹכְרִים כַּרְטִיסִים בַּחֲבִילוֹת שֶׁל 8 כַּרְטִיסִים. הַמּוֹרָה קָנְתָה 7 חֲבִילוֹת שְׁלֵמוֹת. לְכַמָּה יְלָדִים יֵשׁ כַּרְטִיס, אִם כָּל יֶלֶד מְקַבֵּל אֶחָד?","a":7,"b":8},{"id":"w153","level":2,"text":"מוֹכְרִים כַּרְטִיסִים בַּחֲבִילוֹת שֶׁל 3 כַּרְטִיסִים. הַמּוֹרָה קָנְתָה 8 חֲבִילוֹת שְׁלֵמוֹת. לְכַמָּה יְלָדִים יֵשׁ כַּרְטִיס, אִם כָּל יֶלֶד מְקַבֵּל אֶחָד?","a":8,"b":3},{"id":"w154","level":2,"text":"מוֹכְרִים כַּרְטִיסִים בַּחֲבִילוֹת שֶׁל 6 כַּרְטִיסִים. הַמּוֹרָה קָנְתָה 8 חֲבִילוֹת שְׁלֵמוֹת. לְכַמָּה יְלָדִים יֵשׁ כַּרְטִיס, אִם כָּל יֶלֶד מְקַבֵּל אֶחָד?","a":8,"b":6},{"id":"w155","level":2,"text":"מוֹכְרִים כַּרְטִיסִים בַּחֲבִילוֹת שֶׁל 9 כַּרְטִיסִים. הַמּוֹרָה קָנְתָה 8 חֲבִילוֹת שְׁלֵמוֹת. לְכַמָּה יְלָדִים יֵשׁ כַּרְטִיס, אִם כָּל יֶלֶד מְקַבֵּל אֶחָד?","a":8,"b":9},{"id":"w156","level":2,"text":"לְהַכָּנַת דֶּגֶם אֶחָד צָרִיךְ 4 חֲלָקִים. הַכִּתָּה בּוֹנָה 8 דְּגָמִים זֵהִים, בְּלִי לְשַׁתֵּף חֲלָקִים בֵּינֵיהֶם. כַּמָּה חֲלָקִים צָרִיךְ בְּסַךְ הַכֹּל?","a":8,"b":4},{"id":"w157","level":2,"text":"לְהַכָּנַת דֶּגֶם אֶחָד צָרִיךְ 7 חֲלָקִים. הַכִּתָּה בּוֹנָה 8 דְּגָמִים זֵהִים, בְּלִי לְשַׁתֵּף חֲלָקִים בֵּינֵיהֶם. כַּמָּה חֲלָקִים צָרִיךְ בְּסַךְ הַכֹּל?","a":8,"b":7},{"id":"w158","level":2,"text":"לְהַכָּנַת דֶּגֶם אֶחָד צָרִיךְ 10 חֲלָקִים. הַכִּתָּה בּוֹנָה 8 דְּגָמִים זֵהִים, בְּלִי לְשַׁתֵּף חֲלָקִים בֵּינֵיהֶם. כַּמָּה חֲלָקִים צָרִיךְ בְּסַךְ הַכֹּל?","a":8,"b":10},{"id":"w159","level":2,"text":"לְהַכָּנַת דֶּגֶם אֶחָד צָרִיךְ 5 חֲלָקִים. הַכִּתָּה בּוֹנָה 9 דְּגָמִים זֵהִים, בְּלִי לְשַׁתֵּף חֲלָקִים בֵּינֵיהֶם. כַּמָּה חֲלָקִים צָרִיךְ בְּסַךְ הַכֹּל?","a":9,"b":5},{"id":"w160","level":2,"text":"לְהַכָּנַת דֶּגֶם אֶחָד צָרִיךְ 8 חֲלָקִים. הַכִּתָּה בּוֹנָה 9 דְּגָמִים זֵהִים, בְּלִי לְשַׁתֵּף חֲלָקִים בֵּינֵיהֶם. כַּמָּה חֲלָקִים צָרִיךְ בְּסַךְ הַכֹּל?","a":9,"b":8},{"id":"w161","level":2,"text":"בְּלֻחַ הַתְּמוּנוֹת יֵשׁ 9 שׁוּרוֹת, וּבְכָל שׁוּרָה 3 מְקוֹמוֹת. מַדְבִּיקִים תְּמוּנָה אַחַת בְּכָל מָקוֹם וּמְמַלְּאִים אֶת הַלּוּחַ. כַּמָּה תְּמוּנוֹת צָרִיךְ?","a":9,"b":3},{"id":"w162","level":2,"text":"בְּלֻחַ הַתְּמוּנוֹת יֵשׁ 9 שׁוּרוֹת, וּבְכָל שׁוּרָה 6 מְקוֹמוֹת. מַדְבִּיקִים תְּמוּנָה אַחַת בְּכָל מָקוֹם וּמְמַלְּאִים אֶת הַלּוּחַ. כַּמָּה תְּמוּנוֹת צָרִיךְ?","a":9,"b":6},{"id":"w163","level":2,"text":"בְּלֻחַ הַתְּמוּנוֹת יֵשׁ 9 שׁוּרוֹת, וּבְכָל שׁוּרָה 9 מְקוֹמוֹת. מַדְבִּיקִים תְּמוּנָה אַחַת בְּכָל מָקוֹם וּמְמַלְּאִים אֶת הַלּוּחַ. כַּמָּה תְּמוּנוֹת צָרִיךְ?","a":9,"b":9},{"id":"w164","level":2,"text":"בְּלֻחַ הַתְּמוּנוֹת יֵשׁ 10 שׁוּרוֹת, וּבְכָל שׁוּרָה 4 מְקוֹמוֹת. מַדְבִּיקִים תְּמוּנָה אַחַת בְּכָל מָקוֹם וּמְמַלְּאִים אֶת הַלּוּחַ. כַּמָּה תְּמוּנוֹת צָרִיךְ?","a":10,"b":4},{"id":"w165","level":2,"text":"בְּלֻחַ הַתְּמוּנוֹת יֵשׁ 10 שׁוּרוֹת, וּבְכָל שׁוּרָה 7 מְקוֹמוֹת. מַדְבִּיקִים תְּמוּנָה אַחַת בְּכָל מָקוֹם וּמְמַלְּאִים אֶת הַלּוּחַ. כַּמָּה תְּמוּנוֹת צָרִיךְ?","a":10,"b":7},{"id":"w166","level":2,"text":"בְּתַחֲרוּת יֵשׁ 9 קְבוּצוֹת שָׁווֹת בְּגָדְלָן. בְּכָל קְבוּצָה 10 יְלָדִים. כָּל יֶלֶד מְקַבֵּל מְדַלְיָה אַחַת. כַּמָּה מְדַלְיוֹת צָרִיךְ לְכָל הַיְּלָדִים?","a":9,"b":10},{"id":"w167","level":2,"text":"בְּתַחֲרוּת יֵשׁ 10 קְבוּצוֹת שָׁווֹת בְּגָדְלָן. בְּכָל קְבוּצָה 5 יְלָדִים. כָּל יֶלֶד מְקַבֵּל מְדַלְיָה אַחַת. כַּמָּה מְדַלְיוֹת צָרִיךְ לְכָל הַיְּלָדִים?","a":10,"b":5},{"id":"w168","level":2,"text":"בְּתַחֲרוּת יֵשׁ 10 קְבוּצוֹת שָׁווֹת בְּגָדְלָן. בְּכָל קְבוּצָה 8 יְלָדִים. כָּל יֶלֶד מְקַבֵּל מְדַלְיָה אַחַת. כַּמָּה מְדַלְיוֹת צָרִיךְ לְכָל הַיְּלָדִים?","a":10,"b":8},{"id":"w169","level":2,"text":"בְּתַחֲרוּת יֵשׁ 6 קְבוּצוֹת שָׁווֹת בְּגָדְלָן. בְּכָל קְבוּצָה 3 יְלָדִים. כָּל יֶלֶד מְקַבֵּל מְדַלְיָה אַחַת. כַּמָּה מְדַלְיוֹת צָרִיךְ לְכָל הַיְּלָדִים?","a":6,"b":3},{"id":"w170","level":2,"text":"בְּתַחֲרוּת יֵשׁ 6 קְבוּצוֹת שָׁווֹת בְּגָדְלָן. בְּכָל קְבוּצָה 6 יְלָדִים. כָּל יֶלֶד מְקַבֵּל מְדַלְיָה אַחַת. כַּמָּה מְדַלְיוֹת צָרִיךְ לְכָל הַיְּלָדִים?","a":6,"b":6},{"id":"w171","level":2,"text":"מְסַדְּרִים 10 קֻפְסָאוֹת מַתָּנָה. בְּכָל קֻפְסָה אוֹתוֹ מִסְפַּר מַדְבֵּקוֹת: 9. כַּמָּה מַדְבֵּקוֹת יֵשׁ לְהוֹצִיא מֵהַמְּגֵרָה כְּדֵי לְמַלֵּא אֶת כָּל הַקֻּפְסָאוֹת?","a":10,"b":9},{"id":"w172","level":2,"text":"מְסַדְּרִים 6 קֻפְסָאוֹת מַתָּנָה. בְּכָל קֻפְסָה אוֹתוֹ מִסְפַּר מַדְבֵּקוֹת: 4. כַּמָּה מַדְבֵּקוֹת יֵשׁ לְהוֹצִיא מֵהַמְּגֵרָה כְּדֵי לְמַלֵּא אֶת כָּל הַקֻּפְסָאוֹת?","a":6,"b":4},{"id":"w173","level":2,"text":"מְסַדְּרִים 6 קֻפְסָאוֹת מַתָּנָה. בְּכָל קֻפְסָה אוֹתוֹ מִסְפַּר מַדְבֵּקוֹת: 7. כַּמָּה מַדְבֵּקוֹת יֵשׁ לְהוֹצִיא מֵהַמְּגֵרָה כְּדֵי לְמַלֵּא אֶת כָּל הַקֻּפְסָאוֹת?","a":6,"b":7},{"id":"w174","level":2,"text":"מְסַדְּרִים 6 קֻפְסָאוֹת מַתָּנָה. בְּכָל קֻפְסָה אוֹתוֹ מִסְפַּר מַדְבֵּקוֹת: 10. כַּמָּה מַדְבֵּקוֹת יֵשׁ לְהוֹצִיא מֵהַמְּגֵרָה כְּדֵי לְמַלֵּא אֶת כָּל הַקֻּפְסָאוֹת?","a":6,"b":10},{"id":"w175","level":2,"text":"מְסַדְּרִים 7 קֻפְסָאוֹת מַתָּנָה. בְּכָל קֻפְסָה אוֹתוֹ מִסְפַּר מַדְבֵּקוֹת: 5. כַּמָּה מַדְבֵּקוֹת יֵשׁ לְהוֹצִיא מֵהַמְּגֵרָה כְּדֵי לְמַלֵּא אֶת כָּל הַקֻּפְסָאוֹת?","a":7,"b":5},{"id":"w176","level":2,"text":"בְּכָל יוֹם שָׁקֵד פּוֹתֶרֶת 8 תַּרְגִּילִים. הִיא הִתְמִידָה בְּכָךְ בְּמֶשֶׁךְ 6 יָמִים בְּדִיּוּק. כַּמָּה תַּרְגִּילִים פָּתְרָה בִּתְקוּפָה זוֹ?","a":6,"b":8},{"id":"w177","level":2,"text":"בְּכָל יוֹם שָׁקֵד פּוֹתֶרֶת 3 תַּרְגִּילִים. הִיא הִתְמִידָה בְּכָךְ בְּמֶשֶׁךְ 7 יָמִים בְּדִיּוּק. כַּמָּה תַּרְגִּילִים פָּתְרָה בִּתְקוּפָה זוֹ?","a":7,"b":3},{"id":"w178","level":2,"text":"בְּכָל יוֹם שָׁקֵד פּוֹתֶרֶת 6 תַּרְגִּילִים. הִיא הִתְמִידָה בְּכָךְ בְּמֶשֶׁךְ 7 יָמִים בְּדִיּוּק. כַּמָּה תַּרְגִּילִים פָּתְרָה בִּתְקוּפָה זוֹ?","a":7,"b":6},{"id":"w179","level":2,"text":"בְּכָל יוֹם שָׁקֵד פּוֹתֶרֶת 9 תַּרְגִּילִים. הִיא הִתְמִידָה בְּכָךְ בְּמֶשֶׁךְ 7 יָמִים בְּדִיּוּק. כַּמָּה תַּרְגִּילִים פָּתְרָה בִּתְקוּפָה זוֹ?","a":7,"b":9},{"id":"w180","level":2,"text":"בְּכָל יוֹם שָׁקֵד פּוֹתֶרֶת 4 תַּרְגִּילִים. הִיא הִתְמִידָה בְּכָךְ בְּמֶשֶׁךְ 8 יָמִים בְּדִיּוּק. כַּמָּה תַּרְגִּילִים פָּתְרָה בִּתְקוּפָה זוֹ?","a":8,"b":4},{"id":"w181","level":2,"text":"לְכָל תַּחֲנַת יְצִירָה מַקְצִיבִים 7 צְבָעִים. בַּחֲצַר פּוֹעֲלוֹת 7 תַּחֲנוֹת, וְהַצְּבָעִים נִשְׁאָרִים בְּכָל תַּחֲנָה. כַּמָּה צְבָעִים צָרִיךְ לְהָבִיא לַחֲצַר?","a":7,"b":7},{"id":"w182","level":2,"text":"לְכָל תַּחֲנַת יְצִירָה מַקְצִיבִים 10 צְבָעִים. בַּחֲצַר פּוֹעֲלוֹת 7 תַּחֲנוֹת, וְהַצְּבָעִים נִשְׁאָרִים בְּכָל תַּחֲנָה. כַּמָּה צְבָעִים צָרִיךְ לְהָבִיא לַחֲצַר?","a":7,"b":10},{"id":"w183","level":2,"text":"לְכָל תַּחֲנַת יְצִירָה מַקְצִיבִים 5 צְבָעִים. בַּחֲצַר פּוֹעֲלוֹת 8 תַּחֲנוֹת, וְהַצְּבָעִים נִשְׁאָרִים בְּכָל תַּחֲנָה. כַּמָּה צְבָעִים צָרִיךְ לְהָבִיא לַחֲצַר?","a":8,"b":5},{"id":"w184","level":2,"text":"לְכָל תַּחֲנַת יְצִירָה מַקְצִיבִים 8 צְבָעִים. בַּחֲצַר פּוֹעֲלוֹת 8 תַּחֲנוֹת, וְהַצְּבָעִים נִשְׁאָרִים בְּכָל תַּחֲנָה. כַּמָּה צְבָעִים צָרִיךְ לְהָבִיא לַחֲצַר?","a":8,"b":8},{"id":"w185","level":2,"text":"לְכָל תַּחֲנַת יְצִירָה מַקְצִיבִים 3 צְבָעִים. בַּחֲצַר פּוֹעֲלוֹת 9 תַּחֲנוֹת, וְהַצְּבָעִים נִשְׁאָרִים בְּכָל תַּחֲנָה. כַּמָּה צְבָעִים צָרִיךְ לְהָבִיא לַחֲצַר?","a":9,"b":3},{"id":"w186","level":2,"text":"בְּסֵפֶר יֵשׁ 8 פְּרָקִים בְּאוֹתוֹ אֹרֶךְ. כָּל פֶּרֶק מֵכִיל 6 עַמּוּדִים. כַּמָּה עַמּוּדִים יֵשׁ בְּכָל הַפְּרָקִים יַחַד, בְּלִי לִסְפֹּר אֶת הַכְּרִיכָה?","a":8,"b":6},{"id":"w187","level":2,"text":"בְּסֵפֶר יֵשׁ 8 פְּרָקִים בְּאוֹתוֹ אֹרֶךְ. כָּל פֶּרֶק מֵכִיל 9 עַמּוּדִים. כַּמָּה עַמּוּדִים יֵשׁ בְּכָל הַפְּרָקִים יַחַד, בְּלִי לִסְפֹּר אֶת הַכְּרִיכָה?","a":8,"b":9},{"id":"w188","level":2,"text":"בְּסֵפֶר יֵשׁ 9 פְּרָקִים בְּאוֹתוֹ אֹרֶךְ. כָּל פֶּרֶק מֵכִיל 4 עַמּוּדִים. כַּמָּה עַמּוּדִים יֵשׁ בְּכָל הַפְּרָקִים יַחַד, בְּלִי לִסְפֹּר אֶת הַכְּרִיכָה?","a":9,"b":4},{"id":"w189","level":2,"text":"בְּסֵפֶר יֵשׁ 9 פְּרָקִים בְּאוֹתוֹ אֹרֶךְ. כָּל פֶּרֶק מֵכִיל 7 עַמּוּדִים. כַּמָּה עַמּוּדִים יֵשׁ בְּכָל הַפְּרָקִים יַחַד, בְּלִי לִסְפֹּר אֶת הַכְּרִיכָה?","a":9,"b":7},{"id":"w190","level":2,"text":"בְּסֵפֶר יֵשׁ 9 פְּרָקִים בְּאוֹתוֹ אֹרֶךְ. כָּל פֶּרֶק מֵכִיל 10 עַמּוּדִים. כַּמָּה עַמּוּדִים יֵשׁ בְּכָל הַפְּרָקִים יַחַד, בְּלִי לִסְפֹּר אֶת הַכְּרִיכָה?","a":9,"b":10},{"id":"w191","level":2,"text":"רוֹצִים לְמַלֵּא 9 מַגָּשִׁים. בְּכָל מַגָּשׁ יֵשׁ מָקוֹם לְ־5 מַאֲפִים. כָּל הַמַּגָּשִׁים צְרִיכִים לִהְיוֹת מְלֵאִים. כַּמָּה מַאֲפִים צָרִיךְ לֶאֱפוֹת?","a":9,"b":5},{"id":"w192","level":2,"text":"רוֹצִים לְמַלֵּא 9 מַגָּשִׁים. בְּכָל מַגָּשׁ יֵשׁ מָקוֹם לְ־8 מַאֲפִים. כָּל הַמַּגָּשִׁים צְרִיכִים לִהְיוֹת מְלֵאִים. כַּמָּה מַאֲפִים צָרִיךְ לֶאֱפוֹת?","a":9,"b":8},{"id":"w193","level":2,"text":"רוֹצִים לְמַלֵּא 10 מַגָּשִׁים. בְּכָל מַגָּשׁ יֵשׁ מָקוֹם לְ־3 מַאֲפִים. כָּל הַמַּגָּשִׁים צְרִיכִים לִהְיוֹת מְלֵאִים. כַּמָּה מַאֲפִים צָרִיךְ לֶאֱפוֹת?","a":10,"b":3},{"id":"w194","level":2,"text":"רוֹצִים לְמַלֵּא 10 מַגָּשִׁים. בְּכָל מַגָּשׁ יֵשׁ מָקוֹם לְ־6 מַאֲפִים. כָּל הַמַּגָּשִׁים צְרִיכִים לִהְיוֹת מְלֵאִים. כַּמָּה מַאֲפִים צָרִיךְ לֶאֱפוֹת?","a":10,"b":6},{"id":"w195","level":2,"text":"רוֹצִים לְמַלֵּא 10 מַגָּשִׁים. בְּכָל מַגָּשׁ יֵשׁ מָקוֹם לְ־9 מַאֲפִים. כָּל הַמַּגָּשִׁים צְרִיכִים לִהְיוֹת מְלֵאִים. כַּמָּה מַאֲפִים צָרִיךְ לֶאֱפוֹת?","a":10,"b":9},{"id":"w196","level":2,"text":"בְּכָל סַבָּב שֶׁל הַמִּשְׂחָק אוֹסְפִים 4 אֲבָנִים. מְשַׂחֲקִים 10 סְבָבִים וְשׁוֹמְרִים אֶת כָּל הָאֲבָנִים שֶׁנֶּאֶסְפוּ. כַּמָּה אֲבָנִים יִהְיוּ בַּסּוֹף?","a":10,"b":4},{"id":"w197","level":2,"text":"בְּכָל סַבָּב שֶׁל הַמִּשְׂחָק אוֹסְפִים 7 אֲבָנִים. מְשַׂחֲקִים 10 סְבָבִים וְשׁוֹמְרִים אֶת כָּל הָאֲבָנִים שֶׁנֶּאֶסְפוּ. כַּמָּה אֲבָנִים יִהְיוּ בַּסּוֹף?","a":10,"b":7},{"id":"w198","level":2,"text":"בְּכָל סַבָּב שֶׁל הַמִּשְׂחָק אוֹסְפִים 10 אֲבָנִים. מְשַׂחֲקִים 10 סְבָבִים וְשׁוֹמְרִים אֶת כָּל הָאֲבָנִים שֶׁנֶּאֶסְפוּ. כַּמָּה אֲבָנִים יִהְיוּ בַּסּוֹף?","a":10,"b":10},{"id":"w199","level":2,"text":"בְּכָל סַבָּב שֶׁל הַמִּשְׂחָק אוֹסְפִים 5 אֲבָנִים. מְשַׂחֲקִים 6 סְבָבִים וְשׁוֹמְרִים אֶת כָּל הָאֲבָנִים שֶׁנֶּאֶסְפוּ. כַּמָּה אֲבָנִים יִהְיוּ בַּסּוֹף?","a":6,"b":5},{"id":"w200","level":2,"text":"בְּכָל סַבָּב שֶׁל הַמִּשְׂחָק אוֹסְפִים 8 אֲבָנִים. מְשַׂחֲקִים 6 סְבָבִים וְשׁוֹמְרִים אֶת כָּל הָאֲבָנִים שֶׁנֶּאֶסְפוּ. כַּמָּה אֲבָנִים יִהְיוּ בַּסּוֹף?","a":6,"b":8}];
"use strict";

// One personal game, persisted only in this browser. No accounts or network API.
class PersonalGame {
  static storageKey = "shaked.multiplication.personal.v5";

  constructor(bank, storage) {
    this.bank = bank;
    this.storage = storage;
    this.storageAvailable = true;
    this.state = this.fresh();
    try {
      const saved = JSON.parse(storage.getItem(PersonalGame.storageKey));
      if (saved?.version === 5) {
        for (const activity of ["quick", "words", "maze"]) {
          const level = saved.unlocked?.[activity];
          if (Number.isInteger(level) && level >= 0 && level <= 2)
            this.state.unlocked[activity] = level;
        }
        for (const activity of ["table", "quick", "words", "maze"])
          if (this.validRun(saved.runs?.[activity], activity))
            this.state.runs[activity] = saved.runs[activity];
      } else if (!saved) {
        // Retain the multiplication table from the original personal edition.
        const old = JSON.parse(storage.getItem("shaked.multiplication.v3"));
        if (old?.version === 3 && Array.isArray(old.table) && old.table.length === 100) {
          const run = this.newRun("table", 0);
          run.values = old.table.map(v => typeof v === "string" ? v.slice(0, 3) : "");
          this.state.runs.table = run;
          if (Number.isInteger(old.unlocked) && old.unlocked >= 0 && old.unlocked <= 2)
            this.state.unlocked.maze = old.unlocked;
        }
      }
    } catch { /* Unavailable or damaged saved data never blocks playing. */ }
    this.save();
  }

  fresh() {
    return { version: 5, runs: { table: null, quick: null, words: null, maze: null },
      unlocked: { quick: 0, words: 0, maze: 0 } };
  }

  validRun(r, activity) {
    if (!r || r.activity !== activity || typeof r.id !== "string" ||
        !["active", "passed", "retry"].includes(r.status) ||
        !Number.isInteger(r.level) || r.level < 0 || r.level > 2) return false;
    if (activity === "table")
      return [r.values, r.marks, r.first].every(a => Array.isArray(a) && a.length === 100) &&
        r.values.every(v => typeof v === "string" && v.length <= 3) &&
        r.marks.every(v => ["", "correct", "wrong"].includes(v)) &&
        r.first.every(v => v === null || typeof v === "boolean");
    const total = activity === "maze" ? [10, 15, 20][r.level] : 20;
    if (!Array.isArray(r.questions) || r.questions.length !== total ||
        !r.questions.every(q => Number.isInteger(q.a) && q.a >= 1 && q.a <= 10 &&
          Number.isInteger(q.b) && q.b >= 1 && q.b <= 10 &&
          (activity !== "words" || typeof q.text === "string")) ||
        !Number.isInteger(r.index) || r.index < 0 || r.index > total ||
        !Number.isInteger(r.tries) || r.tries < 0 ||
        !Number.isInteger(r.completed) || r.completed < 0 || r.completed > total ||
        !Number.isInteger(r.first_correct) || r.first_correct < 0 || r.first_correct > total ||
        !Number.isFinite(r.points) || r.points < 0 ||
        typeof r.solved !== "boolean" || typeof r.revealed !== "boolean") return false;
    if (activity !== "maze") return r.index < total;
    return Array.isArray(r.grid) && r.grid.length === 9 &&
      r.grid.every(row => Array.isArray(row) && row.length === 9 && row.every(v => v === 0 || v === 1)) &&
      [r.x, r.y, r.goal?.x, r.goal?.y].every(v => Number.isInteger(v) && v >= 0 && v < 9) &&
      r.grid[r.y][r.x] === 0 && r.grid[r.goal.y][r.goal.x] === 0 &&
      Array.isArray(r.visited) && r.visited.length === 81 &&
      Number.isInteger(r.lives) && r.lives >= 0 && r.lives <= 3 &&
      Number.isInteger(r.moves) && r.moves >= 0 && r.moves <= 3 && typeof r.pending === "boolean";
  }

  save() {
    try {
      this.storage.setItem(PersonalGame.storageKey, JSON.stringify(this.state));
      this.storageAvailable = true;
    } catch { this.storageAvailable = false; }
    return this.storageAvailable;
  }

  shuffle(items) {
    const result = [...items];
    for (let i = result.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [result[i], result[j]] = [result[j], result[i]];
    }
    return result;
  }

  newRun(activity, level) {
    const id = globalThis.crypto?.randomUUID?.() || Date.now().toString(36) + Math.random().toString(36).slice(2);
    const run = { id, activity, level, status: "active", first_correct: 0, completed: 0, score: null };
    if (activity === "table") return Object.assign(run, {
      total: 100, values: Array(100).fill(""), marks: Array(100).fill(""), first: Array(100).fill(null)
    });
    let pool;
    if (activity === "words") pool = this.bank.filter(q => q.level === level);
    else {
      pool = [];
      for (let a = [1, 2, 6][level]; a <= [5, 10, 10][level]; a++)
        for (let b = 1; b <= 10; b++) pool.push({ a, b, text: null, id: `q${a}-${b}` });
    }
    const total = activity === "maze" ? [10, 15, 20][level] : 20;
    Object.assign(run, { total, questions: this.shuffle(pool).slice(0, total),
      index: 0, tries: 0, solved: false, revealed: false, points: 0 });
    if (activity === "maze") Object.assign(run, this.makeMaze());
    return run;
  }

  makeMaze() {
    const grid = Array.from({ length: 9 }, () => Array(9).fill(1));
    const stack = [[1, 1]];
    grid[1][1] = 0;
    while (stack.length) {
      const [x, y] = stack[stack.length - 1];
      const options = [[2, 0], [-2, 0], [0, 2], [0, -2]].filter(([dx, dy]) =>
        x + dx > 0 && x + dx < 8 && y + dy > 0 && y + dy < 8 && grid[y + dy][x + dx]);
      if (!options.length) { stack.pop(); continue; }
      const [dx, dy] = options[Math.floor(Math.random() * options.length)];
      grid[y + dy / 2][x + dx / 2] = 0;
      grid[y + dy][x + dx] = 0;
      stack.push([x + dx, y + dy]);
    }
    const queue = [[1, 1]], seen = new Set([10]);
    for (let i = 0; i < queue.length; i++) {
      const [x, y] = queue[i];
      for (const [dx, dy] of [[1, 0], [-1, 0], [0, 1], [0, -1]]) {
        const nx = x + dx, ny = y + dy, key = ny * 9 + nx;
        if (grid[ny]?.[nx] === 0 && !seen.has(key)) { seen.add(key); queue.push([nx, ny]); }
      }
    }
    const [gx, gy] = queue[queue.length - 1];
    return { grid, x: 1, y: 1, goal: { x: gx, y: gy }, moves: 0, pending: false,
      lives: 3, visited: Array.from({ length: 81 }, (_, i) => i === 10) };
  }

  snapshot() {
    const result = JSON.parse(JSON.stringify(this.state));
    for (const run of Object.values(result.runs)) {
      if (!run || run.activity === "table") continue;
      const q = run.questions[run.index];
      if (q) {
        run.question = { key: `${run.id}:${run.index}`, a: q.a, b: q.b, text: q.text };
        if (run.revealed) run.question.answer = q.a * q.b;
      }
      delete run.questions;
    }
    return result;
  }

  finish(run) {
    if (run.status !== "active") return;
    run.score = Math.round(run.first_correct / run.total * 10000) / 100;
    run.status = run.score >= 80 ? "passed" : "retry";
    if (run.status === "passed" && run.activity !== "table")
      this.state.unlocked[run.activity] = Math.max(this.state.unlocked[run.activity], Math.min(2, run.level + 1));
  }

  mazeFinish(run) {
    if (run.completed === run.total && !run.pending && run.x === run.goal.x && run.y === run.goal.y)
      this.finish(run);
  }

  mazeAdvance(run) {
    Object.assign(run, { index: run.index + 1, tries: 0, solved: false, revealed: false,
      pending: false, moves: 0, lives: 3 });
    this.mazeFinish(run);
  }

  currentQuestion(run, payload) {
    if (payload.question_key !== `${run.id}:${run.index}` || !run.questions?.[run.index])
      throw new Error("הַשְּׁאֵלָה הִתְעַדְּכְנָה. נַעֲנֶה עַל הַשְּׁאֵלָה הַמֻּצֶּגֶת.");
    return run.questions[run.index];
  }

  table(action, payload) {
    let run = this.state.runs.table;
    if (payload.run_id && run?.id !== payload.run_id) throw new Error("הַלּוּחַ הִתְעַדְּכֵן.");
    if (!run || action === "table_clear") run = this.state.runs.table = this.newRun("table", 0);
    if (action === "table_clear" || run.status !== "active") return false;
    if (!Array.isArray(payload.values) || payload.values.length !== 100) throw new Error("הַלּוּחַ אֵינוֹ תַּקִּין.");
    let filled = 0, correct = 0;
    payload.values.forEach((raw, i) => {
      const value = String(raw).trim().slice(0, 3);
      const good = /^[0-9]{1,3}$/.test(value) && Number(value) === (Math.floor(i / 10) + 1) * (i % 10 + 1);
      if (value !== run.values[i]) run.marks[i] = "";
      run.values[i] = value;
      if (action === "table_clear_wrong" && value && !good) { run.values[i] = ""; run.marks[i] = ""; }
      if (action === "table_check") {
        run.marks[i] = value ? (good ? "correct" : "wrong") : "";
        if (value) { filled++; correct += Number(good); if (run.first[i] === null) run.first[i] = good; }
      }
    });
    run.first_correct = run.first.filter(v => v === true).length;
    run.completed = run.marks.filter(v => v === "correct").length;
    if (action === "table_check" && filled === 100 && correct === 100) this.finish(run);
    return action === "table_check" && filled > 0 && filled === correct;
  }

  perform(action, payload = {}) {
    let celebrate = false;
    if (action === "start") {
      const { activity, level } = payload;
      if (!["quick", "words", "maze"].includes(activity) || !Number.isInteger(level) || level < 0 || level > this.state.unlocked[activity])
        throw new Error("קֹדֶם נְסַיֵּם אֶת הָרָמָה הַקּוֹדֶמֶת עִם לְפָחוֹת 80% הַצְלָחָה.");
      if (this.state.runs[activity]?.status !== "active") this.state.runs[activity] = this.newRun(activity, level);
    } else if (["table_save", "table_check", "table_clear_wrong", "table_clear"].includes(action)) {
      celebrate = this.table(action, payload);
    } else if (action !== "sync") {
      const run = Object.values(this.state.runs).find(r => r?.id === payload.run_id);
      if (!run) throw new Error("נִפְתַּח אֶת הַמִּשְׂחָק וְנַמְשִׁיךְ.");
      if (action === "maze_restart" && run.activity === "maze") this.state.runs.maze = this.newRun("maze", run.level);
      else if (run.status === "active") {
        if (action === "move" && run.activity === "maze") {
          if (!run.pending) {
            const delta = { right: [1, 0], left: [-1, 0], up: [0, -1], down: [0, 1] }[payload.direction];
            if (!delta) throw new Error("כִּוּוּן לֹא תַּקִּין.");
            const nx = run.x + delta[0], ny = run.y + delta[1];
            if (run.grid[ny]?.[nx] === 0) {
              run.x = nx; run.y = ny; run.visited[ny * 9 + nx] = true;
              if (run.completed < run.total && ++run.moves === 3) run.pending = true;
              this.mazeFinish(run);
            }
          }
        } else if (action === "answer") {
          const q = this.currentQuestion(run, payload);
          if (run.activity === "maze" && !run.pending) throw new Error("קֹדֶם מִתְקַדְּמִים בַּמָּבוֹךְ.");
          if (!run.solved && !(run.activity === "maze" && run.revealed)) {
            const answer = String(payload.answer ?? "").trim();
            if (!/^[0-9]{1,3}$/.test(answer)) throw new Error("נַקְלִיד מִסְפָּר שָׁלֵם.");
            if (Number(answer) === q.a * q.b) {
              if (run.tries === 0) run.first_correct++;
              run.points += run.tries === 0 ? 10 : 5;
              run.solved = true; run.completed++; celebrate = true;
              if (run.activity === "maze") this.mazeAdvance(run);
              else if (run.completed === run.total) this.finish(run);
            } else {
              run.tries++;
              if (run.activity === "maze") run.lives = Math.max(0, 3 - run.tries);
              if (run.tries >= 3) run.revealed = true;
            }
          }
        } else if (action === "next" && ["quick", "words"].includes(run.activity)) {
          this.currentQuestion(run, payload);
          if (!run.solved) throw new Error("קֹדֶם נַקְלִיד תְּשׁוּבָה נְכוֹנָה.");
          Object.assign(run, { index: run.index + 1, tries: 0, solved: false, revealed: false });
        } else if (action === "maze_continue" && run.activity === "maze") {
          this.currentQuestion(run, payload);
          if (!run.pending || !run.revealed || run.tries < 3) throw new Error("קֹדֶם נַעֲנֶה עַל הַשְּׁאֵלָה.");
          run.completed++; this.mazeAdvance(run);
        } else throw new Error("פְּעֻלָּה לֹא מַתְאִימָה לַמִּשְׂחָק.");
      }
    }
    this.save();
    return { snapshot: this.snapshot(), celebrate };
  }
}

if (typeof module !== "undefined") module.exports = { PersonalGame };

"use strict";
const $ = (id) => document.getElementById(id);
const LEVEL_NAMES = ["א׳", "ב׳", "ג׳"];
let page = "home", lastHeight = 0, heightQueued = false, fireworkTimer = null;
let pending = null;
let tableDraft = Array(100).fill(""),
  draftRun = null,
  dirty = false,
  draftVersion = 0,
  saveTimer = null,
  large = false;
let questionKeys = {},
  lastMazePending = false,
  restartConfirm = false;
const esc = (value) =>
  String(value ?? "").replace(
    /[&<>"']/g,
    (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[c],
  );
const n = (value) => "<bdi>" + esc(value) + "</bdi>";
const fixed = (value) =>
  value === null || value === undefined
    ? "—"
    : Number(value).toLocaleString("he-IL", { maximumFractionDigits: 2 });
const normalizeDigits = (value) =>
  value
    .replace(/[٠-٩]/g, (c) => String(c.charCodeAt(0) - 1632))
    .replace(/[۰-۹]/g, (c) => String(c.charCodeAt(0) - 1776));
document.addEventListener(
  "input",
  (event) => {
    if (event.target.matches("input[inputmode=numeric]"))
      event.target.value = normalizeDigits(event.target.value);
  },
  true,
);

function message(type, extra = {}) {
  if (window.parent !== window)
    window.parent.postMessage({ isStreamlitMessage: true, type, ...extra }, "*");
}
function resizeFrame() {
  if (heightQueued) return;
  heightQueued = true;
  requestAnimationFrame(() => {
    heightQueued = false;
    const height = Math.ceil($("app").getBoundingClientRect().height) + 4;
    if (height !== lastHeight) {
      lastHeight = height;
      message("streamlit:setFrameHeight", { height });
    }
  });
}
function status(id, text, kind = "") {
  const el = $(id);
  if (!el) return;
  el.textContent = text;
  el.className = "status " + kind;
  resizeFrame();
}
function storageNotice() {
  $("storage-note").hidden = game.storageAvailable;
}
function rpc(action, payload = {}) {
  try {
    const reply = game.perform(action, payload);
    snapshot = reply.snapshot;
    renderAll();
    storageNotice();
    if (reply.celebrate) fireworks();
    return Promise.resolve(reply);
  } catch (error) {
    return Promise.reject(error);
  }
}
function gameButton(button, locked = false) { button.disabled = locked; }
function actionError(error, target = "global-status") {
  status(target, error.message || "הַפְּעֻלָּה לֹא הֻשְׁלְמָה. נְנַסֶּה שׁוּב.", "error");
}
window.addEventListener("message", event => {
  if (event.source === window.parent && event.data?.type === "streamlit:render") resizeFrame();
});
function navigate(next) {
  if (!["home", "table", "quick", "words", "maze"].includes(next)) return;
  if (page === "table" && next !== "table" && dirty) flushTable().catch(actionError);
  page = next;
  document.querySelectorAll(".page").forEach((el) => (el.hidden = el.id !== "page-" + page));
  document.querySelectorAll(".nav [data-page]").forEach((button) => {
    const on = button.dataset.page === page;
    button.classList.toggle("active", on);
    if (on) button.setAttribute("aria-current", "page");
    else button.removeAttribute("aria-current");
  });
  status("global-status", "");
  renderAll();
  $("app").scrollIntoView({ block: "start", behavior: "instant" });
  resizeFrame();
}
document
  .querySelectorAll("[data-page]")
  .forEach((button) => button.addEventListener("click", () => navigate(button.dataset.page)));
function renderAll() {
  renderTable();
  renderQuiz("quick");
  renderQuiz("words");
  renderMaze();
  resizeFrame();
}

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

// Preserve the spreadsheet geometry and save every edit on this device.
function createTable() {
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
        input.setAttribute("aria-label", `${r} כָּפוּל ${c}`);
        input.addEventListener("focus", () => {
          $("selected-exercise").textContent = `${r} × ${c} = ?`;
        });
        input.addEventListener("input", () => {
          tableDraft[i] = input.value;
          dirty = true;
          draftVersion++;
          cell.className = "table-cell";
          input.setAttribute("aria-invalid", "false");
          $("table-draft-note").textContent = "מַמְתִּינִים לִשְׁמִירָה…";
          status("table-status", "");
          clearTimeout(saveTimer);
          flushTable().catch(actionError);
        });
        input.addEventListener("keydown", (event) => {
          const delta = { ArrowLeft: -1, ArrowRight: 1, ArrowUp: -10, ArrowDown: 10, Enter: 1 }[
            event.key
          ];
          if (delta !== undefined && i + delta >= 0 && i + delta < 100) {
            event.preventDefault();
            $("table-" + (i + delta)).focus();
            $("table-" + (i + delta)).select();
          }
        });
        cell.append(input);
      }
      frag.append(cell);
    }
  $("times-table").replaceChildren(frag);
}
function renderTable() {
  const t = snapshot.runs.table;
  if ((t?.id || null) !== draftRun) {
    const preserve = dirty && draftRun === null && !!t;
    if (!preserve) {
      tableDraft = t ? [...t.values] : Array(100).fill("");
      dirty = false;
      draftVersion++;
    }
    draftRun = t?.id || null;
  } else if (!dirty && t) tableDraft = [...t.values];
  tableDraft.forEach((value, i) => {
    const input = $("table-" + i);
    if (document.activeElement !== input && input.value !== value) input.value = value;
    input.disabled = !!t && t.status !== "active";
    const mark = t && value === t.values[i] ? t.marks[i] : "";
    $("cell-" + i).className = "table-cell" + (mark ? " " + mark : "");
    input.setAttribute("aria-invalid", String(mark === "wrong"));
  });
  $("times-table").classList.toggle("large", large);
  $("table-zoom").setAttribute("aria-pressed", String(large));
  $("table-zoom").textContent = large ? "כָּל הַלּוּחַ בַּמָּסָךְ ⤡" : "הַגְדָּלַת הַתָּאִים ⤢";
  $("zoom-hint").hidden = !large;
  gameButton($("check-table"), !!t && t.status !== "active");
  gameButton($("clear-wrong"), !!t && t.status !== "active");
  gameButton($("clear-table"));
  if (t && t.status !== "active")
    status(
      "table-status",
      `הַלּוּחַ הֻשְׁלַם! הַצִּיּוּן ${fixed(t.score)}  לְלוּחַ חָדָשׁ לוֹחֲצִים עַל מְחִיקַת הַכֹּל.`,
      "success",
    );
}
async function tableAction(action) {
  clearTimeout(saveTimer);
  if (!snapshot) return;
  const version = draftVersion,
    values = [...tableDraft],
    run_id = draftRun;
  try {
    const reply = await rpc(action, { run_id, values });
    if (version === draftVersion) {
      dirty = false;
      renderTable();
      $("table-draft-note").textContent = game.storageAvailable ? "נִשְׁמַר ✓" : "";
    }
    if (action === "table_check" && snapshot.runs.table?.status === "active") {
      const marks = snapshot.runs.table.marks,
        correct = marks.filter((x) => x === "correct").length,
        wrong = marks.filter((x) => x === "wrong").length;
      status(
        "table-status",
        correct + wrong
          ? `${correct} תְּשׁוּבוֹת נְכוֹנוֹת מִתּוֹךְ ${correct + wrong}. ${wrong ? "אֶפְשָׁר לְתַקֵּן וְלִבְדֹּק שׁוּב." : "כָּל הַכָּבוֹד! 🎆"}`
          : "עֲדַיִן לֹא מִלֵּאנוּ תְּשׁוּבוֹת.",
        wrong ? "warning" : correct ? "success" : "",
      );
    }
    return reply;
  } catch (error) {
    $("table-draft-note").textContent = "הַשִּׁנּוּיִים עֲדַיִן לֹא נִשְׁמְרוּ.";
    throw error;
  }
}
function flushTable() {
  return dirty ? tableAction("table_save") : Promise.resolve();
}
$("check-table").addEventListener("click", () =>
  tableAction("table_check").catch((error) => actionError(error, "table-status")),
);
$("clear-wrong").addEventListener("click", () =>
  tableAction("table_clear_wrong").catch((error) => actionError(error, "table-status")),
);
$("clear-table").addEventListener("click", async () => {
  clearTimeout(saveTimer);
  dirty = false;
  draftVersion++;
  try {
    await rpc("table_clear", { run_id: draftRun });
    status("table-status", "הַטַּבְלָה נְקִיָּה. מַתְחִילִים מֵחָדָשׁ!");
  } catch (error) {
    actionError(error, "table-status");
  }
});
$("table-zoom").addEventListener("click", () => {
  large = !large;
  renderTable();
  resizeFrame();
});

function levels(activity, id) {
  const container = $(id),
    run = snapshot.runs[activity],
    opened = snapshot.unlocked[activity];
  container.replaceChildren();
  for (let level = 0; level < 3; level++) {
    const button = document.createElement("button"),
      locked = level > opened || (run?.status === "active" && run.level !== level);
    button.className = "level" + (run?.level === level ? " active" : "");
    button.dataset.level = level;
    button.dataset.activity = activity;
    button.setAttribute("aria-pressed", String(run?.level === level));
    const total = activity === "maze" ? [10, 15, 20][level] : 20;
    button.innerHTML = `<strong>${level > opened ? "🔒 " : ""}רָמָה ${LEVEL_NAMES[level]}</strong><small>${n(total)} ${activity === "maze" ? "שְׁלָבִים" : "שְׁאֵלוֹת"}</small>`;
    gameButton(button, locked);
    button.addEventListener("click", () => rpc("start", { activity, level }).catch(actionError));
    container.append(button);
  }
}
function renderQuiz(activity) {
  const run = snapshot.runs[activity];
  levels(activity, activity + "-levels");
  $(activity + "-start").hidden = !!run;
  $(activity + "-card").hidden = !run;
  if (!run) return;
  $(activity + "-progress-label").innerHTML =
    `רָמָה ${LEVEL_NAMES[run.level]} · שְׁאֵלָה ${n(Math.min(run.index + 1, 20) + " / 20")}`;
  $(activity + "-first").textContent = run.first_correct;
  $(activity + "-progress-fill").style.width = (run.completed / 20) * 100 + "%";
  const ended = run.status !== "active";
  $(activity + "-question-area").hidden = ended;
  $(activity + "-result").hidden = !ended;
  if (ended) {
    renderQuizResult(activity, run);
    return;
  }
  const q = run.question,
    input = $(activity + "-answer");
  if (questionKeys[activity] !== q.key) {
    questionKeys[activity] = q.key;
    input.value = "";
  }
  if (activity === "quick") $("quick-exercise").textContent = `${q.a} × ${q.b} = ?`;
  else $("words-question").innerHTML = esc(q.text).replace(/\d+/g, (x) => n(x));
  input.disabled = run.solved;
  gameButton($(activity + "-submit"), run.solved);
  gameButton($(activity + "-next"), !run.solved);
  $(activity + "-reveal").hidden = !run.revealed;
  if (run.revealed)
    $(activity + "-solution").textContent =
      activity === "quick" ? `${q.a} × ${q.b} = ${q.answer}` : String(q.answer);
  status(
    activity + "-status",
    run.solved
      ? "נָכוֹן! עַכְשָׁו אֶפְשָׁר לְהַמְשִׁיךְ."
      : run.tries
        ? `נְנַסֶּה שׁוּב. נִסְיוֹנוֹת שֶׁלֹּא הִצְלִיחוּ: ${run.tries}.`
        : "",
    run.solved ? "success" : run.tries ? "warning" : "",
  );
}
function renderQuizResult(activity, run) {
  const node = $(activity + "-result");
  node.replaceChildren();
  const title = document.createElement("h3");
  title.textContent =
    run.status === "passed"
      ? "כָּל הַכָּבוֹד! עָבַרְנוּ אֶת הָרָמָה 🏆"
      : "סִיַּמְנוּ סֶבֶב שֶׁל לְמִידָה 🌱";
  const value = document.createElement("bdi");
  value.className = "result-number";
  value.textContent = fixed(run.score) + " / 100";
  const text = document.createElement("p");
  text.innerHTML = `${n(run.first_correct + " / 20")} תְּשׁוּבוֹת נְכוֹנוֹת בַּנִּסָּיוֹן הָרִאשׁוֹן.${run.status === "passed" ? "" : " נְנַסֶּה שׁוּב כְּדֵי לְהַגִּיעַ לְ־" + n("80%") + "."}`;
  const actions = document.createElement("div");
  actions.className = "quiz-end-actions";
  if (run.status === "passed" && run.level < 2) {
    const next = document.createElement("button");
    next.className = "btn";
    next.textContent = "לָרָמָה הַבָּאָה ←";
    gameButton(next);
    next.addEventListener("click", () =>
      rpc("start", { activity, level: run.level + 1 }).catch(actionError),
    );
    actions.append(next);
  }
  const again = document.createElement("button");
  again.className = "btn secondary";
  again.textContent = "הַגְרָלָה חֲדָשָׁה בְּאוֹתָהּ רָמָה";
  gameButton(again);
  again.addEventListener("click", () =>
    rpc("start", { activity, level: run.level }).catch(actionError),
  );
  actions.append(again);
  node.append(title, value, text, actions);
}
for (const activity of ["quick", "words"]) {
  $(activity + "-form").addEventListener("submit", async (event) => {
    event.preventDefault();
    const run = snapshot?.runs[activity];
    if (!run || run.solved || pending) return;
    try {
      await rpc("answer", {
        run_id: run.id,
        question_key: run.question.key,
        answer: $(activity + "-answer").value,
      });
      const current = snapshot.runs[activity];
      if (current.revealed && current.tries === 3 && !current.solved) {
        $(activity + "-answer").blur();
        $(activity + "-reveal").scrollIntoView({ block: "center", behavior: "instant" });
      } else if (!current.solved) $(activity + "-answer").select();
    } catch (error) {
      actionError(error, activity + "-status");
    }
  });
  $(activity + "-next").addEventListener("click", () => {
    const run = snapshot?.runs[activity];
    if (run?.solved)
      rpc("next", { run_id: run.id, question_key: run.question.key }).catch((error) =>
        actionError(error, activity + "-status"),
      );
  });
}

function renderMaze() {
  levels("maze", "levels");
  const m = snapshot.runs.maze;
  $("maze-start").hidden = !!m;
  $("maze-panel").hidden = !m;
  if (!m) return;
  $("maze-stage").innerHTML =
    `רָמָה ${LEVEL_NAMES[m.level]} · שָׁלָב ${n(Math.min(m.completed + 1, m.total) + " / " + m.total)}`;
  $("maze-hearts").textContent = "❤️".repeat(m.lives) + "🤍".repeat(3 - m.lives);
  $("maze-hearts").setAttribute("aria-label", `נוֹתְרוּ ${m.lives} לְבָבוֹת`);
  $("maze-score").textContent = m.points;
  $("maze-progress").setAttribute("aria-valuemax", m.total);
  $("maze-progress").setAttribute("aria-valuenow", m.completed);
  $("maze-progress-fill").style.width = (m.completed / m.total) * 100 + "%";
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
  board.setAttribute("aria-label", `מַפַּת הַמָּבוֹךְ. שׁוּרָה ${m.y}, עַמּוּדָה ${m.x}.`);
  $("maze-caption").innerHTML =
    m.completed >= m.total
      ? "סִיַּמְנוּ אֶת כָּל הַשְּׁאֵלוֹת. מַגִּיעִים לַדֶּגֶל!"
      : `צְעָדִים עַד לַשְּׁאֵלָה הַבָּאָה: ${n(3 - m.moves)}`;
  $("maze-question").hidden = !m.pending || m.status !== "active";
  $("maze-end").hidden = m.status === "active";
  document
    .querySelectorAll("[data-move]")
    .forEach((button) => gameButton(button, m.pending || m.status !== "active"));
  gameButton($("maze-restart"));
  $("maze-restart").textContent = restartConfirm
    ? "לְהַתְחִיל מֵחָדָשׁ? לְחִיצָה נוֹסֶפֶת לְאִשּׁוּר"
    : "הַתְחָלַת הָרָמָה מֵחָדָשׁ ↻";
  if (m.pending) {
    const q = m.question;
    $("maze-question-title").textContent = m.revealed
      ? "נִלְמַד יַחַד אֶת הַתְּשׁוּבָה ✨"
      : "עֲצִירָה לְשְׁאֵלָה ✨";
    $("maze-exercise").textContent = `${q.a} × ${q.b} = ${m.revealed ? q.answer : "?"}`;
    $("maze-form").hidden = m.revealed;
    $("maze-reveal").hidden = !m.revealed;
    if (questionKeys.maze !== q.key) {
      $("maze-answer").value = "";
      questionKeys.maze = q.key;
    }
    gameButton($("maze-form").querySelector("button"), m.revealed);
    gameButton($("maze-continue"), !m.revealed);
    status(
      "maze-answer-status",
      m.tries && !m.revealed ? `נְנַסֶּה שׁוּב. נוֹתְרוּ ${m.lives} לְבָבוֹת.` : "",
      m.tries && !m.revealed ? "error" : "",
    );
    if (!lastMazePending && page === "maze") {
      requestAnimationFrame(() => {
        $("maze-question").scrollIntoView({ block: "center", behavior: "instant" });
        $(m.revealed ? "maze-continue" : "maze-answer").focus({ preventScroll: true });
      });
    }
  }
  lastMazePending = m.pending;
  if (m.status !== "active") renderMazeEnd(m);
}
function move(direction) {
  const m = snapshot?.runs.maze;
  if (page !== "maze" || !m || pending || m.pending || m.status !== "active") return;
  const [dx, dy] = { up: [0, -1], down: [0, 1], left: [-1, 0], right: [1, 0] }[direction];
  if (m.grid[m.y + dy]?.[m.x + dx] !== 0) {
    status("maze-status", "כָּאן יֵשׁ עֵץ. נִבְחַר כִּוּוּן אַחֵר.");
    return;
  }
  restartConfirm = false;
  status("maze-status", "");
  rpc("move", { run_id: m.id, direction }).catch((error) => actionError(error, "maze-status"));
}
document
  .querySelectorAll("[data-move]")
  .forEach((button) => button.addEventListener("click", () => move(button.dataset.move)));
document.addEventListener("keydown", (event) => {
  if (event.target.matches("input,textarea") || event.altKey || event.ctrlKey || event.metaKey)
    return;
  const direction = { ArrowUp: "up", ArrowDown: "down", ArrowLeft: "left", ArrowRight: "right" }[
    event.key
  ];
  if (page === "maze" && direction) {
    event.preventDefault();
    move(direction);
  }
});
$("maze-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  const m = snapshot?.runs.maze;
  if (!m?.pending || m.revealed || pending) return;
  try {
    await rpc("answer", {
      run_id: m.id,
      question_key: m.question.key,
      answer: $("maze-answer").value,
    });
    if (snapshot.runs.maze.pending && !snapshot.runs.maze.revealed)
      $("maze-answer").select();
    else {
      $("maze-answer").blur();
      if (snapshot.runs.maze.revealed) $("maze-continue").focus({ preventScroll: true });
    }
  } catch (error) {
    actionError(error, "maze-answer-status");
  }
});
$("maze-continue").addEventListener("click", async () => {
  const m = snapshot?.runs.maze;
  if (!m?.pending || !m.revealed || pending) return;
  try {
    await rpc("maze_continue", { run_id: m.id, question_key: m.question.key });
  } catch (error) {
    actionError(error, "maze-answer-status");
  }
});
function renderMazeEnd(m) {
  const box = $("maze-end-content");
  box.replaceChildren();
    box.innerHTML =
      '<div class="end-icon" aria-hidden="true">' +
      (m.status === "passed" ? "🏆" : "🌱") +
      "</div><h3>" +
      (m.status === "passed"
        ? "כָּל הַכָּבוֹד! הָרָמָה הֻשְׁלְמָה."
        : "הִגַּעְנוּ לַדֶּגֶל! נְנַסֶּה שׁוּב לְ־80%.") +
      "</h3>";
  const score = document.createElement("p");
  score.innerHTML = `הַצִּיּוּן ${n(fixed(m.score) + " / 100")} `;
  box.append(score);
  if (m.status === "passed" && m.level < 2) {
    const next = document.createElement("button");
    next.className = "btn";
    next.textContent = "לָרָמָה הַבָּאָה ←";
    gameButton(next);
    next.addEventListener("click", () =>
      rpc("start", { activity: "maze", level: m.level + 1 }).catch(actionError),
    );
    box.append(next);
  }
  const again = document.createElement("button");
  again.className = "btn secondary";
  again.textContent = "נִסָּיוֹן חָדָשׁ · שְׁלוֹשָׁה לְבָבוֹת";
  gameButton(again);
  again.addEventListener("click", () => rpc("maze_restart", { run_id: m.id }).catch(actionError));
  box.append(again);
}
$("maze-restart").addEventListener("click", () => {
  const m = snapshot?.runs.maze;
  if (!m) return;
  if (!restartConfirm && m.status === "active") {
    restartConfirm = true;
    renderMaze();
    return;
  }
  restartConfirm = false;
  rpc("maze_restart", { run_id: m.id }).catch((error) => actionError(error, "maze-status"));
});

let browserStorage;
try { browserStorage = window.localStorage; }
catch { browserStorage = { getItem() { return null; }, setItem() { throw new Error("unavailable"); } }; }
const game = new PersonalGame(WORD_BANK, browserStorage);
let snapshot = game.snapshot();
createTable();
renderAll();
storageNotice();
window.addEventListener("pagehide", () => { if (dirty) flushTable().catch(() => {}); });

message("streamlit:componentReady", { apiVersion: 1 });
if ("ResizeObserver" in window) new ResizeObserver(resizeFrame).observe($("app"));
window.addEventListener("resize", resizeFrame);
resizeFrame();

</script>
</body></html>'''

st.set_page_config(page_title="לוּחַ הַכֶּפֶל שֶׁל שָׁקֵד בֶּן עֶזְרָא",page_icon="🌱",layout="wide")
st.markdown("""<style>
.stApp,[data-testid="stAppViewContainer"]{background:#f7f5ee}
[data-testid="stMainBlockContainer"],.block-container{max-width:1100px;padding:.5rem .25rem 1rem}
[data-testid="stHeader"]{display:none}
@media(max-width:600px){[data-testid="stMainBlockContainer"],.block-container{padding:.25rem 0 .5rem}}
</style>""",unsafe_allow_html=True)

@st.cache_resource
def frontend_directory(html):
    directory=Path(tempfile.mkdtemp(prefix="shaked_personal_"))
    (directory/"index.html").write_text(html,encoding="utf-8")
    return str(directory)

# Stable component name retains browser storage between reloads and deployments.
widget=components.declare_component("shaked_multiplication",path=frontend_directory(APP_HTML))
widget(key="shaked_personal_v5",default=None)
