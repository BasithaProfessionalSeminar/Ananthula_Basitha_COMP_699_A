import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import json
import datetime
import uuid
import hashlib
import time
import random
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from enum import Enum

st.set_page_config(
    page_title="DecisionIQ - Business Planning",
    page_icon="",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito+Sans:wght@300;400;600;700;900&family=Bebas+Neue&family=DM+Sans:wght@300;400;500;700&display=swap');

:root {
    --bg-primary: #0a0a0f;
    --bg-secondary: #111118;
    --bg-card: #16161f;
    --bg-card-hover: #1e1e2a;
    --accent: #1ce783;
    --accent-dim: #12a05a;
    --accent-glow: rgba(28, 231, 131, 0.15);
    --accent2: #00c2ff;
    --accent2-dim: #0089b3;
    --text-primary: #f5f5f7;
    --text-secondary: #9999aa;
    --text-muted: #555566;
    --border: #2a2a38;
    --border-bright: #3a3a50;
    --danger: #ff4757;
    --warning: #ffa502;
    --purple: #a855f7;
    --shadow: 0 4px 32px rgba(0,0,0,0.5);
    --card-radius: 12px;
}

* { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
    background: var(--bg-primary) !important;
    color: var(--text-primary) !important;
    font-family: 'DM Sans', sans-serif !important;
}

[data-testid="stSidebar"] { display: none !important; }
[data-testid="collapsedControl"] { display: none !important; }
header[data-testid="stHeader"] { display: none !important; }
#MainMenu { display: none !important; }
footer { display: none !important; }

[data-testid="stAppViewContainer"] {
    background: var(--bg-primary) !important;
}

[data-testid="block-container"] {
    padding: 0 !important;
    max-width: 100% !important;
}

section[data-testid="stMain"] > div {
    padding: 0 !important;
}

div[data-testid="stVerticalBlock"] > div[data-testid="stVerticalBlock"] {
    gap: 0 !important;
}

.stButton > button {
    background: var(--accent) !important;
    color: #000 !important;
    border: none !important;
    border-radius: 6px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 700 !important;
    font-size: 14px !important;
    padding: 10px 24px !important;
    cursor: pointer !important;
    transition: all 0.2s ease !important;
    width: 100% !important;
    letter-spacing: 0.3px !important;
}

.stButton > button:hover {
    background: #22ff95 !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 20px rgba(28,231,131,0.3) !important;
}

.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div > div,
.stNumberInput > div > div > input {
    background: #0e0e16 !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text-primary) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 14px !important;
    padding: 10px 14px !important;
}

.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 2px var(--accent-glow) !important;
    outline: none !important;
}

.stSelectbox > div > div {
    background: #0e0e16 !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
}

.stSlider > div > div > div > div {
    background: var(--accent) !important;
}

.stSlider > div > div > div > div > div {
    background: var(--accent) !important;
    border: 2px solid var(--accent) !important;
}

label, .stTextInput label, .stSelectbox label, .stTextArea label, .stSlider label, .stNumberInput label {
    color: var(--text-secondary) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 12px !important;
    font-weight: 600 !important;
    letter-spacing: 0.8px !important;
    text-transform: uppercase !important;
}

.stCheckbox > label {
    color: var(--text-primary) !important;
    text-transform: none !important;
    font-size: 14px !important;
    letter-spacing: 0 !important;
}

.stSuccess, div[data-baseweb="notification"] {
    background: rgba(28,231,131,0.1) !important;
    border: 1px solid rgba(28,231,131,0.3) !important;
    border-radius: 8px !important;
    color: var(--accent) !important;
}

.stError {
    background: rgba(255,71,87,0.1) !important;
    border: 1px solid rgba(255,71,87,0.3) !important;
    border-radius: 8px !important;
    color: var(--danger) !important;
}

.stWarning {
    background: rgba(255,165,2,0.1) !important;
    border: 1px solid rgba(255,165,2,0.3) !important;
    border-radius: 8px !important;
    color: var(--warning) !important;
}

.stInfo {
    background: rgba(0,194,255,0.08) !important;
    border: 1px solid rgba(0,194,255,0.2) !important;
    border-radius: 8px !important;
    color: var(--accent2) !important;
}

[data-testid="metric-container"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--card-radius) !important;
    padding: 16px !important;
}

[data-testid="stMetricValue"] {
    color: var(--accent) !important;
    font-family: 'Bebas Neue', sans-serif !important;
    font-size: 2rem !important;
}

[data-testid="stMetricLabel"] {
    color: var(--text-secondary) !important;
    font-size: 11px !important;
    text-transform: uppercase !important;
    letter-spacing: 1px !important;
}

div.stTabs [data-baseweb="tab-list"] {
    background: transparent !important;
    border-bottom: 1px solid var(--border) !important;
    gap: 0 !important;
}

div.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: var(--text-muted) !important;
    border: none !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 13px !important;
    font-weight: 600 !important;
    padding: 12px 24px !important;
    text-transform: uppercase !important;
    letter-spacing: 1px !important;
    transition: color 0.2s !important;
}

div.stTabs [data-baseweb="tab"]:hover {
    color: var(--text-primary) !important;
}

div.stTabs [aria-selected="true"] {
    color: var(--accent) !important;
    border-bottom: 2px solid var(--accent) !important;
    background: transparent !important;
}

div.stTabs [data-baseweb="tab-panel"] {
    padding-top: 24px !important;
}

.stDataFrame, [data-testid="stDataFrame"] {
    background: var(--bg-card) !important;
    border-radius: var(--card-radius) !important;
    border: 1px solid var(--border) !important;
    overflow: hidden !important;
}

div[data-testid="stDataFrame"] table {
    background: var(--bg-card) !important;
}

div[data-testid="stDataFrame"] th {
    background: #0e0e16 !important;
    color: var(--text-secondary) !important;
    font-size: 11px !important;
    text-transform: uppercase !important;
    letter-spacing: 1px !important;
    border-bottom: 1px solid var(--border) !important;
}

div[data-testid="stDataFrame"] td {
    color: var(--text-primary) !important;
    border-bottom: 1px solid var(--border) !important;
    font-size: 13px !important;
}

.stExpander {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--card-radius) !important;
    overflow: hidden !important;
}

.stExpander summary {
    color: var(--text-primary) !important;
    font-weight: 600 !important;
    padding: 16px !important;
}

div[data-testid="stProgressBar"] > div {
    background: var(--border) !important;
    border-radius: 4px !important;
}

div[data-testid="stProgressBar"] > div > div {
    background: var(--accent) !important;
    border-radius: 4px !important;
}

.main-nav {
    background: rgba(10,10,15,0.97);
    border-bottom: 1px solid var(--border);
    padding: 0 40px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    height: 64px;
    position: sticky;
    top: 0;
    z-index: 1000;
    backdrop-filter: blur(12px);
}

.nav-logo {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 26px;
    color: var(--accent);
    letter-spacing: 3px;
    text-decoration: none;
    display: flex;
    align-items: center;
    gap: 10px;
}

.nav-logo-dot {
    width: 8px;
    height: 8px;
    background: var(--accent);
    border-radius: 50%;
    display: inline-block;
    box-shadow: 0 0 8px var(--accent);
}

.nav-user-pill {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 40px;
    padding: 6px 16px 6px 6px;
    display: inline-flex;
    align-items: center;
    gap: 10px;
    font-size: 13px;
    color: var(--text-primary);
    font-weight: 600;
}

.nav-avatar {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 13px;
    font-weight: 800;
    letter-spacing: -0.5px;
}

.role-badge {
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    padding: 2px 8px;
    border-radius: 20px;
    margin-left: 6px;
}

.role-planner { background: rgba(28,231,131,0.15); color: var(--accent); border: 1px solid rgba(28,231,131,0.3); }
.role-reviewer { background: rgba(0,194,255,0.15); color: var(--accent2); border: 1px solid rgba(0,194,255,0.3); }
.role-administrator { background: rgba(168,85,247,0.15); color: var(--purple); border: 1px solid rgba(168,85,247,0.3); }

.hero-section {
    background: linear-gradient(135deg, #0a0a0f 0%, #0d0d1a 50%, #0a0f0a 100%);
    padding: 60px 40px 40px;
    position: relative;
    overflow: hidden;
}

.hero-section::before {
    content: '';
    position: absolute;
    top: -100px;
    right: -100px;
    width: 500px;
    height: 500px;
    background: radial-gradient(circle, rgba(28,231,131,0.04) 0%, transparent 70%);
    pointer-events: none;
}

.hero-section::after {
    content: '';
    position: absolute;
    bottom: -50px;
    left: 200px;
    width: 300px;
    height: 300px;
    background: radial-gradient(circle, rgba(0,194,255,0.03) 0%, transparent 70%);
    pointer-events: none;
}

.hero-title {
    font-family: 'Nunito Sans', sans-serif;
    font-size: 52px;
    font-weight: 900;
    color: var(--text-primary);
    line-height: 1.05;
    letter-spacing: -1.5px;
    margin-bottom: 12px;
}

.hero-title span {
    color: var(--accent);
    position: relative;
}

.hero-subtitle {
    font-size: 16px;
    color: var(--text-secondary);
    font-weight: 400;
    max-width: 520px;
    line-height: 1.6;
}

.hero-breadcrumb {
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: var(--accent);
    margin-bottom: 16px;
    display: flex;
    align-items: center;
    gap: 8px;
}

.hero-breadcrumb::before {
    content: '';
    width: 20px;
    height: 2px;
    background: var(--accent);
    display: inline-block;
}

.kpi-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--card-radius);
    padding: 24px;
    position: relative;
    overflow: hidden;
    transition: border-color 0.2s, transform 0.2s;
}

.kpi-card:hover {
    border-color: var(--border-bright);
    transform: translateY(-2px);
}

.kpi-card::after {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 2px;
}

.kpi-green::after { background: var(--accent); }
.kpi-blue::after { background: var(--accent2); }
.kpi-purple::after { background: var(--purple); }
.kpi-orange::after { background: var(--warning); }
.kpi-red::after { background: var(--danger); }

.kpi-value {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 42px;
    color: var(--text-primary);
    line-height: 1;
    letter-spacing: 1px;
}

.kpi-label {
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: var(--text-muted);
    margin-top: 6px;
}

.kpi-change {
    font-size: 12px;
    font-weight: 700;
    margin-top: 8px;
}

.kpi-icon {
    position: absolute;
    top: 20px;
    right: 20px;
    font-size: 28px;
    opacity: 0.12;
}

.section-divider {
    padding: 40px 40px 20px;
}

.section-title {
    font-family: 'Nunito Sans', sans-serif;
    font-size: 22px;
    font-weight: 800;
    color: var(--text-primary);
    letter-spacing: -0.5px;
    margin-bottom: 6px;
}

.section-subtitle {
    font-size: 13px;
    color: var(--text-muted);
    font-weight: 400;
}

.content-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--card-radius);
    padding: 24px;
    margin-bottom: 16px;
    transition: border-color 0.2s;
}

.content-card:hover {
    border-color: var(--border-bright);
}

.content-card-header {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    margin-bottom: 16px;
}

.content-card-title {
    font-family: 'Nunito Sans', sans-serif;
    font-size: 17px;
    font-weight: 800;
    color: var(--text-primary);
    letter-spacing: -0.3px;
}

.content-card-meta {
    font-size: 12px;
    color: var(--text-muted);
    margin-top: 4px;
}

.status-badge {
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    padding: 3px 10px;
    border-radius: 20px;
    white-space: nowrap;
}

.status-draft { background: rgba(85,85,102,0.3); color: #888899; border: 1px solid rgba(85,85,102,0.4); }
.status-active { background: rgba(28,231,131,0.1); color: var(--accent); border: 1px solid rgba(28,231,131,0.25); }
.status-submitted { background: rgba(0,194,255,0.1); color: var(--accent2); border: 1px solid rgba(0,194,255,0.25); }
.status-approved { background: rgba(28,231,131,0.15); color: #22ff95; border: 1px solid rgba(28,231,131,0.4); }
.status-rejected { background: rgba(255,71,87,0.1); color: var(--danger); border: 1px solid rgba(255,71,87,0.25); }
.status-revision { background: rgba(255,165,2,0.1); color: var(--warning); border: 1px solid rgba(255,165,2,0.25); }
.status-archived { background: rgba(168,85,247,0.1); color: var(--purple); border: 1px solid rgba(168,85,247,0.25); }

.progress-bar-wrap {
    background: #1a1a24;
    border-radius: 4px;
    height: 6px;
    overflow: hidden;
    margin-top: 8px;
}

.progress-bar-fill {
    height: 100%;
    border-radius: 4px;
    transition: width 0.6s ease;
}

.tag-row {
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
    margin-top: 12px;
}

.tag {
    background: rgba(255,255,255,0.04);
    border: 1px solid var(--border);
    border-radius: 4px;
    padding: 3px 10px;
    font-size: 11px;
    color: var(--text-secondary);
    font-weight: 600;
}

.score-ring {
    display: inline-flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}

.divider-line {
    height: 1px;
    background: var(--border);
    margin: 24px 0;
}

.auth-wrap {
    min-height: 100vh;
    background: var(--bg-primary);
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
    overflow: hidden;
}

.auth-bg-grid {
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    background-image: 
        linear-gradient(rgba(28,231,131,0.03) 1px, transparent 1px),
        linear-gradient(90deg, rgba(28,231,131,0.03) 1px, transparent 1px);
    background-size: 60px 60px;
    pointer-events: none;
    z-index: 0;
}

.auth-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 48px 44px;
    width: 100%;
    max-width: 440px;
    position: relative;
    z-index: 1;
    box-shadow: 0 24px 80px rgba(0,0,0,0.6);
}

.auth-logo {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 36px;
    color: var(--accent);
    letter-spacing: 4px;
    text-align: center;
    margin-bottom: 8px;
}

.auth-tagline {
    font-size: 13px;
    color: var(--text-muted);
    text-align: center;
    margin-bottom: 36px;
    letter-spacing: 0.3px;
}

.auth-title {
    font-family: 'Nunito Sans', sans-serif;
    font-size: 24px;
    font-weight: 800;
    color: var(--text-primary);
    margin-bottom: 4px;
    letter-spacing: -0.5px;
}

.auth-sub {
    font-size: 13px;
    color: var(--text-muted);
    margin-bottom: 28px;
}

.alt-action {
    text-align: center;
    margin-top: 20px;
    font-size: 13px;
    color: var(--text-muted);
}

.alt-action a {
    color: var(--accent);
    font-weight: 700;
    text-decoration: none;
    cursor: pointer;
}

.activity-item {
    display: flex;
    align-items: flex-start;
    gap: 12px;
    padding: 12px 0;
    border-bottom: 1px solid var(--border);
}

.activity-item:last-child { border-bottom: none; }

.activity-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    margin-top: 5px;
    flex-shrink: 0;
}

.activity-text {
    font-size: 13px;
    color: var(--text-secondary);
    line-height: 1.5;
}

.activity-time {
    font-size: 11px;
    color: var(--text-muted);
    margin-top: 3px;
    font-weight: 600;
    letter-spacing: 0.5px;
}

.rank-table {
    width: 100%;
    border-collapse: collapse;
}

.rank-table th {
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: var(--text-muted);
    padding: 10px 14px;
    text-align: left;
    border-bottom: 1px solid var(--border);
    background: #0e0e16;
}

.rank-table td {
    padding: 12px 14px;
    font-size: 13px;
    color: var(--text-primary);
    border-bottom: 1px solid rgba(255,255,255,0.04);
    vertical-align: middle;
}

.rank-table tr:last-child td { border-bottom: none; }

.rank-table tr:hover td { background: rgba(255,255,255,0.02); }

.rank-num {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 20px;
    color: var(--text-muted);
}

.rank-num.top { color: var(--accent); }

.score-pill {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 700;
}

.score-high { background: rgba(28,231,131,0.12); color: var(--accent); border: 1px solid rgba(28,231,131,0.25); }
.score-med { background: rgba(255,165,2,0.1); color: var(--warning); border: 1px solid rgba(255,165,2,0.2); }
.score-low { background: rgba(255,71,87,0.1); color: var(--danger); border: 1px solid rgba(255,71,87,0.2); }

.chart-container {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--card-radius);
    padding: 24px;
    margin-bottom: 16px;
}

.chart-title {
    font-family: 'Nunito Sans', sans-serif;
    font-size: 16px;
    font-weight: 800;
    color: var(--text-primary);
    letter-spacing: -0.3px;
    margin-bottom: 4px;
}

.chart-subtitle {
    font-size: 12px;
    color: var(--text-muted);
    margin-bottom: 16px;
}

.feedback-card {
    background: #0d0d16;
    border: 1px solid var(--border);
    border-left: 3px solid var(--accent2);
    border-radius: 8px;
    padding: 16px;
    margin-bottom: 12px;
}

.feedback-author {
    font-size: 12px;
    font-weight: 700;
    color: var(--accent2);
    letter-spacing: 0.5px;
    text-transform: uppercase;
    margin-bottom: 6px;
}

.feedback-text {
    font-size: 13px;
    color: var(--text-secondary);
    line-height: 1.6;
}

.feedback-time {
    font-size: 11px;
    color: var(--text-muted);
    margin-top: 6px;
}

.empty-state {
    text-align: center;
    padding: 60px 20px;
    color: var(--text-muted);
}

.empty-state-icon {
    font-size: 48px;
    margin-bottom: 16px;
    opacity: 0.4;
}

.empty-state-text {
    font-size: 15px;
    font-weight: 600;
    color: var(--text-secondary);
    margin-bottom: 6px;
}

.empty-state-sub {
    font-size: 13px;
    color: var(--text-muted);
    max-width: 320px;
    margin: 0 auto;
    line-height: 1.6;
}

.page-pad {
    padding: 32px 40px;
}

.grid-2 {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 16px;
}

.grid-3 {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap: 16px;
}

.grid-4 {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;
}

