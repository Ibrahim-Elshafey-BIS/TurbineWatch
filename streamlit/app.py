import streamlit as st
from theme import inject_css
from model_loader import get_available_models
from i18n import t
from ui_components import (init_session_state, render_dashboard, render_single_prediction,
    render_batch_prediction, render_model_comparison, render_feature_importance,
    render_settings, render_about)

st.set_page_config(page_title="Gas Turbine Emissions", page_icon="🏭", layout="wide",
                   initial_sidebar_state="expanded")
st.session_state.setdefault('lang', 'en')
inject_css(st.session_state['lang'])
init_session_state()

PAGES = {
    "dash": ("📊", render_dashboard), "single": ("🎯", render_single_prediction),
    "compare": ("⚖️", render_model_comparison), "impact": ("🔬", render_feature_importance),
    "batch": ("📁", render_batch_prediction), "settings": ("⚙️", render_settings), "about": ("ℹ️", render_about),
}

GITHUB_URL = "https://github.com/Ibrahim-Elshafey-BIS"
GITHUB_MARK = ("M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z")
# The avatar sits on top of a GitHub mark; if the image cannot load, the mark stays visible.
GITHUB_LOGO = (
    f"<a class='gh-link' href='{GITHUB_URL}' target='_blank' title='GitHub: Ibrahim-Elshafey-BIS'>"
    f"<svg width='28' height='28' viewBox='0 0 16 16'><path d='{GITHUB_MARK}'/></svg>"
    f"<img src='{GITHUB_URL}.png?size=120' alt=''>"
    f"<span class='badge'><svg width='12' height='12' viewBox='0 0 16 16'><path d='{GITHUB_MARK}'/></svg></span></a>"
)


def go_to(name):
    st.session_state['page'] = name


def toggle_lang():
    st.session_state['lang'] = 'ar' if st.session_state['lang'] == 'en' else 'en'


def main():
    st.session_state.setdefault('page', 'dash')
    ok, _ = get_available_models()
    st.sidebar.button("🌐  " + t('lang_btn'), key="lang_toggle", on_click=toggle_lang)
    st.sidebar.markdown(f"<div class='brand'>🏭 Turbine<span>Watch</span></div>"
                        f"<div class='brand-sub'>{t('brand_sub')}</div>", unsafe_allow_html=True)
    for pid, (icon, _) in PAGES.items():
        st.sidebar.button(f"{icon}  {t('nav_' + pid)}", key=f"nav_{pid}", on_click=go_to, args=(pid,),
                          type="primary" if st.session_state['page'] == pid else "secondary")
    st.sidebar.markdown("---")
    st.sidebar.caption("UI build 2.9")
    st.sidebar.caption(f"{t('active_models')}: {', '.join(ok) if ok else '-'}")
    st.markdown(GITHUB_LOGO, unsafe_allow_html=True)
    if not ok:
        st.error(t('no_model'))
        return
    PAGES[st.session_state['page']][1]()


if __name__ == "__main__":
    main()
