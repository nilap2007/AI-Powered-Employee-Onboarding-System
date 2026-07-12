# AI-Powered Employee Onboarding System

A Streamlit application that generates a complete onboarding package for a
new employee based on their **name**, **role**, and **department** — no
external APIs required. All content is produced locally using conditional
logic and templates.

## Generated Output

Given the employee's details, the app produces:

1. A professional welcome email
2. A structured 7-day onboarding plan
3. A checklist of required documents
4. An IT access checklist tailored to the department
5. FAQs for new employees
6. Training resources tailored to the role

## Project Structure

```
.
├── app.py        # Main Streamlit application
└── README.md      # This file
```

## Requirements

- Python 3.8+
- Streamlit

## Setup

1. (Optional) Create and activate a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:

   ```bash
   pip install streamlit
   ```

## Run the App

From the project directory, run:

```bash
streamlit run app.py
```

Streamlit will start a local server and open the app in your browser
(typically at `http://localhost:8501`).

## Usage

1. Enter the employee's name.
2. Select (or specify) their role.
3. Select (or specify) their department.
4. Click **Generate Onboarding Package**.
5. Review the welcome email, 7-day plan, document checklist, IT access
   checklist, FAQs, and training resources — each in its own clearly
   labeled section.
