import { Search, Loader2 } from 'lucide-react'
import { useState } from 'react'

export default function SearchInterface({ onSearch, isLoading }) {
  const [drugName, setDrugName] = useState('')
  const [targetCondition, setTargetCondition] = useState('')

  const handleSubmit = (e) => {
    e.preventDefault()
    if (drugName.trim() && targetCondition.trim()) {
      onSearch({ drugName: drugName.trim(), targetCondition: targetCondition.trim() })
    }
  }

  return (
    <section className="py-16 px-4 bg-white">
      <div className="max-w-4xl mx-auto">
        <div className="text-center mb-12">
          <h2 className="text-3xl font-bold text-gray-900 mb-4">
            Discover Repurposing Opportunities
          </h2>
          <p className="text-gray-600">
            Enter a drug name and target condition to generate your Repurposeability Report
          </p>
        </div>

        <form onSubmit={handleSubmit} className="card">
          <div className="space-y-6">
            <div>
              <label htmlFor="drugName" className="block text-sm font-medium text-gray-700 mb-2">
                Drug Name
              </label>
              <input
                type="text"
                id="drugName"
                value={drugName}
                onChange={(e) => setDrugName(e.target.value)}
                placeholder="e.g., Metformin, Aspirin, Sildenafil, Thalidomide, Zinc"
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent outline-none transition"
                required
              />
            </div>

            <div>
              <label htmlFor="targetCondition" className="block text-sm font-medium text-gray-700 mb-2">
                Target Condition
              </label>
              <input
                type="text"
                id="targetCondition"
                value={targetCondition}
                onChange={(e) => setTargetCondition(e.target.value)}
                placeholder="e.g., Cancer, PCOS, Cardiovascular Disease, Pulmonary Hypertension, Multiple Myeloma, Diarrhea"
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent outline-none transition"
                required
              />
            </div>

            <button
              type="submit"
              disabled={isLoading || !drugName.trim() || !targetCondition.trim()}
              className="btn-primary w-full flex items-center justify-center space-x-2 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isLoading ? (
                <>
                  <Loader2 className="h-5 w-5 animate-spin" />
                  <span>Analyzing...</span>
                </>
              ) : (
                <>
                  <Search className="h-5 w-5" />
                  <span>Generate Repurposeability Report</span>
                </>
              )}
            </button>
          </div>
        </form>

        <div className="mt-8">
          <div className="bg-primary-50 border border-primary-200 rounded-lg p-4 mb-4">
            <h3 className="text-sm font-semibold text-primary-900 mb-2">Example Searches:</h3>
            <ul className="text-sm text-primary-700 space-y-1">
              <li>• <strong>Metformin</strong> for <strong>Cancer</strong> - Well-documented repurposing case</li>
              <li>• <strong>Metformin</strong> for <strong>PCOS</strong> - FDA-approved off-label use</li>
              <li>• <strong>Aspirin</strong> for <strong>Cardiovascular Disease</strong> - Established prevention use</li>
              <li>• <strong>Sildenafil</strong> for <strong>Pulmonary Hypertension</strong> - FDA-approved as Revatio</li>
              <li>• <strong>Zinc</strong> for <strong>Diarrhea</strong> - WHO-recommended adjunct to ORS</li>
            </ul>
          </div>
          <div className="text-center text-sm text-gray-500">
            <p className="flex items-center justify-center space-x-2">
              <span className="inline-block w-2 h-2 bg-primary-600 rounded-full animate-pulse"></span>
              <span>AI agents are analyzing research papers, clinical trials, and patents...</span>
            </p>
          </div>
        </div>
      </div>
    </section>
  )
}

