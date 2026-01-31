import {useState} from "react";
import {getMe, login} from "./api";

export default function App() {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [access, setAccess] = useState(localStorage.getItem("access") || "");
    const [me, setMe] = useState(null);
    const [error, setError] = useState("");

    async function handleLogin(e) {
        e.preventDefault();
        setError("");
        try {
            const data = await login(username, password);
            setAccess(data.access);
            localStorage.setItem("access", data.access);
        } catch (err) {
            setError(err.message);
        }
    }

    async function handleGetMe() {
        setError("");
        try {
            const data = await getMe(access);
            setMe(data);
        } catch (err) {
            setError(err.message);
        }
    }

    return (
        <div className="container py-4" style={{maxWidth: 520}}>
            <h1 className="mb-3">Clinic Frontend</h1>

            <form onSubmit={handleLogin} className="card card-body mb-3">
                <div className="mb-2">
                    <label className="form-label">Username</label>
                    <input className="form-control" value={username} onChange={(e) => setUsername(e.target.value)}/>
                </div>

                <div className="mb-3">
                    <label className="form-label">Password</label>
                    <input className="form-control" type="password" value={password}
                           onChange={(e) => setPassword(e.target.value)}/>
                </div>

                <button className="btn btn-primary" type="submit">Login</button>
            </form>

            <div className="card card-body">
                <div className="d-flex gap-2 align-items-center mb-2">
                    <button className="btn btn-outline-secondary" onClick={handleGetMe} disabled={!access}>
                        Get /api/me/
                    </button>
                    <small className="text-muted">{access ? "token saved" : "no token"}</small>
                </div>

                {error && <div className="alert alert-danger mb-2">{error}</div>}
                {me && <pre className="mb-0">{JSON.stringify(me, null, 2)}</pre>}
            </div>
        </div>
    );
}