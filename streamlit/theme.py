import streamlit as st

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600;700&display=swap');
:root{--ink:#0E1A22;--panel:#152631;--line:#25404F;--txt:#E7EFF3;--mute:#8FA7B5;--teal:#2EC4B6;--amber:#F4A259;--red:#E5484D;--green:#3DD68C}
html,body,[class*="css"],.stApp{font-family:'IBM Plex Sans',sans-serif}
.stApp{background:var(--ink);color:var(--txt)}
.block-container{padding-top:2rem;max-width:1300px}
[data-testid="stSidebar"]{background:#0A131A;border-right:1px solid var(--line)}
.brand{font-size:1.9rem;font-weight:700;margin-top:.5rem}.brand span{color:var(--teal)}
.brand-sub{color:var(--mute);font-size:1rem;margin-bottom:1rem}
h1{font-weight:700;letter-spacing:-.02em}
h2,h3{font-weight:600}
.page-head{margin-bottom:1.2rem}.page-head p{color:var(--mute);margin:.2rem 0 0}
.kpi{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:1rem 1.2rem}
.kpi .l{color:var(--mute);font-size:.85rem}.kpi .v{font-size:1.9rem;font-weight:700;line-height:1.2}
.kpi .s{font-size:.85rem;margin-top:.2rem}
.pill{display:inline-block;padding:.15rem .7rem;border-radius:99px;font-size:.8rem;font-weight:600}
.pill.g{background:rgba(61,214,140,.15);color:var(--green)}.pill.y{background:rgba(244,162,89,.15);color:var(--amber)}.pill.r{background:rgba(229,72,77,.18);color:var(--red)}
.stButton>button,.stDownloadButton>button,.stFormSubmitButton>button,button[data-testid^="baseButton-"]{border-radius:8px!important;font-weight:600!important}
/* Predict and other primary action buttons outside the sidebar keep Streamlit's default red. */
[data-testid="stExpander"],[data-testid="stForm"]{background:var(--panel);border:1px solid var(--line);border-radius:10px}
[data-testid="stDataFrame"]{border:1px solid var(--line);border-radius:8px}
hr{border-color:var(--line)}

[data-testid="stSidebar"] .stButton>button{width:100%;justify-content:flex-start;text-align:left;background:transparent;border:1px solid transparent;color:var(--mute);padding:.85rem 1rem;min-height:3.2rem}
[data-testid="stSidebar"] .stButton>button:hover{background:var(--panel);color:var(--txt);border-color:var(--line)}
[data-testid="stSidebar"] .stButton>button[kind="primary"]{background:linear-gradient(90deg,rgba(46,196,182,.28),rgba(46,196,182,.08));color:#fff;border:1px solid rgba(46,196,182,.5);border-left:4px solid var(--teal)}
[data-testid="stSidebar"] .stButton>button p{text-align:left;font-size:1.25rem;font-weight:500}
[data-testid="stSidebar"] [data-testid="stCaptionContainer"]{font-size:1rem}
[data-testid="stSidebar"] [data-testid="stCaptionContainer"] p{font-size:1rem}
.gh-link{position:fixed;right:28px;bottom:28px;z-index:9999;display:inline-flex;align-items:center;justify-content:center;width:52px;height:52px;border-radius:50%;background:var(--panel);border:1px solid var(--line);transition:.2s}
.gh-link:hover{border-color:var(--teal);transform:translateY(-2px)}
.gh-link svg{fill:var(--txt);position:absolute}
.gh-link img{position:absolute;inset:0;width:100%;height:100%;border-radius:50%;object-fit:cover}
.gh-link .badge{position:absolute;right:-4px;bottom:-4px;width:20px;height:20px;border-radius:50%;background:#0A131A;border:1px solid var(--line);display:flex;align-items:center;justify-content:center}
.gh-link .badge svg{position:static}

[data-baseweb="tab-highlight"],[data-baseweb="tab-border"]{display:none!important}
[data-baseweb="tab-list"]{gap:.4rem!important;padding:.35rem!important;background:var(--panel)!important;border:1px solid var(--line)!important;border-radius:12px!important;flex-wrap:wrap}
button[data-baseweb="tab"],button[role="tab"]{height:auto!important;padding:.55rem 1.2rem!important;border-radius:9px!important;color:var(--mute)!important;background:transparent!important;transition:.2s}
button[data-baseweb="tab"] p,button[role="tab"] p{font-size:1.05rem!important;font-weight:600!important;color:inherit!important}
button[data-baseweb="tab"]:hover,button[role="tab"]:hover{background:rgba(46,196,182,.12)!important;color:#fff!important}
button[data-baseweb="tab"][aria-selected="true"],button[role="tab"][aria-selected="true"]{background:var(--teal)!important;color:#062B27!important}
[data-baseweb="tab-panel"]{padding-top:1.4rem!important}
.card-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:.9rem;margin:.6rem 0 1.4rem}
.card{position:relative;background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:1.1rem;transition:.25s}
.card:hover{transform:translateY(-4px);border-color:var(--teal);box-shadow:0 10px 24px rgba(0,0,0,.35)}
.card .ic{font-size:1.9rem}.card .n{position:absolute;top:.7rem;right:.9rem;color:var(--teal);font-weight:700;opacity:.7}
.card h4{margin:.5rem 0 .25rem;font-size:1.05rem}.card p{margin:0;color:var(--mute);font-size:.92rem;line-height:1.5}
[data-testid="stExpander"] summary{font-weight:600;font-size:1.02rem}

[data-testid="stHorizontalBlock"]:has(.tabnav-marker){gap:.5rem;padding:.4rem;background:var(--panel);border:1px solid var(--line);border-radius:14px}
.tabnav-marker{display:block;height:0;margin:0;padding:0}
[data-testid="stHorizontalBlock"]:has(.tabnav-marker) [data-testid="stVerticalBlock"]{gap:0!important}
[data-testid="stHorizontalBlock"]:has(.tabnav-marker) [data-testid="stElementContainer"]:has(.tabnav-marker),[data-testid="stHorizontalBlock"]:has(.tabnav-marker) .element-container:has(.tabnav-marker){height:0;min-height:0;margin:0;overflow:hidden}
[data-testid="stHorizontalBlock"]:has(.tabnav-marker){align-items:flex-start}
[data-testid="stHorizontalBlock"]:has(.tabnav-marker) .stButton>button{width:100%;background:transparent;border:1px solid transparent;color:var(--mute);padding:.7rem .5rem}
[data-testid="stHorizontalBlock"]:has(.tabnav-marker) .stButton>button p{font-size:1.1rem;font-weight:600}
[data-testid="stHorizontalBlock"]:has(.tabnav-marker) .stButton>button:hover{background:rgba(46,196,182,.14);color:#fff}
[data-testid="stHorizontalBlock"]:has(.tabnav-marker) .stButton>button[kind="primary"]{background:var(--teal);color:#062B27;box-shadow:0 4px 14px rgba(46,196,182,.35)}
</style>
"""

RTL = """<style>
[data-testid="stMarkdownContainer"],.page-head,.kpi,label,[data-testid="stCaptionContainer"],.brand,.brand-sub{direction:rtl;text-align:right}
[data-testid="stSidebar"] .stButton>button{justify-content:flex-start;direction:rtl;text-align:right}
[data-testid="stSidebar"] .stButton>button p{text-align:right}
[data-baseweb="tab-list"]{direction:rtl}
.js-plotly-plot,[data-testid="stDataFrame"]{direction:ltr}
</style>"""


def inject_css(lang="en"):
    st.markdown(CSS, unsafe_allow_html=True)
    if lang == "ar":
        st.markdown(RTL, unsafe_allow_html=True)

def page_head(title, subtitle=""):
    st.markdown(f"<div class='page-head'><h1>{title}</h1><p>{subtitle}</p></div>", unsafe_allow_html=True)

def pill(status, names=None):
    word = status.split(' ')[-1]
    label = (names or {}).get(word, word)
    cls = 'r' if 'Red' in status else 'y' if 'Yellow' in status else 'g' if 'Green' in status else 'y'
    return f"<span class='pill {cls}'>{label}</span>"

def kpi(label, value, sub=""):
    return f"<div class='kpi'><div class='l'>{label}</div><div class='v'>{value}</div><div class='s'>{sub}</div></div>"
