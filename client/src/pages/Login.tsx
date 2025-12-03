import { useState } from "react";
import { useLocation } from "wouter";
import { useAuth } from "@/lib/auth";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent, CardHeader, CardTitle, CardDescription, CardFooter } from "@/components/ui/card";
import { useToast } from "@/hooks/use-toast";
import { Loader2, Lock } from "lucide-react";
import logo from "@assets/generated_images/emunah_brand_logo.png";

export default function Login() {
  const [email, setEmail] = useState("admin@emunah.com");
  const [password, setPassword] = useState("123456");
  const [loading, setLoading] = useState(false);
  const { login } = useAuth();
  const [, setLocation] = useLocation();
  const { toast } = useToast();

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    try {
      const success = await login(email, password);
      if (success) {
        toast({
          title: "Login realizado com sucesso",
          description: "Bem-vindo de volta ao Emunah System.",
        });
        setLocation("/");
      } else {
        toast({
          variant: "destructive",
          title: "Falha no login",
          description: "Credenciais inválidas. Tente admin@emunah.com / 123456",
        });
      }
    } catch (error) {
      toast({
        variant: "destructive",
        title: "Erro",
        description: "Ocorreu um erro ao tentar fazer login.",
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-background relative overflow-hidden">
      {/* Decorative Background Elements */}
      <div className="absolute top-0 left-0 w-full h-1/2 bg-primary/5 -skew-y-6 transform origin-top-left" />
      <div className="absolute bottom-0 right-0 w-full h-1/2 bg-secondary/10 -skew-y-6 transform origin-bottom-right" />

      <Card className="w-full max-w-md relative z-10 border-none shadow-xl">
        <CardHeader className="space-y-1 text-center flex flex-col items-center">
          <div className="h-16 w-16 bg-white rounded-full shadow-sm border border-muted flex items-center justify-center mb-4">
             <img src={logo} alt="Emunah" className="h-10 w-10" />
          </div>
          <CardTitle className="text-2xl font-serif text-primary">Acesso Administrativo</CardTitle>
          <CardDescription>
            Entre com suas credenciais para acessar o sistema
          </CardDescription>
        </CardHeader>
        <form onSubmit={handleLogin}>
          <CardContent className="grid gap-4">
            <div className="grid gap-2">
              <Label htmlFor="email">Email</Label>
              <Input 
                id="email" 
                type="email" 
                placeholder="nome@exemplo.com" 
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
            </div>
            <div className="grid gap-2">
              <Label htmlFor="password">Senha</Label>
              <Input 
                id="password" 
                type="password" 
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </div>
          </CardContent>
          <CardFooter className="flex flex-col gap-4">
            <Button className="w-full bg-primary text-primary-foreground hover:bg-primary/90" disabled={loading}>
              {loading ? (
                <>
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" /> Entrando...
                </>
              ) : (
                <>
                  <Lock className="mr-2 h-4 w-4" /> Entrar
                </>
              )}
            </Button>
            <div className="text-center text-xs text-muted-foreground">
              <p>Credenciais de teste:</p>
              <p className="font-mono mt-1">admin@emunah.com / 123456</p>
            </div>
          </CardFooter>
        </form>
      </Card>
    </div>
  );
}
