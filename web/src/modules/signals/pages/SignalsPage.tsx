import SignalsTable from "../components/SignalsTable";
import ConfigurationsPanel from "@/modules/configurations/components/ConfigurationsPanel";
import styles from "./SignalsPage.module.scss";

export default function SignalsPage() {

  return (
    <div className={styles.page}>
      <div className={`card ${styles.configCard}`}>
        <div className={styles.configWrapper}>
          <ConfigurationsPanel />
        </div>
      </div>
      <div className={`card ${styles.signalsCard}`}>
        <SignalsTable />
      </div>
    </div>
  );
}
