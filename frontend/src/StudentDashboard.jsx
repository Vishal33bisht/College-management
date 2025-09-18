import { useEffect, useState } from "react";

function StudentDashboard({ user, fetchWithAuth }) {
  const [courses, setCourses] = useState([]);
  const [attendance, setAttendance] = useState([]);
  const [grades, setGrades] = useState([]);

  useEffect(() => {
    const loadData = async () => {
      setCourses(await fetchWithAuth("http://127.0.0.1:8000/courses"));
      setAttendance(await fetchWithAuth("http://127.0.0.1:8000/attendance"));
      setGrades(await fetchWithAuth("http://127.0.0.1:8000/grades"));
    };
    loadData();
  }, []);

  return (
    <div className="min-h-screen bg-[#121212] text-white p-8">
      <h1 className="text-3xl font-bold mb-4">🎓 Student Dashboard</h1>
      <p className="mb-6">Welcome, {user.name} ({user.email})</p>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-[#1f1f1f] p-6 rounded-xl shadow">
          <h2 className="text-xl font-semibold mb-3">📘 Courses</h2>
          <ul>
            {courses?.map((c) => (
              <li key={c.id}>{c.name} — {c.teacher}</li>
            ))}
          </ul>
        </div>

        <div className="bg-[#1f1f1f] p-6 rounded-xl shadow">
          <h2 className="text-xl font-semibold mb-3">📊 Attendance</h2>
          <ul>
            {attendance?.map((a, idx) => (
              <li key={idx}>{a.course}: {a.attendance}</li>
            ))}
          </ul>
        </div>

        <div className="bg-[#1f1f1f] p-6 rounded-xl shadow md:col-span-2">
          <h2 className="text-xl font-semibold mb-3">📝 Grades</h2>
          <ul>
            {grades?.map((g, idx) => (
              <li key={idx}>
                {g.course} — Assignment: {g.assignment}, Exam: {g.exam}
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
}

export default StudentDashboard;
