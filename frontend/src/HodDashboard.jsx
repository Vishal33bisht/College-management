function HodDashboard({ user }) {
  return (
    <div className="min-h-screen bg-[#121212] text-white p-8">
      <h1 className="text-3xl font-bold mb-4">🏫 HOD Dashboard</h1>
      <p className="mb-6">Welcome, {user.name} ({user.email})</p>

      <div className="grid gap-6">
        <div className="bg-[#1f1f1f] p-6 rounded-xl shadow">
          <h2 className="text-xl font-semibold mb-3">📈 Reports</h2>
          <p>Attendance and grade analytics (charts).</p>
        </div>

        <div className="bg-[#1f1f1f] p-6 rounded-xl shadow">
          <h2 className="text-xl font-semibold mb-3">✅ Approve Grades</h2>
          <p>Workflow: approve teacher-submitted grades.</p>
        </div>

        <div className="bg-[#1f1f1f] p-6 rounded-xl shadow">
          <h2 className="text-xl font-semibold mb-3">👨‍🏫 Manage Teachers</h2>
          <p>Assign courses, manage faculty (future feature).</p>
        </div>
      </div>
    </div>
  );
}

export default HodDashboard;
