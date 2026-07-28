import toast from "react-hot-toast";
import {
  useAnalysisStatus,
  useToggleAnalysis,
} from "../hooks/useAnalysis";
import styles from "./AnalysisSwitch.module.scss";

export default function AnalysisSwitch() {
  const { data, isLoading } = useAnalysisStatus();
  const toggle = useToggleAnalysis();

  const enabled = data?.enabled ?? false;

  const handleToggle = () => {
    toggle.mutate(!enabled, {
      onError: () => {
        toast.error("Failed to update analysis");
      },
    });
  };

  return (
    <button
      type="button"
      className={
        enabled
          ? `${styles.switch} ${styles.on}`
          : `${styles.switch} ${styles.off}`
      }
      role="switch"
      aria-checked={enabled}
      disabled={isLoading || toggle.isPending}
      onClick={handleToggle}
    >
      <span className={styles.label}>{enabled ? "ON" : "OFF"}</span>
      <span className={styles.track}>
        <span className={styles.thumb} />
      </span>
    </button>
  );
}
