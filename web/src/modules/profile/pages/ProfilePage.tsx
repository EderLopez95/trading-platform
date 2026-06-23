import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import toast from "react-hot-toast";
import DashboardLayout from "@/shared/layouts/DashboardLayout";
import Loader from "@/shared/components/ui/Loader/Loader";
import ProfileForm from "../components/ProfileForm";
import { profileApi } from "../api/profileApi";
import { type ProfileFormData } from "../services/profileSchema";

export default function ProfilePage() {
  const queryClient = useQueryClient();

  const { data, isLoading } = useQuery({
    queryKey: ["profile"],
    queryFn: profileApi.getProfile,
  });

  const updateProfileMutation = useMutation({
    mutationFn: profileApi.updateProfile,

    onSuccess: () => {
      toast.success("Profile updated successfully");
      queryClient.invalidateQueries({
        queryKey: ["profile"],
      });
    },

    onError: () => {
      toast.error("Error updating profile");
    },
  });

  const handleSubmit = async (
    formData: ProfileFormData
  ) => {
    await updateProfileMutation.mutateAsync(formData);
  };

  if (isLoading) {
    return (
      <DashboardLayout>
        <Loader />
      </DashboardLayout>
    );
  }

  if (!data) {
    return (
      <DashboardLayout>
        <p>Unable to load profile</p>
      </DashboardLayout>
    );
  }

  return (
    <DashboardLayout>
      <h2>Profile</h2>
      <ProfileForm
        email={data.email}
        defaultValues={{
          telegram_token: data.telegram_token ?? "",
          telegram_chat_id: data.telegram_chat_id ?? "",
        }}
        onSubmit={handleSubmit}
      />
    </DashboardLayout>
  );
}
