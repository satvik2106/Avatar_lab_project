import React from 'react';
// Ensure you are using react-router-dom v5 for this Switch syntax
// If using v6, the syntax would be different (Routes, element prop)
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';

// Page Components
import HomePage from './HomePage'; // Assuming you have this
import TemplateSelect from './TemplateSelect'; // Assuming you have this
import EnterTranscript from './EnterTranscript'; // Assuming you have this
import VideoOutput from './VideoOutput'; // Assuming you have this

// Import the new combined AuthPage that handles Login and Signup
import AuthPage from './AuthPage'; 

// Import your main CSS file that includes AuthPages.css or import AuthPages.css directly
import './AuthPages.css'; // Or your main App.css if it imports AuthPages.css

const App = () => {
  return (
    <Router>
      <Switch>
        {/* General application routes */}
        <Route exact path="/" component={HomePage} />
        <Route path="/templates" component={TemplateSelect} />
        <Route path="/enter-transcript" component={EnterTranscript} />
        <Route path="/video-output" component={VideoOutput} />

        {/* Auth routes now point to the combined AuthPage */}
        <Route path="/auth" component={AuthPage} /> 
        <Route path="/login" component={AuthPage} />
        <Route path="/signup" component={AuthPage} />

        {/* Define other routes like /forgot-password, /terms, /privacy if needed */}
        {/* Example:
        <Route path="/forgot-password" component={ForgotPasswordPage} />
        <Route path="/terms" component={TermsPage} />
        <Route path="/privacy" component={PrivacyPolicyPage} />
        */}

      </Switch>
    </Router>
  );
};

export default App;
