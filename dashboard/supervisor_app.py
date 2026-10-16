from pathlib import Path
from textwrap import dedent
import json

import pandas as pd
import streamlit as st
import plotly.graph_objects as go


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Underwater Acoustic AI - Supervisor Dashboard",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# PROJECT PATHS
# ============================================================

ROOT = Path(__file__).resolve().parents[1]

FINAL_RESULTS = (
    ROOT
    / "final_results"
)

MASTER_VERIFIED = (
    FINAL_RESULTS
    / "MASTER_VERIFIED_RESULTS_v1.json"
)

MASTER_STATUS = (
    FINAL_RESULTS
    / "MASTER_PROJECT_STATUS_v1.json"
)

SUPERVISOR_SUMMARY = (
    FINAL_RESULTS
    / "MASTER_SUPERVISOR_RESULTS_SUMMARY_v1.csv"
)

ACOUSTIC_FEATURES = (
    ROOT
    / "acoustic_analysis_v2"
    / "acoustic_features_all_files_v1.csv"
)

ACOUSTIC_FIGURE_DIR = (
    ROOT
    / "acoustic_analysis_v3"
    / "figures"
)

SHIPSEAR_FIGURE_DIR = (
    FINAL_RESULTS
    / "ShipsEar_Acoustic_Characterization_v1"
    / "figures"
)


# ============================================================
# LOADERS
# ============================================================

@st.cache_data
def load_json(path_string):

    path = Path(path_string)

    if not path.exists():
        return {}

    with path.open(
        "r",
        encoding="utf-8",
    ) as f:

        return json.load(f)


@st.cache_data
def load_csv(path_string):

    path = Path(path_string)

    if not path.exists():
        return pd.DataFrame()

    return pd.read_csv(path)


verified = load_json(
    str(MASTER_VERIFIED)
)

project_status = load_json(
    str(MASTER_STATUS)
)

summary_df = load_csv(
    str(SUPERVISOR_SUMMARY)
)


# ============================================================
# DATA SAFETY CHECK
# ============================================================

if not verified:

    st.error(
        "MASTER_VERIFIED_RESULTS_v1.json was not found."
    )

    st.stop()


results = verified.get(
    "results",
    {}
)


speedboat = results.get(
    "SpeedBoat",
    {}
)

uuv = results.get(
    "UUV",
    {}
)

noise = results.get(
    "NoiseTarget",
    {}
)

deepship = results.get(
    "DeepShip",
    {}
)

shipsear = results.get(
    "ShipsEar",
    {}
)

ds3500 = results.get(
    "DS3500",
    {}
)


# ============================================================
# STYLE
# ============================================================

