import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import StudentDashboard from "./StudentDashboard";
import TeacherDashboard from "./TeacherDashboard";
import HodDashboard from "./HodDashboard";

function Dashboard() {
  const [user, setUser] = useState(null);
  const navigate = useNavigate();

  const fetchWithAuth = async (url) => {
    const token = localStorage.getItem("token");
    if (!token) {
      navigate("/");
      return null;
    }

    const response = await fetch(url, {
      headers: { Authorization: `Bearer ${token}` },
    });

    if (response.status === 401) {
      localStorage.removeItem("token");
      navigate("/");
      return null;
    }
    return await response.json();
  };

  useEffect(() => {
    const loadUser = async () => {
      const me = await fetchWithAuth("http://127.0.0.1:8000/me");
      if (me) setUser(me);
    };
    loadUser();
  }, []);

  if (!user) return <div className="text-white p-6">Loading...</div>;

  switch (user.role) {
  case "Student":
    return <StudentDashboard user={user} fetchWithAuth={fetchWithAuth} />;
  case "Teacher":
    return <TeacherDashboard user={user} fetchWithAuth={fetchWithAuth} />;
  case "HOD":
    return <HodDashboard user={user} fetchWithAuth={fetchWithAuth} />;
  default:
    return (
      <div className="text-white p-6">
        Unknown role: {user.role}
      </div>
    );
}
}

export default Dashboard;
