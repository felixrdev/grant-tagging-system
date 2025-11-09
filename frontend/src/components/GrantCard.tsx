import { Grant } from '@/lib/types'

interface GrantCardProps {
  grant: Grant
}

export function GrantCard({ grant }: GrantCardProps) {
  return (
    <div className="border rounded-lg p-4 shadow-sm hover:shadow-md transition-shadow bg-white">
      <h3 className="text-lg font-semibold text-gray-900 mb-2">
        {grant.grant_name}
      </h3>
      <p className="text-sm text-gray-600 mb-3 line-clamp-3">
        {grant.grant_description}
      </p>
      {grant.tags && grant.tags.length > 0 && (
        <div className="flex flex-wrap gap-2">
          {grant.tags.map(tag => (
            <span
              key={tag}
              className="px-2 py-1 text-xs font-medium bg-blue-100 text-blue-700 rounded-full"
            >
              {tag}
            </span>
          ))}
        </div>
      )}
    </div>
  )
}
