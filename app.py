"""
AI-Powered Employee Onboarding System
A Streamlit application that generates a complete onboarding package
(welcome email, 7-day plan, document checklist, IT access checklist,
FAQs, and training resources) based on employee name, role, and department.

No external APIs are used — all content is generated with conditional
logic and templates defined in this file.
"""

import streamlit as st
from datetime import date, timedelta


# --------------------------------------------------------------------------
# Data: Department & Role knowledge base
# --------------------------------------------------------------------------

DEPARTMENTS = [
    "Engineering",
    "Sales",
    "Marketing",
    "Human Resources",
    "Finance",
    "Customer Support",
    "Other",
]

ROLES = [
    "Software Engineer",
    "Product Manager",
    "Sales Executive",
    "Marketing Specialist",
    "HR Specialist",
    "Financial Analyst",
    "Customer Support Representative",
    "Other",
]

# IT access checklist keyed by department
IT_ACCESS_BY_DEPARTMENT = {
    "Engineering": [
        "Company email & Slack/Teams account",
        "GitHub/GitLab organization access",
        "VPN and SSH keys for internal servers",
        "Cloud provider access (AWS/GCP/Azure) with least-privilege role",
        "CI/CD pipeline access (Jenkins/GitHub Actions)",
        "Local dev environment setup (IDE, Docker, package managers)",
        "Access to internal wiki / architecture docs",
    ],
    "Sales": [
        "Company email & Slack/Teams account",
        "CRM access (Salesforce/HubSpot)",
        "Sales enablement tools (LinkedIn Sales Navigator, Outreach)",
        "Quoting/contract management tool access",
        "VoIP / dialer software account",
    ],
    "Marketing": [
        "Company email & Slack/Teams account",
        "Marketing automation platform (HubSpot/Marketo)",
        "Social media management tools (Buffer/Hootsuite)",
        "Analytics dashboards (Google Analytics, Looker)",
        "Design tool access (Figma/Canva/Adobe Suite)",
        "CMS access for company website/blog",
    ],
    "Human Resources": [
        "Company email & Slack/Teams account",
        "HRIS system access (Workday/BambooHR)",
        "Applicant Tracking System (ATS) access",
        "Payroll system access (view-only unless applicable)",
        "Employee document management system",
    ],
    "Finance": [
        "Company email & Slack/Teams account",
        "ERP/accounting system access (NetSuite/QuickBooks/SAP)",
        "Expense management tool (Expensify/Concur)",
        "Financial reporting dashboard access",
        "Restricted access to banking/payment portals (approval-based)",
    ],
    "Customer Support": [
        "Company email & Slack/Teams account",
        "Helpdesk/ticketing system access (Zendesk/Freshdesk)",
        "Knowledge base editing rights",
        "Live chat tool access",
        "Customer account lookup/admin tool (read-only initially)",
    ],
    "Other": [
        "Company email & Slack/Teams account",
        "Shared drive / document management system access",
        "Relevant department-specific tool access (to be confirmed with manager)",
    ],
}

# Training resources keyed by role
TRAINING_RESOURCES_BY_ROLE = {
    "Software Engineer": [
        "Internal engineering onboarding wiki",
        "Codebase walkthrough sessions with tech lead",
        "Coding standards & style guide documentation",
        "Git workflow and code review process guide",
        "Access to internal tech talks / recorded architecture sessions",
    ],
    "Product Manager": [
        "Product roadmap and strategy documentation",
        "Customer research repository access",
        "Agile/Scrum process training",
        "Analytics tool training (Amplitude/Mixpanel)",
        "Stakeholder communication guidelines",
    ],
    "Sales Executive": [
        "Sales playbook and pitch deck library",
        "CRM training modules",
        "Product demo certification course",
        "Objection handling and negotiation training",
        "Territory / account mapping guide",
    ],
    "Marketing Specialist": [
        "Brand guidelines and voice/tone documentation",
        "Marketing automation platform training",
        "SEO/content strategy playbook",
        "Campaign analytics and reporting training",
    ],
    "HR Specialist": [
        "HR policies and compliance training",
        "HRIS system training modules",
        "Recruitment and interviewing best practices",
        "Employee relations and conflict resolution training",
    ],
    "Financial Analyst": [
        "Financial modeling templates and guidelines",
        "ERP/accounting system training",
        "Company budgeting and forecasting process docs",
        "Compliance and audit training",
    ],
    "Customer Support Representative": [
        "Product knowledge base and FAQ training",
        "Helpdesk tool certification",
        "Customer communication and de-escalation training",
        "SLA and escalation process documentation",
    ],
    "Other": [
        "General company onboarding course",
        "Role-specific training to be assigned by manager",
        "Access to internal Learning Management System (LMS)",
    ],
}

