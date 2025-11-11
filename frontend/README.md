# CareBridge AI Frontend

React-based staff dashboard interface for the CareBridge AI healthcare platform. Provides real-time monitoring and management of patient communications across multiple channels (KakaoTalk, WeChat, LINE, SMS).

## Features

### Core Functionality
- **Real-time Dashboard** - Monitor patient messages and system performance
- **Message Management** - View and respond to patient conversations
- **Appointment Scheduling** - Manage patient appointments and bookings
- **System Monitoring** - Track system health and performance metrics

### Technical Features
- **Multi-language Support** - Korean, English, Chinese, Japanese
- **Real-time Updates** - Polling-based updates for live message monitoring
- **Responsive Design** - Optimized for desktop healthcare workstations
- **Professional Healthcare UI** - Clean, accessible interface design

## Technology Stack

- **Framework**: React 18 with TypeScript
- **Build Tool**: Vite
- **Styling**: Tailwind CSS with custom healthcare theme
- **Routing**: React Router v6
- **State Management**: React Query for server state
- **HTTP Client**: Axios
- **Icons**: Lucide React
- **Date Handling**: date-fns

## Project Structure

```
frontend/
├── src/
│   ├── components/          # Reusable UI components
│   │   └── Layout.tsx      # Main application layout
│   ├── pages/              # Page components
│   │   ├── Dashboard.tsx   # Staff dashboard
│   │   ├── Messages.tsx    # Message management
│   │   ├── PatientDetails.tsx # Individual patient view
│   │   ├── Appointments.tsx # Appointment management
│   │   └── Monitoring.tsx  # System monitoring
│   ├── services/           # API integration
│   │   ├── apiClient.ts   # HTTP client configuration
│   │   └── apiServices.ts # Service functions
│   ├── hooks/              # Custom React hooks
│   │   └── useApi.ts      # API and data hooks
│   ├── utils/              # Utility functions
│   │   └── helpers.ts     # Helper functions
│   ├── types/              # TypeScript definitions
│   │   └── index.ts       # Type definitions
│   ├── App.tsx            # Main application component
│   ├── main.tsx           # Application entry point
│   └── index.css          # Global styles
├── public/                 # Static assets
├── package.json           # Dependencies and scripts
├── vite.config.ts         # Vite configuration
├── tailwind.config.js     # Tailwind CSS configuration
└── tsconfig.json          # TypeScript configuration
```

## Getting Started

### Prerequisites
- Node.js 16+ and npm/yarn
- CareBridge AI backend running on port 8000

### Installation

1. **Install Dependencies**
   ```bash
   cd frontend
   npm install
   ```

2. **Environment Setup**
   ```bash
   cp .env.example .env
   # Edit .env to configure API URL if needed
   ```

3. **Start Development Server**
   ```bash
   npm run dev
   ```

   The application will be available at `http://localhost:3000`

### Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint
- `npm run type-check` - TypeScript type checking

## API Integration

### Base Configuration
The frontend is configured to communicate with the Django backend at `http://localhost:8000/api`.

### Endpoints Used
- `GET /patients/` - List all patients
- `GET /messages/` - Get messages (supports patient_id filtering)
- `GET /appointments/` - Get appointments
- `GET /system-metrics/` - Get system metrics
- `GET /system-metrics/summary/` - Get metrics summary
- `POST /process-message/` - Process test messages
- `GET /health/` - Health check endpoint

### Error Handling
- Automatic retry with exponential backoff
- Connection status monitoring
- User-friendly error messages

## Key Components

### Dashboard
- Real-time message monitoring
- System performance metrics
- Quick action buttons
- Channel status indicators

### Messages
- Conversation list with search and filters
- Real-time message updates
- AI confidence indicators
- Human intervention flags

### Patient Details
- Individual patient information sidebar
- Full conversation history
- Staff response interface
- Message flagging for human review

### Appointments
- Appointment scheduling form
- Status management
- Patient search integration
- Calendar-style display

### Monitoring
- System health dashboard
- Performance metrics
- Channel analytics
- Recent activity logs

## Styling and Theming

### Healthcare Theme
- Primary color: Healthcare teal (#0F766E)
- Secondary colors: Healthcare greens
- Clean, professional design
- Accessible color contrasts

### Responsive Design
- Mobile-first approach
- Tablet and desktop optimized
- Healthcare workstation friendly
- Touch-friendly interface elements

## Multi-language Support

### Supported Languages
- Korean (Primary) 🇰🇷
- English (Secondary) 🇺🇸
- Chinese 🇨🇳
- Japanese 🇯🇵

### Implementation
- Language preference stored per patient
- Unicode emoji flags for visual identification
- Text truncation for long messages
- RTL language ready

## Real-time Features

### Polling Strategy
- Messages: 5-second intervals
- Appointments: 10-second intervals  
- System metrics: 30-second intervals
- Health checks: 60-second intervals

### Connection Monitoring
- Online/offline status detection
- Automatic reconnection
- Visual connection indicators
- Graceful degradation

## Security Considerations

### Current Implementation
- No authentication (demo mode)
- CORS enabled for development
- API proxy configuration
- No sensitive data stored

### Production Considerations
- Implement JWT authentication
- Add CSRF protection
- Secure API communication (HTTPS)
- Role-based access control

## Development Guidelines

### Code Standards
- TypeScript for type safety
- ESLint for code quality
- Consistent naming conventions
- Component composition patterns

### Performance Optimization
- React Query for caching
- Lazy loading for routes
- Memoization for expensive computations
- Efficient re-rendering strategies

## Troubleshooting

### Common Issues
1. **Backend Connection Failed**
   - Ensure Django backend is running on port 8000
   - Check API proxy configuration
   - Verify CORS settings

2. **Build Errors**
   - Clear node_modules and reinstall dependencies
   - Check TypeScript configuration
   - Verify all imports are correct

3. **Real-time Updates Not Working**
   - Check network connectivity
   - Verify polling intervals
   - Review API endpoint availability

## Future Enhancements

### Planned Features
- WebSocket integration for true real-time updates
- Push notifications for urgent messages
- Advanced analytics dashboard
- Mobile responsive improvements
- Offline mode support
- Dark theme option

### Technical Improvements
- Unit and integration tests
- E2E testing with Cypress
- Progressive Web App (PWA) features
- Performance monitoring
- Error boundary implementation

## Support

For technical issues or questions:
- Check the troubleshooting section
- Review the Django backend README
- Contact the development team

---

**Built with ❤️ for healthcare professionals**