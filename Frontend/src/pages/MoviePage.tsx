import { ArrowLeft } from 'lucide-react'
import { useEffect, useState } from 'react'
import { Link, useParams } from 'react-router'
import MoviePoster from '@/components/MoviePoster'
import { Badge } from '@/components/ui/badge'
import { buttonVariants } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { API_URL, formatGenre, type Movie } from '@/lib/api'

function MoviePage() {
  const { movieId } = useParams()
  const [movie, setMovie] = useState<Movie | null>(null)
  const [error, setError] = useState(false)

  useEffect(() => {
    fetch(`${API_URL}/movies/${movieId}`)
      .then((response) => {
        if (!response.ok) {
          throw new Error('Backend returned an error')
        }

        return response.json()
      })
      .then(setMovie)
      .catch((error) => {
        console.error('Movie fetch failed:', error)
        setError(true)
      })
  }, [movieId])

  return (
    <main className="mx-auto max-w-3xl p-6">
      <Link to="/" className={buttonVariants({ variant: 'ghost', className: 'mb-4' })}>
        <ArrowLeft /> All films
      </Link>

      {error && <p className="text-muted-foreground">Movie not found.</p>}

      {movie && (
        <Card className="grid gap-6 p-6 sm:grid-cols-[200px_1fr]">
          <MoviePoster />
          <div>
            <CardHeader className="px-0">
              <CardTitle className="text-3xl font-bold">{movie.name}</CardTitle>
            </CardHeader>
            <CardContent className="mt-6 divide-y border-y px-0">
              <div className="flex items-center justify-between gap-4 py-3">
                <span className="text-muted-foreground">Genres</span>
                <div className="flex flex-wrap justify-end gap-1">
                  {movie.genres.map((genre) => (
                    <Badge key={genre} variant="secondary">{formatGenre(genre)}</Badge>
                  ))}
                </div>
              </div>
              <div className="flex items-center justify-between gap-4 py-3">
                <span className="text-muted-foreground">Film no.</span>
                <span>{movie.id}</span>
              </div>
            </CardContent>
          </div>
        </Card>
      )}
    </main>
  )
}

export default MoviePage
