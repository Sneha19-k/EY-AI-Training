import os
import json
import pandas as pd
from datetime import datetime
from typing import List, Dict, Any, Optional

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("✅ Loaded environment variables from .env file")
except ImportError:
    print("⚠️  python-dotenv not installed. Install with: pip install python-dotenv")
    print("   Trying to use system environment variables...")

# Updated LangChain imports
try:
    from langchain_openai import ChatOpenAI
except ImportError:
    print("Installing required package: langchain-openai")
    os.system("pip install langchain-openai")
    from langchain_openai import ChatOpenAI

try:
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_core.messages import HumanMessage, SystemMessage
except ImportError:
    print("Installing required package: langchain-core")
    os.system("pip install langchain-core")
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_core.messages import HumanMessage, SystemMessage

from pydantic import BaseModel, Field

# ============================================================================
# Configuration
# ============================================================================

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_BASE_URL = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")

# Validate API key
if not OPENROUTER_API_KEY:
    print("❌ ERROR: OPENROUTER_API_KEY not found!")
    exit(1)

print(f"🔑 API Key loaded: {OPENROUTER_API_KEY[:10]}...{OPENROUTER_API_KEY[-4:]}")

# Initialize Mistral LLM via OpenRouter
llm = ChatOpenAI(
    model="mistralai/mistral-large",
    api_key=OPENROUTER_API_KEY,
    base_url=OPENROUTER_BASE_URL,
    temperature=0.1,
    max_tokens=2000
)

# ============================================================================
# Data Models
# ============================================================================

class AnomalyType:
    MISSING_DATA = "missing_data"
    FRAUD_PATTERN = "fraud_pattern"
    DUPLICATE = "duplicate_transaction"
    INCONSISTENT_DATA = "inconsistent_data"
    SUSPICIOUS_BEHAVIOR = "suspicious_behavior"

class DetectedAnomaly(BaseModel):
    """Model for detected anomalies"""
    transaction_id: str = Field(description="Unique transaction identifier")
    anomaly_type: str = Field(description="Type of anomaly detected")
    severity: str = Field(description="Severity level: LOW, MEDIUM, HIGH, CRITICAL")
    description: str = Field(description="Description of the anomaly")
    affected_fields: List[str] = Field(description="Fields affected by the anomaly")
    confidence_score: float = Field(description="Confidence score between 0 and 1")

class ValidationResult(BaseModel):
    """Model for validation results"""
    transaction_id: str
    is_valid_anomaly: bool = Field(description="Whether the anomaly is confirmed")
    validation_reason: str = Field(description="Reason for validation decision")
    requires_human_review: bool = Field(description="Whether human review is needed")
    priority: str = Field(description="Priority level: LOW, MEDIUM, HIGH, URGENT")

class ResolutionAction(BaseModel):
    """Model for resolution actions"""
    transaction_id: str
    action_type: str = Field(description="Type of action: FIX, FLAG, ALERT, INVESTIGATE")
    suggested_fix: str = Field(description="Suggested resolution")
    automated_fix_possible: bool = Field(description="Can be fixed automatically")
    workflow_trigger: Optional[str] = Field(description="Workflow to trigger")

# ============================================================================
# Helper: Load Data from CSV
# ============================================================================

def load_data_from_csv(file_path: str) -> List[Dict[str, Any]]:
    """
    Load and prepare the data from CSV for anomaly detection
    """
    df = pd.read_csv(file_path)
    print(f"✅ Loaded {len(df)} records from {file_path}")

    # Process the data to match the format required for anomaly detection
    transactions = []
    for _, row in df.iterrows():
        transaction = {
            "transaction_id": str(row["Customer_ID"]),
            "customer_id": str(row["Customer_ID"]),
            "amount": row["Balance"],  # Using Balance as the amount for anomaly detection
            "date": None,  # No transaction date in this dataset, set as None
            "merchant": "Unknown",  # No merchant info available
            "card_number": "****" + str(row["Customer_ID"])[-4:],  # Just using the last 4 digits of Customer_ID
            "credit_score": row["Credit_Score"],
            "transactions_last_month": row["Transactions_Last_Month"],
            "is_anomaly": row["Is_Anomaly"]
        }
        transactions.append(transaction)

    return transactions

# ============================================================================
# Agent System
# ============================================================================

# Agent 1: Detection Agent
# ============================================================================

