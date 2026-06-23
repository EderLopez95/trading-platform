import { NavLink } from "react-router-dom";
import styles from "./Sidebar.module.scss";

export default function Sidebar() {
  
  return (
    <aside className={styles.sidebar}>
      <nav className={styles.nav}>
        <ul>
          <li>
            <NavLink to="/">
              Dashboard
            </NavLink>
          </li>
          <li>
            <NavLink to="/signals">
              Signals
            </NavLink>
          </li>
          <li>
            <NavLink to="/configurations">
              Configurations
            </NavLink>
          </li>
          <li>
            <NavLink to="/profile">
              Profile
            </NavLink>
          </li>
        </ul>
      </nav>
    </aside>
  );
}
