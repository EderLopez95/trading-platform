import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import {
  telegramSchema,
  type TelegramFormData,
} from "../services/telegramSchema";
import styles from "./TelegramForm.module.scss";
import Input from "@/shared/components/ui/Input/Input";
import Button from "@/shared/components/ui/Button/Button";

type Props = {
  onSubmit: (data: TelegramFormData) => Promise<void>;
};

export default function TelegramForm({
  onSubmit,
}: Props) {
  const {
    register,
    handleSubmit,
    formState: {
      errors,
      isSubmitting,
    },
  } = useForm<TelegramFormData>({
    resolver: zodResolver(telegramSchema),
  });

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <div className={styles.field}>
        <label>Telegram Token</label>
        <Input
          type="text"
          autoComplete="off"
          placeholder="123456789:ABC-DEF..."
          {...register("telegram_token")}
        />
        <p className={styles.error}>
          {errors.telegram_token?.message}
        </p>
      </div>
      <div className={styles.field}>
        <label>Telegram Chat ID</label>
        <Input
          type="text"
          autoComplete="off"
          placeholder="123456789"
          {...register("telegram_chat_id")}
        />
        <p className={styles.error}>
          {errors.telegram_chat_id?.message}
        </p>
      </div>
      <Button
        type="submit"
        disabled={isSubmitting}
      >
        {isSubmitting ? "Saving..." : "Save"}
      </Button>
    </form>
  );
}
