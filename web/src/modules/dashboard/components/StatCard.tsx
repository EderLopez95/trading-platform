import styles from "./StatCard.module.scss";

type Props = {
  title: string;
  value: string | number;
};

export default function StatCard({
  title,
  value,
}: Props) {
  return (
    <div className={styles.card}>
      <span>{title}</span>
      <span>{value}</span>
    </div>
  );
}
