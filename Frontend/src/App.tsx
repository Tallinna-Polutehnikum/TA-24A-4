import './App.css'
import { useEffect, useState } from 'react'
import MovieCard from './components/MovieCard'


type Movie = {
  id: number
  name: string
  genre: string
}

function App() {
  const [movies, setMovies] = useState<Movie[]>([])

  useEffect(() => {
    fetch('http://127.0.0.1:8000/movies')
      .then((response) => {
        console.log('Response:', response)

        if (!response.ok) {
          throw new Error('Backend returned an error')
        }

        return response.json()
      })
      .then((data) => {
        console.log('Movies:', data)
        setMovies(data)
      })
      .catch((error) => {
        console.error('Movies fetch failed:', error)
      })
  }, [])

  return (
    <main>
      <h1>Filmid</h1>

    {movies.map((movie) => (
      <MovieCard
        key={movie.id}
        name={movie.name}
        genre={movie.genre}
      />
    ))}
    </main>
  )
}

export default App