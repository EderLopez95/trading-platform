import { useContext } from "react";
import { AppContext } from "../App";
import "./ConfigCards.scss";
import { StrategyType } from "../enums";
import { saveConfig } from "../services/api";
import StrategyTooltip from "./StrategyTooltip";

function ConfigCards() {
    const { config, setConfig, setSelectedConfig, showToast } = useContext(AppContext);

    const strategyDocs = {
        [StrategyType.RSI_CROSS_TREND]: "rsi_cross_trend_strategy.md",
        [StrategyType.MULTI_SMAS_MOMENTUM]: "multi_smas_momentum_strategy.md",
        [StrategyType.RSI_DIP_ACCUMULATION]: "rsi_dip_accumulation_strategy.md"
    };

    const updateDeleteConfig = async (getUpdatedConfigs, successMessage) => {
        const newConfig = {
            ...config,
            configurations: getUpdatedConfigs(config.configurations)
        };
        const response = await saveConfig(newConfig);
        
        if (response.success) {
            showToast("info", successMessage);
            setConfig(newConfig);
        } else {
            const msg = response.errors?.[0]?.msg || "Invalid data";
            showToast("error", msg);
        }
    };

    const handleDelete = (id) => {
        updateDeleteConfig(
            (configs) => configs.filter(c => c.id !== id),
            "Configuration deleted"
        );
    };

    const handleToggle = (id) => {
        updateDeleteConfig(
            (configs) => configs.map(c => c.id === id ? { ...c, enabled: !c.enabled } : c),
            "Configuration status updated"
        );
    };

    return (
        <>
            {config.configurations.map(c => (
                <div key={c.id} className={`card ${!c.enabled ? 'disable' : ''}`}>
                    <div className="delete" onClick={() => handleDelete(c.id)}></div>
                    <div className="label">
                        Symbols
                    </div>
                    <div className="label-data">
                        <ul className="grid">
                            {c.symbols.map((symbol, index) => (
                                <li key={index}>{symbol}</li>
                            ))}
                        </ul>
                    </div>
                    <div className="label">
                        Strategies
                    </div>
                    <div className="label-data">
                        <ul>
                            {c.strategies.map((strategy, index) => {
                                let label = "Unknown";
                                let doc = "";
                                
                                if (strategy === StrategyType.RSI_CROSS_TREND) {
                                    label = StrategyType.RSI_CROSS_TREND_value;
                                    doc = strategyDocs[StrategyType.RSI_CROSS_TREND];
                                }
                                else if (strategy === StrategyType.MULTI_SMAS_MOMENTUM) {
                                    label = StrategyType.MULTI_SMAS_MOMENTUM_value;
                                    doc = strategyDocs[StrategyType.MULTI_SMAS_MOMENTUM];
                                }
                                else if (strategy === StrategyType.RSI_DIP_ACCUMULATION) {
                                    label = StrategyType.RSI_DIP_ACCUMULATION_value;
                                    doc = strategyDocs[StrategyType.RSI_DIP_ACCUMULATION];
                                }

                                return (
                                    <li key={index}>
                                        <div className="strategy-row">
                                            <span>{label}</span>
                                            {doc && (
                                                <div className="tooltip-wrapper">
                                                    <span className="info-icon"></span>
                                                    <StrategyTooltip path={`/strategies/${doc}`} />
                                                </div>
                                            )}
                                        </div>
                                    </li>
                                );
                            })}
                        </ul>
                    </div>
                    <div className="label">
                        Temporalities
                    </div>
                    <div className="label-data temps">
                        <ul>
                            <li>Trend: {c.timeframes.trend}</li>
                            <li>Entry: {c.timeframes.entry}</li>
                        </ul>
                        <div className="controls">
                            <button className="edit" onClick={() => setSelectedConfig(c)}></button>
                            <label className="status">
                                <input type="checkbox"
                                    checked={c.enabled}
                                    onChange={() => handleToggle(c.id)}
                                />
                                <span className="slider"></span>
                            </label>
                        </div>
                    </div>
                </div>
            ))}
        </>
    )
}

export default ConfigCards;
