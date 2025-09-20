import { useState } from "react";
import { BrowserRouter, Routes, Route, useNavigate } from "react-router-dom";
import { FiMail, FiLock, FiBox } from "react-icons/fi";
import Dashboard from "./Dashboard";
import ProtectedRoute from './components/ProtectedRoute';

// --- Register Component ---
function Register() {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [role, setRole] = useState("Student");
  const [message, setMessage] = useState("");
  const navigate = useNavigate();

  const handleRegister = async (e) => {
    e.preventDefault();
    setMessage("");
    try {
      const res = await fetch("http://127.0.0.1:8000/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, email, password, role }),
      });

      if (!res.ok) {
        const err = await res.json().catch(() => ({}));
        throw new Error(err.detail || "Registration failed");
      }

      await res.json();
      setMessage("✅ Registered successfully! Redirecting...");
      setTimeout(() => navigate("/"), 1500);
    } catch (err) {
      setMessage("❌ " + err.message);
    }
  };

  return (
    <div className="flex h-screen items-center justify-center bg-[#1a1a1a] text-white">
      <form
        onSubmit={handleRegister}
        className="bg-[#2a2a2a] p-8 rounded-lg w-96"
      >
        <h2 className="text-2xl font-bold mb-4 text-center">Register</h2>

        <input
          type="text"
          placeholder="Full Name"
          value={name}
          onChange={(e) => setName(e.target.value)}
          className="w-full mb-3 p-3 rounded bg-[#3c3c3c]"
        />

        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          className="w-full mb-3 p-3 rounded bg-[#3c3c3c]"
        />

        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="w-full mb-3 p-3 rounded bg-[#3c3c3c]"
        />

        <select
          value={role}
          onChange={(e) => setRole(e.target.value)}
          className="w-full mb-3 p-3 rounded bg-[#3c3c3c]"
        >
          <option value="Student">Student</option>
          <option value="Teacher">Teacher</option>
          <option value="HOD">HOD</option>
          <option value="Admin">Admin</option>
          <option value="TA">TA</option>
        </select>

        <button
          type="submit"
          className="w-full bg-green-500 py-2 rounded text-gray-900 font-bold hover:bg-green-400"
        >
          Register
        </button>

        {message && (
          <p className="mt-3 text-center text-sm">{message}</p>
        )}
      </form>
    </div>
  );
}

// --- Login Component ---
function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [role, setRole] = useState("Student"); // ✅ match backend casing
  const [message, setMessage] = useState("");
  const navigate = useNavigate();

  const handleLogin = async () => {
    setMessage("");
    try {
      const response = await fetch("http://127.0.0.1:8000/token", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: new URLSearchParams({
          username: email,
          password: password,
        }),
      });

      if (!response.ok) {
        const err = await response.json().catch(() => ({}));
        throw new Error(err.detail || "Login failed");
      }

      const data = await response.json();
      localStorage.setItem("token", data.access_token);
      localStorage.setItem("role", role); // ✅ store role in correct casing
      setMessage("✅ Login successful!");
      navigate("/dashboard");
    } catch (error) {
      console.error("Login error:", error);
      setMessage("❌ " + error.message);
    }
  };

  return (
    <div className="relative flex min-h-screen flex-col items-center justify-center bg-[#1a1a1a] font-sans text-white">
      {/* Header Branding */}
      <div className="absolute top-8 left-8 flex items-center gap-2">
        <FiBox className="h-7 w-7 text-[#34D399]" />
        <h1 className="text-xl font-bold">College Management</h1>
      </div>

      {/* Login Box */}
      <div className="w-full max-w-sm rounded-2xl bg-[#2a2a2a] p-8">
        <div className="mb-6 text-center">
          <h2 className="text-3xl font-bold">Welcome back!</h2>
          <p className="mt-2 text-gray-400">Log in to your account to continue.</p>
        </div>

        <div className="space-y-4">
          {/* Email */}
          <div className="relative">
            <FiMail className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400" />
            <input
              type="email"
              placeholder="Enter your email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full rounded-lg border border-gray-600 bg-[#3c3c3c] py-3 pl-12 pr-4 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-[#34D399]"
            />
          </div>

          {/* Password */}
          <div className="relative">
            <FiLock className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400" />
            <input
              type="password"
              placeholder="Enter your password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full rounded-lg border border-gray-600 bg-[#3c3c3c] py-3 pl-12 pr-4 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-[#34D399]"
            />
          </div>

          {/* Role Selector */}
          <div className="relative">
            <label className="block mb-1 text-sm text-gray-300">Login as</label>
            <select
              value={role}
              onChange={(e) => setRole(e.target.value)}
              className="w-full rounded-lg border border-gray-600 bg-[#3c3c3c] py-3 px-4 text-gray-100 focus:outline-none focus:ring-2 focus:ring-[#34D399]"
            >
              <option value="Student">Student</option>
              <option value="Teacher">Teacher</option>
              <option value="HOD">HOD</option>
            </select>
          </div>

          {/* Submit Button */}
          <button
            onClick={handleLogin}
            className="w-full rounded-lg bg-[#34D399] py-3 font-semibold text-gray-900 transition hover:bg-[#2cb782]"
          >
            Login
          </button>
        </div>

        {message && (
          <p
            className={`mt-4 text-center font-medium ${
              message.includes("successful") ? "text-green-400" : "text-red-400"
            }`}
          >
            {message}
          </p>
        )}

        <p className="mt-4 text-center text-gray-400">
          Don’t have an account?{" "}
          <a href="/register" className="text-green-400 hover:underline">Register</a>
        </p>
      </div>
    </div>
  );
}

// --- App Root ---
function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route
          path="/dashboard"
          element={
            <ProtectedRoute allowedRoles={['Student', 'Teacher', 'HOD']}>
              <Dashboard />
            </ProtectedRoute>
          }
        />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
