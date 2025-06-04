import React, { createContext, useContext, useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

interface AuthContextType {
  isAuthenticated: boolean;
  userId: string | null;
  userEmail: string | null;
  username: string | null;
  userType: string | null;
  login: (userData: any) => void;
  logout: () => void;
}

export const AuthContext = createContext<AuthContextType | undefined>(
  undefined
);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({
  children,
}) => {
  const [isAuthenticated, setIsAuthenticated] = useState<boolean>(false);
  const [userId, setUserId] = useState<string | null>(null);
  const [userEmail, setUserEmail] = useState<string | null>(null);
  const [username, setUsername] = useState<string | null>(null);
  const [userType, setUserType] = useState<string | null>(null);
  const navigate = useNavigate();

  useEffect(() => {
    // 페이지 로드 시 로컬 스토리지에서 사용자 정보 불러오기
    const token = localStorage.getItem("access_token");
    const savedUserId = localStorage.getItem("user_id");
    const savedUserEmail = localStorage.getItem("user_email");
    const savedUsername = localStorage.getItem("username");
    const savedUserType = localStorage.getItem("user_type");

    if (token && savedUserId) {
      setIsAuthenticated(true);
      setUserId(savedUserId);
      setUserEmail(savedUserEmail);
      setUsername(savedUsername);
      setUserType(savedUserType);
    }
  }, []);

  const login = (userData: any) => {
    localStorage.setItem("access_token", userData.access_token);
    localStorage.setItem("user_id", userData.user_id);
    localStorage.setItem("user_email", userData.email);
    localStorage.setItem("username", userData.username);
    localStorage.setItem("user_type", userData.user_type);

    setIsAuthenticated(true);
    setUserId(userData.user_id);
    setUserEmail(userData.email);
    setUsername(userData.username);
    setUserType(userData.user_type);
  };

  const logout = () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("user_id");
    localStorage.removeItem("user_email");
    localStorage.removeItem("username");
    localStorage.removeItem("user_type");

    setIsAuthenticated(false);
    setUserId(null);
    setUserEmail(null);
    setUsername(null);
    setUserType(null);

    navigate("/");
  };

  return (
    <AuthContext.Provider
      value={{
        isAuthenticated,
        userId,
        userEmail,
        username,
        userType,
        login,
        logout,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
};
