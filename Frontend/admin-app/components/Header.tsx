import Link from 'next/link';

export default function Header() {
  return (
    <header className="bg-white shadow-sm">
      <div className="px-8 py-4 flex justify-between items-center">
        {/* Logo Section */}
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-gray-900 rounded-lg flex items-center justify-center text-white text-xl">
            ◉
          </div>
          <div>
            <h1 className="text-base font-semibold">FakeNewsDetector Admin</h1>
            <p className="text-xs text-gray-600">Panel Administrasi</p>
          </div>
        </div>

        {/* Navigation Menu */}
        <nav className="flex items-center gap-8">
          <Link 
            href="#" 
            className="flex items-center gap-2 text-gray-600 hover:text-gray-900 text-sm"
          >
            <span>📊</span>
            <span>Dataset</span>
          </Link>
          <Link 
            href="#" 
            className="flex items-center gap-2 text-gray-600 hover:text-gray-900 text-sm"
          >
            <span>📈</span>
            <span>Analytics</span>
          </Link>
          <Link 
            href="#" 
            className="flex items-center gap-2 text-gray-600 hover:text-gray-900 text-sm"
          >
            <span>⚙️</span>
            <span>Pengaturan</span>
          </Link>
        </nav>
      </div>
    </header>
  );
}