class DetectionAgent:
    """
    Monitors data for anomalies using AI-powered pattern recognition
    """

    def __init__(self, llm):
        self.llm = llm
        self.detection_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert AI agent specialized in detecting anomalies in banking and financial data.

Your task is to analyze transaction records and identify:
1. Missing entries (incomplete data records)
2. Fraud patterns (unusual transactions or suspicious behavior)
3. Duplicate transactions (repeated entries due to errors)
4. Inconsistent data (unrealistic values for credit scores, amounts, dates, etc.)

For each anomaly detected, provide:
- Transaction ID
- Anomaly type
- Severity (LOW, MEDIUM, HIGH, CRITICAL)
- Clear description
- Affected fields
- Confidence score (0-1)

Analyze the data carefully and return valid JSON with detected anomalies."""),

            ("human", """Analyze the following transaction data for anomalies:

{transaction_data}

Detect all anomalies and return a JSON array with this structure:
[
  {{
    "transaction_id": "string",
    "anomaly_type": "string",
    "severity": "string",
    "description": "string",
    "affected_fields": ["field1", "field2"],
    "confidence_score": 0.95
  }}
]

Return ONLY the JSON array, no additional text.""")
        ])

    def detect_anomalies(self, transactions: List[Dict]) -> List[DetectedAnomaly]:
        """
        Detect anomalies in transaction data
        """
        print("\n🔍 Detection Agent: Analyzing transactions...")

        # Prepare transaction data for analysis
        transaction_data = json.dumps(transactions, indent=2)

        # Create prompt
        messages = self.detection_prompt.format_messages(transaction_data=transaction_data)

        # Get LLM response
        try:
            response = self.llm.invoke(messages)
            response_text = response.content
        except Exception as e:
            print(f"❌ Error calling LLM: {e}")
            return []

        try:
            # Clean response text - remove markdown code blocks if present
            response_text = response_text.strip()
            if response_text.startswith("```"):
                lines = response_text.split('\n')
                response_text = '\n'.join(lines[1:-1] if len(lines) > 2 else lines)

            # Parse JSON response
            anomalies_data = json.loads(response_text)

            if not anomalies_data:
                print("❌ No anomalies detected by the model")
                return []

            # Convert to DetectedAnomaly objects
            anomalies = []
            for anomaly_dict in anomalies_data:
                try:
                    anomaly = DetectedAnomaly(**anomaly_dict)
                    anomalies.append(anomaly)
                except Exception as e:
                    print(f"⚠️  Error parsing anomaly: {e}")
                    continue

            print(f"✅ Detected {len(anomalies)} anomalies")
            return anomalies

        except json.JSONDecodeError as e:
            print(f"❌ Error parsing LLM response: {e}")
            print(f"Response: {response_text[:500]}...")
            return []
# ============================================================================
# Agent 2: Validation Agent
# ============================================================================

class ValidationAgent:
    """
    Validates detected anomalies and determines if they require action
    """
    def __init__(self, llm):
        self.llm = llm
        self.validation_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert AI agent specialized in validating anomalies in banking data.
Your task is to review detected anomalies and determine:
1. Is this a valid anomaly that requires action?
2. What is the reason for your validation decision?
3. Does it require human review?
4. What is the priority level?

Consider:
- Business rules and thresholds
- Historical patterns
- Risk levels
- Regulatory requirements

Be conservative with false positives but never miss critical issues."""),
            ("human", """Validate the following detected anomaly:

Transaction ID: {transaction_id}
Anomaly Type: {anomaly_type}
Severity: {severity}
Description: {description}
Affected Fields: {affected_fields}
Confidence Score: {confidence_score}

Original Transaction Data:
{transaction_data}

Provide validation result as JSON:
{{
  "transaction_id": "string",
  "is_valid_anomaly": true,
  "validation_reason": "string",
  "requires_human_review": true,
  "priority": "HIGH"
}}

Return ONLY the JSON object, no additional text.""")
        ])

    def validate_anomaly(self, anomaly: DetectedAnomaly,
                         transaction_data: Dict) -> ValidationResult:
        """
        Validate a detected anomaly
        """
        print(f"\n✓ Validation Agent: Validating {anomaly.transaction_id}...")

        # Create prompt
        messages = self.validation_prompt.format_messages(
            transaction_id=anomaly.transaction_id,
            anomaly_type=anomaly.anomaly_type,
            severity=anomaly.severity,
            description=anomaly.description,
            affected_fields=json.dumps(anomaly.affected_fields),
            confidence_score=anomaly.confidence_score,
            transaction_data=json.dumps(transaction_data, indent=2)
        )

        # Get LLM response
        try:
            response = self.llm.invoke(messages)
            response_text = response.content.strip()

            # Clean response text
            if response_text.startswith("```"):
                lines = response_text.split('\n')
                response_text = '\n'.join(lines[1:-1] if len(lines) > 2 else lines)

            # Parse JSON response
            validation_data = json.loads(response_text)
            validation_result = ValidationResult(**validation_data)

            status = "✅ VALID" if validation_result.is_valid_anomaly else "❌ FALSE POSITIVE"
            print(f"{status} - Priority: {validation_result.priority}")

            return validation_result

        except Exception as e:
            print(f"⚠️  Error in validation: {e}")
            # Return conservative default
            return ValidationResult(
                transaction_id=anomaly.transaction_id,
                is_valid_anomaly=True,
                validation_reason="Validation failed, defaulting to valid for safety",
                requires_human_review=True,
                priority="HIGH"
            )


