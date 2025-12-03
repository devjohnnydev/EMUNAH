import React, { createContext, useContext, useState, useEffect } from "react";
import { useLocation } from "wouter";

// Mock User Type
export interface User {
  id: string;
  name: string;
  email: string;
  role: "ADMIN" | "SELLER" | "SUPPLIER";
  avatar?: string;
}

interface AuthContextType {
  user: User | null;
  isLoading: boolean;
  login: (email: string, password: string) => Promise<boolean>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | null>(null);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [, setLocation] = useLocation();

  useEffect(() => {
    // Simulate checking for existing session
    const storedUser = localStorage.getItem("emunah_user");
    if (storedUser) {
      setUser(JSON.parse(storedUser));
    }
    setIsLoading(false);
  }, []);

  const login = async (email: string, password: string) => {
    // Mock Authentication Logic
    // In a real app, this would hit the backend API
    return new Promise<boolean>((resolve) => {
      setTimeout(() => {
        if (email === "admin@emunah.com" && password === "123456") {
          const adminUser: User = {
            id: "1",
            name: "Admin User",
            email: "admin@emunah.com",
            role: "ADMIN",
            avatar: "/avatars/01.png"
          };
          setUser(adminUser);
          localStorage.setItem("emunah_user", JSON.stringify(adminUser));
          resolve(true);
        } else {
          resolve(false);
        }
      }, 1000); // Simulate network delay
    });
  };

  const logout = () => {
    setUser(null);
    localStorage.removeItem("emunah_user");
    setLocation("/login");
  };

  return (
    <AuthContext.Provider value={{ user, isLoading, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
}
