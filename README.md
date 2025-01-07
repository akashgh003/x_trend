# 🚀 Twitter Trend Scraper

> A sleek web app that grabs what's trending on Twitter/X and shows it in a clean, modern interface.

![Twitter Trend Scraper Screenshot](https://github.com/akashgh003/x_trend/blob/main/Screenshot%202025-01-07%20173226.png)

## ⚡ Quick Demo
[Watch it in action!](https://github.com/akashgh003/x_trend/blob/main/clip.mp4)

## 🛠️ Tech Stack We're Using

### Backend Magic 🧙‍♂️
- **🐍 Python**: Our trusty programming language
- **🌶️ Flask**: Light and powerful web framework
- **🤖 Selenium**: The automation wizard for scraping trends
- **🍃 MongoDB**: Where we store all our cool data
- **🔌 PyMongo**: Helps Python talk to MongoDB
- **📡 Requests**: For smooth API calls

### Frontend Goodness 🎨
- **🎨 HTML/CSS**: Making things pretty
- **⚡ JavaScript**: Adding that interactive sparkle
- **🔄 Fetch API**: Keeping everything real-time

## ✨ Cool Features
- 🔥 Real-time Twitter trends
- 📱 Clean, responsive design
- 🌐 IP tracking
- ⏰ Timestamp for every update
- 💾 MongoDB for data storage
- 🛡️ Solid error handling

## ⚠️ Why We Can't Go Serverless

Here's the thing - we can't deploy on platforms like Vercel because:

1. **🤖 Selenium Needs Its Space**
  - Needs a real Chrome browser
  - Requires ChromeDriver
  - Likes its system dependencies
  - Serverless platforms aren't built for this

2. **💭 Serverless Is Stateless**
  - Can't keep browser sessions going
  - Chrome gets lonely between requests
  - Functions timeout too quickly

## 🚀 Where Can We Deploy?

For this beauty to work, you'll need:
- 🖥️ A proper server (VPS)
- 🌐 Chrome + ChromeDriver installed
- ⚡ Always-on capabilities

Your best bets are:
- 🌊 DigitalOcean
- ☁️ AWS EC2
- 🚀 Google Cloud
- 💜 Heroku (with some tweaks)

## 🏃‍♂️ Run It Locally

1. Clone this bad boy
2. Install the goodies:
```bash
pip install -r requirements.txt
