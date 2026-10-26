type MovieCardProps = {
  name: string
  genre: string
}

function MovieCard({ name, genre }: MovieCardProps) {
  return (
    <div>
      <h2>{name}</h2>
      <p>{genre}</p>
    </div>
  )
}

export default MovieCard