import { ClipboardList, Calendar, Users, Activity } from 'lucide-react'

export default function ClinicalTrials({ trials }) {
  const getStatusColor = (status) => {
    const colors = {
      'Recruiting': 'bg-green-100 text-green-800',
      'Active': 'bg-blue-100 text-blue-800',
      'Completed': 'bg-gray-100 text-gray-800',
      'Terminated': 'bg-red-100 text-red-800',
    }
    return colors[status] || 'bg-gray-100 text-gray-800'
  }

  return (
    <div className="space-y-4">
      {trials.map((trial, idx) => (
        <div key={idx} className="card hover:shadow-xl transition-shadow">
          <div className="flex flex-col md:flex-row md:items-center md:justify-between mb-4">
            <div className="flex-1">
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                {trial.title}
              </h3>
              <div className="flex flex-wrap items-center gap-4 text-sm text-gray-600">
                <span className="flex items-center space-x-1">
                  <ClipboardList className="h-4 w-4" />
                  <span className="font-mono">{trial.id}</span>
                </span>
                <span className="flex items-center space-x-1">
                  <Activity className="h-4 w-4" />
                  <span>{trial.phase}</span>
                </span>
                <span className="flex items-center space-x-1">
                  <Users className="h-4 w-4" />
                  <span>{trial.participants} participants</span>
                </span>
                <span className="flex items-center space-x-1">
                  <Calendar className="h-4 w-4" />
                  <span>Completion: {trial.completionDate}</span>
                </span>
              </div>
            </div>
            <div className={`mt-4 md:mt-0 px-4 py-2 rounded-lg ${getStatusColor(trial.status)}`}>
              <span className="text-sm font-semibold">{trial.status}</span>
            </div>
          </div>
        </div>
      ))}
    </div>
  )
}

