# MyBioTracker 🧬

## Overview

MyBioTracker is a modern, privacy-focused and fully local-first web application for nutrition, fitness and biohacking. Built with FastAPI and Vue.js, it calculates individual nutrient needs, lets you track caffeine intake and meals, and offers a clean Admin-Interface with two-factor authentication and QR-based product scanning.

## Installation

### Prerequisites

- `docker-compose`

### Clone the repository

```bash
git clone https://github.com/lytexdev/mybiotracker.git
cd mybiotracker
```

### Copy and rename the environment file

```bash
cp env.example .env
```

### Insert your secret keys in `.env`

```bash
JWT_SECRET_KEY=your-super-secret-jwt-key
JWT_REFRESH_SECRET_KEY=your-super-secret-refresh-key
```

### Build the application

```bash
chmod +x build
./build
```

### Run the Docker containers

```bash
docker-compose up -d
```

### Access the application
By default, the app will be available at [http://localhost:8000](http://localhost:8000)

---

## Features

* 🌿 Local-first: No cloud, full data ownership
* 📸 QR-Scanner for food product recognition
* 🔐 2FA with TOTP and downloadable backup codes
* 📊 Nutrient and calorie tracking based on body composition
* ☕ Caffeine tracker with real-time decay simulation
* 🧑‍💻 Admin interface for user and content management

---

## License

This project is licensed under the **GNU Affero General Public License v3.0** – see the [LICENSE](LICENSE) file for details.
