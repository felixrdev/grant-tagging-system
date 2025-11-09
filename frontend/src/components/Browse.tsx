import { useState, useMemo, useEffect, useRef } from 'react'
import { GrantCard } from './GrantCard'
import { useGrants, useTags, useAdvancedSearch } from '@/lib/hooks'

export function Browse() {
  const [searchQuery, setSearchQuery] = useState('')
  const [debouncedQuery, setDebouncedQuery] = useState('')
  const [selectedTags, setSelectedTags] = useState<string[]>([])
  const [searchMode, setSearchMode] = useState<'all' | 'any'>('all')

  const { data: allGrants, isLoading: grantsLoading } = useGrants()
  const { data: tags, isLoading: tagsLoading } = useTags()
  const { data: searchResults } = useAdvancedSearch(
    debouncedQuery || undefined,
    selectedTags.length > 0 ? selectedTags : undefined,
    searchMode
  )

  const debounceTimer = useRef<ReturnType<typeof setTimeout> | null>(null)

  useEffect(() => {
    if (debounceTimer.current) {
      clearTimeout(debounceTimer.current)
    }
    debounceTimer.current = setTimeout(() => {
      setDebouncedQuery(searchQuery)
    }, 300)

    return () => {
      if (debounceTimer.current) {
        clearTimeout(debounceTimer.current)
      }
    }
  }, [searchQuery])

  const handleSearchChange = (value: string) => {
    setSearchQuery(value)
  }

  const displayGrants =
    debouncedQuery || selectedTags.length > 0
      ? searchResults?.grants
      : allGrants

  const resolvedTags = searchResults?.resolved_tags || []

  const availableTags = useMemo(() => {
    return tags?.sort() || []
  }, [tags])

  const toggleTag = (tag: string) => {
    setSelectedTags(prev =>
      prev.includes(tag) ? prev.filter(t => t !== tag) : [...prev, tag]
    )
  }

  const clearFilters = () => {
    setSelectedTags([])
    setSearchQuery('')
    setDebouncedQuery('')
  }

  if (grantsLoading || tagsLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-gray-500">Loading grants...</div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div className="bg-white border rounded-lg p-4">
        <div className="space-y-4">
          <div>
            <label
              htmlFor="search"
              className="block text-sm font-semibold text-gray-900 mb-2"
            >
              Search grants
            </label>
            <input
              id="search"
              type="text"
              value={searchQuery}
              onChange={e => handleSearchChange(e.target.value)}
              placeholder="e.g., learning, irrigation, local food..."
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none"
            />
            {resolvedTags.length > 0 && (
              <div className="mt-2 flex flex-wrap gap-1.5">
                <span className="text-xs text-gray-600">Searching for:</span>
                {resolvedTags.map(tag => (
                  <span
                    key={tag}
                    className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-blue-100 text-blue-800"
                  >
                    {tag}
                  </span>
                ))}
              </div>
            )}
          </div>

          <div>
            <div className="flex items-center justify-between mb-3">
              <h3 className="text-sm font-semibold text-gray-900">
                Filter by tags
              </h3>
              <div className="flex items-center gap-4">
                <div className="flex items-center gap-2">
                  <label className="text-xs text-gray-600">Match:</label>
                  <select
                    value={searchMode}
                    onChange={e =>
                      setSearchMode(e.target.value as 'all' | 'any')
                    }
                    className="text-xs border border-gray-300 rounded px-2 py-1"
                  >
                    <option value="all">All tags</option>
                    <option value="any">Any tag</option>
                  </select>
                </div>
                {(selectedTags.length > 0 || searchQuery) && (
                  <button
                    onClick={clearFilters}
                    className="text-sm text-blue-600 hover:text-blue-700 underline"
                  >
                    Clear all
                  </button>
                )}
              </div>
            </div>
            <div className="flex flex-wrap gap-2 max-h-48 overflow-y-auto">
              {availableTags.map(tag => (
                <button
                  key={tag}
                  onClick={() => toggleTag(tag)}
                  className={`px-3 py-1.5 text-sm font-medium rounded-full transition-colors ${
                    selectedTags.includes(tag)
                      ? 'bg-blue-600 text-white'
                      : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                  }`}
                >
                  {tag}
                </button>
              ))}
            </div>
          </div>
        </div>
      </div>

      <div>
        {!displayGrants || displayGrants.length === 0 ? (
          <div className="text-center py-12 bg-gray-50 rounded-lg border-2 border-dashed">
            <svg
              className="mx-auto h-12 w-12 text-gray-400"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
              />
            </svg>
            <h3 className="mt-2 text-sm font-medium text-gray-900">
              {selectedTags.length > 0 || searchQuery
                ? 'No matching grants'
                : 'No grants yet'}
            </h3>
            <p className="mt-1 text-sm text-gray-500">
              {selectedTags.length > 0 || searchQuery
                ? 'Try adjusting your search or filters, or add some grants first.'
                : 'Get started by adding some grants in the Add Grants tab.'}
            </p>
          </div>
        ) : (
          <>
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold text-gray-900">
                {displayGrants.length} grant
                {displayGrants.length !== 1 ? 's' : ''}
              </h3>
            </div>
            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
              {displayGrants.map((grant, idx) => (
                <GrantCard key={idx} grant={grant} />
              ))}
            </div>
          </>
        )}
      </div>
    </div>
  )
}
