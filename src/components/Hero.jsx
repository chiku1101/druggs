import { Sparkles, Zap, Shield } from 'lucide-react'

export default function Hero() {
  return (
    <section className="bg-gradient-to-br from-primary-50 via-white to-primary-50 py-20 px-4">
      <div className="max-w-7xl mx-auto">
        <div className="text-center mb-16">
          <h1 className="text-5xl md:text-6xl font-bold text-gray-900 mb-6">
            Transform Drug Repurposing from
            <span className="text-primary-600 block mt-2">Months to Minutes</span>
          </h1>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto mb-8">
            Our multi-agent AI platform automatically scans global research papers, 
            clinical trials, and patents to deliver ready-to-use Repurposeability Reports 
            in minutes, not months.
          </p>
        </div>

        <div className="grid md:grid-cols-3 gap-8 max-w-5xl mx-auto">
          <div className="card text-center">
            <div className="bg-primary-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
              <Sparkles className="h-8 w-8 text-primary-600" />
            </div>
            <h3 className="text-xl font-semibold mb-2">AI-Powered Discovery</h3>
            <p className="text-gray-600">
              Automatically scans millions of research papers and clinical data
            </p>
          </div>

          <div className="card text-center">
            <div className="bg-primary-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
              <Zap className="h-8 w-8 text-primary-600" />
            </div>
            <h3 className="text-xl font-semibold mb-2">Lightning Fast</h3>
            <p className="text-gray-600">
              Get comprehensive reports in minutes instead of months of manual work
            </p>
          </div>

          <div className="card text-center">
            <div className="bg-primary-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
              <Shield className="h-8 w-8 text-primary-600" />
            </div>
            <h3 className="text-xl font-semibold mb-2">Complete Insights</h3>
            <p className="text-gray-600">
              Scientific, legal, and market intelligence in one unified report
            </p>
          </div>
        </div>
      </div>
    </section>
  )
}

