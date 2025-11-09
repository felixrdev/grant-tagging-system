import {
  AdvancedSearchResponse,
  AdvancedSearchResponseSchema,
  Grant,
  GrantInput,
  GrantsArraySchema,
  TagsArraySchema,
} from './types'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

class ApiClient {
  private baseUrl: string

  constructor(baseUrl: string) {
    this.baseUrl = baseUrl
  }

  async getTags(): Promise<string[]> {
    const response = await fetch(`${this.baseUrl}/api/tags`)
    if (!response.ok) {
      throw new Error('Failed to fetch tags')
    }
    const data = await response.json()
    return TagsArraySchema.parse(data)
  }

  async getGrants(): Promise<Grant[]> {
    const response = await fetch(`${this.baseUrl}/api/grants`)
    if (!response.ok) {
      throw new Error('Failed to fetch grants')
    }
    const data = await response.json()
    return GrantsArraySchema.parse(data)
  }

  async batchTagGrants(grants: GrantInput[]): Promise<Grant[]> {
    const response = await fetch(`${this.baseUrl}/api/grants/batch`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(grants),
    })

    if (!response.ok) {
      const error = await response.json().catch(() => ({}))
      throw new Error(error.error || 'Failed to tag grants')
    }

    const data = await response.json()
    return GrantsArraySchema.parse(data)
  }

  async searchGrants(tags: string[]): Promise<Grant[]> {
    const tagsParam = tags.join(',')
    const response = await fetch(
      `${this.baseUrl}/api/search?tags=${encodeURIComponent(tagsParam)}`
    )
    if (!response.ok) {
      throw new Error('Failed to search grants')
    }
    const data = await response.json()
    return GrantsArraySchema.parse(data)
  }

  async advancedSearch(
    query?: string,
    tags?: string[],
    mode: 'all' | 'any' = 'all'
  ): Promise<AdvancedSearchResponse> {
    const params = new URLSearchParams()
    if (query) params.append('q', query)
    if (tags && tags.length > 0) params.append('tags', tags.join(','))
    params.append('mode', mode)

    const response = await fetch(
      `${this.baseUrl}/api/search/advanced?${params.toString()}`
    )
    if (!response.ok) {
      throw new Error('Failed to perform advanced search')
    }
    const data = await response.json()
    return AdvancedSearchResponseSchema.parse(data)
  }
}

export const apiClient = new ApiClient(API_BASE_URL)
