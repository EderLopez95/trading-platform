import { useMemo, useRef } from "react";
import AsyncSelect from "react-select/async";
import type { MultiValue, StylesConfig } from "react-select";
import { optionsApi } from "../api/optionsApi";

type Option = {
  value: string;
  label: string;
};

type Props = {
  value: string[];
  onChange: (next: string[]) => void;
  placeholder?: string;
};

const MIN_QUERY_LENGTH = 1;
const DEBOUNCE_MS = 300;

// Theme tokens mirrored from styles/_variables.scss
const colors = {
  background: "#1E222D",
  card: "#262B3B",
  border: "#363C4E",
  borderHover: "#137CBD",
  textPrimary: "#E4E7EC",
  textSecondary: "#787B86",
  primary: "#0284C7",
  danger: "#CF6679",
};

const selectStyles: StylesConfig<Option, true> = {
  control: (base, state) => ({
    ...base,
    backgroundColor: colors.background,
    borderColor: state.isFocused ? colors.borderHover : colors.border,
    borderRadius: 8,
    boxShadow: "none",
    minHeight: 40,
    "&:hover": {
      borderColor: colors.borderHover,
    },
  }),
  valueContainer: (base) => ({
    ...base,
    padding: "4px 8px",
    gap: 4,
  }),
  input: (base) => ({
    ...base,
    color: colors.textPrimary,
    margin: 0,
    padding: 0,
  }),
  placeholder: (base) => ({
    ...base,
    color: colors.textSecondary,
  }),
  menu: (base) => ({
    ...base,
    backgroundColor: colors.card,
    border: `1px solid ${colors.border}`,
    borderRadius: 8,
    overflow: "hidden",
    zIndex: 20,
  }),
  menuPortal: (base) => ({
    ...base,
    zIndex: 9999,
  }),
  option: (base, state) => ({
    ...base,
    backgroundColor: state.isFocused ? colors.background : colors.card,
    color: colors.textPrimary,
    cursor: "pointer",
    "&:active": {
      backgroundColor: colors.primary,
    },
  }),
  noOptionsMessage: (base) => ({
    ...base,
    color: colors.textSecondary,
  }),
  loadingMessage: (base) => ({
    ...base,
    color: colors.textSecondary,
  }),
  multiValue: (base) => ({
    ...base,
    backgroundColor: colors.border,
    borderRadius: 6,
    overflow: "hidden",
  }),
  multiValueLabel: (base) => ({
    ...base,
    color: colors.textPrimary,
    fontSize: 13,
    padding: "2px 6px",
  }),
  multiValueRemove: (base) => ({
    ...base,
    color: colors.textSecondary,
    width: 0,
    paddingLeft: 0,
    paddingRight: 0,
    opacity: 0,
    overflow: "hidden",
    transition: "opacity 120ms ease, width 120ms ease",
    ".symbol-select__multi-value:hover &": {
      width: 20,
      paddingLeft: 2,
      paddingRight: 2,
      opacity: 1,
    },
    "&:hover": {
      backgroundColor: colors.danger,
      color: colors.textPrimary,
    },
  }),
  indicatorSeparator: (base) => ({
    ...base,
    backgroundColor: colors.border,
  }),
  dropdownIndicator: (base) => ({
    ...base,
    color: colors.textSecondary,
    "&:hover": {
      color: colors.textPrimary,
    },
  }),
  clearIndicator: (base) => ({
    ...base,
    color: colors.textSecondary,
    "&:hover": {
      color: colors.danger,
    },
  }),
};

function debounceLoad(
  loader: (query: string) => Promise<Option[]>,
  wait: number
) {
  let timer: ReturnType<typeof setTimeout> | undefined;

  return (query: string) =>
    new Promise<Option[]>((resolve) => {
      if (timer) {
        clearTimeout(timer);
      }

      timer = setTimeout(() => {
        loader(query).then(resolve).catch(() => resolve([]));
      }, wait);
    });
}

export default function AsyncSymbolSelect({
  value,
  onChange,
  placeholder = "Search symbols...",
}: Props) {
  const selectedOptions = useMemo<Option[]>(
    () => value.map((symbol) => ({ value: symbol, label: symbol })),
    [value]
  );

  const loadOptions = useRef(
    debounceLoad(async (query: string) => {
      const trimmed = query.trim();

      if (trimmed.length < MIN_QUERY_LENGTH) {
        return [];
      }

      const symbols = await optionsApi.getSymbols(trimmed);

      return symbols.map((symbol) => ({ value: symbol, label: symbol }));
    }, DEBOUNCE_MS)
  ).current;

  const handleChange = (next: MultiValue<Option>) => {
    onChange(next.map((option) => option.value));
  };

  return (
    <AsyncSelect<Option, true>
      isMulti
      classNamePrefix="symbol-select"
      value={selectedOptions}
      onChange={handleChange}
      loadOptions={loadOptions}
      cacheOptions
      defaultOptions={false}
      placeholder={placeholder}
      loadingMessage={() => "Searching..."}
      noOptionsMessage={({ inputValue }) =>
        inputValue.trim().length < MIN_QUERY_LENGTH
          ? "Type to search symbols"
          : "No symbols found"
      }
      menuPortalTarget={
        typeof document !== "undefined" ? document.body : undefined
      }
      styles={selectStyles}
    />
  );
}
