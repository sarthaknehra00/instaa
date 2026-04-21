# InstaTrack: Instagram Intelligence Engine

InstaTrack is a sophisticated OSINT (Open Source Intelligence) tool designed to track and extract public interactions made by specified Instagram accounts. It combines a high-performance Python backend with a modern, glassmorphic Next.js frontend to provide real-time intelligence on user footprints across the network.

![InstaTrack Interface](https://via.placeholder.com/1200x600.png?text=InstaTrack+Interface+Mockup) 

## 🚀 Key Features

- **Passive OSINT Tracking**: Monitors public comments and interactions without requiring aggressive headless browsing or direct account access.
- **Neural Graph Scanning**: Deep-scans public Instagram posts to identify verified comments from target profiles.
- **Async Engine**: Built with FastAPI and `Instaloader`, utilizing background workers for non-blocking extraction.
- **Glassmorphic UI**: A premium, Gen-Z inspired dark-themed dashboard built with Next.js, Tailwind CSS, and Framer Motion.
- **Real-time Feedback**: Live progress tracking of scanning nodes and data extraction status.
- **Social Metadata**: Displays original post context, including thumbnails, timestamps, and direct links to verify interactions.

## 🛠️ Technology Stack

### Backend
- **Framework**: [FastAPI](https://fastapi.tiangolo.com/)
- **Core Engine**: [Instaloader](https://instaloader.github.io/)
- **Logic**: Async background tasks with `asyncio`
- **API Design**: Standardized JSON intelligence payloads

### Frontend
- **Framework**: [Next.js 15+](https://nextjs.org/)
- **Styling**: [Tailwind CSS](https://tailwindcss.com/)
- **Icons**: [Lucide React](https://lucide.dev/)
- **Aesthetics**: Glassmorphism with dynamic mesh gradients and micro-animations

## 🏁 Getting Started

### Prerequisites
- Python 3.9+
- Node.js 18+
- npm/yarn

### Backend Setup
1. Navigate to the `backend` directory:
   ```bash
   cd backend
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Start the API server:
   ```bash
   python main.py
   ```

### Frontend Setup
1. Navigate to the `frontend` directory:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the development server:
   ```bash
   npm run dev
   ```

## 🛡️ Ethical Use & Disclaimer
This tool is intended for **legitimate OSINT research and educational purposes only**. Users are responsible for complying with Instagram's [Terms of Service](https://help.instagram.com/581066165581870) and local privacy laws. The developers assume no liability for misuse or unauthorized data collection.

## 📜 License
MIT License - Copyright (c) 2026 Sarthak Nehra
