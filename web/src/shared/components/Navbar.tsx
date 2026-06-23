import { useNavigate } from "react-router-dom";
import { useAuth } from "@/app/providers/AuthProvider";

export default function Navbar() {
  const navigate = useNavigate();
  const { logout, user } = useAuth();

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  return (
    <header>
      <div>
        Trading Platform
      </div>
      <div>
        <span>
          {user?.email}
        </span>
        <button onClick={handleLogout}>
          Logout
        </button>
      </div>
    </header>
  );
}
