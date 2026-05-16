# ScniseShop
ScniseShop - Asynchronous Telegram Digital Store Bot
Welcome to ScniseShop, a modern, lightweight, and fully asynchronous Telegram bot designed for selling digital goods, services, keys, or subscriptions (such as Discord Nitro, Telegram Premium, game assets, etc.).

This repository implements a production-ready architectural pattern utilizing the latest versions of industry-standard Python libraries. It serves as an excellent foundational template for scalable e-commerce bots or a strong addition to a backend developer's portfolio.

🚀 Key Features
🛒 Dynamic Catalog: Automatically fetches products from the database and renders clean Telegram inline keyword menus on the fly.

👤 User Accounts & Persistence: Automatic background user registration upon executing /start. Users can check their internal balance and Telegram metadata instantly.

💳 Mock Deposit System: Features an instant balance simulator (+500 RUB) to seamlessly test the entire checkout flow and wallet deduction engine.

🔒 Protected Admin Suite: Contains a restricted /admin command that validates user identity via strict environment variables, serving global store diagnostics to authorized personnel only.

🏗️ Clean Enterprise Architecture: Implements asynchronous scoped context sessions, declarative ORM modeling, and granular configuration lifecycle management.

🛠️ Tech Stack & Architecture Highlights
Framework: aiogram 3.x (Advanced, asynchronous Telegram Bot API framework).

Database ORM: SQLAlchemy 2.0 (Utilizing declarative mapping and fully asynchronous execution engines).

Database Driver: aiosqlite (Asynchronous SQLite 3 driver preventing synchronous thread blocking).

Configuration & Validation: Pydantic Settings v2 (Type-safe environmental variable parsing and runtime configuration guardrails).

Session Middleware Lifecycle: The bot uses an architectural Outer Middleware interceptor pattern injected directly into the execution flow. It automatically handles database connection pooling, opening a secure session per Telegram event, injecting it into handlers, and cleanly committing/closing it without resource leaks.



⚙️ Installation & Setup Guide
1. Prerequisites
Ensure you have a stable production version of Python installed (Python 3.10, 3.11, or 3.12 is highly recommended).

⚠️ Warning: Avoid utilizing experimental/pre-release branches (such as Python 3.14+), as binary wheels for core components like pydantic-core may fail to compile from source due to Rust compiler dependencies.

2. Environment Configuration
Create a .env file in the root directory of the project alongside main.py:

BOT_TOKEN=1234567890:ABCdefGhIJKlmNoPQRsTUVwXyZ  # Your Telegram Bot Token

DB_URL=sqlite+aiosqlite:///scniseshop.db         # Async SQLite Database Connection String

ADMIN_ID=123456789                               # Your Telegram Numerical ID

3. Virtual Environment & Dependency Installation
Open your terminal inside the project root folder and execute the following commands to spin up an isolated virtual environment and fetch the packages:

Bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate 

# Upgrade package manager and install dependencies
pip install --upgrade pip
pip install -r requirements.txt



4. Database Seeding
Populate your freshly created local SQLite database with mocked digital products before turning the server on:

Bash
python seed.py
Expected Output: Тестовые товары успешно добавлены в базу данных ScniseShop!

5. Running the Application
Fire up the asynchronous pooling engine to bring the bot online:

Bash
python main.py
📊 Database Schema Blueprint
The architecture is backed by two cleanly coupled relational database tables:

users: Tracks user metrics (id, telegram_id, and balance decimal points).

items: Holds inventory data (id, name, price, and raw text description blocks).
