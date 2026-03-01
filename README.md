# ✈️ AirportAPI

Full-stack airport management system with flight search, ticket booking, Stripe payments, and an AI travel assistant powered by Google Gemini.

## 📐 Architecture

```
Airport/
├── aviation/                # Django backend (manage.py is here)
│   ├── aviation/            # Django project settings, urls, asgi
│   ├── core/                # Models: Country, Airport, Airline, Airplane, Flight, Ticket
│   ├── orders/              # Order management (booking, expiry)
│   ├── payments/            # Stripe checkout, webhooks
│   ├── users/               # Custom User model, JWT auth, registration
│   └── assistant/           # AI chatbot (Gemini LLM + tools)
├── airport-ui/              # React + Vite frontend
├── docker-compose.yml       # Full stack: web, db, redis, celery, ui
├── Dockerfile               # Backend Docker image
├── requirements.txt         # Python dependencies
└── .env                     # Environment variables (not committed)
```

## 🛠 Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Django 5.2, Django REST Framework, Django Channels |
| Auth | JWT (SimpleJWT) |
| Database | SQLite (dev) / PostgreSQL (prod) |
| Payments | Stripe Checkout + Webhooks |
| AI Assistant | Google Gemini 2.5 Flash |
| Task Queue | Celery + Redis |
| Frontend | React 19, Vite 6, React Router 7 |
| Maps | Leaflet + React-Leaflet |
| Deployment | Docker, Render |

---

## 🚀 Local Setup (without Docker)

### Prerequisites

- Python 3.12+
- Node.js 18+
- Git

### 1. Clone the repo

```bash
git clone https://github.com/your-username/AirportAPI.git
cd AirportAPI
```

### 2. Create `.env` file

Create a `.env` in the project root with the following variables:

```env
# Django
SECRET_KEY=your-django-secret-key
DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

# Stripe
STRIPE_SECRET_KEY=sk_test_...
STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...
STRIPE_SUCCESS_URL=http://localhost:5173/payment/success
STRIPE_CANCEL_URL=http://localhost:5173/payment/cancel

# Gemini AI
GEMINI_API_KEY=your-gemini-api-key

# CORS
CSRF_TRUSTED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173

DJANGO_SETTINGS_MODULE=aviation.settings
```

### 3. Backend setup

```bash
# Create virtual environment
python -m venv .venv

# Activate it
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
cd aviation
python manage.py migrate

# Seed database with demo data
python manage.py seed_data

# Create superuser (optional, for Django admin)
python manage.py createsuperuser

# Start backend server
python manage.py runserver
```

Backend runs at **http://localhost:8000**

### 4. Frontend setup

```bash
# In a new terminal, from project root:
cd airport-ui

# Install dependencies
npm install

# Start dev server
npm run dev
```

Frontend runs at **http://localhost:5173**

---

## 🐳 Docker Setup (full stack)

```bash
# Build and start all services
docker-compose up --build

# In another terminal, seed the database
docker-compose exec web python manage.py seed_data

# (Optional) Create superuser
docker-compose exec web python manage.py createsuperuser
```

This starts:
- **PostgreSQL** on port 5433
- **Redis** on port 6379
- **Backend** (uvicorn) on port 8000
- **Frontend** (Vite) on port 5173
- **Celery** worker for async tasks

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register/` | Register new user |
| POST | `/api/auth/login/` | Login (returns JWT) |
| POST | `/api/token/` | Obtain JWT token pair |
| POST | `/api/token/refresh/` | Refresh access token |
| GET | `/api/me/` | Current user profile |
| GET | `/api/airports/` | List airports |
| GET | `/api/airlines/` | List airlines |
| GET | `/api/flights/` | List flights (filterable) |
| GET | `/api/flights/{id}/` | Flight detail |
| GET | `/api/tickets/` | List tickets (filterable) |
| GET | `/api/orders/` | User's orders |
| POST | `/api/orders/` | Create order (book tickets) |
| POST | `/payments/checkout-session/` | Create Stripe checkout |
| POST | `/payments/webhook/` | Stripe webhook |
| GET | `/payments/payments/` | User's payment history |
| POST | `/api/assistant/nl-query/` | AI assistant (natural language) |
| GET | `/api/docs/` | Swagger API documentation |
| GET | `/api/schema/` | OpenAPI schema |

---

## 🤖 AI Assistant

The built-in AI chatbot (powered by Gemini) can:

- **Search flights** by destination, origin, dates
- **Check ticket availability** and prices
- **View user orders** and booking status
- **Search airports** by name, IATA code, or country
- **Search airlines** by name or code
- **Get weather** info for any city/country
- **Mirror language** — responds in the user's language

Access via the chat widget in the bottom-right corner of the UI, or via the API endpoint `/api/assistant/nl-query/`.

---

## 💳 Payments (Stripe)

The app uses **Stripe Checkout** for payments:

1. User books tickets → Order is created with status `booked` (expires in 15 min)
2. User clicks "Pay Now" → Redirected to Stripe Checkout
3. After payment → Webhook updates order to `paid`
4. If time expires → Order auto-expires, tickets released

For local webhook testing, use `stripe listen --forward-to localhost:8000/payments/webhook/`

---

## 🧪 Useful Commands

```bash
# Run Django tests
cd aviation
python manage.py test

# Collect static files
python manage.py collectstatic --noinput

# Check for migration issues
python manage.py makemigrations --check

# Run with ASGI (WebSocket support)
uvicorn aviation.asgi:application --host 0.0.0.0 --port 8000
```

---

## 📁 Environment Variables Reference

| Variable | Required | Description |
|----------|----------|-------------|
| `SECRET_KEY` | ✅ | Django secret key |
| `DEBUG` | ✅ | `True` for development |
| `DJANGO_ALLOWED_HOSTS` | ✅ | Comma-separated hosts |
| `STRIPE_SECRET_KEY` | ✅ | Stripe secret key |
| `STRIPE_PUBLISHABLE_KEY` | ✅ | Stripe publishable key |
| `STRIPE_WEBHOOK_SECRET` | ✅ | Stripe webhook secret |
| `STRIPE_SUCCESS_URL` | ✅ | Payment success redirect URL |
| `STRIPE_CANCEL_URL` | ✅ | Payment cancel redirect URL |
| `GEMINI_API_KEY` | ✅ | Google Gemini API key |
| `POSTGRES_HOST` | ❌ | Set to use PostgreSQL (empty = SQLite) |
| `POSTGRES_DB` | ❌ | PostgreSQL database name |
| `POSTGRES_USER` | ❌ | PostgreSQL user |
| `POSTGRES_PASSWORD` | ❌ | PostgreSQL password |
| `REDIS_URL` | ❌ | Redis URL (empty = in-memory channels) |
| `EMAIL_HOST_USER` | ❌ | Gmail for email sending |
| `EMAIL_HOST_PASSWORD` | ❌ | Gmail app password |
