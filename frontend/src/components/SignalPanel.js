import "./SignalPanel.scss";
import { SignalType, StrategyType } from "../enums";

function SignalPanel({ signals }) {
    return (
        <div className="container-table-wrapper">
            <div className="container-table">
                <table className="signals-table">
                    <thead>
                        <tr>
                            <th>Symbol</th>
                            <th>Signal</th>
                            <th>Temp</th>
                            <th>Price</th>
                            <th>Strategy</th>
                            <th>Time</th>
                        </tr>
                    </thead>
                    <tbody>
                        {signals.length === 0 ? (
                            <tr className="no-data">
                                <td colSpan={6}>No signals to display</td>
                            </tr>
                        ) : (
                            signals.map((signal, i) => (
                                <tr key={i}>
                                    <td>{signal.symbol}</td>
                                    <td className={`${signal.signal === SignalType.BUY ? "buy" : signal.signal === SignalType.SELL ? "sell" : "hold"}`}>
                                        {signal.signal}
                                    </td>
                                    <td>{signal.temporality}</td>
                                    <td>{signal.price}</td>
                                    <td>
                                        {signal.strategy === StrategyType.MULTI_SMA ? StrategyType.MULTI_SMA_value
                                        : signal.strategy === StrategyType.RSI_CROSS_TREND ? StrategyType.RSI_CROSS_TREND_value
                                        : "Unknown"}
                                    </td>
                                    <td>
                                        {(() => {
                                            const date = new Date(signal.timestamp);
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
                                </tr>
                            ))
                        )}
                    </tbody>
                </table>
            </div>
        </div>
    );
}

export default SignalPanel;