.inline-badge {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    font-size: 11px;
    font-weight: 700;
    padding: 2px 8px;
    border-radius: 4px;
    letter-spacing: 0.5px;
}

.constraint-row {
    background: #0e0e16;
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 12px 16px;
    margin-bottom: 8px;
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.constraint-name {
    font-size: 13px;
    font-weight: 700;
    color: var(--text-primary);
}

.constraint-range {
    font-size: 12px;
    color: var(--text-muted);
    margin-top: 2px;
}

.log-entry {
    display: flex;
    gap: 12px;
    padding: 10px 0;
    border-bottom: 1px solid rgba(255,255,255,0.04);
    font-size: 13px;
}

.log-time {
    color: var(--text-muted);
    font-size: 11px;
    font-weight: 600;
    white-space: nowrap;
    min-width: 90px;
    padding-top: 1px;
}

.log-action {
    color: var(--text-secondary);
}

.log-action strong { color: var(--text-primary); font-weight: 700; }
.log-action .log-green { color: var(--accent); font-weight: 700; }
.log-action .log-blue { color: var(--accent2); font-weight: 700; }
.log-action .log-red { color: var(--danger); font-weight: 700; }
.log-action .log-purple { color: var(--purple); font-weight: 700; }

.sensitivity-bar {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 10px;
}

.sensitivity-label {
    font-size: 12px;
    font-weight: 700;
    color: var(--text-secondary);
    min-width: 100px;
}

.sensitivity-track {
    flex: 1;
    height: 8px;
    background: #1a1a24;
    border-radius: 4px;
    overflow: hidden;
}

.sensitivity-fill {
    height: 100%;
    border-radius: 4px;
}

.sensitivity-val {
    font-size: 12px;
    font-weight: 700;
    color: var(--text-primary);
    min-width: 44px;
    text-align: right;
}

.obj-row {
    background: #0e0e16;
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 14px 16px;
    margin-bottom: 8px;
}

.obj-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 8px;
}

.obj-name {
    font-size: 14px;
    font-weight: 700;
    color: var(--text-primary);
}

.obj-type {
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1px;
    text-transform: uppercase;
}

.obj-type-min { color: var(--danger); }
.obj-type-max { color: var(--accent); }

.weight-display {
    display: flex;
    align-items: center;
    gap: 8px;
}

.weight-val {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 22px;
    color: var(--accent);
}

.weight-label {
    font-size: 10px;
    color: var(--text-muted);
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.user-row {
    display: flex;
    align-items: center;
    gap: 16px;
    padding: 14px 18px;
    background: #0e0e16;
    border: 1px solid var(--border);
    border-radius: 8px;
    margin-bottom: 8px;
    transition: border-color 0.2s;
}

.user-row:hover { border-color: var(--border-bright); }

.user-avatar-sm {
    width: 38px;
    height: 38px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 14px;
    font-weight: 900;
    flex-shrink: 0;
}

.user-info { flex: 1; }

.user-name {
    font-size: 14px;
    font-weight: 700;
    color: var(--text-primary);
}

.user-email {
    font-size: 12px;
    color: var(--text-muted);
}

.deactivated-badge {
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 1px;
    text-transform: uppercase;
    color: var(--danger);
    background: rgba(255,71,87,0.1);
    border: 1px solid rgba(255,71,87,0.2);
    padding: 2px 8px;
    border-radius: 4px;
}

.template-card {
    background: #0e0e16;
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 16px;
    margin-bottom: 8px;
    transition: border-color 0.2s;
}

.template-card:hover { border-color: rgba(28,231,131,0.3); }

.template-name {
    font-size: 14px;
    font-weight: 700;
    color: var(--text-primary);
    margin-bottom: 4px;
}

.template-desc {
    font-size: 12px;
    color: var(--text-muted);
    line-height: 1.5;
}

.eval-method-card {
    background: #0e0e16;
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 16px;
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.method-name {
    font-size: 14px;
    font-weight: 700;
    color: var(--text-primary);
}

.method-desc {
    font-size: 12px;
    color: var(--text-muted);
    margin-top: 3px;
}

.toggle-on {
    background: rgba(28,231,131,0.15);
    color: var(--accent);
    border: 1px solid rgba(28,231,131,0.3);
    padding: 3px 12px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1px;
}

.toggle-off {
    background: rgba(85,85,102,0.2);
    color: var(--text-muted);
    border: 1px solid var(--border);
    padding: 3px 12px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1px;
}

.assumption-row {
    background: #0e0e16;
    border: 1px solid var(--border);
    border-left: 3px solid rgba(168,85,247,0.5);
    border-radius: 8px;
    padding: 12px 16px;
    margin-bottom: 8px;
}

.assumption-text {
    font-size: 13px;
    color: var(--text-secondary);
    line-height: 1.6;
}

.compare-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 13px;
}

.compare-table th {
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: var(--text-muted);
    padding: 10px 16px;
    background: #0e0e16;
    border-bottom: 1px solid var(--border);
    text-align: center;
}

.compare-table th:first-child { text-align: left; }

.compare-table td {
    padding: 12px 16px;
    border-bottom: 1px solid rgba(255,255,255,0.04);
    text-align: center;
    color: var(--text-secondary);
}

.compare-table td:first-child {
    text-align: left;
    font-weight: 700;
    color: var(--text-primary);
}

.compare-table tr:last-child td { border-bottom: none; }

.best-cell {
    color: var(--accent) !important;
    font-weight: 700 !important;
    background: rgba(28,231,131,0.05) !important;
}

div[data-testid="stHorizontalBlock"] > div {
    gap: 16px !important;
}

.page-actions {
    display: flex;
    gap: 12px;
    align-items: center;
    margin-top: 20px;
}

.btn-primary {
    background: var(--accent);
    color: #000;
    border: none;
    border-radius: 6px;
    padding: 10px 24px;
    font-size: 13px;
    font-weight: 700;
    cursor: pointer;
    letter-spacing: 0.3px;
    transition: background 0.2s;
}

.btn-secondary {
    background: transparent;
    color: var(--text-primary);
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 10px 24px;
    font-size: 13px;
    font-weight: 700;
    cursor: pointer;
    transition: border-color 0.2s;
}

.btn-danger {
    background: rgba(255,71,87,0.1);
    color: var(--danger);
    border: 1px solid rgba(255,71,87,0.3);
    border-radius: 6px;
    padding: 10px 24px;
    font-size: 13px;
    font-weight: 700;
    cursor: pointer;
}

.radar-legend {
    display: flex;
    gap: 16px;
    margin-top: 12px;
    flex-wrap: wrap;
}

.radar-legend-item {
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 12px;
    color: var(--text-secondary);
}

.radar-legend-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
}

.scrollable-list {
    max-height: 320px;
    overflow-y: auto;
    padding-right: 4px;
}

.scrollable-list::-webkit-scrollbar { width: 4px; }
.scrollable-list::-webkit-scrollbar-track { background: transparent; }
.scrollable-list::-webkit-scrollbar-thumb { background: var(--border); border-radius: 4px; }

.highlight-box {
    background: rgba(28,231,131,0.06);
    border: 1px solid rgba(28,231,131,0.2);
    border-radius: 8px;
    padding: 14px 18px;
    margin-bottom: 12px;
}

.highlight-box-blue {
    background: rgba(0,194,255,0.05);
    border: 1px solid rgba(0,194,255,0.2);
    border-radius: 8px;
    padding: 14px 18px;
    margin-bottom: 12px;
}

.form-section {
    margin-bottom: 20px;
}

.form-section-title {
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: var(--accent);
    margin-bottom: 14px;
    display: flex;
    align-items: center;
    gap: 8px;
}

.form-section-title::after {
    content: '';
    flex: 1;
    height: 1px;
    background: rgba(28,231,131,0.15);
}

.scenario-list-item {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--card-radius);
    padding: 20px 24px;
    margin-bottom: 12px;
    transition: all 0.2s;
    cursor: pointer;
}

.scenario-list-item:hover {
    border-color: rgba(28,231,131,0.3);
    background: var(--bg-card-hover);
    transform: translateY(-1px);
}

.scenario-name {
    font-family: 'Nunito Sans', sans-serif;
    font-size: 16px;
    font-weight: 800;
    color: var(--text-primary);
    margin-bottom: 4px;
    letter-spacing: -0.3px;
}

.scenario-desc {
    font-size: 13px;
    color: var(--text-muted);
    margin-bottom: 12px;
    line-height: 1.5;
}

.scenario-meta {
    display: flex;
    gap: 20px;
    align-items: center;
    flex-wrap: wrap;
}

.scenario-meta-item {
    font-size: 11px;
    color: var(--text-muted);
    font-weight: 600;
    display: flex;
    align-items: center;
    gap: 5px;
}

