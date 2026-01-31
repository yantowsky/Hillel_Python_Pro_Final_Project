const API_BASE = "http://127.0.0.1:8000";

export async function login(username, password) {
    const res = await fetch(`${API_BASE}/api/token/`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({username, password}),
    });

    if (!res.ok) {
        throw new Error("Login failed");
    }
    return res.json(); // {access, refresh}
}

export async function getMe(accessToken) {
    const res = await fetch(`${API_BASE}/api/me/`, {
        headers: {Authorization: `Bearer ${accessToken}`},
    });

    if (!res.ok) {
        throw new Error("Unauthorized");
    }
    return res.json();
}

export async function getDoctors(accessToken) {
    const res = await fetch(`${API_BASE}/api/doctors/`, {
        headers: {Authorization: `Bearer ${accessToken}`},
    });
    if (!res.ok) throw new Error("Failed to load doctors");
    return res.json();
}

export async function getAppointments(accessToken) {
    const res = await fetch(`${API_BASE}/api/appointments/`, {
        headers: {Authorization: `Bearer ${accessToken}`},
    });
    if (!res.ok) throw new Error("Failed to load appointments");
    return res.json();
}

export async function createAppointment(accessToken, doctorId, startsAt) {
    const res = await fetch(`${API_BASE}/api/appointments/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${accessToken}`,
        },
        body: JSON.stringify({doctor: Number(doctorId), starts_at: startsAt}),
    });

    if (!res.ok) {
        const text = await res.text();
        throw new Error(`Failed to create appointment: ${text}`);
    }
    return res.json();
}