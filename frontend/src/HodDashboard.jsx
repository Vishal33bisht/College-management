import { useEffect, useState } from "react";

function HodDashboard({ user, fetchWithAuth }) {
  const [courses, setCourses] = useState([]);
  const [users, setUsers] = useState([]);
  const [message, setMessage] = useState("");

  useEffect(() => {
    const loadData = async () => {
      try {
        const courseData = await fetchWithAuth("http://127.0.0.1:8000/courses");
        const userData = await fetchWithAuth("http://127.0.0.1:8000/users");
        setCourses(courseData);
        setUsers(userData);
      } catch {
        setMessage("❌ Failed to load dashboard data.");
      }
    };
    loadData();
  }, []);

  const handleCreateCourse = async (e) => {
    e.preventDefault();
    const name = e.target.name.value;
    const description = e.target.description.value;
    const teacher_id = e.target.teacher_id.value;

    try {
      await fetchWithAuth("http://127.0.0.1:8000/courses", {
        method: "POST",
        body: JSON.stringify({ name, description, teacher_id }),
        headers: { "Content-Type": "application/json" },
      });
      setMessage("✅ Course created");
    } catch {
      setMessage("❌ Failed to create course");
    }
  };

  return (
    <div className="min-h-screen bg-[#121212] text-white p-8">
      <h1 className="text-3xl font-bold mb-4">🏫 HOD Dashboard</h1>
      <p className="mb-6">Welcome, {user.name} ({user.email})</p>

      {message && <p className="mb-4 text-green-400">{message}</p>}

      <div className="grid gap-6">
        {/* 📈 Reports */}
        <div className="bg-[#1f1f1f] p-6 rounded-xl shadow">
          <h2 className="text-xl font-semibold mb-3">📈 Reports</h2>
          <p>Attendance and grade analytics (charts coming soon).</p>
        </div>

        {/* ✅ Approve Grades */}
        <div className="bg-[#1f1f1f] p-6 rounded-xl shadow">
          <h2 className="text-xl font-semibold mb-3">✅ Approve Grades</h2>
          <p>Workflow to approve teacher-submitted grades (backend endpoint needed).</p>
        </div>

        {/* 👨‍🏫 Manage Teachers */}
        <div className="bg-[#1f1f1f] p-6 rounded-xl shadow">
          <h2 className="text-xl font-semibold mb-3">👨‍🏫 Manage Teachers</h2>
          <form onSubmit={handleCreateCourse} className="space-y-3 mb-4">
            <input
              name="name"
              placeholder="Course Name"
              className="w-full p-2 rounded bg-[#2a2a2a]"
              required
            />
            <input
              name="description"
              placeholder="Description"
              className="w-full p-2 rounded bg-[#2a2a2a]"
              required
            />
            <select name="teacher_id" className="w-full p-2 rounded bg-[#2a2a2a]" required>
              <option value="">Select Teacher</option>
              {users.filter(u => u.role === "Teacher").map((t) => (
                <option key={t.id} value={t.id}>
                  {t.name} ({t.email})
                </option>
              ))}
            </select>
            <button
              type="submit"
              className="w-full bg-green-500 py-2 rounded text-black font-bold hover:bg-green-400"
            >
              Assign Course
            </button>
          </form>

          <h3 className="text-lg font-semibold mb-2">👥 Faculty List</h3>
          <ul className="space-y-2">
            {users.filter(u => u.role === "Teacher").map((t) => (
              <li key={t.id} className="bg-[#2a2a2a] p-3 rounded">
                {t.name} — {t.email}
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
}

export default HodDashboard;
