import {useState} from "react";
import {createAppointment, getAppointments, getDoctors, getMe, login} from "./api";

export default function App() {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [access, setAccess] = useState(localStorage.getItem("access") || "");
    const [me, setMe] = useState(null);
    const [error, setError] = useState("");

    const [doctors, setDoctors] = useState([]);
    const [appointments, setAppointments] = useState([]);

    const [selectedDoctorId, setSelectedDoctorId] = useState("");
    const [startsAt, setStartsAt] = useState(""); // example: 2026-01-31T18:30:00Z

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

    async function handleLoadDoctors() {
        setError("");
        try {
            const data = await getDoctors(access);
            setDoctors(data);
        } catch (err) {
            setError(err.message);
        }
    }

    async function handleLoadAppointments() {
        setError("");
        try {
            const data = await getAppointments(access);
            setAppointments(data);
        } catch (err) {
            setError(err.message);
        }
    }

    async function handleCreateAppointment(e) {
        e.preventDefault();
        setError("");

        try {
            await createAppointment(access, selectedDoctorId, startsAt);
            await handleLoadAppointments();
        } catch (err) {
            setError(err.message);
        }
    }

    return (<div className="container py-4" style={{maxWidth: 720}}>
            <h1 className="mb-3">Clinic Frontend</h1>

            <form onSubmit={handleLogin} className="card card-body mb-3">
                <h5 className="mb-3">Login</h5>

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

            <div className="card card-body mb-3">
                <div className="d-flex flex-wrap gap-2 align-items-center mb-2">
                    <button className="btn btn-outline-secondary" onClick={handleGetMe} disabled={!access}>
                        Get /api/me/
                    </button>
                    <button className="btn btn-outline-secondary" onClick={handleLoadDoctors} disabled={!access}>
                        Load doctors
                    </button>
                    <button className="btn btn-outline-secondary" onClick={handleLoadAppointments} disabled={!access}>
                        Load appointments
                    </button>
                    <small className="text-muted">{access ? "token saved" : "no token"}</small>
                </div>

                {error && <div className="alert alert-danger mb-2">{error}</div>}
                {me && <pre className="mb-0">{JSON.stringify(me, null, 2)}</pre>}
            </div>

            <div className="card card-body mb-3">
                <h5 className="mb-3">Create appointment</h5>

                <form onSubmit={handleCreateAppointment} className="row g-2 align-items-end">
                    <div className="col-md-6">
                        <label className="form-label">Doctor</label>
                        <select
                            className="form-select"
                            value={selectedDoctorId}
                            onChange={(e) => setSelectedDoctorId(e.target.value)}
                        >
                            <option value="">-- select doctor --</option>
                            {doctors.map((d) => (<option key={d.id} value={d.id}>
                                    {d.username} (id: {d.id})
                                </option>))}
                        </select>

                        <pre className="mt-2 mb-0">{JSON.stringify(doctors, null, 2)}</pre>
                    </div>

                    <div className="col-md-6">
                        <label className="form-label">Starts at (ISO datetime)</label>
                        <input
                            className="form-control"
                            value={startsAt}
                            onChange={(e) => setStartsAt(e.target.value)}
                            placeholder="2026-01-31T18:30:00Z"
                        />
                    </div>

                    <div className="col-12">
                        <button className="btn btn-success" type="submit"
                                disabled={!access || !selectedDoctorId || !startsAt}>
                            Create
                        </button>
                    </div>
                </form>
            </div>

            <div className="card card-body">
                <h5 className="mb-3">My appointments</h5>

                {appointments.length === 0 ? (<div className="text-muted">No appointments yet.</div>) : (
                    <div className="table-responsive">
                        <table className="table table-sm">
                            <thead>
                            <tr>
                                <th>ID</th>
                                <th>Doctor</th>
                                <th>Starts</th>
                                <th>Status</th>
                            </tr>
                            </thead>
                            <tbody>
                            {appointments.map((a) => (<tr key={a.id}>
                                    <td>{a.id}</td>
                                    <td>{a.doctor_username} (id: {a.doctor})</td>
                                    <td>{a.starts_at}</td>
                                    <td>{a.status}</td>
                                </tr>))}
                            </tbody>
                        </table>
                    </div>)}
            </div>
        </div>);
}