import { useEffect, useState } from "react";

function TeacherDashboard({ user, fetchWithAuth }) {
  const [courses, setCourses] = useState([]);
  const [assignments, setAssignments] = useState([]);
  const [message, setMessage] = useState("");

  useEffect(() => {
    const loadData = async () => {
      try {
        const courseData = await fetchWithAuth("http://127.0.0.1:8000/courses?teacher_id=" + user.id);
        const assignmentData = await fetchWithAuth("http://127.0.0.1:8000/assignments-to-review");
        setCourses(courseData);
        setAssignments(assignmentData);
      } catch (err) {
        setMessage("❌ Failed to load dashboard data.");
      }
    };
    loadData();
  }, []);

  const handleAttendance = async (studentId, courseId, status) => {
    try {
      await fetchWithAuth("http://127.0.0.1:8000/attendance", {
        method: "POST",
        body: JSON.stringify({ student_id: studentId, course_id: courseId, status }),
        headers: { "Content-Type": "application/json" },
      });
      setMessage("✅ Attendance marked");
    } catch {
      setMessage("❌ Failed to mark attendance");
    }
  };

  return (
    <div className="min-h-screen bg-[#121212] text-white p-8">
      <h1 className="text-3xl font-bold mb-4">👨‍🏫 Teacher Dashboard</h1>
      <p className="mb-6">Welcome, {user.name} ({user.email})</p>

      {message && <p className="mb-4 text-green-400">{message}</p>}

      <div className="grid gap-6">
        {/* My Courses */}
        <div className="bg-[#1f1f1f] p-6 rounded-xl shadow">
          <h2 className="text-xl font-semibold mb-3">📘 My Courses</h2>
          <ul className="space-y-2">
            {courses.map((course) => (
              <li key={course.id} className="bg-[#2a2a2a] p-3 rounded">
                {course.name} — {course.description}
              </li>
            ))}
          </ul>
        </div>

        {/* Review Assignments */}
        <div className="bg-[#1f1f1f] p-6 rounded-xl shadow">
          <h2 className="text-xl font-semibold mb-3">📝 Review Assignments</h2>
          <ul className="space-y-2">
            {assignments.map((a) => (
              <li key={a.id} className="bg-[#2a2a2a] p-3 rounded">
                Student {a.student_id} submitted for Assignment {a.assignment_id}
                <a
                  href={`http://127.0.0.1:8000/${a.file_path}`}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="ml-2 text-green-400 underline"
                >
                  View File
                </a>
              </li>
            ))}
          </ul>
        </div>

        {/* Mark Attendance */}
        <div className="bg-[#1f1f1f] p-6 rounded-xl shadow">
          <h2 className="text-xl font-semibold mb-3">📊 Mark Attendance</h2>
          <form
            onSubmit={(e) => {
              e.preventDefault();
              const studentId = e.target.studentId.value;
              const courseId = e.target.courseId.value;
              const status = e.target.status.value;
              handleAttendance(studentId, courseId, status);
            }}
            className="space-y-3"
          >
            <input
              name="studentId"
              placeholder="Student ID"
              className="w-full p-2 rounded bg-[#2a2a2a]"
              required
            />
            <select name="courseId" className="w-full p-2 rounded bg-[#2a2a2a]" required>
              <option value="">Select Course</option>
              {courses.map((c) => (
                <option key={c.id} value={c.id}>{c.name}</option>
              ))}
            </select>
            <select name="status" className="w-full p-2 rounded bg-[#2a2a2a]" required>
              <option value="Present">Present</option>
              <option value="Absent">Absent</option>
            </select>
            <button
              type="submit"
              className="w-full bg-green-500 py-2 rounded text-black font-bold hover:bg-green-400"
            >
              Submit Attendance
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}

export default TeacherDashboard;
