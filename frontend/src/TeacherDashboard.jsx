function TeacherDashboard({ user, fetchWithAuth }) {
  return (
    <div className="min-h-screen bg-[#121212] text-white p-8">
      <h1 className="text-3xl font-bold mb-4">👨‍🏫 Teacher Dashboard</h1>
      <p className="mb-6">Welcome, {user.name} ({user.email})</p>

      <div className="grid gap-6">
        <div className="bg-[#1f1f1f] p-6 rounded-xl shadow">
          <h2 className="text-xl font-semibold mb-3">📘 My Courses</h2>
          <p>List courses taught by this teacher (backend filter needed).</p>
        </div>

        <div className="bg-[#1f1f1f] p-6 rounded-xl shadow">
          <h2 className="text-xl font-semibold mb-3">📝 Review Assignments</h2>
          <p>Fetch `/assignments-to-review` (to be implemented).</p>
        </div>

        <div className="bg-[#1f1f1f] p-6 rounded-xl shadow">
          <h2 className="text-xl font-semibold mb-3">📊 Mark Attendance</h2>
          <p>Interactive attendance marking UI.</p>
        </div>
      </div>
    </div>
  );
}

export default TeacherDashboard;
