import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api, { setAuthToken } from './services/api';

function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [role, setRole] = useState('Student'); // or 'Teacher', 'HOD'
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const res = await api.post('/login', {
        email,
        password,
        role,
      });

      // ✅ Store token and user info
      localStorage.setItem('token', res.data.access_token);
      localStorage.setItem('role', res.data.role);
      localStorage.setItem('name', res.data.name);

      // ✅ Set token for future requests
      setAuthToken(res.data.access_token);

      // ✅ Redirect to role-based dashboard
      navigate(`/${res.data.role.toLowerCase()}-dashboard`);
    } catch (err) {
      alert('Login failed: ' + err.response.data.detail);
    }
  };

  return (
    <form onSubmit={handleLogin}>
      <input
        type="email"
        placeholder="Email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        required
      />
      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        required
      />
      <select value={role} onChange={(e) => setRole(e.target.value)}>
        <option value="Student">Student</option>
        <option value="Teacher">Teacher</option>
        <option value="HOD">HOD</option>
      </select>
      <button type="submit">Login</button>
    </form>
  );
}

export default Login;
