import { useState } from 'react'
import axios from 'axios'
import { motion, AnimatePresence } from 'framer-motion'
import { 
  Sparkles, 
  Search, 
  Zap, 
  Brain, 
  BookOpen, 
  Loader2,
  X,
  RefreshCw,
  Copy,
  CheckCircle2,
  Clock,
  MessageSquare,
  ArrowRight
} from 'lucide-react'
import { AnimatedBackground } from './components/AnimatedBackground'
import './App.css'

const API_URL = import.meta.env.VITE_API_URL || 
                (import.meta.env.DEV 
                  ? 'http://localhost:5000' 
                  : 'https://fusionai-backend-suul.onrender.com')

const fadeUp = {
  hidden: { opacity: 0, y: 20 },
  visible: (i) => ({
    opacity: 1,
    y: 0,
    transition: { delay: i * 0.1, duration: 0.5, ease: 'easeOut' },
  }),
}

const scaleIn = {
  hidden: { opacity: 0, scale: 0.8 },
  visible: { 
    opacity: 1, 
    scale: 1,
    transition: { type: 'spring', stiffness: 200, damping: 20 }
  },
}

function App() {
  const [query, setQuery] = useState('')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)
  const [copied, setCopied] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    
    if (!query.trim()) {
      setError('Please enter a research topic')
      return
    }

    if (query.trim().length < 3) {
      setError('Topic too short. Please be more specific.')
      return
    }

    setLoading(true)
    setError(null)
    setResult(null)

    try {
      const response = await axios.post(`${API_URL}/api/research`, {
        query: query.trim()
      })
      setResult(response.data)
    } catch (err) {
      setError(err.response?.data?.error || 'An error occurred. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  const handleReset = () => {
    setQuery('')
    setResult(null)
    setError(null)
  }

  const handleCopy = () => {
    if (result?.summary) {
      navigator.clipboard.writeText(result.summary)
      setCopied(true)
      setTimeout(() => setCopied(false), 2000)
    }
  }

  return (
    <div className="app">
      {/* Animated Background */}
      <AnimatedBackground />

      {/* Navbar */}
      <nav className="navbar">
        <div className="nav-container">
          <motion.div 
            className="logo"
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5 }}
            whileHover={{ scale: 1.05 }}
          >
            <motion.div 
              className="logo-icon"
              whileHover={{ rotate: 15 }}
              transition={{ type: 'spring', stiffness: 300 }}
            >
              <Zap className="icon" />
            </motion.div>
            <span className="logo-text">FusionAI</span>
          </motion.div>

          <motion.div 
            className="nav-badge"
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5, delay: 0.2 }}
            whileHover={{ scale: 1.05 }}
          >
            <motion.div 
              className="status-dot"
              animate={{ scale: [1, 1.2, 1] }}
              transition={{ duration: 2, repeat: Infinity }}
            />
            <span>AI Powered</span>
          </motion.div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="main">
        <div className="container">
          
          {/* Hero Section */}
          <AnimatePresence mode="wait">
            {!result && !loading && (
              <motion.div 
                className="hero"
                initial="hidden"
                animate="visible"
                exit="hidden"
              >
                <motion.div
                  className="hero-icon"
                  variants={scaleIn}
                >
                  <motion.div 
                    className="icon-glow"
                    animate={{ 
                      scale: [1, 1.2, 1],
                      opacity: [0.5, 0.8, 0.5]
                    }}
                    transition={{ duration: 3, repeat: Infinity }}
                  />
                  <motion.div 
                    className="icon-wrapper"
                    whileHover={{ rotate: 360 }}
                    transition={{ duration: 0.6 }}
                  >
                    <motion.div
                      animate={{ 
                        scale: [1, 1.1, 1],
                        rotate: [0, 5, -5, 0]
                      }}
                      transition={{ duration: 4, repeat: Infinity, ease: 'easeInOut' }}
                    >
                      <Sparkles className="sparkle-icon" />
                    </motion.div>
                  </motion.div>
                </motion.div>

                <div className="hero-content">
                  <motion.h1 
                    className="hero-title"
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.2 }}
                  >
                    Research Assistant{' '}
                    <motion.span 
                      className="gradient-text"
                      animate={{ 
                        backgroundPosition: ['0% 50%', '100% 50%', '0% 50%']
                      }}
                      transition={{ duration: 5, repeat: Infinity }}
                    >
                      Reimagined
                    </motion.span>
                  </motion.h1>

                  <motion.p 
                    className="hero-description"
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.35 }}
                  >
                    Fuse knowledge from Wikipedia and Claude AI into beautiful,
                    comprehensive insights. Experience research like never before.
                  </motion.p>

                  <motion.div 
                    className="feature-grid"
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.5 }}
                  >
                    {[
                      { icon: Zap, label: 'Lightning Fast' },
                      { icon: Brain, label: 'AI-Powered' },
                      { icon: BookOpen, label: 'Multi-Source' },
                    ].map(({ icon: Icon, label }, i) => (
                      <motion.div
                        key={label}
                        className="feature-tag"
                        custom={i}
                        initial="hidden"
                        animate="visible"
                        variants={fadeUp}
                        whileHover={{ 
                          y: -4, 
                          scale: 1.05,
                          boxShadow: '0 10px 30px rgba(139, 92, 246, 0.3)'
                        }}
                        transition={{ type: 'spring', stiffness: 300 }}
                      >
                        <motion.div
                          whileHover={{ rotate: 360 }}
                          transition={{ duration: 0.6 }}
                        >
                          <Icon className="feature-icon" />
                        </motion.div>
                        <span>{label}</span>
                      </motion.div>
                    ))}
                  </motion.div>
                </div>
              </motion.div>
            )}
          </AnimatePresence>

          {/* Search Section */}
          <motion.div 
            className="search-section"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
          >
            <motion.div 
              className="search-card"
              whileHover={{ 
                boxShadow: '0 20px 60px rgba(139, 92, 246, 0.2)',
                y: -2
              }}
              transition={{ duration: 0.3 }}
            >
              <form onSubmit={handleSubmit} className="search-form">
                <div className="input-container">
                  <Search className="search-icon" />
                  <input
                    type="text"
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    placeholder="Ask me anything..."
                    className="search-input"
                    disabled={loading}
                  />
                  <AnimatePresence>
                    {query && !loading && (
                      <motion.button
                        type="button"
                        className="clear-btn"
                        onClick={() => setQuery('')}
                        initial={{ opacity: 0, scale: 0.8 }}
                        animate={{ opacity: 1, scale: 1 }}
                        exit={{ opacity: 0, scale: 0.8 }}
                        whileHover={{ scale: 1.1, rotate: 90 }}
                        whileTap={{ scale: 0.9 }}
                      >
                        <X className="icon" />
                      </motion.button>
                    )}
                  </AnimatePresence>
                </div>

                <motion.button
                  type="submit"
                  className="search-button"
                  disabled={loading || !query.trim()}
                  whileHover={{ scale: 1.02, y: -2 }}
                  whileTap={{ scale: 0.98 }}
                  transition={{ type: 'spring', stiffness: 400 }}
                >
                  {loading ? (
                    <>
                      <Loader2 className="icon spin" />
                      <span>Researching...</span>
                    </>
                  ) : (
                    <>
                      <Sparkles className="icon" />
                      <span>Search</span>
                      <motion.div
                        animate={{ x: [0, 5, 0] }}
                        transition={{ duration: 1.5, repeat: Infinity }}
                      >
                        <ArrowRight className="arrow-icon" />
                      </motion.div>
                    </>
                  )}
                </motion.button>
              </form>

              <AnimatePresence>
                {error && (
                  <motion.div
                    className="alert error"
                    initial={{ opacity: 0, height: 0, marginTop: 0 }}
                    animate={{ opacity: 1, height: 'auto', marginTop: 16 }}
                    exit={{ opacity: 0, height: 0, marginTop: 0 }}
                    transition={{ duration: 0.3 }}
                  >
                    <X className="alert-icon" />
                    <span>{error}</span>
                  </motion.div>
                )}
              </AnimatePresence>
            </motion.div>

            {/* Loading State */}
            <AnimatePresence>
              {loading && (
                <motion.div
                  className="loading-card"
                  initial={{ opacity: 0, y: 20, scale: 0.95 }}
                  animate={{ opacity: 1, y: 0, scale: 1 }}
                  exit={{ opacity: 0, y: -20, scale: 0.95 }}
                  transition={{ duration: 0.4 }}
                >
                  <div className="loading-content">
                    <div className="loader">
                      <motion.div 
                        className="pulse-ring"
                        animate={{ scale: [1, 1.5], opacity: [0.8, 0] }}
                        transition={{ duration: 1.5, repeat: Infinity, ease: 'easeOut' }}
                      />
                      <motion.div 
                        className="pulse-ring delay-1"
                        animate={{ scale: [1, 1.5], opacity: [0.8, 0] }}
                        transition={{ duration: 1.5, repeat: Infinity, ease: 'easeOut', delay: 0.5 }}
                      />
                      <motion.div 
                        className="pulse-ring delay-2"
                        animate={{ scale: [1, 1.5], opacity: [0.8, 0] }}
                        transition={{ duration: 1.5, repeat: Infinity, ease: 'easeOut', delay: 1 }}
                      />
                      <motion.div
                        animate={{ rotate: 360 }}
                        transition={{ duration: 3, repeat: Infinity, ease: 'linear' }}
                      >
                        <Sparkles className="loader-icon" />
                      </motion.div>
                    </div>
                    <motion.p 
                      className="loading-text"
                      animate={{ opacity: [0.5, 1, 0.5] }}
                      transition={{ duration: 2, repeat: Infinity }}
                    >
                      Gathering insights from multiple sources...
                    </motion.p>
                    <div className="progress-steps">
                      {['Analyzing query', 'Searching sources', 'Synthesizing results'].map((step, i) => (
                        <motion.div 
                          key={step} 
                          className={`step ${i < 2 ? 'active' : ''}`}
                          initial={{ opacity: 0, x: -20 }}
                          animate={{ opacity: 1, x: 0 }}
                          transition={{ delay: i * 0.2 }}
                        >
                          <motion.div
                            animate={i < 2 ? { rotate: 360 } : {}}
                            transition={{ duration: 2, repeat: Infinity, ease: 'linear' }}
                          >
                            <CheckCircle2 className="step-icon" />
                          </motion.div>
                          <span>{step}</span>
                        </motion.div>
                      ))}
                    </div>
                  </div>
                </motion.div>
              )}
            </AnimatePresence>
          </motion.div>

