import { Outlet } from "react-router-dom";
import Header from "@/shared/components/Header/Header";
import styles from "./MainLayout.module.scss";

export default function MainLayout() {

  return (
    <div className={styles.layout}>
      <Header />
      <main className={styles.content}>
        <Outlet />
      </main>
    </div>
  );
}