st.markdown(
    """
    <style>

    .stApp {
        background:
            radial-gradient(
                circle at 90% 5%,
                rgba(18, 144, 165, 0.16),
                transparent 28%
            ),
            radial-gradient(
                circle at 5% 50%,
                rgba(30, 78, 155, 0.10),
                transparent 30%
            ),
            #07131d;
    }

    [data-testid="stSidebar"] {
        background:
            linear-gradient(
                180deg,
                #081925 0%,
                #0b2231 100%
            );
        border-right:
            1px solid rgba(255,255,255,0.08);
    }

    .block-container {
        max-width: 1500px;
        padding-top: 1.7rem;
        padding-bottom: 4rem;
    }

    .hero {
        padding: 2.2rem 2.4rem;
        border-radius: 24px;
        background:
            linear-gradient(
                120deg,
                rgba(10, 44, 65, 0.98),
                rgba(8, 94, 111, 0.78)
            );
        border:
            1px solid rgba(79, 214, 225, 0.23);
        box-shadow:
            0 20px 55px rgba(0,0,0,0.23);
        margin-bottom: 1.5rem;
    }

    .hero-kicker {
        color: #65e6ee;
        font-size: 0.78rem;
        font-weight: 800;
        letter-spacing: 0.15em;
        text-transform: uppercase;
        margin-bottom: 0.65rem;
    }

    .hero-title {
        color: #f6fcff;
        font-size: 2.35rem;
        font-weight: 850;
        line-height: 1.12;
        margin-bottom: 0.7rem;
    }

    .hero-subtitle {
        color: #bdd9e4;
        max-width: 1000px;
        line-height: 1.65;
        font-size: 1.02rem;
    }

    .metric-card {
        min-height: 128px;
        border-radius: 18px;
        padding: 1.2rem 1.25rem;
        background:
            rgba(12, 34, 49, 0.94);
        border:
            1px solid rgba(255,255,255,0.08);
        box-shadow:
            0 10px 30px rgba(0,0,0,0.16);
    }

    .metric-label {
        color: #83acbd;
        font-size: 0.75rem;
        font-weight: 760;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }

    .metric-value {
        color: #f7fcff;
        font-size: 1.85rem;
        font-weight: 850;
        margin-top: 0.28rem;
    }

    .metric-note {
        color: #91afbd;
        font-size: 0.79rem;
        margin-top: 0.25rem;
    }

    .section-kicker {
        color: #62dfe8;
        font-size: 0.75rem;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        font-weight: 800;
        margin-top: 1.5rem;
        margin-bottom: 0.25rem;
    }

    .research-box {
        padding: 1.4rem 1.6rem;
        border-radius: 18px;
        border-left:
            4px solid #25c8d8;
        background:
            rgba(9, 39, 56, 0.86);
        margin-bottom: 1.3rem;
        line-height: 1.65;
    }

    .finding {
        padding: 1.1rem 1.25rem;
        border-radius: 15px;
        margin-bottom: 0.75rem;
        background:
            linear-gradient(
                120deg,
                rgba(9, 75, 87, 0.55),
                rgba(13, 43, 61, 0.75)
            );
        border:
            1px solid rgba(77, 211, 219, 0.18);
        line-height: 1.55;
    }

    .status-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 1rem;
        padding: 0.85rem 1rem;
        margin-bottom: 0.55rem;
        border-radius: 14px;
        background:
            rgba(12, 34, 49, 0.92);
        border:
            1px solid rgba(255,255,255,0.07);
    }

    .status-title {
        color: #f1f8fb;
        font-weight: 720;
    }

    .status-note {
        color: #87a8b6;
        font-size: 0.80rem;
        margin-top: 0.12rem;
    }

    .badge-green {
        color: #69efb3;
        background:
            rgba(16,185,129,0.13);
        border-radius: 999px;
        padding: 0.32rem 0.65rem;
        font-size: 0.75rem;
        font-weight: 760;
        white-space: nowrap;
    }

    .badge-blue {
        color: #91c9ff;
        background:
            rgba(59,130,246,0.14);
        border-radius: 999px;
        padding: 0.32rem 0.65rem;
        font-size: 0.75rem;
        font-weight: 760;
        white-space: nowrap;
    }

    .small-note {
        color: #8eacb9;
        font-size: 0.82rem;
        line-height: 1.55;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# UI HELPERS
# ============================================================

def metric_card(
    label,
    value,
    note,
):

    html = f"""
    <div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
        <div class="metric-note">{note}</div>
    </div>
    """

    st.markdown(
        dedent(html),
        unsafe_allow_html=True,
    )


def status_row(
    title,
    note,
    badge,
    badge_class="badge-green",
):

    html = f"""
    <div class="status-row">
        <div>
            <div class="status-title">{title}</div>
            <div class="status-note">{note}</div>
        </div>
        <span class="{badge_class}">{badge}</span>
    </div>
    """

    st.markdown(
        dedent(html),
        unsafe_allow_html=True,
    )


def percent(
    value,
):

    if value in [
        None,
        "",
    ]:

        return "N/A"

    return (
        f"{float(value) * 100:.1f}%"
    )


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        """
        ## Underwater Acoustic AI

        **Supervisor Research Dashboard**

        Evidence-based summary of acoustic
        characterization and ML/AI classification.
        """
    )

    st.divider()

    page = st.radio(
        "Navigate",
        [
            "Executive Summary",
            "Research Workflow",
            "Dataset Journey",
            "Acoustic Analysis",
            "ML / AI Results",
            "Scientific Validation",
            "Future Operational System",
            "Final Conclusions",
        ],
        label_visibility="collapsed",
    )

    st.divider()

    st.success(
        "Experimental phase complete"
    )

    st.caption(
        "Dashboard values are read from the "
        "frozen MASTER_VERIFIED_RESULTS_v1 source."
    )


# ============================================================
# PAGE - EXECUTIVE SUMMARY
# ============================================================

if page == "Executive Summary":

    hero_html = """
    <div class="hero">
        <div class="hero-kicker">
            PASSIVE ACOUSTIC SENSING • MACHINE LEARNING • AI
        </div>
        <div class="hero-title">
            Underwater Acoustic Contact Classification
        </div>
        <div class="hero-subtitle">
            A consolidated research study investigating how
            underwater acoustic contacts can be characterized
            and classified using engineered acoustic features,
            conventional machine learning and deep-learning
            approaches.
        </div>
    </div>
    """

    st.markdown(
        dedent(hero_html),
        unsafe_allow_html=True,
    )

    research_html = """
    <div class="research-box">
        <strong>
            Can underwater acoustic contacts be detected,
            acoustically characterized and classified using
            machine learning / artificial intelligence?
        </strong>
        <br><br>
        The work evaluates this question through multiple
        underwater-acoustic datasets, acoustic-domain analysis,
        controlled train/test protocols and comparison of
        classical and deep-learning models.
    </div>
    """

    st.markdown(
        dedent(research_html),
        unsafe_allow_html=True,
    )


    # ========================================================
    # TOP METRICS
    # ========================================================

    c1, c2, c3, c4 = st.columns(4)


    with c1:

        metric_card(
            "Research Families",
            "4",
            (
                "QiandaoEar22, DeepShip, "
                "ShipsEar and DS3500"
            ),
        )


    with c2:

        metric_card(
            "Verified Tasks",
            "6",
            (
                "Three Qiandao tasks plus "
                "DeepShip, ShipsEar and DS3500"
            ),
        )


    with c3:

        metric_card(
            "Best Macro-F1",
            percent(
                noise.get(
                    "winner_macro_f1"
                )
            ),
            "Noise Target held-out evaluation",
        )


    with c4:

        metric_card(
            "Project Status",
            "FROZEN",
            "Experimental results consolidated",
        )


    # ========================================================
    # DIRECT ANSWER
    # ========================================================

    st.markdown(
        '<div class="section-kicker">Direct Answer</div>',
        unsafe_allow_html=True,
    )


    st.markdown(
        dedent(
            """
            <div class="finding">
                <strong>
                    Yes — ML/AI can discriminate useful patterns
                    in the available underwater acoustic data.
                </strong>
                The experiments demonstrate measurable classification
                capability across several tasks, but performance varies
                considerably with dataset structure, source variability
                and the number of independent recordings.
            </div>
            """
        ),
        unsafe_allow_html=True,
    )


    st.markdown(
        """
        <div class="finding">

        <strong>Acoustic-domain information is useful.</strong>

        Spectrum, broadband and narrowband structure,
        LOFAR-style low-frequency tonal information and
        DEMON-style modulation features were incorporated into
        the research workflow for characterization and,
        where scientifically appropriate, model fusion.

        </div>
        """,
        unsafe_allow_html=True,
    )


    st.markdown(
        """
        <div class="finding">

        <strong>More complex models were not automatically
        better.</strong>

        Across the completed Qiandao classification tasks and
        DeepShip comparison, the MFCC + SVM family provided
        the strongest locked result under the predefined
        evaluation protocols.

        </div>
        """,
        unsafe_allow_html=True,
    )


    # ========================================================
    # DATASET STATUS
    # ========================================================

    st.markdown(
        '<div class="section-kicker">Final Dataset Status</div>',
        unsafe_allow_html=True,
    )

    left, right = st.columns(
        2,
        gap="large",
    )


    with left:

        status_row(
            "QiandaoEar22",
            (
                "SpeedBoat, UUV and Noise Target "
                "classification evidence finalized."
            ),
            "COMPLETE",
        )


        status_row(
            "DeepShip",
            (
                "Four-class parent-source-held-out "
                "A/B/C comparison finalized."
            ),
            "COMPLETE",
        )


    with right:

        status_row(
            "ShipsEar",
            (
                "Five-class acoustic characterization and "
                "restricted three-class exploratory ML finalized."
            ),
            "COMPLETE",
        )


        status_row(
            "DS3500",
            (
                "One-to-one paired relationship with "
                "ShipsEar audited and frozen."
            ),
            "RESEARCH ONLY",
            "badge-blue",
        )


    # ========================================================
    # VERIFIED RESULTS SNAPSHOT
    # ========================================================

    st.markdown(
        '<div class="section-kicker">Verified Results Snapshot</div>',
        unsafe_allow_html=True,
    )


    result_rows = [

        {
            "Task":
                "SpeedBoat",

            "Evaluation":
                "Frozen final test",

            "Best Model":
                speedboat.get(
                    "winner",
                    "N/A",
                ),

            "Primary Macro-F1":
                speedboat.get(
                    "winner_macro_f1"
                ),
        },

        {
            "Task":
                "UUV",

            "Evaluation":
                "Frozen final test",

            "Best Model":
                uuv.get(
                    "winner",
                    "N/A",
                ),

            "Primary Macro-F1":
                uuv.get(
                    "winner_macro_f1"
                ),
        },

        {
            "Task":
                "Noise Target",

            "Evaluation":
                noise.get(
                    "evaluation_design",
                    "N/A",
                ),

            "Best Model":
                noise.get(
                    "winner",
                    "N/A",
                ),

            "Primary Macro-F1":
                noise.get(
                    "winner_macro_f1"
                ),
        },

        {
            "Task":
                "DeepShip",

            "Evaluation":
                "Parent-source-held-out outer OOF",

            "Best Model":
                deepship.get(
                    "winner",
                    "N/A",
                ),

            "Primary Macro-F1":
                deepship.get(
                    "winner_segment_macro_f1"
                ),
        },

        {
            "Task":
                "ShipsEar restricted 3-class",

            "Evaluation":
                "Natural-group-held-out exploratory ML",

            "Best Model":
                (
                    shipsear
                    .get(
                        "restricted_ml",
                        {}
                    )
                    .get(
                        "model",
                        "N/A",
                    )
                ),

            "Primary Macro-F1":
                (
                    shipsear
                    .get(
                        "restricted_ml",
                        {}
                    )
                    .get(
                        "segment_macro_f1"
                    )
                ),
        },
    ]


    snapshot = pd.DataFrame(
        result_rows
    )


    snapshot[
        "Primary Macro-F1"
    ] = snapshot[
        "Primary Macro-F1"
    ].apply(
        lambda x:
            round(
                float(x),
                3,
            )
            if pd.notna(x)
            else ""
    )


    st.dataframe(
        snapshot,
        use_container_width=True,
        hide_index=True,
    )


    st.caption(
        "Macro-F1 values are not interpreted as directly "
        "comparable across all tasks because the datasets, "
        "class structures and evaluation protocols differ."
    )


    # ========================================================
    # SCIENTIFIC BOUNDARIES
    # ========================================================

    st.markdown(
        '<div class="section-kicker">Important Scientific Boundaries</div>',
        unsafe_allow_html=True,
    )


    st.info(
        "ShipsEar restricted three-class ML is exploratory and "
        "must not be reported as a full five-class classifier."
    )


    st.info(
        "DS3500 is retained as a paired research counterpart of "
        "ShipsEar and is not counted as an independent validation dataset."
    )


    st.info(
        "Current local recordings are primarily mono. "
        "True beamforming, direction-of-arrival estimation and "
        "spatial tracking require synchronized hydrophone-array data."
    )


# ============================================================
# PAGE - RESEARCH WORKFLOW
# ============================================================

elif page == "Research Workflow":

    st.title(
        "Research Workflow"
    )

    st.caption(
        "How the project moved from raw underwater recordings "
        "to validated acoustic and ML/AI evidence."
    )


    # ========================================================
    # WHY THIS WORKFLOW
    # ========================================================

    st.markdown(
        '<div class="section-kicker">Why a structured workflow was needed</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        dedent(
            """
            <div class="research-box">

            The project did not begin by directly training an AI model.

            <br><br>

            Underwater acoustic datasets can contain duplicate files,
            multiple five-second segments from the same original source,
            unequal class structures and dataset relationships that can
            make model performance appear stronger than it really is.

            <br><br>

            Therefore, the work first established the data structure and
            provenance, then extracted acoustic evidence, and only after
            that performed ML/AI experiments where a defensible
            train/test separation was possible.

            </div>
            """
        ),
        unsafe_allow_html=True,
    )


    # ========================================================
    # MAIN PIPELINE
    # ========================================================

    st.markdown(
        '<div class="section-kicker">End-to-End Research Pipeline</div>',
        unsafe_allow_html=True,
    )

    pipeline_html = (
        '<div class="pipeline">'
        '<strong>1. Raw Underwater Audio</strong><br>'
        'Original WAV recordings from the available datasets'
        '<br><br>↓<br><br>'
        '<strong>2. Dataset Audit &amp; Provenance Checking</strong><br>'
        'File validity • classes • sample rates • durations • '
        'duplicates • source/group relationships'
        '<br><br>↓<br><br>'
        '<strong>3. Standardized Analysis Preparation</strong><br>'
        'Consistent metadata • canonical records • '
        'controlled analysis structure'
        '<br><br>↓<br><br>'
        '<strong>4. Acoustic Characterization</strong><br>'
        'Spectrum • PSD • STFT • Broadband • Narrowband • '
        'LOFAR-style tonal analysis • DEMON-style modulation analysis'
        '<br><br>↓<br><br>'
        '<strong>5. ML Feature Preparation</strong><br>'
        'MFCC • Log-Mel representations • engineered acoustic features'
        '<br><br>↓<br><br>'
        '<strong>6. Leakage-Controlled Evaluation Design</strong><br>'
        'Source / session / provenance-group separation where supported'
        '<br><br>↓<br><br>'
        '<strong>7. ML / AI Model Evaluation</strong><br>'
        'Model A: MFCC + SVM<br>'
        'Model B: Log-Mel CNN<br>'
        'Model C: CNN + Acoustic Feature Fusion'
        '<br><br>↓<br><br>'
        '<strong>8. Frozen Final Evaluation</strong><br>'
        'Test or outer-test data used only after model/protocol freeze'
        '<br><br>↓<br><br>'
        '<strong>9. Scientific Interpretation</strong><br>'
        'Performance • limitations • provenance • '
        'dataset independence • future system potential'
        '</div>'
    )

    st.markdown(
        pipeline_html,
        unsafe_allow_html=True,
    )


    # ========================================================
    # PHASE EXPLANATION
    # ========================================================

    st.markdown(
        '<div class="section-kicker">What happened at each stage</div>',
        unsafe_allow_html=True,
    )


    tab1, tab2, tab3, tab4 = st.tabs(
        [
            "Data Preparation",
            "Acoustic Analysis",
            "ML / AI",
            "Scientific Validation",
        ]
    )


    with tab1:

        st.markdown(
            "### Data Preparation"
        )

        st.markdown(
            """
            Before classification, the datasets were inspected to
            understand what an individual file actually represented.

            The audit covered:

            - file validity and audio format
            - dataset and class membership
            - duration and sampling structure
            - duplicate / related records
            - source, session or provenance groups
            - existing train/test split risks
            - relationships between datasets
            """
        )

        st.success(
            "Outcome: a consolidated master dataset structure was "
            "created before relying on model performance."
        )


    with tab2:

        st.markdown(
            "### Acoustic Analysis"
        )

        st.markdown(
            """
            Each usable audio record was converted into measurable
            acoustic information.

            The project examined:

            - frequency spectrum and power distribution
            - spectral centroid and bandwidth
            - broadband versus low-frequency energy
            - narrowband tonal peaks
            - LOFAR-style stable low-frequency lines
            - DEMON-style envelope modulation features
            - MFCC and Log-Mel representations for ML
            """
        )

        st.info(
            "These acoustic measurements describe the signal. "
            "They are not automatically equivalent to a vessel identity "
            "or a physical shaft/blade rate unless additional evidence "
            "supports that interpretation."
        )


    with tab3:

        st.markdown(
            "### ML / AI Evaluation"
        )

        st.markdown(
            """
            Three levels of modeling were compared where the dataset
            supported the experiment:

            **Model A — MFCC + RBF-SVM**

            A conventional machine-learning baseline using compact
            acoustic descriptors.

            **Model B — Log-Mel CNN**

            A deep-learning model operating on a time-frequency
            representation.

            **Model C — Acoustic Fusion**

            A CNN representation combined with engineered acoustic
            features such as spectral, tonal, LOFAR-style and
            DEMON-style information.
            """
        )

        st.success(
            "Important result: higher model complexity did not "
            "automatically produce better held-out performance."
        )


    with tab4:

        st.markdown(
            "### Scientific Validation"
        )

        st.markdown(
            """
            The central rule was:

            **training and testing should represent genuinely different
            sources whenever the dataset structure allows it.**

            A model can otherwise learn characteristics of the same
            recording source and appear to generalize when it has only
            seen another segment from that source.

            This principle affected several final decisions:

            - DeepShip used parent-source-held-out evaluation.
            - Noise Target used background-session-held-out evaluation.
            - ShipsEar's supplied file-level split was not used for
              independent-generalization claims.
            - ShipsEar full five-class source-held-out ML was not claimed
              because two classes had only one natural provenance group.
            - DS3500 was not treated as an independent validation dataset
              after its one-to-one relationship with ShipsEar was verified.
            """
        )


    # ========================================================
    # WHAT THIS WORKFLOW PROTECTS AGAINST
    # ========================================================

    st.markdown(
        '<div class="section-kicker">Why this matters</div>',
        unsafe_allow_html=True,
    )

    c1, c2, c3 = st.columns(
        3
    )


    with c1:

        metric_card(
            "Avoids",
            "Leakage",
            "Same-source information entering both train and test.",
        )


    with c2:

        metric_card(
            "Improves",
            "Credibility",
            "Results are tied to explicit frozen evaluation protocols.",
        )


    with c3:

        metric_card(
            "Supports",
            "Reproducibility",
            "Outputs, protocols and result locks are preserved.",
        )


    # ========================================================
    # FINAL TAKEAWAY
    # ========================================================

    st.markdown(
        '<div class="section-kicker">Key Takeaway</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        dedent(
            """
            <div class="finding">

            <strong>
            The main achievement was not simply training several models.
            </strong>

            The project built an evidence chain from raw underwater sound,
            through acoustic characterization and provenance-aware data
            preparation, to controlled ML/AI evaluation.

            This makes it possible to distinguish between a promising
            model result and a result that can reasonably support a
            scientific generalization claim.

            </div>
            """
        ),
        unsafe_allow_html=True,
    )


# ============================================================
# PAGE - DATASET JOURNEY
# ============================================================

elif page == "Dataset Journey":

    st.title(
        "Dataset Journey"
    )

    st.caption(
        "How each dataset was inspected, prepared, evaluated "
        "and assigned its final scientific role."
    )


    st.markdown(
        '<div class="section-kicker">Project Dataset Map</div>',
        unsafe_allow_html=True,
    )

    overview_rows = [
        {
            "Dataset / Family": "QiandaoEar22",
            "Main Use": "Target-vs-other / background classification",
            "Final Role": "Primary classification evidence",
            "Status": "Complete",
        },
        {
            "Dataset / Family": "DeepShip",
            "Main Use": "Four-class vessel classification",
            "Final Role": "Source-held-out multiclass benchmark",
            "Status": "Complete",
        },
        {
            "Dataset / Family": "ShipsEar",
            "Main Use": "Five-class acoustic characterization",
            "Final Role": "Characterization + restricted exploratory ML",
            "Status": "Complete",
        },
        {
            "Dataset / Family": "DS3500",
            "Main Use": "ShipsEar relationship investigation",
            "Final Role": "Research-only paired counterpart",
            "Status": "Complete",
        },
    ]

    st.dataframe(
        pd.DataFrame(
            overview_rows
        ),
        use_container_width=True,
        hide_index=True,
    )


    tab_q, tab_d, tab_s, tab_ds = st.tabs(
        [
            "QiandaoEar22",
            "DeepShip",
            "ShipsEar",
            "DS3500",
        ]
    )


    # ========================================================
    # QIANDAOEAR22
    # ========================================================

    with tab_q:

        st.markdown(
            "## QiandaoEar22"
        )

        st.markdown(
            """
            QiandaoEar22 provided several underwater-acoustic
            target categories. The current project developed
            three completed classification tasks from this family:

            - **SpeedBoat — Target vs Other**
            - **UUV — Target vs Other**
            - **Noise Target — Target-present vs Background**
            """
        )

        q1, q2, q3 = st.columns(3)

        with q1:

            metric_card(
                "SpeedBoat Final Test",
                f"{speedboat.get('test_samples', 0):,}",
                "Frozen final-test observations",
            )

        with q2:

            metric_card(
                "UUV Final Test",
                f"{uuv.get('test_samples', 0):,}",
                "Frozen final-test observations",
            )

        with q3:

            metric_card(
                "Noise Target OOF",
                f"{noise.get('total_unique_oof_samples', 0):,}",
                "Unique held-out observations",
            )


        st.markdown(
            "### What was done?"
        )

        st.markdown(
            """
            The work progressed from data preparation to three
            progressively different model approaches:

            **Model A — MFCC + SVM**

            **Model B — Log-Mel CNN**

            **Model C — Log-Mel CNN + engineered acoustic-feature fusion**

            The models were evaluated using frozen or held-out
            evaluation data rather than repeatedly tuning against
            the final result.
            """
        )


        st.markdown(
            "### Final finding"
        )

        st.success(
            "Across SpeedBoat, UUV and Noise Target, "
            "Model A — MFCC + SVM achieved the strongest "
            "locked Macro-F1 under the respective evaluation protocols."
        )


        st.markdown(
            "### Why this dataset family matters"
        )

        st.markdown(
            """
            QiandaoEar22 provided the strongest proof-of-concept
            evidence that useful underwater acoustic target patterns
            can be learned by ML/AI.

            It also showed that a simpler conventional model can
            generalize better than a more complex CNN or fusion model.
            """
        )


    # ========================================================
    # DEEPSHIP
    # ========================================================

    with tab_d:

        st.markdown(
            "## DeepShip"
        )

        st.markdown(
            """
            DeepShip was used for a more difficult **four-class
            vessel classification** problem:

            - Cargo
            - Passengership
            - Tanker
            - Tug
            """
        )

        d1, d2, d3 = st.columns(3)

        with d1:

            metric_card(
                "5-sec Observations",
                "1,118",
                "Used in the frozen comparison",
            )

        with d2:

            metric_card(
                "Parent Sources",
                f"{deepship.get('independent_parent_sources', 0)}",
                "Independent parent recordings",
            )

        with d3:

            metric_card(
                "Classes",
                "4",
                "Cargo • Passenger • Tanker • Tug",
            )


        st.markdown(
            "### Main scientific issue"
        )

        st.warning(
            "Multiple five-second observations can come from the "
            "same original recording. Randomly mixing those segments "
            "between training and testing could exaggerate performance."
        )


        st.markdown(
            "### What was done?"
        )

        st.markdown(
            f"""
            DeepShip therefore used a **3-fold parent-source-held-out
            outer evaluation**.

            The comparison included Models A, B and C.

            Final reporting winner:

            **{deepship.get('winner', 'N/A')}**

            Segment-level Macro-F1:
            **{deepship.get('winner_segment_macro_f1', 0):.3f}**

            Source-level Macro-F1:
            **{deepship.get('winner_source_macro_f1', 0):.3f}**
            """
        )


        st.markdown(
            "### Final interpretation"
        )

        st.info(
            "DeepShip demonstrated that vessel classification is "
            "possible but substantially harder than the binary Qiandao "
            "tasks. Strong source-to-source variation remained, and Tug "
            "evidence is especially limited because very few independent "
            "Tug parent recordings were available."
        )


    # ========================================================
    # SHIPSEAR
    # ========================================================

    with tab_s:

        st.markdown(
            "## ShipsEar"
        )

        s1, s2, s3 = st.columns(3)

        with s1:

            metric_card(
                "Segments",
                f"{shipsear.get('available_segments', 0):,}",
                "Five-second local audio records",
            )

        with s2:

            metric_card(
                "Natural Groups",
                f"{shipsear.get('natural_provenance_groups', 0)}",
                "Relevant independence units",
            )

        with s3:

            metric_card(
                "Local Classes",
                "5",
                "Used for acoustic characterization",
            )


        st.markdown(
            "### What did the audit discover?"
        )

        st.markdown(
            """
            The supplied file-level split was not considered sufficient
            for an independent-generalization claim because natural
            provenance groups crossed the original train/test structure.

            A second limitation was more important:

            **class_2 and class_4 each had only one natural provenance
            group.**
            """
        )


        st.markdown(
            "### Scientific decision"
        )

        st.warning(
            "A full five-class source-held-out ML experiment was not "
            "claimed because holding out the only available group for "
            "class_2 or class_4 would leave no independent training "
            "source for that class."
        )


        st.markdown(
            "### What was completed instead?"
        )

        st.markdown(
            """
            **1. Five-class acoustic characterization**

            All five local classes remained part of the Spectrum,
            broadband, narrowband, LOFAR-style and DEMON-style analysis.

            **2. Restricted exploratory ML**

            ML was limited to classes with more than one natural
            provenance group:
            **class_0, class_1 and class_3**.
            """
        )


        restricted = shipsear.get(
            "restricted_ml",
            {}
        )

        s4, s5, s6 = st.columns(3)

        with s4:

            metric_card(
                "Restricted Segments",
                f"{restricted.get('segments', 0):,}",
                "Three-class exploratory experiment",
            )

        with s5:

            metric_card(
                "Restricted Groups",
                f"{restricted.get('natural_groups', 0)}",
                "Held out by provenance group",
            )

        with s6:

            metric_card(
                "Group Macro-F1",
                f"{restricted.get('group_macro_f1', 0):.3f}",
                "Secondary group-level result",
            )


        st.info(
            "This restricted result is exploratory. "
            "It is not presented as a full ShipsEar five-class classifier."
        )


    # ========================================================
    # DS3500
    # ========================================================

    with tab_ds:

        st.markdown(
            "## DS3500"
        )

        ds1, ds2, ds3 = st.columns(3)

        with ds1:

            metric_card(
                "Paired Records",
                f"{ds3500.get('paired_records', 0):,}",
                "One-to-one with ShipsEar",
            )

        with ds2:

            metric_card(
                "Exact PCM Matches",
                str(
                    ds3500
                    .get(
                        "relationship_evidence",
                        {}
                    )
                    .get(
                        "exact_pcm_matches",
                        0,
                    )
                ),
                "Audio is not PCM-identical",
            )

        with ds3:

            metric_card(
                "Independent Benchmark",
                "NO",
                "Research-only paired dataset",
            )


        st.markdown(
            "### Why DS3500 was investigated separately"
        )

        st.markdown(
            """
            DS3500 initially appeared to provide another set of
            underwater-acoustic records that might be usable as an
            independent benchmark.

            The project therefore audited its relationship with ShipsEar
            before using it for another ML experiment.
            """
        )


        st.markdown(
            "### What was found?"
        )

        evidence = ds3500.get(
            "relationship_evidence",
            {}
        )

        st.markdown(
            f"""
            Across the available project data:

            - **{ds3500.get('paired_records', 0):,} / {ds3500.get('paired_records', 0):,}**
              records had a one-to-one pairing.
            - filenames matched across the paired records.
            - class assignments matched.
            - provenance groups matched.
            - original split assignments matched.
            - exact file matches = **{evidence.get('exact_file_hash_matches', 0)}**
            - exact PCM matches = **{evidence.get('exact_pcm_matches', 0)}**
            - median spectral cosine similarity =
              **{evidence.get('median_magnitude_spectrum_cosine_similarity', 0):.3f}**
            """
        )


        st.markdown(
            "### Final decision"
        )

        st.warning(
            "DS3500 is retained for research comparison and provenance "
            "investigation, but it is not counted as an independent "
            "second validation dataset."
        )


    # ========================================================
    # OVERALL TAKEAWAY
    # ========================================================

    st.markdown(
        '<div class="section-kicker">Overall Dataset Lesson</div>',
        unsafe_allow_html=True,
    )

    st.success(
        "The datasets were not treated as interchangeable collections "
        "of WAV files. Each dataset was assigned a role based on its "
        "provenance structure, class coverage and ability to support "
        "a defensible evaluation."
    )


# ============================================================
# PAGE - ACOUSTIC ANALYSIS
# ============================================================

elif page == "Acoustic Analysis":

    st.title(
        "Acoustic Analysis"
    )

    st.caption(
        "Frequency-domain and modulation-domain evidence used to "
        "understand underwater acoustic contacts before and alongside ML/AI."
    )


    # ========================================================
    # PROCESSING STATUS
    # ========================================================

    acoustic_df = load_csv(
        str(
            ACOUSTIC_FEATURES
        )
    )

    a1, a2, a3 = st.columns(
        3
    )

    with a1:

        metric_card(
            "Processed Records",
            f"{len(acoustic_df):,}",
            "Records with extracted acoustic features",
        )

    with a2:

        metric_card(
            "Core Acoustic Views",
            "5",
            "Spectrum • Broadband • Narrowband • LOFAR • DEMON",
        )

    with a3:

        metric_card(
            "Analysis Rate",
            "16 kHz",
            "Common cross-dataset comparison rate",
        )


    # ========================================================
    # WHY ACOUSTIC ANALYSIS
    # ========================================================

    st.markdown(
        '<div class="section-kicker">Why analyze the sound before classification?</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        ML/AI predicts a class, but acoustic analysis helps explain
        **what measurable signal structure exists inside the sound**.

        In this project, the acoustic layer was used to investigate
        frequency-energy distribution, tonal content, low-frequency
        machinery-like structure and amplitude-modulation behavior.
        """
    )


    # ========================================================
    # FIVE REQUIRED ACOUSTIC CONCEPTS
    # ========================================================

    st.markdown(
        '<div class="section-kicker">Core Acoustic Views</div>',
        unsafe_allow_html=True,
    )

    tab_sp, tab_bb, tab_nb, tab_lofar, tab_demon = st.tabs(
        [
            "Spectrum",
            "Broadband",
            "Narrowband",
            "LOFAR",
            "DEMON",
        ]
    )


    with tab_sp:

        st.markdown(
            "### Spectrum"
        )

        st.markdown(
            """
            **Simple meaning:**  
            Spectrum shows **where the sound energy is located across
            frequency**.

            For example, one contact may contain most of its energy at
            lower frequencies while another may extend more strongly into
            higher frequencies.

            In this project, spectral measurements included quantities
            such as:

            - dominant frequency
            - spectral centroid
            - spectral bandwidth
            - spectral roll-off
            - spectral flatness
            - spectral entropy
            """
        )

        st.info(
            "Spectrum describes the acoustic structure of the signal. "
            "A spectral peak alone is not treated as proof of a specific "
            "vessel or machinery component."
        )


    with tab_bb:

        st.markdown(
            "### Broadband Energy"
        )

        st.markdown(
            """
            **Simple meaning:**  
            Broadband sound has energy distributed across a relatively
            wide range of frequencies rather than being concentrated in
            only a few sharp tones.

            The project measured energy fractions in several frequency
            bands and compared lower-frequency versus higher-frequency
            energy distributions.

            This helps describe whether a contact is predominantly
            low-frequency, more broadband, or somewhere between the two.
            """
        )


    with tab_nb:

        st.markdown(
            "### Narrowband / Tonal Structure"
        )

        st.markdown(
            """
            **Simple meaning:**  
            Narrowband analysis looks for **sharp frequency peaks or
            stable tones**.

            Such peaks can arise from periodic machinery, rotating
            components or other tonal acoustic mechanisms.

            The project quantified features including:

            - narrowband peak count
            - prominent tonal frequencies
            - stable low-frequency lines
            - tonal contrast
            """
        )

        st.warning(
            "A tonal line can be acoustically useful for discrimination, "
            "but it should not automatically be labelled as a specific "
            "shaft or blade frequency without independent physical evidence."
        )


    with tab_lofar:

        st.markdown(
            "### LOFAR-style Analysis"
        )

        st.markdown(
            """
            **LOFAR = Low Frequency Analysis and Recording**

            **Simple meaning:**  
            LOFAR emphasizes relatively stable low-frequency tonal
            structure that may be associated with machinery-related
            acoustic signatures.

            In this project, LOFAR-style features included:

            - number of stable low-frequency lines
            - frequencies of prominent lines
            - line contrast relative to the surrounding spectrum

            These features were used as acoustic evidence and also formed
            part of the engineered feature set used in fusion modeling.
            """
        )


    with tab_demon:

        st.markdown(
            "### DEMON-style Analysis"
        )

        st.markdown(
            """
            **DEMON = Detection of Envelope Modulation on Noise**

            **Simple meaning:**  
            DEMON examines repeating patterns in the **amplitude envelope**
            of an acoustic signal.

            The project extracted quantities including:

            - dominant modulation frequency
            - modulation-peak prominence
            - number of modulation peaks
            - observation-duration information

            This can reveal periodic amplitude-modulation structure that
            may contain useful machinery or propeller-related information.
            """
        )

        st.warning(
            "The project reports DEMON modulation candidates. "
            "It does not automatically interpret every DEMON peak as a "
            "true shaft-rate or blade-rate measurement."
        )


    # ========================================================
    # CROSS-DATASET FIGURES
    # ========================================================

    st.markdown(
        '<div class="section-kicker">Cross-Dataset Acoustic Evidence</div>',
        unsafe_allow_html=True,
    )

    cross_figures = {
        "DeepShip class comparison":
            ACOUSTIC_FIGURE_DIR
            / "01_deepship_class_comparison.png",

        "SpeedBoat target vs other":
            ACOUSTIC_FIGURE_DIR
            / "02_speedboat_target_vs_other.png",

        "UUV target vs other":
            ACOUSTIC_FIGURE_DIR
            / "03_uuv_target_vs_other.png",

        "Noise Target vs background":
            ACOUSTIC_FIGURE_DIR
            / "04_noise_target_vs_background.png",

        "ShipsEar vs DS3500":
            ACOUSTIC_FIGURE_DIR
            / "05_shipsear_vs_ds3500.png",

        "LOFAR / DEMON across groups":
            ACOUSTIC_FIGURE_DIR
            / "06_lofar_demon_all_groups.png",

        "DEMON duration coverage":
            ACOUSTIC_FIGURE_DIR
            / "07_demon_duration_coverage.png",
    }


    available_cross_figures = {
        name: path
        for name, path in cross_figures.items()
        if path.exists()
    }


    if available_cross_figures:

        selected_cross = st.selectbox(
            "Select cross-dataset acoustic figure",
            list(
                available_cross_figures.keys()
            ),
        )

        st.image(
            str(
                available_cross_figures[
                    selected_cross
                ]
            ),
            use_container_width=True,
        )

    else:

        st.warning(
            "Cross-dataset acoustic figures were not found."
        )


    # ========================================================
    # SHIPSEAR GROUP-LEVEL EVIDENCE
    # ========================================================

    st.markdown(
        '<div class="section-kicker">ShipsEar Group-Level Acoustic Evidence</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        ShipsEar required special care because many five-second segments
        belonged to a much smaller number of natural provenance groups.

        Therefore these figures emphasize **group-level acoustic behavior**
        rather than treating every segment as an independent recording.
        """
    )


    ship_figures = {
        "Spectral centroid":
            SHIPSEAR_FIGURE_DIR
            / "figure_1_shipsear_group_spectral_centroid_v1.png",

        "Low-frequency fraction":
            SHIPSEAR_FIGURE_DIR
            / "figure_2_shipsear_group_low_frequency_fraction_v1.png",

        "Narrowband peaks":
            SHIPSEAR_FIGURE_DIR
            / "figure_3_shipsear_group_narrowband_peaks_v1.png",

        "LOFAR line contrast":
            SHIPSEAR_FIGURE_DIR
            / "figure_4_shipsear_group_lofar_contrast_v1.png",

        "DEMON modulation":
            SHIPSEAR_FIGURE_DIR
            / "figure_5_shipsear_group_demon_modulation_v1.png",
    }


    available_ship_figures = {
        name: path
        for name, path in ship_figures.items()
        if path.exists()
    }


    if available_ship_figures:

        selected_ship = st.selectbox(
            "Select ShipsEar group-level figure",
            list(
                available_ship_figures.keys()
            ),
        )

        st.image(
            str(
                available_ship_figures[
                    selected_ship
                ]
            ),
            use_container_width=True,
        )

    else:

        st.warning(
            "ShipsEar group-level figures were not found."
        )


    # ========================================================
    # SHIPSEAR INTERPRETATION
    # ========================================================

    st.markdown(
        '<div class="section-kicker">Example Scientific Findings</div>',
        unsafe_allow_html=True,
    )

    f1, f2, f3 = st.columns(
        3
    )

    with f1:

        metric_card(
            "class_3",
            "Low-frequency",
            "Strongest low-frequency-dominated pattern among group summaries",
        )

    with f2:

        metric_card(
            "class_4",
            "Broadband",
            "Highest spectral-centroid / broader-frequency behavior",
        )

    with f3:

        metric_card(
            "DEMON",
            "Overlap",
            "Dominant modulation alone did not clearly separate all classes",
        )


    st.markdown(
        """
        These observations are **descriptive acoustic findings**.

        They are useful for understanding the data and supporting feature
        engineering, but they are not interpreted as universal physical
        signatures of every vessel belonging to a class.
        """
    )


    # ========================================================
    # CONNECTION TO ML
    # ========================================================

    st.markdown(
        '<div class="section-kicker">How acoustic analysis connected to ML</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        The project used three complementary representation levels:

        **MFCC**  
        Compact acoustic descriptors used by Model A.

        **Log-Mel representation**  
        Time-frequency input used by the CNN in Model B.

        **Engineered acoustic features**  
        Spectral, broadband, narrowband, LOFAR-style and DEMON-style
        measurements used with the CNN representation in Model C.

        This allowed the study to test whether explicitly engineered
        acoustic information added value beyond a learned Log-Mel
        representation.
        """
    )

    st.success(
        "DeepShip showed that acoustic fusion improved substantially over "
        "the plain Log-Mel CNN, although the simpler MFCC + RBF-SVM still "
        "achieved the strongest predefined overall held-out result."
    )


    # ========================================================
    # IMPORTANT LIMITATIONS
    # ========================================================

    st.markdown(
        '<div class="section-kicker">Important Interpretation Limits</div>',
        unsafe_allow_html=True,
    )

    st.info(
        "The standardized cross-dataset analysis uses a 16 kHz analysis "
        "rate. Therefore the common comparison represents frequencies "
        "up to approximately 8 kHz."
    )

    st.info(
        "Amplitude values should not automatically be interpreted as "
        "absolute source level because recordings were collected under "
        "different acquisition conditions."
    )

    st.info(
        "Current recordings are primarily mono, so these acoustic analyses "
        "do not provide true spatial direction-of-arrival or beamforming "
        "information."
    )


