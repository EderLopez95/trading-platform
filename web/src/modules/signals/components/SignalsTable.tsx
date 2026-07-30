import { useState } from "react";
import { useSignals } from "../hooks/useSignals";
import { type Signal } from "../types/signal.types";
import styles from "./SignalsTable.module.scss";

const PAGE_SIZE = 20;

function formatTimeframes(signal: Signal) {

  return [
    signal.trend_timeframe,
    signal.context_timeframe,
    signal.entry_timeframe,
  ]
    .filter(val => val && val.trim() !== "" && val !== "string")
    .join(" - ");
}

function formatTime(value: string) {
  const date = new Date(value);

  if (Number.isNaN(date.getTime())) {
    return value;
  }

  return date.toLocaleString();
}

export default function SignalsTable() {
  const [page, setPage] = useState(1);

  const { data, isLoading, isError, isFetching } = useSignals({
    page,
    page_size: PAGE_SIZE,
  });

  const signals = data?.signals ?? [];
  const total = data?.total ?? 0;
  const totalPages = Math.max(Math.ceil(total / PAGE_SIZE), 1);

  const canPrev = page > 1;
  const canNext = page < totalPages;

  return (
    <div className={styles.wrapper}>
      <div className={styles.tableScroll}>
        <table className={styles.table}>
          <thead>
            <tr>
              <th>Symbol</th>
              <th>Signal</th>
              <th>Timeframes</th>
              <th>Strategy</th>
              <th>Time</th>
              <th>Price</th>
            </tr>
          </thead>
          <tbody>
            {isLoading && (
              <tr>
                <td colSpan={6} className={styles.state}>
                  Loading...
                </td>
              </tr>
            )}

            {isError && !isLoading && (
              <tr>
                <td colSpan={6} className={styles.state}>
                  Failed to load signals
                </td>
              </tr>
            )}

            {!isLoading && !isError && signals.length === 0 && (
              <tr>
                <td colSpan={6} className={styles.state}>
                  No signals yet
                </td>
              </tr>
            )}

            {!isError &&
              signals.map((signal) => (
                <tr key={signal.id}>
                  <td className={styles.symbol}>{signal.symbol}</td>
                  <td>
                    <span
                      className={
                        signal.signal === "BUY" ? `${styles.badge} ${styles.buy}`
                        : signal.signal === "SELL" ? `${styles.badge} ${styles.sell}` : ""
                      }
                    >
                      {signal.signal}
                    </span>
                  </td>
                  <td>{formatTimeframes(signal)}</td>
                  <td>{signal.strategy}</td>
                  <td className={styles.time}>
                    {formatTime(signal.signal_time)}
                  </td>
                  <td>{signal.price}</td>
                </tr>
              ))}
          </tbody>
        </table>
      </div>

      <div className={styles.pagination}>
        <span className={styles.pageInfo}>
          Page {page} of {totalPages} {isFetching ? " · updating..." : ""}
        </span>
        <div className={styles.pageButtons}>
          <button
            type="button"
            className={styles.pageButton}
            disabled={!canPrev}
            onClick={() => setPage((p) => Math.max(p - 1, 1))}
          >
            Previous
          </button>
          <button
            type="button"
            className={styles.pageButton}
            disabled={!canNext}
            onClick={() => setPage((p) => p + 1)}
          >
            Next
          </button>
        </div>
      </div>
    </div>
  );
}
