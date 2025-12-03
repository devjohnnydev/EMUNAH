import { Layout } from "@/components/layout/Layout";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { SUPPLIERS } from "@/lib/constants";
import { Search, Plus, Star, Mail, Phone, MapPin } from "lucide-react";

export default function Suppliers() {
  return (
    <Layout title="Fornecedores">
      <div className="flex items-center justify-between mb-6">
        <div className="relative w-72">
          <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
          <Input 
            placeholder="Buscar fornecedor..." 
            className="pl-9 bg-background"
          />
        </div>
        <Button className="bg-primary text-primary-foreground hover:bg-primary/90">
          <Plus className="mr-2 h-4 w-4" /> Novo Fornecedor
        </Button>
      </div>

      <div className="grid md:grid-cols-1 gap-6">
        <Card className="border-none shadow-sm">
          <CardHeader>
             <CardTitle className="font-serif text-lg text-primary">Lista de Parceiros</CardTitle>
          </CardHeader>
          <CardContent>
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Fornecedor</TableHead>
                  <TableHead>Contato</TableHead>
                  <TableHead>Avaliação</TableHead>
                  <TableHead>Prazo Médio</TableHead>
                  <TableHead className="text-right">Ações</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {SUPPLIERS.map((supplier) => (
                  <TableRow key={supplier.id}>
                    <TableCell>
                      <div className="font-medium">{supplier.name}</div>
                      <div className="text-xs text-muted-foreground flex items-center gap-2 mt-1">
                        <span className="flex items-center gap-1"><Mail className="h-3 w-3" /> {supplier.email}</span>
                      </div>
                    </TableCell>
                    <TableCell>
                      <div className="text-sm">{supplier.contact}</div>
                      <div className="text-xs text-muted-foreground flex items-center gap-1 mt-1">
                        <Phone className="h-3 w-3" /> {supplier.phone}
                      </div>
                    </TableCell>
                    <TableCell>
                      <div className="flex items-center gap-1 bg-amber-50 text-amber-700 px-2 py-1 rounded-full w-fit text-xs font-medium">
                        <Star className="h-3 w-3 fill-amber-500 text-amber-500" />
                        {supplier.rating}
                      </div>
                    </TableCell>
                    <TableCell>
                       <span className="text-sm">{supplier.productionTime}</span>
                    </TableCell>
                    <TableCell className="text-right">
                      <Button variant="ghost" size="sm">Editar</Button>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </CardContent>
        </Card>
      </div>
    </Layout>
  );
}
