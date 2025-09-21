import { useEffect, useState } from "react";

function StudentDashboard({ user, fetchWithAuth }) {
  const [courses, setCourses] = useState([]);
  const [attendance, setAttendance] = useState([]);
  const [grades, setGrades] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [activeTab, setActiveTab] = useState("courses");

  useEffect(() => {
    const loadData = async () => {
      try {
        const [c, a, g] = await Promise.all([
          fetchWithAuth("http://127.0.0.1:8000/courses"),
          fetchWithAuth("http://127.0.0.1:8000/attendance/me"),
          fetchWithAuth("http://127.0.0.1:8000/grades/me"),
        ]);
        setCourses(c || []);
        setAttendance(a || []);
        setGrades(g || []);
      } catch (err) {
        setError("❌ Failed to load dashboard data.");
      } finally {
        setLoading(false);
      }
    };
    loadData();
  }, []);

  const handleLogout = () => {
    localStorage.clear();
    window.location.href = "/";
  };

  const attendancePercent =
    attendance.length > 0
      ? Math.round(
          (attendance.filter((a) => a.status === "Present").length /
            attendance.length) *
            100
        )
      : 0;

  const gpa =
    grades.length > 0
      ? (
          grades.reduce((sum, g) => sum + (g.gpa || g.score || 0), 0) /
          grades.length
        ).toFixed(2)
      : "N/A";

  if (!user) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-[#121212] text-red-400">
        <p>User not found. Please log in again.</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#121212] text-white p-8">
      {/* Header */}
      <div className="flex justify-between items-center mb-6">
        <div>
          <h1 className="text-3xl font-bold">🎓 Student Dashboard</h1>
          <p className="text-gray-400">
            Welcome, {user.name} ({user.email})
          </p>
        </div>
        <button
          onClick={handleLogout}
          className="bg-red-500 px-4 py-2 rounded text-white hover:bg-red-400"
        >
          Logout
        </button>
      </div>

      {/* Quick Stats */}
      {!loading && !error && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
          <div className="bg-[#1f1f1f] p-4 rounded-lg text-center">
            <p className="text-2xl font-bold">{courses.length}</p>
            <p className="text-gray-400">Courses</p>
          </div>
          <div className="bg-[#1f1f1f] p-4 rounded-lg text-center">
            <p className="text-2xl font-bold">{attendancePercent}%</p>
            <p className="text-gray-400">Attendance</p>
          </div>
          <div className="bg-[#1f1f1f] p-4 rounded-lg text-center">
            <p className="text-2xl font-bold">{gpa}</p>
            <p className="text-gray-400">GPA</p>
          </div>
        </div>
      )}

      {/* Tabs */}
      <div className="flex gap-4 mb-6">
        {["courses", "attendance", "grades"].map((tab) => (
          <button
            key={tab}
            onClick={() => setActiveTab(tab)}
            className={`px-4 py-2 rounded ${
              activeTab === tab
                ? "bg-green-500 text-black font-semibold"
                : "bg-[#2a2a2a] text-gray-300 hover:bg-[#3a3a3a]"
            }`}
          >
            {tab.charAt(0).toUpperCase() + tab.slice(1)}
          </button>
        ))}
      </div>

      {/* Content */}
      {loading && <p className="text-gray-400">Loading your dashboard...</p>}
      {error && <div className="bg-red-500 text-white p-3 rounded">{error}</div>}

      {!loading && !error && (
        <div className="bg-[#1f1f1f] p-6 rounded-xl shadow">
          {activeTab === "courses" && (
            <>
              <h2 className="text-xl font-semibold mb-3">📘 Courses</h2>
              <table className="w-full text-left border-collapse">
                <thead>
                  <tr className="bg-[#2a2a2a]">
                    <th className="p-3">Course</th>
                    <th className="p-3">Teacher</th>
                  </tr>
                </thead>
                <tbody>
                  {courses.map((c) => (
                    <tr key={c.id} className="border-b border-gray-700">
                      <td className="p-3">{c.name}</td>
                      <td className="p-3">{c.teacher?.name}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </>
          )}

          {activeTab === "attendance" && (
            <>
              <h2 className="text-xl font-semibold mb-3">📊 Attendance</h2>
              <table className="w-full text-left border-collapse">
                <thead>
                  <tr className="bg-[#2a2a2a]">
                    <th className="p-3">Course</th>
                    <th className="p-3">Status</th>
                  </tr>
                </thead>
                <tbody>
                  {attendance.map((a, idx) => (
                    <tr key={idx} className="border-b border-gray-700">
                      <td className="p-3">{a.course}</td>
                      <td className="p-3">{a.status}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </>
          )}

          {activeTab === "grades" && (
            <>
              <h2 className="text-xl font-semibold mb-3">📝 Grades</h2>
              <table className="w-full text-left border-collapse">
                <thead>
                  <tr className="bg-[#2a2a2a]">
                    <th className="p-3">Course</th>
                    <th className="p-3">Assignment</th>
                    <th className="p-3">Exam</th>
                  </tr>
                </thead>
                <tbody>
                  {grades.map((g, idx) => (
                    <tr key={idx} className="border-b border-gray-700">
                      <td className="p-3">{g.course}</td>
                      <td className="p-3">{g.assignment}</td>
                      <td className="p-3">{g.exam}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </>
          )}
        </div>
      )}
    </div>
  );
}

export default StudentDashboard;
