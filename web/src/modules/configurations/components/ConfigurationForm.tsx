import { useForm } from "react-hook-form";
import {
  type ConfigurationFormData,
  configurationSchema,
} from "../services/configurationSchema";
import { zodResolver } from "@hookform/resolvers/zod";
import Input from "@/shared/components/ui/Input/Input";
import Button from "@/shared/components/ui/Button/Button";
import Select from "@/shared/components/ui/Select/Select";
import { TIMEFRAMES } from "@/shared/constants/timeframes";

type Props = {
  onSubmit: (
    data: ConfigurationFormData
  ) => Promise<void>;
};

export default function ConfigurationForm({
  onSubmit,
}: Props) {
  const {
    register,
    handleSubmit,
    formState: {
      isSubmitting,
    },
  } = useForm<ConfigurationFormData>({
    resolver:
      zodResolver(configurationSchema),
  });

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <h3>Create Configuration</h3>
      <Input
        placeholder="BTCUSDT,ETHUSDT"
        {...register("symbols")}
      />
      <Input
        placeholder="EMA_CROSS"
        {...register("strategies")}
      />
      <Select
        {...register("trend_timeframe")}
      >
        {TIMEFRAMES.map((tf) => (
          <option
            key={tf}
            value={tf}
          >
            {tf}
          </option>
        ))}
      </Select>
      <Select
        {...register("entry_timeframe")}
      >
        {TIMEFRAMES.map((tf) => (
          <option
            key={tf}
            value={tf}
          >
            {tf}
          </option>
        ))}
      </Select>
      <Button
        type="submit"
        disabled={isSubmitting}
      >
        {isSubmitting ? "Creating..." : "Create"}
      </Button>
    </form>
  );
}