# ============================================================
# PAGE - ML / AI RESULTS
# ============================================================

elif page == "ML / AI Results":

    st.title(
        "ML / AI Results"
    )

    st.caption(
        "Verified classification results from frozen evaluation "
        "protocols. No post-test model retuning is included."
    )


    # ========================================================
    # MODEL FAMILY EXPLANATION
    # ========================================================

    st.markdown(
        '<div class="section-kicker">Models Compared</div>',
        unsafe_allow_html=True,
    )

    m1, m2, m3 = st.columns(3)

    with m1:

        metric_card(
            "Model A",
            "MFCC + SVM",
            "Conventional acoustic ML baseline",
        )

        st.markdown(
            """
            Uses compact MFCC acoustic descriptors followed by
            a support-vector machine.

            This was the strongest model across the completed
            Qiandao classification tasks and DeepShip.
            """
        )

    with m2:

        metric_card(
            "Model B",
            "Log-Mel CNN",
            "Deep-learning time-frequency model",
        )

        st.markdown(
            """
            Uses Log-Mel time-frequency representations
            with a convolutional neural network.

            This allows the network to learn acoustic patterns
            directly from spectrogram-like input.
            """
        )

    with m3:

        metric_card(
            "Model C",
            "Acoustic Fusion",
            "CNN + engineered acoustic features",
        )

        st.markdown(
            """
            Combines learned CNN information with engineered
            spectral, broadband, narrowband, LOFAR-style and
            DEMON-style acoustic features.
            """
        )


    # ========================================================
    # FINAL RESULT SUMMARY
    # ========================================================

    st.markdown(
        '<div class="section-kicker">Final Verified Results</div>',
        unsafe_allow_html=True,
    )


    final_rows = [
        {
            "Task":
                "SpeedBoat",

            "Evaluation":
                "Frozen final test",

            "Winner":
                speedboat.get(
                    "winner",
                    "N/A",
                ),

            "Primary Macro-F1":
                speedboat.get(
                    "winner_macro_f1"
                ),
        },

        {
            "Task":
                "UUV",

            "Evaluation":
                "Frozen final test",

            "Winner":
                uuv.get(
                    "winner",
                    "N/A",
                ),

            "Primary Macro-F1":
                uuv.get(
                    "winner_macro_f1"
                ),
        },

        {
            "Task":
                "Noise Target",

            "Evaluation":
                noise.get(
                    "evaluation_design",
                    "N/A",
                ),

            "Winner":
                noise.get(
                    "winner",
                    "N/A",
                ),

            "Primary Macro-F1":
                noise.get(
                    "winner_macro_f1"
                ),
        },

        {
            "Task":
                "DeepShip",

            "Evaluation":
                "3-fold parent-source-held-out OOF",

            "Winner":
                deepship.get(
                    "winner",
                    "N/A",
                ),

            "Primary Macro-F1":
                deepship.get(
                    "winner_segment_macro_f1"
                ),
        },

        {
            "Task":
                "ShipsEar restricted 3-class",

            "Evaluation":
                "2-fold natural-group-held-out exploratory ML",

            "Winner":
                (
                    shipsear
                    .get(
                        "restricted_ml",
                        {}
                    )
                    .get(
                        "model",
                        "N/A",
                    )
                ),

            "Primary Macro-F1":
                (
                    shipsear
                    .get(
                        "restricted_ml",
                        {}
                    )
                    .get(
                        "segment_macro_f1"
                    )
                ),
        },
    ]


    final_df = pd.DataFrame(
        final_rows
    )


    final_df[
        "Primary Macro-F1"
    ] = final_df[
        "Primary Macro-F1"
    ].apply(
        lambda x:
            round(
                float(x),
                3,
            )
            if pd.notna(x)
            else ""
    )


    st.dataframe(
        final_df,
        use_container_width=True,
        hide_index=True,
    )


    st.info(
        "Macro-F1 values should not be interpreted as a direct "
        "competition between datasets because each task has different "
        "classes, sample structures and evaluation protocols."
    )


    # ========================================================
    # DATASET TABS
    # ========================================================

    st.markdown(
        '<div class="section-kicker">Dataset-Specific Model Evidence</div>',
        unsafe_allow_html=True,
    )


    tab_speed, tab_uuv, tab_noise, tab_deep, tab_ship = st.tabs(
        [
            "SpeedBoat",
            "UUV",
            "Noise Target",
            "DeepShip",
            "ShipsEar",
        ]
    )


    # ========================================================
    # SPEEDBOAT
    # ========================================================

    with tab_speed:

        st.markdown(
            "## SpeedBoat — Target vs Other"
        )

        speed_models = speedboat.get(
            "models",
            {}
        )

        speed_rows = []

        for model_id in [
            "A",
            "B",
            "C",
        ]:

            model_data = speed_models.get(
                model_id,
                {}
            )

            speed_rows.append(
                {
                    "Model":
                        model_data.get(
                            "model",
                            model_id,
                        ),

                    "Accuracy":
                        model_data.get(
                            "accuracy"
                        ),

                    "Balanced Accuracy":
                        model_data.get(
                            "balanced_accuracy"
                        ),

                    "Macro-F1":
                        model_data.get(
                            "macro_f1"
                        ),

                    "Target Recall":
                        model_data.get(
                            "target_recall"
                        ),
                }
            )


        speed_df = pd.DataFrame(
            speed_rows
        )


        st.dataframe(
            speed_df.style.format(
                {
                    "Accuracy": "{:.3f}",
                    "Balanced Accuracy": "{:.3f}",
                    "Macro-F1": "{:.3f}",
                    "Target Recall": "{:.3f}",
                }
            ),
            use_container_width=True,
            hide_index=True,
        )


        fig_speed = go.Figure()

        fig_speed.add_trace(
            go.Bar(
                x=speed_df[
                    "Model"
                ],
                y=speed_df[
                    "Macro-F1"
                ],
                name="Macro-F1",
            )
        )

        fig_speed.update_layout(
            title="SpeedBoat Final-Test Macro-F1",
            yaxis_title="Macro-F1",
            xaxis_title="",
            height=430,
        )

        st.plotly_chart(
            fig_speed,
            use_container_width=True,
        )


        st.success(
            f"Winner: {speedboat.get('winner', 'N/A')} — "
            f"Macro-F1 = {speedboat.get('winner_macro_f1', 0):.3f}"
        )


        st.markdown(
            """
            **Interpretation:**  
            The simpler MFCC + SVM model generalized better
            than both the Log-Mel CNN and the acoustic-fusion model
            on the frozen final test.
            """
        )


    # ========================================================
    # UUV
    # ========================================================

    with tab_uuv:

        st.markdown(
            "## UUV — Target vs Other"
        )

        uuv_models = uuv.get(
            "models",
            {}
        )

        uuv_rows = []

        for model_id in [
            "A",
            "B",
            "C",
        ]:

            model_data = uuv_models.get(
                model_id,
                {}
            )

            uuv_rows.append(
                {
                    "Model":
                        model_data.get(
                            "model",
                            model_id,
                        ),

                    "Accuracy":
                        model_data.get(
                            "accuracy"
                        ),

                    "Balanced Accuracy":
                        model_data.get(
                            "balanced_accuracy"
                        ),

                    "Macro-F1":
                        model_data.get(
                            "macro_f1"
                        ),

                    "Target Recall":
                        model_data.get(
                            "target_recall"
                        ),
                }
            )


        uuv_df = pd.DataFrame(
            uuv_rows
        )


        st.dataframe(
            uuv_df.style.format(
                {
                    "Accuracy": "{:.3f}",
                    "Balanced Accuracy": "{:.3f}",
                    "Macro-F1": "{:.3f}",
                    "Target Recall": "{:.3f}",
                }
            ),
            use_container_width=True,
            hide_index=True,
        )


        fig_uuv = go.Figure()

        fig_uuv.add_trace(
            go.Bar(
                x=uuv_df[
                    "Model"
                ],
                y=uuv_df[
                    "Macro-F1"
                ],
                name="Macro-F1",
            )
        )

        fig_uuv.update_layout(
            title="UUV Final-Test Macro-F1",
            yaxis_title="Macro-F1",
            xaxis_title="",
            height=430,
        )

        st.plotly_chart(
            fig_uuv,
            use_container_width=True,
        )


        st.success(
            f"Winner: {uuv.get('winner', 'N/A')} — "
            f"Macro-F1 = {uuv.get('winner_macro_f1', 0):.3f}"
        )


        st.markdown(
            """
            **Interpretation:**  
            Model A again produced the strongest final-test
            Macro-F1. Models B and C achieved high Other-class
            recall but lower target recall.
            """
        )


    # ========================================================
    # NOISE TARGET
    # ========================================================

    with tab_noise:

        st.markdown(
            "## Noise Target — Target Present vs Background"
        )


        noise_models = noise.get(
            "models",
            {}
        )


        noise_rows = []

        for model_id in [
            "A",
            "B",
            "C",
        ]:

            model_data = noise_models.get(
                model_id,
                {}
            )

            noise_rows.append(
                {
                    "Model":
                        f"Model {model_id}",

                    "Accuracy":
                        model_data.get(
                            "accuracy"
                        ),

                    "Balanced Accuracy":
                        model_data.get(
                            "balanced_accuracy"
                        ),

                    "Macro-F1":
                        model_data.get(
                            "macro_f1"
                        ),

                    "Background Recall":
                        model_data.get(
                            "background_recall"
                        ),

                    "Target Recall":
                        model_data.get(
                            "target_recall"
                        ),
                }
            )


        noise_df = pd.DataFrame(
            noise_rows
        )


        st.dataframe(
            noise_df.style.format(
                {
                    "Accuracy": "{:.3f}",
                    "Balanced Accuracy": "{:.3f}",
                    "Macro-F1": "{:.3f}",
                    "Background Recall": "{:.3f}",
                    "Target Recall": "{:.3f}",
                }
            ),
            use_container_width=True,
            hide_index=True,
        )


        fig_noise = go.Figure()

        fig_noise.add_trace(
            go.Bar(
                x=noise_df[
                    "Model"
                ],
                y=noise_df[
                    "Macro-F1"
                ],
                name="Macro-F1",
            )
        )

        fig_noise.update_layout(
            title="Noise Target Two-Fold OOF Macro-F1",
            yaxis_title="Macro-F1",
            xaxis_title="",
            height=430,
        )

        st.plotly_chart(
            fig_noise,
            use_container_width=True,
        )


        st.success(
            f"Winner: {noise.get('winner', 'N/A')} — "
            f"Macro-F1 = {noise.get('winner_macro_f1', 0):.3f}"
        )


        st.warning(
            "Only two independent background sessions were available. "
            "The pooled result is useful, but per-fold variation remains "
            "important evidence of background/domain sensitivity."
        )


    # ========================================================
    # DEEPSHIP
    # ========================================================

    with tab_deep:

        st.markdown(
            "## DeepShip — Four-Class Vessel Classification"
        )


        deep_models = deepship.get(
            "models",
            {}
        )


        deep_rows = []

        for model_id in [
            "A",
            "B",
            "C",
        ]:

            model_data = deep_models.get(
                model_id,
                {}
            )

            deep_rows.append(
                {
                    "Model":
                        (
                            f"Model {model_id} - "
                            f"{model_data.get('model_name', '')}"
                        ),

                    "Segment Macro-F1":
                        model_data.get(
                            "segment_macro_f1"
                        ),

                    "Segment Balanced Accuracy":
                        model_data.get(
                            "segment_balanced_accuracy"
                        ),

                    "Source Macro-F1":
                        model_data.get(
                            "source_macro_f1"
                        ),

                    "Source Balanced Accuracy":
                        model_data.get(
                            "source_balanced_accuracy"
                        ),
                }
            )


        deep_df = pd.DataFrame(
            deep_rows
        )


        st.dataframe(
            deep_df.style.format(
                {
                    "Segment Macro-F1": "{:.3f}",
                    "Segment Balanced Accuracy": "{:.3f}",
                    "Source Macro-F1": "{:.3f}",
                    "Source Balanced Accuracy": "{:.3f}",
                }
            ),
            use_container_width=True,
            hide_index=True,
        )


        fig_deep = go.Figure()

        fig_deep.add_trace(
            go.Bar(
                x=deep_df[
                    "Model"
                ],
                y=deep_df[
                    "Segment Macro-F1"
                ],
                name="Segment Macro-F1",
            )
        )

        fig_deep.add_trace(
            go.Bar(
                x=deep_df[
                    "Model"
                ],
                y=deep_df[
                    "Source Macro-F1"
                ],
                name="Source Macro-F1",
            )
        )

        fig_deep.update_layout(
            title="DeepShip Held-Out Performance",
            barmode="group",
            yaxis_title="Macro-F1",
            xaxis_title="",
            height=470,
        )

        st.plotly_chart(
            fig_deep,
            use_container_width=True,
        )


        d1, d2 = st.columns(2)

        with d1:

            metric_card(
                "Winner Segment Macro-F1",
                f"{deepship.get('winner_segment_macro_f1', 0):.3f}",
                deepship.get(
                    "winner",
                    "N/A",
                ),
            )

        with d2:

            metric_card(
                "Winner Source Macro-F1",
                f"{deepship.get('winner_source_macro_f1', 0):.3f}",
                "Majority-vote source-level result",
            )


        st.markdown(
            """
            **Key finding:**  
            Model C improved substantially over the plain Log-Mel CNN,
            showing that engineered acoustic features added complementary
            information.

            However, Model C still did not outperform Model A on the
            predefined primary held-out metric.
            """
        )


        st.warning(
            "DeepShip showed substantial source/domain variability. "
            "Tug conclusions are especially uncertain because only "
            "three independent Tug parent recordings were available."
        )


    # ========================================================
    # SHIPSEAR
    # ========================================================

    with tab_ship:

        st.markdown(
            "## ShipsEar — Restricted Exploratory ML"
        )


        restricted = shipsear.get(
            "restricted_ml",
            {}
        )


        s1, s2, s3, s4 = st.columns(4)


        with s1:

            metric_card(
                "Classes",
                "3",
                "class_0 • class_1 • class_3",
            )


        with s2:

            metric_card(
                "Segments",
                f"{restricted.get('segments', 0):,}",
                "Restricted exploratory dataset",
            )


        with s3:

            metric_card(
                "Segment Macro-F1",
                f"{restricted.get('segment_macro_f1', 0):.3f}",
                "Pooled outer held-out segments",
            )


        with s4:

            metric_card(
                "Group Macro-F1",
                f"{restricted.get('group_macro_f1', 0):.3f}",
                "Natural-group majority vote",
            )


        st.markdown(
            """
            The restricted experiment used a fixed acoustic-feature
            RBF-SVM and natural provenance groups as the train/test
            separation unit.

            **Important class-level behavior:**

            - class_1 generalized strongly at group level
            - class_3 generalized strongly at group level
            - class_0 showed substantially weaker group-level generalization
            """
        )


        st.warning(
            "This is not a full ShipsEar five-class classifier. "
            "class_2 and class_4 each had only one natural provenance "
            "group and therefore could not support a defensible "
            "within-class source-held-out experiment."
        )


    # ========================================================
    # CROSS-TASK TAKEAWAY
    # ========================================================

    st.markdown(
        '<div class="section-kicker">Overall ML / AI Finding</div>',
        unsafe_allow_html=True,
    )


    st.success(
        "The experiments demonstrate that useful underwater acoustic "
        "classification is achievable, but model performance depends "
        "strongly on dataset structure and source variability. "
        "The simplest model family — MFCC + SVM — provided the strongest "
        "locked result across the completed Qiandao tasks and DeepShip."
    )


    st.info(
        "Model complexity alone should not be treated as evidence of "
        "better operational generalization. Held-out source/session "
        "performance is more important than architecture complexity."
    )


