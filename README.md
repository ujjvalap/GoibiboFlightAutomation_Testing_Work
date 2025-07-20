# Goibibo Flight Search Automation (Final Version)

## ✅ Overview

This project automates the **flight search process** on [Goibibo](https://goibibo.com) using **Python and Selenium**.

### ✈️ Features

- Opens Goibibo Flights page
- Closes login popup (if present)
- Selects FROM and TO cities
- Selects departure date
- Sets number of passengers (optional)
- Clicks the 'Search Flights' button
- Verifies flight search results
- Takes screenshots at every major step
- Logs the full process in a `.log` file

---

## 🖥️ How to Run

### 1. Clone the repository

```bash
git clone https://github.com/ujjvalap/GoibiboFlightAutomation_Testing.git
cd GoibiboFlightAutomation_Testing
2. Install dependencies
bash
Copy
Edit
pip install -r requirements.txt
If you don't have a requirements.txt, just run:

bash
Copy
Edit
pip install selenium
3. Run the script
bash
Copy
Edit
python test_flight_search.py
⚙️ Optional CLI Arguments
Option	Description
--headless	Run Chrome in headless (invisible) mode
--login	Use logged-in Chrome session
--user-data-dir	Specify Chrome user profile path

Example:

bash
Copy
Edit
python test_flight_search.py --headless
📁 Project Structure
bash
Copy
Edit
GoibiboFlightAutomation_Testing/
│
├── test_flight_search.py         # Main automation script
├── flight_search.log             # Auto-generated log file
├── /screenshots/                 # Auto-generated screenshots
├── requirements.txt              # (Optional) Python dependencies
└── README.md                     # This file
🛠 Requirements
Python 3.x

Google Chrome (latest)

ChromeDriver (compatible with your Chrome version)

Download ChromeDriver: https://sites.google.com/chromium.org/driver/

👤 Author
Ujjval Pateliya
📧 Email: ujjvalpateliya@gmail.com
📞 Phone: +918435423244
🔗 GitHub: @ujjvalap

📌 Notes
This script is designed for testing/demo purposes.

Use --disable-blink-features=AutomationControlled to avoid Goibibo blocking automation in some environments.

csharp
Copy
Edit

### ✅ Instructions:

- Replace `your-email@example.com` and phone number with your real contact.
- Save this as `README.md` and push to GitHub:

```bash
git add README.md
git commit -m "Added clean README.md"
git push
