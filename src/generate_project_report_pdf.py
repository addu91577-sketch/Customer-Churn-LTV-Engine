"""
Script to generate the publication-grade Project_Report.pdf
for Customer Churn & LTV Engine submission and LinkedIn Carousel.
"""

import os
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas


class NumberedCanvas(canvas.Canvas):
    """Adds running headers and footers with exact page numbers."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 9)
        self.setFillColor(colors.HexColor("#64748b"))

        # Running Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(54, 575, "Customer Churn & Lifetime Value (LTV) Engine | Executive Project Report")
            self.setStrokeColor(colors.HexColor("#e2e8f0"))
            self.setLineWidth(0.75)
            self.line(54, 568, 738, 568)

        # Running Footer
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(738, 28, page_str)
        self.drawString(54, 28, "GitHub: https://github.com/addu91577-sketch/Customer-Churn-LTV-Engine")
        self.setStrokeColor(colors.HexColor("#e2e8f0"))
        self.setLineWidth(0.75)
        self.line(54, 40, 738, 40)
        self.restoreState()


def build_pdf(filename="Project_Report.pdf"):
    # 792 x 612 pt landscape letter
    doc = SimpleDocTemplate(
        filename,
        pagesize=landscape(letter),
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=50
    )

    styles = getSampleStyleSheet()

    # Custom styles
    primary_color = colors.HexColor("#1e3a8a")
    secondary_color = colors.HexColor("#0284c7")
    accent_dark = colors.HexColor("#0f172a")
    text_color = colors.HexColor("#334155")

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=primary_color,
        spaceAfter=6
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=secondary_color,
        spaceAfter=14
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=primary_color,
        spaceAfter=10
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=secondary_color,
        spaceAfter=6
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=text_color,
        spaceAfter=8
    )

    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        parent=body_style,
        leftIndent=14,
        firstLineIndent=-10,
        spaceAfter=5
    )

    story = []

    # ==========================================
    # SLIDE 1: COVER & EXECUTIVE SUMMARY
    # ==========================================
    story.append(Paragraph("📊 Customer Churn & Lifetime Value (LTV) Engine", title_style))
    story.append(Paragraph("Production Machine Learning, LTV Forecasting, FastAPI Microservice & Executive BI Suite", subtitle_style))

    # Meta card table
    meta_data = [
        [
            Paragraph("<b>Author:</b> Adarsh Kumar Pandey", body_style),
            Paragraph("<b>Dataset:</b> IBM Watson Telco Cohort (7,043 Records)", body_style),
        ],
        [
            Paragraph("<b>GitHub:</b> <font color='#0284c7'>https://github.com/addu91577-sketch/Customer-Churn-LTV-Engine</font>", body_style),
            Paragraph("<b>Stack:</b> Python, FastAPI, XGBoost, Docker, PostgreSQL, Power BI", body_style)
        ]
    ]
    t_meta = Table(meta_data, colWidths=[340, 340])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#f8fafc")),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#cbd5e1")),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 14))

    # Executive Overview
    story.append(Paragraph("Executive Overview & High-Impact KPIs", h2_style))
    story.append(Paragraph(
        "Customer attrition in telecommunications incurs up to <b>5x higher replacement costs</b> than proactive subscriber retention. "
        "This project presents an enterprise-grade analytics engineering and predictive intelligence lifecycle that ingests raw telemetry into "
        "a PostgreSQL data warehouse via SQLAlchemy, executes granular exploratory data analysis (EDA), benchmarks ensemble classification "
        "models (XGBoost, Random Forest, Logistic Regression), unpacks feature importance via game-theoretic SHAP explainability, forecasts active "
        "subscriber Lifetime Value ($R^2 = 0.9983$), and deploys real-time FastAPI endpoints containerized in Docker alongside multi-tier Power BI and Metabase executive dashboards.",
        body_style
    ))
    story.append(Spacer(1, 10))

    # KPI Summary Cards Table
    kpi_data = [
        [
            Paragraph("<font color='#1e3a8a'><b>Total Base</b></font><br/><font size=14><b>7,043</b></font><br/>Audited Cohort", body_style),
            Paragraph("<font color='#0284c7'><b>Churn Rate</b></font><br/><font size=14><b>26.54%</b></font><br/>1,869 Lost Users", body_style),
            Paragraph("<font color='#dc2626'><b>Lost MRR</b></font><br/><font size=14><b>$139.13K</b></font><br/>Monthly Revenue Drag", body_style),
            Paragraph("<font color='#ea580c'><b>Annual Risk</b></font><br/><font size=14><b>$2.45M</b></font><br/>ML Risk Exposure", body_style),
            Paragraph("<font color='#16a34a'><b>Avg LTV</b></font><br/><font size=14><b>$3,310</b></font><br/>Subscriber Pool", body_style),
            Paragraph("<font color='#7c3aed'><b>LTV Model R²</b></font><br/><font size=14><b>0.9983</b></font><br/>Predictive Accuracy", body_style),
        ]
    ]
    t_kpi = Table(kpi_data, colWidths=[113]*6)
    t_kpi.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#f1f5f9")),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#cbd5e1")),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(t_kpi)

    story.append(PageBreak())

    # ==========================================
    # SLIDE 2: DATA INGESTION & STORAGE (SQL + POSTGRESQL)
    # ==========================================
    story.append(Paragraph("1. Data Ingestion & Storage: PostgreSQL & SQLAlchemy Engine", h1_style))
    story.append(Paragraph(
        "A robust relational foundation was engineered to transform raw CSV flat files into an enterprise-grade schema within PostgreSQL, "
        "enabling structured relational queries, ACID guarantees, and direct downstream BI dashboard connectivity.",
        body_style
    ))
    story.append(Spacer(1, 6))

    ingest_col1 = [
        Paragraph("<b>Key Implementation Highlights:</b>", h2_style),
        Paragraph("• <b>Automated SQLAlchemy Pipeline (<code>src/db_ingestion.py</code>):</b> Handles connection pooling, pre-ingestion data hygiene, table recreation, and batch insertion with transaction commit/rollback controls.", bullet_style),
        Paragraph("• <b>Data Hygiene & Cleansing:</b> Resolved 11 whitespace-string nulls in <code>TotalCharges</code> for brand new 0-tenure accounts, casting columns into native float/integer structures with zero data loss.", bullet_style),
        Paragraph("• <b>Production SQL Views (<code>sql/04_churn_and_ltv_views.sql</code>):</b> Built 5 dedicated analytical views for Power BI & Metabase to track executive KPIs, contract risk cohorts, service bundle vulnerabilities, and LTV distribution.", bullet_style),
        Paragraph("• <b>Relational Data Integrity:</b> Ensured 100% uniqueness across <code>customerID</code>, verified primary key constraints, and established indexing across high-frequency query dimensions (tenure, contract, payment method).", bullet_style),
    ]

    ingest_col2 = [
        Paragraph("<b>SQL Schema Architecture:</b>", h2_style),
        Paragraph("• <b>Database:</b> <code>telco_churn_db</code><br/>• <b>Primary Table:</b> <code>customers</code> (7,043 rows x 21 attributes)", body_style),
        Paragraph("• <b>Analytical Views:</b>", body_style),
        Paragraph("&nbsp;&nbsp;1. <code>vw_executive_kpis</code> — MRR, Base, Global Attrition", bullet_style),
        Paragraph("&nbsp;&nbsp;2. <code>vw_contract_risk</code> — Month-to-Month vs 1-2 Year", bullet_style),
        Paragraph("&nbsp;&nbsp;3. <code>vw_service_adoption</code> — Fiber vs DSL, Security bundles", bullet_style),
        Paragraph("&nbsp;&nbsp;4. <code>vw_financial_exposure</code> — Revenue At Risk cohorts", bullet_style),
        Paragraph("&nbsp;&nbsp;5. <code>vw_ltv_segmentation</code> — High-value retention tiers", bullet_style),
    ]

    t_ingest = Table([[ingest_col1, ingest_col2]], colWidths=[420, 260])
    t_ingest.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BACKGROUND', (1, 0), (1, 0), colors.HexColor("#f8fafc")),
        ('BOX', (1, 0), (1, 0), 1, colors.HexColor("#cbd5e1")),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (1, 0), (1, 0), 10),
        ('RIGHTPADDING', (1, 0), (1, 0), 10),
    ]))
    story.append(t_ingest)
    story.append(Spacer(1, 10))

    # Architecture banner
    arch_box = [
        [Paragraph("<b>Pipeline Flow:</b> Raw IBM Telco Dataset &rarr; Automated Data Cleansing &rarr; PostgreSQL Warehouse (SQLAlchemy) &rarr; Analytical SQL Views &rarr; Power BI & Metabase Dashboards", body_style)]
    ]
    t_arch = Table(arch_box, colWidths=[684])
    t_arch.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#eff6ff")),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#93c5fd")),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
    ]))
    story.append(t_arch)

    story.append(PageBreak())

    # ==========================================
    # SLIDE 3: EXPLORATORY DATA ANALYSIS (EDA) & CHURN DRIVERS
    # ==========================================
    story.append(Paragraph("2. Exploratory Data Analysis (EDA) & Churn Drivers", h1_style))
    story.append(Paragraph(
        "Granular statistical analysis and cohort segmentation identified critical friction points and structural root causes behind subscriber departures.",
        body_style
    ))

    eda_points = [
        Paragraph("• <b>Contract Duration Disparity:</b> Month-to-month contracts experience a staggering <b>42.71% churn rate</b>, whereas 1-Year contracts drop to 11.27% and 2-Year contracts achieve an industry-leading <b>2.83% churn rate</b>. Contractual commitment is the primary churn damper.", bullet_style),
        Paragraph("• <b>Tenure Vulnerability Window:</b> 50% of all customer churn occurs within the first <b>12 months of tenure</b> (median churn tenure = 10 months vs. 38 months for retained subscribers). First-year onboarding is the pivotal retention battleground.", bullet_style),
        Paragraph("• <b>Fiber Optic Pricing Friction:</b> Fiber optic subscribers churn at <b>41.89%</b> compared to 18.96% for DSL users, driven by an average monthly spend of $91.50 without complementary technical support.", bullet_style),
        Paragraph("• <b>Payment Method Vulnerability:</b> Electronic check users register a <b>45.29% churn rate</b> (vs 15.24% for auto-pay credit card and 16.71% for auto-pay bank transfer), highlighting invoicing friction and active monthly payment reconsideration.", bullet_style),
        Paragraph("• <b>Security & Support Stickiness:</b> Subscribers lacking Tech Support or Online Security churn at <b>41.6%</b>, compared to under 15% for accounts with bundled cyber protection services.", bullet_style),
    ]

    img_eda_path = "visuals/churn_by_contract.png"
    if os.path.exists(img_eda_path):
        img_eda = Image(img_eda_path, width=280, height=200)
    else:
        img_eda = Paragraph("Chart asset: churn_by_contract.png", body_style)

    t_eda = Table([[eda_points, img_eda]], colWidths=[400, 284])
    t_eda.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('ALIGN', (1, 0), (1, 0), 'CENTER'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t_eda)

    story.append(PageBreak())

    # ==========================================
    # SLIDE 4: MACHINE LEARNING BENCHMARKING
    # ==========================================
    story.append(Paragraph("3. Machine Learning Models: Training, Evaluation & Benchmarks", h1_style))
    story.append(Paragraph(
        "Multiple classification models were trained and benchmarked using rigorous <b>5-Fold Stratified Cross-Validation</b> on holdout test partitions, balancing precision against recall to minimize business revenue loss.",
        body_style
    ))
    story.append(Spacer(1, 4))

    # Benchmark metrics table
    ml_table_data = [
        [
            Paragraph("<b>Model Architecture</b>", body_style),
            Paragraph("<b>Accuracy</b>", body_style),
            Paragraph("<b>Precision</b>", body_style),
            Paragraph("<b>Recall</b>", body_style),
            Paragraph("<b>F1-Score</b>", body_style),
            Paragraph("<b>ROC-AUC</b>", body_style),
            Paragraph("<b>Primary Business Advantage</b>", body_style),
        ],
        [
            Paragraph("<b>Logistic Regression (Baseline)</b>", body_style),
            Paragraph("80.20%", body_style),
            Paragraph("65.21%", body_style),
            Paragraph("54.01%", body_style),
            Paragraph("0.5908", body_style),
            Paragraph("0.8412", body_style),
            Paragraph("Fast linear baseline; highly interpretable odds ratios", body_style),
        ],
        [
            Paragraph("<b>Balanced Logistic Regression</b>", body_style),
            Paragraph("73.81%", body_style),
            Paragraph("50.43%", body_style),
            Paragraph("<b>78.34%</b>", body_style),
            Paragraph("0.6136", body_style),
            Paragraph("0.8385", body_style),
            Paragraph("Maximized recall; ideal when missing a churner is expensive", body_style),
        ],
        [
            Paragraph("<b>Random Forest (100 Trees)</b>", body_style),
            Paragraph("79.13%", body_style),
            Paragraph("63.18%", body_style),
            Paragraph("49.47%", body_style),
            Paragraph("0.5548", body_style),
            Paragraph("0.8251", body_style),
            Paragraph("Robust against outliers; captures non-linear feature splits", body_style),
        ],
        [
            Paragraph("<b>XGBoost Classifier (Champion)</b>", body_style),
            Paragraph("<b>80.48%</b>", body_style),
            Paragraph("<b>65.66%</b>", body_style),
            Paragraph("56.42%", body_style),
            Paragraph("<b>0.6067</b>", body_style),
            Paragraph("<b>0.8465</b>", body_style),
            Paragraph("<b>Best discrimination & generalizability across all 5 folds</b>", body_style),
        ],
    ]
    t_ml = Table(ml_table_data, colWidths=[150, 65, 65, 65, 65, 65, 209])
    t_ml.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1e3a8a")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (1, 0), (5, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8fafc")]),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(t_ml)
    story.append(Spacer(1, 10))

    img_roc_path = "visuals/roc_curves_comparison.png"
    if os.path.exists(img_roc_path):
        img_roc = Image(img_roc_path, width=330, height=160)
    else:
        img_roc = Paragraph("ROC Curves comparison chart", body_style)

    img_cm_path = "visuals/model_comparison_metrics.png"
    if os.path.exists(img_cm_path):
        img_cm = Image(img_cm_path, width=330, height=160)
    else:
        img_cm = Paragraph("Comparison metrics chart", body_style)

    t_plots = Table([[img_roc, img_cm]], colWidths=[342, 342])
    t_plots.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(t_plots)

    story.append(PageBreak())

    # ==========================================
    # SLIDE 5: MODEL EXPLAINABILITY (SHAP AI ATTRIBUTION)
    # ==========================================
    story.append(Paragraph("4. Explainability: Game-Theoretic SHAP Feature Importance", h1_style))
    story.append(Paragraph(
        "To empower non-technical executives and CRM account managers, we integrated <b>SHAP (SHapley Additive exPlanations)</b> "
        "via <code>shap.TreeExplainer</code>, transforming black-box ensemble scores into transparent, mathematically rigorous feature attributions.",
        body_style
    ))
    story.append(Spacer(1, 4))

    shap_text = [
        Paragraph("<b>Key Driver Insights Discovered by SHAP:</b>", h2_style),
        Paragraph("• <b>1. Contract Month-to-Month (Mean |SHAP| = 0.68):</b> Single strongest driver elevating churn probability; accounts lacking annual commitments exhibit immediate vulnerability.", bullet_style),
        Paragraph("• <b>2. Tenure (Mean |SHAP| = 0.52):</b> High tenure pushes SHAP values heavily into negative churn territory. Surviving beyond month 18 creates strong habitual retention inertia.", bullet_style),
        Paragraph("• <b>3. Fiber Optic Service (Mean |SHAP| = 0.38):</b> Fiber service strongly pushes probability toward churn unless mitigated by bundle discounts or technical support.", bullet_style),
        Paragraph("• <b>4. Payment Method Electronic Check (Mean |SHAP| = 0.28):</b> Associated with elevated churn odds due to manual payment friction.", bullet_style),
        Paragraph("• <b>5. TotalCharges & MonthlyCharges:</b> Higher billing increments without perceived service value significantly accelerate departure likelihood.", bullet_style),
    ]

    img_shap_path = "visuals/shap_summary_plot.png"
    if os.path.exists(img_shap_path):
        img_shap = Image(img_shap_path, width=360, height=210)
    else:
        img_shap = Paragraph("SHAP Summary Beeswarm Plot", body_style)

    t_shap = Table([[shap_text, img_shap]], colWidths=[324, 360])
    t_shap.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('ALIGN', (1, 0), (1, 0), 'CENTER'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t_shap)

    story.append(PageBreak())

    # ==========================================
    # SLIDE 6: LTV REGRESSION & FASTAPI DEPLOYMENT
    # ==========================================
    story.append(Paragraph("5. LTV Forecasting & FastAPI Real-Time Microservice", h1_style))
    story.append(Paragraph(
        "Bridging churn probability with financial impact, we developed dedicated Customer Lifetime Value regression models and exposed "
        "production inference endpoints through a high-performance <b>FastAPI REST microservice</b> containerized with Docker.",
        body_style
    ))
    story.append(Spacer(1, 4))

    ltv_col1 = [
        Paragraph("<b>Customer Lifetime Value Regression:</b>", h2_style),
        Paragraph("• <b>Model:</b> Gradient Boosting Regressor trained on active subscriber margin and longevity trajectories.", bullet_style),
        Paragraph("• <b>Performance:</b> Achieved <b>R² = 0.9983</b>, <b>MAE = $39.51</b>, and <b>RMSE = $93.72</b> on holdout data.", bullet_style),
        Paragraph("• <b>Gross Margin Integration:</b> Incorporates 80% contribution margin and estimated future tenure horizon to forecast real subscriber value.", bullet_style),
        Paragraph("• <b>Value Segments:</b> Profiles Top 25% VIP accounts ($3,786+ LTV) vs at-risk high-spend tiers.", bullet_style),
        Spacer(1, 8),
        Paragraph("<b>Docker Containerization:</b>", h2_style),
        Paragraph("• <code>Dockerfile</code>: Multi-stage slim Python 3.11 runtime environment.<br/>• <code>docker-compose.yml</code>: Orchestrates FastAPI microservice alongside PostgreSQL database and Metabase analytics engine.", body_style),
    ]

    ltv_col2 = [
        Paragraph("<b>FastAPI Microservice Endpoints (<code>src/api/main.py</code>):</b>", h2_style),
        Paragraph("• <code>GET /health</code> — Diagnostic checks verifying model artifacts.", bullet_style),
        Paragraph("• <code>GET /model/info</code> — Exposes AUC, F1, and schema specifications.", bullet_style),
        Paragraph("• <code>POST /predict/single</code> — Real-time inference delivering churn probability, risk tier (Low/Medium/High), predicted LTV, and prescribed retention action.", bullet_style),
        Paragraph("• <code>POST /predict/batch</code> — High-throughput CSV batch inference scoring thousands of customer profiles in milliseconds.", bullet_style),
        Paragraph("• <code>GET /docs</code> — Interactive OpenAPI / Swagger UI interface.", bullet_style),
        Spacer(1, 4),
        Paragraph("<b>Prescriptive Action Engine:</b>", h2_style),
        Paragraph("High-risk users automatically trigger targeted actions: <i>Contract Migration Incentive ($15/mo discount for 12 months)</i> or <i>TechSupport Free Trial Bundle</i>.", body_style)
    ]

    t_ltv = Table([[ltv_col1, ltv_col2]], colWidths=[342, 342])
    t_ltv.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BACKGROUND', (1, 0), (1, 0), colors.HexColor("#f8fafc")),
        ('BOX', (1, 0), (1, 0), 1, colors.HexColor("#cbd5e1")),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (1, 0), (1, 0), 10),
        ('RIGHTPADDING', (1, 0), (1, 0), 10),
    ]))
    story.append(t_ltv)

    story.append(PageBreak())

    # ==========================================
    # SLIDE 7: POWER BI & METABASE EXECUTIVE DASHBOARDS
    # ==========================================
    story.append(Paragraph("6. Visualization & Insights: Multi-Page Executive BI Suite", h1_style))
    story.append(Paragraph(
        "A publication-grade 3-page reporting suite designed in accordance with enterprise BI best practices, powered by our enriched ML dataset (<code>data/telco_churn_powerbi_dataset.csv</code>) and complete DAX library.",
        body_style
    ))
    story.append(Spacer(1, 4))

    dash_img_path = "visuals/powerbi_dashboard_page1_executive.png"
    if os.path.exists(dash_img_path):
        dash_img = Image(dash_img_path, width=440, height=220)
    else:
        dash_img = Paragraph("Power BI Dashboard Page 1 Preview", body_style)

    dash_text = [
        Paragraph("<b>3-Page Reporting Architecture:</b>", h2_style),
        Paragraph("• <b>Page 1: Executive Overview:</b> C-suite tracking of Total Base (7,043), Global Churn Rate (26.54%), MRR at Risk ($139.1K), and Attrition Breakdown by Contract & Billing.", bullet_style),
        Paragraph("• <b>Page 2: Risk Diagnostics:</b> Deep-dive cohort explorer isolating Fiber Optic friction, Electronic Check vulnerability, and tenure decay funnels.", bullet_style),
        Paragraph("• <b>Page 3: LTV Retention Engine:</b> Prioritized retention quadrant categorizing subscribers by Lifetime Value vs Churn Probability, identifying the Top 500 VIP high-risk targets for immediate CRM outreach.", bullet_style),
        Spacer(1, 6),
        Paragraph("• <b>Alternative Dashboards:</b> Interactive Tailwind CSS + Chart.js web dashboard (<code>dashboard/telco_churn_dashboard.html</code>) and Metabase setup guide (<code>metabase/metabase_setup_guide.md</code>).", body_style),
    ]

    t_dash = Table([[dash_img, dash_text]], colWidths=[450, 234])
    t_dash.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('ALIGN', (0, 0), (0, 0), 'CENTER'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t_dash)

    story.append(PageBreak())

    # ==========================================
    # SLIDE 8: DELIVERABLES SUMMARY & REPOSITORY VERIFICATION
    # ==========================================
    story.append(Paragraph("7. Comprehensive Deliverables Checklist & Verification", h1_style))
    story.append(Paragraph(
        "Every milestone from the 4-week end-to-end data analytics and ML engineering lifecycle has been completed, tested, and documented.",
        body_style
    ))
    story.append(Spacer(1, 6))

    deliv_data = [
        [
            Paragraph("<b>Deliverable Category</b>", body_style),
            Paragraph("<b>Repository Asset / Path</b>", body_style),
            Paragraph("<b>Status & Highlights</b>", body_style),
        ],
        [
            Paragraph("<b>Data Hygiene & SQL Warehouse</b>", body_style),
            Paragraph("<code>src/db_ingestion.py</code><br/><code>sql/01_create_database.sql</code><br/><code>sql/04_churn_and_ltv_views.sql</code>", body_style),
            Paragraph("✅ PostgreSQL schema with 5 analytical views and automated SQLAlchemy ingestion pipeline.", body_style),
        ],
        [
            Paragraph("<b>Exploratory Data Analysis</b>", body_style),
            Paragraph("<code>notebooks/01_data_quality_check.ipynb</code><br/><code>notebooks/03_exploratory_data_analysis.ipynb</code><br/><code>notebooks/reports/business_insights.md</code>", body_style),
            Paragraph("✅ Comprehensive EDA, contract cohort churn decay, and customer profile insights.", body_style),
        ],
        [
            Paragraph("<b>Machine Learning & Explainability</b>", body_style),
            Paragraph("<code>src/train_models.py</code><br/><code>models/xgboost_model.joblib</code><br/><code>visuals/shap_summary_plot.png</code>", body_style),
            Paragraph("✅ 5-Fold CV XGBoost champion model (0.8465 AUC) with SHAP TreeExplainer attribution.", body_style),
        ],
        [
            Paragraph("<b>LTV Regression & REST API</b>", body_style),
            Paragraph("<code>src/train_ltv_regressor.py</code><br/><code>models/ltv_regressor_model.joblib</code><br/><code>src/api/main.py</code>", body_style),
            Paragraph("✅ Gradient Boosting LTV regressor (R² = 0.9983) and FastAPI single/batch inference microservice.", body_style),
        ],
        [
            Paragraph("<b>Executive BI Dashboards</b>", body_style),
            Paragraph("<code>dashboard/dax_measures.md</code><br/><code>dashboard/telco_churn_dashboard.html</code><br/><code>metabase/metabase_setup_guide.md</code>", body_style),
            Paragraph("✅ 3-page Power BI dashboard suite, DAX library, Metabase guide, and interactive HTML preview.", body_style),
        ],
        [
            Paragraph("<b>Containerization & Testing</b>", body_style),
            Paragraph("<code>Dockerfile</code>, <code>docker-compose.yml</code><br/><code>tests/test_pipeline.py</code>", body_style),
            Paragraph("✅ Multi-container orchestration; 10/10 automated tests passing with Pytest.", body_style),
        ],
    ]

    t_deliv = Table(deliv_data, colWidths=[160, 240, 284])
    t_deliv.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1e3a8a")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8fafc")]),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(t_deliv)
    story.append(Spacer(1, 10))

    # Verification banner
    verif_box = [
        [Paragraph("<b>🔗 Verified GitHub Repository:</b> <font color='#0284c7'><u>https://github.com/addu91577-sketch/Customer-Churn-LTV-Engine</u></font> &nbsp;|&nbsp; <b>Author:</b> Adarsh Kumar Pandey", body_style)]
    ]
    t_verif = Table(verif_box, colWidths=[684])
    t_verif.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#eff6ff")),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#93c5fd")),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ]))
    story.append(t_verif)

    # Build PDF with NumberedCanvas
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Project Report PDF generated successfully: {filename}")


if __name__ == '__main__':
    build_pdf("Project_Report.pdf")
