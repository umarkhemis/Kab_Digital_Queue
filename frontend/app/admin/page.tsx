"use client";

import { useEffect, useState } from "react";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";

type Statistics = {
  total_queue_entries: number;
  completed_services: number;
  waiting_students: number;
  active_services: number;
  total_appointments: number;
  average_waiting_time_minutes: number;
  feedback_count: number;
  average_satisfaction_rating: number;
};

export default function AdminDashboard() {
  const [stats, setStats] = useState<Statistics | null>(null);
  const [message, setMessage] = useState("");

  async function loadStatistics() {
    try {
      const response = await fetch(`${API_URL}/statistics/`);

      if (!response.ok) {
        throw new Error();
      }

      const data = await response.json();
      setStats(data);
    } catch {
      setMessage("Unable to load evaluation statistics.");
    }
  }

  useEffect(() => {
    loadStatistics();

    const interval = setInterval(loadStatistics, 5000);

    return () => clearInterval(interval);
  }, []);

  return (
    <main className="container">
      <header className="header">
        <div>
          <h1>Kabale University</h1>
          <p>Queue System Evaluation Dashboard</p>
        </div>

        <div className="student">
          <strong>System Administrator</strong>
          <span>Evaluation</span>
        </div>
      </header>

      <section className="welcome">
        <h2>System Performance</h2>
        <p>
          Monitor queue activity, appointments, waiting time and
          student satisfaction.
        </p>
      </section>

      {message && <div className="message">{message}</div>}

      {stats && (
        <section className="stats-grid">
          <div className="stat-card">
            <span>Total Queue Entries</span>
            <strong>{stats.total_queue_entries}</strong>
          </div>

          <div className="stat-card">
            <span>Completed Services</span>
            <strong>{stats.completed_services}</strong>
          </div>

          <div className="stat-card">
            <span>Students Waiting</span>
            <strong>{stats.waiting_students}</strong>
          </div>

          <div className="stat-card">
            <span>Active Services</span>
            <strong>{stats.active_services}</strong>
          </div>

          <div className="stat-card">
            <span>Appointments</span>
            <strong>{stats.total_appointments}</strong>
          </div>

          <div className="stat-card">
            <span>Average Waiting Time</span>
            <strong>
              {stats.average_waiting_time_minutes} min
            </strong>
          </div>

          <div className="stat-card">
            <span>Feedback Responses</span>
            <strong>{stats.feedback_count}</strong>
          </div>

          <div className="stat-card">
            <span>Average Satisfaction</span>
            <strong>
              {stats.average_satisfaction_rating}/5
            </strong>
          </div>
        </section>
      )}

      <section className="card">
        <h2>Evaluation Measures</h2>

        <p>
          <strong>Waiting time:</strong> Time between joining the
          queue and the start of service.
        </p>

        <p>
          <strong>Queue congestion:</strong> Number of students
          currently waiting for service.
        </p>

        <p>
          <strong>User satisfaction:</strong> Student rating from
          1 to 5 after service.
        </p>
      </section>
    </main>
  );
}
