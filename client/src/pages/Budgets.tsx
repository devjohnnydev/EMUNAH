import { Layout } from "@/components/layout/Layout";
import { Card, CardContent, CardHeader, CardTitle, CardDescription, CardFooter } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Separator } from "@/components/ui/separator";
import { BUDGETS } from "@/lib/constants";
import { FileText, Download, Share2, Printer, QrCode } from "lucide-react";
import logo from "@assets/generated_images/emunah_brand_logo.png";

export default function Budgets() {
  return (
    <Layout title="Orçamentos">
      <div className="grid lg:grid-cols-3 gap-6">
        {/* Sidebar List */}
        <div className="lg:col-span-1 space-y-4">
           <div className="flex items-center justify-between mb-2">
              <h3 className="font-serif text-primary font-medium">Recentes</h3>
              <Button variant="ghost" size="sm" className="text-xs">Ver todos</Button>
           </div>
           
           {BUDGETS.map((budget) => (
             <div key={budget.id} className="bg-card p-4 rounded-lg shadow-sm border border-border hover:border-primary/50 cursor-pointer transition-colors">
               <div className="flex justify-between items-start mb-2">
                 <span className="text-xs font-mono text-muted-foreground">{budget.id}</span>
                 <span className={`text-[10px] px-2 py-0.5 rounded-full font-medium ${budget.status === 'Enviado' ? 'bg-blue-50 text-blue-600' : 'bg-emerald-50 text-emerald-600'}`}>
                   {budget.status}
                 </span>
               </div>
               <h4 className="font-medium text-sm mb-1">{budget.client}</h4>
               <div className="flex justify-between items-center text-sm">
                 <span className="font-semibold text-primary">{budget.value}</span>
                 <span className="text-xs text-muted-foreground">{budget.date}</span>
               </div>
             </div>
           ))}
           
           <Button className="w-full mt-4" variant="outline">
             <FileText className="mr-2 h-4 w-4" /> Novo Orçamento
           </Button>
        </div>

        {/* Preview Area */}
        <div className="lg:col-span-2">
           <Card className="border-none shadow-md overflow-hidden">
             <CardHeader className="bg-muted/30 border-b border-border flex flex-row items-center justify-between">
               <div>
                 <CardTitle className="font-serif text-primary">Visualização</CardTitle>
                 <CardDescription>Orçamento #ORC-1042</CardDescription>
               </div>
               <div className="flex gap-2">
                  <Button size="sm" variant="outline"><Printer className="h-4 w-4" /></Button>
                  <Button size="sm" variant="outline"><Download className="h-4 w-4" /></Button>
                  <Button size="sm" className="bg-primary text-primary-foreground"><Share2 className="h-4 w-4 mr-2" /> Enviar</Button>
               </div>
             </CardHeader>
             <CardContent className="p-8 bg-white min-h-[600px] text-sm relative">
                {/* Paper Mockup */}
                <div className="flex justify-between items-start mb-12">
                   <div className="flex items-center gap-3">
                      <img src={logo} alt="Logo" className="h-12 w-12" />
                      <div>
                        <h1 className="font-serif text-2xl text-primary font-bold">Emunah</h1>
                        <p className="text-xs text-muted-foreground">Vendas e Confecções</p>
                      </div>
                   </div>
                   <div className="text-right">
                      <h2 className="text-xl font-bold text-gray-800">ORÇAMENTO</h2>
                      <p className="text-muted-foreground">#ORC-1042</p>
                      <p className="text-muted-foreground mt-1">Data: 03/12/2024</p>
                      <p className="text-muted-foreground">Validade: 10/12/2024</p>
                   </div>
                </div>

                <div className="grid grid-cols-2 gap-8 mb-12">
                   <div>
                      <h3 className="font-bold text-gray-700 mb-2 text-xs uppercase tracking-wider">Cliente</h3>
                      <p className="font-medium">Tech Solutions Ltda</p>
                      <p className="text-gray-500">CNPJ: 12.345.678/0001-90</p>
                      <p className="text-gray-500">Av. Paulista, 1000 - SP</p>
                      <p className="text-gray-500">contato@techsolutions.com</p>
                   </div>
                   <div className="text-right">
                      <h3 className="font-bold text-gray-700 mb-2 text-xs uppercase tracking-wider">Emitido Por</h3>
                      <p className="font-medium">Emunah Confecções</p>
                      <p className="text-gray-500">CNPJ: 98.765.432/0001-10</p>
                      <p className="text-gray-500">Rua das Flores, 123 - SP</p>
                      <p className="text-gray-500">vendas@emunah.com</p>
                   </div>
                </div>

                <table className="w-full mb-8">
                   <thead>
                      <tr className="border-b-2 border-gray-100">
                         <th className="text-left py-3 text-xs uppercase tracking-wider text-gray-500">Descrição</th>
                         <th className="text-center py-3 text-xs uppercase tracking-wider text-gray-500">Qtd</th>
                         <th className="text-right py-3 text-xs uppercase tracking-wider text-gray-500">Valor Unit.</th>
                         <th className="text-right py-3 text-xs uppercase tracking-wider text-gray-500">Total</th>
                      </tr>
                   </thead>
                   <tbody>
                      <tr className="border-b border-gray-50">
                         <td className="py-4">
                            <p className="font-medium text-gray-800">Camiseta Básica Algodão - Preta</p>
                            <p className="text-xs text-gray-500">Estampa "Logo Tech" (Peito e Costas)</p>
                         </td>
                         <td className="text-center py-4 text-gray-700">50</td>
                         <td className="text-right py-4 text-gray-700">R$ 50,00</td>
                         <td className="text-right py-4 font-medium text-gray-800">R$ 2.500,00</td>
                      </tr>
                   </tbody>
                </table>

                <div className="flex justify-end mb-12">
                   <div className="w-64 space-y-3">
                      <div className="flex justify-between text-gray-600">
                         <span>Subtotal</span>
                         <span>R$ 2.500,00</span>
                      </div>
                      <div className="flex justify-between text-gray-600">
                         <span>Desconto</span>
                         <span>R$ 0,00</span>
                      </div>
                      <Separator />
                      <div className="flex justify-between font-bold text-lg text-primary">
                         <span>Total</span>
                         <span>R$ 2.500,00</span>
                      </div>
                   </div>
                </div>

                <div className="bg-secondary/10 p-6 rounded-lg border border-secondary/30 flex items-start gap-6">
                   <div className="bg-white p-2 rounded shadow-sm">
                      <QrCode className="h-24 w-24 text-gray-800" />
                   </div>
                   <div>
                      <h4 className="font-bold text-primary mb-2">Dados para Pagamento (PIX)</h4>
                      <p className="text-sm text-gray-600 mb-1">Chave PIX (CNPJ): <strong>98.765.432/0001-10</strong></p>
                      <p className="text-sm text-gray-600 mb-4">Banco: Nubank | Titular: Emunah Confecções</p>
                      <div className="bg-amber-50 border border-amber-200 rounded p-2">
                         <p className="text-xs text-amber-800 font-medium">⚠ Sinal de 50% (R$ 1.250,00) necessário para início da produção.</p>
                      </div>
                   </div>
                </div>
             </CardContent>
           </Card>
        </div>
      </div>
    </Layout>
  );
}
