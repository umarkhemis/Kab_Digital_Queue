
"use client";

import { useEffect, useState } from "react";

const API_URL = "http://127.0.0.1:8000";

type Office = {
  id: number;
  name: string;
};

type Service = {
  id: number;
  name: string;
};

type QueueEntry = {
  id: number;
  queue_number: number;
  user_id: number;
  status: string;
  joined_at: string;
};

export default function StaffDashboard() {
  const [offices, setOffices] = useState<Office[]>([]);
  const [services, setServices] = useState<Service[]>([]);
  const [selectedOffice, setSelectedOffice] = useState("");
  const [selectedService, setSelectedService] = useState("");
  const [queue, setQueue] = useState<QueueEntry[]>([]);
  const [message, setMessage] = useState("");

  useEffect(() => {
    fetch(`${API_URL}/services/offices`)
      .then((res) => res.json())
      .then((data) => setOffices(data));
  }, []);

  useEffect(() => {
    if (!selectedOffice) {
      setServices([]);
      setSelectedService("");
      setQueue([]);
      return;
    }

    fetch(`${API_URL}/services/office/${selectedOffice}`)
      .then((res) => res.json())
      .then((data) => setServices(data));
  }, [selectedOffice]);

  async function loadQueue(serviceId: string) {
    if (!serviceId) {
      setQueue([]);
      return;
    }

    const response = await fetch(
      `${API_URL}/staff/queue/${serviceId}`
    );

    const data = await response.json();
    setQueue(data);
  }

  async function callNext() {
    if (!selectedService) {
      setMessage("Please select a service.");
      return;
    }

    const response = await fetch(
      `${API_URL}/staff/queue/${selectedService}/next`,
      {
        method: "POST",
      }
    );

    const data = await response.json();

    if (!response.ok) {
      setMessage(data.detail || "Unable to call next student.");
      return;
    }

    setMessage(`Student ${data.queue_number} has been called.`);
    loadQueue(selectedService);
  }

  async function startService(queueId: number) {
    const response = await fetch(
      `${API_URL}/staff/queue/${queueId}/start`,
      {
        method: "POST",
      }
    );

    const data = await response.json();

    if (!response.ok) {
      setMessage(data.detail || "Unable to start service.");
      return;
    }

    setMessage(`Queue ${data.queue_number} is now being served.`);
    loadQueue(selectedService);
  }

  async function completeService(queueId: number) {
    const response = await fetch(
      `${API_URL}/staff/queue/${queueId}/complete`,
      {
        method: "POST",
      }
    );

    const data = await response.json();

    if (!response.ok) {
      setMessage(data.detail || "Unable to complete service.");
      return;
    }

    setMessage(`Queue ${data.queue_number} has been completed.`);
    loadQueue(selectedService);
  }

  return (
    <main className="staff-container">
      <header className="staff-header">
        <div>
          <h1>Kabale University</h1>
          <p>Staff Queue Management Dashboard</p>
        </div>

        <div>
          <strong>Service Staff</strong>
        </div>
      </header>

      <section className="staff-card">
        <h2>Select Service Point</h2>

        <label>Office</label>

        <select
          value={selectedOffice}
          onChange={(e) => setSelectedOffice(e.target.value)}
        >
          <option value="">Choose office</option>

          {offices.map((office) => (
            <option key={office.id} value={office.id}>
              {office.name}
            </option>
          ))}
        </select>

        <label>Service</label>

        <select
          value={selectedService}
          disabled={!selectedOffice}
          onChange={(e) => {
            setSelectedService(e.target.value);
            loadQueue(e.target.value);
          }}
        >
          <option value="">Choose service</option>

          {services.map((service) => (
            <option key={service.id} value={service.id}>
              {service.name}
            </option>
          ))}
        </select>

        <button className="call-button" onClick={callNext}>
          Call Next Student
        </button>

        {message && <div className="staff-message">{message}</div>}
      </section>

      <section className="staff-card">
        <div className="queue-heading">
          <div>
            <h2>Current Queue</h2>
            <p>{queue.length} active queue entries</p>
          </div>

          {selectedService && (
            <button
              className="refresh-button"
              onClick={() => loadQueue(selectedService)}
            >
              Refresh
            </button>
          )}
        </div>

        {queue.length === 0 ? (
          <div className="empty">
            No students are currently waiting.
          </div>
        ) : (
          <div className="queue-list">
            {queue.map((entry) => (
              <div className="queue-row" key={entry.id}>
                <div className="queue-token">
                  <strong>#{entry.queue_number}</strong>
                  <span>Student {entry.user_id}</span>
                </div>

                <span className={`status ${entry.status}`}>
                  {entry.status}
                </span>

                <div className="queue-actions">
                  {entry.status === "called" && (
                    <button
                      onClick={() => startService(entry.id)}
                    >
                      Start Service
                    </button>
                  )}

                  {entry.status === "serving" && (
                    <button
                      onClick={() => completeService(entry.id)}
                    >
                      Complete
                    </button>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
      </section>
    </main>
  );
}