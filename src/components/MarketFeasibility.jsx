import { TrendingUp, DollarSign, Users, Clock, CheckCircle } from 'lucide-react'

export default function MarketFeasibility({ data }) {
  const metrics = [
    { icon: DollarSign, label: 'Market Size', value: data.marketSize },
    { icon: TrendingUp, label: 'Growth Rate', value: data.growthRate },
    { icon: Users, label: 'Competition', value: data.competition },
    { icon: Clock, label: 'Timeline', value: data.timeline },
  ]

  return (
    <div className="card">
      <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6 mb-6">
        {metrics.map((metric, idx) => {
          const Icon = metric.icon
          return (
            <div key={idx} className="text-center">
              <div className="bg-primary-100 w-12 h-12 rounded-full flex items-center justify-center mx-auto mb-3">
                <Icon className="h-6 w-6 text-primary-600" />
              </div>
              <div className="text-2xl font-bold text-gray-900 mb-1">{metric.value}</div>
              <div className="text-sm text-gray-600">{metric.label}</div>
            </div>
          )
        })}
      </div>

      <div className="border-t pt-6">
        <div className="flex items-start space-x-3">
          <CheckCircle className="h-5 w-5 text-green-600 mt-0.5 flex-shrink-0" />
          <div>
            <h4 className="font-semibold text-gray-900 mb-1">Regulatory Pathway</h4>
            <p className="text-gray-700">{data.regulatoryPath}</p>
          </div>
        </div>
      </div>
    </div>
  )
}

