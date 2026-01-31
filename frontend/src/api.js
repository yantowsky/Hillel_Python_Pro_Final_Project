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