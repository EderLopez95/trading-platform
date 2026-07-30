import { Controller, useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import {
  configurationSchema,
  type ConfigurationFormData,
} from "../services/configurationSchema";
import { type Configuration } from "../types/configuration.types";
import { useFormOptions } from "../hooks/useFormOptions";
import MultiSelect from "./MultiSelect";
import Select from "@/shared/components/ui/Select/Select";
import Button from "@/shared/components/ui/Button/Button";
import styles from "./ConfigurationForm.module.scss";

type Props = {
  initialValue?: Configuration;
  onSubmit: (data: ConfigurationFormData) => Promise<void>;
};

export default function ConfigurationForm({
  initialValue,
  onSubmit,
}: Props) {
  const { symbols, strategies, timeframes, isLoading } = useFormOptions(true);

  const {
    control,
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<ConfigurationFormData>({
    resolver: zodResolver(configurationSchema),
    defaultValues: {
      symbols: initialValue?.symbols ?? [],
      strategies: initialValue?.strategies ?? [],
      trend_timeframe: initialValue?.trend_timeframe ?? "",
      context_timeframe: initialValue?.context_timeframe ?? "",
      entry_timeframe: initialValue?.entry_timeframe ?? "",
    },
  });

  const symbolOptions = symbols.map((symbol) => ({
    value: symbol,
    label: symbol,
  }));

  const strategyOptions = strategies.map((strategy) => ({
    value: strategy.id,
    label: strategy.name,
  }));

  if (isLoading) {
    return <p className={styles.loading}>Loading options...</p>;
  }

  return (
    <form
      className={styles.form}
      onSubmit={handleSubmit(onSubmit)}
    >
      <div className={styles.field}>
        <label>Symbols</label>
        <Controller
          control={control}
          name="symbols"
          render={({ field }) => (
            <MultiSelect
              options={symbolOptions}
              selected={field.value}
              onChange={field.onChange}
              searchable
              placeholder="Search symbols..."
            />
          )}
        />
        <p className={styles.error}>{errors.symbols?.message}</p>
      </div>

      <div className={styles.field}>
        <label>Strategies</label>
        <Controller
          control={control}
          name="strategies"
          render={({ field }) => (
            <MultiSelect
              options={strategyOptions}
              selected={field.value}
              onChange={field.onChange}
            />
          )}
        />
        <p className={styles.error}>{errors.strategies?.message}</p>
      </div>

      <div className={styles.field}>
        <label>Trend timeframe</label>
        <Select {...register("trend_timeframe")}>
          <option value="">Select timeframe</option>
          {timeframes.map((timeframe) => (
            <option key={timeframe} value={timeframe}>
              {timeframe}
            </option>
          ))}
        </Select>
        <p className={styles.error}>{errors.trend_timeframe?.message}</p>
      </div>

      <div className={styles.field}>
        <label>Context timeframe (optional)</label>
        <Select {...register("context_timeframe")}>
          <option value="">Select timeframe</option>
          {timeframes.map((timeframe) => (
            <option key={timeframe} value={timeframe}>
              {timeframe}
            </option>
          ))}
        </Select>
        <p className={styles.error}>{errors.context_timeframe?.message}</p>
      </div>

      <div className={styles.field}>
        <label>Entry timeframe</label>
        <Select {...register("entry_timeframe")}>
          <option value="">Select timeframe</option>
          {timeframes.map((timeframe) => (
            <option key={timeframe} value={timeframe}>
              {timeframe}
            </option>
          ))}
        </Select>
        <p className={styles.error}>{errors.entry_timeframe?.message}</p>
      </div>

      <Button type="submit" disabled={isSubmitting}>
        {isSubmitting
          ? "Saving..."
          : initialValue
            ? "Update configuration"
            : "Create configuration"}
      </Button>
    </form>
  );
}
