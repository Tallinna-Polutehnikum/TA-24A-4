import { NavLink, Route, Routes } from 'react-router'
import { buttonVariants } from '@/components/ui/button'
import MoviePage from '@/pages/MoviePage'
import MoviesPage from '@/pages/MoviesPage'

function App() {
  return (
    <>
      <header className="sticky top-0 z-10 flex h-16 items-center border-b bg-background px-6">
        <NavLink to="/" className={({ isActive }) => buttonVariants({ variant: isActive ? 'secondary' : 'ghost' })}>
          Films
        </NavLink>
      </header>
      <Routes>
        <Route path="/" element={<MoviesPage />} />
        <Route path="/movies/:movieId" element={<MoviePage />} />
      </Routes>
    </>
  )
}

export default App
