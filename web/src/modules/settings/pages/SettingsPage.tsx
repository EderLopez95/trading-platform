import toast from "react-hot-toast";
import TelegramForm from "../components/TelegramForm";
import { settingsApi } from "../api/settingsApi";
import { type TelegramFormData } from "../services/telegramSchema";
import styles from "./SettingsPage.module.scss";

export default function SettingsPage() {

  const handleSubmit = async (
    data: TelegramFormData
  ) => {
    try {
      await settingsApi.updateTelegram(data);
      toast.success("Telegram settings updated");
    } catch (error) {
      console.error(error);
      toast.error("Failed to update settings");
    }
  };

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <h1>Settings</h1>
      </div>
      <div className={`card ${styles.card}`}>
        <h2>Notifications</h2>
        <p className={styles.description}>Configure your Telegram bot to receive signal alerts</p>
        <TelegramForm onSubmit={handleSubmit} />
      </div>
    </div>
  );
}