# ============================================================================
# Agent 3: Resolution Agent
# ============================================================================

class ResolutionAgent:
    """
    Suggests fixes and triggers workflows to resolve anomalies
    """

    def __init__(self, llm):
        self.llm = llm
        self.resolution_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert AI agent specialized in resolving anomalies in banking data.

Your task is to suggest appropriate actions for validated anomalies:
1. Determine the action type (FIX, FLAG, ALERT, INVESTIGATE)
2. Suggest specific fixes or remediation steps
3. Determine if automated fix is possible
4. Identify workflows to trigger

Action Types:
- FIX: Can be corrected automatically or with minimal intervention
- FLAG: Mark for review but no immediate action
- ALERT: Notify compliance/fraud team immediately
- INVESTIGATE: Requires detailed investigation

Be specific and actionable in your suggestions."""),
            ("human", """Provide resolution for the following validated anomaly:

Transaction ID: {transaction_id}
Anomaly Type: {anomaly_type}
Severity: {severity}
Description: {description}
Validation Status: {is_valid}
Priority: {priority}

Original Transaction:
{transaction_data}

Provide resolution action as JSON:
{{
  "transaction_id": "string",
  "action_type": "INVESTIGATE",
  "suggested_fix": "detailed description",
  "automated_fix_possible": false,
  "workflow_trigger": null
}}

