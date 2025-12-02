# Movie Rating System - Frontend

A modern, responsive React frontend for a movie rating and discovery system. This application provides an intuitive interface for users to browse, rate, and manage their movie watchlist.

## 🎬 Features

### Authentication
- **Login/Register Page**: Secure user authentication with email and password
- **Protected Routes**: Automatic redirection based on authentication status
- **User Context**: Global state management for user data

### Movie Discovery
- **Home Page**: Browse movies with advanced filtering and search
- **Search Functionality**: Real-time movie search with URL parameters
- **Advanced Filters**: Filter by genre, language, and sort options
- **Responsive Grid**: Beautiful movie card layout with hover effects

### Movie Details
- **Detailed View**: Comprehensive movie information display
- **Interactive Actions**: Add to watchlist, like movies, and navigation
- **Star Ratings**: Visual IMDb rating display with star icons
- **Responsive Design**: Optimized for all screen sizes

### User Dashboard
- **Watchlist Management**: View and manage saved movies
- **Recommendations**: Personalized movie suggestions (future feature)
- **Statistics**: User activity and engagement metrics

### Profile Management
- **User Profile**: Account information and settings
- **Quick Actions**: Easy navigation to key features
- **Account Settings**: Notification and privacy preferences

## 📸 Screenshots

### Movie Filtering
![Movie Filtering](movie_filtering.png)
*Advanced filtering options with real-time search and category selection*

### User Profile
![Profile Information](prodile_info.png)
*User profile page with account details and quick actions*

### Watchlist
![Watchlist](watchlist.png)
*Personal watchlist management with saved movies*

## 🚀 Getting Started

### Prerequisites
- Node.js (v14 or higher)
- npm or yarn
- Flask backend running on `http://localhost:5000`

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd movie_rating_system/front_end
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Start the development server**
   ```bash
   npm start
   ```

4. **Open your browser**
   Navigate to `http://localhost:3000`

### Backend Integration

The frontend is configured to communicate with a Flask backend. Make sure your backend is running on `http://localhost:5000` with the following endpoints:

#### Authentication Endpoints
- `POST /auth/login` - User login
- `POST /auth/register` - User registration
- `GET /auth/me` - Get current user info

#### Movie Endpoints
- `GET /movies` - Get movies with filters
- `GET /movies/:id` - Get movie details
- `GET /movies?search=query` - Search movies

#### User Endpoints
- `GET /user/watchlist` - Get user's watchlist
- `POST /user/watchlist` - Add movie to watchlist
- `DELETE /user/watchlist/:id` - Remove movie from watchlist
- `GET /user/recommendations` - Get movie recommendations

## 🎨 Design System

### Color Palette
- **Primary**: `#667eea` (Blue gradient)
- **Secondary**: `#764ba2` (Purple gradient)
- **Background**: `#0f0f23` (Dark blue)
- **Surface**: `#1a1a2e` (Darker blue)
- **Text**: `#e0e0e0` (Light gray)
- **Muted**: `#6c757d` (Gray)

### Typography
- **Font Family**: Inter (Google Fonts)
- **Weights**: 300, 400, 500, 600, 700

### Components
- **Cards**: Rounded corners with subtle shadows
- **Buttons**: Gradient backgrounds with hover effects
- **Forms**: Clean inputs with focus states
- **Navigation**: Sticky header with search functionality

## 📱 Responsive Design

The application is fully responsive and optimized for:
- **Desktop**: Full sidebar and grid layout
- **Tablet**: Collapsible sidebar and adjusted grid
- **Mobile**: Single column layout with touch-friendly interactions

## 🛠️ Available Scripts

- `npm start` - Start development server
- `npm build` - Build for production
- `npm test` - Run tests
- `npm eject` - Eject from Create React App

## 📁 Project Structure

```
src/
├── components/          # Reusable UI components
│   ├── Navbar.js       # Navigation header
│   ├── SidebarFilters.js # Filter sidebar
│   ├── MovieCard.js    # Movie card component
│   ├── MovieGrid.js    # Movie grid layout
│   ├── LoginForm.js    # Login form
│   └── RegisterForm.js # Registration form
├── pages/              # Page components
│   ├── LoginPage.js    # Authentication page
│   ├── HomePage.js     # Movie browsing page
│   ├── MovieDetailPage.js # Movie details
│   ├── DashboardPage.js # User dashboard
│   └── ProfilePage.js  # User profile
├── contexts/           # React contexts
│   └── AuthContext.js  # Authentication state
├── App.js             # Main app component
├── App.css            # Global styles
├── index.js           # Entry point
└── index.css          # Base styles
```

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the root directory:

```env
REACT_APP_API_URL=http://localhost:5000
REACT_APP_APP_NAME=MovieRate
```

### API Configuration
The API base URL is configured in `src/contexts/AuthContext.js`. Update the `baseURL` if your backend runs on a different port.

## 🎯 Key Features Implementation

### Authentication Flow
1. User enters credentials on login/register page
2. API call to Flask backend for authentication
3. JWT token stored in localStorage
4. User redirected to home page
5. Protected routes check authentication status

### Movie Filtering
1. User selects filters in sidebar
2. Filters state updated in real-time
3. API call with filter parameters
4. Movie grid updates with filtered results
5. URL parameters sync with current filters

### Watchlist Management
1. User clicks "Add to Watchlist" on movie detail page
2. API call to add/remove movie from watchlist
3. Button state updates to reflect current status
4. Dashboard shows updated watchlist

## 🚀 Deployment

### Build for Production
```bash
npm run build
```

This creates a `build` folder with optimized production files.

### Deploy to Netlify/Vercel
1. Connect your repository
2. Set build command: `npm run build`
3. Set publish directory: `build`
4. Deploy!

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request


## 🆘 Support

For support or questions, please open an issue in the repository or contact the development team.

---
# Backend (Flask) for Movie Rating System

Quick start

1. Create virtualenv and install deps
   python -m venv .venv
   .venv\\Scripts\\activate
   pip install -r requirements.txt

2. Configure environment
   Copy .env.example to .env and update values as needed.

   Required variables:
   - SECRET_KEY
   - DATABASE_URL (e.g. postgresql+psycopg2://postgres:postgres@localhost:5432/movies_db)
   - JWT_SECRET_KEY
   - CORS_ORIGINS (dev: http://localhost:3000)

3. Initialize database
   flask --app app:create_app init-db

4. Run the server
   flask --app app:create_app run -p 5000

API routes

- Auth: /auth/register, /auth/login, /auth/me
- Movies: GET /movies, GET /movies/<id>
- Watchlist: GET /watchlist, POST /watchlist/add, POST /watchlist/remove


