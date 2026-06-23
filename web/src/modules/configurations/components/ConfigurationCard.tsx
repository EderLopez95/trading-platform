import Card from "@/shared/components/ui/Card/Card";
import { type Configuration } from "../types/configuration.types";

type Props = {
  configuration: Configuration;
};

export default function ConfigurationCard({
  configuration,
}: Props) {
  return (
    <Card>
      <h3>
        {configuration.symbols.join(", ")}
      </h3>
      <p>
        Strategies:
        {" "}
        {configuration.strategies.join(", ")}
      </p>
      <p>
        Trend:
        {" "}
        {configuration.trend_timeframe}
      </p>
      <p>
        Entry:
        {" "}
        {configuration.entry_timeframe}
      </p>
      <p>
        Status:
        {" "}
        {configuration.enabled
          ? "Enabled"
          : "Disabled"}
      </p>
    </Card>
  );
}
