import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import {
  profileSchema,
  type ProfileFormData,
} from "../services/profileSchema";
import Input from "@/shared/components/ui/Input/Input";
import Button from "@/shared/components/ui/Button/Button";

type Props = {
  email: string;
  defaultValues: {
    telegram_token: string;
    telegram_chat_id: string;
  };
  onSubmit: (data: ProfileFormData) => Promise<void>;
};

export default function ProfileForm({
  email,
  defaultValues,
  onSubmit,
}: Props) {
  const {
    register,
    handleSubmit,
    formState: {
      isSubmitting,
    },
  } = useForm<ProfileFormData>({
    resolver: zodResolver(profileSchema),
    values: defaultValues,
  });

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <p>Email</p>
      <Input
        value={email}
        disabled
      />
      <p>Telegram Token</p>
      <Input
        {...register(
          "telegram_token"
        )}
      />
      <p>Telegram Chat Id</p>
      <Input
        {...register(
          "telegram_chat_id"
        )}
      />
      <Button
        type="submit"
        disabled={isSubmitting}
      >
        {isSubmitting ? "Saving..." : "Save"}
      </Button>
    </form>
  );
}
