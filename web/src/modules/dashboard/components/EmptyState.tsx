type Props = {
  title: string;
  description: string;
};

export default function EmptyState({
  title,
  description,
}: Props) {
  return (
    <div>
      <span>{title}</span>
      <p>{description}</p>
    </div>
  );
}
