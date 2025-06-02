# MyBioTracker 🧬

## Overview

MyBioTracker is a modern, privacy-focused and fully local-first web application for nutrition, fitness and biohacking. Built with FastAPI and Vue.js, it calculates individual nutrient needs, lets you track caffeine intake and meals.

## Features

### Core Functionality
- **Nutrition Tracking**: Complete food database with barcode scanning
- **Caffeine Monitoring**: Real-time caffeine level tracking with decay curves
- **Biohacking Tools**: Advanced analytics for self-optimization
- **Privacy First**: All data stored locally, no external tracking

## Quick Start

### Prerequisites
- docker-compose

### Production Deployment

1. **Clone the repository**
```bash
git clone https://github.com/lytexdev/MyBioTracker.git
cd MyBioTracker
```

2. **Configure environment**
```bash
cp env.example .env
# Edit .env with your settings
```

3. **Start the application**
```bash
docker-compose up -d
```

4. **Access the application**
- App: http://localhost:80
- API: http://localhost:8000

## Features

### Nutrition Tracking
- **Food Database**: 10,000+ foods from OpenFoodFacts (stored locally)
- **Barcode Scanner**: Camera and upload support
- **Meal Planning**: Track breakfast, lunch, dinner, snacks
- **Macro & Micro Nutrients**: Complete nutritional analysis
- **Daily Goals**: Personalized targets based on user profile

### Caffeine Tracking
- **Real-time Levels**: Live caffeine concentration in bloodstream
- **Decay Curves**: Scientific half-life calculations
- **Product Library**: Coffee, tea, energy drinks, supplements
- **Optimization**: Timing recommendations for peak performance

### User Profile & Goals
- **Biometric Tracking**: Age, weight, height, body fat percentage
- **Activity Levels**: Sedentary to extremely active
- **Goal Setting**: Weight loss, muscle gain, maintenance
- **Calculations**: BMR, TDEE, macro distributions

### Analytics & Reports
- **Daily Summaries**: Complete nutrition breakdown
- **Trend Analysis**: Weekly and monthly patterns
- **Export Options**: JSON, CSV, Markdown formats
- **Visual Charts**: Interactive graphs with Chart.js

## License
This project is licensed under the **GNU Affero General Public License v3.0** – see the [LICENSE](LICENSE) file for details.
