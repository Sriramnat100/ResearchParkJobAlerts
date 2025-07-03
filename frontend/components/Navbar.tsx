"use client"

import { Building2, Linkedin } from "lucide-react"
import { useState } from "react"

export function Navbar() {
  const [isMenuOpen, setIsMenuOpen] = useState(false)

  return (
    <nav className="fixed top-0 left-0 right-0 z-50 bg-white/80 backdrop-blur-lg border-b border-gray-200/20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo and Title */}
          <div className="flex items-center space-x-3">
            <div className="bg-gradient-to-br from-blue-600 to-blue-700 p-2 rounded-xl">
              <Building2 className="h-6 w-6 text-white" />
            </div>
            <div>
              <div className="font-bold text-gray-900">Research Park Jobs</div>
              <div className="text-xs text-gray-500">UIUC Innovation Hub</div>
            </div>
          </div>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center space-x-6">
            <a 
              href="https://researchpark.illinois.edu/work-here/careers/" 
              target="_blank" 
              rel="noopener noreferrer"
              className="text-gray-600 hover:text-blue-600 transition-colors font-medium"
            >
              View All Jobs
            </a>
            <a 
              href="https://www.linkedin.com/in/sriramnat/" 
              target="_blank" 
              rel="noopener noreferrer"
              className="text-gray-600 hover:text-blue-600 transition-colors"
            >
              <Linkedin className="h-5 w-5" />
            </a>
          </div>

          {/* Mobile menu button */}
          <div className="md:hidden">
            <button 
              onClick={() => setIsMenuOpen(!isMenuOpen)}
              className="p-2 rounded-md text-gray-600 hover:text-blue-600 hover:bg-gray-100 transition-colors"
            >
              {isMenuOpen ? (
                <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              ) : (
                <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                </svg>
              )}
            </button>
          </div>
        </div>

        {/* Mobile Navigation */}
        {isMenuOpen && (
          <div className="md:hidden border-t border-gray-200/20 bg-white/95 backdrop-blur-lg">
            <div className="px-2 pt-2 pb-3 space-y-1">
              <a 
                href="https://researchpark.illinois.edu/work-here/careers/" 
                target="_blank" 
                rel="noopener noreferrer"
                className="block px-3 py-2 text-gray-600 hover:text-blue-600 transition-colors"
              >
                View All Jobs
              </a>
              <a 
                href="https://www.linkedin.com/in/sriramnat/" 
                target="_blank" 
                rel="noopener noreferrer"
                className="flex items-center px-3 py-2 text-gray-600 hover:text-blue-600 transition-colors"
              >
                <Linkedin className="h-4 w-4 mr-2" />
                LinkedIn
              </a>
            </div>
          </div>
        )}
      </div>
    </nav>
  )
} 