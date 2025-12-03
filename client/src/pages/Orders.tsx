import { Layout } from "@/components/layout/Layout";
import { Card, CardContent, CardHeader, CardTitle, CardDescription, CardFooter } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { 
  Table, 
  TableBody, 
  TableCell, 
  TableHead, 
  TableHeader, 
  TableRow 
} from "@/components/ui/table";
import { 
  DropdownMenu, 
  DropdownMenuContent, 
  DropdownMenuItem, 
  DropdownMenuLabel, 
  DropdownMenuSeparator, 
  DropdownMenuTrigger 
} from "@/components/ui/dropdown-menu";
import { 
  Package, 
  Truck, 
  CheckCircle2, 
  Clock, 
  AlertCircle, 
  MoreHorizontal, 
  FileText, 
  Printer,
  Scissors,
  Palette
} from "lucide-react";

// Mock Data for Orders
const ORDERS = [
  { 
    id: "PED-2024-001", 
    client: "Tech Solutions", 
    items: "50x Camisetas Algodão", 
    total: "R$ 2.500,00", 
    status: "Produção", 
    progress: 60,
    step: "Estamparia",
    deliveryDate: "10/12/2024",
    supplier: "Estamparia Silva" 
  },
  { 
    id: "PED-2024-002", 
    client: "Café do João", 
    items: "20x Aventais Bege", 
    total: "R$ 1.200,00", 
    status: "Enviado", 
    progress: 90,
    step: "Transporte",
    deliveryDate: "05/12/2024",
    supplier: "Confecção Rápida" 
  },
  { 
    id: "PED-2024-003", 
    client: "Evento XP", 
    items: "200x Camisetas Brancas", 
    total: "R$ 8.000,00", 
    status: "Entregue", 
    progress: 100,
    step: "Concluído",
    deliveryDate: "01/12/2024",
    supplier: "Malharia Premium" 
  },
  { 
    id: "PED-2024-004", 
    client: "Startup Hub", 
    items: "30x Moletons", 
    total: "R$ 4.500,00", 
    status: "Aprovado", 
    progress: 10,
    step: "Corte",
    deliveryDate: "15/12/2024",
    supplier: "Estamparia Silva" 
  }
];

