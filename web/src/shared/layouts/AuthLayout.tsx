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
      <div className={styles.header}>
        <h1>Welcome to Trading Platform!</h1>
        <p>{title === "Sign In" ? "Please log in to continue" : "Please sign up to continue"}</p>
      </div>
      <div className={`card ${styles.card}`}>
        <h2>{title}</h2>
        {children}
      </div>
    </div>
  );
}
