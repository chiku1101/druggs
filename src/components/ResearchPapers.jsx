import { FileText, Calendar, Users, TrendingUp } from 'lucide-react'

export default function ResearchPapers({ papers }) {
  return (
    <div className="space-y-4">
      {papers.map((paper, idx) => (
        <div key={idx} className="card hover:shadow-xl transition-shadow">
          <div className="flex items-start justify-between mb-3">
            <div className="flex-1">
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                {paper.title}
              </h3>
              <p className="text-sm text-gray-600 mb-2">
                {paper.authors} • {paper.journal} • {paper.year}
              </p>
            </div>
            <div className="ml-4 flex items-center space-x-1 bg-primary-100 text-primary-700 px-3 py-1 rounded-full">
              <TrendingUp className="h-4 w-4" />
              <span className="text-sm font-semibold">{paper.relevance}%</span>
            </div>
          </div>
          <p className="text-gray-700 leading-relaxed">{paper.summary}</p>
        </div>
      ))}
    </div>
  )
}

