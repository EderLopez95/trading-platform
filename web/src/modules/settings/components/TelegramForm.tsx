import { useState } from "react";
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
  initialValue?: TelegramFormData;
  onSubmit: (data: TelegramFormData) => Promise<void>;
};

const EMPTY_VALUES: TelegramFormData = {
  telegram_token: "",
  telegram_chat_id: "",
};

function EyeIcon({ visible }: { visible: boolean }) {
  if (visible) {
    return (
      <svg
        width="18"
        height="18"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        strokeWidth="2"
        strokeLinecap="round"
        strokeLinejoin="round"
      >
        <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24" />
        <line x1="1" y1="1" x2="23" y2="23" />
      </svg>
    );
  }

  return (
    <svg
      width="18"
      height="18"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <path d="M1 12s4-7 11-7 11 7 11 7-4 7-11 7-11-7-11-7z" />
      <circle cx="12" cy="12" r="3" />
    </svg>
  );
}

export default function TelegramForm({
  initialValue,
  onSubmit,
}: Props) {
  const [showToken, setShowToken] = useState(false);
  const [showChatId, setShowChatId] = useState(false);

  const {
    register,
    handleSubmit,
    reset,
    formState: {
      errors,
      isSubmitting,
      isDirty,
    },
  } = useForm<TelegramFormData>({
    resolver: zodResolver(telegramSchema),
    values: initialValue ?? EMPTY_VALUES,
  });

  const submit = handleSubmit(async (data) => {
    if (!isDirty) {
      return;
    }

    await onSubmit(data);
    reset(data);
  });

  return (
    <form onSubmit={submit}>
      <div className={styles.field}>
        <label>Telegram Token</label>
        <div className={styles.inputWrapper}>
          <Input
            type={showToken ? "text" : "password"}
            autoComplete="off"
            placeholder="123456789:ABC-DEF..."
            {...register("telegram_token")}
          />
          <button
            type="button"
            className={styles.toggle}
            aria-label={showToken ? "Hide token" : "Show token"}
            aria-pressed={showToken}
            onClick={() => setShowToken((value) => !value)}
          >
            <EyeIcon visible={showToken} />
          </button>
        </div>
        <p className={styles.error}>
          {errors.telegram_token?.message}
        </p>
      </div>
      <div className={styles.field}>
        <label>Telegram Chat ID</label>
        <div className={styles.inputWrapper}>
          <Input
            type={showChatId ? "text" : "password"}
            autoComplete="off"
            placeholder="123456789"
            {...register("telegram_chat_id")}
          />
          <button
            type="button"
            className={styles.toggle}
            aria-label={showChatId ? "Hide chat ID" : "Show chat ID"}
            aria-pressed={showChatId}
            onClick={() => setShowChatId((value) => !value)}
          >
            <EyeIcon visible={showChatId} />
          </button>
        </div>
        <p className={styles.error}>
          {errors.telegram_chat_id?.message}
        </p>
      </div>
      <Button
        type="submit"
        disabled={isSubmitting || !isDirty}
      >
        {isSubmitting ? "Saving..." : "Save"}
      </Button>
    </form>
  );
}
