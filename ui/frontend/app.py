import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

st.set_page_config(
    page_title="Project R – Oracle AI",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ──────────────────────────────────────────────────────────────────────────────
# SESSION STATE
# ──────────────────────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

# ──────────────────────────────────────────────────────────────────────────────
# CURRENT PAGE  (driven by ?page= query param)
# ──────────────────────────────────────────────────────────────────────────────
page = st.query_params.get("page", "knowledge_vault")

# ──────────────────────────────────────────────────────────────────────────────
# GLOBAL CSS
# ──────────────────────────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;700;800&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;700&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap');

    /* ── base reset ── */
    html, body { background-color: #0A0A0A !important; }
    .stApp {
        background-color: #131313 !important;
        color: #e5e2e1 !important;
        font-family: 'Inter', sans-serif !important;
    }

    /* ── hide Streamlit chrome ── */
    #MainMenu, footer, 
    [data-testid="stDecoration"],
    [data-testid="stStatusWidget"] { display: none !important; }

    /* ── main content block ── */
    .block-container {
        padding: 2.5rem 2.5rem 5rem 2.5rem !important;
        max-width: 1100px !important;
    }

    /* ────────────────── SIDEBAR ────────────────── */
    [data-testid="stSidebar"] {
        background-color: #1C1B1B !important;
        min-width: 256px !important;
        max-width: 256px !important;
        border-right: 1px solid rgba(60,73,78,0.12) !important;
    }
    [data-testid="stSidebar"] > div:first-child { padding-top: 0 !important; }
    [data-testid="stSidebarNav"] { display: none !important; }

    /* ── nav link styles ── */
    .nav-link {
        display: flex;
        align-items: center;
        gap: 0.7rem;
        padding: 0.75rem 1rem 0.75rem 1.1rem;
        color: rgba(229,226,225,0.38);
        text-decoration: none !important;
        font-family: 'Inter', sans-serif;
        font-size: 0.65rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.13em;
        border-left: 3px solid transparent;
        border-radius: 0 8px 8px 0;
        transition: background 0.18s, color 0.18s;
        margin-bottom: 2px;
    }
    .nav-link:hover {
        background: rgba(42,42,42,0.55);
        color: #00D2FF;
        text-decoration: none !important;
    }
    .nav-link.nav-active {
        background: #2A2A2A;
        color: #00D2FF !important;
        border-left: 3px solid #00D2FF !important;
    }
    .nav-link .ms { font-family: 'Material Symbols Outlined'; font-size: 16px; line-height: 1; }

    /* ── sidebar footer ── */
    .sidebar-footer {
        padding: 1rem 1.1rem;
        border-top: 1px solid rgba(60,73,78,0.15);
        margin-top: 1.5rem;
        font-family: 'Inter', sans-serif;
    }
    .sidebar-footer .status-row {
        display: flex; align-items: center; gap: 0.5rem;
        font-size: 0.58rem; text-transform: uppercase;
        letter-spacing: 0.15em; color: #bbc9cf; font-weight: 600;
        margin-bottom: 0.4rem;
    }
    .sidebar-footer .version {
        font-size: 0.55rem; text-transform: uppercase;
        letter-spacing: 0.1em; color: rgba(229,226,225,0.25);
    }

    /* ── pulse dot ── */
    @keyframes pulse-dot {
        0%,100% { opacity: 1; box-shadow: 0 0 0 0 rgba(0,210,255,0.6); }
        50% { opacity: 0.7; box-shadow: 0 0 0 4px rgba(0,210,255,0); }
    }
    .pulse-dot {
        display: inline-block;
        width: 8px; height: 8px;
        background: #00D2FF;
        border-radius: 50%;
        flex-shrink: 0;
        animation: pulse-dot 2s ease-in-out infinite;
    }

    /* ────────────────── BUTTONS (main area) ────────────────── */
    .main .stButton > button,
    section[data-testid="stMain"] .stButton > button {
        background: linear-gradient(135deg, #a5e7ff 0%, #00D2FF 100%) !important;
        color: #003543 !important;
        border: none !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 700 !important;
        font-size: 0.68rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.12em !important;
        border-radius: 4px !important;
        padding: 0.65rem 1.6rem !important;
        transition: filter 0.2s ease, transform 0.15s ease !important;
        box-shadow: 0 4px 16px rgba(0,210,255,0.15) !important;
    }
    .main .stButton > button:hover,
    section[data-testid="stMain"] .stButton > button:hover {
        filter: brightness(1.1) !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 20px rgba(0,210,255,0.25) !important;
    }
    .main .stButton > button:active,
    section[data-testid="stMain"] .stButton > button:active {
        transform: scale(0.97) !important;
    }

    /* ────────────────── INPUTS ────────────────── */
    .stTextInput > div > div > input,
    .stTextArea textarea {
        background-color: #0E0E0E !important;
        border: 1px solid rgba(60,73,78,0.3) !important;
        border-radius: 4px !important;
        color: #e5e2e1 !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 0.875rem !important;
    }
    .stTextInput > div > div > input:focus,
    .stTextArea textarea:focus {
        border-color: #00D2FF !important;
        box-shadow: 0 0 0 1px rgba(0,210,255,0.25) !important;
    }
    .stTextInput > div > div > input::placeholder,
    .stTextArea textarea::placeholder { color: #859399 !important; }

    /* ────────────────── FILE UPLOADER ────────────────── */
    [data-testid="stFileUploaderDropzone"] {
        background-color: #1C1B1B !important;
        border: 1px dashed rgba(0,210,255,0.35) !important;
        border-radius: 8px !important;
        transition: border-color 0.2s !important;
    }
    [data-testid="stFileUploaderDropzone"]:hover {
        border-color: rgba(0,210,255,0.6) !important;
    }
    [data-testid="stFileUploaderDropzone"] p,
    [data-testid="stFileUploaderDropzone"] span,
    [data-testid="stFileUploaderDropzone"] small { color: #bbc9cf !important; }

    /* ────────────────── RADIO ────────────────── */
    [data-testid="stRadio"] label {
        color: rgba(229,226,225,0.7) !important;
        font-size: 0.82rem !important;
        text-transform: none !important;
        letter-spacing: 0 !important;
        font-weight: 400 !important;
    }

    /* ────────────────── TABS ────────────────── */
    .stTabs [data-baseweb="tab-list"] {
        background: transparent !important;
        border-bottom: 1px solid rgba(60,73,78,0.2) !important;
        gap: 0 !important;
    }
    .stTabs [data-baseweb="tab"] {
        background: transparent !important;
        color: rgba(229,226,225,0.38) !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 0.65rem !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.13em !important;
        border-bottom: 2px solid transparent !important;
        padding: 0.75rem 1.5rem !important;
        transition: color 0.2s !important;
    }
    .stTabs [aria-selected="true"] {
        color: #00D2FF !important;
        border-bottom: 2px solid #00D2FF !important;
        background: transparent !important;
    }
    .stTabs [data-baseweb="tab-highlight"],
    .stTabs [data-baseweb="tab-border"] { display: none !important; }

    /* ────────────────── CHAT ────────────────── */
    [data-testid="stChatMessage"] {
        background-color: #1C1B1B !important;
        border-radius: 8px !important;
        border: 1px solid rgba(60,73,78,0.15) !important;
        padding: 1.1rem 1.25rem !important;
        margin-bottom: 0.75rem !important;
    }
    /* assistant message gets a left cyan accent */
    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) {
        border-left: 2px solid rgba(0,210,255,0.35) !important;
    }
    [data-testid="stChatMessage"] p {
        color: #e5e2e1 !important;
        font-size: 0.9rem !important;
        line-height: 1.7 !important;
    }

    /* ── chat input ── */
    [data-testid="stChatInput"] > div {
        background-color: #1C1B1B !important;
        border: 1px solid rgba(60,73,78,0.3) !important;
        border-radius: 8px !important;
    }
    [data-testid="stChatInput"]:focus-within > div {
        border-color: rgba(0,210,255,0.4) !important;
        box-shadow: 0 0 0 1px rgba(0,210,255,0.12) !important;
    }
    [data-testid="stChatInput"] textarea {
        color: #e5e2e1 !important;
        background: transparent !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 0.9rem !important;
    }
    [data-testid="stChatInput"] textarea::placeholder { color: #859399 !important; }
    [data-testid="stChatInput"] button {
        background: linear-gradient(135deg, #a5e7ff 0%, #00D2FF 100%) !important;
        color: #003543 !important;
        border-radius: 4px !important;
    }

    /* ────────────────── ALERTS ────────────────── */
    [data-testid="stAlert"] {
        border-radius: 4px !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 0.82rem !important;
    }
    [data-testid="stSuccessMessage"],
    div[data-baseweb="notification"][kind="positive"] {
        background: rgba(0,210,255,0.05) !important;
        border-left: 3px solid #00D2FF !important;
        color: #e5e2e1 !important;
        border-radius: 0 4px 4px 0 !important;
    }
    [data-testid="stWarningMessage"] {
        background: rgba(255,178,41,0.06) !important;
        border-left: 3px solid #FFB229 !important;
        color: #e5e2e1 !important;
        border-radius: 0 4px 4px 0 !important;
    }
    [data-testid="stErrorMessage"] {
        background: rgba(255,180,171,0.06) !important;
        border-left: 3px solid #ffb4ab !important;
        color: #e5e2e1 !important;
        border-radius: 0 4px 4px 0 !important;
    }

    /* ────────────────── LABELS ────────────────── */
    label, .stLabel, [data-testid="stWidgetLabel"] p {
        color: #bbc9cf !important;
        font-size: 0.7rem !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.09em !important;
        font-family: 'Inter', sans-serif !important;
    }
    /* Fix radio + text area labels to allow normal case */
    [data-testid="stRadio"] [data-testid="stWidgetLabel"] p,
    [data-testid="stTextArea"] [data-testid="stWidgetLabel"] p,
    [data-testid="stTextInput"] [data-testid="stWidgetLabel"] p {
        text-transform: uppercase !important;
    }

    /* ────────────────── SCROLLBAR ────────────────── */
    ::-webkit-scrollbar { width: 4px; }
    ::-webkit-scrollbar-track { background: #131313; }
    ::-webkit-scrollbar-thumb { background: #2A2A2A; border-radius: 10px; }
    ::-webkit-scrollbar-thumb:hover { background: #00D2FF; }

    /* ────────────────── DIVIDER ────────────────── */
    hr { border-color: rgba(60,73,78,0.15) !important; margin: 1.5rem 0 !important; }

    /* ────────────────── CUSTOM COMPONENTS ────────────────── */

    /* page header */
    .page-eyebrow {
        font-family: 'Inter', sans-serif;
        font-size: 0.58rem; font-weight: 700;
        text-transform: uppercase; letter-spacing: 0.2em;
        color: #00D2FF; margin-bottom: 0.4rem;
    }
    .page-title {
        font-family: 'Manrope', sans-serif;
        font-weight: 800; font-size: 1.85rem;
        color: #e5e2e1; letter-spacing: -0.02em;
        line-height: 1.15; margin-bottom: 0.3rem;
    }
    .page-desc {
        font-size: 0.82rem; color: #859399;
        max-width: 560px; line-height: 1.6;
    }

    /* section card */
    .s-card {
        background: #1C1B1B;
        border-radius: 8px;
        padding: 1.5rem;
        border: 1px solid rgba(60,73,78,0.12);
        margin-bottom: 1.25rem;
    }
    .s-card-title {
        font-family: 'Inter', sans-serif;
        font-size: 0.62rem; font-weight: 700;
        text-transform: uppercase; letter-spacing: 0.15em;
        color: #00D2FF; margin-bottom: 0.75rem;
    }

    /* stat chip */
    .stat-chip {
        display: inline-flex; align-items: center; gap: 0.4rem;
        padding: 0.3rem 0.75rem;
        background: #2A2A2A;
        border-radius: 4px;
        font-family: 'Inter', sans-serif;
        font-size: 0.6rem; font-weight: 600;
        text-transform: uppercase; letter-spacing: 0.09em;
        color: #bbc9cf;
        margin-right: 0.5rem; margin-bottom: 0.5rem;
    }
    .stat-chip .val { color: #e5e2e1; }
    .stat-chip.cyan .val { color: #00D2FF; }

    /* oracle system message */
    .oracle-init {
        display: flex; gap: 1.2rem; align-items: flex-start;
        padding: 1.5rem; background: rgba(0,210,255,0.04);
        border: 1px solid rgba(0,210,255,0.12);
        border-radius: 8px; margin-bottom: 1.5rem;
    }
    .oracle-icon {
        width: 40px; height: 40px; flex-shrink: 0;
        background: rgba(0,210,255,0.08);
        border: 1px solid rgba(0,210,255,0.2);
        border-radius: 8px;
        display: flex; align-items: center; justify-content: center;
        font-family: 'Manrope', sans-serif;
        font-weight: 900; font-size: 1.1rem;
        color: #00D2FF;
        box-shadow: 0 0 16px rgba(0,210,255,0.1);
    }
    .oracle-init-text {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.85rem; color: #e5e2e1;
        line-height: 1.65; letter-spacing: -0.01em;
    }
    .oracle-init-label {
        font-size: 0.58rem; font-weight: 700;
        text-transform: uppercase; letter-spacing: 0.18em;
        color: #00D2FF; margin-bottom: 0.4rem;
    }

    /* status indicator */
    .neural-status {
        display: inline-flex; align-items: center; gap: 0.5rem;
        padding: 0.3rem 0.75rem;
        background: #1C1B1B;
        border: 1px solid rgba(60,73,78,0.2);
        border-radius: 4px;
        font-size: 0.58rem; font-weight: 700;
        text-transform: uppercase; letter-spacing: 0.15em;
        color: #bbc9cf;
    }

    /* ingest success card */
    .ingest-result {
        background: rgba(0,210,255,0.05);
        border: 1px solid rgba(0,210,255,0.2);
        border-radius: 8px;
        padding: 1rem 1.25rem;
        margin-top: 1rem;
        display: flex; align-items: center; gap: 0.75rem;
    }
    .ingest-result-icon {
        font-size: 1.2rem; color: #00D2FF;
    }
    .ingest-result-text {
        font-family: 'Inter', sans-serif;
        font-size: 0.82rem; color: #e5e2e1; line-height: 1.5;
    }
    .ingest-result-text strong { color: #00D2FF; }

    /* clear chat button override */
    .clear-btn > div > .stButton > button {
        background: transparent !important;
        color: rgba(229,226,225,0.35) !important;
        border: 1px solid rgba(60,73,78,0.25) !important;
        font-size: 0.6rem !important;
        padding: 0.35rem 0.75rem !important;
        box-shadow: none !important;
    }
    .clear-btn > div > .stButton > button:hover {
        color: #ffb4ab !important;
        border-color: rgba(255,180,171,0.4) !important;
        filter: none !important;
        transform: none !important;
        box-shadow: none !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ──────────────────────────────────────────────────────────────────────────────
# SIDEBAR
# ──────────────────────────────────────────────────────────────────────────────
def render_sidebar(current_page: str) -> None:
    with st.sidebar:
        # ── Brand ──
        st.markdown(
            """
            <div style="padding: 1.75rem 1.1rem 1.5rem 1.1rem;">
                <div style="display:flex; align-items:center; gap:0.65rem;">
                    <div style="
                        width:34px; height:34px; flex-shrink:0;
                        background: linear-gradient(135deg,#a5e7ff,#00D2FF);
                        border-radius:5px;
                        display:flex; align-items:center; justify-content:center;
                        color:#003543; font-weight:900; font-size:15px;
                        box-shadow: 0 0 14px rgba(0,210,255,0.25);
                    ">⚡</div>
                    <div>
                        <div style="
                            font-family:'Manrope',sans-serif;
                            font-weight:800; font-size:0.95rem;
                            color:#e5e2e1; line-height:1;
                        ">Project R</div>
                        <div style="
                            font-family:'Inter',sans-serif;
                            font-size:0.5rem; font-weight:700;
                            text-transform:uppercase; letter-spacing:0.22em;
                            color:#00D2FF; margin-top:3px;
                        ">ORACLE AI V1.0</div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # ── Nav items ──
        nav_items = [
            ("knowledge_vault",  "database",  "Knowledge Vault"),
            ("the_oracle",       "psychology", "The Oracle"),
        ]

        nav_html = '<nav style="padding: 0 0.25rem;">'
        for key, ms_icon, label in nav_items:
            active_cls = "nav-link nav-active" if current_page == key else "nav-link"
            nav_html += f"""
            <a href="?page={key}" target="_self" class="{active_cls}">
                <span class="ms">{ms_icon}</span>
                {label}
            </a>"""
        nav_html += "</nav>"
        st.markdown(nav_html, unsafe_allow_html=True)

        # ── Footer ──
        st.markdown(
            """
            <div class="sidebar-footer">
                <div class="status-row">
                    <span class="pulse-dot"></span>
                    Neural Engine Active
                </div>
                <div class="version">v1.0.0 &nbsp;·&nbsp; Agentic RAG</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


# ──────────────────────────────────────────────────────────────────────────────
# PAGE: KNOWLEDGE VAULT
# ──────────────────────────────────────────────────────────────────────────────
def render_knowledge_vault() -> None:
    # ── Page header ──
    st.markdown(
        """
        <div style="margin-bottom:2rem;">
            <div class="page-eyebrow">01 — Knowledge Vault</div>
            <div class="page-title">Ingest Documents</div>
            <div class="page-desc">
                Feed raw text or PDF documents into the neural knowledge base.
                Each document is chunked, embedded, and indexed into Qdrant for
                semantic retrieval.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Tabs ──
    tab_text, tab_pdf = st.tabs(["  ✦ Text Document", "  ✦ PDF Upload"])

    # ──────── TEXT INGEST ────────
    with tab_text:
        st.markdown(
            """
            <div style="height:1.25rem;"></div>
            <div class="s-card-title">Raw Context Stream</div>
            """,
            unsafe_allow_html=True,
        )

        col_left, col_right = st.columns([3, 2], gap="large")

        with col_left:
            source_name = st.text_input(
                "Document name (optional)",
                placeholder="e.g. HR_Policies_Q3",
                key="text_source",
            )
            text_body = st.text_area(
                "Paste document text",
                placeholder="Paste technical documentation, system notes, or unstructured content here...",
                height=260,
                key="text_body",
            )

        with col_right:
            st.markdown(
                """
                <div class="s-card" style="margin-top:0.1rem;">
                    <div class="s-card-title">Neural Integration</div>
                    <div style="space-y:0.75rem;">
                        <div style="display:flex; justify-content:space-between; align-items:center;
                                    font-size:0.72rem; padding:0.5rem 0;
                                    border-bottom:1px solid rgba(60,73,78,0.12);">
                            <span style="color:#859399;">Pipeline</span>
                            <span style="color:#00D2FF;">Text → Chunk → Embed</span>
                        </div>
                        <div style="display:flex; justify-content:space-between; align-items:center;
                                    font-size:0.72rem; padding:0.5rem 0;
                                    border-bottom:1px solid rgba(60,73,78,0.12);">
                            <span style="color:#859399;">Vector Store</span>
                            <span style="color:#e5e2e1;">Qdrant</span>
                        </div>
                        <div style="display:flex; justify-content:space-between; align-items:center;
                                    font-size:0.72rem; padding:0.5rem 0;">
                            <span style="color:#859399;">Transport</span>
                            <span style="color:#e5e2e1;">Kafka Stream</span>
                        </div>
                    </div>
                    <div style="margin-top:1rem; background:#0E0E0E; height:3px; border-radius:2px; overflow:hidden;">
                        <div style="width:40%; height:100%;
                                    background:linear-gradient(90deg,#a5e7ff,#00D2FF);
                                    box-shadow:0 0 8px rgba(0,210,255,0.4);"></div>
                    </div>
                    <div style="font-size:0.6rem; color:#859399; margin-top:0.4rem; text-align:right; text-transform:uppercase; letter-spacing:0.1em;">Ready</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            ingest_text_btn = st.button(
                "⚡  Process Text",
                key="ingest_text_btn",
                use_container_width=True,
            )

        if ingest_text_btn:
            if not text_body.strip():
                st.warning("Please enter some text before ingesting.")
            else:
                with st.spinner("Streaming to neural pipeline..."):
                    try:
                        response = requests.post(
                            f"{BACKEND_URL}/ingest/text",
                            json={
                                "text": text_body,
                                "source": source_name.strip() or "manual_text",
                            },
                            timeout=30,
                        )
                        if response.status_code == 200:
                            data = response.json()
                            chunks = data.get("chunks", "—")
                            st.markdown(
                                f"""
                                <div class="ingest-result">
                                    <div class="ingest-result-icon">✦</div>
                                    <div class="ingest-result-text">
                                        Successfully queued <strong>{chunks} chunks</strong>
                                        into the neural knowledge base.
                                        The embeddings will be indexed momentarily.
                                    </div>
                                </div>
                                """,
                                unsafe_allow_html=True,
                            )
                        else:
                            st.error(f"Ingestion failed — server returned {response.status_code}.")
                    except requests.exceptions.RequestException as exc:
                        st.error(f"Connection error: {exc}")

    # ──────── PDF INGEST ────────
    with tab_pdf:
        st.markdown(
            """
            <div style="height:1.25rem;"></div>
            <div class="s-card-title">PDF Neural Upload</div>
            """,
            unsafe_allow_html=True,
        )

        col_upload, col_info = st.columns([3, 2], gap="large")

        with col_upload:
            uploaded_file = st.file_uploader(
                "Drop a PDF file",
                type=["pdf"],
                key="pdf_upload",
                help="Maximum recommended size: 128 MB",
            )

            if uploaded_file:
                st.markdown(
                    f"""
                    <div style="
                        display:flex; align-items:center; gap:0.6rem;
                        padding:0.6rem 0.9rem; background:#2A2A2A;
                        border-radius:5px; margin-top:0.75rem;
                        font-size:0.75rem;
                    ">
                        <span style="color:#00D2FF; font-size:0.9rem;">📄</span>
                        <span style="color:#e5e2e1; font-weight:600;">{uploaded_file.name}</span>
                        <span style="color:#859399; margin-left:auto;">
                            {uploaded_file.size / 1024:.1f} KB
                        </span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            ingest_pdf_btn = st.button(
                "⚡  Process PDF",
                key="ingest_pdf_btn",
                use_container_width=False,
                disabled=uploaded_file is None,
            )

        with col_info:
            st.markdown(
                """
                <div class="s-card" style="margin-top:0.1rem;">
                    <div class="s-card-title">Supported Formats</div>
                    <div style="display:flex; flex-wrap:wrap; gap:0.4rem; margin-bottom:1rem;">
                        <span class="stat-chip"><span class="val">.pdf</span></span>
                    </div>
                    <div class="s-card-title" style="margin-top:0.75rem;">Processing Steps</div>
                    <ol style="
                        padding-left:1.1rem;
                        font-size:0.72rem; color:#859399;
                        line-height:2;
                    ">
                        <li>Text extraction via pdfplumber</li>
                        <li>Whitespace normalisation</li>
                        <li>Semantic chunking</li>
                        <li>Embedding → Qdrant ingestion</li>
                    </ol>
                </div>
                """,
                unsafe_allow_html=True,
            )

        if ingest_pdf_btn and uploaded_file:
            with st.spinner("Extracting & streaming PDF to pipeline..."):
                try:
                    files = {
                        "file": (
                            uploaded_file.name,
                            uploaded_file,
                            "application/pdf",
                        )
                    }
                    response = requests.post(
                        f"{BACKEND_URL}/ingest/pdf",
                        files=files,
                        timeout=60,
                    )
                    if response.status_code == 200:
                        data = response.json()
                        chunks = data.get("chunks", "—")
                        st.markdown(
                            f"""
                            <div class="ingest-result">
                                <div class="ingest-result-icon">✦</div>
                                <div class="ingest-result-text">
                                    <strong>{uploaded_file.name}</strong> processed —
                                    <strong>{chunks} chunks</strong> queued for neural indexing.
                                </div>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )
                    else:
                        st.error(f"PDF ingestion failed — server returned {response.status_code}.")
                except requests.exceptions.RequestException as exc:
                    st.error(f"Connection error: {exc}")


# ──────────────────────────────────────────────────────────────────────────────
# PAGE: THE ORACLE (Chat)
# ──────────────────────────────────────────────────────────────────────────────
def render_oracle() -> None:
    # ── Page header row ──
    col_title, col_status = st.columns([5, 2], gap="small")
    with col_title:
        st.markdown(
            """
            <div style="margin-bottom:1.5rem;">
                <div class="page-eyebrow">02 — The Oracle</div>
                <div class="page-title">Query Intelligence</div>
                <div class="page-desc">
                    Ask questions against your ingested knowledge base.
                    The agentic RAG pipeline retrieves, reasons, and responds.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col_status:
        st.markdown(
            """
            <div style="display:flex; justify-content:flex-end; align-items:center; height:100%; padding-top:1rem;">
                <div class="neural-status">
                    <span class="pulse-dot"></span>
                    Neural Engine Active
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ── System init message (shown when no history) ──
    if not st.session_state.messages:
        st.markdown(
            """
            <div class="oracle-init">
                <div class="oracle-icon">Σ</div>
                <div>
                    <div class="oracle-init-label">The Oracle · System Core</div>
                    <div class="oracle-init-text">
                        SYSTEM_CORE initialized. Neural Engine optimized for semantic retrieval.
                        Agentic RAG pipeline active. Query your knowledge base below.
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ── Chat history ──
    for msg in st.session_state.messages:
        avatar = "🧠" if msg["role"] == "assistant" else "👤"
        with st.chat_message(msg["role"], avatar=avatar):
            st.write(msg["content"])

    # ── Clear history ──
    if st.session_state.messages:
        st.markdown('<div class="clear-btn">', unsafe_allow_html=True)
        col_gap, col_clear = st.columns([8, 2])
        with col_clear:
            if st.button("✕  Clear history", key="clear_chat"):
                st.session_state.messages = []
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    # ── Input ──
    if question := st.chat_input("Query the Oracle..."):
        st.session_state.messages.append({"role": "user", "content": question})
        with st.chat_message("user", avatar="👤"):
            st.write(question)

        with st.chat_message("assistant", avatar="🧠"):
            with st.spinner("Querying neural engine..."):
                try:
                    response = requests.post(
                        f"{BACKEND_URL}/chat",
                        json={"question": question},
                        timeout=60,
                    )
                    if response.status_code == 200:
                        answer = response.json().get("answer", "No answer returned.")
                        st.write(answer)
                        st.session_state.messages.append(
                            {"role": "assistant", "content": answer}
                        )
                    else:
                        err = f"Oracle encountered an error (HTTP {response.status_code}). Please try again."
                        st.error(err)
                        st.session_state.messages.append(
                            {"role": "assistant", "content": err}
                        )
                except requests.exceptions.RequestException as exc:
                    err = f"Connection error — could not reach backend: {exc}"
                    st.error(err)
                    st.session_state.messages.append(
                        {"role": "assistant", "content": err}
                    )


# ──────────────────────────────────────────────────────────────────────────────
# MAIN
# ──────────────────────────────────────────────────────────────────────────────
render_sidebar(page)

if page == "the_oracle":
    render_oracle()
else:
    render_knowledge_vault()
