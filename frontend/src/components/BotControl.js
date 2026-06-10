import { startBot, stopBot } from "../services/api";
import "./BotControl.scss";
import { useContext } from "react";
import { AppContext } from "../App";
import { BotStatus } from "../enums";

function BotControl({ status }) {
  const { showToast, setStatus, setSignals, setLogs, setSelectedConfig } = useContext(AppContext);
  const isRunning = status === BotStatus.RUNNING;

  const handleToggle = async () => {
    if (isRunning) {
      try {
        const response = await stopBot();

        if (response.status === BotStatus.STOPPED) {
          setStatus(BotStatus.STOPPED);
          showToast("info", "Bot stopped");
        }
      } catch (err) {
        console.error("Error stopping bot:", err);
        showToast("error", "Error stopping bot");
      }
    }
    else {
      try {
        const response = await startBot();
        
        if (response.status === BotStatus.RUNNING) {
          setStatus(BotStatus.RUNNING);
          showToast("info", "Bot running");
        }
      } catch (err) {
        console.error("Error starting bot:", err);
        showToast("error", "Error starting bot");
      }
    }
  };

  const handleClear = async () => {
    try {
      localStorage.removeItem("signals");
      localStorage.removeItem("logs");
      setSignals([]);
      setLogs([]);
      setSelectedConfig(null);
      showToast("info", "Configuration form and logs cleared");
    } catch (err) {
      console.error("Error resetting:", err);
      showToast("error", "Error resetting");
    }
  };

  return (
    <div className="bot-controls">
      <label className="switch">
        <input
          type="checkbox"
          checked={isRunning}
          onChange={handleToggle}
        />
        <span className="slider">
          <span className="text-status">{isRunning ? "ON" : "OFF"}</span>
        </span>
      </label>
      <button className="btn-reset" onClick={handleClear}>
        Clear
      </button>
    </div>
  );
}

export default BotControl;
