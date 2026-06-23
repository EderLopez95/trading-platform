import { type ReactNode } from "react";
import Navbar from "@/shared/components/Navbar";
import Sidebar from "@/modules/dashboard/components/Sidebar";
import styles from "./DashboardLayout.module.scss";

type Props = {
  children: ReactNode;
};

export default function DashboardLayout({
  children,
}: Props) {
  return (
    <>
      <Navbar />
      <div className={styles.container}>
        <Sidebar />
        <main className={styles.main}>
          {children}
        </main>
      </div>
    </>
  );
}
