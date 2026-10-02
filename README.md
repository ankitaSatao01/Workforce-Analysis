# AI-Based Workforce Demand & Resource Planning System

## 📌 Project Overview

The **AI-Based Workforce Demand & Resource Planning System** is a web-based application designed to help organizations manage employees, skills, projects, workforce demand, and resource allocation.

The system uses historical workforce demand data to generate **AI-based workforce forecasts** and helps identify resource gaps for future planning.

---

## 🎯 Objectives

- Manage employee information and skills.
- Manage projects and project requirements.
- Track workforce demand.
- Assign employees to projects.
- Forecast future workforce requirements.
- Identify resource gaps.
- Support better workforce planning and resource management.

---

## 🛠️ Technologies Used

### Frontend
- HTML
- CSS
- JavaScript

### Backend
- Python
- Flask

### Database
- MySQL

### AI / Forecasting
- Python
- Machine Learning / Forecasting techniques

### Tools
- Visual Studio Code
- MySQL Workbench
- Git & GitHub

---

## ✨ Main Features

### 👨‍💼 Employee Management
- Add employees
- Edit employee details
- View employee information
- Manage employee skills

### 🧑‍💻 Skill Management
- Add and manage skills
- Assign skills to employees
- Match employee skills with project requirements

### 📋 Project Management
- Add projects
- Edit projects
- Define project requirements
- Manage project resources

### 📊 Workforce Demand
- Add workforce demand
- View historical demand
- Analyze demand based on skills

### 🤖 AI Workforce Forecasting
- Analyze historical workforce demand
- Generate future workforce demand predictions
- Store and display forecast results

### 📈 Resource Gap Analysis
- Compare available employees with required employees
- Identify workforce shortages
- Support resource allocation decisions

### 🔮 Future Workforce Gap
- Analyze future workforce requirements
- Compare predicted demand with available resources

### 📊 Dashboard
The dashboard provides an overview of:

- Total Employees
- Total Skills
- Total Projects
- Available Employees
- AI Forecasts
- Average Predicted Demand

---

## 🗂️ Project Structure

```text
Workforce_Planning/
│
├── app.py
├── database.sql
├── erdiagram.mwb
├── requirements.txt
├── .gitignore
│
├── model/
│   └── forecasting.py
│
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── script.js
│
└── templates/
    ├── base.html
    ├── dashboard.html
    ├── employees.html
    ├── skills.html
    ├── projects.html
    ├── assignments.html
    ├── demand.html
    ├── forecast.html
    ├── forecasts.html
    ├── resource_gap.html
    ├── future_workforce_gap.html
    └── ...
