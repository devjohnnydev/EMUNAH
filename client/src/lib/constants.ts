import {
  LayoutDashboard,
  ShoppingCart,
  FileText,
  ClipboardList,
  Users,
  Palette,
  Settings,
  BarChart,
  Truck
} from "lucide-react";

export const NAV_ITEMS = [
  { icon: LayoutDashboard, label: "Dashboard", href: "/" },
  { icon: ShoppingCart, label: "Pedidos", href: "/orders" },
  { icon: FileText, label: "Orçamentos", href: "/budgets" },
  { icon: ClipboardList, label: "Cotações", href: "/quotes" },
  { icon: Truck, label: "Fornecedores", href: "/suppliers" },
  { icon: Palette, label: "Estampas", href: "/prints" },
  { icon: Users, label: "Clientes", href: "/clients" },
  { icon: BarChart, label: "Relatórios", href: "/reports" },
  { icon: Settings, label: "Configurações", href: "/settings" },
];

// Mock Data

export const KPIS = [
  { label: "Faturamento (Mês)", value: "R$ 42.500", change: "+12%", trend: "up" },
  { label: "Pedidos Concluídos", value: "156", change: "+8%", trend: "up" },
  { label: "Orçamentos Pendentes", value: "23", change: "-5%", trend: "down" },
  { label: "Ticket Médio", value: "R$ 272", change: "+2%", trend: "up" },
];

export const REVENUE_DATA = [
  { name: "Jan", value: 18000 },
  { name: "Fev", value: 22000 },
  { name: "Mar", value: 25000 },
  { name: "Abr", value: 21000 },
  { name: "Mai", value: 28000 },
  { name: "Jun", value: 32000 },
  { name: "Jul", value: 38000 },
  { name: "Ago", value: 42000 },
  { name: "Set", value: 39000 },
  { name: "Out", value: 45000 },
  { name: "Nov", value: 41000 },
  { name: "Dez", value: 52000 },
];

export const ORDER_STATUS_DATA = [
  { name: "Cotação", value: 30, fill: "hsl(var(--chart-2))" },
  { name: "Aprovado", value: 45, fill: "hsl(var(--chart-1))" },
  { name: "Produção", value: 25, fill: "hsl(var(--chart-4))" },
  { name: "Enviado", value: 15, fill: "hsl(var(--chart-3))" },
  { name: "Entregue", value: 80, fill: "hsl(var(--chart-5))" },
];

export const SUPPLIERS = [
  { id: 1, name: "Estamparia Silva", contact: "Carlos", email: "contato@silva.com", phone: "11 9999-8888", productionTime: "5 dias", rating: 4.8 },
  { id: 2, name: "Confecção Rápida", contact: "Ana", email: "ana@confeccao.com", phone: "11 9777-6666", productionTime: "3 dias", rating: 4.2 },
  { id: 3, name: "Malharia Premium", contact: "Roberto", email: "beto@malharia.com", phone: "11 9555-4444", productionTime: "7 dias", rating: 4.9 },
];

export const PRINTS = [
  { id: 1, name: "Logo Minimalista", colors: ["Preto", "Branco"], positions: ["Peito", "Costas"] },
  { id: 2, name: "Campanha Verão 24", colors: ["Colorido"], positions: ["Frente Total"] },
  { id: 3, name: "Uniforme Staff", colors: ["Branco"], positions: ["Costas", "Manga"] },
];

export const QUOTES = [
  { id: "COT-001", client: "Tech Solutions", items: "50x Camiseta Preta", status: "Respondida", date: "03/12/2024" },
  { id: "COT-002", client: "Café do João", items: "20x Avental Bege", status: "Pendente", date: "02/12/2024" },
  { id: "COT-003", client: "Evento XP", items: "200x Camiseta Branca", status: "Aprovada", date: "01/12/2024" },
];

export const BUDGETS = [
  { id: "ORC-1042", client: "Tech Solutions", value: "R$ 2.500,00", status: "Enviado", date: "03/12/2024" },
  { id: "ORC-1041", client: "Escola Viver", value: "R$ 1.800,00", status: "Aprovado", date: "28/11/2024" },
];
