import { Briefcase, Calendar, Building2, FileCheck } from 'lucide-react'

export default function Patents({ patents }) {
  const getStatusColor = (status) => {
    const colors = {
      'Pending': 'bg-yellow-100 text-yellow-800',
      'Granted': 'bg-green-100 text-green-800',
      'Expired': 'bg-gray-100 text-gray-800',
      'Abandoned': 'bg-red-100 text-red-800',
    }
    return colors[status] || 'bg-gray-100 text-gray-800'
  }

  return (
    <div className="space-y-4">
      {patents.map((patent, idx) => (
        <div key={idx} className="card hover:shadow-xl transition-shadow">
          <div className="flex flex-col md:flex-row md:items-center md:justify-between mb-4">
            <div className="flex-1">
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                {patent.title}
              </h3>
              <div className="flex flex-wrap items-center gap-4 text-sm text-gray-600">
                <span className="flex items-center space-x-1">
                  <FileCheck className="h-4 w-4" />
                  <span className="font-mono">{patent.number}</span>
                </span>
                <span className="flex items-center space-x-1">
                  <Building2 className="h-4 w-4" />
                  <span>{patent.assignee}</span>
                </span>
                <span className="flex items-center space-x-1">
                  <Calendar className="h-4 w-4" />
                  <span>Filed: {patent.filingDate}</span>
                </span>
              </div>
            </div>
            <div className={`mt-4 md:mt-0 px-4 py-2 rounded-lg ${getStatusColor(patent.status)}`}>
              <span className="text-sm font-semibold">{patent.status}</span>
            </div>
          </div>
        </div>
      ))}
    </div>
  )
}

