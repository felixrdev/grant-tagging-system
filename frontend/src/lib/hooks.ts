import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { apiClient } from './api'
import { GrantInput } from './types'

export const useGrants = () => {
  return useQuery({
    queryKey: ['grants'],
    queryFn: () => apiClient.getGrants(),
  })
}

export const useTags = () => {
  return useQuery({
    queryKey: ['tags'],
    queryFn: () => apiClient.getTags(),
  })
}

export const useSearchGrants = (tags: string[]) => {
  return useQuery({
    queryKey: ['grants', 'search', tags],
    queryFn: () => apiClient.searchGrants(tags),
    enabled: tags.length > 0,
  })
}

export const useAdvancedSearch = (
  query?: string,
  tags?: string[],
  mode: 'all' | 'any' = 'all'
) => {
  return useQuery({
    queryKey: ['grants', 'advanced-search', query, tags, mode],
    queryFn: () => apiClient.advancedSearch(query, tags, mode),
    enabled: !!query || (!!tags && tags.length > 0),
  })
}

export const useBatchTagGrants = () => {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (grants: GrantInput[]) => apiClient.batchTagGrants(grants),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['grants'] })
    },
  })
}
