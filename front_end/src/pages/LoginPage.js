import React, { useState } from 'react';
import LoginForm from '../components/LoginForm';
import RegisterForm from '../components/RegisterForm';
import './LoginPage.css';

const LoginPage = () => {
  const [isLogin, setIsLogin] = useState(true);

  const switchToRegister = () => {
    setIsLogin(false);
  };

  const switchToLogin = () => {
    setIsLogin(true);
  };

  return (
    <div className="login-page">
      <div className="login-container">
        <div className="login-header">
          <div className="logo">
            <span className="logo-icon">🎬</span>
            <h1 className="logo-text">MovieRate</h1>
          </div>
          <p className="tagline">
            Discover, Rate, and Share Your Favorite Movies
          </p>
        </div>

        <div className="auth-section">
          {isLogin ? (
            <LoginForm onSwitchToRegister={switchToRegister} />
          ) : (
            <RegisterForm onSwitchToLogin={switchToLogin} />
          )}
        </div>

        <div className="login-footer">
          <p>© 2024 MovieRate. All rights reserved.</p>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;
