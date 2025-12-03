import { Layout } from "@/components/layout/Layout";
import { Card, CardContent, CardHeader, CardTitle, CardDescription, CardFooter } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Separator } from "@/components/ui/separator";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { BUDGETS } from "@/lib/constants";
import { FileText, Download, Share2, Printer, QrCode, CheckCircle2, XCircle, Calendar } from "lucide-react";
import logo from "@assets/generated_images/emunah_brand_logo.png";
import { useState } from "react";

export default function Budgets() {
  const [selectedBudget, setSelectedBudget] = useState(BUDGETS[0]);
  const [isCreating, setIsCreating] = useState(false);

  return (
    <Layout title="Orçamentos">
      <div className="grid lg:grid-cols-12 gap-6 h-[calc(100vh-8rem)]">
        {/* Sidebar List */}
        <div className="lg:col-span-4 flex flex-col h-full gap-4">
           <div className="flex items-center justify-between">
              <h3 className="font-serif text-primary font-medium">Histórico</h3>
              <Button onClick={() => setIsCreating(true)} variant="default" size="sm" className="bg-primary text-primary-foreground">
                <FileText className="mr-2 h-4 w-4" /> Novo
              </Button>
           </div>
           
           <div className="flex-1 overflow-y-auto space-y-3 pr-2">
             {BUDGETS.map((budget) => (
               <div 
                  key={budget.id} 
                  onClick={() => {
                    setSelectedBudget(budget);
                    setIsCreating(false);
                  }}
                  className={`p-4 rounded-lg border cursor-pointer transition-all duration-200 ${
                    selectedBudget.id === budget.id && !isCreating
                      ? 'bg-white border-primary shadow-md ring-1 ring-primary/20' 
                      : 'bg-card border-border hover:border-primary/50'
                  }`}
               >
                 <div className="flex justify-between items-start mb-2">
                   <span className="text-xs font-mono text-muted-foreground">{budget.id}</span>
                   <span className={`text-[10px] px-2 py-0.5 rounded-full font-medium ${
                     budget.status === 'Enviado' ? 'bg-blue-50 text-blue-600' : 
                     budget.status === 'Aprovado' ? 'bg-emerald-50 text-emerald-600' :
                     'bg-gray-100 text-gray-600'
                   }`}>
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
           </div>
        </div>

        {/* Main Content Area */}
        <div className="lg:col-span-8 h-full overflow-y-auto">
           {isCreating ? (
             <Card className="border-none shadow-md h-full">
               <CardHeader>
                 <CardTitle className="font-serif text-primary">Novo Orçamento</CardTitle>
                 <CardDescription>Gerar proposta comercial a partir de cotação aprovada</CardDescription>
               </CardHeader>
               <CardContent className="space-y-6">
                  <div className="grid grid-cols-2 gap-6">
                    <div className="space-y-2">
                      <Label>Cotação de Referência</Label>
                      <Select>
                        <SelectTrigger><SelectValue placeholder="Selecione a cotação..." /></SelectTrigger>
                        <SelectContent>
                          <SelectItem value="cot-003">COT-003 - Tech Solutions (Aprovada)</SelectItem>
                          <SelectItem value="cot-001">COT-001 - Café do João (Aprovada)</SelectItem>
                        </SelectContent>
                      </Select>
                    </div>
                    <div className="space-y-2">
                      <Label>Validade da Proposta</Label>
                      <Input type="date" />
                    </div>
                  </div>

                  <Separator />

                  <div className="space-y-4">
                    <h4 className="font-medium text-sm">Condições de Pagamento</h4>
                    <div className="grid grid-cols-3 gap-4">
                      <div className="space-y-2">
                         <Label>Valor Total (Custo + Margem)</Label>
                         <Input defaultValue="R$ 2.500,00" />
                      </div>
                      <div className="space-y-2">
                         <Label>Sinal (%)</Label>
                         <div className="relative">
                           <Input type="number" defaultValue="50" className="pr-8" />
                           <span className="absolute right-3 top-2.5 text-xs text-muted-foreground">%</span>
                         </div>
                      </div>
                      <div className="space-y-2">
                         <Label>Valor do Sinal</Label>
                         <Input defaultValue="R$ 1.250,00" disabled />
                      </div>
                    </div>
                    
                    <div className="space-y-2">
                       <Label>Instruções / Observações</Label>
                       <Input defaultValue="Prazo de produção conta a partir do pagamento do sinal." />
                    </div>
                  </div>

                  <div className="bg-amber-50 border border-amber-200 rounded-lg p-4 flex items-start gap-3">
                     <QrCode className="h-5 w-5 text-amber-700 mt-0.5" />
                     <div>
                        <h4 className="text-sm font-bold text-amber-800">Integração PIX Automática</h4>
                        <p className="text-xs text-amber-700">Ao gerar este orçamento, um QR Code PIX exclusivo será criado usando a chave da empresa. O cliente poderá pagar instantaneamente.</p>
                     </div>
                  </div>
               </CardContent>
               <CardFooter className="flex justify-end gap-3">
                  <Button variant="outline" onClick={() => setIsCreating(false)}>Cancelar</Button>
                  <Button className="bg-primary text-primary-foreground">Gerar & Enviar PDF</Button>
               </CardFooter>
             </Card>
           ) : (
             <Card className="border-none shadow-md overflow-hidden h-full flex flex-col">
               <CardHeader className="bg-muted/30 border-b border-border flex flex-row items-center justify-between py-4">
                 <div>
                   <CardTitle className="font-serif text-primary text-lg">Visualização do PDF</CardTitle>
                   <CardDescription className="text-xs">Orçamento #{selectedBudget.id}</CardDescription>
                 </div>
                 <div className="flex gap-2">
                    <Button size="sm" variant="outline" className="h-8"><Printer className="h-4 w-4" /></Button>
                    <Button size="sm" variant="outline" className="h-8"><Download className="h-4 w-4" /></Button>
                    <Button size="sm" className="bg-primary text-primary-foreground h-8"><Share2 className="h-4 w-4 mr-2" /> Reenviar</Button>
                 </div>
               </CardHeader>
               <CardContent className="flex-1 overflow-y-auto p-8 bg-white text-sm relative">
                  {/* Paper Mockup */}
                  <div className="flex justify-between items-start mb-10">
                     <div className="flex items-center gap-3">
                        <img src={logo} alt="Logo" className="h-12 w-12" />
                        <div>
                          <h1 className="font-serif text-2xl text-primary font-bold">Emunah</h1>
                          <p className="text-xs text-muted-foreground">Vendas e Confecções</p>
                        </div>
                     </div>
                     <div className="text-right">
                        <h2 className="text-xl font-bold text-gray-800">ORÇAMENTO</h2>
                        <p className="text-muted-foreground">#{selectedBudget.id}</p>
                        <p className="text-muted-foreground mt-1 text-xs">Emitido em: {selectedBudget.date}</p>
                     </div>
                  </div>

                  <div className="grid grid-cols-2 gap-8 mb-10">
                     <div>
                        <h3 className="font-bold text-gray-700 mb-2 text-xs uppercase tracking-wider border-b pb-1">Dados do Cliente</h3>
                        <p className="font-medium text-base">{selectedBudget.client}</p>
                        <p className="text-gray-500">CNPJ: 12.345.678/0001-90</p>
                        <p className="text-gray-500">Av. Paulista, 1000 - SP</p>
                     </div>
                     <div className="text-right">
                        <h3 className="font-bold text-gray-700 mb-2 text-xs uppercase tracking-wider border-b pb-1">Emissor</h3>
                        <p className="font-medium">Emunah Confecções</p>
                        <p className="text-gray-500">CNPJ: 98.765.432/0001-10</p>
                        <p className="text-gray-500">Rua das Flores, 123 - SP</p>
                     </div>
                  </div>

                  <table className="w-full mb-8">
                     <thead>
                        <tr className="border-b-2 border-gray-100">
                           <th className="text-left py-2 text-xs uppercase tracking-wider text-gray-500">Item / Descrição</th>
                           <th className="text-center py-2 text-xs uppercase tracking-wider text-gray-500">Qtd</th>
                           <th className="text-right py-2 text-xs uppercase tracking-wider text-gray-500">Unit.</th>
                           <th className="text-right py-2 text-xs uppercase tracking-wider text-gray-500">Total</th>
                        </tr>
                     </thead>
                     <tbody>
                        <tr className="border-b border-gray-50">
                           <td className="py-3">
                              <p className="font-medium text-gray-800">Camiseta Básica Algodão - Preta</p>
                              <p className="text-xs text-gray-500">Estampa "Logo Tech" (Peito e Costas) • Tamanhos variados</p>
                           </td>
                           <td className="text-center py-3 text-gray-700">50</td>
                           <td className="text-right py-3 text-gray-700">R$ 50,00</td>
                           <td className="text-right py-3 font-medium text-gray-800">R$ 2.500,00</td>
                        </tr>
                     </tbody>
                  </table>

                  <div className="flex justify-end mb-10">
                     <div className="w-64 space-y-2">
                        <div className="flex justify-between text-gray-600 text-sm">
                           <span>Subtotal</span>
                           <span>R$ 2.500,00</span>
                        </div>
                        <div className="flex justify-between text-gray-600 text-sm">
                           <span>Desconto</span>
                           <span>R$ 0,00</span>
                        </div>
                        <Separator className="my-2" />
                        <div className="flex justify-between font-bold text-lg text-primary">
                           <span>Total</span>
                           <span>R$ 2.500,00</span>
                        </div>
                     </div>
                  </div>

                  <div className="bg-secondary/5 p-6 rounded-lg border border-secondary/20 flex items-start gap-6">
                     <div className="bg-white p-2 rounded shadow-sm shrink-0">
                        <QrCode className="h-20 w-20 text-gray-800" />
                     </div>
                     <div>
                        <h4 className="font-bold text-primary mb-2">Dados Bancários / PIX</h4>
                        <p className="text-sm text-gray-600 mb-1">Chave PIX (CNPJ): <span className="font-mono bg-gray-100 px-1 rounded">98.765.432/0001-10</span></p>
                        <p className="text-xs text-gray-500 mb-3">Banco: Nubank | Titular: Emunah Confecções</p>
                        <div className="flex gap-2">
                           <div className="bg-amber-50 border border-amber-200 rounded px-2 py-1">
                              <p className="text-xs text-amber-800 font-medium">Sinal Necessário: R$ 1.250,00</p>
                           </div>
                           <div className="bg-blue-50 border border-blue-200 rounded px-2 py-1">
                              <p className="text-xs text-blue-800 font-medium">Validade: 10/12/2024</p>
                           </div>
                        </div>
                     </div>
                  </div>
               </CardContent>
               
               {selectedBudget.status === 'Enviado' && (
                  <div className="bg-muted/50 p-4 border-t border-border flex justify-between items-center">
                     <p className="text-sm text-muted-foreground">Ações do Cliente (Simulação)</p>
                     <div className="flex gap-2">
                        <Button variant="destructive" size="sm" className="h-8"><XCircle className="mr-2 h-4 w-4" /> Rejeitar</Button>
                        <Button variant="default" size="sm" className="h-8 bg-emerald-600 hover:bg-emerald-700"><CheckCircle2 className="mr-2 h-4 w-4" /> Aprovar Orçamento</Button>
                     </div>
                  </div>
               )}
             </Card>
           )}
        </div>
      </div>
    </Layout>
  );
}
