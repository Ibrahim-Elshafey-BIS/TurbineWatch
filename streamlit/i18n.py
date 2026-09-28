import streamlit as st

TR = {
 'nav_dash': ("Dashboard", "لوحة المتابعة"), 'nav_single': ("Single Prediction", "تنبؤ فردي"),
 'nav_compare': ("Model Comparison", "مقارنة الموديلات"), 'nav_impact': ("Feature Impact", "تأثير المتغيرات"),
 'nav_batch': ("Batch Prediction", "تنبؤ دفعي"), 'nav_settings': ("Settings", "الإعدادات"), 'nav_about': ("About", "حول النظام"),
 'brand_sub': ("CO and NOx emissions monitor", "مراقبة انبعاثات CO وNOx"),
 'active_models': ("Active models", "الموديلات الفعّالة"), 'lang_btn': ("العربية", "English"),
 'no_model': ("No model could be loaded. Check the Models folder and requirements.", "تعذر تحميل أي موديل. تحقق من مجلد Models وملف المتطلبات."),
 'green': ("Green", "أخضر"), 'yellow': ("Yellow", "أصفر"), 'red': ("Red", "أحمر"),
 'g_amb': ("Ambient conditions", "الظروف المحيطة"), 'g_ops': ("Turbine operation", "تشغيل التوربين"), 'g_out': ("Turbine output", "مخرجات التوربين"),
 'co_model': ("CO model", "موديل CO"), 'nox_model': ("NOx model", "موديل NOx"),
 'out_range': ("Outside typical range ({lo} to {hi}). Prediction may be less reliable.", "خارج المدى المعتاد ({lo} إلى {hi}). قد تكون النتيجة أقل موثوقية."),
 'dash_title': ("Emissions dashboard", "لوحة متابعة الانبعاثات"), 'dash_sub': ("Move any slider and the predictions update instantly.", "حرّك أي شريط وستتحدث التنبؤات فوراً."),
 'pred_fail': ("Prediction failed", "فشل التنبؤ"), 'cv_rmse': ("Cross-validated RMSE", "خطأ RMSE بالتحقق المتقاطع"),
 'per_model': ("What each model predicts for these inputs", "تنبؤ كل موديل لهذه المدخلات"),
 'save_hist': ("Save to history", "حفظ في السجل"), 'saved': ("Saved predictions", "التنبؤات المحفوظة"), 'clear': ("Clear history", "مسح السجل"),
 'single_title': ("Single prediction", "تنبؤ فردي"), 'single_sub': ("Enter readings, choose models and export a PDF report.", "أدخل القراءات واختر الموديلات ثم صدّر تقرير PDF."),
 'predict': ("Predict", "تنبأ"), 'dl_pdf': ("Download PDF report", "تنزيل تقرير PDF"), 'gen_pdf': ("Generate PDF report", "إنشاء تقرير PDF"),
 'batch_title': ("Batch prediction", "تنبؤ دفعي"), 'batch_sub': ("Upload a CSV with these columns", "ارفع ملف CSV بهذه الأعمدة"),
 'co_models': ("CO models", "موديلات CO"), 'nox_models': ("NOx models", "موديلات NOx"), 'csv_file': ("CSV file", "ملف CSV"),
 'missing_cols': ("Missing columns", "أعمدة ناقصة"), 'pick_model': ("Select at least one model.", "اختر موديلاً واحداً على الأقل."),
 'run_batch': ("Run batch prediction", "تشغيل التنبؤ الدفعي"), 'predicting': ("Predicting...", "جارٍ التنبؤ..."),
 'predicted_rows': ("Predicted {n} rows.", "تم التنبؤ لعدد {n} صف."), 'dl_csv': ("Download predictions (CSV)", "تنزيل التنبؤات (CSV)"),
 'file_err': ("Could not process the file", "تعذرت معالجة الملف"),
 'cmp_title': ("Model comparison", "مقارنة الموديلات"), 'cmp_sub': ("Live predictions next to each model's offline test metrics.", "تنبؤات مباشرة بجانب مقاييس اختبار كل موديل."),
 'cmp_cap': ("Bars show the prediction. Whiskers show each model's typical test error (RMSE).", "الأعمدة تمثل التنبؤ، والخطوط تمثل الخطأ المعتاد للموديل (RMSE)."),
 'imp_title': ("Feature impact", "تأثير المتغيرات"), 'imp_sub': ("Global importance: which inputs matter most overall, not why one prediction changed.", "أهمية عامة: أي المدخلات أهم بشكل عام، وليس سبب تغير تنبؤ بعينه."),
 'target': ("Target", "المتغير المستهدف"), 'model': ("Model", "الموديل"), 'calc_imp': ("Calculate importance", "احسب الأهمية"),
 'imp_none': ("Importance could not be calculated. Neural networks need the dataset file (gt_full.csv).", "تعذر حساب الأهمية. الشبكات العصبية تحتاج ملف البيانات (gt_full.csv)."),
 'view_data': ("View data", "عرض البيانات"), 'imp_err': ("Could not calculate importance", "تعذر حساب الأهمية"),
 'set_title': ("Settings", "الإعدادات"), 'set_sub': ("Set the Yellow and Red reference thresholds for your site.", "حدد العتبات المرجعية الصفراء والحمراء لموقعك."),
 'yellow_from': ("Yellow from (mg/m³)", "أصفر من (mg/m³)"), 'red_from': ("Red from (mg/m³)", "أحمر من (mg/m³)"),
 'th_invalid': ("Yellow must be lower than Red. The previous valid values are still in use.", "يجب أن يكون الأصفر أقل من الأحمر. ما زالت القيم الصحيحة السابقة مستخدمة."),
 'th_note': ("Thresholds apply to every page and to PDF reports until you close the browser tab. They are references, not legal limits.", "تنطبق العتبات على كل الصفحات وتقارير PDF حتى تغلق تبويب المتصفح. هي مرجعية وليست حدوداً قانونية."),
 'reset': ("Reset to defaults", "استعادة الافتراضي"),
 'about_title': ("About", "حول النظام"), 'about_sub': ("How this system works, what it can and cannot tell you.", "كيف يعمل النظام، وما الذي يمكنه وما لا يمكنه إخباره لك."),
 'tabs': (["Overview", "Inputs and features", "Models", "Reading the results", "Limitations"], ["نظرة عامة", "المدخلات والميزات", "الموديلات", "قراءة النتائج", "حدود النظام"]),
 'col_page': ("Page", "الصفحة"), 'col_purpose': ("Purpose", "الغرض"), 'col_code': ("Code", "الرمز"), 'col_meaning': ("Meaning", "المعنى"),
 'col_unit': ("Unit", "الوحدة"), 'col_range': ("Typical range", "المدى المعتاد"), 'col_feat': ("Feature", "الميزة"), 'col_formula': ("Formula", "المعادلة"),
 'pages_h': ("Pages", "الصفحات"), 'sensor_h': ("Sensor inputs", "مدخلات الحساسات"), 'eng_h': ("Engineered features (calculated automatically)", "ميزات محسوبة تلقائياً"),
 'units_note': ("Units are the usual ones for this type of dataset. Check them against your own data source.", "الوحدات هي المعتادة لهذا النوع من البيانات. تحقق منها من مصدر بياناتك."),
 'eval_h': ("offline evaluation", "التقييم المسبق"), 'status_h': ("Status levels (current settings)", "مستويات الحالة (الإعدادات الحالية)"),
}