{/* Results Section */}
<AnimatePresence>
  {result && (
    <motion.div
      className="results"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -20 }}
      transition={{ duration: 0.4 }}
    >
      {/* Results Header */}
      <motion.div 
        className="results-header"
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1 }}
      >
        <div className="results-info">
          <motion.h2 
            className="results-title"
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.2 }}
          >
            {result.topic}
          </motion.h2>
          <div className="results-meta">
            <motion.span 
              className="meta-item"
              initial={{ opacity: 0, scale: 0.8 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: 0.3 }}
            >
              <Clock className="meta-icon" />
              Just now
            </motion.span>
            <motion.span 
              className="meta-item"
              initial={{ opacity: 0, scale: 0.8 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: 0.4 }}
            >
              <BookOpen className="meta-icon" />
              {result.sources.length} sources
            </motion.span>
            <motion.span 
              className="meta-item quality-badge"
              initial={{ opacity: 0, scale: 0.8 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: 0.5 }}
            >
              <CheckCircle2 className="meta-icon" />
              Verified
            </motion.span>
          </div>
        </div>
        <motion.button
          className="reset-button"
          onClick={handleReset}
          initial={{ opacity: 0, scale: 0.8 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.5 }}
          whileHover={{ scale: 1.05, rotate: 180 }}
          whileTap={{ scale: 0.95 }}
        >
          <RefreshCw className="icon" />
          <span>New Search</span>
        </motion.button>
      </motion.div>

      {/* Summary Card - Enhanced */}
      <motion.div
        className="result-card summary-card"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2 }}
        whileHover={{ y: -4, boxShadow: '0 20px 60px rgba(139, 92, 246, 0.2)' }}
      >
        <div className="card-header">
          <div className="header-left">
            <div className="icon-badge">
              <Sparkles className="badge-icon" />
            </div>
            <h3>Research Summary</h3>
          </div>
          <motion.button
            className="icon-button"
            onClick={handleCopy}
            whileHover={{ scale: 1.1, rotate: 5 }}
            whileTap={{ scale: 0.9 }}
            title="Copy to clipboard"
          >
            <AnimatePresence mode="wait">
              {copied ? (
                <motion.div
                  key="check"
                  initial={{ scale: 0, rotate: -180 }}
                  animate={{ scale: 1, rotate: 0 }}
                  exit={{ scale: 0, rotate: 180 }}
                >
                  <CheckCircle2 className="icon check" />
                </motion.div>
              ) : (
                <motion.div
                  key="copy"
                  initial={{ scale: 0 }}
                  animate={{ scale: 1 }}
                  exit={{ scale: 0 }}
                >
                  <Copy className="icon" />
                </motion.div>
              )}
            </AnimatePresence>
          </motion.button>
        </div>
        <div className="card-content">
          <div className="summary-content">
            {result.summary.split('\n\n').map((paragraph, index) => (
              <motion.p 
                key={index}
                className="summary-paragraph"
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.3 + index * 0.1 }}
              >
                {paragraph}
              </motion.p>
            ))}
          </div>
        </div>
      </motion.div>

      {/* Sources Card - Enhanced */}
      <motion.div
        className="result-card sources-card"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.3 }}
        whileHover={{ y: -4, boxShadow: '0 20px 60px rgba(139, 92, 246, 0.2)' }}
      >
        <div className="card-header">
          <div className="header-left">
            <div className="icon-badge sources">
              <BookOpen className="badge-icon" />
            </div>
            <h3>Sources & References</h3>
          </div>
          <motion.div 
            className="source-badge"
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            transition={{ type: 'spring', delay: 0.4 }}
          >
            {result.sources.length}
          </motion.div>
        </div>
        <div className="card-content">
          <div className="sources-list">
            {result.sources.map((source, index) => (
              <motion.div
                key={index}
                className="source-item"
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.4 + index * 0.05 }}
                whileHover={{ 
                  x: 8, 
                  backgroundColor: 'rgba(139, 92, 246, 0.05)',
                  borderColor: 'rgba(139, 92, 246, 0.3)'
                }}
              >
                <motion.div 
                  className="source-number"
                  whileHover={{ scale: 1.2, rotate: 360 }}
                  transition={{ duration: 0.4 }}
                >
                  {index + 1}
                </motion.div>
                <div className="source-content">
                  <p>{source}</p>
                </div>
                <motion.div
                  className="source-check"
                  initial={{ opacity: 0, scale: 0 }}
                  animate={{ opacity: 1, scale: 1 }}
                  transition={{ delay: 0.5 + index * 0.05 }}
                >
                  <CheckCircle2 className="check-icon" />
                </motion.div>
              </motion.div>
            ))}
          </div>
        </div>
      </motion.div>

      {/* Tools Section - Enhanced */}
      <motion.div
        className="tools-card"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.5 }}
      >
        <div className="tools-header">
          <Brain className="tools-icon" />
          <span className="tools-label">Research powered by</span>
        </div>
        <div className="tools-list">
          {result.tools_used.map((tool, index) => (
            <motion.div
              key={index}
              className="tool-chip"
              initial={{ opacity: 0, scale: 0.8 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: 0.6 + index * 0.05 }}
              whileHover={{ scale: 1.1, y: -2 }}
            >
              <span className="tool-emoji">
                {tool === 'wikipedia' && '📚'}
                {tool === 'search' && '🌐'}
                {tool === 'claude' && '🤖'}
                {tool === 'claude-ai' && '🤖'}
                {tool === 'general_knowledge' && '🧠'}
              </span>
              <span className="tool-name">{tool}</span>
            </motion.div>
          ))}
        </div>
      </motion.div>
    </motion.div>
  )}
</AnimatePresence>
        </div>
      </main>

    </div>
  )
}

export default App