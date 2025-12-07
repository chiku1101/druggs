import { ArrowLeft, FileText, ClipboardList, Briefcase, TrendingUp, CheckCircle, AlertCircle } from 'lucide-react'
import ResearchPapers from './ResearchPapers'
import ClinicalTrials from './ClinicalTrials'
import Patents from './Patents'
import MarketFeasibility from './MarketFeasibility'

export default function RepurposeabilityReport({ data, onNewSearch }) {
  const getScoreColor = (score) => {
    if (score >= 80) return 'text-green-600 bg-green-100'
    if (score >= 60) return 'text-yellow-600 bg-yellow-100'
    return 'text-red-600 bg-red-100'
  }

  return (
    <div className="py-8 px-4 bg-gray-50 min-h-screen">
      <div className="max-w-7xl mx-auto">
        <button
          onClick={onNewSearch}
          className="mb-6 flex items-center space-x-2 text-gray-600 hover:text-primary-600 transition-colors"
        >
          <ArrowLeft className="h-5 w-5" />
          <span>New Search</span>
        </button>

        {/* Header Section */}
        <div className="card mb-8">
          <div className="flex flex-col md:flex-row md:items-center md:justify-between mb-6">
            <div>
              <h1 className="text-3xl font-bold text-gray-900 mb-2">
                Repurposeability Report
              </h1>
              <p className="text-gray-600">
                <span className="font-semibold">{data.drugName}</span> for{' '}
                <span className="font-semibold">{data.targetCondition}</span>
              </p>
            </div>
            <div className={`mt-4 md:mt-0 px-6 py-3 rounded-lg ${getScoreColor(data.repurposeabilityScore)}`}>
              <div className="text-sm font-medium mb-1">Repurposeability Score</div>
              <div className="text-3xl font-bold">{data.repurposeabilityScore}/100</div>
            </div>
          </div>

          {/* Recommendations */}
          <div className="border-t pt-6">
            <h3 className="text-lg font-semibold mb-4 flex items-center space-x-2">
              <CheckCircle className="h-5 w-5 text-green-600" />
              <span>Key Recommendations</span>
            </h3>
            <ul className="space-y-2">
              {data.recommendations.map((rec, idx) => (
                <li key={idx} className="flex items-start space-x-2 text-gray-700">
                  <CheckCircle className="h-5 w-5 text-green-600 mt-0.5 flex-shrink-0" />
                  <span>{rec}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>

        {/* Research Papers Section */}
        <div className="mb-8">
          <div className="flex items-center space-x-2 mb-4">
            <FileText className="h-6 w-6 text-primary-600" />
            <h2 className="text-2xl font-bold text-gray-900">Research Papers</h2>
          </div>
          <ResearchPapers papers={data.researchPapers} />
        </div>

        {/* Clinical Trials Section */}
        <div className="mb-8">
          <div className="flex items-center space-x-2 mb-4">
            <ClipboardList className="h-6 w-6 text-primary-600" />
            <h2 className="text-2xl font-bold text-gray-900">Clinical Trials</h2>
          </div>
          <ClinicalTrials trials={data.clinicalTrials} />
        </div>

        {/* Patents Section */}
        <div className="mb-8">
          <div className="flex items-center space-x-2 mb-4">
            <Briefcase className="h-6 w-6 text-primary-600" />
            <h2 className="text-2xl font-bold text-gray-900">Patent Landscape</h2>
          </div>
          <Patents patents={data.patents} />
        </div>

        {/* Market Feasibility Section */}
        <div className="mb-8">
          <div className="flex items-center space-x-2 mb-4">
            <TrendingUp className="h-6 w-6 text-primary-600" />
            <h2 className="text-2xl font-bold text-gray-900">Market Feasibility</h2>
          </div>
          <MarketFeasibility data={data.marketFeasibility} />
        </div>
      </div>
    </div>
  )
}

