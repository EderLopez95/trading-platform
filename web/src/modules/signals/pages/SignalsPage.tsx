import SignalsTable from "../components/SignalsTable";
import styles from "./SignalsPage.module.scss";

export default function SignalsPage() {

  return (
    <div className={styles.page}>
      <div className={`card ${styles.configCard}`}>
        <h3 className={styles.configTitle}>Configurations</h3>
      </div>
      <div className={`card ${styles.signalsCard}`}>
        <SignalsTable />
      </div>
    </div>
  );
}
