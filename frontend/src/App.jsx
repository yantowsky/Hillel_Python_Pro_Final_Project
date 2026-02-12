import {useEffect, useState} from "react";
import {projectA, projectB} from "./api/http.js";

function LoginForm({label, onLogin}) {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [err, setErr] = useState("");

    const submit = async (e) => {
        e.preventDefault();
        setErr("");
        try {
            await onLogin({username, password});
            setPassword("");
        } catch (e2) {
            setErr(String(e2.message || e2));
        }
    };

    return (
        <div style={{border: "1px solid #ddd", padding: 12, borderRadius: 8}}>
            <h3>{label}</h3>
            <form onSubmit={submit} style={{display: "grid", gap: 8}}>
                <input
                    placeholder="username"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                />
                <input
                    placeholder="password"
                    type="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                />
                <button type="submit">Login</button>
                {err ? <div style={{color: "crimson"}}>{err}</div> : null}
            </form>
        </div>
    );
}

export default function App() {
    const [appointments, setAppointments] = useState([]);
    const [conversations, setConversations] = useState([]);
    const [selectedConvId, setSelectedConvId] = useState(null);
    const [messages, setMessages] = useState([]);
    const [msgText, setMsgText] = useState("");
    const [error, setError] = useState("");

    const hasTokenA = Boolean(localStorage.getItem("tokenA"));
    const hasTokenB = Boolean(localStorage.getItem("tokenB"));

    const loginA = async ({username, password}) => {
        const baseUrl = import.meta.env.VITE_PROJECTA_API_URL;
        const res = await fetch(`${baseUrl}/api/auth/token/`, {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({username, password}),
        });
        const data = await res.json();
        if (!res.ok) throw new Error(data?.detail || "Login A failed");
        localStorage.setItem("tokenA", data.access);
        await loadAppointments();
    };

    const loginB = async ({username, password}) => {
        const baseUrl = import.meta.env.VITE_PROJECTB_API_URL;
        const res = await fetch(`${baseUrl}/api/auth/token/`, {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({username, password}),
        });
        const data = await res.json();
        if (!res.ok) throw new Error(data?.detail || "Login B failed");
        localStorage.setItem("tokenB", data.access);
        await loadConversations();
    };

    const logout = () => {
        localStorage.removeItem("tokenA");
        localStorage.removeItem("tokenB");
        setAppointments([]);
        setConversations([]);
        setSelectedConvId(null);
        setMessages([]);
    };

    const loadAppointments = async () => {
        setError("");
        const data = await projectA("/api/appointments/");
        setAppointments(data);
    };

    const loadConversations = async () => {
        setError("");
        const data = await projectB("/api/telemed/conversations/");
        setConversations(data);
    };

    const loadMessages = async (convId) => {
        setError("");
        const data = await projectB(`/api/telemed/conversations/${convId}/messages/`);
        setMessages(data);
    };

    const sendMessage = async () => {
        if (!selectedConvId || !msgText.trim()) return;
        setError("");
        await projectB(`/api/telemed/conversations/${selectedConvId}/messages/`, {
            method: "POST",
            body: JSON.stringify({text: msgText}),
        });
        setMsgText("");
        await loadMessages(selectedConvId);
    };

    useEffect(() => {
        const run = async () => {
            try {
                if (hasTokenA) await loadAppointments();
                if (hasTokenB) await loadConversations();
            } catch (e) {
                setError(String(e.message || e));
            }
        };
        run();
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, []);

    return (
        <div style={{padding: 16, fontFamily: "system-ui, sans-serif"}}>
            <h2>Medical Demo UI (React)</h2>

            <div style={{display: "flex", gap: 12, flexWrap: "wrap"}}>
                {!hasTokenA ? (
                    <LoginForm label="Login ProjectA (Appointments)" onLogin={loginA}/>
                ) : (
                    <div style={{border: "1px solid #ddd", padding: 12, borderRadius: 8}}>
                        <h3>ProjectA</h3>
                        <button onClick={loadAppointments}>Refresh appointments</button>
                    </div>
                )}

                {!hasTokenB ? (
                    <LoginForm label="Login ProjectB (Messages)" onLogin={loginB}/>
                ) : (
                    <div style={{border: "1px solid #ddd", padding: 12, borderRadius: 8}}>
                        <h3>ProjectB</h3>
                        <button onClick={loadConversations}>Refresh conversations</button>
                    </div>
                )}

                <div style={{border: "1px solid #ddd", padding: 12, borderRadius: 8}}>
                    <h3>Session</h3>
                    <button onClick={logout}>Logout</button>
                </div>
            </div>

            {error ? <p style={{color: "crimson"}}>{error}</p> : null}

            <hr/>

            <h3>Appointments (ProjectA)</h3>
            <pre style={{background: "#f6f6f6", color: "#111", padding: 12, borderRadius: 8}}>
        {JSON.stringify(appointments, null, 2)}
      </pre>

            <hr/>

            <h3>Conversations (ProjectB)</h3>
            <div style={{display: "flex", gap: 12}}>
                <div style={{minWidth: 260}}>
                    {conversations.map((c) => (
                        <button
                            key={c.id}
                            onClick={async () => {
                                setSelectedConvId(c.id);
                                await loadMessages(c.id);
                            }}
                            style={{
                                display: "block",
                                width: "100%",
                                textAlign: "left",
                                marginBottom: 8,
                                padding: 8,
                                borderRadius: 6,
                                border: selectedConvId === c.id ? "2px solid #333" : "1px solid #ddd",
                            }}
                        >
                            #{c.id} ext_ref={c.external_ref}
                        </button>
                    ))}
                </div>

                <div style={{flex: 1}}>
                    <h4>Messages {selectedConvId ? `(conversation ${selectedConvId})` : ""}</h4>
                    <pre style={{background: "#f6f6f6", color: "#111", padding: 12, borderRadius: 8, minHeight: 160}}>
            {JSON.stringify(messages, null, 2)}
          </pre>

                    <div style={{display: "flex", gap: 8}}>
                        <input
                            style={{flex: 1}}
                            placeholder="Type message..."
                            value={msgText}
                            onChange={(e) => setMsgText(e.target.value)}
                        />
                        <button onClick={sendMessage} disabled={!selectedConvId}>
                            Send
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
}