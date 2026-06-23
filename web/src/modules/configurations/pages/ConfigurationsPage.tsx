import { useQuery } from "@tanstack/react-query";
import DashboardLayout from "@/shared/layouts/DashboardLayout";
import Loader from "@/shared/components/ui/Loader/Loader";
import { configurationApi } from "../api/configurationApi";
import ConfigurationCard from "../components/ConfigurationCard";
import { Link } from "react-router-dom";

export default function ConfigurationsPage() {
  const {
    data,
    isLoading,
  } = useQuery({
    queryKey: ["configurations"],
    queryFn: configurationApi.getAll,
  });

  if (isLoading) {
    return (
      <DashboardLayout>
        <Loader />
      </DashboardLayout>
    );
  }

  return (
    <DashboardLayout>
      <h2>Configurations</h2>
      <Link to="/configurations/new">
        Create Configuration
      </Link>
      {data?.map((configuration: any) => (
        <ConfigurationCard
          key={configuration.id}
          configuration={configuration}
        />
      ))}
    </DashboardLayout>
  );
}
