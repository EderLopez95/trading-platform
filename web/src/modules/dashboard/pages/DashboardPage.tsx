import DashboardLayout from "@/shared/layouts/DashboardLayout";
import StatCard from "../components/StatCard";
import EmptyState from "../components/EmptyState";
import styles from "./DashboardPage.module.scss";

export default function DashboardPage() {
  
  return (
    <DashboardLayout>
      <h1>Dashboard</h1>
      <div className={styles.statsContainer}>
        <StatCard
          title="Active Configurations"
          value={0}
        />
        <StatCard
          title="Signals Today"
          value={0}
        />
        <StatCard
          title="Enabled Strategies"
          value={0}
        />
      </div>
      <div className={styles.emptyStateContainer}>
        <EmptyState
          title="No signals yet"
          description="Signals will appear here"
        />
      </div>
    </DashboardLayout>
  );
}
