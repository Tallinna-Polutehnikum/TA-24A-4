import { Link } from 'react-router'
import MoviePoster from '@/components/MoviePoster'
import { Badge } from '@/components/ui/badge'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { formatGenre, type Movie } from '@/lib/api'

function MovieCard({ movie }: { movie: Movie }) {
  return (
    <Link to={`/movies/${movie.id}`}>
      <Card className="h-full pt-0 transition-colors hover:bg-muted/50">
        <MoviePoster className="rounded-b-none" />
        <CardHeader>
          <CardTitle>{movie.name}</CardTitle>
        </CardHeader>
        <CardContent className="flex-row flex-wrap gap-1">
          {movie.genres.map((genre) => (
            <Badge key={genre} variant="secondary">{formatGenre(genre)}</Badge>
          ))}
        </CardContent>
      </Card>
    </Link>
  )
}

export default MovieCard
