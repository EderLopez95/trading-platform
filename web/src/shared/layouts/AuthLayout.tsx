import { type ReactNode } from "react";
import styles from "./AuthLayout.module.scss";

type Props = {
  title: string;
  children: ReactNode;
};

export default function AuthLayout({
  title,
  children,
}: Props) {
  return (
    <div className={styles.container}>
      <div className={`card ${styles.card}`}>
        <h1>{title}</h1>
        {children}
      </div>
    </div>
  );
}
