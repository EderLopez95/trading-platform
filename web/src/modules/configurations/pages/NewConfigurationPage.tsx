import {
  useMutation,
  useQueryClient,
} from "@tanstack/react-query";
import toast from "react-hot-toast";
import DashboardLayout from "@/shared/layouts/DashboardLayout";
import ConfigurationForm from "../components/ConfigurationForm";
import { configurationApi } from "../api/configurationApi";

export default function NewConfigurationPage() {
  const queryClient = useQueryClient();

  const mutation = useMutation({
    mutationFn: configurationApi.create,

    onSuccess: () => {
      toast.success("Configuration created");
      queryClient.invalidateQueries({
        queryKey: [
          "configurations",
        ],
      });
    },
  });

  return (
    <DashboardLayout>
      <ConfigurationForm
        onSubmit={(data) =>
          mutation.mutateAsync(data)
        }
      />
    </DashboardLayout>
  );
}