# General documents required for all employees
BASE_REQUIRED_DOCUMENTS = [
    "Signed offer letter",
    "Government-issued photo ID",
    "Proof of address",
    "Tax registration documents (e.g., PAN/SSN/TIN as applicable)",
    "Bank account details for payroll",
    "Signed employment contract / NDA",
    "Educational certificates",
    "Previous employment relieving letter / experience certificates",
    "Emergency contact information form",
]

# Additional documents by department
EXTRA_DOCUMENTS_BY_DEPARTMENT = {
    "Engineering": ["Signed IP assignment agreement", "Background check consent (if applicable)"],
    "Finance": ["Signed confidentiality agreement", "Background/credit check consent"],
    "Human Resources": ["Signed confidentiality agreement"],
    "Sales": ["Signed non-compete agreement (if applicable)"],
    "Marketing": [],
    "Customer Support": [],
    "Other": [],
}

FAQS = [
    (
        "When and where should I report on my first day?",
        "Please arrive at the office (or log in remotely) by 9:00 AM on your start date. "
        "Your manager or HR representative will send exact location/link details beforehand.",
    ),
    (
        "What should I bring on my first day?",
        "Bring a valid government-issued ID and any pending original documents listed in "
        "your document checklist. A laptop will be provided if applicable to your role.",
    ),
    (
        "Who do I contact if I face any issues during onboarding?",
        "Your assigned HR buddy and reporting manager are your primary points of contact. "
        "Their details will be shared in your welcome email.",
    ),
    (
        "When will I get my system/IT access?",
        "Most IT access is provisioned within the first 1-2 business days. If anything is "
        "delayed, reach out to the IT helpdesk.",
    ),
    (
        "What is the dress code?",
        "Business casual is the general norm, but this may vary by department/team — "
        "your manager will clarify during your first week.",
    ),
    (
        "When is the probation review?",
        "Probation periods are typically reviewed at 90 days, but exact timelines depend "
        "on your offer letter — check with HR for specifics.",
    ),
]


# --------------------------------------------------------------------------
# Generation functions
# --------------------------------------------------------------------------

def generate_welcome_email(name: str, role: str, department: str) -> str:
    return f"""Subject: Welcome to the Team, {name}!

Dear {name},

Welcome aboard! We are thrilled to have you join us as a **{role}** in the
**{department}** department. Your skills and experience make you a great
addition to our team, and we're confident you'll make a strong impact here.

Over the next few days, you'll receive a structured onboarding plan to help
you settle in smoothly. This will include introductions to your team,
access to necessary systems and tools, and training sessions tailored to
your role.

Please don't hesitate to reach out to your manager or the HR team if you
have any questions before or during your first week.

Once again, welcome to the team — we're excited to see what we'll
accomplish together!

Best regards,
Human Resources Team
"""


def generate_7_day_plan(name: str, role: str, department: str) -> list:
    start = date.today()
    plan = [
        (
            "Day 1",
            "Orientation & Introductions",
            [
                f"Welcome session with HR and introduction to company culture and values",
                f"Meet your manager and {department} team members",
                "Workstation and IT equipment setup",
                "Complete pending paperwork and document submission",
            ],
        ),
        (
            "Day 2",
            "Systems & Tools Setup",
            [
                "Get IT access provisioned (see IT Access Checklist)",
                f"Walkthrough of tools used by the {department} team",
                "Set up communication channels (Slack/Teams, email)",
                "Review company policies and employee handbook",
            ],
        ),
        (
            "Day 3",
            f"Role-Specific Deep Dive: {role}",
            [
                f"1:1 with manager to discuss role expectations and goals",
                f"Review of {role} responsibilities and key deliverables",
                "Shadow a team member to understand daily workflows",
            ],
        ),
        (
            "Day 4",
            "Training & Skill Building",
            [
                "Begin role-specific training modules (see Training Resources)",
                "Attend a relevant internal training session or workshop",
                "Review key documentation and internal wiki/resources",
            ],
        ),
        (
            "Day 5",
            "Process & Collaboration",
            [
                f"Learn key {department} processes and workflows",
                "Attend a team stand-up / weekly sync meeting",
                "Set up 30-60-90 day goals with your manager",
            ],
        ),
        (
            "Day 6",
            "Hands-on Contribution",
            [
                "Begin working on a small starter task or project",
                "Pair with a mentor/buddy for guidance",
                "Ask questions and clarify any doubts from the week",
            ],
        ),
        (
            "Day 7",
            "Review & Feedback",
            [
                "End-of-week check-in with manager",
                "Share onboarding feedback with HR",
                "Finalize goals and roadmap for the coming weeks",
            ],
        ),
    ]

    detailed_plan = []
    for i, (day_label, theme, tasks) in enumerate(plan):
        actual_date = start + timedelta(days=i)
        detailed_plan.append(
            {
                "day": day_label,
                "date": actual_date.strftime("%A, %B %d, %Y"),
                "theme": theme,
                "tasks": tasks,
            }
        )
    return detailed_plan


