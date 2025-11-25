# React + TypeScript + Vite

This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react) uses [Babel](https://babeljs.io/) (or [oxc](https://oxc.rs) when used in [rolldown-vite](https://vite.dev/guide/rolldown)) for Fast Refresh
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react-swc) uses [SWC](https://swc.rs/) for Fast Refresh

## React Compiler

The React Compiler is currently not compatible with SWC. See [this issue](https://github.com/vitejs/vite-plugin-react/issues/428) for tracking the progress.

## Expanding the ESLint configuration

If you are developing a production application, we recommend updating the configuration to enable type-aware lint rules:

```js
export default defineConfig([
  globalIgnores(['dist']),
  {
    files: ['**/*.{ts,tsx}'],
    extends: [
      // Other configs...

      // Remove tseslint.configs.recommended and replace with this
      tseslint.configs.recommendedTypeChecked,
      // Alternatively, use this for stricter rules
      tseslint.configs.strictTypeChecked,
      // Optionally, add this for stylistic rules
      tseslint.configs.stylisticTypeChecked,

      // Other configs...
    ],
    languageOptions: {
      parserOptions: {
        project: ['./tsconfig.node.json', './tsconfig.app.json'],
        tsconfigRootDir: import.meta.dirname,
      },
      // other options...
    },
  },
])
```

You can also install [eslint-plugin-react-x](https://github.com/Rel1cx/eslint-react/tree/main/packages/plugins/eslint-plugin-react-x) and [eslint-plugin-react-dom](https://github.com/Rel1cx/eslint-react/tree/main/packages/plugins/eslint-plugin-react-dom) for React-specific lint rules:

```js
// eslint.config.js
import reactX from 'eslint-plugin-react-x'
import reactDom from 'eslint-plugin-react-dom'

export default defineConfig([
  globalIgnores(['dist']),
  {
    files: ['**/*.{ts,tsx}'],
    extends: [
      // Other configs...
      // Enable lint rules for React
      reactX.configs['recommended-typescript'],
      // Enable lint rules for React DOM
      reactDom.configs.recommended,
    ],
    languageOptions: {
      parserOptions: {
        project: ['./tsconfig.node.json', './tsconfig.app.json'],
        tsconfigRootDir: import.meta.dirname,
      },
      // other options...
    },
  },
])
```
# Frontend - Fake News Detection UI

Framework used: **Next.js 15** (App Router) with **TypeScript** and **Tailwind CSS v4**

Modern web interface for Indonesian fake news detection with support for text input, image OCR, and DOCX document upload.

## 📁 Project Structure

```
Frontend/nextjs-app/
├── app/
│   ├── page.tsx              # Home: News checker (text/file)
│   ├── hasil-analisis/
│   │   └── page.tsx          # Results page
│   ├── layout.tsx            # Root layout
│   └── globals.css           # Tailwind styles
├── package.json              # Node dependencies
├── tsconfig.json             # TypeScript config
├── tailwind.config.ts        # Tailwind v4 config
└── next.config.mjs           # Next.js config
```

## 🚀 Setup Instructions (Windows)

### 1. Install dependencies

```powershell
cd Frontend/nextjs-app
npm install
```

### 2. Configure environment variables (optional)

Create `.env.local` file for custom backend URL:

```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

**Default:** `http://localhost:8000` (if not set)

### 3. Run development server

```powershell
npm run dev
```

Frontend will start on: **http://localhost:3000**

### 4. Build for production

```powershell
npm run build
npm start
```

## 🎨 Features

### 🏠 Home Page (`/`)
- **Dual Input Methods:**
  - **Text Tab:** Input news title and body text
  - **File Tab:** Upload images (PNG/JPG) or documents (DOCX)
- **File Upload with Preview:**
  - Drag & drop or click to select
  - Thumbnail preview for images
  - Document icon for DOCX files
  - File info display (name, size, type)
  - Change/remove file buttons
- **Real-time Validation:**
  - Text: minimum 10 characters
  - File: accepted formats only
- **Analysis Button:** Submits to backend API

### 📊 Results Page (`/hasil-analisis`)
- Color-coded result banner (green = valid, red = hoax)
- Displays:
  - Prediction result
  - Confidence score
  - Extracted text snippet (for file uploads)
  - Source reference (title or filename)
- **Action buttons:**
  - Save result
  - Share result
  - Check again (returns to home)

### 📱 Additional Pages (Planned)
- `/history` - Feedback history table
- `/admin` - Model version and management

## 🧪 BDD Testing Support

Frontend includes `data-testid` attributes for automated testing with Behave + Selenium:

| Element | Test ID | Purpose |
|---------|---------|---------|
| Text input | `news_text` | News body textarea |
| File input | `news_file` | File upload input |
| Submit button | `check` | Analyze button |

Run BDD tests from project root:
```powershell
cd tests/bdd
.testenv\Scripts\Activate.ps1
behave features/check_news.feature
```

## 📦 Dependencies

### Core Framework
```json
{
  "next": "15.1.3",
  "react": "^18.3.1",
  "react-dom": "^18.3.1",
  "typescript": "^5"
}
```

### Styling
```json
{
  "tailwindcss": "^4.0.0",
  "postcss": "^8.4.49"
}
```

### Development
```json
{
  "@types/node": "^20",
  "@types/react": "^18",
  "@types/react-dom": "^18",
  "eslint": "^8",
  "eslint-config-next": "15.1.3"
}
```

## 🔧 Configuration Files

### `next.config.mjs`
- Next.js configuration
- API proxy settings (if needed)
- Build optimizations

### `tailwind.config.ts`
- Tailwind v4 settings
- Custom theme colors
- Plugin configurations

### `tsconfig.json`
- TypeScript compiler options
- Path aliases (`@/app`, `@/components`)
- Strict type checking

## 🎯 API Integration

Frontend communicates with backend API at `NEXT_PUBLIC_API_BASE_URL`:

**Text Analysis:**
```typescript
POST /predict
Body: { title, text, body, log_feedback }
Response: { prediction, prob_hoax, model_version }
```

**File Analysis:**
```typescript
POST /predict-file
Body: FormData with file + log_feedback
Response: { prediction, prob_hoax, model_version, extracted_text }
```

## 🎨 Styling System

Using Tailwind CSS v4 with custom classes:

```css
/* Global styles in globals.css */
.container { max-width: 1280px; padding: 2rem; margin: 0 auto; }
.card { background: white; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
.btn { primary button styles }
.btn-outline { secondary button styles }
.tab { tab button styles }
.dropzone { file upload area styles }
.notice { warning/info box styles }
```

## 🚀 Deployment

### Vercel (Recommended)
```powershell
npm install -g vercel
vercel
```

### Docker
```dockerfile
FROM node:20-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build
EXPOSE 3000
CMD ["npm", "start"]
```

## 🔗 Related

- Backend API: `Backend/fastapi-app/`
- Model: `Model IndoBERT/`
- Tests: `tests/bdd/`

## 📝 Development Notes

- **App Router:** Uses Next.js 15 App Router (not Pages Router)
- **TypeScript:** Strict mode enabled for type safety
- **Tailwind v4:** Latest version with improved performance
- **Client Components:** Uses `'use client'` for interactive components
- **File Handling:** FileReader API for image previews
- **Responsive:** Mobile-first responsive design
