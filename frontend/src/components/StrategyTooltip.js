import { useEffect, useState } from "react";
import ReactMarkdown from "react-markdown";

function StrategyTooltip({ file }) {
  const [content, setContent] = useState("");

  useEffect(() => {
    fetch(`/strategies/${file}`)
      .then(res => res.text())
      .then(text => setContent(text));
  }, [file]);

  return (
    <div className="strategy-tooltip">
      <div className="strategy-tooltip-wrapper">
        <ReactMarkdown
            components={{
                h1: ({ children }) => (
                <div className="md-title">
                    {children}
                </div>
                ),
                h2: ({ children }) => (
                <div className="md-subtitle">
                    {children}
                </div>
                ),
                p: ({ children }) => (
                <div className="md-text">
                    {children}
                </div>
                ),
                ul: ({ children }) => (
                <ul className="md-list">
                    {children}
                </ul>
                )
            }}
            >
            {content}
        </ReactMarkdown>
      </div>
    </div>
  );
}

export default StrategyTooltip;
