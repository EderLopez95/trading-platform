import { useState, useEffect, createContext, useRef } from "react";
import { getStatus } from "./services/api";
import BotControl from "./components/BotControl";
import ConfigPanel from "./components/ConfigPanel";
import LogPanel from "./components/LogPanel";
import SignalPanel from "./components/SignalPanel";
import ConfigCards from "./components/ConfigCards";
import { SignalType, LogType, BotStatus } from "./enums";
import { getConfig } from "./services/api";

export const AppContext = createContext();

function App() {
  const [status, setStatus] = useState("Loading...");
  const [signals, setSignals] = useState([]);
  const [alerts, setAlerts] = useState([]);
  const [logs, setLogs] = useState([]);
  const wsRef = useRef(null);
  const hasInitialized = useRef(false);
  const [config, setConfig] = useState({
    execution_interval: 30, // minimum interval
    configurations: []
  })
  const [selectedConfig, setSelectedConfig] = useState(null);

  const showToast = (type, message) => {
    const id = Date.now();
    const newAlert = { id, type, message };
    setAlerts(prev => [newAlert, ...prev]);
    setTimeout(() => {
      setAlerts(prev => prev.filter(alert => alert.id !== id));
    }, 2000);
  };

  const loadConfig = async () => {
    try {
      const data = await getConfig();
      setConfig({
        ...data
      });
    } catch (error) {
      console.error("Error loading config:", error);
    }
  };

  useEffect(() => {
    loadConfig();
  }, []);

  useEffect(() => {
    const storedSignals = localStorage.getItem("signals");

    if (storedSignals) {
      setSignals(JSON.parse(storedSignals));
    }
  }, []);

  useEffect(() => {
    const storedLogs = localStorage.getItem("logs");

    if (storedLogs) {
      setLogs(JSON.parse(storedLogs));
    }
  }, []);

  useEffect(() => {
    if (hasInitialized.current) return;
    hasInitialized.current = true;

    const connectWebSocket = () => {
      // avoid websocket double connection on hot reload
      if (
        wsRef.current &&
        (wsRef.current.readyState === WebSocket.OPEN ||
          wsRef.current.readyState === WebSocket.CONNECTING)
      ) {
        console.log("WebSocket already connected");
        return;
      }

      const ws = new WebSocket(process.env.REACT_APP_WS_URL);
      wsRef.current = ws;
      
      ws.onopen = () => {
        console.log("WebSocket connected");
      };
      
      ws.onmessage = (event) => {
        const MAX_LOGS = 100;
        try {
          const message = JSON.parse(event.data);
          
          // messages from backend
          if (message.signal === SignalType.BUY || message.signal === SignalType.SELL) {
            setSignals(prev => {
              const updated = [message, ...prev].slice(0, MAX_LOGS);
              localStorage.setItem("signals", JSON.stringify(updated));
              return updated;
            });
          }
          
          if (message.level === LogType.ERROR || message.level === LogType.INFO) {
            setLogs(prev => {
              const updated = [message, ...prev].slice(0, MAX_LOGS);
              localStorage.setItem("logs", JSON.stringify(updated));
              return updated;
            });
          }
        } catch (error) {
          console.error("Error parsing WS message:", error);
        }
      };
      
      ws.onclose = () => {
        wsRef.current = null;
        console.log("WebSocket disconnected");
        // automatic reconnection
        setTimeout(() => {
          console.log("Reconnecting...");
          connectWebSocket();
        }, 3000);
      };
      
      ws.onerror = (error) => {
        console.error("WebSocket error:", error);
        ws.close();
      };
    };

    // validate backend before connecting WebSocket
    const init = async () => {
      try {
        const ready = await getStatus();
        
        if (ready) {
          connectWebSocket();
          
          if (ready.status === BotStatus.RUNNING) {
            setStatus(BotStatus.RUNNING);
          } else if (ready.status === BotStatus.STOPPED) {
            setStatus(BotStatus.STOPPED);
          } else {
            setStatus(BotStatus.UNKNOWN);
            showToast("error", "Could not determine bot status");
          }
        } else {
          setTimeout(init, 1000);
        }
      }
      catch (error) {
        console.error("Error initializing app:", error);
        showToast("error", "Could not determine bot status");
      }
    };

    init();

    return () => {
      if (wsRef.current) {
        wsRef.current.close();
        wsRef.current = null;
      }
    };
  }, []);

  return (
    <AppContext.Provider value={{ 
      showToast,
      setStatus,
      setSignals,
      setLogs,
      config,
      setConfig,
      selectedConfig,
      setSelectedConfig
    }}>
      <div className="container">
        <div className="wrapper">
          <div className="wrapper-config">
            <div className="wrapper-bot">
              <BotControl status={status} />
            </div>
            <ConfigPanel />
          </div>
          {config.configurations?.length > 0 && (
            <div className="wrapper-config cards">
              <ConfigCards />
            </div>
          )}
          <div className="wrapper-tables">
            <SignalPanel signals={signals} />
            <LogPanel logs={logs} />
          </div>
        </div>
      </div>
      <div className="toast-container">
        {alerts.map(alert => (
          <div key={alert.id} className={`alert-toast ${alert.type}`}>
            {alert.message}
          </div>
        ))}
      </div>
    </AppContext.Provider>
  );
}

export default App;
