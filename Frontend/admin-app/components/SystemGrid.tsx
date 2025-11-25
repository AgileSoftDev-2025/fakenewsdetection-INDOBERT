export default function SystemGrid() {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
      {/* System Overview Card */}
      <div className="bg-white rounded-xl p-6 shadow-sm">
        <h3 className="text-base font-semibold mb-2">Sistem Overview</h3>
        <p className="text-sm text-gray-600 mb-6">
          Status kesehatan sistem dan infrastruktur
        </p>
        <div className="inline-flex items-center gap-2 bg-purple-100 text-purple-700 px-4 py-2 rounded-lg text-sm font-medium mb-4">
          <span>🧠</span>
          <span>Update Model</span>
        </div>
        <div className="text-sm text-gray-600">
          <strong>Versi model:</strong><br />
          v2.0
        </div>
      </div>

      {/* Admin Actions Card */}
      <div className="bg-white rounded-xl p-6 shadow-sm">
        <h3 className="text-base font-semibold mb-2">Aksi Admin</h3>
        <p className="text-sm text-gray-600 mb-6">
          Akses Pemodelan Versi Platform
        </p>
        <div className="flex flex-col items-center justify-center py-8 text-center min-h-[150px]">
          <div className="text-4xl text-gray-400 mb-4">⚙️</div>
          <h4 className="text-sm font-semibold mb-1">Pengaturan Sistem</h4>
          <p className="text-sm text-gray-500">Konfigurasi sistem dan parameter</p>
        </div>
      </div>
    </div>
  );
}
