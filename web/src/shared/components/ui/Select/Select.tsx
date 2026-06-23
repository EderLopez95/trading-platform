import { type SelectHTMLAttributes } from "react";
import styles from "./Select.module.scss";

type Props = SelectHTMLAttributes<HTMLSelectElement>;

export default function Select(props: Props) {
  
  return (
    <select
      className={styles.select}
      {...props}
    />
  );
}
