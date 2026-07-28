import { useState } from "react";
import toast from "react-hot-toast";
import AnalysisSwitch from "./AnalysisSwitch";
import ConfigurationCard from "./ConfigurationCard";
import ConfigurationForm from "./ConfigurationForm";
import Modal from "@/shared/components/ui/Modal/Modal";
import {
  useConfigurations,
  useCreateConfiguration,
  useDeleteConfiguration,
  useToggleConfiguration,
} from "../hooks/useConfigurations";
import { type Configuration } from "../types/configuration.types";
import { type ConfigurationFormData } from "../services/configurationSchema";
import styles from "./ConfigurationsPanel.module.scss";

export default function ConfigurationsPanel() {
  const { data: configurations = [], isLoading } = useConfigurations();
  const createConfiguration = useCreateConfiguration();
  const toggleConfiguration = useToggleConfiguration();
  const deleteConfiguration = useDeleteConfiguration();

  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editing, setEditing] = useState<Configuration | null>(null);

  const openCreate = () => {
    setEditing(null);
    setIsModalOpen(true);
  };

  const openEdit = (configuration: Configuration) => {
    setEditing(configuration);
    setIsModalOpen(true);
  };

  const closeModal = () => {
    setIsModalOpen(false);
    setEditing(null);
  };

  const handleSubmit = async (data: ConfigurationFormData) => {
    const payload = {
      symbols: data.symbols,
      strategies: data.strategies,
      trend_timeframe: data.trend_timeframe,
      context_timeframe: data.context_timeframe || null,
      entry_timeframe: data.entry_timeframe,
    };

    try {
      if (editing) {
        const created = await createConfiguration.mutateAsync(payload);

        if (created.enabled !== editing.enabled) {
          await toggleConfiguration.mutateAsync({
            id: created.id,
            enabled: editing.enabled,
          });
        }

        await deleteConfiguration.mutateAsync(editing.id);
        toast.success("Configuration updated");
      } else {
        await createConfiguration.mutateAsync(payload);
        toast.success("Configuration created");
      }

      closeModal();
    } catch {
      toast.error("Failed to save configuration");
    }
  };

  return (
    <div className={styles.panel}>
      <div className={styles.actions}>
        <AnalysisSwitch />
        <button
          type="button"
          className={styles.countButton}
          onClick={openCreate}
        >
          {configurations.length} Configurations
        </button>
      </div>

      <div className={styles.list}>
        {isLoading && (
          <p className={styles.state}>Loading configurations...</p>
        )}

        {!isLoading && configurations.length === 0 && (
          <p className={styles.state}>No configurations yet</p>
        )}

        {configurations.map((configuration) => (
          <ConfigurationCard
            key={configuration.id}
            configuration={configuration}
            onEdit={openEdit}
          />
        ))}
      </div>

      <Modal
        isOpen={isModalOpen}
        onClose={closeModal}
        title={editing ? "Edit configuration" : "New configuration"}
      >
        <ConfigurationForm
          key={editing?.id ?? "new"}
          initialValue={editing ?? undefined}
          onSubmit={handleSubmit}
        />
      </Modal>
    </div>
  );
}
