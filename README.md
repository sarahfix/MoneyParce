# 💰 MoneyParce

**MoneyParce** is a web application developed for a Georgia Tech CS 2340 group project. It helps users **track income and expenses**, **analyze spending behavior**, and **gain personalized financial insights**. By integrating real-time banking data with **AI-driven analysis** and **intuitive visualizations**, MoneyParce empowers users to take control of their finances and make smarter money decisions.

---

## ✨ Features

- 📈 **Expense & Income Tracking**: Users can log and categorize financial transactions.
- 🧠 **AI-Driven Insights**: Personalized recommendations based on spending trends.
- 📊 **Visual Analytics**: Pie charts, bar graphs, and time-series plots to visualize spending behavior.
- 🔒 **Secure Login**: Basic authentication for account access and data protection.
- 🏦 **Bank Data Integration** *(Simulated)*: Future-ready design to support real-time bank API integration.
- 📆 **Monthly Summaries**: Automatically generate monthly spending reports.

---

## 🛠️ Technologies Used

| Technology    | Purpose                        |
|---------------|--------------------------------|
| Python        | Backend logic and AI analysis  |
| Django        | Web framework                  |
| HTML/CSS      | Frontend templates & styling   |
| JavaScript    | Interactivity and charts       |
| Pycharm       | Primary development environment |

---

## 🚀 Installation

### Clone the Repository
```bash
git clone https://github.com/sarahfix/MoneyParce.git
cd MoneyParce
```

### Set Up Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### Run the Server
```bash
python manage.py migrate
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` in your browser to view the app.

---

## 👥 Team Members

This project was built as part of **CS 2340: Objects and Design** at Georgia Tech.  
Contributors include:
- Sarah Fix
- Mimi Masson
- Brant Becker
- Lulu Greco
