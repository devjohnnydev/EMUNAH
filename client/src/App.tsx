import { Switch, Route } from "wouter";
import { queryClient } from "./lib/queryClient";
import { QueryClientProvider } from "@tanstack/react-query";
import { Toaster } from "@/components/ui/toaster";
import { TooltipProvider } from "@/components/ui/tooltip";
import NotFound from "@/pages/not-found";

// Pages
import Dashboard from "@/pages/Dashboard";
import Quotes from "@/pages/Quotes";
import Budgets from "@/pages/Budgets";
import Suppliers from "@/pages/Suppliers";
import Prints from "@/pages/Prints";

function Router() {
  return (
    <Switch>
      <Route path="/" component={Dashboard} />
      <Route path="/quotes" component={Quotes} />
      <Route path="/budgets" component={Budgets} />
      <Route path="/suppliers" component={Suppliers} />
      <Route path="/prints" component={Prints} />
      {/* Placeholders for other routes to avoid 404 immediately if clicked */}
      <Route path="/orders" component={Dashboard} />
      <Route path="/clients" component={Dashboard} />
      <Route path="/reports" component={Dashboard} />
      <Route path="/settings" component={Dashboard} />
      
      <Route component={NotFound} />
    </Switch>
  );
}

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <TooltipProvider>
        <Toaster />
        <Router />
      </TooltipProvider>
    </QueryClientProvider>
  );
}

export default App;
