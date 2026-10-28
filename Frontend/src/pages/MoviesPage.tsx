import { useEffect, useState } from 'react'
import MovieCard from '@/components/MovieCard'
import { API_URL, type Movie } from '@/lib/api'

function MoviesPage() {
  const [movies, setMovies] = useState<Movie[]>([])

  useEffect(() => {
    fetch(`${API_URL}/movies`)
      .then((response) => {
        if (!response.ok) {
          throw new Error('Backend returned an error')
        }

        return response.json()
      })
      .then(setMovies)
      .catch((error) => {
        console.error('Movies fetch failed:', error)
      })
  }, [])

  return (
    <main className="mx-auto max-w-6xl p-6">
      <h1 className="mb-6 font-heading text-3xl font-bold">Filmid</h1>

      <div className="grid grid-cols-2 gap-4 sm:grid-cols-3 lg:grid-cols-5">
        {movies.map((movie) => (
          <MovieCard key={movie.id} movie={movie} />
        ))}
      </div>
    </main>
  )
}

export default MoviesPage
