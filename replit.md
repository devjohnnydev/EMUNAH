# Emunah - Sales and Budget System

## Overview

Emunah is a comprehensive web application for managing t-shirt sales, production, and supplier relationships. The system provides tools for creating quotes, managing budgets, tracking orders, and monitoring business metrics through an intuitive dashboard.

The application serves multiple user roles (Admin, Seller, Supplier) and facilitates the complete sales cycle - from initial supplier quotations to final order delivery and payment tracking. It includes inventory management for t-shirt products and print designs, along with analytics for revenue tracking and conversion metrics.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture

**Technology Stack:**
- React with TypeScript for component-based UI
- Vite as the build tool and dev server
- Wouter for client-side routing
- TanStack Query for server state management
- Tailwind CSS with shadcn/ui component library
- Lucide icons for UI elements

**Design Decisions:**
- Single Page Application (SPA) architecture for smooth user experience
- Protected routes with authentication checks before rendering
- Custom color palette (Burgundy #520B1B, Secondary #C5A995) matching the Emunah brand
- Responsive design supporting mobile and desktop viewports
- Font stack: DM Sans (sans-serif) and Playfair Display (serif) for brand consistency

**Component Structure:**
- Reusable UI components from shadcn/ui (buttons, forms, dialogs, tables)
- Page-level components for each major feature area
- Custom hooks for mobile detection and toast notifications
- Auth context provider for global authentication state

### Backend Architecture

**Dual Stack Approach:**
The application currently shows evidence of two backend implementations:

1. **Flask + SQLAlchemy (Python)** - Legacy/Alternative Implementation:
   - Flask web framework with Jinja2 templates
   - SQLAlchemy ORM for database operations
   - Flask-Login for authentication
   - Flask-Migrate for database migrations
   - Supports both SQLite (local) and PostgreSQL (production)
   - Railway deployment configuration included

2. **Express + Drizzle (Node.js)** - Modern/Primary Implementation:
   - Express.js web server
   - Drizzle ORM with Neon serverless PostgreSQL
   - Type-safe database schema definitions
   - Storage layer abstraction for CRUD operations
   - Server-side rendering setup with Vite integration

**Rationale:** The repository contains both Python (Flask) and TypeScript (Express) backend code. The Express/Drizzle stack appears to be the intended primary implementation based on the modern tooling and integration with the React frontend, while Flask code may be legacy or an alternative deployment option.

### Data Storage

**Database:** PostgreSQL (via Neon serverless)
- Schema defined in TypeScript using Drizzle ORM (`shared/schema.ts`)
- Connection pooling through Neon's serverless driver
- Database migrations managed via Drizzle Kit

**Core Data Models:**
- **Users:** Authentication and role-based access (Admin, Seller, Supplier)
- **Clients:** Customer information and contact details
- **Suppliers:** Vendor management with ratings and delivery times
- **Products:** T-shirt inventory with models, fabrics, sizes, and pricing
- **Prints:** Design assets with colors, positions, and techniques
- **Quotes:** Supplier quotations with status tracking
- **Budgets:** Customer proposals with pricing and payment terms
- **Orders:** Production orders linked to budgets and suppliers
- **Transactions:** Payment tracking for orders

**Design Patterns:**
- Relational schema with foreign key relationships
- JSONB fields for flexible array storage (colors, sizes, positions)
- Timestamp columns for audit trails
- Status enums for workflow management
- Decimal types for precise financial calculations

### Authentication & Authorization

**Current Implementation:**
- Client-side auth context with localStorage persistence
- Mock authentication for development (admin@emunah.com / 123456)
- Protected routes using custom ProtectedRoute wrapper
- Role-based access control ready (ADMIN, SELLER, SUPPLIER)

**Production Requirements:**
- JWT or session-based authentication needed
- Password hashing (Flask implementation shows werkzeug.security)
- Secure secret key management via environment variables
- HTTPS enforcement for production deployments

### API Structure

**RESTful Endpoints (Planned):**
- `/api/*` prefix for all backend routes
- Storage layer abstraction for database operations
- CRUD operations for all major entities
- JSON request/response format

**Current State:**
- Route registration framework in place (`server/routes.ts`)
- Storage interface defined but not fully implemented
- Frontend expects API endpoints but they need to be built

## External Dependencies

### Third-Party Services

**Database:**
- Neon (serverless PostgreSQL) - Primary database host
- Connection string via `DATABASE_URL` environment variable
- Automatic connection pooling and scaling

**Development Tools:**
- Replit-specific plugins for dev experience:
  - `@replit/vite-plugin-cartographer` - Code navigation
  - `@replit/vite-plugin-dev-banner` - Development banner
  - `@replit/vite-plugin-runtime-error-modal` - Error overlay

**Deployment:**
- Railway platform support (legacy Flask deployment)
- Nixpacks build system
- Gunicorn WSGI server for Python
- Health check endpoint configuration

### NPM Packages

**UI & Styling:**
- Radix UI primitives (dialogs, dropdowns, tooltips, etc.)
- Tailwind CSS with custom theme configuration
- class-variance-authority for component variants
- cmdk for command palette functionality
- embla-carousel-react for carousel components

**Data & Forms:**
- react-hook-form with @hookform/resolvers
- zod for schema validation
- drizzle-zod for database schema validation
- date-fns for date manipulation

**API & State:**
- @tanstack/react-query for server state
- express for HTTP server
- connect-pg-simple for session storage
- express-session for session management

### Environment Variables

**Required:**
- `DATABASE_URL` - PostgreSQL connection string (auto-provisioned by Replit/Railway)
- `SECRET_KEY` - Application secret for sessions/JWT (must be set securely)
- `NODE_ENV` - Development or production mode

**Optional:**
- `FLASK_DEBUG` - Flask debug mode (Python implementation)
- `PORT` - Server port (defaults handled by hosting platform)

### Build & Development

**Scripts:**
- `npm run dev` - Start development server with hot reload
- `npm run build` - Production build (client + server bundling)
- `npm run start` - Run production server
- `npm run db:push` - Push database schema changes

**Build Process:**
- Vite bundles the React frontend
- esbuild bundles the Express server with selective dependencies
- Static files served from `dist/public`
- Server bundle optimized for cold start performance