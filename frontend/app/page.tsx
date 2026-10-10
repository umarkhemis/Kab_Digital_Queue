"use client";

import { useEffect, useState } from "react";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";

type Office = {
  id: number;
  name: string;
  description: string;
};

type Service = {
  id: number;
  office_id: number;
  name: string;
  description: string;
};

type QueueStatus = {
  queue_id: number;
  queue_number: number;
  status: string;
  position: number;
};

type Appointment = {
  id: number;
  service_id: number;
  appointment_time: string;
  status: string;
};

export default function Home() {
  const [offices, setOffices] = useState<Office[]>([]);
  const [services, setServices] = useState<Service[]>([]);
  const [selectedOffice, setSelectedOffice] = useState("");
  const [selectedService, setSelectedService] = useState("");

  const [queueStatus, setQueueStatus] = useState<QueueStatus | null>(null);

  const [appointments, setAppointments] = useState<Appointment[]>([]);
  const [appointmentTime, setAppointmentTime] = useState("");

  const [rating, setRating] = useState(0);
  const [comment, setComment] = useState("");

  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  const userId = 1;

  useEffect(() => {
    fetch(`${API_URL}/services/offices`)
      .then((res) => res.json())
      .then((data) => setOffices(data))
      .catch(() => setMessage("Unable to load offices."));
  }, []);

  useEffect(() => {
    if (!selectedOffice) {
      setServices([]);
      setSelectedService("");
      return;
    }

    fetch(`${API_URL}/services/office/${selectedOffice}`)
      .then((res) => res.json())
      .then((data) => setServices(data))
      .catch(() => setMessage("Unable to load services."));
  }, [selectedOffice]);

  useEffect(() => {
    loadAppointments();
  }, []);

  useEffect(() => {
    if (!queueStatus?.queue_id) return;

    const interval = setInterval(async () => {
      try {
        const response = await fetch(
          `${API_URL}/queue/${queueStatus.queue_id}`
        );

        if (!response.ok) return;

        const data = await response.json();
        setQueueStatus(data);
      } catch {
        console.log("Unable to refresh queue status.");
      }
    }, 5000);

    return () => clearInterval(interval);
  }, [queueStatus?.queue_id]);

  async function loadAppointments() {
    try {
      const response = await fetch(
        `${API_URL}/appointments/user/${userId}`
      );

      if (!response.ok) return;

      const data = await response.json();
      setAppointments(data);
    } catch {
      console.log("Unable to load appointments.");
    }
  }

  async function joinQueue() {
    if (!selectedService) {
      setMessage("Please select a service first.");
      return;
    }

    setLoading(true);
    setMessage("");

    try {
      const response = await fetch(`${API_URL}/queue/join`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          user_id: userId,
          service_id: Number(selectedService),
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        setMessage(data.detail || "Unable to join queue.");
        return;
      }

      setQueueStatus({
        queue_id: data.queue_id,
        queue_number: data.queue_number,
        status: data.status,
        position: data.position,
      });

      setMessage("Successfully joined the queue.");
    } catch {
      setMessage("Could not connect to the server.");
    } finally {
      setLoading(false);
    }
  }

  async function bookAppointment() {
    if (!selectedService) {
      setMessage("Please select a service first.");
      return;
    }

    if (!appointmentTime) {
      setMessage("Please select an appointment date and time.");
      return;
    }

    setLoading(true);
    setMessage("");

    try {
      const response = await fetch(`${API_URL}/appointments/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          user_id: userId,
          service_id: Number(selectedService),
          appointment_time: appointmentTime,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        setMessage(data.detail || "Unable to book appointment.");
        return;
      }

      setMessage("Appointment booked successfully.");
      setAppointmentTime("");
      await loadAppointments();
    } catch {
      setMessage("Could not connect to the server.");
    } finally {
      setLoading(false);
    }
  }

  async function submitFeedback() {
    if (!rating) {
      setMessage("Please select a rating from 1 to 5.");
      return;
    }

    if (!queueStatus?.queue_id) {
      setMessage("Please complete a queue service before submitting feedback.");
      return;
    }

    setLoading(true);
    setMessage("");

    try {
      const response = await fetch(`${API_URL}/feedback/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          user_id: userId,
          queue_id: queueStatus.queue_id,
          rating,
          comment: comment || null,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        setMessage(data.detail || "Unable to submit feedback.");
        return;
      }

      setMessage("Thank you. Your feedback has been submitted.");
      setRating(0);
      setComment("");
    } catch {
      setMessage("Could not connect to the server.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="container">
      <header className="header">
        <div>
          <h1>Kabale University</h1>
          <p>Digital Queue & Appointment System</p>
        </div>

        <div className="student">
          <strong>Ahmed Umar</strong>
          <span>Student</span>
        </div>
      </header>

      <section className="welcome">
        <h2>Student Support Services</h2>
        <p>
          Join a queue remotely or book an appointment without waiting
          physically at the office.
        </p>
      </section>

      <section className="card">
        <h2>Request a Service</h2>

        <label>Select Office</label>

        <select
          value={selectedOffice}
          onChange={(e) => setSelectedOffice(e.target.value)}
        >
          <option value="">Choose an office</option>

          {offices.map((office) => (
            <option key={office.id} value={office.id}>
              {office.name}
            </option>
          ))}
        </select>

        <label>Select Service</label>

        <select
          value={selectedService}
          onChange={(e) => setSelectedService(e.target.value)}
          disabled={!selectedOffice}
        >
          <option value="">Choose a service</option>

          {services.map((service) => (
            <option key={service.id} value={service.id}>
              {service.name}
            </option>
          ))}
        </select>

        <label>Appointment Date and Time</label>

        <input
          type="datetime-local"
          value={appointmentTime}
          onChange={(e) => setAppointmentTime(e.target.value)}
        />

        <div className="actions">
          <button onClick={joinQueue} disabled={loading}>
            {loading ? "Processing..." : "Join Queue"}
          </button>

          <button
            className="secondary"
            onClick={bookAppointment}
            disabled={loading}
          >
            Book Appointment
          </button>
        </div>

        {message && <div className="message">{message}</div>}
      </section>

      {queueStatus && (
        <section className="queue-card">
          <h2>Your Queue Status</h2>

          <div className="queue-number">
            {queueStatus.queue_number}
          </div>

          <p>Queue Number</p>

          <div className="queue-info">
            <div>
              <span>Position</span>
              <strong>{queueStatus.position}</strong>
            </div>

            <div>
              <span>Status</span>
              <strong>{queueStatus.status}</strong>
            </div>
          </div>
        </section>
      )}

      <section className="card">
        <h2>My Appointments</h2>

        {appointments.length === 0 ? (
          <p>No appointments booked yet.</p>
        ) : (
          <div>
            {appointments.map((appointment) => (
              <div key={appointment.id} className="appointment">
                <strong>
                  Appointment #{appointment.id}
                </strong>

                <p>
                  {new Date(
                    appointment.appointment_time
                  ).toLocaleString()}
                </p>

                <span>{appointment.status}</span>
              </div>
            ))}
          </div>
        )}
      </section>

      {queueStatus && (
        <section className="card">
          <h2>Service Feedback</h2>

          <p>How satisfied were you with the service?</p>

          <div className="rating">
            {[1, 2, 3, 4, 5].map((value) => (
              <button
                key={value}
                type="button"
                className={rating === value ? "rating-selected" : ""}
                onClick={() => setRating(value)}
              >
                {value}
              </button>
            ))}
          </div>

          <textarea
            placeholder="Optional comment"
            value={comment}
            onChange={(e) => setComment(e.target.value)}
            rows={4}
          />

          <button onClick={submitFeedback} disabled={loading}>
            Submit Feedback
          </button>
        </section>
      )}
    </main>
  );
}
