# Sono-Eval Frontend

Modern web interface for the Sono-Eval developer assessment platform, built with Next.js 14, TypeScript, and TailwindCSS.

## Features

- 🎨 **Modern UI**: Clean, responsive design with TailwindCSS
- ⚡ **Fast**: Server-side rendering with Next.js 14
- 🔄 **Real-time Data**: React Query for efficient data fetching and caching
- 📊 **Analytics**: Interactive charts with Chart.js
- 🔐 **Secure**: JWT authentication with automatic token management
- 📱 **Responsive**: Mobile-first design approach

## Getting Started

### Prerequisites

- Node.js 18+
- npm or yarn
- Sono-Eval backend API running (default: <http://localhost:8000>)

### Installation

```bash
# Install dependencies
npm install

# Create environment file
cp .env.local.example .env.local

# Edit .env.local and set your API URL
# NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Development

```bash
# Start development server
npm run dev

# Open http://localhost:3000
```

### Build

```bash
# Create production build
npm run build

# Start production server
npm run start
```

## Project Structure

```
frontend/
├── app/                    # Next.js app directory
│   ├── assessments/       # Assessment pages
│   ├── layout.tsx         # Root layout
│   └── page.tsx           # Homepage
├── components/            # React components
│   ├── ui/               # Reusable UI components
│   └── Navigation.tsx     # Main navigation
├── lib/                   # Utilities and hooks
│   ├── hooks/            # Custom React hooks
│   ├── api-client.ts     # Axios API client
│   └── providers.tsx      # React Query provider
└── types/                 # TypeScript type definitions
    └── assessment.ts      # Assessment models
```

## Environment Variables

Create a `.env.local` file with the following variables:

```env
# API Configuration
NEXT_PUBLIC_API_URL=http://localhost:8000

# Development
NODE_ENV=development
```

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Create production build
- `npm run start` - Start production server
- `npm run lint` - Run ESLint

## Technologies

- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Styling**: TailwindCSS
- **State Management**: React Query (TanStack Query)
- **HTTP Client**: Axios
- **Charts**: Chart.js + react-chartjs-2
- **Date Utilities**: date-fns

## Features Implemented

### Phase 5a: Frontend Foundation ✅

- [x] Next.js 14 project setup with TypeScript
- [x] TailwindCSS configuration
- [x] React Query provider setup
- [x] API client with authentication
- [x] Base layout and navigation
- [x] Reusable UI components (Card, Button, Badge)
- [x] Homepage with features grid
- [x] Assessments list page
- [x] TypeScript types for API models

### Coming in Phase 5b: Assessment Views

- [ ] Single assessment detail page
- [ ] Score visualization components
- [ ] Micro-motive display
- [ ] Export functionality (PDF, JSON)

### Coming in Phase 5c: Analytics Dashboard

- [ ] Interactive charts
- [ ] Filter controls
- [ ] Trend analysis
- [ ] Path breakdown visualization

### Coming in Phase 5d: Batch Processing

- [ ] Batch upload interface
- [ ] Progress tracking
- [ ] Results download

## License

MIT License - see parent repository for details

## Support

For issues and questions, please refer to the main S ono-Eval repository.
