import { Link, useLocation } from "wouter";
import { cn } from "@/lib/utils";
import { NAV_ITEMS } from "@/lib/constants";
import { useAuth } from "@/lib/auth";
import { LogOut } from "lucide-react";
import logo from "@assets/generated_images/emunah_brand_logo.png";

export function Sidebar() {
  const [location] = useLocation();
  const { user, logout } = useAuth();

  if (!user) return null;

  return (
    <aside className="hidden md:flex w-64 flex-col h-screen bg-sidebar text-sidebar-foreground border-r border-sidebar-border fixed left-0 top-0 z-50">
      <div className="p-6 flex items-center justify-center border-b border-sidebar-border/50">
        <div className="flex items-center gap-3">
          <img src={logo} alt="Emunah Logo" className="h-10 w-10 rounded-full border border-sidebar-primary/20" />
          <h1 className="text-2xl font-serif font-medium tracking-wide text-sidebar-primary">Emunah</h1>
        </div>
      </div>
      
      <nav className="flex-1 py-6 px-4 space-y-1 overflow-y-auto">
        {NAV_ITEMS.map((item) => {
          const isActive = location === item.href;
          const Icon = item.icon;
          
          return (
            <Link key={item.href} href={item.href}>
              <div className={cn(
                "flex items-center gap-3 px-4 py-3 rounded-md transition-all duration-200 group cursor-pointer",
                isActive 
                  ? "bg-sidebar-accent text-sidebar-accent-foreground shadow-sm" 
                  : "text-sidebar-foreground/70 hover:bg-sidebar-accent/50 hover:text-sidebar-foreground"
              )}>
                <Icon className={cn("h-5 w-5", isActive ? "text-sidebar-primary" : "text-sidebar-foreground/50 group-hover:text-sidebar-primary")} />
                <span className={cn("font-medium text-sm", isActive ? "font-semibold" : "")}>{item.label}</span>
              </div>
            </Link>
          );
        })}
      </nav>

      <div className="p-4 border-t border-sidebar-border/50">
        <div className="bg-sidebar-accent/30 rounded-lg p-4 mb-2">
          <p className="text-xs text-sidebar-foreground/60 mb-1">Usuário Logado</p>
          <div className="flex items-center gap-2">
            <div className="h-8 w-8 rounded-full bg-sidebar-primary flex items-center justify-center text-sidebar-primary-foreground font-bold text-xs">
              {user.name.charAt(0).toUpperCase() + user.name.charAt(1).toUpperCase()}
            </div>
            <div className="overflow-hidden">
              <p className="text-sm font-medium text-sidebar-foreground truncate">{user.name}</p>
              <p className="text-xs text-sidebar-foreground/50 truncate">{user.email}</p>
            </div>
          </div>
        </div>
        
        <button 
          onClick={logout}
          className="w-full flex items-center justify-center gap-2 text-xs text-sidebar-foreground/50 hover:text-destructive transition-colors py-2"
        >
          <LogOut className="h-3 w-3" /> Sair do Sistema
        </button>
      </div>
    </aside>
  );
}
