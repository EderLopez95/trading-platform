import toast from "react-hot-toast";
import TelegramForm from "../components/TelegramForm";
import {
  useTelegramSettings,
  useUpdateTelegramSettings,
} from "../hooks/useTelegramSettings";
import { type TelegramFormData } from "../services/telegramSchema";
import styles from "./SettingsPage.module.scss";

export default function SettingsPage() {
  const { data, isLoading } = useTelegramSettings();
  const updateTelegram = useUpdateTelegramSettings();

  const handleSubmit = async (formData: TelegramFormData) => {
    try {
      await updateTelegram.mutateAsync(formData);
      toast.success("Telegram settings updated");
    } catch (error) {
      console.error(error);
      toast.error("Failed to update telegram settings");
    }
  };

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <h1>Settings</h1>
      </div>
      <div className={`card ${styles.card}`}>
        <h2>Notifications</h2>
        <p className={styles.description}>
          Configure your Telegram bot to receive alerts
        </p>
        {isLoading ? (
          <p className={styles.description}>Loading...</p>
        ) : (
          <TelegramForm initialValue={data} onSubmit={handleSubmit} />
        )}
      </div>
    </div>
  );
}
