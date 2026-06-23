import {
  createContext,
  useContext,
  useState,
  type ReactNode,
  useEffect
} from "react";
import { authApi } from "@/modules/auth/api/authApi";
import { type User } from "@/modules/auth/types/auth.types";

type AuthContextType = {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;

  login: (token: string) => void;
  logout: () => void;
};

const AuthContext = createContext<AuthContextType | null>(null);

type Props = {children: ReactNode;};

export function AuthProvider({ children }: Props) {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  const loadUser = async () => {
    const token = localStorage.getItem("token");

    if (!token) {
      setIsLoading(false);
      return;
    }

    try {
      const currentUser = await authApi.getMe();
      setUser(currentUser);
      setIsAuthenticated(true);
    } catch {
      localStorage.removeItem("token");
      setUser(null);
      setIsAuthenticated(false);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    loadUser();
  }, []);

  const login = (token: string) => {
    localStorage.setItem("token", token);
    loadUser();
  };

  const logout = () => {
    localStorage.removeItem("token");
    setUser(null);
    setIsAuthenticated(false);
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        isAuthenticated,
        isLoading,
        login,
        logout,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export const useAuth = () => {
  const context = useContext(AuthContext);

  if (!context) {
    throw new Error("AuthProvider missing");
  }

  return context;
};
