import { Clapperboard } from 'lucide-react'
import { cn } from '@/lib/utils'

// Stand-in until movies have poster images in the database
function MoviePoster({ className }: { className?: string }) {
  return (
    <div className={cn('flex aspect-2/3 items-center justify-center rounded-lg bg-muted text-muted-foreground', className)}>
      <Clapperboard className="size-10" />
    </div>
  )
}

export default MoviePoster
