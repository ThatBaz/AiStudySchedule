import React from 'react'
import { Toaster } from 'react-hot-toast'
import AuthInterface from './AuthInterface'
import './globals.css'

function App() {
  return (
    <>
      <AuthInterface />
      <Toaster />
    </>
  )
}

export default App