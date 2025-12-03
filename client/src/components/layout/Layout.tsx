import { Sidebar } from "./Sidebar";
import { Header } from "./Header";
import { Toaster } from "@/components/ui/toaster";

interface LayoutProps {
  children: React.ReactNode;
  title?: string;
}

export function Layout({ children, title }: LayoutProps) {
  return (
    <div className="min-h-screen bg-background font-sans text-foreground">
      <Sidebar />
      <div className="md:pl-64 min-h-screen flex flex-col transition-all duration-300">
        <Header title={title} />
        <main className="flex-1 p-6 overflow-x-hidden animate-in fade-in slide-in-from-bottom-4 duration-500">
          {children}
        </main>
      </div>
      <Toaster />
    </div>
  );
}
