import React, { useState } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { useNavigate } from 'react-router-dom';
import './ProfilePage.css';

const ProfilePage = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [isLoggingOut, setIsLoggingOut] = useState(false);

  const handleLogout = async () => {
    setIsLoggingOut(true);
    
    // Add a small delay for better UX
    setTimeout(() => {
      logout();
      navigate('/login');
    }, 1000);
  };

  const handleEditProfile = () => {
    // This would open an edit profile modal or navigate to edit page
    // For now, we'll just show an alert
    alert('Edit profile functionality coming soon!');
  };

  const handleChangePassword = () => {
    // This would open a change password modal
    // For now, we'll just show an alert
    alert('Change password functionality coming soon!');
  };

  return (
    <div className="profile-page">
      <div className="profile-container">
        <div className="profile-header">
          <h1>Profile Settings</h1>
          <p>Manage your account information and preferences</p>
        </div>

        <div className="profile-content">
          <div className="profile-card">
            <div className="profile-avatar-section">
              <div className="profile-avatar">
                {user?.username?.charAt(0).toUpperCase() || 'U'}
              </div>
              <h2 className="profile-username">{user?.username || 'User'}</h2>
              <p className="profile-email">{user?.email || 'user@example.com'}</p>
            </div>

            <div className="profile-info">
              <div className="info-section">
                <h3>Account Information</h3>
                <div className="info-grid">
                  <div className="info-item">
                    <span className="info-label">Username:</span>
                    <span className="info-value">{user?.username || 'N/A'}</span>
                  </div>
                  <div className="info-item">
                    <span className="info-label">Email:</span>
                    <span className="info-value">{user?.email || 'N/A'}</span>
                  </div>
                  <div className="info-item">
                    <span className="info-label">Member Since:</span>
                    <span className="info-value">
                      {user?.created_at 
                        ? new Date(user.created_at).toLocaleDateString()
                        : 'N/A'
                      }
                    </span>
                  </div>
                  <div className="info-item">
                    <span className="info-label">Account Status:</span>
                    <span className="info-value status-active">Active</span>
                  </div>
                </div>
              </div>

              <div className="info-section">
                <h3>Statistics</h3>
                <div className="stats-grid">
                  <div className="stat-item">
                    <div className="stat-number">0</div>
                    <div className="stat-label">Movies Rated</div>
                  </div>
                  <div className="stat-item">
                    <div className="stat-number">0</div>
                    <div className="stat-label">Watchlist Items</div>
                  </div>
                  <div className="stat-item">
                    <div className="stat-number">0</div>
                    <div className="stat-label">Reviews Written</div>
                  </div>
                  <div className="stat-item">
                    <div className="stat-number">0</div>
                    <div className="stat-label">Likes Given</div>
                  </div>
                </div>
              </div>
            </div>

            <div className="profile-actions">
              <button 
                className="btn btn-primary"
                onClick={handleEditProfile}
              >
                ✏️ Edit Profile
              </button>
              
              <button 
                className="btn btn-secondary"
                onClick={handleChangePassword}
              >
                🔒 Change Password
              </button>
              
              <button 
                className="btn btn-danger"
                onClick={handleLogout}
                disabled={isLoggingOut}
              >
                {isLoggingOut ? (
                  <>
                    <span className="spinner-small"></span>
                    Logging Out...
                  </>
                ) : (
                  <>
                    🚪 Logout
                  </>
                )}
              </button>
            </div>
          </div>

          <div className="profile-sidebar">
            <div className="sidebar-card">
              <h3>Quick Actions</h3>
              <div className="quick-actions">
                <button 
                  className="quick-action-btn"
                  onClick={() => navigate('/dashboard')}
                >
                  📊 View Dashboard
                </button>
                <button 
                  className="quick-action-btn"
                  onClick={() => navigate('/')}
                >
                  🎬 Browse Movies
                </button>
                <button 
                  className="quick-action-btn"
                  onClick={() => navigate('/?sort_by=rating')}
                >
                  ⭐ Top Rated Movies
                </button>
              </div>
            </div>

            <div className="sidebar-card">
              <h3>Account Settings</h3>
              <div className="settings-list">
                <div className="setting-item">
                  <span>Email Notifications</span>
                  <label className="toggle">
                    <input type="checkbox" defaultChecked />
                    <span className="slider"></span>
                  </label>
                </div>
                <div className="setting-item">
                  <span>Public Profile</span>
                  <label className="toggle">
                    <input type="checkbox" />
                    <span className="slider"></span>
                  </label>
                </div>
                <div className="setting-item">
                  <span>Show Activity</span>
                  <label className="toggle">
                    <input type="checkbox" defaultChecked />
                    <span className="slider"></span>
                  </label>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProfilePage;
