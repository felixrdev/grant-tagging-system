import { useState } from 'react'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { Toaster } from 'sonner'
import { AddGrants } from './components/AddGrants'
import { Browse } from './components/Browse'

const queryClient = new QueryClient()

type Tab = 'add' | 'browse'

function App() {
  const [activeTab, setActiveTab] = useState<Tab>('add')

  return (
    <QueryClientProvider client={queryClient}>
      <div className="min-h-screen bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 py-8">
          <header className="mb-8">
            <h1 className="text-4xl font-bold text-gray-900 mb-2">
              Grant Tagging System
            </h1>
            <p className="text-lg text-gray-600">
              Automatically tag and organize your grants—fast and deterministic (no LLM required)
            </p>
          </header>

          <div className="bg-white rounded-lg shadow-sm border">
            <div className="border-b border-gray-200">
              <nav className="flex -mb-px">
                <button
                  onClick={() => setActiveTab('add')}
                  className={`px-6 py-3 text-sm font-medium border-b-2 transition-colors ${
                    activeTab === 'add'
                      ? 'border-blue-600 text-blue-600'
                      : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                  }`}
                >
                  Add Grants
                </button>
                <button
                  onClick={() => setActiveTab('browse')}
                  className={`px-6 py-3 text-sm font-medium border-b-2 transition-colors ${
                    activeTab === 'browse'
                      ? 'border-blue-600 text-blue-600'
                      : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                  }`}
                >
                  Browse Grants
                </button>
              </nav>
            </div>

            <div className="p-6">
              {activeTab === 'add' ? <AddGrants /> : <Browse />}
            </div>
          </div>
        </div>
      </div>
      <Toaster position="top-right" richColors />
    </QueryClientProvider>
  )
}

export default App
