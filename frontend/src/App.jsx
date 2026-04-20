import { useCallback, useEffect, useState } from 'react'
import './App.css'

const API_BASE = import.meta.env.VITE_API_URL ?? 'http://localhost:8000'

export default function App() {
  const [todos, setTodos] = useState([])
  const [title, setTitle] = useState('')
  const [error, setError] = useState(null)
  const [loading, setLoading] = useState(true)

  const load = useCallback(async () => {
    setError(null)
    const res = await fetch(`${API_BASE}/todos`)
    if (!res.ok) {
      setError('Could not load todos')
      return
    }
    setTodos(await res.json())
  }, [])

  useEffect(() => {
    let cancelled = false
    ;(async () => {
      setLoading(true)
      try {
        await load()
      } finally {
        if (!cancelled) setLoading(false)
      }
    })()
    return () => {
      cancelled = true
    }
  }, [load])

  async function addTodo(e) {
    e.preventDefault()
    const trimmed = title.trim()
    if (!trimmed) return
    setError(null)
    const res = await fetch(`${API_BASE}/todos`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title: trimmed }),
    })
    if (!res.ok) {
      setError('Could not add todo')
      return
    }
    setTitle('')
    await load()
  }

  async function toggleDone(todo) {
    setError(null)
    const res = await fetch(`${API_BASE}/todos/${todo.id}`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ done: !todo.done }),
    })
    if (!res.ok) {
      setError('Could not update todo')
      return
    }
    await load()
  }

  async function removeTodo(id) {
    setError(null)
    const res = await fetch(`${API_BASE}/todos/${id}`, { method: 'DELETE' })
    if (!res.ok) {
      setError('Could not delete todo')
      return
    }
    await load()
  }

  return (
    <main className="app">
      <h1>Todos</h1>
      <p className="hint">
        Start the API: <code>cd backend && uvicorn app.main:app --reload</code>
      </p>

      <form className="row" onSubmit={addTodo}>
        <input
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          placeholder="New todo"
          aria-label="New todo title"
        />
        <button type="submit">Add</button>
      </form>

      {error && <p className="error">{error}</p>}
      {loading ? (
        <p>Loading…</p>
      ) : (
        <ul className="list">
          {todos.map((t) => (
            <li key={t.id} className="item">
              <label>
                <input
                  type="checkbox"
                  checked={t.done}
                  onChange={() => toggleDone(t)}
                />
                <span className={t.done ? 'done' : ''}>{t.title}</span>
              </label>
              <button type="button" onClick={() => removeTodo(t.id)}>
                Delete
              </button>
            </li>
          ))}
        </ul>
      )}
    </main>
  )
}
