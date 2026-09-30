import React, { useState } from 'react';

export const LoginScreen: React.FC<{ onLogin: () => void }> = ({ onLogin }) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    
    try {
      const { apiClient } = await import('@/api/client');
      const response = await apiClient.login(username, password);
      localStorage.setItem('aiseo_auth_token', response.token);
      onLogin();
    } catch (err: any) {
      setError(err.message || 'Invalid username or password');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-slate-50 dark:bg-slate-800 dark:bg-slate-950">
      <div className="p-8 bg-white dark:bg-slate-900 rounded-xl shadow-xl border border-slate-200 dark:border-slate-700 dark:border-slate-800 space-y-6 w-full max-w-sm">
        <div className="text-center space-y-2">
          <div className="mx-auto w-10 h-10 rounded-lg bg-slate-900 dark:bg-slate-50 dark:bg-white dark:bg-slate-900 flex items-center justify-center text-white dark:text-slate-900 font-bold text-sm tracking-tight shadow-xs mb-4">
            <span>AI</span>
          </div>
          <h2 className="text-xl font-bold text-slate-900 dark:text-slate-50">Welcome to AISEO</h2>
          <p className="text-sm text-slate-500 dark:text-slate-400">Please enter your details to sign in</p>
        </div>
        
        <form onSubmit={handleSubmit} className="space-y-4">
          {error && (
            <div className="p-2.5 bg-rose-50 dark:bg-rose-950/30 dark:bg-rose-950/50 border border-rose-200 dark:border-rose-900 rounded-lg text-xs text-rose-600 dark:text-rose-400 font-medium text-center">
              {error}
            </div>
          )}
          
          <div className="space-y-1.5">
            <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300">Username</label>
            <input 
              type="text" 
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="username"
              className="w-full bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-lg px-3.5 py-2 text-sm text-slate-900 dark:text-slate-50 focus:outline-none focus:border-slate-900 dark:focus:border-slate-500 transition-colors"
              required
            />
          </div>
          
          <div className="space-y-1.5">
            <label className="block text-xs font-semibold text-slate-700 dark:text-slate-300">Password</label>
            <input 
              type="password" 
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="••••••••"
              className="w-full bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-lg px-3.5 py-2 text-sm text-slate-900 dark:text-slate-50 focus:outline-none focus:border-slate-900 dark:focus:border-slate-500 transition-colors"
              required
            />
          </div>
          
          <button 
            type="submit"
            className="w-full px-4 py-2.5 bg-slate-900 dark:bg-slate-50 dark:bg-white dark:bg-slate-900 text-white dark:text-slate-900 rounded-lg text-sm font-semibold hover:bg-slate-800 dark:hover:bg-slate-200 transition-colors mt-2"
          >
            Sign In
          </button>
        </form>
      </div>
    </div>
  );
};
