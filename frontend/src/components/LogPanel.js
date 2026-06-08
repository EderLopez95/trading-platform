import "./SignalPanel.scss";

function LogPanel({ logs }) {
  return (
    <div className="container-table-wrapper">
        <div className="container-table logs-table">
            <table className="signals-table">
                <thead>
                    <tr>
                        <th>Type</th>
                        <th>Time</th>
                        <th>Message</th>
                    </tr>
                </thead>
                <tbody>
                    {logs.length === 0 ? (
                        <tr className="no-data">
                            <td colSpan={6}>No logs to display</td>
                        </tr>
                    ) : (
                        logs.map((log, i) => (
                            <tr key={i}>
                                <td>{log.level}</td>
                                <td>
                                    {(() => {
                                        const date = new Date(log.timestamp);
                                        const timeStr = date.toLocaleTimeString('en-US', {
                                            hour: 'numeric',
                                            minute: '2-digit',
                                            hour12: true
                                        }).replace(' ', '');
                                        const dateStr = date.toLocaleDateString('es-ES', {
                                            day: '2-digit',
                                            month: '2-digit',
                                            year: '2-digit'
                                        });
                                        return `${timeStr} ${dateStr}`;
                                    })()}
                                </td>
                                <td>{log.message}</td>
                            </tr>
                        ))
                    )}
                </tbody>
            </table>
        </div>
    </div>
  );
}

export default LogPanel;
