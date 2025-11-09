import { useState } from 'react'
import { toast } from 'sonner'
import { GrantCard } from './GrantCard'
import { useBatchTagGrants } from '@/lib/hooks'
import { GrantInputArraySchema, type Grant } from '@/lib/types'

const SAMPLE_JSON = `[
  {
    "grant_name": "Sustainable Agriculture Research Grant",
    "grant_description": "Funding for projects that promote organic farming practices and soil conservation."
  },
  {
    "grant_name": "STEM Education Initiative",
    "grant_description": "Support for programs that encourage high school students to pursue careers in science, technology, engineering, and mathematics."
  }
]`

export function AddGrants() {
  const [jsonInput, setJsonInput] = useState('')
  const [previewGrants, setPreviewGrants] = useState<Grant[] | null>(null)
  const batchTagMutation = useBatchTagGrants()

  const handleValidate = () => {
    try {
      const parsed = JSON.parse(jsonInput)
      const validated = GrantInputArraySchema.parse(parsed)

      setPreviewGrants(
        validated.map(g => ({
          ...g,
          tags: [],
          website_urls: g.website_urls || [],
          document_urls: g.document_urls || [],
        }))
      )
      toast.success(`Valid! Found ${validated.length} grant(s) ready to tag.`)
    } catch (error) {
      if (error instanceof Error) {
        toast.error(`Invalid JSON: ${error.message}`)
      } else {
        toast.error('Invalid JSON format')
      }
      setPreviewGrants(null)
    }
  }

  const handleSend = async () => {
    if (!previewGrants) {
      toast.error('Please validate your input first')
      return
    }

    try {
      const result = await batchTagMutation.mutateAsync(previewGrants)
      setPreviewGrants(result)
      toast.success(
        `Successfully tagged ${result.length} grant(s)! Check the Browse tab.`
      )
      setJsonInput('')
    } catch (error) {
      if (error instanceof Error) {
        toast.error(`Failed to tag grants: ${error.message}`)
      } else {
        toast.error('Failed to tag grants')
      }
    }
  }

  const loadSample = () => {
    setJsonInput(SAMPLE_JSON)
    setPreviewGrants(null)
  }

  return (
    <div className="space-y-6">
      <div>
        <div className="flex items-center justify-between mb-2">
          <label className="block text-sm font-medium text-gray-700">
            Paste your grants JSON here
          </label>
          <button
            onClick={loadSample}
            className="text-sm text-blue-600 hover:text-blue-700 underline"
          >
            Load sample
          </button>
        </div>
        <textarea
          value={jsonInput}
          onChange={e => setJsonInput(e.target.value)}
          placeholder='[{"grant_name": "...", "grant_description": "..."}]'
          className="w-full h-64 p-3 border border-gray-300 rounded-lg font-mono text-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        />
        <p className="mt-1 text-sm text-gray-500">
          Format: Array of objects with grant_name and grant_description
        </p>
      </div>

      <div className="flex gap-3">
        <button
          onClick={handleValidate}
          disabled={!jsonInput.trim()}
          className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors"
        >
          Validate & Preview
        </button>
        <button
          onClick={handleSend}
          disabled={!previewGrants || batchTagMutation.isPending}
          className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors"
        >
          {batchTagMutation.isPending ? 'Tagging...' : 'Send to Backend'}
        </button>
      </div>

      {previewGrants && previewGrants.length > 0 && (
        <div className="space-y-4">
          <h3 className="text-lg font-semibold text-gray-900">
            Preview ({previewGrants.length} grant
            {previewGrants.length !== 1 ? 's' : ''})
          </h3>
          <div className="grid gap-4 md:grid-cols-2">
            {previewGrants.map((grant, idx) => (
              <GrantCard key={idx} grant={grant} />
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
