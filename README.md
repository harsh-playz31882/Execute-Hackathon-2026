## Execute Hackathon 2026 – Renewable Energy Marketplace Portal

### 1. Problem Statement

Design a **web platform that connects renewable energy producers** (solar rooftop owners, biogas plants, wind farms, etc.) **with consumers or investors**.

The portal should:
- **Promote decentralized energy exchange**
- **Enable peer‑to‑peer green energy trading**
- **Encourage community‑based sustainability**

For the hackathon prototype, we focus on a **simple but end‑to‑end working marketplace**: producers can list their renewable assets, and consumers/investors can discover them and express interest in peer‑to‑peer deals.

---

### 2. What Our Prototype Delivers

- **User onboarding with roles**
  - Register as **Producer**, **Consumer**, or **Investor**.
  - Secure login (FastAPI security).

- **Energy asset listings (Marketplace)**
  - Producers can create and manage **energy assets**  
    (e.g., “10 kW rooftop solar in Pune, ₹5.5/unit”).
  - Public marketplace endpoint to list/filter assets by **type** and **location**.

- **Peer‑to‑peer trade intent**
  - Consumers/Investors can **send “Interest”** messages on specific assets.
  - Producers can view all interests on their assets and mark them as  
    **pending / accepted / rejected**.

- **Data is persisted**
  - All users, assets, and interests are stored in **SQLite** using **SQLAlchemy ORM**.

The focus is on a **clean, minimal API** and **clear separation of concerns**, so different team members can work independently on frontend and backend.

---

### 3. Technology Stack

- **Frontend**
  - HTML, CSS (basic, functional UI)
  - lightweight JavaScript for calling APIs

- **Backend**
  - **Python** + **FastAPI** (REST API + docs)
  - **SQLite** (lightweight embedded database)
  - **SQLAlchemy** (ORM)
  - **Pydantic v2** for request/response schemas
  - **python‑jose** + **passlib (bcrypt)** for JWT and password hashing

---

### 4. System Architecture 

**Logical components:**

1. **Authentication & Users**
   - Manages registration, login, and current user profile.
   - Assigns a **role** to each user: `producer`, `consumer`, or `investor`.

2. **Energy Assets**
   - Represents a renewable energy resource offered by a producer.
   - Core fields: asset type, capacity (kW), location, price per unit, description, status.

3. **Trade Interests**
   - Connects **interested consumers/investors** with **producer assets**.
   - Captures a short message and a status (pending/accepted/rejected).

4. **APIs**
   - Clean REST endpoints for:
     - `/api/v1/auth` – auth & user profile
     - `/api/v1/assets` – asset CRUD + marketplace listing
     - `/api/v1/interests` – trade interest lifecycle

5. **Database**
   - One SQLite database file: `energy_marketplace.db`.
   - Three main tables: `users`, `energy_assets`, `trade_interests`.

---

### 5. Database Model Overview

- **User**
  - `id`, `email`, `hashed_password`, `full_name`, `role`, `created_at`
  - Relationships:
    - `assets` → list of `EnergyAsset` owned
    - `trade_interests` → list of `TradeInterest` created by this user

- **EnergyAsset**
  - `id`, `owner_id`, `asset_type` (solar/biogas/wind), `capacity_kw`, `location`,
    `price_per_unit`, `description`, `status`, `created_at`
  - Relationships:
    - `owner` → `User` (producer)
    - `interests` → list of `TradeInterest` on this asset

- **TradeInterest**
  - `id`, `asset_id`, `interested_user_id`, `message`, `status`, `created_at`
  - Connects **a consumer/investor** to **a producer asset**.

This schema enables a **many‑to‑one** relationship from interests to assets and from assets to producers, modeling a peer‑to‑peer marketplace.

---

### 6. Backend Folder Structure (API + DB)

```text
backend/
  app/
    main.py                 # FastAPI app, CORS, startup, router registration
    core/
      config.py             # Settings (JWT secret, algorithm, token expiry)
      security.py           # Password hashing, JWT create/verify, current user
    db/
      database.py           # SQLite engine, SessionLocal, Base, init_db()
      models.py             # SQLAlchemy models (User, EnergyAsset, TradeInterest)
      schemas.py            # Pydantic schemas for requests/responses
      crud.py               # DB operations for users, assets, interests
    api/
      v1/
        routes_auth.py      # /api/v1/auth – register, login, current user
        routes_assets.py    # /api/v1/assets – marketplace + producer assets
        routes_interests.py # /api/v1/interests – trade intent lifecycle
    services/
      permissions.py        # Role & ownership checks (producer‑only actions)
```

This structure keeps the **business logic, HTTP layer, and persistence layer cleanly separated**.

---

### 7. High‑Level User Flows

#### 7.1 Producer Flow (Supply Side)

1. **Register as Producer**
   - Calls `POST /api/v1/auth/register` with role = `"producer"`.
2. **Login**
   - Calls `POST /api/v1/auth/login` and receives a JWT token.
3. **Create Asset**
   - Calls `POST /api/v1/assets/` with asset details (type, capacity, price, location).
4. **View Own Assets**
   - Calls `GET /api/v1/assets/owner/me` to see their portfolio.
5. **Receive Trade Interests**
   - Calls `GET /api/v1/interests/received` to see all interests on their assets.
6. **Accept / Reject Offers**
   - Calls `PATCH /api/v1/interests/{id}` to update status (`accepted` / `rejected`).

This models a **decentralized listing and negotiation process** for green energy.

#### 7.2 Consumer / Investor Flow (Demand Side)

1. **Register as Consumer/Investor**
   - Role set to `"consumer"` or `"investor"`.
2. **Browse Marketplace**
   - Calls `GET /api/v1/assets/` (with optional filters for type and location).
3. **View Asset Details**
   - Calls `GET /api/v1/assets/{asset_id}` for more information.
4. **Express Interest**
   - Calls `POST /api/v1/interests/` with `asset_id` and an optional message.
5. **Track Interest Status**
   - Calls `GET /api/v1/interests/mine` to see which interests are pending/accepted.

This provides a **transparent, peer‑to‑peer discovery and matching mechanism**.

---



### 9. Team Workflow & Branching (Git)

- **main**  
  - Stable branch used for final demo of the prototype.

- **develop**  
  - Integration branch where backend (API) and frontend (UI) work are merged.

- **Features‑API**  
  - Backend developer branch.  
  - Implements FastAPI routes, DB models, CRUD, security.

- **Features‑UI**  
  - Frontend developer branch.  
  - Builds HTML/CSS/JS pages that call the backend APIs.

This workflow keeps **frontend and backend work decoupled** while still aligning on a common API contract.

---

### 10. Future Enhancements

- Add **real‑time updates** or notifications when interests are accepted.
- Add **pricing analytics** (average tariffs, capacity utilization).
- Integrate a **payment gateway** or escrow logic for energy contracts.
- Add **community features** (ratings, reviews, local energy communities).
