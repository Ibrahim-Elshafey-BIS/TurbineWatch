import copy
import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px
from prediction import predict_batch, predict_target, get_emission_status
from config import (ORIGINAL_FEATURES, FEATURE_LABELS, OFFLINE_METRICS,
                    REFERENCE_THRESHOLDS, SENSOR_RANGES)
from model_loader import load_model, get_available_models
from feature_importance import get_feature_importance
from report_generator import generate_pdf_report
from theme import page_head, pill, kpi
from i18n import t, pt, lang

TARGETS = {'CO': 'CO', 'NOX': 'NOx'}
UNITS = {'AT': '°C', 'AP': 'mbar', 'AH': '%', 'AFDP': 'mbar', 'GTEP': 'mbar',
         'TIT': '°C', 'TAT': '°C', 'TEY': 'MWh', 'CDP': 'mbar'}
PLOT = dict(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#E7EFF3', family='IBM Plex Sans'))


def models():
    return get_available_models()[0]


def default_model(names):
    return "Random Forest" if "Random Forest" in names else names[0]


def init_session_state():
    st.session_state.setdefault('prediction_result', None)
    st.session_state.setdefault('history', [])
    st.session_state.setdefault('thresholds', copy.deepcopy(REFERENCE_THRESHOLDS))


def get_thresholds():
    return st.session_state['thresholds']


def P(status):
    return pill(status, {'Red': t('red'), 'Yellow': t('yellow'), 'Green': t('green')})


def flabel(f):
    parts = FEATURE_LABELS[f].split(' | ')
    return parts[0] if lang() == 'en' else f"{f} ({parts[-1]})"


def sensor_inputs(prefix, use_slider=False):
    groups = [(t('g_amb'), ['AT', 'AP', 'AH']), (t('g_ops'), ['AFDP', 'GTEP', 'TIT']),
              (t('g_out'), ['TAT', 'TEY', 'CDP'])]
    values = {}
    for col, (title, feats) in zip(st.columns(3), groups):
        with col:
            st.markdown(f"**{title}**")
            for f in feats:
                lo, hi, d = SENSOR_RANGES[f]
                step = 1.0 if (hi - lo) >= 50 else 0.1
                key = f"{prefix}_{f}"
                if use_slider:
                    values[f] = st.slider(flabel(f), lo, hi, float(d), step=step, key=key)
                    continue
                values[f] = st.number_input(flabel(f), value=float(d), step=step, format="%.2f", key=key)
                if not lo <= values[f] <= hi:
                    st.caption(":orange[" + t('out_range', lo=f"{lo:g}", hi=f"{hi:g}") + "]")
    return values


def gauge(value, title, target):
    th = get_thresholds()[target]
    top = max(th['red'] * 1.6, value * 1.1)
    fig = go.Figure(go.Indicator(
        mode="gauge+number", value=value, number=dict(suffix=" mg/m³", valueformat=".2f"),
        title=dict(text=title, font=dict(size=16)),
        gauge=dict(axis=dict(range=[0, top]), bar=dict(color="#E7EFF3", thickness=.25),
                   bgcolor="rgba(0,0,0,0)", borderwidth=0,
                   steps=[dict(range=[0, th['yellow']], color="#1F7A54"),
                          dict(range=[th['yellow'], th['red']], color="#B9772F"),
                          dict(range=[th['red'], top], color="#E5484D")])
    ))
    fig.update_layout(height=270, margin=dict(l=20, r=20, t=50, b=10), **PLOT)
    return fig


def render_dashboard():
    page_head(t('dash_title'), t('dash_sub'))
    names, th = models(), get_thresholds()
    with st.container(border=True):
        inputs = sensor_inputs("dash", use_slider=True)
    c1, c2 = st.columns(2)
    di = names.index(default_model(names))
    co_model = c1.selectbox(t('co_model'), names, index=di, key="dash_co_m")
    nox_model = c2.selectbox(t('nox_model'), names, index=di, key="dash_nox_m")
    try:
        co = predict_target(inputs, 'CO', co_model)
        nox = predict_target(inputs, 'NOX', nox_model)
    except Exception as e:
        st.error(f"{t('pred_fail')}: {e}")
        return
    co_s, nox_s = get_emission_status(co, 'CO', th), get_emission_status(nox, 'NOX', th)
    st.session_state['prediction_result'] = dict(co=co, nox=nox, co_model=co_model, nox_model=nox_model,
                                                 co_status=co_s, nox_status=nox_s, input_data=inputs)
    k = st.columns(4)
    k[0].markdown(kpi("CO", f"{co:.2f}", P(co_s)), unsafe_allow_html=True)
    k[1].markdown(kpi("NOx", f"{nox:.2f}", P(nox_s)), unsafe_allow_html=True)
    k[2].markdown(kpi(t('co_model'), co_model, f"{t('cv_rmse')} {OFFLINE_METRICS['CO'][co_model]['CV RMSE']}"),
                  unsafe_allow_html=True)
    k[3].markdown(kpi(t('nox_model'), nox_model, f"{t('cv_rmse')} {OFFLINE_METRICS['NOX'][nox_model]['CV RMSE']}"),
                  unsafe_allow_html=True)
    st.write("")
    g1, g2 = st.columns(2)
    g1.plotly_chart(gauge(co, "CO", 'CO'), use_container_width=True)
    g2.plotly_chart(gauge(nox, "NoX", 'NOX'), use_container_width=True)

    st.markdown(f"### {t('per_model')}")
    rows = [dict(Model=m, CO=predict_target(inputs, 'CO', m), NOx=predict_target(inputs, 'NOX', m)) for m in names]
    df = pd.DataFrame(rows).melt('Model', var_name='Gas', value_name='mg/m³')
    fig = px.bar(df, x='Model', y='mg/m³', color='Gas', barmode='group',
                 color_discrete_map={'CO': '#2EC4B6', 'NOx': '#F4A259'})
    fig.update_layout(height=320, margin=dict(t=10), **PLOT)
    st.plotly_chart(fig, use_container_width=True)

    if st.button(t('save_hist')):
        st.session_state['history'].append({'Time': datetime.now().strftime('%H:%M:%S'),
                                            'CO': round(co, 3), 'NOx': round(nox, 3),
                                            **{f: round(v, 2) for f, v in inputs.items()}})
    hist = st.session_state['history']
    if hist:
        h = pd.DataFrame(hist)
        st.markdown(f"### {t('saved')}")
        fig = go.Figure()
        fig.add_scatter(y=h['CO'], name='CO', mode='lines+markers', line=dict(color='#2EC4B6'))
        fig.add_scatter(y=h['NOx'], name='NOx', mode='lines+markers', line=dict(color='#F4A259'), yaxis='y2')
        fig.update_layout(height=280, margin=dict(t=10), yaxis=dict(title='CO'),
                          yaxis2=dict(title='NOx', overlaying='y', side='right'), **PLOT)
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(h, use_container_width=True)
        if st.button(t('clear')):
            st.session_state['history'] = []
            st.rerun()


def pdf_download(pred, summary):
    """The PDF is built only when the user clicks download, never after Predict."""
    fname = f"emission_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    build = lambda: generate_pdf_report(pred['input_data'], summary, get_thresholds()).getvalue()
    try:
        st.download_button(t('dl_pdf'), data=build, file_name=fname, mime="application/pdf")
    except Exception:
        if st.button(t('gen_pdf')):
            st.session_state['pdf_ready'] = build()
        if st.session_state.get('pdf_ready'):
            st.download_button(t('dl_pdf'), data=st.session_state['pdf_ready'], file_name=fname, mime="application/pdf")


def render_single_prediction():
    page_head(t('single_title'), t('single_sub'))
    names, th = models(), get_thresholds()
    with st.form("prediction_form"):
        inputs = sensor_inputs("single")
        c1, c2 = st.columns(2)
        di = names.index(default_model(names))
        co_model = c1.selectbox(t('co_model'), names, index=di)
        nox_model = c2.selectbox(t('nox_model'), names, index=di)
        submit = st.form_submit_button(t('predict'), type="primary")
    if submit:
        st.session_state.pop('pdf_ready', None)
        try:
            co = predict_target(inputs, 'CO', co_model)
            nox = predict_target(inputs, 'NOX', nox_model)
            st.session_state['single_result'] = dict(
                co=co, nox=nox, co_model=co_model, nox_model=nox_model, input_data=inputs,
                co_status=get_emission_status(co, 'CO', th), nox_status=get_emission_status(nox, 'NOX', th))
        except Exception as e:
            st.error(f"{t('pred_fail')}: {e}")
    pred = st.session_state.get('single_result')
    if pred:
        k = st.columns(2)
        k[0].markdown(kpi(f"CO ({pred['co_model']})", f"{pred['co']:.3f} mg/m³", P(pred['co_status'])), unsafe_allow_html=True)
        k[1].markdown(kpi(f"NOx ({pred['nox_model']})", f"{pred['nox']:.3f} mg/m³", P(pred['nox_status'])), unsafe_allow_html=True)
        st.write("")
        summary = [{'Target': 'CO', 'Model': pred['co_model'], 'Value': pred['co'], 'Status': pred['co_status']},
                   {'Target': 'NOx', 'Model': pred['nox_model'], 'Value': pred['nox'], 'Status': pred['nox_status']}]
        pdf_download(pred, summary)


def render_batch_prediction():
    page_head(t('batch_title'), f"{t('batch_sub')}: {', '.join(ORIGINAL_FEATURES)}")
    names = models()
    c1, c2 = st.columns(2)
    co_sel = c1.multiselect(t('co_models'), names, default=[default_model(names)])
    nox_sel = c2.multiselect(t('nox_models'), names, default=[default_model(names)])
    file = st.file_uploader(t('csv_file'), type=['csv'])
    if file is None:
        return
    try:
        df = pd.read_csv(file)
        st.dataframe(df.head(), use_container_width=True)
        missing = [c for c in ORIGINAL_FEATURES if c not in df.columns]
        if missing:
            st.error(f"{t('missing_cols')}: {missing}")
        elif not (co_sel or nox_sel):
            st.warning(t('pick_model'))
        elif st.button(t('run_batch'), type="primary"):
            with st.spinner(t('predicting')):
                res = predict_batch(df, co_sel, nox_sel, get_thresholds())
            st.success(t('predicted_rows', n=len(res)))
            st.dataframe(res.head(20), use_container_width=True)
            st.download_button(t('dl_csv'), res.to_csv(index=False).encode('utf-8'),
                               file_name=f"batch_predictions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv", mime="text/csv")
    except Exception as e:
        st.error(f"{t('file_err')}: {e}")


def render_model_comparison():
    page_head(t('cmp_title'), t('cmp_sub'))
    names = models()
    with st.container(border=True):
        inputs = sensor_inputs("comp")
    for key, label in TARGETS.items():
        st.markdown(f"### {label}")
        rows = []
        for m in names:
            mt = OFFLINE_METRICS[key][m]
            rows.append({'Model': m, f'Predicted {label}': predict_target(inputs, key, m),
                         'CV RMSE': mt['CV RMSE'], 'Test RMSE': mt['Test RMSE'], 'Test R²': mt['Test R²']})
        df = pd.DataFrame(rows)
        c1, c2 = st.columns([3, 2])
        c1.dataframe(df, use_container_width=True, hide_index=True)
        fig = px.bar(df, x='Model', y=f'Predicted {label}', color='Model', error_y='Test RMSE',
                     color_discrete_sequence=['#2EC4B6', '#F4A259', '#7C9CF5', '#E5484D'])
        fig.update_yaxes(title=f'Predicted {label} (mg/m³)')
        fig.update_layout(height=300, showlegend=False, margin=dict(t=10), **PLOT)
        c2.plotly_chart(fig, use_container_width=True)
        c2.caption(t('cmp_cap'))


def render_feature_importance():
    page_head(t('imp_title'), t('imp_sub'))
    names = models()
    c1, c2 = st.columns(2)
    target = c1.radio(t('target'), ["CO", "NOx"], horizontal=True)
    name = c2.selectbox(t('model'), names)
    if st.button(t('calc_imp'), type="primary"):
        try:
            imp = get_feature_importance(load_model(target.upper(), name), name, target.upper())
            if imp is None:
                st.warning(t('imp_none'))
                return
            typ = imp['Type'].iloc[0]
            fig = px.bar(imp, x='Importance', y='Feature', orientation='h', title=f"{typ}: {name}",
                         color='Importance', color_continuous_scale='Teal')
            fig.update_layout(yaxis={'categoryorder': 'total ascending'}, height=460, **PLOT)
            st.plotly_chart(fig, use_container_width=True)
            with st.expander(t('view_data')):
                st.dataframe(imp, use_container_width=True)
        except Exception as e:
            st.error(f"{t('imp_err')}: {e}")


def render_settings():
    page_head(t('set_title'), t('set_sub'))
    cur = st.session_state['thresholds']
    new, valid = copy.deepcopy(cur), True
    for key, label in TARGETS.items():
        st.markdown(f"### {label}")
        c1, c2 = st.columns(2)
        step = 0.1 if key == 'CO' else 1.0
        y = c1.number_input(f"{label}: {t('yellow_from')}", min_value=0.0, value=float(cur[key]['yellow']), step=step)
        r = c2.number_input(f"{label}: {t('red_from')}", min_value=0.0, value=float(cur[key]['red']), step=step)
        if y < r:
            new[key] = {'yellow': y, 'red': r}
        else:
            valid = False
    if not valid:
        st.error(t('th_invalid'))
    st.session_state['thresholds'] = new
    if st.button(t('reset')):
        st.session_state['thresholds'] = copy.deepcopy(REFERENCE_THRESHOLDS)
        st.rerun()
    st.caption(t('th_note'))


STEPS = [
    ("🎛️", ("Enter readings", "أدخل القراءات"), ("Provide the 9 sensor values.", "قدّم قيم الحساسات التسعة.")),
    ("🧮", ("Engineer features", "احسب الميزات"), ("4 extra features are calculated automatically.", "تُحسب 4 ميزات إضافية تلقائياً.")),
    ("🩹", ("Fill gaps", "املأ الفراغات"), ("Missing values use default medians.", "القيم الناقصة تُملأ بالوسيط الافتراضي.")),
    ("🤖", ("Predict", "تنبأ"), ("The pipeline scales once, then the model predicts CO and NOx.", "يوحّد الخط المقياس مرة واحدة ثم يتنبأ الموديل بـ CO وNOx.")),
    ("🚦", ("Classify", "صنّف"), ("Compared with thresholds: Green, Yellow or Red.", "تُقارن بالعتبات: أخضر أو أصفر أو أحمر.")),
]
LIMITS = [
    ("🏭", ("Trained on one turbine", "دُرّب على توربين واحد"),
     ("The models may not transfer to another turbine or site.", "قد لا تنطبق الموديلات على توربين أو موقع آخر.")),
    ("📏", ("Inputs outside the training range", "مدخلات خارج مدى التدريب"),
     ("Values far from the typical range give unreliable results. The app warns you when this happens.", "القيم البعيدة عن المدى المعتاد تعطي نتائج غير موثوقة، ويحذرك التطبيق عند حدوث ذلك.")),
    ("🎯", ("Predictions have error", "التنبؤات فيها خطأ"),
     ("See the RMSE values in the Models tab. They do not replace a calibrated emissions analyser.", "انظر قيم RMSE في تبويب الموديلات. لا تغني عن جهاز قياس انبعاثات معاير.")),
    ("🌳", ("Tree models cannot extrapolate", "الموديلات الشجرية لا تستقرئ"),
     ("They cannot predict beyond values seen in training.", "لا تتنبأ بقيم خارج ما رأته في التدريب.")),
    ("👩‍🔧", ("Verify important decisions", "تحقق من القرارات المهمة"),
     ("Ask a domain expert before acting on a prediction.", "استشر مختصاً قبل الاعتماد على أي تنبؤ.")),
]


def _pick(pair):
    return pair[1 if lang() == 'ar' else 0]


def metric_chart(key, metric, names):
    vals = [OFFLINE_METRICS[key][m][metric] for m in names]
    best = max(vals) if metric == 'Test R²' else min(vals)
    fig = go.Figure(go.Bar(x=names, y=vals, text=[f"{v:.3f}" for v in vals], textposition='outside',
                           marker_color=['#2EC4B6' if v == best else '#3A5568' for v in vals]))
    fig.update_layout(height=300, margin=dict(t=30, b=10), yaxis=dict(range=[0, max(vals) * 1.2]), **PLOT)
    return fig


def _set_about_tab(i):
    st.session_state['about_tab'] = i


def about_nav(labels):
    """Button-based sub-navigation (more reliable to style than st.tabs)."""
    cur = st.session_state.setdefault('about_tab', 0)
    cols = st.columns(len(labels))
    cols[0].markdown("", unsafe_allow_html=True)
    for i, (col, label) in enumerate(zip(cols, labels)):
        col.button(label, key=f"about_tab_{i}", on_click=_set_about_tab, args=(i,),
                   type="primary" if i == cur else "secondary", use_container_width=True)
    st.write("")
    return cur


def render_about():
    page_head(t('about_title'), t('about_sub'))
    ok, _ = get_available_models()
    idx = about_nav(t('tabs'))
    ar = lang() == 'ar'

    if idx == 0:
        st.markdown("### " + pt('overview').split('\n### ')[1])
        st.markdown(f"### {'كيف يتم التنبؤ' if ar else 'How a prediction is made'}")
        cards = "".join(f"