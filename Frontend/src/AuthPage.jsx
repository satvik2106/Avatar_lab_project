import React, { useState, useEffect } from 'react';
// Ensure these import paths match your file structure and naming
import LoginPageContent from './LoginPagecontent'; 
import SignUpPageContent from './SignUpPageContent'; 
import ParticleBackgroundSimple from './ParticleBackgroundSimple';

// Import your AuthPages.css. This ensures the styles are applied.
// If it's already imported globally (e.g., in App.js or index.js), this line might be redundant
// but it's good practice to have it where the components it styles are defined or used.
import './AuthPages.css'; 

export default function AuthPage() {
  // State to determine whether to show the Login or SignUp form
  // true = show Login, false = show SignUp
  const [isLoginView, setIsLoginView] = useState(true); // Default to showing the login form

  // Function to switch to the SignUp view
  const switchToSignup = () => {
    setIsLoginView(false);
  };

  // Function to switch to the Login view
  const switchToLogin = () => {
    setIsLoginView(true);
  };

  return (
    // This structure (.auth-page > .auth-container > .auth-card)
    // is based on your AuthPages.css for a single, centered card.
    <div className="auth-page"> 
      
      {/* Your ParticleBackgroundSimple component for the background */}
      <ParticleBackgroundSimple 
        particleCount={400} 
        particleSize={0.02}
        speedFactor={0.5}
      />
      
      <div className="auth-container">
        <div className="auth-card">
          {/* Conditionally render Login or SignUp content based on isLoginView state */}
          {isLoginView ? (
            <LoginPageContent onSwitchToSignup={switchToSignup} />
          ) : (
            <SignUpPageContent onSwitchToLogin={switchToLogin} />
          )}
        </div>
      </div>
    </div>
  );
}
