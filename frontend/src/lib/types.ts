import { z } from 'zod'

export const GrantSchema = z.object({
  grant_name: z.string(),
  grant_description: z.string(),
  tags: z.array(z.string()),
  website_urls: z.array(z.string()).optional(),
  document_urls: z.array(z.string()).optional(),
})

export const GrantInputSchema = z.object({
  grant_name: z.string().min(1, 'Grant name is required'),
  grant_description: z.string().min(1, 'Grant description is required'),
  website_urls: z.array(z.string()).optional(),
  document_urls: z.array(z.string()).optional(),
})

export const GrantsArraySchema = z.array(GrantSchema)
export const GrantInputArraySchema = z.array(GrantInputSchema)
export const TagsArraySchema = z.array(z.string())

export const AdvancedSearchResponseSchema = z.object({
  resolved_tags: z.array(z.string()),
  grants: z.array(GrantSchema),
})

export type Grant = z.infer<typeof GrantSchema>
export type GrantInput = z.infer<typeof GrantInputSchema>
export type AdvancedSearchResponse = z.infer<typeof AdvancedSearchResponseSchema>
