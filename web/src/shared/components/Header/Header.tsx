import { useEffect, useRef, useState } from "react";
import { NavLink, useNavigate } from "react-router-dom";
import { useAuth } from "@/app/providers/AuthProvider";
import styles from "./Header.module.scss";

export default function Header() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const menuRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!isMenuOpen) {
      return;
    }

    const handleClickOutside = (event: MouseEvent) => {
      if (
        menuRef.current &&
        !menuRef.current.contains(event.target as Node)
      ) {
        setIsMenuOpen(false);
      }
    };

    const handleEscape = (event: KeyboardEvent) => {
      if (event.key === "Escape") {
        setIsMenuOpen(false);
      }
    };

    document.addEventListener("mousedown", handleClickOutside);
    document.addEventListener("keydown", handleEscape);

    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
      document.removeEventListener("keydown", handleEscape);
    };
  }, [isMenuOpen]);

  const handleLogout = () => {
    setIsMenuOpen(false);
    logout();
    navigate("/login", { replace: true });
  };

  const handleSettings = () => {
    setIsMenuOpen(false);
    navigate("/settings");
  };

  const tabClassName = ({ isActive }: { isActive: boolean }) =>
    isActive ? `${styles.tab} ${styles.tabActive}` : styles.tab;

  return (
    <header className={styles.header}>
      <div className={styles.topRow}>
        <span className={styles.email}>{user?.email}</span>
        <div className={styles.menuWrapper} ref={menuRef}>
          <button
            type="button"
            className={styles.burger}
            aria-label="Open menu"
            aria-haspopup="true"
            aria-expanded={isMenuOpen}
            onClick={() => setIsMenuOpen((open) => !open)}
          >
            <svg
              width="22"
              height="22"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
            >
              <line x1="3" y1="6" x2="21" y2="6" />
              <line x1="3" y1="12" x2="21" y2="12" />
              <line x1="3" y1="18" x2="21" y2="18" />
            </svg>
          </button>

          {isMenuOpen && (
            <div className={styles.dropdown} role="menu">
              <button
                type="button"
                role="menuitem"
                className={styles.dropdownItem}
                onClick={handleSettings}
              >
                Settings
              </button>
              <button
                type="button"
                role="menuitem"
                className={styles.dropdownItem}
                onClick={handleLogout}
              >
                Logout
              </button>
            </div>
          )}
        </div>
      </div>

      <nav className={styles.tabs}>
        <NavLink to="/signals" className={tabClassName}>
          Signals
        </NavLink>
      </nav>
    </header>
  );
}
