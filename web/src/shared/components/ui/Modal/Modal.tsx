import { useEffect, useState, type ReactNode } from "react";
import styles from "./Modal.module.scss";

type Props = {
  isOpen: boolean;
  onClose: () => void;
  title?: string;
  children: ReactNode;
};

const ANIMATION_MS = 300;

export default function Modal({
  isOpen,
  onClose,
  title,
  children,
}: Props) {
  const [isRendered, setIsRendered] = useState(isOpen);
  const [isClosing, setIsClosing] = useState(false);

  useEffect(() => {
    if (isOpen) {
      setIsRendered(true);
      setIsClosing(false);

      return;
    }

    if (!isRendered) {
      return;
    }

    setIsClosing(true);

    const timer = setTimeout(() => {
      setIsRendered(false);
      setIsClosing(false);
    }, ANIMATION_MS);

    return () => clearTimeout(timer);
  }, [isOpen, isRendered]);

  useEffect(() => {
    if (!isOpen) {
      return;
    }

    const handleEscape = (event: KeyboardEvent) => {
      if (event.key === "Escape") {
        onClose();
      }
    };

    document.addEventListener("keydown", handleEscape);

    return () => {
      document.removeEventListener("keydown", handleEscape);
    };
  }, [isOpen, onClose]);

  if (!isRendered) {
    return null;
  }

  const overlayClass = isClosing
    ? `${styles.overlay} ${styles.overlayClosing}`
    : styles.overlay;

  const modalClass = isClosing
    ? `${styles.modal} ${styles.modalClosing}`
    : styles.modal;

  return (
    <div className={overlayClass} onMouseDown={onClose}>
      <div
        className={modalClass}
        role="dialog"
        aria-modal="true"
        onMouseDown={(event) => event.stopPropagation()}
      >
        <div className={styles.header}>
          {title && <h3 className={styles.title}>{title}</h3>}
          <button
            type="button"
            className={styles.close}
            aria-label="Close"
            onClick={onClose}
          >
            <svg
              width="20"
              height="20"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
            >
              <line x1="6" y1="6" x2="18" y2="18" />
              <line x1="18" y1="6" x2="6" y2="18" />
            </svg>
          </button>
        </div>
        <div className={styles.body}>{children}</div>
      </div>
    </div>
  );
}