# ============================================================
# PAGE - SCIENTIFIC VALIDATION
# ============================================================

elif page == "Future Operational System":

    st.title(
        "Future Operational System"
    )

    st.caption(
        "How the completed research can be extended from an offline "
        "classification study into a future operational acoustic-AI system."
    )


    # ========================================================
    # CURRENT POSITION
    # ========================================================

    st.markdown(
        '<div class="section-kicker">Where the project stands today</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        The current project has established the **research foundation**:

        - underwater audio can be systematically processed
        - Spectrum, broadband, narrowband, LOFAR-style and DEMON-style
          information can be extracted
        - ML/AI models can classify several available acoustic tasks
        - source/session-aware validation can be applied
        - model limitations can be separated from genuine evidence

        The next stage would convert this research pipeline into a
        continuously operating system.
        """
    )


    current_1, current_2, current_3 = st.columns(3)

    with current_1:

        metric_card(
            "Current Stage",
            "Research",
            "Offline acoustic analysis and validated ML experiments",
        )

    with current_2:

        metric_card(
            "Next Stage",
            "Prototype",
            "Live audio ingestion and automatic inference",
        )

    with current_3:

        metric_card(
            "Long-Term Stage",
            "Operational",
            "Detection, classification, localization and tracking",
        )


    # ========================================================
    # FUTURE PIPELINE
    # ========================================================

    st.markdown(
        '<div class="section-kicker">Future End-to-End Architecture</div>',
        unsafe_allow_html=True,
    )

    future_pipeline = (
        '<div class="pipeline">'
        '<strong>1. Hydrophone / Sonar Acoustic Input</strong><br>'
        'Continuous underwater acoustic stream'
        '<br><br>↓<br><br>'
        '<strong>2. Signal Conditioning</strong><br>'
        'Filtering • resampling • segmentation • quality checks'
        '<br><br>↓<br><br>'
        '<strong>3. Contact Detection</strong><br>'
        'Identify time regions containing meaningful acoustic activity'
        '<br><br>↓<br><br>'
        '<strong>4. Acoustic Analysis</strong><br>'
        'Spectrum • STFT • Broadband • Narrowband • LOFAR • DEMON'
        '<br><br>↓<br><br>'
        '<strong>5. AI / ML Classification</strong><br>'
        'MFCC / Log-Mel / engineered features → trained classifier'
        '<br><br>↓<br><br>'
        '<strong>6. Confidence &amp; Decision Logic</strong><br>'
        'Predicted class • confidence • uncertainty • rejection threshold'
        '<br><br>↓<br><br>'
        '<strong>7. Operator Dashboard</strong><br>'
        'Contact type • acoustic evidence • history • alerts'
        '<br><br>↓<br><br>'
        '<strong>8. Future Multi-Hydrophone Extension</strong><br>'
        'Beamforming • direction of arrival • localization • tracking'
        '</div>'
    )

    st.markdown(
        future_pipeline,
        unsafe_allow_html=True,
    )


    # ========================================================
    # CURRENT VS FUTURE
    # ========================================================

    st.markdown(
        '<div class="section-kicker">Current Capability vs Future Capability</div>',
        unsafe_allow_html=True,
    )

    capability_rows = [
        {
            "Capability":
                "Acoustic feature extraction",

            "Current Project":
                "Implemented",

            "Future System":
                "Real-time / continuous",
        },
        {
            "Capability":
                "Spectrum / STFT analysis",

            "Current Project":
                "Implemented",

            "Future System":
                "Live visualization",
        },
        {
            "Capability":
                "Broadband / Narrowband analysis",

            "Current Project":
                "Implemented",

            "Future System":
                "Automatic contact descriptors",
        },
        {
            "Capability":
                "LOFAR-style analysis",

            "Current Project":
                "Implemented",

            "Future System":
                "Continuous tonal monitoring",
        },
        {
            "Capability":
                "DEMON-style analysis",

            "Current Project":
                "Implemented",

            "Future System":
                "Continuous modulation monitoring",
        },
        {
            "Capability":
                "ML / AI classification",

            "Current Project":
                "Offline validated experiments",

            "Future System":
                "Real-time inference",
        },
        {
            "Capability":
                "Confidence / uncertainty handling",

            "Current Project":
                "Limited",

            "Future System":
                "Required",
        },
        {
            "Capability":
                "Direction of Arrival",

            "Current Project":
                "Not supported by mono data",

            "Future System":
                "Possible with synchronized array",
        },
        {
            "Capability":
                "Beamforming",

            "Current Project":
                "Not implemented",

            "Future System":
                "Possible with array geometry",
        },
        {
            "Capability":
                "Tracking",

            "Current Project":
                "Not implemented",

            "Future System":
                "Possible after detection + localization",
        },
    ]

    st.dataframe(
        pd.DataFrame(
            capability_rows
        ),
        use_container_width=True,
        hide_index=True,
    )


    # ========================================================
    # PRODUCT MODULES
    # ========================================================

    st.markdown(
        '<div class="section-kicker">Possible Product Modules</div>',
        unsafe_allow_html=True,
    )

    module_1, module_2, module_3 = st.columns(3)

    with module_1:

        metric_card(
            "Module 1",
            "Acoustic Engine",
            "Signal conditioning, Spectrum, LOFAR, DEMON and feature extraction",
        )

        st.markdown(
            """
            This module would continuously receive audio and convert it
            into the same types of acoustic evidence already investigated
            in the research project.
            """
        )

    with module_2:

        metric_card(
            "Module 2",
            "AI Classifier",
            "Detection, class prediction and confidence estimation",
        )

        st.markdown(
            """
            The classifier would use validated representations such as
            MFCC, Log-Mel and engineered acoustic features to assign a
            contact category.
            """
        )

    with module_3:

        metric_card(
            "Module 3",
            "Operator UI",
            "Contact display, evidence, history and alerts",
        )

        st.markdown(
            """
            The operator interface would present the result in a form
            suitable for decision support rather than exposing raw
            model files or Python outputs.
            """
        )


    # ========================================================
    # OPERATOR VIEW
    # ========================================================

    st.markdown(
        '<div class="section-kicker">What an operator could eventually see</div>',
        unsafe_allow_html=True,
    )

    operator_rows = [
        {
            "Display":
                "Detected Contact",

            "Example Information":
                "Contact detected at current time window",
        },
        {
            "Display":
                "Predicted Class",

            "Example Information":
                "Vessel / target category predicted by AI",
        },
        {
            "Display":
                "Confidence",

            "Example Information":
                "Model confidence or calibrated probability",
        },
        {
            "Display":
                "Spectrum",

            "Example Information":
                "Current frequency-energy structure",
        },
        {
            "Display":
                "LOFAR",

            "Example Information":
                "Stable low-frequency tonal lines",
        },
        {
            "Display":
                "DEMON",

            "Example Information":
                "Envelope-modulation candidates",
        },
        {
            "Display":
                "History",

            "Example Information":
                "Previous detections and classification trend",
        },
        {
            "Display":
                "Future Bearing / Track",

            "Example Information":
                "Available only after array-based localization is added",
        },
    ]

    st.dataframe(
        pd.DataFrame(
            operator_rows
        ),
        use_container_width=True,
        hide_index=True,
    )


    # ========================================================
    # DEVELOPMENT PHASES
    # ========================================================

    st.markdown(
        '<div class="section-kicker">Recommended Development Path</div>',
        unsafe_allow_html=True,
    )

    phase1, phase2, phase3, phase4 = st.tabs(
        [
            "Phase 1",
            "Phase 2",
            "Phase 3",
            "Phase 4",
        ]
    )


    with phase1:

        st.markdown(
            "### Phase 1 — Research Consolidation"
        )

        st.success(
            "Current project stage — substantially completed."
        )

        st.markdown(
            """
            - dataset and provenance audit
            - acoustic characterization
            - ML/AI experiments
            - scientific validation
            - reproducible frozen results
            - supervisor dashboard and technical report
            """
        )


    with phase2:

        st.markdown(
            "### Phase 2 — Real-Time Software Prototype"
        )

        st.markdown(
            """
            Develop a local application capable of:

            - reading microphone / hydrophone input
            - segmenting incoming audio
            - generating live acoustic features
            - running a frozen classifier
            - displaying class and confidence
            - saving detection history
            """
        )

        st.info(
            "This phase can begin without changing the underlying "
            "scientific conclusions of the completed experiments."
        )


    with phase3:

        st.markdown(
            "### Phase 3 — Field Validation"
        )

        st.markdown(
            """
            The system should then be evaluated on new recordings collected
            under different operational conditions:

            - different locations
            - different sea states
            - different ranges
            - different sensors
            - unseen vessels / targets
            - changing background noise
            """
        )

        st.warning(
            "This stage is essential before claiming operational "
            "generalization."
        )


    with phase4:

        st.markdown(
            "### Phase 4 — Spatial / Tracking Extension"
        )

        st.markdown(
            """
            With synchronized multi-hydrophone array data and known sensor
            geometry, the system could be extended to investigate:

            - beamforming
            - direction-of-arrival estimation
            - MUSIC / MVDR or related array processing
            - localization
            - multi-contact tracking
            """
        )

        st.warning(
            "These capabilities are future extensions. "
            "They have not been demonstrated by the current mono datasets."
        )


    # ========================================================
    # RESEARCH EXTENSIONS
    # ========================================================

    st.markdown(
        '<div class="section-kicker">How the ML research can be extended</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        Future research can improve the classification layer through:

        - larger numbers of independent recording sources
        - stronger cross-location and cross-sensor evaluation
        - open-set or unknown-contact recognition
        - confidence calibration
        - self-supervised acoustic representations
        - transformer-based time-frequency models
        - longer-duration temporal context
        - multimodal fusion with environmental or platform information
        - continual learning under carefully controlled validation
        """
    )


    # ========================================================
    # IMPORTANT PRODUCT DISTINCTION
    # ========================================================

    st.markdown(
        '<div class="section-kicker">Research result vs operational product</div>',
        unsafe_allow_html=True,
    )

    left_product, right_product = st.columns(
        2,
        gap="large",
    )


    with left_product:

        st.markdown(
            "### What we have now"
        )

        st.markdown(
            """
            A reproducible research prototype demonstrating:

            - acoustic analysis
            - ML/AI feasibility
            - controlled evaluation
            - dataset limitations
            - candidate system architecture
            """
        )


    with right_product:

        st.markdown(
            "### What a deployable product still needs"
        )

        st.markdown(
            """
            - live sensor interface
            - real-time inference service
            - calibrated confidence thresholds
            - unknown-contact handling
            - field validation
            - reliability / latency testing
            - system security and logging
            - operator requirements
            - array hardware for spatial processing
            """
        )


    # ========================================================
    # FINAL MESSAGE
    # ========================================================

    st.markdown(
        '<div class="section-kicker">Future System Takeaway</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        dedent(
            """
            <div class="finding">

            <strong>
            The present work should be viewed as the acoustic-AI
            research foundation of a larger operational system.
            </strong>

            It establishes how underwater sound can be characterized,
            how classification models can be evaluated and where the
            current data limits the claim.

            The natural next step is a real-time prototype, followed by
            independent field validation and, when synchronized array
            data become available, spatial localization and tracking.

            </div>
            """
        ),
        unsafe_allow_html=True,
    )


    # ========================================================
    # CORE PRINCIPLE
    # ========================================================

    st.markdown(
        '<div class="section-kicker">Core Scientific Principle</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        dedent(
            """
            <div class="research-box">

            <strong>
            A model should be tested on genuinely unseen sources,
            not simply on different five-second pieces from a source
            it has already encountered during training.
            </strong>

            <br><br>

            This principle guided the final evaluation design across
            the project.

            </div>
            """
        ),
        unsafe_allow_html=True,
    )


    # ========================================================
    # LEAKAGE EXPLANATION
    # ========================================================

    st.markdown(
        '<div class="section-kicker">What is data leakage?</div>',
        unsafe_allow_html=True,
    )

    left, right = st.columns(
        2,
        gap="large",
    )


    with left:

        st.markdown(
            "### Unsafe example"
        )

        st.markdown(
            """
            Suppose one long ship recording is divided into many
            five-second clips.

            If some clips enter **training** and other clips from the
            same original recording enter **testing**, the model may learn
            recording-specific characteristics rather than a truly
            general vessel pattern.

            The final score can then look stronger than the true
            unseen-source performance.
            """
        )

        st.error(
            "Different files do not automatically mean independent data."
        )


    with right:

        st.markdown(
            "### Safer evaluation"
        )

        st.markdown(
            """
            Wherever the data supported it, the project separated
            complete:

            - parent recordings
            - source components
            - background sessions
            - provenance groups

            between training and testing.
            """
        )

        st.success(
            "The independence unit was chosen from the dataset structure, "
            "not simply from the number of WAV files."
        )


    # ========================================================
    # DATASET-SPECIFIC VALIDATION
    # ========================================================

    st.markdown(
        '<div class="section-kicker">How this affected each dataset</div>',
        unsafe_allow_html=True,
    )


    tab_q, tab_d, tab_s, tab_ds = st.tabs(
        [
            "QiandaoEar22",
            "DeepShip",
            "ShipsEar",
            "DS3500",
        ]
    )


    # ========================================================
    # QIANDAO
    # ========================================================

    with tab_q:

        st.markdown(
            "## QiandaoEar22"
        )

        st.markdown(
            """
            The completed Qiandao tasks used frozen evaluation data
            after model selection.

            **SpeedBoat**
            used an untouched final test.

            **UUV**
            used an untouched final test after Models A/B/C were frozen.

            **Noise Target**
            required a different approach because the available
            background data came from only two independent sessions.
            """
        )

        st.markdown(
            f"""
            Noise Target therefore used:

            **{noise.get('evaluation_design', 'Two-fold held-out evaluation')}**

            Total unique out-of-fold observations:
            **{noise.get('total_unique_oof_samples', 0):,}**
            """
        )

        st.warning(
            "Because only two independent background sessions existed, "
            "the pooled Noise Target result must be interpreted together "
            "with the per-fold variation."
        )


    # ========================================================
    # DEEPSHIP
    # ========================================================

    with tab_d:

        st.markdown(
            "## DeepShip"
        )

        st.markdown(
            f"""
            DeepShip contained **{deepship.get('independent_parent_sources', 0)}**
            independent parent recordings but **1,118 five-second
            observations**.

            Therefore, the five-second clips were not treated as
            1,118 independent acoustic sources.
            """
        )

        st.success(
            "A 3-fold parent-source-held-out outer evaluation was used."
        )

        st.markdown(
            """
            This means that the parent source used in an outer test fold
            was not also present in the corresponding training data.

            The project reported both:

            - segment-level performance
            - source-level majority-vote performance

            to avoid relying only on the large number of short clips.
            """
        )

        st.warning(
            "Tug results remain particularly uncertain because only "
            "three independent Tug parent recordings were available."
        )


    # ========================================================
    # SHIPSEAR
    # ========================================================

    with tab_s:

        st.markdown(
            "## ShipsEar"
        )

        st.markdown(
            f"""
            ShipsEar contained:

            - **{shipsear.get('available_segments', 0):,}** five-second segments
            - only **{shipsear.get('natural_provenance_groups', 0)}**
              natural provenance groups
            """
        )

        st.markdown(
            """
            The supplied train/test split was not used for an
            independent-generalization claim because the natural
            provenance groups crossed the original file-level split.
            """
        )

        st.markdown(
            "### Why full five-class ML was not claimed"
        )

        st.warning(
            shipsear.get(
                "full_five_class_ml_reason",
                (
                    "Two classes did not contain enough independent "
                    "provenance groups for a defensible held-out test."
                ),
            )
        )

        st.markdown(
            """
            If a class contains only one natural source group, then:

            - putting that group in training leaves no independent group
              from that class for testing;
            - putting it in testing leaves no same-class source for training.

            Therefore, forcing a five-class source-held-out experiment
            would create a scientifically weak design.
            """
        )

        st.success(
            "Decision: retain all five classes for acoustic "
            "characterization, but restrict exploratory ML to classes "
            "with more than one natural provenance group."
        )


        restricted = shipsear.get(
            "restricted_ml",
            {}
        )

        st.markdown(
            f"""
            Restricted exploratory experiment:

            - classes: **{", ".join(restricted.get('classes', []))}**
            - segments: **{restricted.get('segments', 0):,}**
            - natural groups: **{restricted.get('natural_groups', 0)}**
            - outer folds: **{restricted.get('outer_folds', 0)}**
            """
        )


    # ========================================================
    # DS3500
    # ========================================================

    with tab_ds:

        st.markdown(
            "## DS3500"
        )

        st.markdown(
            """
            DS3500 was not automatically accepted as another independent
            validation dataset.

            Its relationship with ShipsEar was first investigated at both
            metadata and audio-content level.
            """
        )

        evidence = ds3500.get(
            "relationship_evidence",
            {}
        )

        d1, d2, d3 = st.columns(3)

        with d1:

            metric_card(
                "Paired Records",
                f"{ds3500.get('paired_records', 0):,}",
                "One-to-one relationship",
            )

        with d2:

            metric_card(
                "Exact PCM Matches",
                str(
                    evidence.get(
                        "exact_pcm_matches",
                        0,
                    )
                ),
                "Not exact PCM duplicates",
            )

        with d3:

            metric_card(
                "Spectral Similarity",
                f"{evidence.get('median_magnitude_spectrum_cosine_similarity', 0):.3f}",
                "Median paired spectral cosine",
            )


        st.markdown(
            """
            The audit found the same:

            - pair identifiers
            - filenames
            - class assignments
            - provenance groups
            - original split assignments

            across all paired records.
            """
        )

        st.info(
            "The audio files were not byte-identical or PCM-identical, "
            "but the one-to-one metadata relationship means DS3500 cannot "
            "be counted as an independent second source of generalization "
            "evidence."
        )

        st.warning(
            "Final decision: DS3500 is research-only and must not be "
            "presented as an independent benchmark."
        )


    # ========================================================
    # FROZEN RESULTS
    # ========================================================

    st.markdown(
        '<div class="section-kicker">Why the results were frozen</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        Once final-test or outer-test results were revealed, those results
        were not used for further model tuning.

        This prevents the final evaluation set from gradually becoming
        another validation set.
        """
    )


    v1, v2, v3 = st.columns(3)


    with v1:

        metric_card(
            "Expected Locks",
            "16",
            "Final experimental/result status locks",
        )


    with v2:

        metric_card(
            "Missing Locks",
            "0",
            "Master project audit",
        )


    with v3:

        metric_card(
            "Unexpected Locks",
            "0",
            "Master project audit",
        )


    st.success(
        "A master verified-results source was created so the dashboard, "
        "final report and presentation can use the same frozen numbers."
    )


    # ========================================================
    # WHAT CAN / CANNOT BE CLAIMED
    # ========================================================

    st.markdown(
        '<div class="section-kicker">What the project can and cannot claim</div>',
        unsafe_allow_html=True,
    )


    claim_left, claim_right = st.columns(
        2,
        gap="large",
    )


    with claim_left:

        st.markdown(
            "### Supported by the current work"
        )

        st.markdown(
            """
            - useful acoustic patterns exist in the available data
            - ML/AI can classify several available target tasks
            - source/session structure strongly affects generalization
            - engineered acoustic features can add useful information
            - a reproducible evaluation workflow can be constructed
            """
        )


    with claim_right:

        st.markdown(
            "### Not established by the current work"
        )

        st.markdown(
            """
            - universal performance in arbitrary ocean environments
            - a full source-held-out five-class ShipsEar classifier
            - DS3500 as independent confirmation of ShipsEar
            - true direction-of-arrival estimation from current mono data
            - operational real-time naval deployment without further testing
            """
        )


    # ========================================================
    # FINAL VALIDATION MESSAGE
    # ========================================================

    st.markdown(
        '<div class="section-kicker">Scientific Takeaway</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        dedent(
            """
            <div class="finding">

            <strong>
            The scientific value of the project is not only the model scores.
            </strong>FV

            The work also identified where a model result could be defended,
            where the available data imposed a limitation, and where an
            apparently separate dataset should not be counted as independent
            evidence.

            </div>
            """
        ),
        unsafe_allow_html=True,
    )


# ============================================================
# PAGE - FUTURE OPERATIONAL SYSTEM
# ============================================================

elif page == "Future Operational System":

    st.title(
        "Future Operational System"
    )

    st.info(
        "This section will translate the research into a future "
        "hydrophone-to-AI operational architecture."
    )


# ============================================================
# PAGE - FINAL CONCLUSIONS
# ============================================================

elif page == "Final Conclusions":

    st.title(
        "Final Conclusions"
    )

    st.caption(
        "Final scientific interpretation of the underwater acoustic "
        "classification study and its future development path."
    )


    # ========================================================
    # FINAL ANSWER TO RESEARCH QUESTION
    # ========================================================

    st.markdown(
        '<div class="section-kicker">Final Answer to the Research Question</div>',
        unsafe_allow_html=True,
    )

    final_answer_html = (
        '<div class="research-box">'
        '<strong>'
        'Yes — the completed experiments demonstrate that '
        'ML/AI can classify useful patterns in underwater acoustic '
        'contacts within the available datasets and evaluation protocols.'
        '</strong>'
        '<br><br>'
        'However, the strength of classification depends strongly on '
        'the acoustic task, source variability, number of independent '
        'recordings and the scientific quality of the train/test split.'
        '<br><br>'
        'The present work therefore supports the feasibility of '
        'underwater acoustic classification, but it does not claim '
        'universal operational performance in every ocean environment.'
        '</div>'
    )

    st.markdown(
        final_answer_html,
        unsafe_allow_html=True,
    )


    # ========================================================
    # FINAL RESULT SNAPSHOT
    # ========================================================

    st.markdown(
        '<div class="section-kicker">Final Verified Evidence</div>',
        unsafe_allow_html=True,
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        metric_card(
            "SpeedBoat Macro-F1",
            f"{speedboat.get('winner_macro_f1', 0):.3f}",
            speedboat.get(
                "winner",
                "N/A",
            ),
        )

    with c2:

        metric_card(
            "UUV Macro-F1",
            f"{uuv.get('winner_macro_f1', 0):.3f}",
            uuv.get(
                "winner",
                "N/A",
            ),
        )

    with c3:

        metric_card(
            "Noise Target Macro-F1",
            f"{noise.get('winner_macro_f1', 0):.3f}",
            noise.get(
                "winner",
                "N/A",
            ),
        )

    with c4:

        metric_card(
            "DeepShip Macro-F1",
            f"{deepship.get('winner_segment_macro_f1', 0):.3f}",
            deepship.get(
                "winner",
                "N/A",
            ),
        )


    st.caption(
        "These scores come from different tasks and evaluation protocols "
        "and should not be interpreted as a direct cross-dataset ranking."
    )


    # ========================================================
    # WHAT WAS DEMONSTRATED
    # ========================================================

    st.markdown(
        '<div class="section-kicker">What the project demonstrated</div>',
        unsafe_allow_html=True,
    )

    left, right = st.columns(
        2,
        gap="large",
    )

    with left:

        st.markdown(
            "### Acoustic findings"
        )

        st.markdown(
            """
            The project demonstrated that underwater recordings contain
            measurable acoustic structure that can be represented using:

            - Spectrum and spectral-energy measures
            - Broadband frequency-energy distribution
            - Narrowband tonal information
            - LOFAR-style low-frequency tonal structure
            - DEMON-style envelope-modulation information
            - MFCC descriptors
            - Log-Mel time-frequency representations
            """
        )

    with right:

        st.markdown(
            "### ML / AI findings"
        )

        st.markdown(
            """
            The experiments demonstrated that:

            - several target-vs-other tasks can be classified
            - multiclass vessel classification is possible but harder
            - model complexity does not guarantee better generalization
            - source/session independence strongly affects measured performance
            - engineered acoustic features can add complementary information
            - conventional MFCC + SVM remained highly competitive
            """
        )


    # ========================================================
    # DATASET-BY-DATASET CONCLUSION
    # ========================================================

    st.markdown(
        '<div class="section-kicker">Dataset-by-Dataset Conclusion</div>',
        unsafe_allow_html=True,
    )

    tab_q, tab_d, tab_s, tab_ds = st.tabs(
        [
            "QiandaoEar22",
            "DeepShip",
            "ShipsEar",
            "DS3500",
        ]
    )


    with tab_q:

        st.markdown(
            "### QiandaoEar22"
        )

        st.markdown(
            f"""
            Three completed classification tasks produced useful
            held-out evidence.

            **SpeedBoat**
            - winner: **{speedboat.get('winner', 'N/A')}**
            - Macro-F1: **{speedboat.get('winner_macro_f1', 0):.3f}**

            **UUV**
            - winner: **{uuv.get('winner', 'N/A')}**
            - Macro-F1: **{uuv.get('winner_macro_f1', 0):.3f}**

            **Noise Target**
            - winner: **{noise.get('winner', 'N/A')}**
            - Macro-F1: **{noise.get('winner_macro_f1', 0):.3f}**
            """
        )

        st.success(
            "QiandaoEar22 provided the strongest overall proof-of-concept "
            "evidence for the feasibility of ML-based underwater acoustic "
            "target discrimination in this project."
        )


    with tab_d:

        st.markdown(
            "### DeepShip"
        )

        st.markdown(
            f"""
            DeepShip tested a more difficult four-class vessel problem
            under parent-source-held-out evaluation.

            Winner:
            **{deepship.get('winner', 'N/A')}**

            Segment Macro-F1:
            **{deepship.get('winner_segment_macro_f1', 0):.3f}**

            Source Macro-F1:
            **{deepship.get('winner_source_macro_f1', 0):.3f}**
            """
        )

        st.info(
            "The result demonstrates useful multiclass capability, "
            "but also shows that source/domain variability remains a "
            "major challenge for vessel classification."
        )


    with tab_s:

        st.markdown(
            "### ShipsEar"
        )

        restricted = shipsear.get(
            "restricted_ml",
            {}
        )

        st.markdown(
            f"""
            ShipsEar supported complete five-class acoustic
            characterization.

            A full five-class source-held-out ML claim was not made
            because class_2 and class_4 each contained only one natural
            provenance group.

            A restricted exploratory experiment using class_0,
            class_1 and class_3 produced:

            - segment Macro-F1:
              **{restricted.get('segment_macro_f1', 0):.3f}**
            - group Macro-F1:
              **{restricted.get('group_macro_f1', 0):.3f}**
            """
        )

        st.success(
            "The scientifically stronger decision was to limit the ML "
            "claim rather than force an invalid five-class experiment."
        )


    with tab_ds:

        st.markdown(
            "### DS3500"
        )

        evidence = ds3500.get(
            "relationship_evidence",
            {}
        )

        st.markdown(
            f"""
            The DS3500 audit identified **{ds3500.get('paired_records', 0):,}**
            one-to-one paired records with ShipsEar.

            Exact PCM matches:
            **{evidence.get('exact_pcm_matches', 0)}**

            Median magnitude-spectrum cosine similarity:
            **{evidence.get('median_magnitude_spectrum_cosine_similarity', 0):.3f}**
            """
        )

        st.warning(
            "DS3500 is therefore retained as a research-only paired "
            "counterpart and is not counted as an independent validation "
            "dataset."
        )


    # ========================================================
    # MODEL CONCLUSION
    # ========================================================

    st.markdown(
        '<div class="section-kicker">Final Model Conclusion</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        One of the clearest findings of the project is that **more complex
        AI models did not automatically generalize better**.

        Across the completed Qiandao tasks and DeepShip comparison,
        **Model A — MFCC + RBF-SVM** produced the strongest locked result.

        The CNN and acoustic-fusion approaches remain scientifically useful,
        particularly because they show how learned and engineered features
        behave, but complexity alone was not a substitute for robust
        generalization.
        """
    )

    st.success(
        "For the present datasets, a strong conventional acoustic-ML "
        "baseline remained the most reliable overall model family."
    )


    # ========================================================
    # WHAT HAS NOT BEEN DEMONSTRATED
    # ========================================================

    st.markdown(
        '<div class="section-kicker">What has not yet been demonstrated</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        The current project does **not** establish:

        - universal performance across arbitrary oceans and environments
        - reliable classification of every possible underwater contact
        - a scientifically valid five-class ShipsEar source-held-out classifier
        - DS3500 as an independent confirmation dataset
        - true source bearing or direction-of-arrival estimation
        - hydrophone-array beamforming
        - localization or multi-contact tracking
        - a field-certified real-time operational system
        """
    )

    st.info(
        "These are future research and engineering objectives, not failures "
        "of the present study."
    )


    # ========================================================
    # FUTURE PRIORITIES
    # ========================================================

    st.markdown(
        '<div class="section-kicker">Recommended Next Priorities</div>',
        unsafe_allow_html=True,
    )

    priority_rows = [
        {
            "Priority": "1",
            "Next Step": "Collect more independent field recordings",
            "Reason": "Improve source diversity and generalization evidence",
        },
        {
            "Priority": "2",
            "Next Step": "Build real-time acoustic ingestion prototype",
            "Reason": "Move from offline research to live inference",
        },
        {
            "Priority": "3",
            "Next Step": "Add confidence and unknown-contact handling",
            "Reason": "Operational systems should be able to reject uncertainty",
        },
        {
            "Priority": "4",
            "Next Step": "Cross-location / cross-sensor validation",
            "Reason": "Test robustness to environmental and hardware changes",
        },
        {
            "Priority": "5",
            "Next Step": "Acquire synchronized hydrophone-array data",
            "Reason": "Enable DOA, beamforming, localization and tracking",
        },
    ]

    st.dataframe(
        pd.DataFrame(
            priority_rows
        ),
        use_container_width=True,
        hide_index=True,
    )


    # ========================================================
    # RESEARCH CONTRIBUTION
    # ========================================================

    st.markdown(
        '<div class="section-kicker">Overall Research Contribution</div>',
        unsafe_allow_html=True,
    )

    contribution_html = (
        '<div class="finding">'
        '<strong>'
        'The project produced more than a set of classification scores.'
        '</strong>'
        '<br><br>'
        'It established a complete research chain from raw underwater '
        'audio, dataset auditing and acoustic characterization through '
        'ML/AI modeling, source-aware validation, frozen results and a '
        'future operational-system concept.'
        '<br><br>'
        'Equally important, the work identified where the available data '
        'supported a scientific claim and where the correct decision was '
        'to limit that claim.'
        '</div>'
    )

    st.markdown(
        contribution_html,
        unsafe_allow_html=True,
    )


    # ========================================================
    # FINAL SUPERVISOR MESSAGE
    # ========================================================

    st.markdown(
        '<div class="section-kicker">Final Supervisor Summary</div>',
        unsafe_allow_html=True,
    )

    st.success(
        "The research question has been answered positively at the "
        "proof-of-concept level: underwater acoustic contacts can be "
        "characterized and classified using ML/AI within controlled "
        "dataset-specific evaluation protocols."
    )

    st.info(
        "The strongest path forward is to preserve the current frozen "
        "research evidence, expand the number of genuinely independent "
        "field sources, build a real-time inference prototype, and later "
        "extend the system with synchronized hydrophone-array data for "
        "spatial processing."
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.markdown(
    """
    <div class="small-note">

    Underwater Acoustic AI Research •
    Supervisor Delivery Dashboard •
    Verified experimental evidence

    </div>
    """,
    unsafe_allow_html=True,
)