def generate_document_checklist(department: str) -> list:
    docs = list(BASE_REQUIRED_DOCUMENTS)
    docs.extend(EXTRA_DOCUMENTS_BY_DEPARTMENT.get(department, []))
    return docs


def generate_it_access_checklist(department: str) -> list:
    return IT_ACCESS_BY_DEPARTMENT.get(department, IT_ACCESS_BY_DEPARTMENT["Other"])


def generate_training_resources(role: str) -> list:
    return TRAINING_RESOURCES_BY_ROLE.get(role, TRAINING_RESOURCES_BY_ROLE["Other"])


# --------------------------------------------------------------------------
# Streamlit UI
# --------------------------------------------------------------------------

def main():
    st.set_page_config(
        page_title="AI-Powered Employee Onboarding System",
        page_icon="🧑‍💼",
        layout="centered",
    )

    st.title("🧑‍💼 AI-Powered Employee Onboarding System")
    st.write(
        "Enter a new employee's details below to instantly generate a complete "
        "onboarding package: welcome email, 7-day plan, document checklist, "
        "IT access checklist, FAQs, and training resources."
    )

    st.divider()

    # --- Input Form ---
    with st.form("onboarding_form"):
        st.subheader("Employee Details")
        name = st.text_input("Employee Name", placeholder="e.g., Jordan Smith")

        col1, col2 = st.columns(2)
        with col1:
            role = st.selectbox("Role", ROLES)
            if role == "Other":
                role = st.text_input("Please specify the role", key="custom_role") or "Other"
        with col2:
            department = st.selectbox("Department", DEPARTMENTS)
            if department == "Other":
                department = st.text_input("Please specify the department", key="custom_dept") or "Other"

        submitted = st.form_submit_button("Generate Onboarding Package 🚀")

    # Persist submission across reruns (e.g. when checkboxes are clicked).
    if submitted:
        if not name.strip():
            st.error("Please enter the employee's name before generating the onboarding package.")
            st.session_state["onboarding_generated"] = False
            return
        st.session_state["onboarding_generated"] = True
        st.session_state["onboarding_name"] = name
        st.session_state["onboarding_role"] = role
        st.session_state["onboarding_department"] = department

    if not st.session_state.get("onboarding_generated"):
        st.info("Fill in the employee details above and click **Generate Onboarding Package** to begin.")
        return

    # Use the stored values so checkbox clicks don't wipe the generated content.
    name = st.session_state["onboarding_name"]
    role = st.session_state["onboarding_role"]
    department = st.session_state["onboarding_department"]

    st.success(f"Onboarding package generated for **{name}** ({role}, {department})")
    st.divider()

    # --- 1. Welcome Email ---
    st.header("1️⃣ Professional Welcome Email")
    email_text = generate_welcome_email(name, role, department)
    st.text_area("Welcome Email", email_text, height=320, label_visibility="collapsed")

    st.divider()

    # --- 2. 7-Day Onboarding Plan ---
    st.header("2️⃣ 7-Day Onboarding Plan")
    plan = generate_7_day_plan(name, role, department)
    for day in plan:
        with st.expander(f"**{day['day']} — {day['theme']}**  ({day['date']})", expanded=(day["day"] == "Day 1")):
            for task in day["tasks"]:
                st.checkbox(task, key=f"{day['day']}_{task}")

    st.divider()

    # --- 3. Required Documents Checklist ---
    st.header("3️⃣ Required Documents Checklist")
    documents = generate_document_checklist(department)
    for doc in documents:
        st.checkbox(doc, key=f"doc_{doc}")

    st.divider()

    # --- 4. IT Access Checklist ---
    st.header(f"4️⃣ IT Access Checklist — {department} Department")
    it_items = generate_it_access_checklist(department)
    for item in it_items:
        st.checkbox(item, key=f"it_{item}")

    st.divider()

    # --- 5. FAQs ---
    st.header("5️⃣ Frequently Asked Questions")
    for question, answer in FAQS:
        with st.expander(question):
            st.write(answer)

    st.divider()

    # --- 6. Training Resources ---
    st.header(f"6️⃣ Training Resources — {role}")
    training_items = generate_training_resources(role)
    for item in training_items:
        st.markdown(f"- {item}")

    st.divider()
    st.caption(
        "This onboarding package was generated automatically based on the role and "
        "department provided. Please verify details with HR/IT for accuracy before "
        "final distribution."
    )


if __name__ == "__main__":
    main()