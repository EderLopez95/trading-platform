import { useState, useEffect, useContext } from "react";
import { saveConfig, getSymbols } from "../services/api";
import "./ConfigPanel.scss";
import AsyncSelect from "react-select/async";
import { AppContext } from "../App";
import { StrategyType } from "../enums";

function ConfigPanel() {
  const [loading, setLoading] = useState(true);
  const [errors, setErrors] = useState({});
  const { showToast, config, setConfig, selectedConfig, setSelectedConfig } = useContext(AppContext);

  useEffect(() => {
    if (config)
      setLoading(false);
  }, [config]);

  const loadSymbols = async (inputValue) => {
    try {
      const data = await getSymbols(inputValue);
      return data.map((s) => ({
        value: s,
        label: s
      }));
    } catch (error) {
      console.error("Error loading symbols:", error);
      return [];
    }
  };

  const parseSymbols = (symbols) => {
    if (!symbols) return [];
    if (Array.isArray(symbols)) {
      return symbols.map((s) => ({
        value: s,
        label: s
      }));
    }
    return symbols.split(",").map((s) => ({
      value: s.trim(),
      label: s.trim()
    }));
  };

  const strategyOptions = [
    { value: StrategyType.RSI_CROSS_TREND, label: StrategyType.RSI_CROSS_TREND_value },
    { value: StrategyType.MULTI_SMAS_MOMENTUM, label: StrategyType.MULTI_SMAS_MOMENTUM_value },
    { value: StrategyType.RSI_DIP_ACCUMULATION, label: StrategyType.RSI_DIP_ACCUMULATION_value }
  ].sort((a, b) => a.label.localeCompare(b.label));

  const validateConfig = () => {
    const newErrors = {};

    if (!selectedConfig?.symbols || selectedConfig.symbols.length === 0) {
      newErrors.symbols = "At least one symbol is required";
    }

    if (!selectedConfig?.strategies || selectedConfig.strategies.length === 0) {
      newErrors.strategies = "At least one strategy is required";
    }

    if (!selectedConfig?.timeframes?.trend) {
      newErrors.trend = "Trend timeframe required";
    }

    if (!selectedConfig?.timeframes?.entry) {
      newErrors.entry = "Entry timeframe required";
    }

    if (
      selectedConfig?.timeframes?.trend &&
      selectedConfig?.timeframes?.entry &&
      selectedConfig.timeframes.trend === selectedConfig.timeframes.entry
    ) {
      newErrors.entry = "Trend and Entry must be different";
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSaveConfig = async () => {
    if (!selectedConfig) {
      showToast("error", "No entry data to save");
      return;
    }

    if (!validateConfig()) {
      showToast("error", "Fix form errors before saving");
      return;
    }

    try {
      let updatedConfigs;

      if (selectedConfig.id) {
        // update
        updatedConfigs = config.configurations.map(c =>
          c.id === selectedConfig.id ? selectedConfig : c
        );
      } else {
        // create
        updatedConfigs = [
          ...config.configurations,
          {
            ...selectedConfig,
            id: crypto.randomUUID().slice(0, 8),
            enabled: true,
            symbols: selectedConfig.symbols || [],
            strategies: selectedConfig.strategies || [],
            timeframes: selectedConfig.timeframes || { trend: "", entry: "" }
          }
        ];
      }
  
      const newConfig = {
        ...config,
        configurations: updatedConfigs
      };

      const response = await saveConfig(newConfig);

      if (response.success) {
        showToast("info", "Configuration saved");
        setConfig(newConfig);
        setSelectedConfig(null);
      } else {
        const msg = response.errors?.[0]?.msg || "Invalid config";
        showToast("error", msg);
      }
    } catch (error) {
      console.error("Error saving configuration:", error);
      showToast("error", "Error saving configuration");
    }
  };

  const validateConfigInterval = () => {
    const newErrors = {};
    
    if (!config.execution_interval || config.execution_interval < 30) {
      newErrors.execution_interval = "Execution interval must be greater or equal to 30";
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSaveInterval = async () => {
    if (!validateConfigInterval()) {
      showToast("error", "Fix form errors before saving");
      return;
    }

    try {    
      const newConfig = {
        ...config,
        execution_interval: config.execution_interval
      };
      
      const response = await saveConfig(newConfig);

      if (response.success) {
        showToast("info", "Interval saved");
        setConfig(newConfig);
      } else {
        const msg = response.errors?.[0]?.msg || "Invalid interval";
        showToast("error", msg);
      }
    } catch (error) {
      console.error("Error saving interval:", error);
      showToast("error", "Error saving interval");
    }
  };

  if (loading) return <div className="loading-warning">Loading configuration...</div>;
  if (!config) return <div className="loading-warning">Error loading configuration</div>;

  return (
    <>
      <div className="config-panel">
        <div className="config-title">
          Analysis interval
        </div>
        <div className="field">
          <label>Execution (seconds):</label>
          <input
            type="number"
            min={30}
            value={config.execution_interval || ""}
            onChange={(e) => {
              setConfig({
                ...config,
                execution_interval: parseInt(e.target.value) || 0
              });
            }}
          />
          {errors.execution_interval && (
            <span className="error">{errors.execution_interval}</span>
          )}
        </div>
        <div className="actions">
          <button onClick={handleSaveInterval}>
            Save
          </button>
        </div>
      </div>
      <div className="config-panel">
        <div className="config-title">
          Add or edit configuration
        </div>
        <div className="field">
          <label>Symbols:</label>
          <AsyncSelect
              isMulti
              cacheOptions
              isSearchable
              closeMenuOnSelect={false}
              defaultOptions={false}
              value={parseSymbols(selectedConfig?.symbols)}
              loadOptions={loadSymbols}
              onChange={(selected) => {
                const unique = [...new Set((selected || []).map(s => s.value))].sort();
                setSelectedConfig({ ...selectedConfig, symbols: unique });
              }}
              placeholder="Select symbols..."
              classNamePrefix={"symbol-select"}
            />
            {errors.symbols && <span className="error">{errors.symbols}</span>}
        </div>
        <div className="field">
          <label>Strategies:</label>
          <AsyncSelect
              isMulti
              isSearchable
              defaultOptions={strategyOptions}
              value={strategyOptions.filter(opt =>
                selectedConfig?.strategies?.includes(opt.value)
              )}
              onChange={(selected) => {
                const strategies = selected?.map(s => s.value) || [];
                setSelectedConfig({ ...selectedConfig, strategies });
              }}
              placeholder="Select strategies..."
              classNamePrefix={"symbol-select"}
            />
          {errors.strategies && <span className="error">{errors.strategies}</span>}
        </div>
        <div className="field">
          <label>Timeframe Trend:</label>
          <select
            value={selectedConfig?.timeframes?.trend || ""}
            onChange={(e) =>
              setSelectedConfig({
                ...selectedConfig,
                timeframes: {
                  ...(selectedConfig?.timeframes || {}),
                  trend: e.target.value
                }
              })
            }
          >
            <option value="">Select trend...</option>
            <option value="M5">M5</option>
            <option value="M15">M15</option>
            <option value="H1">H1</option>
            <option value="H4">H4</option>
            <option value="D1">D1</option>
            <option value="W1">W1</option>
          </select>
          {errors.trend && <span className="error">{errors.trend}</span>}
        </div>
        <div className="field">
          <label>Timeframe Entry:</label>
          <select
            value={selectedConfig?.timeframes?.entry || ""}
            onChange={(e) =>
              setSelectedConfig({
                ...selectedConfig,
                timeframes: {
                  ...(selectedConfig?.timeframes || {}),
                  entry: e.target.value
                }
              })
            }
          >
            <option value="">Select entry...</option>
            <option value="M5">M5</option>
            <option value="M15">M15</option>
            <option value="H1">H1</option>
            <option value="H4">H4</option>
            <option value="D1">D1</option>
            <option value="W1">W1</option>
          </select>
          {errors.entry && <span className="error">{errors.entry}</span>}
        </div>
        <div className="actions">
          <button onClick={handleSaveConfig}>
            Save
          </button>
        </div>
      </div>
    </>
  );
}

export default ConfigPanel;