PAGE_TEXT = {
 'overview': ("""
### What it does
TurbineWatch estimates two exhaust emissions of a gas turbine, **Carbon Monoxide (CO)** and **Nitrogen Oxides (NOx)**, from sensor readings, in mg/m³.

### How a prediction is made
1. You enter the 9 sensor readings.
2. Four engineered features are calculated automatically.
3. Any missing value is filled with a default median.
4. The trained pipeline scales the features once and the selected model predicts CO and NOx.
5. The result is compared with the reference thresholds and shown as Green, Yellow or Red.
""", """
### ماذا يفعل النظام
يقدّر TurbineWatch انبعاثين من عادم التوربين الغازي هما **أول أكسيد الكربون (CO)** و**أكاسيد النيتروجين (NOx)** بوحدة mg/m³، اعتماداً على قراءات الحساسات.

### كيف يتم التنبؤ
1. تُدخل قراءات الحساسات التسعة.
2. تُحسب أربع ميزات هندسية تلقائياً.
3. تُملأ أي قيمة ناقصة بالوسيط الافتراضي.
4. يقوم خط المعالجة المدرَّب بتوحيد المقياس مرة واحدة ثم يتنبأ الموديل المختار بـ CO وNOx.
5. تُقارن النتيجة بالعتبات المرجعية وتظهر أخضر أو أصفر أو أحمر.
"""),
 'metrics': ("""
- **CV RMSE**: average error across cross-validation folds. **Test RMSE**: error on held-out data. Lower is better, in mg/m³.
- **Test R²**: share of variation explained. 1.0 is perfect.
- These come from the original training run and are not recalculated here.
""", """
- **CV RMSE**: متوسط الخطأ عبر طيات التحقق المتقاطع. **Test RMSE**: الخطأ على بيانات الاختبار. الأقل أفضل، بوحدة mg/m³.
- **Test R²**: نسبة التباين التي يفسرها الموديل. القيمة 1.0 مثالية.
- هذه الأرقام من عملية التدريب الأصلية ولا يعاد حسابها هنا.
"""),
 'reading': ("""
- 🟢 **Green**: below the yellow threshold. 🟡 **Yellow**: warning. 🔴 **Red**: high.
- Thresholds are project-defined references, **not** official legal limits. Change them in Settings.
- **Gauges** show the value against the three zones.
- **Whiskers** on comparison bars show typical test error. If whiskers of two models overlap, their difference is not meaningful.
- **Feature importance** is global, not an explanation of one prediction.
""", """
- 🟢 **أخضر**: أقل من العتبة الصفراء. 🟡 **أصفر**: تحذير. 🔴 **أحمر**: مرتفع.
- العتبات مرجعية حددها المشروع وهي **ليست** حدوداً قانونية رسمية. يمكن تغييرها من الإعدادات.
- **العدادات** تعرض القيمة مقابل المناطق الثلاث.
- **الخطوط فوق الأعمدة** في المقارنة تمثل الخطأ المعتاد. إذا تداخلت خطوط موديلين فالفرق بينهما غير مهم.
- **أهمية المتغيرات** عامة وليست تفسيراً لتنبؤ واحد.
"""),
 'limits': ("""
- The models learned from one turbine's data and may not transfer to another turbine or site.
- Inputs far outside the training range give unreliable results.
- Predictions have error (see RMSE) and do not replace a calibrated emissions analyser.
- Tree-based models cannot predict beyond values seen in training.
- Verify important decisions with a domain expert.
""", """
- تعلمت الموديلات من بيانات توربين واحد وقد لا تنطبق على توربين أو موقع آخر.
- المدخلات البعيدة عن مدى التدريب تعطي نتائج غير موثوقة.
- التنبؤات فيها خطأ (انظر RMSE) ولا تغني عن جهاز قياس انبعاثات معاير.
- الموديلات الشجرية لا تتنبأ بقيم خارج ما رأته في التدريب.
- تحقق من القرارات المهمة مع مختص.
"""),
 'pages': ([("Dashboard", "Live predictions with sliders, gauges and model comparison."), ("Single Prediction", "One reading and a PDF report."),
            ("Model Comparison", "Predictions next to offline metrics."), ("Feature Impact", "Which inputs matter most."),
            ("Batch Prediction", "Predict every row of a CSV."), ("Settings", "Yellow and Red reference thresholds for your site.")],
           [("لوحة المتابعة", "تنبؤات مباشرة مع أشرطة وعدادات ومقارنة الموديلات."), ("تنبؤ فردي", "قراءة واحدة وتقرير PDF."),
            ("مقارنة الموديلات", "التنبؤات بجانب المقاييس المسبقة."), ("تأثير المتغيرات", "أي المدخلات أهم."),
            ("تنبؤ دفعي", "تنبؤ لكل صف في ملف CSV."), ("الإعدادات", "عتبات مخصصة لموقعك.")]),
}


def lang():
    return st.session_state.get('lang', 'en')


def t(key, **kw):
    v = TR[key][1 if lang() == 'ar' else 0]
    return v.format(**kw) if kw and isinstance(v, str) else v


def pt(key):
    return PAGE_TEXT[key][1 if lang() == 'ar' else 0]