export default function Orders() {
  return (
    <Layout title="Pedidos">
      <div className="flex items-center justify-between mb-6">
        <div className="flex flex-col gap-1">
          <h2 className="text-lg font-serif text-primary">Gestão de Produção</h2>
          <p className="text-sm text-muted-foreground">Acompanhe o status de produção e entrega dos pedidos.</p>
        </div>
        <Button className="bg-primary text-primary-foreground">
          <FileText className="mr-2 h-4 w-4" /> Exportar Relatório
        </Button>
      </div>

      <Tabs defaultValue="active" className="w-full">
        <TabsList className="mb-6 bg-muted/50">
          <TabsTrigger value="active">Em Andamento</TabsTrigger>
          <TabsTrigger value="completed">Concluídos</TabsTrigger>
          <TabsTrigger value="all">Todos</TabsTrigger>
        </TabsList>

        <TabsContent value="active" className="space-y-6">
          <div className="grid gap-6">
            {ORDERS.filter(o => o.progress < 100).map((order) => (
              <Card key={order.id} className="border-none shadow-sm overflow-hidden hover:shadow-md transition-shadow">
                <div className="border-l-4 border-primary h-full">
                  <CardHeader className="pb-2 flex flex-row items-start justify-between">
                    <div>
                      <div className="flex items-center gap-2 mb-1">
                        <Badge variant="outline" className="font-mono text-xs">{order.id}</Badge>
                        <Badge className={
                          order.status === 'Produção' ? 'bg-blue-100 text-blue-700 hover:bg-blue-100' :
                          order.status === 'Enviado' ? 'bg-amber-100 text-amber-700 hover:bg-amber-100' :
                          'bg-emerald-100 text-emerald-700 hover:bg-emerald-100'
                        }>
                          {order.status}
                        </Badge>
                      </div>
                      <CardTitle className="text-lg">{order.client}</CardTitle>
                      <CardDescription>{order.items} • {order.supplier}</CardDescription>
                    </div>
                    <DropdownMenu>
                      <DropdownMenuTrigger asChild>
                        <Button variant="ghost" size="icon" className="h-8 w-8">
                          <MoreHorizontal className="h-4 w-4" />
                        </Button>
                      </DropdownMenuTrigger>
                      <DropdownMenuContent align="end">
                        <DropdownMenuLabel>Ações</DropdownMenuLabel>
                        <DropdownMenuItem><Printer className="mr-2 h-4 w-4" /> Imprimir Etiqueta</DropdownMenuItem>
                        <DropdownMenuItem><FileText className="mr-2 h-4 w-4" /> Ver Nota de Produção</DropdownMenuItem>
                        <DropdownMenuSeparator />
                        <DropdownMenuItem>Atualizar Status</DropdownMenuItem>
                      </DropdownMenuContent>
                    </DropdownMenu>
                  </CardHeader>
                  
                  <CardContent className="pb-6">
                    <div className="space-y-4">
                      <div className="flex items-center justify-between text-sm">
                        <span className="flex items-center gap-2 text-muted-foreground">
                          {order.step === 'Corte' && <Scissors className="h-4 w-4" />}
                          {order.step === 'Estamparia' && <Palette className="h-4 w-4" />}
                          {order.step === 'Transporte' && <Truck className="h-4 w-4" />}
                          Etapa Atual: <span className="font-medium text-foreground">{order.step}</span>
                        </span>
                        <span className="flex items-center gap-1 text-muted-foreground">
                          <Clock className="h-3 w-3" /> Entrega: {order.deliveryDate}
                        </span>
                      </div>
                      <div className="space-y-1">
                        <div className="flex justify-between text-xs font-medium">
                          <span>Progresso</span>
                          <span>{order.progress}%</span>
                        </div>
                        <Progress value={order.progress} className="h-2" />
                      </div>
                    </div>
                  </CardContent>
                  
                  <div className="px-6 py-3 bg-muted/20 border-t border-border flex items-center justify-between">
                    <div className="flex items-center gap-4 text-xs text-muted-foreground">
                      <div className={`flex items-center gap-1 ${order.progress >= 20 ? 'text-primary font-medium' : ''}`}>
                        <CheckCircle2 className="h-3 w-3" /> Corte
                      </div>
                      <div className="w-8 h-[1px] bg-border"></div>
                      <div className={`flex items-center gap-1 ${order.progress >= 60 ? 'text-primary font-medium' : ''}`}>
                        <CheckCircle2 className="h-3 w-3" /> Estampa
                      </div>
                      <div className="w-8 h-[1px] bg-border"></div>
                      <div className={`flex items-center gap-1 ${order.progress >= 80 ? 'text-primary font-medium' : ''}`}>
                        <CheckCircle2 className="h-3 w-3" /> Costura
                      </div>
                      <div className="w-8 h-[1px] bg-border"></div>
                      <div className={`flex items-center gap-1 ${order.progress >= 90 ? 'text-primary font-medium' : ''}`}>
                        <CheckCircle2 className="h-3 w-3" /> Envio
                      </div>
                    </div>
                    <Button variant="outline" size="sm" className="h-7 text-xs">
                      Detalhes
                    </Button>
                  </div>
                </div>
              </Card>
            ))}
          </div>
        </TabsContent>

        <TabsContent value="completed">
          <Card className="border-none shadow-sm">
            <CardHeader>
              <CardTitle className="font-serif text-lg">Histórico de Pedidos</CardTitle>
            </CardHeader>
            <CardContent>
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>ID</TableHead>
                    <TableHead>Cliente</TableHead>
                    <TableHead>Itens</TableHead>
                    <TableHead>Fornecedor</TableHead>
                    <TableHead>Entrega</TableHead>
                    <TableHead>Total</TableHead>
                    <TableHead className="text-right">Status</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {ORDERS.filter(o => o.progress === 100).map((order) => (
                    <TableRow key={order.id}>
                      <TableCell className="font-mono text-xs">{order.id}</TableCell>
                      <TableCell className="font-medium">{order.client}</TableCell>
                      <TableCell>{order.items}</TableCell>
                      <TableCell>{order.supplier}</TableCell>
                      <TableCell>{order.deliveryDate}</TableCell>
                      <TableCell>{order.total}</TableCell>
                      <TableCell className="text-right">
                        <Badge variant="secondary" className="bg-emerald-100 text-emerald-700 hover:bg-emerald-100">
                          {order.status}
                        </Badge>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </Layout>
  );
}
