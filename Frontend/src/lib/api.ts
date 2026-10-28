export const API_URL = 'http://127.0.0.1:8000'

export type Movie = {
  id: number
  name: string
  genres: string[]
}

export function formatGenre(genre: string) {
  const label = genre.replace('_', ' ')
  return label[0].toUpperCase() + label.slice(1)
}
