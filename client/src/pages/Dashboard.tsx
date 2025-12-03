import { Layout } from "@/components/layout/Layout";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { KPIS, REVENUE_DATA, ORDER_STATUS_DATA } from "@/lib/constants";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from "recharts";
import { ArrowUpRight, ArrowDownRight, CreditCard, ShoppingBag, FileText, DollarSign } from "lucide-react";

const COLORS = ['hsl(var(--chart-1))', 'hsl(var(--chart-2))', 'hsl(var(--chart-3))', 'hsl(var(--chart-4))', 'hsl(var(--chart-5))'];

export default function Dashboard() {
  return (
    <Layout title="Visão Geral">
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        {KPIS.map((kpi, index) => (
          <Card key={index} className="border-none shadow-sm bg-card hover:shadow-md transition-all duration-200">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium text-muted-foreground">
                {kpi.label}
              </CardTitle>
              {kpi.trend === "up" ? (
                <ArrowUpRight className="h-4 w-4 text-emerald-500" />
              ) : (
                <ArrowDownRight className="h-4 w-4 text-rose-500" />
              )}
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-serif font-bold text-primary">{kpi.value}</div>
              <p className={`text-xs ${kpi.trend === "up" ? "text-emerald-600" : "text-rose-600"} flex items-center mt-1`}>
                {kpi.change} 
                <span className="text-muted-foreground ml-1">vs mês anterior</span>
              </p>
            </CardContent>
          </Card>
        ))}
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-7 mt-6">
        <Card className="col-span-4 border-none shadow-sm">
          <CardHeader>
            <CardTitle className="font-serif text-lg text-primary">Faturamento Anual</CardTitle>
            <CardDescription>Receita acumulada mensalmente</CardDescription>
          </CardHeader>
          <CardContent className="pl-2">
            <div className="h-[300px]">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={REVENUE_DATA}>
                  <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="hsl(var(--muted))" />
                  <XAxis 
                    dataKey="name" 
                    stroke="hsl(var(--muted-foreground))" 
                    fontSize={12} 
                    tickLine={false} 
                    axisLine={false} 
                  />
                  <YAxis 
                    stroke="hsl(var(--muted-foreground))" 
                    fontSize={12} 
                    tickLine={false} 
                    axisLine={false} 
                    tickFormatter={(value) => `R$${value}`} 
                  />
                  <Tooltip 
                    contentStyle={{ backgroundColor: 'hsl(var(--popover))', borderColor: 'hsl(var(--border))', borderRadius: '8px' }}
                    itemStyle={{ color: 'hsl(var(--popover-foreground))' }}
                    formatter={(value) => [`R$ ${value}`, "Receita"]}
                  />
                  <Bar 
                    dataKey="value" 
                    fill="hsl(var(--primary))" 
                    radius={[4, 4, 0, 0]} 
                    barSize={30}
                  />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </CardContent>
        </Card>

        <Card className="col-span-3 border-none shadow-sm">
          <CardHeader>
            <CardTitle className="font-serif text-lg text-primary">Status dos Pedidos</CardTitle>
            <CardDescription>Distribuição atual de pedidos</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="h-[300px] flex items-center justify-center">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={ORDER_STATUS_DATA}
                    cx="50%"
                    cy="50%"
                    innerRadius={60}
                    outerRadius={90}
                    paddingAngle={2}
                    dataKey="value"
                  >
                    {ORDER_STATUS_DATA.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.fill} strokeWidth={0} />
                    ))}
                  </Pie>
                  <Tooltip 
                     contentStyle={{ backgroundColor: 'hsl(var(--popover))', borderColor: 'hsl(var(--border))', borderRadius: '8px' }}
                     itemStyle={{ color: 'hsl(var(--popover-foreground))' }}
                  />
                </PieChart>
              </ResponsiveContainer>
            </div>
            <div className="flex flex-wrap gap-2 justify-center mt-4">
              {ORDER_STATUS_DATA.map((entry, index) => (
                <div key={index} className="flex items-center gap-1 text-xs text-muted-foreground">
                  <div className="w-2 h-2 rounded-full" style={{ backgroundColor: entry.fill }}></div>
                  {entry.name}
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>

      <div className="grid gap-4 md:grid-cols-3 mt-6">
        <Card className="col-span-1 border-none shadow-sm bg-gradient-to-br from-primary/5 to-background">
          <CardHeader>
            <CardTitle className="font-serif text-lg text-primary flex items-center gap-2">
              <FileText className="h-5 w-5" /> Ações Rápidas
            </CardTitle>
          </CardHeader>
          <CardContent className="grid gap-2">
             <button className="w-full text-left px-4 py-3 rounded-lg bg-background border border-border hover:border-primary/50 hover:shadow-sm transition-all flex items-center justify-between group">
                <span className="font-medium text-sm">Nova Cotação</span>
                <ArrowUpRight className="h-4 w-4 text-muted-foreground group-hover:text-primary" />
             </button>
             <button className="w-full text-left px-4 py-3 rounded-lg bg-background border border-border hover:border-primary/50 hover:shadow-sm transition-all flex items-center justify-between group">
                <span className="font-medium text-sm">Cadastrar Cliente</span>
                <ArrowUpRight className="h-4 w-4 text-muted-foreground group-hover:text-primary" />
             </button>
             <button className="w-full text-left px-4 py-3 rounded-lg bg-background border border-border hover:border-primary/50 hover:shadow-sm transition-all flex items-center justify-between group">
                <span className="font-medium text-sm">Lançar Pedido</span>
                <ArrowUpRight className="h-4 w-4 text-muted-foreground group-hover:text-primary" />
             </button>
          </CardContent>
        </Card>
        
        <Card className="col-span-2 border-none shadow-sm">
          <CardHeader>
            <CardTitle className="font-serif text-lg text-primary">Últimos Orçamentos</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {[1, 2, 3].map((i) => (
                <div key={i} className="flex items-center justify-between border-b border-border/50 pb-4 last:border-0 last:pb-0">
                  <div className="flex items-center gap-4">
                    <div className="h-10 w-10 rounded-full bg-secondary/20 flex items-center justify-center text-primary font-bold">
                      TS
                    </div>
                    <div>
                      <p className="font-medium text-sm">Tech Solutions</p>
                      <p className="text-xs text-muted-foreground">50x Camisetas Personalizadas</p>
                    </div>
                  </div>
                  <div className="text-right">
                    <p className="font-medium text-sm">R$ 2.500,00</p>
                    <p className="text-xs text-emerald-600 bg-emerald-50 px-2 py-0.5 rounded-full inline-block mt-1">Aprovado</p>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>
    </Layout>
  );
}
