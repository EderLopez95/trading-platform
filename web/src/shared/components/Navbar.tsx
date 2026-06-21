import { useNavigate } from "react-router-dom";
import { useAuth } from "@/app/providers/AuthProvider";

export default function Navbar() {
  const navigate = useNavigate();
  const { logout } = useAuth();

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  return (
    <header>
      <h2>Trading Platform</h2>
      <button onClick={handleLogout}>
        Logout
      </button>
    </header>
  );
}