Return ONLY the JSON object, no additional text.""")
        ])

    def suggest_resolution(self, anomaly: DetectedAnomaly,
                           validation: ValidationResult,
                           transaction_data: Dict) -> ResolutionAction:
        """
        Suggest resolution for a validated anomaly
        """
        print(f"\n🔧 Resolution Agent: Generating resolution for {anomaly.transaction_id}...")

        # Create prompt
        messages = self.resolution_prompt.format_messages(
            transaction_id=anomaly.transaction_id,
            anomaly_type=anomaly.anomaly_type,
            severity=anomaly.severity,
            description=anomaly.description,
            is_valid=validation.is_valid_anomaly,
            priority=validation.priority,
            transaction_data=json.dumps(transaction_data, indent=2)
        )

        # Get LLM response
        try:
            response = self.llm.invoke(messages)
            response_text = response.content.strip()

            # Clean response text
            if response_text.startswith("```"):
                lines = response_text.split('\n')
                response_text = '\n'.join(lines[1:-1] if len(lines) > 2 else lines)

            # Parse JSON response
            resolution_data = json.loads(response_text)
            resolution_action = ResolutionAction(**resolution_data)

            print(f"📋 Action: {resolution_action.action_type}")
            print(f"🤖 Auto-fix: {'Yes' if resolution_action.automated_fix_possible else 'No'}")

            return resolution_action

        except Exception as e:
            print(f"⚠️  Error in resolution: {e}")
            # Return conservative default
            return ResolutionAction(
                transaction_id=anomaly.transaction_id,
                action_type="INVESTIGATE",
                suggested_fix="Manual investigation required due to resolution parsing error",
                automated_fix_possible=False,
                workflow_trigger="manual_review_queue"
            )
# ============================================================================
# Orchestrator
# ============================================================================

class AnomalyDetectionOrchestrator:
    def __init__(self, llm):
        self.detection_agent = DetectionAgent(llm)
        self.validation_agent = ValidationAgent(llm)
        self.resolution_agent = ResolutionAgent(llm)

    def process_transactions(self, transactions: List[Dict]) -> Dict[str, Any]:
        print("\n" + "="*70)
        print("🚀 ANOMALY DETECTION SYSTEM STARTED")
        print("="*70)

        results = {
            "total_transactions": len(transactions),
            "anomalies_detected": [],
            "validated_anomalies": [],
            "resolution_actions": [],
            "summary": {}
        }

        # Step 1: Detection
        detected_anomalies = self.detection_agent.detect_anomalies(transactions)
        results["anomalies_detected"] = [a.dict() for a in detected_anomalies]  # Save detected anomalies

        # If no anomalies are detected, print a message and return the result
        if not detected_anomalies:
            print("\n✅ No anomalies detected. All transactions appear normal.")
            results["summary"] = {
                "total_detected": 0,
                "valid_anomalies": 0,
                "false_positives": 0,
                "require_human_review": 0,
                "automated_fixes": 0,
                "manual_actions": 0
            }
            return results

        # Step 2: Validation
        validated_anomalies = []
        for anomaly in detected_anomalies:
            transaction = next(
                (t for t in transactions if t.get("transaction_id") == anomaly.transaction_id),
                {}
            )

            validation = self.validation_agent.validate_anomaly(anomaly, transaction)
            validated_anomalies.append(validation)
            results["validated_anomalies"].append(validation.dict())

        # Step 3: Resolution (only for valid anomalies)
        resolution_actions = []
        for anomaly, validation in zip(detected_anomalies, validated_anomalies):
            if validation.is_valid_anomaly:
                transaction = next(
                    (t for t in transactions if t.get("transaction_id") == anomaly.transaction_id),
                    {}
                )

                resolution = self.resolution_agent.suggest_resolution(
                    anomaly, validation, transaction
                )
                resolution_actions.append(resolution)
                results["resolution_actions"].append(resolution.dict())

        # Generate summary
        results["summary"] = {
            "total_detected": len(detected_anomalies),
            "valid_anomalies": sum(1 for v in validated_anomalies if v.is_valid_anomaly),
            "false_positives": sum(1 for v in validated_anomalies if not v.is_valid_anomaly),
            "require_human_review": sum(1 for v in validated_anomalies if v.requires_human_review),
            "automated_fixes": sum(1 for r in resolution_actions if r.automated_fix_possible),
            "manual_actions": sum(1 for r in resolution_actions if not r.automated_fix_possible)
        }

        self._print_summary(results["summary"])

        # Save the results to a file
        output_file = "anomaly_detection_results.json"
        with open(output_file, "w") as f:
            json.dump(results, f, indent=2)

        print(f"✅ Results saved to {output_file}")

        return results

    def _print_summary(self, summary: Dict):
        """Print formatted summary"""
        print("\n" + "="*70)
        print("📊 DETECTION SUMMARY")
        print("="*70)
        print(f"Total Detected:        {summary['total_detected']}")
        print(f"Valid Anomalies:       {summary['valid_anomalies']}")
        print(f"False Positives:       {summary['false_positives']}")
        print(f"Human Review Needed:   {summary['require_human_review']}")
        print(f"Automated Fixes:       {summary['automated_fixes']}")
        print(f"Manual Actions:        {summary['manual_actions']}")
        print("="*70 + "\n")
# ============================================================================
# Example Usage
# ============================================================================

if __name__ == "__main__":
    # Check if API key is set
    if OPENROUTER_API_KEY == "your-api-key-here":
        print("⚠️  WARNING: Please set your OPENROUTER_API_KEY environment variable")
        exit(1)

    # Load the transactions data from the CSV file
    csv_file = "banking_data.csv"
    transactions = load_data_from_csv(csv_file)

    print("🔧 Initializing Anomaly Detection System...")

    # Initialize orchestrator
    orchestrator = AnomalyDetectionOrchestrator(llm)

    # Process transactions
    results = orchestrator.process_transactions(transactions)

    # Save results
    output_file = "anomaly_detection_results.json"
    with open(output_file, "w") as f:
        json.dump(results, f, indent=2)

    print(f"✅ Results saved to {output_file}")
