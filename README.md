# Drug Repurposing Platform - Frontend

A modern React + Vite frontend for an AI-powered drug repurposing platform that transforms the slow, manual process of drug discovery into a fast, intelligent workflow.

## Features

- 🚀 **Fast & Modern UI** - Built with React, Vite, and Tailwind CSS
- 🔍 **Intelligent Search** - Search for drug repurposing opportunities
- 📊 **Comprehensive Reports** - View research papers, clinical trials, patents, and market feasibility
- 🎨 **Beautiful Design** - Modern, responsive UI with smooth animations
- ⚡ **Lightning Fast** - Optimized build with Vite

## Getting Started

### Prerequisites

- Node.js (v18 or higher)
- npm or yarn

### Installation

1. Install dependencies:
```bash
npm install
```

2. Start the development server:
```bash
npm run dev
```

3. Open your browser and navigate to `http://localhost:5173`

### Build for Production

```bash
npm run build
```

The built files will be in the `dist` directory.

### Preview Production Build

```bash
npm run preview
```

## Project Structure

```
druggs/
├── src/
│   ├── components/
│   │   ├── Header.jsx           # Navigation header
│   │   ├── Hero.jsx             # Hero section with key features
│   │   ├── SearchInterface.jsx  # Drug search form
│   │   ├── RepurposeabilityReport.jsx  # Main report display
│   │   ├── ResearchPapers.jsx   # Research papers component
│   │   ├── ClinicalTrials.jsx   # Clinical trials component
│   │   ├── Patents.jsx          # Patents component
│   │   ├── MarketFeasibility.jsx # Market analysis component
│   │   └── Features.jsx         # Features showcase
│   ├── App.jsx                  # Main application component
│   ├── main.jsx                 # Application entry point
│   └── index.css                # Global styles with Tailwind
├── index.html                   # HTML template
├── package.json                 # Dependencies and scripts
├── vite.config.js              # Vite configuration
└── tailwind.config.js          # Tailwind CSS configuration
```

## Technologies Used

- **React 18** - UI library
- **Vite** - Build tool and dev server
- **Tailwind CSS** - Utility-first CSS framework
- **Lucide React** - Icon library
- **Framer Motion** - Animation library (available for future use)

## Features Overview

### Search Interface
- Enter drug name and target condition
- Real-time form validation
- Loading states during analysis

### Repurposeability Report
- **Repurposeability Score** - Overall viability score (0-100)
- **Research Papers** - Relevant scientific publications with relevance scores
- **Clinical Trials** - Ongoing and completed trials
- **Patent Landscape** - Patent status and IP opportunities
- **Market Feasibility** - Market size, growth, competition, and regulatory pathway
- **Key Recommendations** - Actionable insights

## API Integration

Currently, the app uses mock data. To integrate with your backend API:

1. Update the `handleSearch` function in `App.jsx`
2. Replace the `setTimeout` mock with an actual API call:

```javascript
const handleSearch = async (query) => {
  setSearchQuery(query)
  setIsLoading(true)
  
  try {
    const response = await fetch('/api/repurposeability-report', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(query)
    })
    const data = await response.json()
    setReportData(data)
  } catch (error) {
    console.error('Error fetching report:', error)
  } finally {
    setIsLoading(false)
  }
}
```

## Customization

### Colors
Edit `tailwind.config.js` to customize the color scheme. The primary color is currently set to blue.

### Components
All components are modular and can be easily customized or extended in the `src/components/` directory.

## License

MIT

