import toast from "react-hot-toast";
import { type Configuration } from "../types/configuration.types";
import {
  useDeleteConfiguration,
  useToggleConfiguration,
} from "../hooks/useConfigurations";
import styles from "./ConfigurationCard.module.scss";

type Props = {
  configuration: Configuration;
  onEdit: (configuration: Configuration) => void;
};

function getTimeframesArray(configuration: Configuration): string[] {
  
  return [
    configuration.context_timeframe,
    configuration.trend_timeframe,
    configuration.entry_timeframe,
  ].filter((val): val is string => 
    val !== null && val !== undefined && val.trim() !== "" && val !== "string"
  );
}

export default function ConfigurationCard({
  configuration,
  onEdit,
}: Props) {
  const remove = useDeleteConfiguration();
  const toggle = useToggleConfiguration();

  const handleDelete = () => {
    remove.mutate(configuration.id, {
      onError: () => toast.error("Failed to delete configuration"),
    });
  };

  const handleToggle = () => {
    toggle.mutate(
      { id: configuration.id, enabled: !configuration.enabled },
      { onError: () => toast.error("Failed to update configuration") }
    );
  };

  const timeframes = getTimeframesArray(configuration);

  return (
    <div className={styles.card}>
      <button
        type="button"
        className={styles.remove}
        aria-label="Delete configuration"
        disabled={remove.isPending}
        onClick={handleDelete}
      >
        <svg
          width="16"
          height="16"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
        >
          <line x1="6" y1="6" x2="18" y2="18" />
          <line x1="18" y1="6" x2="6" y2="18" />
        </svg>
      </button>

      <div className={styles.row}>
        <span className={styles.label}>Symbols</span>
        <div className={styles.tagScrollBox}>
          <div className={styles.tagGrid}>
            {configuration.symbols.map((symbol) => (
              <span key={symbol} className={styles.badge}>
                {symbol}
              </span>
            ))}
          </div>
        </div>
      </div>

      <div className={styles.splitRow}>
        <div className={styles.column}>
          <span className={styles.label}>Strategies</span>
          <div className={styles.tagGrid}>
            {configuration.strategies.map((strategy) => (
              <span key={strategy} className={styles.strategyText}>
                {strategy}
              </span>
            ))}
          </div>
        </div>
        <div className={styles.column}>
          <span className={styles.label}>Timeframes</span>
          <div className={styles.tagGrid}>
            {timeframes.map((tf) => (
              <span key={tf} className={styles.badge}>
                {tf}
              </span>
            ))}
          </div>
        </div>
      </div>

      <div className={styles.footer}>
        <button
          type="button"
          className={styles.editButton}
          onClick={() => onEdit(configuration)}
        >
          Edit
        </button>
        <button
          type="button"
          className={
            configuration.enabled
              ? `${styles.switch} ${styles.switchOn}`
              : styles.switch
          }
          role="switch"
          aria-checked={configuration.enabled}
          aria-label={configuration.enabled ? "Disable" : "Enable"}
          disabled={toggle.isPending}
          onClick={handleToggle}
        >
          <span className={styles.thumb} />
        </button>
      </div>
    </div>
  );
}
