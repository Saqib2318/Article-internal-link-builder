import { StrictMode } from 'react' 
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.tsx'
import { BrowserRouter } from 'react-router'
import { SelectProvider } from './provider/selectProvider.tsx'

createRoot(document.getElementById('root')!).render(
  <BrowserRouter>
    <SelectProvider>
    <App />
    </SelectProvider>  
  </BrowserRouter>,
)
