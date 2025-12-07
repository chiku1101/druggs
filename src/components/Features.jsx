import { Search, FileText, Briefcase, TrendingUp, Zap, Shield } from 'lucide-react'

export default function Features() {
  const features = [
    {
      icon: Search,
      title: 'Global Research Scan',
      description: 'Automatically scans millions of research papers from PubMed, arXiv, and other global databases'
    },
    {
      icon: FileText,
      title: 'Clinical Trial Analysis',
      description: 'Comprehensive analysis of ongoing and completed clinical trials worldwide'
    },
    {
      icon: Briefcase,
      title: 'Patent Intelligence',
      description: 'Real-time patent landscape analysis with clear visibility on IP opportunities'
    },
    {
      icon: TrendingUp,
      title: 'Market Feasibility',
      description: 'Trade and market analysis to assess commercial viability and competition'
    },
    {
      icon: Zap,
      title: 'AI-Powered Insights',
      description: 'Multi-agent AI system that validates data and generates actionable recommendations'
    },
    {
      icon: Shield,
      title: 'Regulatory Guidance',
      description: 'Clear regulatory pathway recommendations based on FDA and global guidelines'
    }
  ]

  return (
    <section id="features" className="py-16 px-4 bg-white">
      <div className="max-w-7xl mx-auto">
        <div className="text-center mb-12">
          <h2 className="text-3xl font-bold text-gray-900 mb-4">
            Everything You Need in One Platform
          </h2>
          <p className="text-gray-600 max-w-2xl mx-auto">
            Our multi-agent AI system unites scientific, legal, and market insights 
            to deliver comprehensive repurposing intelligence
          </p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
          {features.map((feature, idx) => {
            const Icon = feature.icon
            return (
              <div key={idx} className="card hover:shadow-xl transition-shadow">
                <div className="bg-primary-100 w-12 h-12 rounded-lg flex items-center justify-center mb-4">
                  <Icon className="h-6 w-6 text-primary-600" />
                </div>
                <h3 className="text-xl font-semibold mb-2 text-gray-900">
                  {feature.title}
                </h3>
                <p className="text-gray-600">
                  {feature.description}
                </p>
              </div>
            )
          })}
        </div>
      </div>
    </section>
  )
}

