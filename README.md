# Online Retail Customer Segmentation & Analytics

## Executive Summary

This project analyzes customer purchasing behaviour using the UCI Online Retail Dataset.

The objective is to identify customer segments through RFM (Recency, Frequency, Monetary) analysis and transform transactional retail data into actionable business insights.

The project demonstrates a complete analytics workflow including:

- Data acquisition
- Data cleaning
- Exploratory Data Analysis (EDA)
- Feature engineering
- Customer segmentation
- Data visualization
- Interactive dashboard development with Streamlit

---

## Live Dashboard

🚀 Streamlit Application

Add deployment URL here after publishing:

https://online-retail-rfm-segmentation.streamlit.app/

---

## Business Problem

Retail companies typically serve thousands of customers with very different purchasing behaviours.

Without customer segmentation:

- Marketing campaigns become less effective
- Retention efforts become difficult to prioritize
- High-value customers are harder to identify
- Revenue opportunities may be missed

This project uses customer transaction data to identify meaningful customer segments and support data-driven business decisions.

---

## Dataset

**Source**

UCI Machine Learning Repository

**Dataset**

Online Retail Dataset

**Period Covered**

December 2010 to December 2011

**Description**

A transactional dataset containing purchases made by a UK-based online retail company.

### Key Variables

- InvoiceNo
- StockCode
- Description
- Quantity
- InvoiceDate
- UnitPrice
- CustomerID
- Country

---

## Methodology

### 1. Data Cleaning

The following cleaning rules were applied:

- Removed cancelled transactions
- Removed duplicate records
- Removed missing customer identifiers
- Removed negative quantities
- Removed invalid prices

### 2. Feature Engineering

Revenue was calculated as:

```text
Revenue = Quantity × UnitPrice
```

### 3. RFM Analysis

Customer behaviour was summarized using:

- Recency
- Frequency
- Monetary Value

### 4. Customer Segmentation

Customers were segmented based on purchasing behaviour and spending patterns.

### 5. Dashboard Development

A Streamlit dashboard was built to enable interactive exploration of:

- Customer segments
- Revenue metrics
- Customer value distributions
- Pareto analysis

---

## Key Findings

- Customer purchasing behaviour can be effectively summarized using RFM metrics.
- Customer value is highly concentrated among a relatively small percentage of customers.
- Distinct customer segments exhibit significantly different spending patterns.
- High-value customer groups represent important opportunities for retention and personalized marketing strategies.
- The dataset demonstrates a strong Pareto effect, where a small proportion of customers contributes a large share of total revenue.

---

## Dashboard Features

### Executive KPIs

- Total Customers
- Average Monetary Value
- Average Purchase Frequency
- Average Customer Recency

### Customer Segmentation

- Segment distribution analysis
- Interactive segmentation visualizations

### Customer Value Analysis

- Frequency vs Monetary value exploration
- Segment comparison

### Pareto Analysis

- Revenue contribution by customer group
- Customer concentration insights

---

## Technology Stack

- Python
- Pandas
- NumPy
- Scikit-learn
- Plotly
- Streamlit

---

## Project Structure

```text
online-retail-eda-and-ml/
│
├── streamlit_app.py
├── build_dataset.py
├── create_rfm_dataset.py
├── customer_rfm.csv
├── requirements.txt
├── README.md
└── .gitignore
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/carlos-ruiz-guerrero/online-retail-eda-and-ml.git
```

Move to the project directory:

```bash
cd online-retail-eda-and-ml
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the dashboard:

```bash
streamlit run streamlit_app.py
```

---

## Future Improvements

Potential future enhancements include:

- Customer Lifetime Value (CLV) prediction
- Churn prediction
- Product recommendation systems
- Time-series sales forecasting
- Advanced clustering techniques
- Cloud deployment automation

---

## Author

Carlos Ruiz Guerrero

GitHub:
https://github.com/carlos-ruiz-guerrero

LinkedIn:
(Add your LinkedIn profile here)