.scenario-meta-item strong {
    color: var(--text-secondary);
}
</style>
""", unsafe_allow_html=True)

class UserRole(Enum):
    PLANNER = "planner"
    REVIEWER = "reviewer"
    ADMINISTRATOR = "administrator"

class ScenarioStatus(Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    SUBMITTED = "submitted"
    APPROVED = "approved"
    REJECTED = "rejected"
    REVISION = "revision"
    ARCHIVED = "archived"

@dataclass
class Goal:
    id: str
    name: str
    weight: float
    goal_type: str
    min_val: float
    max_val: float
    description: str = ""

    def validate_value(self, val):
        return self.min_val <= val <= self.max_val

    def set_weight(self, w):
        self.weight = max(0.0, min(1.0, w))

@dataclass
class Constraint:
    id: str
    name: str
    min_val: float
    max_val: float
    unit: str = ""
    description: str = ""

@dataclass
class DecisionAlternative:
    id: str
    name: str
    description: str
    goal_values: Dict[str, float] = field(default_factory=dict)
    excluded: bool = False

    def set_goal_value(self, goal_id, val):
        self.goal_values[goal_id] = val

@dataclass
class EvaluationResult:
    id: str
    timestamp: str
    scores: Dict[str, float]
    ranked: List[tuple]
    weights_snapshot: Dict[str, float]
    feasible: Dict[str, bool]

@dataclass
class RevisionLog:
    id: str
    timestamp: str
    author: str
    action: str
    note: str

@dataclass
class PlanningScenario:
    id: str
    name: str
    description: str
    owner: str
    created: str
    status: str
    goals: List[Goal] = field(default_factory=list)
    constraints: List[Constraint] = field(default_factory=list)
    alternatives: List[DecisionAlternative] = field(default_factory=list)
    eval_results: List[EvaluationResult] = field(default_factory=list)
    assumptions: List[str] = field(default_factory=list)
    reviewer_feedback: str = ""
    approved_alt: str = ""
    revision_log: List[RevisionLog] = field(default_factory=list)
    submitted_to: str = ""

    def add_goal(self, g):
        self.goals.append(g)

    def add_alternative(self, a):
        self.alternatives.append(a)

    def add_assumption(self, text):
        self.assumptions.append(text)

    def change_status(self, s):
        self.status = s

    def log_revision(self, author, action, note=""):
        entry = RevisionLog(
            id=str(uuid.uuid4())[:8],
            timestamp=datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
            author=author,
            action=action,
            note=note
        )
        self.revision_log.append(entry)

    def rank_alternatives(self, result_idx=-1):
        if not self.eval_results:
            return []
        res = self.eval_results[result_idx]
        return res.ranked

    def evaluate(self):
        active_alts = [a for a in self.alternatives if not a.excluded]
        if not self.goals or not active_alts:
            return None
        total_weight = sum(g.weight for g in self.goals)
        if total_weight == 0:
            return None

        all_vals = {g.id: [] for g in self.goals}
        for a in active_alts:
            for g in self.goals:
                v = a.goal_values.get(g.id, 0)
                all_vals[g.id].append(v)

        scores = {}
        feasible = {}
        for a in active_alts:
            score = 0.0
            feasible[a.id] = True
            for c in self.constraints:
                found = False
                for g in self.goals:
                    if g.name.lower() in c.name.lower() or c.name.lower() in g.name.lower():
                        val = a.goal_values.get(g.id, 0)
                        if not (c.min_val <= val <= c.max_val):
                            feasible[a.id] = False
                        found = True
                if not found:
                    pass
            for g in self.goals:
                raw = a.goal_values.get(g.id, 0)
                vals = all_vals[g.id]
                mn, mx = min(vals), max(vals)
                if mx == mn:
                    norm = 0.5
                else:
                    norm = (raw - mn) / (mx - mn)
                if g.goal_type == "minimize":
                    norm = 1.0 - norm
                score += (g.weight / total_weight) * norm
            scores[a.id] = round(score * 100, 2)

        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        weights_snap = {g.id: g.weight for g in self.goals}
        res = EvaluationResult(
            id=str(uuid.uuid4())[:8],
            timestamp=datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
            scores=scores,
            ranked=ranked,
            weights_snapshot=weights_snap,
            feasible=feasible
        )
        self.eval_results.append(res)
        return res

@dataclass
class User:
    id: str
    username: str
    password_hash: str
    role: str
    name: str
    email: str
    active: bool = True

    def authenticate(self, pwd):
        return self.password_hash == hashlib.sha256(pwd.encode()).hexdigest() and self.active

    def deactivate(self):
        self.active = False

class EvaluationService:
    def __init__(self):
        self.enabled = True
        self.decision_model = "weighted_scoring"
        self.weight_min = 0.0
        self.weight_max = 1.0
        self.max_alts = 50

    def validate_scenario(self, scenario):
        if not scenario.goals:
            return False, "No goals defined"
        if not scenario.alternatives:
            return False, "No alternatives defined"
        for g in scenario.goals:
            if not (self.weight_min <= g.weight <= self.weight_max):
                return False, f"Weight for '{g.name}' out of range"
        for a in scenario.alternatives:
            for g in scenario.goals:
                if g.id not in a.goal_values:
                    return False, f"Missing value for goal '{g.name}' in alternative '{a.name}'"
        return True, "OK"

    def calc_scores(self, scenario):
        return scenario.evaluate()

class Administrator:
    def __init__(self, user, db):
        self.user = user
        self.db = db

    def create_user(self, username, name, email, role, password):
        uid = str(uuid.uuid4())[:10]
        ph = hashlib.sha256(password.encode()).hexdigest()
        new_user = User(id=uid, username=username, password_hash=ph, role=role, name=name, email=email)
        self.db["users"][username] = new_user
        self.db["activity_log"].append({
            "time": datetime.datetime.now().strftime("%H:%M"),
            "text": f"Admin <strong>{self.user.name}</strong> created account for <span class='log-green'>{name}</span> ({role})",
            "color": "#a855f7"
        })
        return new_user

    def assign_role(self, username, new_role):
        if username in self.db["users"]:
            self.db["users"][username].role = new_role
            self.db["activity_log"].append({
                "time": datetime.datetime.now().strftime("%H:%M"),
                "text": f"Role updated for <strong>{username}</strong> to <span class='log-purple'>{new_role}</span>",
                "color": "#a855f7"
            })

    def archive_scenario(self, scenario_id):
        for s in self.db["scenarios"]:
            if s.id == scenario_id:
                s.change_status(ScenarioStatus.ARCHIVED.value)
                s.log_revision(self.user.name, "Archived scenario")
                self.db["activity_log"].append({
                    "time": datetime.datetime.now().strftime("%H:%M"),
                    "text": f"Scenario <strong>{s.name}</strong> archived by <span class='log-purple'>{self.user.name}</span>",
                    "color": "#a855f7"
                })

    def configure_evaluation(self, model, wmin, wmax, enabled):
        self.db["eval_service"].decision_model = model
        self.db["eval_service"].weight_min = wmin
        self.db["eval_service"].weight_max = wmax
        self.db["eval_service"].enabled = enabled

class Planner:
    def __init__(self, user, db):
        self.user = user
        self.db = db

    def create_scenario(self, name, description):
        sid = str(uuid.uuid4())[:10]
        s = PlanningScenario(
            id=sid, name=name, description=description,
            owner=self.user.username,
            created=datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
            status=ScenarioStatus.DRAFT.value
        )
        s.log_revision(self.user.name, "Scenario created")
        self.db["scenarios"].append(s)
        self.db["activity_log"].append({
            "time": datetime.datetime.now().strftime("%H:%M"),
            "text": f"<strong>{self.user.name}</strong> created scenario <span class='log-green'>{name}</span>",
            "color": "#1ce783"
        })
        return s

    def duplicate_scenario(self, scenario):
        new_s = PlanningScenario(
            id=str(uuid.uuid4())[:10],
            name=f"{scenario.name} (Copy)",
            description=scenario.description,
            owner=self.user.username,
            created=datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
            status=ScenarioStatus.DRAFT.value
        )
        for g in scenario.goals:
            new_g = Goal(id=str(uuid.uuid4())[:8], name=g.name, weight=g.weight,
                         goal_type=g.goal_type, min_val=g.min_val, max_val=g.max_val,
                         description=g.description)
            new_s.goals.append(new_g)
        for c in scenario.constraints:
            new_c = Constraint(id=str(uuid.uuid4())[:8], name=c.name,
                               min_val=c.min_val, max_val=c.max_val, unit=c.unit)
            new_s.constraints.append(new_c)
        for a in scenario.alternatives:
            new_a = DecisionAlternative(id=str(uuid.uuid4())[:8], name=a.name,
                                        description=a.description,
                                        goal_values=dict(a.goal_values))
            new_s.alternatives.append(new_a)
        new_s.assumptions = list(scenario.assumptions)
        new_s.log_revision(self.user.name, "Duplicated from scenario: " + scenario.name)
        self.db["scenarios"].append(new_s)
        self.db["activity_log"].append({
            "time": datetime.datetime.now().strftime("%H:%M"),
            "text": f"<strong>{self.user.name}</strong> duplicated scenario <span class='log-blue'>{scenario.name}</span>",
            "color": "#00c2ff"
        })
        return new_s

    def submit_scenario(self, scenario, reviewer_username):
        ok, msg = self.db["eval_service"].validate_scenario(scenario)
        if not ok:
            return False, msg
        if not scenario.eval_results:
            return False, "Please evaluate the scenario before submitting"
        scenario.change_status(ScenarioStatus.SUBMITTED.value)
        scenario.submitted_to = reviewer_username
        scenario.log_revision(self.user.name, f"Submitted for review to {reviewer_username}")
        self.db["activity_log"].append({
            "time": datetime.datetime.now().strftime("%H:%M"),
            "text": f"<strong>{self.user.name}</strong> submitted scenario <span class='log-blue'>{scenario.name}</span> for review",
            "color": "#00c2ff"
        })
        return True, "Submitted"

    def analyze_scenario(self, scenario):
        return scenario.eval_results[-1] if scenario.eval_results else None

    def select_alternative(self, scenario, alt_id):
        scenario.approved_alt = alt_id
        scenario.log_revision(self.user.name, f"Selected preferred alternative: {alt_id}")

class Reviewer:
    def __init__(self, user, db):
        self.user = user
        self.db = db

    def review_scenario(self, scenario):
        return scenario

    def approve_scenario(self, scenario, alt_id, note=""):
        scenario.change_status(ScenarioStatus.APPROVED.value)
        scenario.approved_alt = alt_id
        scenario.reviewer_feedback = note
        scenario.log_revision(self.user.name, f"APPROVED - Alternative: {alt_id}", note)
        self.db["activity_log"].append({
            "time": datetime.datetime.now().strftime("%H:%M"),
            "text": f"<span class='log-green'>Reviewer {self.user.name}</span> approved scenario <strong>{scenario.name}</strong>",
            "color": "#1ce783"
        })

    def reject_scenario(self, scenario, feedback):
        scenario.change_status(ScenarioStatus.REJECTED.value)
        scenario.reviewer_feedback = feedback
        scenario.log_revision(self.user.name, "REJECTED", feedback)
        self.db["activity_log"].append({
            "time": datetime.datetime.now().strftime("%H:%M"),
            "text": f"<span class='log-red'>Reviewer {self.user.name}</span> rejected scenario <strong>{scenario.name}</strong>",
            "color": "#ff4757"
        })

    def request_revision(self, scenario, feedback):
        scenario.change_status(ScenarioStatus.REVISION.value)
        scenario.reviewer_feedback = feedback
        scenario.log_revision(self.user.name, "REVISION REQUESTED", feedback)
        self.db["activity_log"].append({
            "time": datetime.datetime.now().strftime("%H:%M"),
            "text": f"<span class='log-blue'>Reviewer {self.user.name}</span> requested revision on <strong>{scenario.name}</strong>",
            "color": "#00c2ff"
        })

def hash_pw(pw):
    return hashlib.sha256(pw.encode()).hexdigest()

def init_db():
    if "db" not in st.session_state:
        eval_svc = EvaluationService()
        users = {
            "admin": User(id="u001", username="admin", password_hash=hash_pw("Admin@123"),
                          role=UserRole.ADMINISTRATOR.value, name="System Admin", email="admin@decisioniq.com"),
            "alice": User(id="u002", username="alice", password_hash=hash_pw("Alice@123"),
                          role=UserRole.PLANNER.value, name="Alice Johnson", email="alice@decisioniq.com"),
            "bob": User(id="u003", username="bob", password_hash=hash_pw("Bob@123"),
                        role=UserRole.PLANNER.value, name="Bob Martinez", email="bob@decisioniq.com"),
            "carol": User(id="u004", username="carol", password_hash=hash_pw("Carol@123"),
                          role=UserRole.REVIEWER.value, name="Carol Thompson", email="carol@decisioniq.com"),
            "david": User(id="u005", username="david", password_hash=hash_pw("David@123"),
                          role=UserRole.REVIEWER.value, name="David Patel", email="david@decisioniq.com"),
        }

        g1 = Goal(id="g1", name="Cost Reduction", weight=0.35, goal_type="minimize", min_val=0, max_val=500000, description="Minimize operational costs")
        g2 = Goal(id="g2", name="Efficiency", weight=0.30, goal_type="maximize", min_val=0, max_val=100, description="Maximize process efficiency (%)")
        g3 = Goal(id="g3", name="Risk Score", weight=0.20, goal_type="minimize", min_val=0, max_val=10, description="Minimize risk exposure")
        g4 = Goal(id="g4", name="Revenue Impact", weight=0.15, goal_type="maximize", min_val=0, max_val=1000000, description="Maximize revenue impact")

        c1 = Constraint(id="c1", name="Budget Limit", min_val=0, max_val=300000, unit="USD")
        c2 = Constraint(id="c2", name="Efficiency Floor", min_val=50, max_val=100, unit="%")

        a1 = DecisionAlternative(id="a1", name="Digital Transformation", description="Full cloud migration and automation",
                                 goal_values={"g1": 180000, "g2": 88, "g3": 3.2, "g4": 750000})
        a2 = DecisionAlternative(id="a2", name="Process Optimization", description="Lean methodology implementation",
                                 goal_values={"g1": 95000, "g2": 75, "g3": 2.1, "g4": 420000})
        a3 = DecisionAlternative(id="a3", name="Hybrid Approach", description="Selective automation with process redesign",
                                 goal_values={"g1": 135000, "g2": 82, "g3": 2.8, "g4": 590000})
        a4 = DecisionAlternative(id="a4", name="Status Quo+", description="Incremental improvements to current state",
                                 goal_values={"g1": 55000, "g2": 62, "g3": 1.5, "g4": 210000})
        a5 = DecisionAlternative(id="a5", name="Outsourcing", description="Strategic outsourcing of non-core functions",
                                 goal_values={"g1": 220000, "g2": 70, "g3": 5.5, "g4": 380000})

        s1 = PlanningScenario(id="sc001", name="Q3 Operational Planning", description="Multi-objective analysis for Q3 operational strategy selection",
                              owner="alice", created="2026-04-15 09:30", status=ScenarioStatus.APPROVED.value,
                              goals=[g1, g2, g3, g4], constraints=[c1, c2],
                              alternatives=[a1, a2, a3, a4, a5])
        s1.assumptions = [
            "Cost figures are based on 12-month projections with 5% variance allowance",
            "Efficiency scores represent steady-state performance after 6-month ramp-up",
            "Risk scores use a 10-point scale validated against industry benchmarks",
            "Revenue impact assumes stable market conditions through Q4"
        ]
        s1.evaluate()
        s1.approved_alt = "a1"
        s1.reviewer_feedback = "Excellent analysis. Digital Transformation clearly dominates on strategic objectives. Approved."
        s1.submitted_to = "carol"
        s1.log_revision("Alice Johnson", "Scenario created")
        s1.log_revision("Alice Johnson", "Goals and alternatives defined")
        s1.log_revision("Alice Johnson", "Submitted for review to carol")
        s1.log_revision("Carol Thompson", "APPROVED - Alternative: a1", "Excellent analysis.")

        g5 = Goal(id="g5", name="Market Share", weight=0.40, goal_type="maximize", min_val=0, max_val=100, description="Market share gain (%)")
        g6 = Goal(id="g6", name="Investment Cost", weight=0.35, goal_type="minimize", min_val=0, max_val=5000000, description="Total investment required")
        g7 = Goal(id="g7", name="Time to Market", weight=0.25, goal_type="minimize", min_val=0, max_val=24, description="Months to market launch")

        b1 = DecisionAlternative(id="b1", name="Product A - Premium", description="High-end market positioning",
                                 goal_values={"g5": 18, "g6": 2800000, "g7": 14})
        b2 = DecisionAlternative(id="b2", name="Product B - Value", description="Mass market value proposition",
                                 goal_values={"g5": 32, "g6": 1200000, "g7": 8})
        b3 = DecisionAlternative(id="b3", name="Product C - Niche", description="Specialized niche focus",
                                 goal_values={"g5": 9, "g6": 600000, "g7": 5})

        s2 = PlanningScenario(id="sc002", name="Product Launch Strategy 2026", description="Evaluating three product launch alternatives for Q4 2026",
                              owner="bob", created="2026-04-28 14:15", status=ScenarioStatus.SUBMITTED.value,
                              goals=[g5, g6, g7], alternatives=[b1, b2, b3])
        s2.assumptions = ["Market projections based on industry analyst reports for FY2026"]
        s2.submitted_to = "david"
        s2.evaluate()
        s2.log_revision("Bob Martinez", "Scenario created")
        s2.log_revision("Bob Martinez", "Submitted for review to david")

        g8 = Goal(id="g8", name="Cost Savings", weight=0.50, goal_type="maximize", min_val=0, max_val=200000, description="Annual cost savings")
        g9 = Goal(id="g9", name="Implementation Risk", weight=0.30, goal_type="minimize", min_val=1, max_val=5, description="Risk rating 1-5")
        g10 = Goal(id="g10", name="Scalability", weight=0.20, goal_type="maximize", min_val=1, max_val=10, description="Future scalability score")

        d1 = DecisionAlternative(id="d1", name="AWS Migration", description="Full AWS cloud infrastructure",
                                 goal_values={"g8": 145000, "g9": 3.2, "g10": 9})
        d2 = DecisionAlternative(id="d2", name="Azure Hybrid", description="Hybrid Azure deployment",
                                 goal_values={"g8": 98000, "g9": 2.5, "g10": 8})
        d3 = DecisionAlternative(id="d3", name="On-Premise Upgrade", description="Modernize existing infrastructure",
                                 goal_values={"g8": 52000, "g9": 1.8, "g10": 5})

        s3 = PlanningScenario(id="sc003", name="IT Infrastructure Decision", description="Cloud migration vs on-premise infrastructure comparison",
                              owner="alice", created="2026-05-01 10:00", status=ScenarioStatus.DRAFT.value,
                              goals=[g8, g9, g10], alternatives=[d1, d2, d3])

        templates = [
            {"id": "t1", "name": "Cost-Efficiency Analysis", "objectives": ["Cost Reduction", "Operational Efficiency", "ROI"], "desc": "Standard cost-benefit analysis template"},
            {"id": "t2", "name": "Risk Management Framework", "objectives": ["Risk Score", "Compliance", "Business Continuity"], "desc": "Enterprise risk evaluation template"},
            {"id": "t3", "name": "Strategic Growth Planning", "objectives": ["Revenue Growth", "Market Share", "Customer Satisfaction"], "desc": "Growth and expansion planning template"},
            {"id": "t4", "name": "Resource Allocation", "objectives": ["Resource Utilization", "Cost per Unit", "Throughput"], "desc": "Operational resource optimization template"},
        ]

        activity_log = [
            {"time": "14:35", "text": "<span class='log-green'>Carol Thompson</span> approved scenario <strong>Q3 Operational Planning</strong>", "color": "#1ce783"},
            {"time": "13:22", "text": "<strong>Alice Johnson</strong> submitted <strong>Q3 Operational Planning</strong> for review", "color": "#00c2ff"},
            {"time": "11:50", "text": "<strong>Bob Martinez</strong> submitted <strong>Product Launch Strategy 2026</strong> for review", "color": "#00c2ff"},
            {"time": "10:30", "text": "<strong>Alice Johnson</strong> evaluated <strong>IT Infrastructure Decision</strong>", "color": "#1ce783"},
            {"time": "09:15", "text": "<span class='log-purple'>System Admin</span> configured evaluation parameters", "color": "#a855f7"},
        ]

        st.session_state.db = {
            "users": users,
            "scenarios": [s1, s2, s3],
            "eval_service": eval_svc,
            "templates": templates,
            "activity_log": activity_log,
            "eval_methods": {
                "Weighted Scoring": True,
                "TOPSIS": True,
                "AHP": False,
                "ELECTRE": False
            },
            "weight_limits": {"min": 0.0, "max": 1.0}
        }
    if "auth" not in st.session_state:
        st.session_state.auth = {"logged_in": False, "user": None}
    if "current_page" not in st.session_state:
        st.session_state.current_page = "dashboard"
    if "selected_scenario" not in st.session_state:
        st.session_state.selected_scenario = None
    if "auth_mode" not in st.session_state:
        st.session_state.auth_mode = "login"

def role_color(role):
    if role == UserRole.PLANNER.value:
        return "#1ce783", "#0a3d1f"
    elif role == UserRole.REVIEWER.value:
        return "#00c2ff", "#00304d"
    else:
        return "#a855f7", "#2d1057"

def avatar_initials(name):
    parts = name.strip().split()
    if len(parts) >= 2:
        return (parts[0][0] + parts[-1][0]).upper()
    return name[:2].upper()

def get_score_class(score):
    if score >= 65:
        return "score-high"
    elif score >= 40:
        return "score-med"
    return "score-low"

def status_html(status):
    cls = f"status-{status}"
    return f'<span class="status-badge {cls}">{status.upper()}</span>'

def render_nav():
    user = st.session_state.auth["user"]
    ac, wc = role_color(user.role)
    initials = avatar_initials(user.name)
    st.markdown(f"""
    <div class="main-nav">
        <div class="nav-logo">
            <span class="nav-logo-dot"></span>
            DECISIONIQ
        </div>
        <div style="display:flex;align-items:center;gap:20px;">
            <div class="nav-user-pill">
                <div class="nav-avatar" style="background:{wc};color:{ac};">{initials}</div>
                <span>{user.name}</span>
                <span class="role-badge role-{user.role}">{user.role}</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_auth():
    st.markdown('<div class="auth-bg-grid"></div>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.markdown('<div class="auth-card">', unsafe_allow_html=True)
        st.markdown('<div class="auth-logo">DECISIONIQ</div>', unsafe_allow_html=True)
        st.markdown('<div class="auth-tagline">Multi-Objective Business Planning Platform</div>', unsafe_allow_html=True)

        if st.session_state.auth_mode == "login":
            st.markdown('<div class="auth-title">Sign in</div>', unsafe_allow_html=True)
            st.markdown('<div class="auth-sub">Access your planning workspace</div>', unsafe_allow_html=True)
            username = st.text_input("Username", key="login_username", placeholder="Enter username")
            password = st.text_input("Password", type="password", key="login_password", placeholder="Enter password")
            if st.button("SIGN IN", key="btn_login"):
                if username and password:
                    db = st.session_state.db
                    if username in db["users"]:
                        u = db["users"][username]
                        if u.authenticate(password):
                            st.session_state.auth = {"logged_in": True, "user": u}
                            st.session_state.current_page = "dashboard"
                            db["activity_log"].insert(0, {
                                "time": datetime.datetime.now().strftime("%H:%M"),
                                "text": f"<strong>{u.name}</strong> signed in",
                                "color": "#1ce783"
                            })
                            st.rerun()
                        elif not u.active:
                            st.error("This account has been deactivated.")
                        else:
                            st.error("Invalid credentials. Please try again.")
                    else:
                        st.error("Account not found.")
                else:
                    st.warning("Please enter username and password.")
            st.markdown('<div class="alt-action">New to DecisionIQ? <a>Create an account</a></div>', unsafe_allow_html=True)
            if st.button("Go to Register", key="go_register"):
                st.session_state.auth_mode = "register"
                st.rerun()

        else:
            st.markdown('<div class="auth-title">Create account</div>', unsafe_allow_html=True)
            st.markdown('<div class="auth-sub">Join the planning platform</div>', unsafe_allow_html=True)
            full_name = st.text_input("Full Name", key="reg_name", placeholder="Your full name")
            email = st.text_input("Email", key="reg_email", placeholder="you@company.com")
            new_username = st.text_input("Username", key="reg_username", placeholder="Choose a username")
            new_password = st.text_input("Password", type="password", key="reg_password", placeholder="Min 8 characters")
            confirm_password = st.text_input("Confirm Password", type="password", key="reg_confirm", placeholder="Repeat password")
            role_sel = st.selectbox("Role", [UserRole.PLANNER.value, UserRole.REVIEWER.value], key="reg_role")
            if st.button("CREATE ACCOUNT", key="btn_register"):
                db = st.session_state.db
                if not all([full_name, email, new_username, new_password, confirm_password]):
                    st.error("All fields are required.")
                elif new_password != confirm_password:
                    st.error("Passwords do not match.")
                elif len(new_password) < 8:
                    st.error("Password must be at least 8 characters.")
                elif new_username in db["users"]:
                    st.error("Username already taken.")
                else:
                    uid = str(uuid.uuid4())[:10]
                    ph = hash_pw(new_password)
                    new_user = User(id=uid, username=new_username, password_hash=ph,
                                    role=role_sel, name=full_name, email=email)
                    db["users"][new_username] = new_user
                    db["activity_log"].insert(0, {
                        "time": datetime.datetime.now().strftime("%H:%M"),
                        "text": f"New account created: <strong>{full_name}</strong> ({role_sel})",
                        "color": "#a855f7"
                    })
                    st.success("Account created! You can now sign in.")
                    st.session_state.auth_mode = "login"
                    st.rerun()
            st.markdown('<div class="alt-action">Already have an account? <a>Sign in</a></div>', unsafe_allow_html=True)
            if st.button("Back to Sign In", key="go_login"):
                st.session_state.auth_mode = "login"
                st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

def render_nav_tabs():
    user = st.session_state.auth["user"]
    role = user.role

    if role == UserRole.PLANNER.value:
        pages = ["dashboard", "scenarios", "create_scenario", "evaluate", "sensitivity", "compare"]
        labels = ["Dashboard", "Scenarios", "New Scenario", "Evaluate", "Sensitivity", "Compare"]
    elif role == UserRole.REVIEWER.value:
        pages = ["dashboard", "review_queue", "approved_history", "compare"]
        labels = ["Dashboard", "Review Queue", "Approved History", "Compare"]
    else:
        pages = ["dashboard", "user_management", "system_config", "activity"]
        labels = ["Dashboard", "Users", "System Config", "Activity Log"]

    current = st.session_state.current_page
    tabs = st.tabs(labels)
    for i, (tab, page) in enumerate(zip(tabs, pages)):
        with tab:
            if current != page:
                if st.button(f"Go to {labels[i]}", key=f"nav_{page}"):
                    st.session_state.current_page = page
                    st.session_state.selected_scenario = None
                    st.rerun()

def plotly_config():
    return {
        'paper_bgcolor': 'rgba(0,0,0,0)',
        'plot_bgcolor': 'rgba(0,0,0,0)',
        'font': {'color': '#9999aa', 'family': 'DM Sans', 'size': 11},
        'margin': dict(l=10, r=10, t=30, b=10),
    }

def plotly_grid():
    return dict(color='rgba(255,255,255,0.05)', gridwidth=1)

def render_dashboard():
    user = st.session_state.auth["user"]
    db = st.session_state.db
    scenarios = db["scenarios"]
    role = user.role

    st.markdown("""
    <div class="hero-section">
        <div class="hero-breadcrumb">Overview</div>
        <div class="hero-title">Planning <span>Command Center</span></div>
        <div class="hero-subtitle">Real-time visibility into decisions, evaluations, and approval workflows across your organization.</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="page-pad">', unsafe_allow_html=True)

    if role == UserRole.PLANNER.value:
        my_s = [s for s in scenarios if s.owner == user.username]
        total = len(my_s)
        approved = sum(1 for s in my_s if s.status == ScenarioStatus.APPROVED.value)
        submitted = sum(1 for s in my_s if s.status == ScenarioStatus.SUBMITTED.value)
        drafts = sum(1 for s in my_s if s.status == ScenarioStatus.DRAFT.value)
        total_alts = sum(len(s.alternatives) for s in my_s)
        evals = sum(len(s.eval_results) for s in my_s)

        c1, c2, c3, c4, c5 = st.columns(5)
        with c1:
            st.markdown(f"""<div class="kpi-card kpi-green">
                <div class="kpi-icon">S</div>
                <div class="kpi-value">{total}</div>
                <div class="kpi-label">Total Scenarios</div>
            </div>""", unsafe_allow_html=True)
        with c2:
            st.markdown(f"""<div class="kpi-card kpi-blue">
                <div class="kpi-icon">A</div>
                <div class="kpi-value">{approved}</div>
                <div class="kpi-label">Approved</div>
            </div>""", unsafe_allow_html=True)
        with c3:
            st.markdown(f"""<div class="kpi-card kpi-orange">
                <div class="kpi-icon">P</div>
                <div class="kpi-value">{submitted}</div>
                <div class="kpi-label">In Review</div>
            </div>""", unsafe_allow_html=True)
        with c4:
            st.markdown(f"""<div class="kpi-card kpi-purple">
                <div class="kpi-icon">D</div>
                <div class="kpi-value">{drafts}</div>
                <div class="kpi-label">Drafts</div>
            </div>""", unsafe_allow_html=True)
        with c5:
            st.markdown(f"""<div class="kpi-card kpi-green">
                <div class="kpi-icon">E</div>
                <div class="kpi-value">{evals}</div>
                <div class="kpi-label">Evaluations Run</div>
            </div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        col_left, col_right = st.columns([2, 1])
        with col_left:
            st.markdown("""<div class="chart-container">
                <div class="chart-title">Scenario Pipeline</div>
                <div class="chart-subtitle">Status distribution across all scenarios</div>
            """, unsafe_allow_html=True)

            statuses = [s.status for s in my_s]
            status_counts = {}
            for s in statuses:
                status_counts[s] = status_counts.get(s, 0) + 1

            if status_counts:
                colors_map = {
                    "draft": "#555566", "active": "#1ce783", "submitted": "#00c2ff",
                    "approved": "#22ff95", "rejected": "#ff4757", "revision": "#ffa502", "archived": "#a855f7"
                }
                fig = go.Figure(data=[go.Bar(
                    x=list(status_counts.keys()),
                    y=list(status_counts.values()),
                    marker_color=[colors_map.get(k, "#555") for k in status_counts.keys()],
                    marker_line_width=0,
                    text=list(status_counts.values()),
                    textposition='outside',
                    textfont=dict(color='#9999aa', size=12)
                )])
                fig.update_layout(**plotly_config(), height=200, showlegend=False,
                                  xaxis=dict(showgrid=False, zeroline=False, tickfont=dict(size=11)),
                                  yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', zeroline=False))
                st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
            else:
                st.markdown('<div class="empty-state"><div class="empty-state-text">No scenarios yet</div></div>', unsafe_allow_html=True)

            st.markdown('</div>', unsafe_allow_html=True)

            if my_s:
                latest_approved = [s for s in my_s if s.status == ScenarioStatus.APPROVED.value and s.eval_results]
                if latest_approved:
                    best_s = latest_approved[0]
                    result = best_s.eval_results[-1]
                    st.markdown(f"""<div class="chart-container">
                        <div class="chart-title">Latest Approved Evaluation - {best_s.name}</div>
                        <div class="chart-subtitle">Alternative score comparison</div>
                    """, unsafe_allow_html=True)
                    alt_names = []
                    alt_scores = []
                    for alt_id, score in result.ranked:
                        alt = next((a for a in best_s.alternatives if a.id == alt_id), None)
                        if alt:
                            alt_names.append(alt.name)
                            alt_scores.append(score)
                    bar_colors = [("#1ce783" if i == 0 else "#2a2a38") for i in range(len(alt_names))]
                    fig2 = go.Figure(data=[go.Bar(
                        x=alt_scores, y=alt_names, orientation='h',
                        marker_color=bar_colors, marker_line_width=0,
                        text=[f"{s:.1f}" for s in alt_scores],
                        textposition='outside',
                        textfont=dict(color='#9999aa', size=11)
                    )])
                    fig2.update_layout(**plotly_config(), height=max(180, len(alt_names) * 40),
                                       showlegend=False,
                                       xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', zeroline=False, range=[0, 115]),
                                       yaxis=dict(showgrid=False, zeroline=False))
                    st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar': False})
                    st.markdown('</div>', unsafe_allow_html=True)

        with col_right:
            st.markdown('<div class="chart-container"><div class="chart-title">Recent Activity</div>', unsafe_allow_html=True)
            logs = db["activity_log"][:8]
            for log in logs:
                st.markdown(f"""<div class="activity-item">
                    <div class="activity-dot" style="background:{log['color']};box-shadow:0 0 6px {log['color']}40;"></div>
                    <div>
                        <div class="activity-text">{log['text']}</div>
                        <div class="activity-time">{log['time']}</div>
                    </div>
                </div>""", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('<br>', unsafe_allow_html=True)

            if my_s and any(s.eval_results for s in my_s):
                for s in my_s:
                    if s.eval_results:
                        res = s.eval_results[-1]
                        top_id, top_score = res.ranked[0] if res.ranked else ("", 0)
                        top_alt = next((a for a in s.alternatives if a.id == top_id), None)
                        if top_alt:
                            st.markdown(f"""<div class="highlight-box">
                                <div style="font-size:10px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;color:var(--accent);margin-bottom:6px;">Top Ranked</div>
                                <div style="font-size:16px;font-weight:800;color:var(--text-primary);margin-bottom:2px;">{top_alt.name}</div>
                                <div style="font-size:13px;color:var(--text-muted);">{s.name}</div>
                                <div style="font-family:'Bebas Neue',sans-serif;font-size:36px;color:var(--accent);margin-top:8px;">{top_score:.1f}<span style="font-family:'DM Sans';font-size:16px;color:var(--text-muted);"> pts</span></div>
                            </div>""", unsafe_allow_html=True)
                        break

    elif role == UserRole.REVIEWER.value:
        all_submitted = [s for s in scenarios if s.status == ScenarioStatus.SUBMITTED.value and s.submitted_to == user.username]
        all_approved = [s for s in scenarios if s.status == ScenarioStatus.APPROVED.value]
        all_rejected = [s for s in scenarios if s.status == ScenarioStatus.REJECTED.value]
        all_revision = [s for s in scenarios if s.status == ScenarioStatus.REVISION.value]

        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.markdown(f"""<div class="kpi-card kpi-blue">
                <div class="kpi-icon">Q</div>
                <div class="kpi-value">{len(all_submitted)}</div>
                <div class="kpi-label">Awaiting Review</div>
            </div>""", unsafe_allow_html=True)
        with c2:
            st.markdown(f"""<div class="kpi-card kpi-green">
                <div class="kpi-icon">A</div>
                <div class="kpi-value">{len(all_approved)}</div>
                <div class="kpi-label">Approved</div>
            </div>""", unsafe_allow_html=True)
        with c3:
            st.markdown(f"""<div class="kpi-card kpi-red">
                <div class="kpi-icon">R</div>
                <div class="kpi-value">{len(all_rejected)}</div>
                <div class="kpi-label">Rejected</div>
            </div>""", unsafe_allow_html=True)
        with c4:
            st.markdown(f"""<div class="kpi-card kpi-orange">
                <div class="kpi-icon">V</div>
                <div class="kpi-value">{len(all_revision)}</div>
                <div class="kpi-label">Revision Requested</div>
            </div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        col_l, col_r = st.columns([3, 2])
        with col_l:
            all_s = [s for s in scenarios if s.status in [ScenarioStatus.SUBMITTED.value, ScenarioStatus.APPROVED.value, ScenarioStatus.REJECTED.value, ScenarioStatus.REVISION.value]]
            stat_vals = {}
            for s in all_s:
                stat_vals[s.status] = stat_vals.get(s.status, 0) + 1
            if stat_vals:
                st.markdown('<div class="chart-container"><div class="chart-title">Review Status Overview</div><div class="chart-subtitle">All scenarios by current status</div>', unsafe_allow_html=True)
                colors_map = {"submitted": "#00c2ff", "approved": "#1ce783", "rejected": "#ff4757", "revision": "#ffa502"}
                fig = go.Figure(data=[go.Pie(
                    labels=list(stat_vals.keys()),
                    values=list(stat_vals.values()),
                    hole=0.62,
                    marker_colors=[colors_map.get(k, "#555") for k in stat_vals.keys()],
                    textfont=dict(size=11, color='#f5f5f7'),
                    hovertemplate='<b>%{label}</b><br>Count: %{value}<extra></extra>'
                )])
                fig.update_layout(**plotly_config(), height=260, showlegend=True,
                                  legend=dict(font=dict(color='#9999aa', size=11),
                                              bgcolor='rgba(0,0,0,0)', x=1))
                st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
                st.markdown('</div>', unsafe_allow_html=True)

        with col_r:
            st.markdown('<div class="chart-container"><div class="chart-title">Recent Activity</div>', unsafe_allow_html=True)
            for log in db["activity_log"][:7]:
                st.markdown(f"""<div class="activity-item">
                    <div class="activity-dot" style="background:{log['color']};"></div>
                    <div>
                        <div class="activity-text">{log['text']}</div>
                        <div class="activity-time">{log['time']}</div>
                    </div>
                </div>""", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

    else:
        total_users = len(db["users"])
        active_users = sum(1 for u in db["users"].values() if u.active)
        total_scenarios = len(scenarios)
        approved_count = sum(1 for s in scenarios if s.status == ScenarioStatus.APPROVED.value)
        submitted_count = sum(1 for s in scenarios if s.status == ScenarioStatus.SUBMITTED.value)

        c1, c2, c3, c4, c5 = st.columns(5)
        with c1:
            st.markdown(f"""<div class="kpi-card kpi-purple"><div class="kpi-icon">U</div>
                <div class="kpi-value">{total_users}</div><div class="kpi-label">Total Users</div></div>""", unsafe_allow_html=True)
        with c2:
            st.markdown(f"""<div class="kpi-card kpi-green"><div class="kpi-icon">A</div>
                <div class="kpi-value">{active_users}</div><div class="kpi-label">Active Users</div></div>""", unsafe_allow_html=True)
        with c3:
            st.markdown(f"""<div class="kpi-card kpi-blue"><div class="kpi-icon">S</div>
                <div class="kpi-value">{total_scenarios}</div><div class="kpi-label">Scenarios</div></div>""", unsafe_allow_html=True)
        with c4:
            st.markdown(f"""<div class="kpi-card kpi-green"><div class="kpi-icon">P</div>
                <div class="kpi-value">{approved_count}</div><div class="kpi-label">Approved</div></div>""", unsafe_allow_html=True)
        with c5:
            st.markdown(f"""<div class="kpi-card kpi-orange"><div class="kpi-icon">R</div>
                <div class="kpi-value">{submitted_count}</div><div class="kpi-label">Pending Review</div></div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        col_l, col_r = st.columns([2, 1])
        with col_l:
            st.markdown('<div class="chart-container"><div class="chart-title">System Scenario Distribution</div><div class="chart-subtitle">Scenario count by status</div>', unsafe_allow_html=True)
            all_statuses = {}
            for s in scenarios:
                all_statuses[s.status] = all_statuses.get(s.status, 0) + 1
            colors_map = {"draft": "#555566", "active": "#1ce783", "submitted": "#00c2ff",
                          "approved": "#22ff95", "rejected": "#ff4757", "revision": "#ffa502", "archived": "#a855f7"}
            if all_statuses:
                fig = go.Figure(data=[go.Bar(
                    x=list(all_statuses.keys()),
                    y=list(all_statuses.values()),
                    marker_color=[colors_map.get(k, "#555") for k in all_statuses.keys()],
                    marker_line_width=0,
                )])
                fig.update_layout(**plotly_config(), height=200, showlegend=False,
                                  xaxis=dict(showgrid=False, zeroline=False),
                                  yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', zeroline=False))
                st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
            st.markdown('</div>', unsafe_allow_html=True)

            role_counts = {}
            for u in db["users"].values():
                role_counts[u.role] = role_counts.get(u.role, 0) + 1
            st.markdown('<div class="chart-container"><div class="chart-title">User Role Distribution</div><div class="chart-subtitle">Active users by role</div>', unsafe_allow_html=True)
            fig2 = go.Figure(data=[go.Pie(
                labels=list(role_counts.keys()),
                values=list(role_counts.values()),
                hole=0.6,
                marker_colors=["#1ce783", "#00c2ff", "#a855f7"],
                textfont=dict(size=11, color='#f5f5f7')
            )])
            fig2.update_layout(**plotly_config(), height=230, showlegend=True,
                               legend=dict(font=dict(color='#9999aa', size=11), bgcolor='rgba(0,0,0,0)'))
            st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar': False})
            st.markdown('</div>', unsafe_allow_html=True)

        with col_r:
            st.markdown('<div class="chart-container"><div class="chart-title">System Activity Log</div>', unsafe_allow_html=True)
            for log in db["activity_log"][:10]:
                st.markdown(f"""<div class="activity-item">
                    <div class="activity-dot" style="background:{log['color']};"></div>
                    <div>
                        <div class="activity-text">{log['text']}</div>
                        <div class="activity-time">{log['time']}</div>
                    </div>
                </div>""", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

    col_lo1, col_lo2, col_lo3 = st.columns([4, 1, 1])
    with col_lo3:
        if st.button("SIGN OUT", key="signout_btn"):
            st.session_state.auth = {"logged_in": False, "user": None}
            st.session_state.current_page = "dashboard"
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

def render_scenarios_list():
    user = st.session_state.auth["user"]
    db = st.session_state.db
    scenarios = [s for s in db["scenarios"] if s.owner == user.username]

    st.markdown("""
    <div class="hero-section">
        <div class="hero-breadcrumb">Planner</div>
        <div class="hero-title">My <span>Scenarios</span></div>
        <div class="hero-subtitle">Manage and track all your planning scenarios in one place.</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="page-pad">', unsafe_allow_html=True)

    if not scenarios:
        st.markdown("""<div class="empty-state">
            <div class="empty-state-icon">S</div>
            <div class="empty-state-text">No scenarios yet</div>
            <div class="empty-state-sub">Create your first planning scenario to start evaluating business decisions.</div>
        </div>""", unsafe_allow_html=True)
        if st.button("CREATE FIRST SCENARIO", key="create_first"):
            st.session_state.current_page = "create_scenario"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        return

    filter_col, sort_col = st.columns([3, 1])
    with filter_col:
        filter_status = st.selectbox("Filter by Status", ["All", "draft", "active", "submitted", "approved", "rejected", "revision", "archived"], key="filter_status")
    with sort_col:
        sort_by = st.selectbox("Sort by", ["Created (Newest)", "Name (A-Z)", "Status"], key="sort_by")

    filtered = scenarios
    if filter_status != "All":
        filtered = [s for s in scenarios if s.status == filter_status]
    if sort_by == "Name (A-Z)":
        filtered = sorted(filtered, key=lambda x: x.name)
    elif sort_by == "Status":
        filtered = sorted(filtered, key=lambda x: x.status)
    else:
        filtered = sorted(filtered, key=lambda x: x.created, reverse=True)

    st.markdown(f"<br><div style='font-size:12px;color:var(--text-muted);font-weight:700;letter-spacing:1px;text-transform:uppercase;margin-bottom:16px;'>SHOWING {len(filtered)} SCENARIOS</div>", unsafe_allow_html=True)

    for s in filtered:
        ac = {"draft": "#555566", "active": "#1ce783", "submitted": "#00c2ff",
              "approved": "#22ff95", "rejected": "#ff4757", "revision": "#ffa502", "archived": "#a855f7"}.get(s.status, "#555")
        evals_count = len(s.eval_results)
        top_score = ""
        if s.eval_results:
            ranked = s.eval_results[-1].ranked
            if ranked:
                top_score = f"{ranked[0][1]:.1f} pts"
        st.markdown(f"""<div class="scenario-list-item">
            <div style="display:flex;align-items:flex-start;justify-content:space-between;margin-bottom:10px;">
                <div>
                    <div class="scenario-name">{s.name}</div>
                    <div class="scenario-desc">{s.description}</div>
                </div>
                {status_html(s.status)}
            </div>
            <div class="scenario-meta">
                <div class="scenario-meta-item">Goals: <strong>{len(s.goals)}</strong></div>
                <div class="scenario-meta-item">Alternatives: <strong>{len(s.alternatives)}</strong></div>
                <div class="scenario-meta-item">Evaluations: <strong>{evals_count}</strong></div>
                <div class="scenario-meta-item">Constraints: <strong>{len(s.constraints)}</strong></div>
                <div class="scenario-meta-item">Created: <strong>{s.created[:10]}</strong></div>
                {f'<div class="scenario-meta-item">Top Score: <strong style="color:var(--accent)">{top_score}</strong></div>' if top_score else ""}
            </div>
        </div>""", unsafe_allow_html=True)

        bcols = st.columns([1, 1, 1, 1, 3])
        with bcols[0]:
            if st.button("Open", key=f"open_{s.id}"):
                st.session_state.selected_scenario = s.id
                st.session_state.current_page = "evaluate"
                st.rerun()
        with bcols[1]:
            if st.button("Duplicate", key=f"dup_{s.id}"):
                planner = Planner(user, db)
                planner.duplicate_scenario(s)
                st.success(f"Duplicated: {s.name}")
                st.rerun()
        with bcols[2]:
            reviewers = [u for u in db["users"].values() if u.role == UserRole.REVIEWER.value and u.active]
            if reviewers and s.status not in [ScenarioStatus.SUBMITTED.value, ScenarioStatus.APPROVED.value, ScenarioStatus.ARCHIVED.value]:
                rev_names = [f"{r.name} ({r.username})" for r in reviewers]
                if st.button("Submit", key=f"submit_quick_{s.id}"):
                    planner = Planner(user, db)
                    ok, msg = planner.submit_scenario(s, reviewers[0].username)
                    if ok:
                        st.success("Submitted for review")
                    else:
                        st.error(msg)
                    st.rerun()
        with bcols[3]:
            if s.status not in [ScenarioStatus.ARCHIVED.value]:
                if st.button("Archive", key=f"arch_{s.id}"):
                    s.change_status(ScenarioStatus.ARCHIVED.value)
                    s.log_revision(user.name, "Archived")
                    st.success("Archived")
                    st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

def render_create_scenario():
    user = st.session_state.auth["user"]
    db = st.session_state.db

    st.markdown("""
    <div class="hero-section">
        <div class="hero-breadcrumb">Planner / New Scenario</div>
        <div class="hero-title">Create <span>Planning Scenario</span></div>
        <div class="hero-subtitle">Define objectives, constraints, and alternatives for a structured multi-objective analysis.</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="page-pad">', unsafe_allow_html=True)

    tab1, tab2, tab3, tab4, tab5 = st.tabs(["SCENARIO INFO", "OBJECTIVES", "CONSTRAINTS", "ALTERNATIVES", "ASSUMPTIONS"])

    with tab1:
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown('<div class="form-section-title">Basic Information</div>', unsafe_allow_html=True)
        sc_name = st.text_input("Scenario Name", key="new_sc_name", placeholder="e.g., Q4 Resource Allocation Plan")
        sc_desc = st.text_area("Description", key="new_sc_desc", placeholder="Describe the business problem and planning context...", height=100)

        st.markdown('<div class="form-section-title" style="margin-top:24px;">Quick Start from Template</div>', unsafe_allow_html=True)
        templates = db["templates"]
        for t in templates:
            st.markdown(f"""<div class="template-card">
                <div class="template-name">{t['name']}</div>
                <div class="template-desc">{t['desc']}</div>
                <div class="tag-row">{''.join(f'<span class="tag">{o}</span>' for o in t['objectives'])}</div>
            </div>""", unsafe_allow_html=True)
            if st.button(f"Use template: {t['name']}", key=f"use_template_{t['id']}"):
                if not sc_name:
                    st.session_state["new_sc_name"] = t['name']
                st.info(f"Template '{t['name']}' selected. Fill in scenario name and proceed to Objectives tab.")

        st.markdown('</div>', unsafe_allow_html=True)

        if sc_name:
            if st.button("SAVE SCENARIO INFO", key="save_sc_info"):
                planner = Planner(user, db)
                new_s = planner.create_scenario(sc_name, sc_desc)
                st.session_state.selected_scenario = new_s.id
                st.success(f"Scenario '{sc_name}' created. Now define objectives.")
                st.rerun()

    with tab2:
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown('<div class="form-section-title">Define Objectives</div>', unsafe_allow_html=True)

        my_scenarios = [s for s in db["scenarios"] if s.owner == user.username and s.status == ScenarioStatus.DRAFT.value]
        if not my_scenarios:
            st.info("Create a scenario first (Scenario Info tab).")
        else:
            sc_opts = {s.name: s for s in my_scenarios}
            sel_sc_name = st.selectbox("Select Scenario", list(sc_opts.keys()), key="sel_sc_goals")
            sel_sc = sc_opts[sel_sc_name]

            if sel_sc.goals:
                st.markdown("<br>", unsafe_allow_html=True)
                for g in sel_sc.goals:
                    ww = (g.weight / max(g.weight for g2 in sel_sc.goals)) * 100 if sel_sc.goals else 0
                    color = "#1ce783" if g.goal_type == "maximize" else "#ff4757"
                    st.markdown(f"""<div class="obj-row">
                        <div class="obj-header">
                            <div class="obj-name">{g.name}</div>
                            <div class="obj-type obj-type-{'max' if g.goal_type=='maximize' else 'min'}">{g.goal_type.upper()}</div>
                        </div>
                        <div class="weight-display">
                            <div class="weight-val">{g.weight:.2f}</div>
                            <div class="weight-label">Weight</div>
                        </div>
                        <div class="progress-bar-wrap">
                            <div class="progress-bar-fill" style="width:{ww:.0f}%;background:{color};"></div>
                        </div>
                        <div style="font-size:11px;color:var(--text-muted);margin-top:6px;">Range: {g.min_val} - {g.max_val} &nbsp;|&nbsp; {g.description}</div>
                    </div>""", unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown('<div class="form-section-title">Add New Objective</div>', unsafe_allow_html=True)
            g_col1, g_col2 = st.columns(2)
            with g_col1:
                g_name = st.text_input("Objective Name", key="g_name", placeholder="e.g., Cost Reduction")
                g_type = st.selectbox("Type", ["minimize", "maximize"], key="g_type")
                g_desc = st.text_input("Description (optional)", key="g_desc", placeholder="Brief description")
            with g_col2:
                g_weight = st.slider("Priority Weight", 0.0, 1.0, 0.25, 0.05, key="g_weight")
                g_min = st.number_input("Min Value", value=0.0, key="g_min")
                g_max = st.number_input("Max Value", value=100.0, key="g_max")

            if g_name:
                eval_svc = db["eval_service"]
                if not (eval_svc.weight_min <= g_weight <= eval_svc.weight_max):
                    st.warning(f"Weight must be between {eval_svc.weight_min} and {eval_svc.weight_max}")
                elif st.button("ADD OBJECTIVE", key="add_goal"):
                    gid = str(uuid.uuid4())[:8]
                    new_g = Goal(id=gid, name=g_name, weight=g_weight, goal_type=g_type,
                                 min_val=g_min, max_val=g_max, description=g_desc)
                    sel_sc.add_goal(new_g)
                    sel_sc.log_revision(user.name, f"Added goal: {g_name}")
                    st.success(f"Objective '{g_name}' added.")
                    st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

    with tab3:
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown('<div class="form-section-title">Define Constraints</div>', unsafe_allow_html=True)

        my_scenarios = [s for s in db["scenarios"] if s.owner == user.username and s.status == ScenarioStatus.DRAFT.value]
        if not my_scenarios:
            st.info("Create a scenario first.")
        else:
            sc_opts = {s.name: s for s in my_scenarios}
            sel_sc_name = st.selectbox("Select Scenario", list(sc_opts.keys()), key="sel_sc_constraints")
            sel_sc = sc_opts[sel_sc_name]

            if sel_sc.constraints:
                for c in sel_sc.constraints:
                    st.markdown(f"""<div class="constraint-row">
                        <div>
                            <div class="constraint-name">{c.name}</div>
                            <div class="constraint-range">Range: {c.min_val} - {c.max_val} {c.unit}</div>
                        </div>
                        <span class="status-badge status-active">ACTIVE</span>
                    </div>""", unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown('<div class="form-section-title">Add New Constraint</div>', unsafe_allow_html=True)
            c_col1, c_col2 = st.columns(2)
            with c_col1:
                c_name = st.text_input("Constraint Name", key="c_name", placeholder="e.g., Budget Limit")
                c_unit = st.text_input("Unit", key="c_unit", placeholder="e.g., USD, %, hours")
                c_desc = st.text_input("Description (optional)", key="c_desc")
            with c_col2:
                c_min = st.number_input("Min Value", value=0.0, key="c_min")
                c_max = st.number_input("Max Value", value=100.0, key="c_max")

            if c_name:
                if c_min >= c_max:
                    st.warning("Min value must be less than max value.")
                elif st.button("ADD CONSTRAINT", key="add_constraint"):
                    cid = str(uuid.uuid4())[:8]
                    new_c = Constraint(id=cid, name=c_name, min_val=c_min, max_val=c_max, unit=c_unit, description=c_desc)
                    sel_sc.constraints.append(new_c)
                    sel_sc.log_revision(user.name, f"Added constraint: {c_name}")
                    st.success(f"Constraint '{c_name}' added.")
                    st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

    with tab4:
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown('<div class="form-section-title">Define Decision Alternatives</div>', unsafe_allow_html=True)

        my_scenarios = [s for s in db["scenarios"] if s.owner == user.username and s.status == ScenarioStatus.DRAFT.value]
        if not my_scenarios:
            st.info("Create a scenario first.")
        else:
            sc_opts = {s.name: s for s in my_scenarios}
            sel_sc_name = st.selectbox("Select Scenario", list(sc_opts.keys()), key="sel_sc_alts")
            sel_sc = sc_opts[sel_sc_name]

            if not sel_sc.goals:
                st.warning("Define objectives first before adding alternatives.")
            else:
                if sel_sc.alternatives:
                    st.markdown(f"<div style='font-size:12px;color:var(--text-muted);font-weight:700;letter-spacing:1px;text-transform:uppercase;margin-bottom:12px;'>{len(sel_sc.alternatives)} ALTERNATIVES DEFINED</div>", unsafe_allow_html=True)
                    for a in sel_sc.alternatives:
                        excl_txt = '<span style="color:var(--warning);font-size:11px;font-weight:700;margin-left:8px;">EXCLUDED</span>' if a.excluded else ''
                        vals_txt = " &nbsp;|&nbsp; ".join([f"{sel_sc.goals[i].name}: <strong>{v}</strong>" for i, (gid, v) in enumerate(a.goal_values.items()) if i < len(sel_sc.goals)])
                        st.markdown(f"""<div class="scenario-list-item" style="padding:14px 18px;margin-bottom:8px;">
                            <div style="font-weight:800;font-size:14px;color:var(--text-primary);">{a.name}{excl_txt}</div>
                            <div style="font-size:12px;color:var(--text-muted);margin-top:3px;">{a.description}</div>
                            <div style="font-size:12px;color:var(--text-secondary);margin-top:8px;">{vals_txt}</div>
                        </div>""", unsafe_allow_html=True)
                        ecols = st.columns([1, 4])
                        with ecols[0]:
                            excl_label = "Re-include" if a.excluded else "Exclude"
                            if st.button(excl_label, key=f"excl_{a.id}"):
                                a.excluded = not a.excluded
                                sel_sc.log_revision(user.name, f"{'Excluded' if a.excluded else 'Re-included'} alternative: {a.name}")
                                st.rerun()

                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown('<div class="form-section-title">Add New Alternative</div>', unsafe_allow_html=True)
                a_name = st.text_input("Alternative Name", key="a_name", placeholder="e.g., Option A - Digital Strategy")
                a_desc = st.text_input("Description", key="a_desc", placeholder="Brief description of this alternative")

                if a_name:
                    st.markdown("<div style='margin-top:12px;'></div>", unsafe_allow_html=True)
                    goal_values = {}
                    gcols = st.columns(min(len(sel_sc.goals), 3))
                    for idx, g in enumerate(sel_sc.goals):
                        with gcols[idx % min(len(sel_sc.goals), 3)]:
                            val = st.number_input(f"{g.name} ({g.goal_type})", min_value=float(g.min_val), max_value=float(g.max_val),
                                                   value=float((g.min_val + g.max_val) / 2), key=f"alt_val_{g.id}")
                            goal_values[g.id] = val

                    if st.button("ADD ALTERNATIVE", key="add_alt"):
                        aid = str(uuid.uuid4())[:8]
                        new_a = DecisionAlternative(id=aid, name=a_name, description=a_desc, goal_values=goal_values)
                        sel_sc.add_alternative(new_a)
                        sel_sc.log_revision(user.name, f"Added alternative: {a_name}")
                        st.success(f"Alternative '{a_name}' added.")
                        st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

    with tab5:
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown('<div class="form-section-title">Document Assumptions</div>', unsafe_allow_html=True)

        my_scenarios = [s for s in db["scenarios"] if s.owner == user.username and s.status == ScenarioStatus.DRAFT.value]
        if not my_scenarios:
            st.info("Create a scenario first.")
        else:
            sc_opts = {s.name: s for s in my_scenarios}
            sel_sc_name = st.selectbox("Select Scenario", list(sc_opts.keys()), key="sel_sc_assum")
            sel_sc = sc_opts[sel_sc_name]

            if sel_sc.assumptions:
                st.markdown(f"<div style='font-size:12px;color:var(--text-muted);font-weight:700;letter-spacing:1px;text-transform:uppercase;margin-bottom:12px;'>{len(sel_sc.assumptions)} ASSUMPTIONS DOCUMENTED</div>", unsafe_allow_html=True)
                for i, assump in enumerate(sel_sc.assumptions):
                    st.markdown(f"""<div class="assumption-row">
                        <div style="font-size:11px;font-weight:700;letter-spacing:1px;color:var(--purple);text-transform:uppercase;margin-bottom:4px;">Assumption {i+1}</div>
                        <div class="assumption-text">{assump}</div>
                    </div>""", unsafe_allow_html=True)
            else:
                st.markdown('<div class="empty-state" style="padding:30px;"><div class="empty-state-text">No assumptions yet</div></div>', unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown('<div class="form-section-title">Add Assumption</div>', unsafe_allow_html=True)
            new_assump = st.text_area("Assumption Text", key="new_assump", placeholder="Describe an assumption made when defining this scenario...", height=80)
            if new_assump:
                if st.button("ADD ASSUMPTION", key="add_assump"):
                    sel_sc.add_assumption(new_assump)
                    sel_sc.log_revision(user.name, "Added assumption")
                    st.success("Assumption added.")
                    st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

def render_evaluate():
    user = st.session_state.auth["user"]
    db = st.session_state.db

    my_scenarios = [s for s in db["scenarios"] if s.owner == user.username]

    st.markdown("""
    <div class="hero-section">
        <div class="hero-breadcrumb">Planner / Evaluate</div>
        <div class="hero-title">Scenario <span>Evaluation</span></div>
        <div class="hero-subtitle">Run multi-objective evaluations and rank decision alternatives by weighted scores.</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="page-pad">', unsafe_allow_html=True)

    if not my_scenarios:
        st.markdown('<div class="empty-state"><div class="empty-state-text">No scenarios available</div></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        return

    sc_opts = {s.name: s for s in my_scenarios}
    sel_name = list(sc_opts.keys())[0]
    if st.session_state.selected_scenario:
        for s in my_scenarios:
            if s.id == st.session_state.selected_scenario:
                sel_name = s.name
                break

    sel_sc_name = st.selectbox("Select Scenario to Evaluate", list(sc_opts.keys()),
                                index=list(sc_opts.keys()).index(sel_name), key="eval_sc_sel")
    sel_sc = sc_opts[sel_sc_name]

    st.markdown(f"""<div class="content-card">
        <div class="content-card-header">
            <div>
                <div class="content-card-title">{sel_sc.name}</div>
                <div class="content-card-meta">{sel_sc.description} &nbsp;|&nbsp; Created: {sel_sc.created}</div>
            </div>
            {status_html(sel_sc.status)}
        </div>
        <div style="display:flex;gap:24px;flex-wrap:wrap;margin-top:4px;">
            <div style="font-size:13px;color:var(--text-muted);">Goals: <strong style="color:var(--text-primary)">{len(sel_sc.goals)}</strong></div>
            <div style="font-size:13px;color:var(--text-muted);">Alternatives: <strong style="color:var(--text-primary)">{len(sel_sc.alternatives)}</strong></div>
            <div style="font-size:13px;color:var(--text-muted);">Constraints: <strong style="color:var(--text-primary)">{len(sel_sc.constraints)}</strong></div>
            <div style="font-size:13px;color:var(--text-muted);">Evaluations Run: <strong style="color:var(--accent)">{len(sel_sc.eval_results)}</strong></div>
        </div>
    </div>""", unsafe_allow_html=True)

    if not sel_sc.goals or not sel_sc.alternatives:
        st.warning("This scenario needs objectives and alternatives defined before evaluation.")
        st.markdown('</div>', unsafe_allow_html=True)
        return

    col_eval, col_info = st.columns([2, 1])

    with col_eval:
        st.markdown('<div class="chart-container"><div class="chart-title">Objective Weights</div><div class="chart-subtitle">Adjust weights before running evaluation</div>', unsafe_allow_html=True)

        new_weights = {}
        for g in sel_sc.goals:
            new_weights[g.id] = st.slider(
                f"{g.name} ({g.goal_type})",
                0.0, 1.0, g.weight, 0.05,
                key=f"w_{sel_sc.id}_{g.id}"
            )

        total_w = sum(new_weights.values())
        wc = "#1ce783" if abs(total_w - 1.0) < 0.01 else "#ffa502"
        st.markdown(f"<div style='margin-top:12px;font-size:13px;font-weight:700;color:{wc};'>Total weight: {total_w:.2f} {'(normalized)' if abs(total_w - 1.0) < 0.01 else '(will be auto-normalized)'}</div>", unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

        if st.button("RUN EVALUATION", key="run_eval"):
            for g in sel_sc.goals:
                g.set_weight(new_weights[g.id])
            eval_svc = db["eval_service"]
            if not eval_svc.enabled:
                st.error("Evaluation service is currently disabled.")
            else:
                ok, msg = eval_svc.validate_scenario(sel_sc)
                if not ok:
                    st.error(f"Validation failed: {msg}")
                else:
                    result = eval_svc.calc_scores(sel_sc)
                    sel_sc.log_revision(user.name, "Evaluation run")
                    db["activity_log"].insert(0, {
                        "time": datetime.datetime.now().strftime("%H:%M"),
                        "text": f"<strong>{user.name}</strong> evaluated scenario <span class='log-green'>{sel_sc.name}</span>",
                        "color": "#1ce783"
                    })
                    if result:
                        st.success(f"Evaluation complete at {result.timestamp}")
                        st.session_state.selected_scenario = sel_sc.id
                        st.rerun()

    with col_info:
        if sel_sc.constraints:
            st.markdown('<div class="content-card"><div style="font-size:11px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;color:var(--text-muted);margin-bottom:12px;">CONSTRAINTS</div>', unsafe_allow_html=True)
            for c in sel_sc.constraints:
                st.markdown(f"""<div class="constraint-row">
                    <div>
                        <div class="constraint-name">{c.name}</div>
                        <div class="constraint-range">{c.min_val} - {c.max_val} {c.unit}</div>
                    </div>
                </div>""", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        if sel_sc.assumptions:
            st.markdown('<div class="content-card"><div style="font-size:11px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;color:var(--text-muted);margin-bottom:12px;">ASSUMPTIONS</div>', unsafe_allow_html=True)
            for a in sel_sc.assumptions[:3]:
                st.markdown(f'<div style="font-size:12px;color:var(--text-secondary);padding:6px 0;border-bottom:1px solid var(--border);">{a}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

    if sel_sc.eval_results:
        result = sel_sc.eval_results[-1]

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f"""<div style="font-size:11px;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:var(--text-muted);margin-bottom:16px;">EVALUATION RESULTS &nbsp;|&nbsp; <span style="color:var(--accent)">{result.timestamp}</span></div>""", unsafe_allow_html=True)

        chart_col, table_col = st.columns([3, 2])

        with chart_col:
            st.markdown('<div class="chart-container"><div class="chart-title">Alternative Rankings</div><div class="chart-subtitle">Weighted composite score (0-100)</div>', unsafe_allow_html=True)
            alt_names = []
            alt_scores = []
            alt_colors = []
            feasibility = []

            COLORS_RANKED = ["#1ce783", "#22d97a", "#28c46e", "#2eaf63", "#349a58"]
            for idx, (alt_id, score) in enumerate(result.ranked):
                alt = next((a for a in sel_sc.alternatives if a.id == alt_id), None)
                if alt:
                    alt_names.append(alt.name)
                    alt_scores.append(score)
                    is_feasible = result.feasible.get(alt_id, True)
                    feasibility.append(is_feasible)
                    if not is_feasible:
                        alt_colors.append("#ff4757")
                    elif idx == 0:
                        alt_colors.append("#1ce783")
                    elif idx == 1:
                        alt_colors.append("#00c2ff")
                    else:
                        alt_colors.append("#2a2a38")

            fig = go.Figure(data=[go.Bar(
                y=alt_names[::-1], x=alt_scores[::-1], orientation='h',
                marker_color=alt_colors[::-1], marker_line_width=0,
                text=[f"{s:.1f}" for s in alt_scores[::-1]],
                textposition='outside',
                textfont=dict(color='#9999aa', size=12),
                hovertemplate='<b>%{y}</b><br>Score: %{x:.2f}<extra></extra>'
            )])
            fig.update_layout(**plotly_config(), height=max(200, len(alt_names) * 50),
                              showlegend=False,
                              xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', zeroline=False, range=[0, 115]),
                              yaxis=dict(showgrid=False, zeroline=False))
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
            st.markdown('</div>', unsafe_allow_html=True)

            if len(sel_sc.goals) >= 3:
                st.markdown('<div class="chart-container"><div class="chart-title">Radar Analysis</div><div class="chart-subtitle">Alternative performance across all objectives</div>', unsafe_allow_html=True)
                categories = [g.name for g in sel_sc.goals]
                fig_radar = go.Figure()
                radar_colors = ["#1ce783", "#00c2ff", "#a855f7", "#ffa502", "#ff4757"]

                top_alts = result.ranked[:min(3, len(result.ranked))]
                for idx, (alt_id, score) in enumerate(top_alts):
                    alt = next((a for a in sel_sc.alternatives if a.id == alt_id), None)
                    if alt:
                        all_vals_radar = []
                        for g in sel_sc.goals:
                            raw = alt.goal_values.get(g.id, 0)
                            mn, mx = g.min_val, g.max_val
                            norm = ((raw - mn) / (mx - mn) * 100) if mx != mn else 50
                            if g.goal_type == "minimize":
                                norm = 100 - norm
                            all_vals_radar.append(round(norm, 1))
                        all_vals_radar.append(all_vals_radar[0])
                        cats = categories + [categories[0]]
                        fig_radar.add_trace(go.Scatterpolar(
                            r=all_vals_radar, theta=cats,
                            fill='toself',
                            name=alt.name,
                            line=dict(color=radar_colors[idx % len(radar_colors)], width=2),
                            fillcolor=radar_colors[idx % len(radar_colors)].replace('#', 'rgba(').replace('1ce783', '28, 231, 131, 0.1)').replace('00c2ff', '0, 194, 255, 0.1)').replace('a855f7', '168, 85, 247, 0.1)'),
                            hovertemplate='<b>%{theta}</b>: %{r:.1f}<extra></extra>'
                        ))

                fig_radar.update_layout(
                    polar=dict(
                        bgcolor='rgba(0,0,0,0)',
                        radialaxis=dict(visible=True, range=[0, 100], color='#555566',
                                        gridcolor='rgba(255,255,255,0.07)', tickfont=dict(size=9)),
                        angularaxis=dict(color='#9999aa', gridcolor='rgba(255,255,255,0.07)',
                                         tickfont=dict(size=10))
                    ),
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='#9999aa', family='DM Sans'),
                    height=320,
                    showlegend=True,
                    legend=dict(font=dict(color='#9999aa', size=11), bgcolor='rgba(0,0,0,0)'),
                    margin=dict(l=30, r=30, t=30, b=10)
                )
                st.plotly_chart(fig_radar, use_container_width=True, config={'displayModeBar': False})
                st.markdown('</div>', unsafe_allow_html=True)

        with table_col:
            st.markdown('<div class="chart-container"><div class="chart-title">Detailed Scores</div><div class="chart-subtitle">Score breakdown per alternative</div>', unsafe_allow_html=True)
            rows_html = ""
            for rank_idx, (alt_id, score) in enumerate(result.ranked):
                alt = next((a for a in sel_sc.alternatives if a.id == alt_id), None)
                if alt:
                    is_feasible = result.feasible.get(alt_id, True)
                    feasible_badge = '<span class="status-badge status-active" style="font-size:9px;">FEASIBLE</span>' if is_feasible else '<span class="status-badge status-rejected" style="font-size:9px;">INFEASIBLE</span>'
                    sc_cls = get_score_class(score)
                    rank_cls = "top" if rank_idx == 0 else ""
                    rows_html += f"""<tr>
                        <td><span class="rank-num {rank_cls}">#{rank_idx+1}</span></td>
                        <td><div style="font-weight:700;font-size:13px;">{alt.name}</div><div style="margin-top:3px;">{feasible_badge}</div></td>
                        <td><span class="score-pill {sc_cls}">{score:.1f}</span></td>
                    </tr>"""
            st.markdown(f"""<table class="rank-table">
                <thead><tr><th>Rank</th><th>Alternative</th><th>Score</th></tr></thead>
                <tbody>{rows_html}</tbody>
            </table>""", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('<div class="chart-container"><div class="chart-title">Objective Values by Alternative</div>', unsafe_allow_html=True)
            if sel_sc.goals and sel_sc.alternatives:
                alt_names_tbl = [a.name for a in sel_sc.alternatives if not a.excluded]
                goal_names_tbl = [g.name for g in sel_sc.goals]
                z_data = []
                for g in sel_sc.goals:
                    row = []
                    for a in sel_sc.alternatives:
                        if not a.excluded:
                            row.append(a.goal_values.get(g.id, 0))
                    z_data.append(row)
                if alt_names_tbl and z_data:
                    fig_heat = go.Figure(data=go.Heatmap(
                        z=z_data,
                        x=alt_names_tbl,
                        y=goal_names_tbl,
                        colorscale=[[0, '#1a1a24'], [0.5, '#1b4d3e'], [1, '#1ce783']],
                        hovertemplate='<b>%{y}</b><br>%{x}: %{z}<extra></extra>',
                        showscale=False
                    ))
                    fig_heat.update_layout(**plotly_config(), height=max(150, len(goal_names_tbl) * 50),
                                           xaxis=dict(tickfont=dict(size=9), tickangle=-30),
                                           yaxis=dict(tickfont=dict(size=10)))
                    st.plotly_chart(fig_heat, use_container_width=True, config={'displayModeBar': False})
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div style="display:flex;gap:16px;flex-wrap:wrap;">', unsafe_allow_html=True)

        sel_preferred = st.selectbox("Select Preferred Alternative",
                                      [a.name for a in sel_sc.alternatives if not a.excluded],
                                      key="sel_preferred")
        pref_alt = next((a for a in sel_sc.alternatives if a.name == sel_preferred), None)

        col_b1, col_b2, col_b3 = st.columns(3)
        with col_b1:
            if pref_alt and st.button("MARK AS PREFERRED", key="mark_preferred"):
                planner = Planner(user, db)
                planner.select_alternative(sel_sc, pref_alt.id)
                sel_sc.log_revision(user.name, f"Marked preferred: {pref_alt.name}")
                st.success(f"'{pref_alt.name}' marked as preferred.")
                st.rerun()
        with col_b2:
            reviewers = [u for u in db["users"].values() if u.role == UserRole.REVIEWER.value and u.active]
            if reviewers:
                rev_opts = {f"{r.name} ({r.username})": r.username for r in reviewers}
                sel_rev = st.selectbox("Submit to Reviewer", list(rev_opts.keys()), key="sel_reviewer")
                if st.button("SUBMIT FOR REVIEW", key="submit_for_review"):
                    planner = Planner(user, db)
                    ok, msg = planner.submit_scenario(sel_sc, rev_opts[sel_rev])
                    if ok:
                        st.success("Scenario submitted for review.")
                        st.rerun()
                    else:
                        st.error(msg)
        with col_b3:
            if len(sel_sc.eval_results) > 1:
                st.info(f"{len(sel_sc.eval_results)} evaluations stored for comparison.")

    st.markdown('</div>', unsafe_allow_html=True)

def render_sensitivity():
    user = st.session_state.auth["user"]
    db = st.session_state.db

    my_scenarios = [s for s in db["scenarios"] if s.owner == user.username and s.eval_results]

    st.markdown("""
    <div class="hero-section">
        <div class="hero-breadcrumb">Planner / Analysis</div>
        <div class="hero-title">Sensitivity <span>Analysis</span></div>
        <div class="hero-subtitle">Understand how changes in objective priorities affect alternative rankings.</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="page-pad">', unsafe_allow_html=True)

    if not my_scenarios:
        st.markdown('<div class="empty-state"><div class="empty-state-text">No evaluated scenarios</div><div class="empty-state-sub">Evaluate a scenario first to run sensitivity analysis.</div></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        return

    sc_opts = {s.name: s for s in my_scenarios}
    sel_sc_name = st.selectbox("Select Scenario", list(sc_opts.keys()), key="sens_sc_sel")
    sel_sc = sc_opts[sel_sc_name]

    baseline_result = sel_sc.eval_results[-1]

    col_l, col_r = st.columns([1, 2])

    with col_l:
        st.markdown('<div class="chart-container"><div class="chart-title">Baseline Weights</div><div class="chart-subtitle">Current objective weights snapshot</div>', unsafe_allow_html=True)
        for g in sel_sc.goals:
            ww = (g.weight / max(gg.weight for gg in sel_sc.goals)) * 100 if sel_sc.goals else 0
            st.markdown(f"""<div class="sensitivity-bar">
                <div class="sensitivity-label">{g.name}</div>
                <div class="sensitivity-track"><div class="sensitivity-fill" style="width:{ww:.0f}%;background:{'#1ce783' if g.goal_type=='maximize' else '#ff4757'};"></div></div>
                <div class="sensitivity-val">{g.weight:.2f}</div>
            </div>""", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="chart-container"><div class="chart-title">Adjust Weights for Analysis</div>', unsafe_allow_html=True)
        test_weights = {}
        for g in sel_sc.goals:
            test_weights[g.id] = st.slider(f"{g.name}", 0.0, 1.0, g.weight, 0.05, key=f"sens_{g.id}")

        if st.button("ANALYZE SENSITIVITY", key="run_sens"):
            orig_weights = {g.id: g.weight for g in sel_sc.goals}
            for g in sel_sc.goals:
                g.set_weight(test_weights[g.id])
            test_result = sel_sc.evaluate()
            for g in sel_sc.goals:
                g.set_weight(orig_weights[g.id])
            if test_result:
                st.session_state["sens_result"] = test_result
                st.success("Sensitivity analysis complete.")
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with col_r:
        if "sens_result" in st.session_state:
            test_result = st.session_state["sens_result"]
            st.markdown('<div class="chart-container"><div class="chart-title">Ranking Shift Analysis</div><div class="chart-subtitle">Position changes between baseline and modified weights</div>', unsafe_allow_html=True)

            baseline_rank = {alt_id: idx for idx, (alt_id, _) in enumerate(baseline_result.ranked)}
            test_rank = {alt_id: idx for idx, (alt_id, _) in enumerate(test_result.ranked)}

            alt_ids = [alt_id for alt_id, _ in baseline_result.ranked]
            alt_names_s = []
            baseline_pos = []
            test_pos = []
            for alt_id in alt_ids:
                alt = next((a for a in sel_sc.alternatives if a.id == alt_id), None)
                if alt:
                    alt_names_s.append(alt.name)
                    baseline_pos.append(baseline_rank.get(alt_id, 0) + 1)
                    test_pos.append(test_rank.get(alt_id, 0) + 1)

            fig_sens = go.Figure()
            fig_sens.add_trace(go.Scatter(
                x=alt_names_s, y=baseline_pos,
                name='Baseline', mode='lines+markers',
                line=dict(color='#00c2ff', width=2, dash='dot'),
                marker=dict(size=8, color='#00c2ff'),
                hovertemplate='<b>%{x}</b><br>Baseline Rank: %{y}<extra></extra>'
            ))
            fig_sens.add_trace(go.Scatter(
                x=alt_names_s, y=test_pos,
                name='Modified', mode='lines+markers',
                line=dict(color='#1ce783', width=2),
                marker=dict(size=8, color='#1ce783'),
                hovertemplate='<b>%{x}</b><br>New Rank: %{y}<extra></extra>'
            ))
            fig_sens.update_layout(**plotly_config(), height=280, showlegend=True,
                                    legend=dict(font=dict(color='#9999aa', size=11), bgcolor='rgba(0,0,0,0)'),
                                    xaxis=dict(showgrid=False, zeroline=False, tickangle=-20),
                                    yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', zeroline=False,
                                               autorange='reversed', title='Rank', titlefont=dict(size=10)))
            st.plotly_chart(fig_sens, use_container_width=True, config={'displayModeBar': False})
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('<div class="chart-container"><div class="chart-title">Score Comparison</div><div class="chart-subtitle">Baseline vs modified scores side-by-side</div>', unsafe_allow_html=True)
            b_scores = dict(baseline_result.ranked)
            t_scores = dict(test_result.ranked)
            fig_comp = go.Figure()
            fig_comp.add_trace(go.Bar(
                name='Baseline', x=alt_names_s,
                y=[b_scores.get(aid, 0) for aid in alt_ids],
                marker_color='#00c2ff', marker_line_width=0,
                hovertemplate='<b>%{x}</b><br>Baseline: %{y:.1f}<extra></extra>'
            ))
            fig_comp.add_trace(go.Bar(
                name='Modified', x=alt_names_s,
                y=[t_scores.get(aid, 0) for aid in alt_ids],
                marker_color='#1ce783', marker_line_width=0,
                hovertemplate='<b>%{x}</b><br>Modified: %{y:.1f}<extra></extra>'
            ))
            fig_comp.update_layout(**plotly_config(), height=250, barmode='group',
                                    showlegend=True,
                                    legend=dict(font=dict(color='#9999aa', size=11), bgcolor='rgba(0,0,0,0)'),
                                    xaxis=dict(showgrid=False, zeroline=False, tickangle=-15, tickfont=dict(size=10)),
                                    yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', zeroline=False))
            st.plotly_chart(fig_comp, use_container_width=True, config={'displayModeBar': False})
            st.markdown('</div>', unsafe_allow_html=True)

            shifted = [(aid, baseline_rank.get(aid, 0) - test_rank.get(aid, 0)) for aid in alt_ids]
            shifted.sort(key=lambda x: abs(x[1]), reverse=True)
            most_sensitive = next((a for a in sel_sc.alternatives if a.id == shifted[0][0]), None)
            if most_sensitive and shifted[0][1] != 0:
                direction = "rose" if shifted[0][1] < 0 else "fell"
                st.markdown(f"""<div class="highlight-box-blue">
                    <div style="font-size:11px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;color:var(--accent2);margin-bottom:6px;">Most Sensitive Alternative</div>
                    <div style="font-size:16px;font-weight:800;color:var(--text-primary);">{most_sensitive.name}</div>
                    <div style="font-size:13px;color:var(--text-muted);margin-top:4px;">Rank {direction} by {abs(shifted[0][1])} position(s) with modified weights</div>
                </div>""", unsafe_allow_html=True)
        else:
            if baseline_result:
                st.markdown('<div class="chart-container"><div class="chart-title">Baseline Ranking</div>', unsafe_allow_html=True)
                rows_html = ""
                for idx, (alt_id, score) in enumerate(baseline_result.ranked):
                    alt = next((a for a in sel_sc.alternatives if a.id == alt_id), None)
                    if alt:
                        sc_cls = get_score_class(score)
                        rank_cls = "top" if idx == 0 else ""
                        rows_html += f"""<tr>
                            <td><span class="rank-num {rank_cls}">#{idx+1}</span></td>
                            <td style="font-weight:700;">{alt.name}</td>
                            <td><span class="score-pill {sc_cls}">{score:.1f}</span></td>
                        </tr>"""
                st.markdown(f"""<table class="rank-table">
                    <thead><tr><th>Rank</th><th>Alternative</th><th>Score</th></tr></thead>
                    <tbody>{rows_html}</tbody>
                </table>""", unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
                st.info("Adjust weights on the left and click 'Analyze Sensitivity' to see ranking changes.")

    st.markdown('</div>', unsafe_allow_html=True)

def render_compare():
    user = st.session_state.auth["user"]
    db = st.session_state.db

    if user.role == UserRole.REVIEWER.value:
        all_scenarios = [s for s in db["scenarios"] if s.eval_results]
    else:
        all_scenarios = [s for s in db["scenarios"] if s.owner == user.username and s.eval_results]

    st.markdown("""
    <div class="hero-section">
        <div class="hero-breadcrumb">Analysis</div>
        <div class="hero-title">Decision <span>Comparison</span></div>
        <div class="hero-subtitle">Cross-scenario analysis and deep alternative comparisons.</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="page-pad">', unsafe_allow_html=True)

    if not all_scenarios:
        st.markdown('<div class="empty-state"><div class="empty-state-text">No evaluated scenarios available</div></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        return

    sc_opts = {s.name: s for s in all_scenarios}
    sel_sc_name = st.selectbox("Select Scenario to Compare", list(sc_opts.keys()), key="cmp_sel")
    sel_sc = sc_opts[sel_sc_name]

    result = sel_sc.eval_results[-1]
    active_alts = [a for a in sel_sc.alternatives if not a.excluded]

    if len(active_alts) < 2:
        st.warning("Need at least 2 alternatives to compare.")
        st.markdown('</div>', unsafe_allow_html=True)
        return

    st.markdown(f"""<div class="content-card">
        <div class="content-card-title">{sel_sc.name}</div>
        <div class="content-card-meta">{sel_sc.description}</div>
        <div class="tag-row">
            {''.join(f'<span class="tag">{g.name}</span>' for g in sel_sc.goals)}
        </div>
    </div>""", unsafe_allow_html=True)

    col1, col2 = st.columns([3, 2])

    with col1:
        st.markdown('<div class="chart-container"><div class="chart-title">Trade-off Analysis</div><div class="chart-subtitle">Parallel coordinate view of all objectives</div>', unsafe_allow_html=True)
        if len(sel_sc.goals) >= 2:
            dims = []
            for g in sel_sc.goals:
                vals = [a.goal_values.get(g.id, 0) for a in active_alts]
                dims.append(dict(range=[min(vals)-0.01, max(vals)+0.01], label=g.name, values=vals))
            score_vals = [result.scores.get(a.id, 0) for a in active_alts]
            fig_par = go.Figure(data=go.Parcoords(
                line=dict(color=score_vals, colorscale=[[0, '#1a1a24'], [0.5, '#006640'], [1, '#1ce783']],
                          showscale=True, colorbar=dict(title='Score', tickfont=dict(color='#9999aa', size=9), titlefont=dict(color='#9999aa', size=10))),
                dimensions=dims
            ))
            fig_par.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                                   font=dict(color='#9999aa', family='DM Sans', size=10),
                                   height=280, margin=dict(l=80, r=60, t=30, b=20))
            st.plotly_chart(fig_par, use_container_width=True, config={'displayModeBar': False})
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="chart-container"><div class="chart-title">Score vs Top Objective Scatter</div><div class="chart-subtitle">Composite score plotted against leading objective</div>', unsafe_allow_html=True)
        if sel_sc.goals:
            g_top = max(sel_sc.goals, key=lambda g: g.weight)
            x_vals = [a.goal_values.get(g_top.id, 0) for a in active_alts]
            y_vals = [result.scores.get(a.id, 0) for a in active_alts]
            names_scatter = [a.name for a in active_alts]
            fig_scatter = go.Figure()
            fig_scatter.add_trace(go.Scatter(
                x=x_vals, y=y_vals, mode='markers+text',
                text=names_scatter, textposition='top center',
                textfont=dict(size=10, color='#9999aa'),
                marker=dict(size=12, color=y_vals, colorscale=[[0, '#1a1a24'], [1, '#1ce783']],
                            line=dict(width=1, color='rgba(255,255,255,0.1)'),
                            showscale=False),
                hovertemplate='<b>%{text}</b><br>%{x}<br>Score: %{y:.1f}<extra></extra>'
            ))
            fig_scatter.update_layout(**plotly_config(), height=260,
                                       xaxis=dict(title=g_top.name, titlefont=dict(size=11), showgrid=True, gridcolor='rgba(255,255,255,0.05)', zeroline=False),
                                       yaxis=dict(title='Score', titlefont=dict(size=11), showgrid=True, gridcolor='rgba(255,255,255,0.05)', zeroline=False),
                                       showlegend=False)
            st.plotly_chart(fig_scatter, use_container_width=True, config={'displayModeBar': False})
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="chart-container"><div class="chart-title">Side-by-Side Comparison</div><div class="chart-subtitle">All objectives for each alternative</div>', unsafe_allow_html=True)
        header_cells = '<th>Objective</th>' + ''.join(f'<th>{a.name[:12]}</th>' for a in active_alts[:4])
        rows_comp = ""
        for g in sel_sc.goals:
            vals = [a.goal_values.get(g.id, 0) for a in active_alts[:4]]
            best_idx = vals.index(min(vals)) if g.goal_type == "minimize" else vals.index(max(vals))
            cells = ""
            for idx, v in enumerate(vals):
                cls = 'class="best-cell"' if idx == best_idx else ""
                cells += f'<td {cls}>{v:,.0f}</td>'
            rows_comp += f'<tr><td><strong>{g.name}</strong><br><span style="font-size:10px;color:var(--text-muted);">{g.goal_type}</span></td>{cells}</tr>'
        score_cells = ""
        for a in active_alts[:4]:
            s = result.scores.get(a.id, 0)
            sc_cls = get_score_class(s)
            score_cells += f'<td><span class="score-pill {sc_cls}">{s:.1f}</span></td>'
        rows_comp += f'<tr><td><strong>SCORE</strong></td>{score_cells}</tr>'
        st.markdown(f"""<table class="compare-table">
            <thead><tr>{header_cells}</tr></thead>
            <tbody>{rows_comp}</tbody>
        </table>""", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        if len(sel_sc.eval_results) > 1:
            st.markdown('<div class="chart-container"><div class="chart-title">Evaluation History</div><div class="chart-subtitle">Top-ranked alternative per evaluation run</div>', unsafe_allow_html=True)
            runs = []
            tops = []
            for i, er in enumerate(sel_sc.eval_results):
                runs.append(f"Run {i+1}")
                if er.ranked:
                    top_alt = next((a for a in sel_sc.alternatives if a.id == er.ranked[0][0]), None)
                    tops.append(er.ranked[0][1] if top_alt else 0)
                else:
                    tops.append(0)
            fig_hist = go.Figure(go.Scatter(x=runs, y=tops, mode='lines+markers',
                                             line=dict(color='#1ce783', width=2),
                                             marker=dict(size=8, color='#1ce783'),
                                             fill='tozeroy',
                                             fillcolor='rgba(28,231,131,0.06)'))
            fig_hist.update_layout(**plotly_config(), height=200, showlegend=False,
                                    xaxis=dict(showgrid=False, zeroline=False),
                                    yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', zeroline=False, title='Top Score'))
            st.plotly_chart(fig_hist, use_container_width=True, config={'displayModeBar': False})
            st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

def render_review_queue():
    user = st.session_state.auth["user"]
    db = st.session_state.db

    submitted = [s for s in db["scenarios"] if s.status == ScenarioStatus.SUBMITTED.value and s.submitted_to == user.username]
    all_submitted = [s for s in db["scenarios"] if s.status == ScenarioStatus.SUBMITTED.value]

    st.markdown("""
    <div class="hero-section">
        <div class="hero-breadcrumb">Reviewer</div>
        <div class="hero-title">Review <span>Queue</span></div>
        <div class="hero-subtitle">Evaluate submitted planning scenarios and make approval decisions.</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="page-pad">', unsafe_allow_html=True)

    queue = submitted if submitted else all_submitted

    if not queue:
        st.markdown('<div class="empty-state"><div class="empty-state-icon">Q</div><div class="empty-state-text">Review queue is empty</div><div class="empty-state-sub">No scenarios are awaiting your review at this time.</div></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        return

    for s in queue:
        owner_user = db["users"].get(s.owner)
        owner_name = owner_user.name if owner_user else s.owner
        st.markdown(f"""<div class="scenario-list-item">
            <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:10px;">
                <div>
                    <div class="scenario-name">{s.name}</div>
                    <div class="scenario-desc">{s.description}</div>
                </div>
                {status_html(s.status)}
            </div>
            <div class="scenario-meta">
                <div class="scenario-meta-item">Submitted by: <strong>{owner_name}</strong></div>
                <div class="scenario-meta-item">Goals: <strong>{len(s.goals)}</strong></div>
                <div class="scenario-meta-item">Alternatives: <strong>{len(s.alternatives)}</strong></div>
                <div class="scenario-meta-item">Evaluations: <strong>{len(s.eval_results)}</strong></div>
            </div>
        </div>""", unsafe_allow_html=True)

        with st.expander(f"Review Details: {s.name}"):
            reviewer = Reviewer(user, db)
            scenario_detail = reviewer.review_scenario(s)

            if s.goals:
                st.markdown('<div style="font-size:11px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;color:var(--text-muted);margin-bottom:10px;">OBJECTIVES</div>', unsafe_allow_html=True)
                for g in s.goals:
                    ww = (g.weight / max(gg.weight for gg in s.goals)) * 100
                    color = "#1ce783" if g.goal_type == "maximize" else "#ff4757"
                    st.markdown(f"""<div style="display:flex;align-items:center;gap:12px;padding:8px 0;border-bottom:1px solid var(--border);">
                        <div style="font-size:13px;font-weight:700;color:var(--text-primary);min-width:140px;">{g.name}</div>
                        <div class="progress-bar-wrap" style="flex:1;"><div class="progress-bar-fill" style="width:{ww:.0f}%;background:{color};"></div></div>
                        <div style="font-size:12px;color:{color};font-weight:700;min-width:50px;">w={g.weight:.2f}</div>
                        <div style="font-size:11px;color:var(--text-muted);min-width:60px;">{g.goal_type}</div>
                    </div>""", unsafe_allow_html=True)

            if s.eval_results:
                result = s.eval_results[-1]
                st.markdown('<br>', unsafe_allow_html=True)
                st.markdown('<div style="font-size:11px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;color:var(--text-muted);margin-bottom:10px;">RANKED ALTERNATIVES</div>', unsafe_allow_html=True)

                alt_names_r = []
                alt_scores_r = []
                for alt_id, score in result.ranked:
                    alt = next((a for a in s.alternatives if a.id == alt_id), None)
                    if alt:
                        alt_names_r.append(alt.name)
                        alt_scores_r.append(score)

                fig_rev = go.Figure(data=[go.Bar(
                    x=alt_scores_r, y=alt_names_r, orientation='h',
                    marker_color=["#1ce783" if i == 0 else "#2a2a38" for i in range(len(alt_names_r))],
                    marker_line_width=0,
                    text=[f"{sc:.1f}" for sc in alt_scores_r], textposition='outside',
                    textfont=dict(color='#9999aa', size=11)
                )])
                fig_rev.update_layout(**plotly_config(), height=max(160, len(alt_names_r) * 42), showlegend=False,
                                       xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', zeroline=False, range=[0, 115]),
                                       yaxis=dict(showgrid=False, zeroline=False))
                st.plotly_chart(fig_rev, use_container_width=True, config={'displayModeBar': False})

                top_alt_id = result.ranked[0][0] if result.ranked else ""
                top_alt = next((a for a in s.alternatives if a.id == top_alt_id), None)

                if s.assumptions:
                    st.markdown('<div style="font-size:11px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;color:var(--text-muted);margin:14px 0 8px;">DOCUMENTED ASSUMPTIONS</div>', unsafe_allow_html=True)
                    for a in s.assumptions:
                        st.markdown(f'<div class="assumption-row"><div class="assumption-text">{a}</div></div>', unsafe_allow_html=True)

            st.markdown('<div style="height:16px;"></div>', unsafe_allow_html=True)
            st.markdown('<div style="font-size:11px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;color:var(--text-muted);margin-bottom:10px;">REVIEW DECISION</div>', unsafe_allow_html=True)

            available_alts = {a.name: a.id for a in s.alternatives if not a.excluded}
            if available_alts:
                sel_alt_review = st.selectbox("Select Alternative to Approve", list(available_alts.keys()), key=f"rev_alt_{s.id}")
                review_note = st.text_area("Notes / Feedback", key=f"rev_note_{s.id}", placeholder="Provide review notes...", height=80)

                rc1, rc2, rc3 = st.columns(3)
                with rc1:
                    if st.button("APPROVE", key=f"approve_{s.id}"):
                        reviewer.approve_scenario(s, available_alts[sel_alt_review], review_note)
                        st.success(f"Approved: {sel_alt_review}")
                        st.rerun()
                with rc2:
                    if st.button("REQUEST REVISION", key=f"revision_{s.id}"):
                        if not review_note:
                            st.error("Please provide feedback for revision.")
                        else:
                            reviewer.request_revision(s, review_note)
                            st.warning("Revision requested.")
                            st.rerun()
                with rc3:
                    if st.button("REJECT", key=f"reject_{s.id}"):
                        if not review_note:
                            st.error("Please provide rejection reason.")
                        else:
                            reviewer.reject_scenario(s, review_note)
                            st.error("Scenario rejected.")
                            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

def render_approved_history():
    user = st.session_state.auth["user"]
    db = st.session_state.db

    approved = [s for s in db["scenarios"] if s.status == ScenarioStatus.APPROVED.value]

    st.markdown("""
    <div class="hero-section">
        <div class="hero-breadcrumb">Reviewer</div>
        <div class="hero-title">Approved <span>Decisions</span></div>
        <div class="hero-subtitle">History of all approved planning decisions and their outcomes.</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="page-pad">', unsafe_allow_html=True)

    if not approved:
        st.markdown('<div class="empty-state"><div class="empty-state-text">No approved decisions yet</div></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        return

    for s in approved:
        approved_alt = next((a for a in s.alternatives if a.id == s.approved_alt), None)
        approved_name = approved_alt.name if approved_alt else "N/A"
        top_score = ""
        if s.eval_results and s.eval_results[-1].ranked:
            for alt_id, sc in s.eval_results[-1].ranked:
                if alt_id == s.approved_alt:
                    top_score = f"{sc:.1f}"
                    break

        st.markdown(f"""<div class="content-card">
            <div class="content-card-header">
                <div>
                    <div class="content-card-title">{s.name}</div>
                    <div class="content-card-meta">{s.description}</div>
                </div>
                {status_html(s.status)}
            </div>
            <div style="background:rgba(28,231,131,0.05);border:1px solid rgba(28,231,131,0.15);border-radius:8px;padding:14px;margin:12px 0;">
                <div style="font-size:10px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;color:var(--accent);margin-bottom:6px;">APPROVED DECISION</div>
                <div style="font-size:18px;font-weight:800;color:var(--text-primary);">{approved_name}</div>
                {f'<div style="font-family:Bebas Neue,sans-serif;font-size:32px;color:var(--accent);margin-top:4px;">{top_score}<span style="font-family:DM Sans;font-size:14px;color:var(--text-muted);"> score</span></div>' if top_score else ''}
            </div>
            {f'<div class="feedback-card"><div class="feedback-author">Reviewer Notes</div><div class="feedback-text">{s.reviewer_feedback}</div></div>' if s.reviewer_feedback else ''}
        </div>""", unsafe_allow_html=True)

        with st.expander(f"View Full Evaluation - {s.name}"):
            if s.eval_results:
                result = s.eval_results[-1]
                rows_html_h = ""
                for idx, (alt_id, score) in enumerate(result.ranked):
                    alt = next((a for a in s.alternatives if a.id == alt_id), None)
                    if alt:
                        is_approved = alt_id == s.approved_alt
                        sc_cls = get_score_class(score)
                        approved_marker = '<span style="color:var(--accent);font-size:10px;font-weight:700;margin-left:6px;">APPROVED</span>' if is_approved else ""
                        rows_html_h += f"""<tr>
                            <td><span class="rank-num {'top' if idx==0 else ''}">#{idx+1}</span></td>
                            <td><div style="font-weight:700;">{alt.name}{approved_marker}</div></td>
                            <td><span class="score-pill {sc_cls}">{score:.1f}</span></td>
                        </tr>"""
                st.markdown(f"""<table class="rank-table">
                    <thead><tr><th>Rank</th><th>Alternative</th><th>Score</th></tr></thead>
                    <tbody>{rows_html_h}</tbody>
                </table>""", unsafe_allow_html=True)

                alt_names_h = []
                alt_scores_h = []
                for alt_id, sc in result.ranked:
                    alt = next((a for a in s.alternatives if a.id == alt_id), None)
                    if alt:
                        alt_names_h.append(alt.name)
                        alt_scores_h.append(sc)

                fig_h = go.Figure(data=[go.Bar(
                    x=alt_scores_h, y=alt_names_h[::-1], orientation='h',
                    marker_color=["#1ce783" if a == approved_name else "#2a2a38" for a in alt_names_h[::-1]],
                    marker_line_width=0,
                    text=[f"{v:.1f}" for v in alt_scores_h[::-1]], textposition='outside',
                    textfont=dict(color='#9999aa', size=11)
                )])
                fig_h.update_layout(**plotly_config(), height=max(160, len(alt_names_h) * 40), showlegend=False,
                                     xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', zeroline=False, range=[0, 115]),
                                     yaxis=dict(showgrid=False, zeroline=False))
                st.plotly_chart(fig_h, use_container_width=True, config={'displayModeBar': False})

    st.markdown('</div>', unsafe_allow_html=True)

def render_user_management():
    user = st.session_state.auth["user"]
    db = st.session_state.db
    admin = Administrator(user, db)

    st.markdown("""
    <div class="hero-section">
        <div class="hero-breadcrumb">Administrator</div>
        <div class="hero-title">User <span>Management</span></div>
        <div class="hero-subtitle">Create, manage, and control access for all system users.</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="page-pad">', unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["USER DIRECTORY", "CREATE USER", "ARCHIVED SCENARIOS"])

    with tab1:
        all_users = list(db["users"].values())
        role_filter = st.selectbox("Filter by Role", ["All", "planner", "reviewer", "administrator"], key="user_role_filter")
        filtered_users = [u for u in all_users if role_filter == "All" or u.role == role_filter]

        st.markdown(f"<div style='font-size:12px;color:var(--text-muted);font-weight:700;letter-spacing:1px;text-transform:uppercase;margin:12px 0;'>{len(filtered_users)} USERS</div>", unsafe_allow_html=True)

        for u in filtered_users:
            ac, wc = role_color(u.role)
            initials = avatar_initials(u.name)
            status_text = '<span class="deactivated-badge">DEACTIVATED</span>' if not u.active else f'<span class="role-badge role-{u.role}">{u.role}</span>'
            st.markdown(f"""<div class="user-row">
                <div class="user-avatar-sm" style="background:{wc};color:{ac};">{initials}</div>
                <div class="user-info">
                    <div class="user-name">{u.name} {status_text}</div>
                    <div class="user-email">{u.email} &nbsp;|&nbsp; @{u.username}</div>
                </div>
            </div>""", unsafe_allow_html=True)

            if u.username != user.username:
                ucols = st.columns([1, 1, 1, 4])
                with ucols[0]:
                    new_role = st.selectbox("Role", ["planner", "reviewer", "administrator"],
                                             index=["planner", "reviewer", "administrator"].index(u.role),
                                             key=f"role_sel_{u.id}")
                with ucols[1]:
                    if st.button("Update Role", key=f"upd_role_{u.id}"):
                        admin.assign_role(u.username, new_role)
                        st.success(f"Role updated: {new_role}")
                        st.rerun()
                with ucols[2]:
                    if u.active:
                        if st.button("Deactivate", key=f"deact_{u.id}"):
                            u.deactivate()
                            db["activity_log"].insert(0, {
                                "time": datetime.datetime.now().strftime("%H:%M"),
                                "text": f"<span class='log-red'>{user.name}</span> deactivated account <strong>{u.name}</strong>",
                                "color": "#ff4757"
                            })
                            st.warning(f"{u.name} deactivated.")
                            st.rerun()
                    else:
                        if st.button("Reactivate", key=f"react_{u.id}"):
                            u.active = True
                            st.success(f"{u.name} reactivated.")
                            st.rerun()

    with tab2:
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown('<div class="form-section-title">New User Account</div>', unsafe_allow_html=True)
        nc1, nc2 = st.columns(2)
        with nc1:
            new_fname = st.text_input("Full Name", key="adm_fname")
            new_email = st.text_input("Email", key="adm_email")
            new_uname = st.text_input("Username", key="adm_uname")
        with nc2:
            new_role_sel = st.selectbox("Role", ["planner", "reviewer", "administrator"], key="adm_role")
            new_pwd = st.text_input("Initial Password", type="password", key="adm_pwd")
            new_pwd2 = st.text_input("Confirm Password", type="password", key="adm_pwd2")

        if st.button("CREATE USER ACCOUNT", key="adm_create_user"):
            if not all([new_fname, new_email, new_uname, new_pwd, new_pwd2]):
                st.error("All fields required.")
            elif new_pwd != new_pwd2:
                st.error("Passwords do not match.")
            elif new_uname in db["users"]:
                st.error("Username already exists.")
            else:
                admin.create_user(new_uname, new_fname, new_email, new_role_sel, new_pwd)
                st.success(f"Account created for {new_fname}.")
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with tab3:
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown('<div class="form-section-title">Archive Approved Scenarios</div>', unsafe_allow_html=True)
        approved_s = [s for s in db["scenarios"] if s.status == ScenarioStatus.APPROVED.value]
        if not approved_s:
            st.info("No approved scenarios available to archive.")
        else:
            for s in approved_s:
                sc_col1, sc_col2 = st.columns([4, 1])
                with sc_col1:
                    st.markdown(f"<div style='font-size:14px;font-weight:700;color:var(--text-primary);'>{s.name}</div><div style='font-size:12px;color:var(--text-muted);'>{s.created[:10]}</div>", unsafe_allow_html=True)
                with sc_col2:
                    if st.button("Archive", key=f"archive_admin_{s.id}"):
                        admin.archive_scenario(s.id)
                        st.success(f"'{s.name}' archived.")
                        st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

def render_system_config():
    user = st.session_state.auth["user"]
    db = st.session_state.db
    admin = Administrator(user, db)
    eval_svc = db["eval_service"]

    st.markdown("""
    <div class="hero-section">
        <div class="hero-breadcrumb">Administrator</div>
        <div class="hero-title">System <span>Configuration</span></div>
        <div class="hero-subtitle">Configure evaluation parameters, objective templates, and evaluation methods.</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="page-pad">', unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["EVALUATION SERVICE", "OBJECTIVE TEMPLATES", "EVAL METHODS"])

    with tab1:
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown('<div class="form-section-title">Evaluation Service Settings</div>', unsafe_allow_html=True)

        svc_col1, svc_col2 = st.columns(2)
        with svc_col1:
            svc_enabled = st.checkbox("Evaluation Service Enabled", value=eval_svc.enabled, key="svc_enabled")
            model_sel = st.selectbox("Decision Model", ["weighted_scoring", "topsis", "ahp"], index=["weighted_scoring", "topsis", "ahp"].index(eval_svc.decision_model) if eval_svc.decision_model in ["weighted_scoring", "topsis", "ahp"] else 0, key="svc_model")
            max_alts = st.number_input("Max Alternatives Limit", value=eval_svc.max_alts, min_value=5, max_value=200, key="svc_max_alts")
        with svc_col2:
            w_min = st.number_input("Min Allowed Weight", value=float(eval_svc.weight_min), min_value=0.0, max_value=0.5, step=0.01, key="svc_wmin")
            w_max = st.number_input("Max Allowed Weight", value=float(eval_svc.weight_max), min_value=0.5, max_value=1.0, step=0.01, key="svc_wmax")

        st.markdown(f"""<div class="highlight-box" style="margin-top:16px;">
            <div style="display:flex;gap:32px;">
                <div><div style="font-size:10px;font-weight:700;letter-spacing:1px;text-transform:uppercase;color:var(--accent);margin-bottom:4px;">Status</div>
                    <div style="font-size:14px;font-weight:700;color:{'var(--accent)' if eval_svc.enabled else 'var(--danger)'};">{'ACTIVE' if eval_svc.enabled else 'DISABLED'}</div></div>
                <div><div style="font-size:10px;font-weight:700;letter-spacing:1px;text-transform:uppercase;color:var(--accent);margin-bottom:4px;">Model</div>
                    <div style="font-size:14px;font-weight:700;color:var(--text-primary);">{eval_svc.decision_model.replace('_', ' ').title()}</div></div>
                <div><div style="font-size:10px;font-weight:700;letter-spacing:1px;text-transform:uppercase;color:var(--accent);margin-bottom:4px;">Weight Range</div>
                    <div style="font-size:14px;font-weight:700;color:var(--text-primary);">{eval_svc.weight_min} - {eval_svc.weight_max}</div></div>
            </div>
        </div>""", unsafe_allow_html=True)

        if st.button("SAVE CONFIGURATION", key="save_svc_config"):
            admin.configure_evaluation(model_sel, w_min, w_max, svc_enabled)
            eval_svc.max_alts = max_alts
            db["activity_log"].insert(0, {
                "time": datetime.datetime.now().strftime("%H:%M"),
                "text": f"<span class='log-purple'>{user.name}</span> updated evaluation configuration",
                "color": "#a855f7"
            })
            st.success("Configuration saved.")
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with tab2:
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown('<div class="form-section-title">Objective Templates</div>', unsafe_allow_html=True)

        for t in db["templates"]:
            st.markdown(f"""<div class="template-card">
                <div style="display:flex;align-items:flex-start;justify-content:space-between;">
                    <div>
                        <div class="template-name">{t['name']}</div>
                        <div class="template-desc">{t['desc']}</div>
                        <div class="tag-row">{''.join(f'<span class="tag">{o}</span>' for o in t['objectives'])}</div>
                    </div>
                </div>
            </div>""", unsafe_allow_html=True)

        st.markdown('<br><div class="form-section-title">Add New Template</div>', unsafe_allow_html=True)
        t_name = st.text_input("Template Name", key="t_name")
        t_desc = st.text_input("Description", key="t_desc")
        t_objs = st.text_input("Objectives (comma-separated)", key="t_objs", placeholder="e.g., Revenue, Cost, Risk")

        if t_name and t_objs:
            if st.button("ADD TEMPLATE", key="add_template"):
                new_t = {
                    "id": str(uuid.uuid4())[:6],
                    "name": t_name,
                    "desc": t_desc,
                    "objectives": [o.strip() for o in t_objs.split(",")]
                }
                db["templates"].append(new_t)
                st.success(f"Template '{t_name}' added.")
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with tab3:
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown('<div class="form-section-title">Enable / Disable Evaluation Methods</div>', unsafe_allow_html=True)

        method_desc = {
            "Weighted Scoring": "Standard weighted sum model for multi-criteria evaluation",
            "TOPSIS": "Technique for Order Preference by Similarity to Ideal Solution",
            "AHP": "Analytic Hierarchy Process for pairwise comparison",
            "ELECTRE": "Elimination Et Choix Traduisant la Réalité outranking method"
        }

        for method, enabled in db["eval_methods"].items():
            toggle_html = f'<span class="toggle-on">ENABLED</span>' if enabled else f'<span class="toggle-off">DISABLED</span>'
            st.markdown(f"""<div class="eval-method-card" style="margin-bottom:8px;">
                <div>
                    <div class="method-name">{method}</div>
                    <div class="method-desc">{method_desc.get(method, '')}</div>
                </div>
                {toggle_html}
            </div>""", unsafe_allow_html=True)

            mc = st.columns([1, 4])
            with mc[0]:
                toggle_label = "Disable" if enabled else "Enable"
                if st.button(toggle_label, key=f"toggle_method_{method}"):
                    db["eval_methods"][method] = not enabled
                    db["activity_log"].insert(0, {
                        "time": datetime.datetime.now().strftime("%H:%M"),
                        "text": f"<span class='log-purple'>{user.name}</span> {'enabled' if not enabled else 'disabled'} eval method: <strong>{method}</strong>",
                        "color": "#a855f7"
                    })
                    st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

def render_activity_log():
    db = st.session_state.db

    st.markdown("""
    <div class="hero-section">
        <div class="hero-breadcrumb">Administrator</div>
        <div class="hero-title">Activity <span>Log</span></div>
        <div class="hero-subtitle">Complete audit trail of system events, approvals, and user actions.</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="page-pad">', unsafe_allow_html=True)

    col_stats, col_chart = st.columns([1, 2])

    with col_stats:
        all_scenarios = db["scenarios"]
        total_evals = sum(len(s.eval_results) for s in all_scenarios)
        total_submissions = sum(1 for s in all_scenarios if s.status in [ScenarioStatus.SUBMITTED.value, ScenarioStatus.APPROVED.value, ScenarioStatus.REJECTED.value])

        st.markdown(f"""<div class="kpi-card kpi-purple" style="margin-bottom:12px;">
            <div class="kpi-value">{len(db['activity_log'])}</div>
            <div class="kpi-label">Total Log Entries</div>
        </div>""", unsafe_allow_html=True)
        st.markdown(f"""<div class="kpi-card kpi-green" style="margin-bottom:12px;">
            <div class="kpi-value">{total_evals}</div>
            <div class="kpi-label">Total Evaluations</div>
        </div>""", unsafe_allow_html=True)
        st.markdown(f"""<div class="kpi-card kpi-blue">
            <div class="kpi-value">{total_submissions}</div>
            <div class="kpi-label">Submissions</div>
        </div>""", unsafe_allow_html=True)

    with col_chart:
        st.markdown('<div class="chart-container"><div class="chart-title">Scenario Status Distribution</div>', unsafe_allow_html=True)
        all_statuses = {}
        for s in all_scenarios:
            all_statuses[s.status] = all_statuses.get(s.status, 0) + 1
        colors_map = {"draft": "#555566", "active": "#1ce783", "submitted": "#00c2ff",
                      "approved": "#22ff95", "rejected": "#ff4757", "revision": "#ffa502", "archived": "#a855f7"}
        if all_statuses:
            fig = go.Figure(data=[go.Bar(
                x=list(all_statuses.keys()), y=list(all_statuses.values()),
                marker_color=[colors_map.get(k, "#555") for k in all_statuses.keys()],
                marker_line_width=0
            )])
            fig.update_layout(**plotly_config(), height=180, showlegend=False,
                              xaxis=dict(showgrid=False, zeroline=False),
                              yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', zeroline=False))
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="chart-container"><div class="chart-title">System Activity Feed</div><div class="chart-subtitle">All logged system events</div>', unsafe_allow_html=True)

    for log in db["activity_log"]:
        st.markdown(f"""<div class="log-entry">
            <div class="log-time">{log['time']}</div>
            <div class="log-action">{log['text']}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="content-card" style="margin-top:16px;"><div class="form-section-title">Scenario Revision Histories</div>', unsafe_allow_html=True)
    all_sc = db["scenarios"]
    for s in all_sc:
        if s.revision_log:
            with st.expander(f"Revision Log: {s.name} ({len(s.revision_log)} entries)"):
                for entry in reversed(s.revision_log):
                    color = "#1ce783" if "APPROVED" in entry.action else "#00c2ff" if "SUBMITTED" in entry.action else "#ff4757" if "REJECTED" in entry.action else "#a855f7" if "ARCHIVED" in entry.action else "#555566"
                    note_html = f'<br><div style="font-size:11px;color:var(--text-muted);margin-top:3px;font-style:italic;">{entry.note}</div>' if entry.note else ''
                    st.markdown(f"""<div class="log-entry">
                        <div class="log-time">{entry.timestamp}</div>
                        <div class="log-action">
                            <strong>{entry.author}</strong> &mdash; <span style="color:{color};font-weight:700;">{entry.action}</span>{note_html}
                        </div>
                    </div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

def main():
    init_db()

    if not st.session_state.auth["logged_in"]:
        render_auth()
        return

    render_nav()
    user = st.session_state.auth["user"]
    role = user.role
    page = st.session_state.current_page

    nav_col1, nav_col2 = st.columns([6, 1])

    with nav_col1:
        if role == UserRole.PLANNER.value:
            pages = ["dashboard", "scenarios", "create_scenario", "evaluate", "sensitivity", "compare"]
            labels = ["Dashboard", "Scenarios", "New Scenario", "Evaluate", "Sensitivity", "Compare"]
        elif role == UserRole.REVIEWER.value:
            pages = ["dashboard", "review_queue", "approved_history", "compare"]
            labels = ["Dashboard", "Review Queue", "Approved History", "Compare"]
        else:
            pages = ["dashboard", "user_management", "system_config", "activity"]
            labels = ["Dashboard", "Users", "System Config", "Activity Log"]

        st.markdown('<div style="background:var(--bg-secondary);border-bottom:1px solid var(--border);padding:0 40px;display:flex;align-items:center;gap:2px;">', unsafe_allow_html=True)
        nav_cols = st.columns(len(pages))
        for i, (nav_col, nav_page, nav_label) in enumerate(zip(nav_cols, pages, labels)):
            with nav_col:
                is_active = page == nav_page
                btn_style = "background:rgba(28,231,131,0.1);color:var(--accent);border:none;border-bottom:2px solid var(--accent);" if is_active else ""
                if st.button(nav_label, key=f"top_nav_{nav_page}",
                              help=f"Go to {nav_label}"):
                    st.session_state.current_page = nav_page
                    if nav_page != "evaluate":
                        st.session_state.selected_scenario = None
                    st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with nav_col2:
        if st.button("Sign Out", key="top_signout"):
            st.session_state.auth = {"logged_in": False, "user": None}
            st.session_state.current_page = "dashboard"
            st.rerun()

    if page == "dashboard":
        render_dashboard()
    elif page == "scenarios":
        render_scenarios_list()
    elif page == "create_scenario":
        render_create_scenario()
    elif page == "evaluate":
        render_evaluate()
    elif page == "sensitivity":
        render_sensitivity()
    elif page == "compare":
        render_compare()
    elif page == "review_queue":
        render_review_queue()
    elif page == "approved_history":
        render_approved_history()
    elif page == "user_management":
        render_user_management()
    elif page == "system_config":
        render_system_config()
    elif page == "activity":
        render_activity_log()
    else:
        render_dashboard()

if __name__ == "__main__":
    main()