import { Layout } from "@/components/layout/Layout";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle, CardDescription, CardFooter } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Textarea } from "@/components/ui/textarea";
import { Badge } from "@/components/ui/badge";
import { QUOTES } from "@/lib/constants";
import { Plus, Search, Filter, MoreVertical, Send, CheckCircle, AlertCircle, ArrowRight } from "lucide-react";
import tShirtWhite from "@assets/generated_images/plain_t-shirt_mockup_white.png";
import printExample from "@assets/generated_images/screen_print_design_example.png";
import { useState } from "react";

export default function Quotes() {
  const [activeTab, setActiveTab] = useState("list");
  const [currentStep, setCurrentStep] = useState(1);

  return (
    <Layout title="Cotações">
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-2">
          <div className="relative w-64">
            <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
            <Input 
              placeholder="Buscar cotação..." 
              className="pl-9 bg-background"
            />
          </div>
          <Button variant="outline" size="icon">
            <Filter className="h-4 w-4" />
          </Button>
        </div>
        <Button 
          className="bg-primary text-primary-foreground hover:bg-primary/90"
          onClick={() => setActiveTab("new")}
        >
          <Plus className="mr-2 h-4 w-4" /> Nova Cotação
        </Button>
      </div>

      <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
        <TabsList className="mb-6 bg-muted/50">
          <TabsTrigger value="list">Todas as Cotações</TabsTrigger>
          <TabsTrigger value="new">Criar Nova</TabsTrigger>
          <TabsTrigger value="compare">Comparativo</TabsTrigger>
        </TabsList>

        <TabsContent value="list" className="space-y-4">
          {QUOTES.map((quote) => (
            <Card key={quote.id} className="hover:shadow-md transition-shadow cursor-pointer border-none shadow-sm group">
              <CardContent className="p-6 flex items-center justify-between">
                <div className="flex items-center gap-4">
                  <div className="h-12 w-12 rounded bg-secondary/20 flex items-center justify-center text-primary font-bold text-xs group-hover:bg-primary group-hover:text-primary-foreground transition-colors">
                    {quote.id.split('-')[1]}
                  </div>
                  <div>
                    <h3 className="font-medium text-lg">{quote.client}</h3>
                    <p className="text-sm text-muted-foreground">{quote.items}</p>
                  </div>
                </div>
                <div className="flex items-center gap-6">
                  <div className="text-right hidden md:block">
                    <p className="text-xs text-muted-foreground uppercase tracking-wider">Data</p>
                    <p className="font-medium text-sm">{quote.date}</p>
                  </div>
                  <div className="text-right min-w-[100px]">
                    <Badge variant="outline" className={`
                      ${quote.status === 'Aprovada' ? 'bg-emerald-50 text-emerald-700 border-emerald-200' : 
                        quote.status === 'Pendente' ? 'bg-amber-50 text-amber-700 border-amber-200' : 
                        'bg-blue-50 text-blue-700 border-blue-200'}
                    `}>
                      {quote.status}
                    </Badge>
                  </div>
                  <Button variant="ghost" size="icon">
                    <MoreVertical className="h-4 w-4" />
                  </Button>
                </div>
              </CardContent>
            </Card>
          ))}
        </TabsContent>

        <TabsContent value="new">
          <div className="grid md:grid-cols-12 gap-6">
            {/* Form Section */}
            <div className="md:col-span-8 space-y-6">
              <Card className="border-none shadow-sm">
                <CardHeader>
                  <div className="flex items-center justify-between">
                    <CardTitle className="font-serif text-primary">
                      {currentStep === 1 ? "1. Detalhes do Produto" : "2. Grade de Tamanhos"}
                    </CardTitle>
                    <span className="text-xs font-mono text-muted-foreground">Passo {currentStep} de 3</span>
                  </div>
                  <Progress value={currentStep * 33} className="h-1" />
                </CardHeader>
                
                <CardContent className="space-y-6 pt-6">
                  {currentStep === 1 && (
                    <div className="space-y-4 animate-in fade-in slide-in-from-left-4 duration-300">
                      <div className="grid grid-cols-2 gap-4">
                        <div className="space-y-2">
                          <Label>Cliente</Label>
                          <Select>
                            <SelectTrigger><SelectValue placeholder="Selecione..." /></SelectTrigger>
                            <SelectContent>
                              <SelectItem value="tech">Tech Solutions</SelectItem>
                              <SelectItem value="cafe">Café do João</SelectItem>
                            </SelectContent>
                          </Select>
                        </div>
                        <div className="space-y-2">
                          <Label>Prazo Desejado</Label>
                          <Input type="date" />
                        </div>
                      </div>

                      <div className="grid grid-cols-3 gap-4">
                        <div className="space-y-2">
                          <Label>Modelo</Label>
                          <Select defaultValue="basic">
                            <SelectTrigger><SelectValue /></SelectTrigger>
                            <SelectContent>
                              <SelectItem value="basic">Camiseta Básica</SelectItem>
                              <SelectItem value="oversized">Oversized</SelectItem>
                              <SelectItem value="polo">Polo</SelectItem>
                            </SelectContent>
                          </Select>
                        </div>
                        <div className="space-y-2">
                          <Label>Tecido</Label>
                          <Select defaultValue="cotton">
                            <SelectTrigger><SelectValue /></SelectTrigger>
                            <SelectContent>
                              <SelectItem value="cotton">Algodão 30.1</SelectItem>
                              <SelectItem value="pv">Malha PV</SelectItem>
                              <SelectItem value="dry">Dry Fit</SelectItem>
                            </SelectContent>
                          </Select>
                        </div>
                        <div className="space-y-2">
                          <Label>Cor</Label>
                          <Select defaultValue="white">
                            <SelectTrigger><SelectValue /></SelectTrigger>
                            <SelectContent>
                              <SelectItem value="white">Branca</SelectItem>
                              <SelectItem value="black">Preta</SelectItem>
                              <SelectItem value="navy">Marinho</SelectItem>
                              <SelectItem value="offwhite">Off-White</SelectItem>
                            </SelectContent>
                          </Select>
                        </div>
                      </div>

                      <div className="space-y-4 border-t border-border pt-4">
                         <h4 className="font-medium text-sm text-muted-foreground">Especificações da Estampa</h4>
                         <div className="grid grid-cols-2 gap-4">
                            <div className="space-y-2">
                              <Label>Arquivo da Estampa</Label>
                              <Select>
                                <SelectTrigger><SelectValue placeholder="Selecione da biblioteca..." /></SelectTrigger>
                                <SelectContent>
                                  <SelectItem value="logo">Logo Tech (SVG)</SelectItem>
                                  <SelectItem value="campanha">Campanha 2024 (PNG)</SelectItem>
                                </SelectContent>
                              </Select>
                            </div>
                            <div className="space-y-2">
                              <Label>Técnica</Label>
                              <Select defaultValue="silk">
                                <SelectTrigger><SelectValue /></SelectTrigger>
                                <SelectContent>
                                  <SelectItem value="silk">Silk Screen (Serigrafia)</SelectItem>
                                  <SelectItem value="dtf">DTF (Digital)</SelectItem>
                                  <SelectItem value="bordado">Bordado</SelectItem>
                                </SelectContent>
                              </Select>
                            </div>
                         </div>
                         <div className="grid grid-cols-3 gap-4">
                            <div className="space-y-2">
                               <Label>Posição</Label>
                               <Select defaultValue="chest">
                                  <SelectTrigger><SelectValue /></SelectTrigger>
                                  <SelectContent>
                                     <SelectItem value="chest">Peito Esquerdo</SelectItem>
                                     <SelectItem value="center">Centro Peito</SelectItem>
                                     <SelectItem value="back">Costas</SelectItem>
                                  </SelectContent>
                               </Select>
                            </div>
                            <div className="space-y-2">
                               <Label>Cores (Qtd)</Label>
                               <Input type="number" placeholder="1" />
                            </div>
                            <div className="space-y-2">
                               <Label>Dimensões (cm)</Label>
                               <Input placeholder="Ex: 10x10" />
                            </div>
                         </div>
                      </div>
                    </div>
                  )}

                  {currentStep === 2 && (
                    <div className="space-y-6 animate-in fade-in slide-in-from-right-4 duration-300">
                       <div className="bg-muted/30 p-4 rounded-lg border border-border">
                          <h4 className="font-medium text-sm mb-4">Grade de Tamanhos</h4>
                          <div className="grid grid-cols-6 gap-4 text-center">
                             <div className="space-y-2">
                                <Label>PP</Label>
                                <Input type="number" className="text-center" placeholder="0" />
                             </div>
                             <div className="space-y-2">
                                <Label>P</Label>
                                <Input type="number" className="text-center" placeholder="0" />
                             </div>
                             <div className="space-y-2">
                                <Label>M</Label>
                                <Input type="number" className="text-center" placeholder="0" />
                             </div>
                             <div className="space-y-2">
                                <Label>G</Label>
                                <Input type="number" className="text-center" placeholder="0" />
                             </div>
                             <div className="space-y-2">
                                <Label>GG</Label>
                                <Input type="number" className="text-center" placeholder="0" />
                             </div>
                             <div className="space-y-2">
                                <Label>XG</Label>
                                <Input type="number" className="text-center" placeholder="0" />
                             </div>
                          </div>
                          <div className="flex justify-end mt-4">
                             <div className="text-right">
                                <p className="text-sm text-muted-foreground">Total de Peças</p>
                                <p className="text-2xl font-bold text-primary">0</p>
                             </div>
                          </div>
                       </div>

                       <div className="space-y-2">
                          <Label>Observações para Produção</Label>
                          <Textarea placeholder="Detalhes sobre acabamento, dobra, embalagem..." className="h-24" />
                       </div>
                    </div>
                  )}

                  {currentStep === 3 && (
                    <div className="space-y-6 animate-in fade-in slide-in-from-right-4 duration-300">
                       <h4 className="font-medium text-sm">Selecionar Fornecedores para Cotação</h4>
                       <div className="space-y-3">
                          {['Estamparia Silva', 'Confecção Rápida', 'Malharia Premium'].map((supplier, idx) => (
                             <div key={idx} className="flex items-center justify-between p-4 border border-border rounded-lg hover:bg-muted/20 transition-colors cursor-pointer">
                                <div className="flex items-center gap-3">
                                   <input type="checkbox" className="h-4 w-4 rounded border-gray-300 text-primary focus:ring-primary" defaultChecked={idx === 0} />
                                   <div>
                                      <p className="font-medium">{supplier}</p>
                                      <p className="text-xs text-muted-foreground">Avaliação: 4.{8-idx} • Prazo médio: {3+idx} dias</p>
                                   </div>
                                </div>
                                <Badge variant="outline" className="text-xs">Recomendado</Badge>
                             </div>
                          ))}
                       </div>
                    </div>
                  )}
                </CardContent>
                <CardFooter className="flex justify-between border-t pt-6">
                   <Button 
                     variant="outline" 
                     onClick={() => setCurrentStep(Math.max(1, currentStep - 1))}
                     disabled={currentStep === 1}
                   >
                     Voltar
                   </Button>
                   
                   {currentStep < 3 ? (
                     <Button onClick={() => setCurrentStep(currentStep + 1)} className="bg-primary text-primary-foreground">
                       Próximo <ArrowRight className="ml-2 h-4 w-4" />
                     </Button>
                   ) : (
                     <Button className="bg-emerald-600 hover:bg-emerald-700 text-white">
                       <Send className="ml-2 h-4 w-4" /> Enviar Cotação
                     </Button>
                   )}
                </CardFooter>
              </Card>
            </div>

            {/* Preview Section */}
            <div className="md:col-span-4 space-y-6">
              <Card className="border-none shadow-sm bg-secondary/10 sticky top-6">
                <CardHeader>
                  <CardTitle className="font-serif text-primary text-base">Resumo Visual</CardTitle>
                </CardHeader>
                <CardContent className="flex flex-col items-center justify-center pb-8">
                   <div className="relative w-full aspect-square max-w-[280px]">
                      <img src={tShirtWhite} alt="T-Shirt" className="w-full h-full object-cover rounded-lg shadow-sm" />
                      <div className="absolute top-[30%] left-1/2 -translate-x-1/2 w-[25%] aspect-square opacity-90 mix-blend-multiply">
                        <img src={printExample} alt="Print" className="w-full h-full object-contain" />
                      </div>
                   </div>
                   <div className="w-full mt-6 space-y-3 text-sm">
                      <div className="flex justify-between border-b border-primary/10 pb-2">
                         <span className="text-muted-foreground">Modelo</span>
                         <span className="font-medium">Camiseta Básica</span>
                      </div>
                      <div className="flex justify-between border-b border-primary/10 pb-2">
                         <span className="text-muted-foreground">Cor</span>
                         <span className="font-medium">Branca</span>
                      </div>
                      <div className="flex justify-between border-b border-primary/10 pb-2">
                         <span className="text-muted-foreground">Estampa</span>
                         <span className="font-medium">Silk (1 cor)</span>
                      </div>
                   </div>
                </CardContent>
              </Card>
            </div>
          </div>
        </TabsContent>

        <TabsContent value="compare">
           <Card className="border-none shadow-sm">
              <CardHeader>
                 <CardTitle className="font-serif text-primary">Comparativo de Respostas</CardTitle>
                 <CardDescription>Cotação #COT-003 - 200x Camisetas Brancas</CardDescription>
              </CardHeader>
              <CardContent>
                 <div className="grid md:grid-cols-3 gap-6">
                    {[
                       { name: 'Estamparia Silva', price: 'R$ 28,50', total: 'R$ 5.700,00', days: '7 dias', winner: true },
                       { name: 'Confecção Rápida', price: 'R$ 32,00', total: 'R$ 6.400,00', days: '5 dias', winner: false },
                       { name: 'Malharia Premium', price: 'R$ 35,00', total: 'R$ 7.000,00', days: '10 dias', winner: false }
                    ].map((offer, idx) => (
                       <div key={idx} className={`relative rounded-xl border-2 p-6 ${offer.winner ? 'border-emerald-500 bg-emerald-50/50' : 'border-border bg-card'}`}>
                          {offer.winner && (
                             <div className="absolute -top-3 left-1/2 -translate-x-1/2 bg-emerald-500 text-white text-xs px-3 py-1 rounded-full font-bold flex items-center gap-1 shadow-sm">
                                <CheckCircle className="h-3 w-3" /> MELHOR PREÇO
                             </div>
                          )}
                          <h3 className="font-bold text-lg text-center mb-4">{offer.name}</h3>
                          <div className="space-y-4">
                             <div className="text-center">
                                <p className="text-sm text-muted-foreground">Preço Unitário</p>
                                <p className="text-2xl font-serif text-primary">{offer.price}</p>
                             </div>
                             <div className="flex justify-between text-sm border-t border-dashed border-gray-300 pt-4">
                                <span>Prazo</span>
                                <span className="font-medium">{offer.days}</span>
                             </div>
                             <div className="flex justify-between text-sm">
                                <span>Total</span>
                                <span className="font-medium">{offer.total}</span>
                             </div>
                             <Button className={`w-full ${offer.winner ? 'bg-primary' : 'bg-secondary text-secondary-foreground hover:bg-secondary/80'}`}>
                                {offer.winner ? 'Aprovar Cotação' : 'Selecionar'}
                             </Button>
                          </div>
                       </div>
                    ))}
                 </div>
              </CardContent>
           </Card>
        </TabsContent>
      </Tabs>
    </Layout>
  );
}

function Progress({ value, className }: { value: number, className?: string }) {
   return (
      <div className={`w-full bg-secondary/20 rounded-full overflow-hidden ${className}`}>
         <div className="h-full bg-primary transition-all duration-500" style={{ width: `${value}%` }} />
      </div>
   )
}
