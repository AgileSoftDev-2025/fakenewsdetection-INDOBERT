# Frontend Requirements & Dependencies

## 📦 Node.js Dependencies

All dependencies are managed via `package.json` and installed with `npm install`.

### Core Dependencies (Production)

| Package | Version | Purpose | Documentation |
|---------|---------|---------|---------------|
| **next** | 14.2.10 | React framework with SSR, routing, and optimization | [Next.js Docs](https://nextjs.org/docs) |
| **react** | 18.3.1 | Core React library for UI components | [React Docs](https://react.dev) |
| **react-dom** | 18.3.1 | React DOM rendering | [React DOM Docs](https://react.dev/reference/react-dom) |
| **swr** | 2.2.5 | Data fetching and caching (for /history, /admin) | [SWR Docs](https://swr.vercel.app) |

### Development Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| **typescript** | 5.4.5 | TypeScript language support |
| **@types/node** | 20.11.30 | Node.js type definitions |
| **@types/react** | 18.2.61 | React type definitions |
| **@types/react-dom** | 18.2.19 | React DOM type definitions |
| **tailwindcss** | ^4.1.15 | Utility-first CSS framework |
| **@tailwindcss/postcss** | ^4.1.15 | Tailwind PostCSS plugin |
| **postcss** | ^8.5.6 | CSS transformation tool |
| **autoprefixer** | ^10.4.21 | Adds vendor prefixes to CSS |
| **eslint** | 8.57.0 | JavaScript/TypeScript linter |
| **eslint-config-next** | 14.2.10 | Next.js ESLint configuration |

## 🛠️ System Requirements

### Minimum Requirements
- **Node.js:** v18.17.0 or higher
- **npm:** v9.0.0 or higher (comes with Node.js)
- **OS:** Windows 10/11, macOS, Linux
- **RAM:** 2GB minimum, 4GB recommended
- **Disk Space:** 500MB for node_modules

### Recommended for Development
- **Node.js:** v20.x LTS (Long Term Support)
- **npm:** v10.x
- **RAM:** 8GB or more
- **VS Code:** Latest version with extensions:
  - ESLint
  - Tailwind CSS IntelliSense
  - TypeScript and JavaScript Language Features

## 📋 Installation Steps

### 1. Check Node.js Version
```powershell
node --version  # Should be v18.17.0+
npm --version   # Should be v9.0.0+
```

### 2. Install Dependencies
```powershell
cd Frontend/nextjs-app
npm install
```

This will install:
- All `dependencies` (runtime packages)
- All `devDependencies` (development tools)
- Creates `node_modules/` folder (~350MB)
- Generates `package-lock.json` (lock file)

### 3. Verify Installation
```powershell
npm list --depth=0
```

## 🔄 Dependency Management

### Update All Dependencies
```powershell
npm update
```

### Update Specific Package
```powershell
npm install next@latest
```

### Check for Outdated Packages
```powershell
npm outdated
```

### Audit Security Vulnerabilities
```powershell
npm audit
npm audit fix  # Auto-fix issues
```

## 📦 Package Purposes Explained

### **Next.js** (`next`)
- Server-side rendering (SSR)
- Static site generation (SSG)
- File-based routing (`app/` directory)
- API routes (optional)
- Image optimization
- Built-in TypeScript support

### **React** (`react`, `react-dom`)
- Component-based UI
- Virtual DOM for performance
- Hooks (useState, useEffect, etc.)
- Client-side interactivity

### **SWR** (`swr`)
- Data fetching library by Vercel
- Automatic revalidation
- Cache management
- Used for `/history` and `/admin` pages
- Alternative to React Query

### **Tailwind CSS** (`tailwindcss`)
- Utility-first CSS framework
- Version 4 (latest)
- Custom design system
- Responsive by default
- Tree-shaking (removes unused CSS)

### **TypeScript** (`typescript`)
- Static type checking
- Better IDE support
- Catch errors early
- Improved code documentation
- All `.tsx` files use TypeScript

### **ESLint** (`eslint`)
- Code quality checker
- Enforces code style
- Catches common bugs
- Next.js includes recommended config

## 🌐 Browser Support

Supports modern browsers:
- Chrome/Edge: Last 2 versions
- Firefox: Last 2 versions
- Safari: Last 2 versions
- Mobile browsers: iOS Safari, Chrome Android

## 🔗 Additional Resources

- **Next.js Learn:** https://nextjs.org/learn
- **React Tutorial:** https://react.dev/learn
- **Tailwind CSS Docs:** https://tailwindcss.com/docs
- **TypeScript Handbook:** https://www.typescriptlang.org/docs
- **SWR Examples:** https://swr.vercel.app/examples

## 🐛 Troubleshooting

### Issue: `npm install` fails
```powershell
# Clear npm cache
npm cache clean --force
# Remove node_modules and lock file
Remove-Item -Recurse -Force node_modules, package-lock.json
# Reinstall
npm install
```

### Issue: Port 3000 already in use
```powershell
# Use different port
npm run dev -- -p 3001
```

### Issue: TypeScript errors
```powershell
# Check TypeScript version
npm list typescript
# Reinstall TypeScript
npm install --save-dev typescript@latest
```

### Issue: Tailwind styles not working
```powershell
# Rebuild Tailwind
npm run build
# Check tailwind.config.ts and globals.css
```

## 📊 Bundle Size Analysis

Run build analysis:
```powershell
npm run build
```

Expected output sizes:
- First Load JS: ~100-150KB (gzipped)
- Page bundles: 1-5KB each
- Total build time: 10-30 seconds

## 🔐 Security Notes

- Keep dependencies updated regularly
- Run `npm audit` before production
- Use `.env.local` for sensitive config (never commit)
- Review `package-lock.json` changes in PR
- Use npm registry with 2FA enabled
