import { Layout } from "@/components/layout/Layout";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle, CardDescription, CardFooter } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Textarea } from "@/components/ui/textarea";
import { QUOTES } from "@/lib/constants";
import { Plus, Search, Filter, MoreVertical, Send, CheckCircle } from "lucide-react";
import tShirtWhite from "@assets/generated_images/plain_t-shirt_mockup_white.png";
import tShirtBlack from "@assets/generated_images/plain_t-shirt_mockup_black.png";
import printExample from "@assets/generated_images/screen_print_design_example.png";

export default function Quotes() {
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
        <Button className="bg-primary text-primary-foreground hover:bg-primary/90">
          <Plus className="mr-2 h-4 w-4" /> Nova Cotação
        </Button>
      </div>

      <Tabs defaultValue="list" className="w-full">
        <TabsList className="mb-6 bg-muted/50">
          <TabsTrigger value="list">Todas as Cotações</TabsTrigger>
          <TabsTrigger value="new">Criar Nova</TabsTrigger>
          <TabsTrigger value="pending">Aguardando Resposta</TabsTrigger>
        </TabsList>

        <TabsContent value="list" className="space-y-4">
          {QUOTES.map((quote) => (
            <Card key={quote.id} className="hover:shadow-md transition-shadow cursor-pointer border-none shadow-sm">
              <CardContent className="p-6 flex items-center justify-between">
                <div className="flex items-center gap-4">
                  <div className="h-12 w-12 rounded bg-secondary/20 flex items-center justify-center text-primary font-bold text-xs">
                    {quote.id}
                  </div>
                  <div>
                    <h3 className="font-medium text-lg">{quote.client}</h3>
                    <p className="text-sm text-muted-foreground">{quote.items}</p>
                  </div>
                </div>
                <div className="flex items-center gap-6">
                  <div className="text-right">
                    <p className="text-sm text-muted-foreground">Data</p>
                    <p className="font-medium">{quote.date}</p>
                  </div>
                  <div className="text-right min-w-[100px]">
                    <span className={`px-3 py-1 rounded-full text-xs font-medium 
                      ${quote.status === 'Aprovada' ? 'bg-emerald-100 text-emerald-700' : 
                        quote.status === 'Pendente' ? 'bg-amber-100 text-amber-700' : 
                        'bg-blue-100 text-blue-700'}`}>
                      {quote.status}
                    </span>
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
          <div className="grid md:grid-cols-2 gap-6">
            <Card className="border-none shadow-sm">
              <CardHeader>
                <CardTitle className="font-serif text-primary">Detalhes do Pedido</CardTitle>
                <CardDescription>Preencha os dados para solicitar orçamentos aos fornecedores.</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="space-y-2">
                  <Label>Cliente</Label>
                  <Select>
                    <SelectTrigger>
                      <SelectValue placeholder="Selecione um cliente" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="tech">Tech Solutions</SelectItem>
                      <SelectItem value="cafe">Café do João</SelectItem>
                    </SelectContent>
                  </Select>
                </div>

                <div className="grid grid-cols-2 gap-4">
                   <div className="space-y-2">
                    <Label>Modelo</Label>
                    <Select defaultValue="basic">
                      <SelectTrigger>
                        <SelectValue placeholder="Modelo" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="basic">Camiseta Básica</SelectItem>
                        <SelectItem value="polo">Polo</SelectItem>
                        <SelectItem value="regata">Regata</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                  <div className="space-y-2">
                    <Label>Cor</Label>
                    <Select defaultValue="white">
                      <SelectTrigger>
                        <SelectValue placeholder="Cor" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="white">Branca</SelectItem>
                        <SelectItem value="black">Preta</SelectItem>
                        <SelectItem value="navy">Marinho</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                </div>

                <div className="space-y-2">
                  <Label>Estampa</Label>
                  <Select>
                     <SelectTrigger>
                        <SelectValue placeholder="Selecione a estampa" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="logo">Logo Minimalista</SelectItem>
                        <SelectItem value="summer">Campanha Verão</SelectItem>
                      </SelectContent>
                  </Select>
                </div>

                 <div className="grid grid-cols-2 gap-4">
                   <div className="space-y-2">
                    <Label>Quantidade</Label>
                    <Input type="number" placeholder="Ex: 50" />
                  </div>
                  <div className="space-y-2">
                    <Label>Posição</Label>
                    <Select defaultValue="chest">
                      <SelectTrigger>
                        <SelectValue placeholder="Posição" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="chest">Peito Esquerdo</SelectItem>
                        <SelectItem value="center">Centro</SelectItem>
                        <SelectItem value="back">Costas</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                </div>

                <div className="space-y-2">
                   <Label>Observações</Label>
                   <Textarea placeholder="Instruções especiais para o fornecedor..." />
                </div>
              </CardContent>
              <CardFooter className="flex justify-between">
                 <Button variant="outline">Cancelar</Button>
                 <Button className="bg-primary text-primary-foreground">
                   Próximo: Selecionar Fornecedores
                 </Button>
              </CardFooter>
            </Card>

            <div className="space-y-6">
              <Card className="border-none shadow-sm bg-secondary/10">
                <CardHeader>
                  <CardTitle className="font-serif text-primary text-base">Preview Mockup</CardTitle>
                </CardHeader>
                <CardContent className="flex flex-col items-center justify-center pb-8">
                   <div className="relative w-64 h-64">
                      <img src={tShirtWhite} alt="T-Shirt" className="w-full h-full object-cover rounded-lg" />
                      <div className="absolute top-1/3 left-1/2 -translate-x-1/2 w-16 h-16 opacity-80 mix-blend-multiply">
                        <img src={printExample} alt="Print" className="w-full h-full object-contain" />
                      </div>
                   </div>
                   <p className="text-xs text-muted-foreground mt-4 text-center max-w-[200px]">
                     Visualização aproximada. A posição real pode variar na produção.
                   </p>
                </CardContent>
              </Card>

              <Card className="border-none shadow-sm">
                <CardHeader>
                   <CardTitle className="font-serif text-primary text-base">Fornecedores Sugeridos</CardTitle>
                </CardHeader>
                <CardContent>
                   <div className="space-y-3">
                      <div className="flex items-center justify-between p-3 bg-background rounded-lg border border-border">
                         <div className="flex items-center gap-3">
                            <CheckCircle className="h-4 w-4 text-primary" />
                            <div>
                               <p className="text-sm font-medium">Estamparia Silva</p>
                               <p className="text-xs text-muted-foreground">Prazo: 5 dias • ⭐ 4.8</p>
                            </div>
                         </div>
                         <Button size="sm" variant="ghost" className="h-8">Detalhes</Button>
                      </div>
                      <div className="flex items-center justify-between p-3 bg-background rounded-lg border border-border opacity-60">
                         <div className="flex items-center gap-3">
                            <div className="h-4 w-4 rounded-full border border-muted-foreground"></div>
                            <div>
                               <p className="text-sm font-medium">Confecção Rápida</p>
                               <p className="text-xs text-muted-foreground">Prazo: 3 dias • ⭐ 4.2</p>
                            </div>
                         </div>
                         <Button size="sm" variant="ghost" className="h-8">Detalhes</Button>
                      </div>
                   </div>
                </CardContent>
              </Card>
            </div>
          </div>
        </TabsContent>
      </Tabs>
    </Layout>
  );
}
