import { useMemo, useState } from "react";
import styles from "./MultiSelect.module.scss";

type Option = {
  value: string;
  label: string;
};

type Props = {
  options: Option[];
  selected: string[];
  onChange: (next: string[]) => void;
  searchable?: boolean;
  placeholder?: string;
};

export default function MultiSelect({
  options,
  selected,
  onChange,
  searchable = false,
  placeholder = "Search...",
}: Props) {
  const [query, setQuery] = useState("");

  const filtered = useMemo(() => {
    if (!searchable || !query.trim()) {
      return options;
    }

    const lower = query.trim().toLowerCase();

    return options.filter((option) =>
      option.label.toLowerCase().includes(lower)
    );
  }, [options, query, searchable]);

  const toggle = (value: string) => {
    if (selected.includes(value)) {
      onChange(selected.filter((item) => item !== value));
    } else {
      onChange([...selected, value]);
    }
  };

  return (
    <div className={styles.container}>
      {searchable && (
        <input
          type="text"
          className={styles.search}
          placeholder={placeholder}
          value={query}
          onChange={(event) => setQuery(event.target.value)}
        />
      )}
      <div className={styles.list}>
        {filtered.length === 0 && (
          <p className={styles.empty}>No options</p>
        )}
        {filtered.map((option) => (
          <label key={option.value} className={styles.item}>
            <input
              type="checkbox"
              className={styles.checkbox}
              checked={selected.includes(option.value)}
              onChange={() => toggle(option.value)}
            />
            <span>{option.label}</span>
          </label>
        ))}
      </div>
    </div>
  );
}
