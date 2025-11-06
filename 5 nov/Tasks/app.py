import streamlit as st
import pandas as pd
import json
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os
from typing import List, Dict, Any

# Page configuration
st.set_page_config(
    page_title="AI Anomaly Detection System",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .anomaly-card {
        background-color: #fff3cd;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #ffc107;
        margin-bottom: 1rem;
    }
    .critical-card {
        background-color: #f8d7da;
        border-left: 4px solid #dc3545;
    }
    .success-card {
        background-color: #d4edda;
        border-left: 4px solid #28a745;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'results' not in st.session_state:
    st.session_state.results = None
if 'transactions' not in st.session_state:
    st.session_state.transactions = None


def load_csv_data(uploaded_file):
    """Load and process CSV data"""
    try:
        df = pd.read_csv(uploaded_file)
        st.success(f"✅ Loaded {len(df)} records from CSV")
        return df
    except Exception as e:
        st.error(f"❌ Error loading CSV: {e}")
        return None


def prepare_transactions(df: pd.DataFrame) -> List[Dict[str, Any]]:
    """Convert DataFrame to transaction format"""
    transactions = []
    for _, row in df.iterrows():
        transaction = {
            "transaction_id": str(row["Customer_ID"]),
            "customer_id": str(row["Customer_ID"]),
            "amount": row["Balance"],
            "date": None,
            "merchant": "Unknown",
            "card_number": "****" + str(row["Customer_ID"])[-4:],
            "credit_score": row["Credit_Score"],
            "transactions_last_month": row["Transactions_Last_Month"],
            "is_anomaly": row["Is_Anomaly"]
        }
        transactions.append(transaction)
    return transactions


def display_summary_metrics(summary: Dict):
    """Display summary metrics in cards"""
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("🔍 Total Detected", summary['total_detected'])
        st.metric("✅ Valid Anomalies", summary['valid_anomalies'])

    with col2:
        st.metric("❌ False Positives", summary['false_positives'])
        st.metric("👤 Human Review", summary['require_human_review'])

    with col3:
        st.metric("🤖 Automated Fixes", summary['automated_fixes'])
        st.metric("🔧 Manual Actions", summary['manual_actions'])


def create_severity_chart(anomalies: List[Dict]):
    """Create severity distribution chart"""
    if not anomalies:
        return None

    severity_counts = {}
    for anomaly in anomalies:
        severity = anomaly.get('severity', 'UNKNOWN')
        severity_counts[severity] = severity_counts.get(severity, 0) + 1

    fig = go.Figure(data=[
        go.Bar(
            x=list(severity_counts.keys()),
            y=list(severity_counts.values()),
            marker_color=['#28a745', '#ffc107', '#fd7e14', '#dc3545'][:len(severity_counts)]
        )
    ])

    fig.update_layout(
        title="Anomaly Severity Distribution",
        xaxis_title="Severity",
        yaxis_title="Count",
        height=400
    )

    return fig


def create_anomaly_type_chart(anomalies: List[Dict]):
    """Create anomaly type distribution chart"""
    if not anomalies:
        return None

    type_counts = {}
    for anomaly in anomalies:
        atype = anomaly.get('anomaly_type', 'UNKNOWN')
        type_counts[atype] = type_counts.get(atype, 0) + 1

    fig = px.pie(
        values=list(type_counts.values()),
        names=list(type_counts.keys()),
        title="Anomaly Type Distribution"
    )

    fig.update_layout(height=400)
    return fig


def display_anomaly_details(anomalies: List[Dict], validations: List[Dict]):
    """Display detailed anomaly information"""
    for i, anomaly in enumerate(anomalies):
        validation = validations[i] if i < len(validations) else None

        # Determine card style based on severity
        if anomaly.get('severity') == 'CRITICAL':
            card_class = "critical-card"
        elif validation and validation.get('is_valid_anomaly'):
            card_class = "anomaly-card"
        else:
            card_class = "success-card"

        with st.expander(
                f"🔍 Transaction {anomaly.get('transaction_id')} - {anomaly.get('anomaly_type')} ({anomaly.get('severity')})",
                expanded=(anomaly.get('severity') in ['CRITICAL', 'HIGH'])
        ):
            col1, col2 = st.columns(2)

            with col1:
                st.markdown("**Anomaly Details:**")
                st.write(f"**Type:** {anomaly.get('anomaly_type')}")
                st.write(f"**Severity:** {anomaly.get('severity')}")
                st.write(f"**Confidence:** {anomaly.get('confidence_score', 0):.2%}")
                st.write(f"**Description:** {anomaly.get('description')}")
                st.write(f"**Affected Fields:** {', '.join(anomaly.get('affected_fields', []))}")

            with col2:
                if validation:
                    st.markdown("**Validation Result:**")
                    status = "✅ Valid" if validation.get('is_valid_anomaly') else "❌ False Positive"
                    st.write(f"**Status:** {status}")
                    st.write(f"**Priority:** {validation.get('priority')}")
                    st.write(f"**Human Review:** {'Yes' if validation.get('requires_human_review') else 'No'}")
                    st.write(f"**Reason:** {validation.get('validation_reason')}")


def display_resolution_actions(resolutions: List[Dict]):
    """Display resolution actions"""
    st.subheader("🔧 Resolution Actions")

    for resolution in resolutions:
        with st.expander(f"Transaction {resolution.get('transaction_id')} - {resolution.get('action_type')}"):
            col1, col2 = st.columns(2)

            with col1:
                st.write(f"**Action Type:** {resolution.get('action_type')}")
                st.write(f"**Automated Fix:** {'Yes ✅' if resolution.get('automated_fix_possible') else 'No ❌'}")
                if resolution.get('workflow_trigger'):
                    st.write(f"**Workflow:** {resolution.get('workflow_trigger')}")

            with col2:
                st.write("**Suggested Fix:**")
                st.info(resolution.get('suggested_fix'))


# Main App
def main():
    # Header
    st.markdown('<h1 class="main-header">🔍 AI-Powered Anomaly Detection System</h1>', unsafe_allow_html=True)

    # Sidebar
    with st.sidebar:
        st.image("https://img.icons8.com/fluency/96/000000/artificial-intelligence.png", width=100)
        st.title("Control Panel")

        # API Key Input
        api_key = st.text_input("OpenRouter API Key", type="password",
                                value=os.getenv("OPENROUTER_API_KEY", ""))

        if api_key:
            os.environ["OPENROUTER_API_KEY"] = api_key
            st.success("✅ API Key Set")

        st.divider()

        # File Upload
        uploaded_file = st.file_uploader("Upload Banking Data (CSV)", type=['csv'])

        if uploaded_file:
            df = load_csv_data(uploaded_file)
            if df is not None:
                st.session_state.transactions = prepare_transactions(df)
                st.success(f"✅ Prepared {len(st.session_state.transactions)} transactions")

        st.divider()

        # Run Detection Button
        if st.button("🚀 Run Anomaly Detection", type="primary", use_container_width=True):
            if not api_key:
                st.error("❌ Please enter your API key")
            elif st.session_state.transactions is None:
                st.error("❌ Please upload a CSV file")
            else:
                with st.spinner("🔍 Analyzing transactions..."):
                    try:
                        # Import and run the detection system
                        from anomaly_detection import AnomalyDetectionOrchestrator, llm

                        orchestrator = AnomalyDetectionOrchestrator(llm)
                        results = orchestrator.process_transactions(st.session_state.transactions)
                        st.session_state.results = results
                        st.success("✅ Detection Complete!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Error: {e}")

        # Load Previous Results
        if st.button("📂 Load Previous Results", use_container_width=True):
            try:
                with open("anomaly_detection_results.json", "r") as f:
                    st.session_state.results = json.load(f)
                st.success("✅ Results Loaded!")
                st.rerun()
            except FileNotFoundError:
                st.error("❌ No previous results found")

        st.divider()

        # System Info
        st.markdown("### 📊 System Info")
        st.info("**Model:** Mistral Large\n\n**Agents:** Detection, Validation, Resolution")

    # Main Content Area
    if st.session_state.results is None:
        # Welcome Screen
        st.info("👋 Welcome! Please upload your banking data CSV and run the anomaly detection system.")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("### 🔍 Detection")
            st.write("AI-powered pattern recognition to identify anomalies in your data.")

        with col2:
            st.markdown("### ✓ Validation")
            st.write("Smart validation to confirm real anomalies and reduce false positives.")

        with col3:
            st.markdown("### 🔧 Resolution")
            st.write("Automated suggestions and workflows for resolving detected issues.")

    else:
        # Display Results
        results = st.session_state.results

        # Summary Section
        st.header("📊 Detection Summary")
        display_summary_metrics(results['summary'])

        st.divider()

        # Visualizations
        st.header("📈 Analytics")

        col1, col2 = st.columns(2)

        with col1:
            if results['anomalies_detected']:
                fig1 = create_severity_chart(results['anomalies_detected'])
                if fig1:
                    st.plotly_chart(fig1, use_container_width=True)

        with col2:
            if results['anomalies_detected']:
                fig2 = create_anomaly_type_chart(results['anomalies_detected'])
                if fig2:
                    st.plotly_chart(fig2, use_container_width=True)

        st.divider()

        # Detailed Results
        tab1, tab2, tab3 = st.tabs(["🔍 Detected Anomalies", "🔧 Resolutions", "📄 Raw Data"])

        with tab1:
            st.header("Detected Anomalies")
            if results['anomalies_detected']:
                display_anomaly_details(
                    results['anomalies_detected'],
                    results['validated_anomalies']
                )
            else:
                st.success("✅ No anomalies detected! All transactions appear normal.")

        with tab2:
            if results['resolution_actions']:
                display_resolution_actions(results['resolution_actions'])
            else:
                st.info("No resolution actions needed.")

        with tab3:
            st.subheader("Complete Results JSON")
            st.json(results)

            # Download button
            json_str = json.dumps(results, indent=2)
            st.download_button(
                label="📥 Download Results (JSON)",
                data=json_str,
                file_name=f"anomaly_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )


if __name__ == "__main__":
    main()