import { Layout } from "@/components/layout/Layout";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { PRINTS } from "@/lib/constants";
import { Search, Plus, UploadCloud, MoreHorizontal } from "lucide-react";
import printExample from "@assets/generated_images/screen_print_design_example.png";
import logo from "@assets/generated_images/emunah_brand_logo.png";

export default function Prints() {
  return (
    <Layout title="Estampas">
       <div className="flex items-center justify-between mb-6">
        <div className="relative w-72">
          <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
          <Input 
            placeholder="Buscar estampas..." 
            className="pl-9 bg-background"
          />
        </div>
        <Button className="bg-primary text-primary-foreground hover:bg-primary/90">
          <UploadCloud className="mr-2 h-4 w-4" /> Upload Estampa
        </Button>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
         {/* Mock Items using generated image */}
         {PRINTS.map((print, i) => (
            <Card key={print.id} className="overflow-hidden border-none shadow-sm group hover:shadow-md transition-all duration-300">
               <div className="aspect-square bg-muted/20 relative overflow-hidden p-6 flex items-center justify-center">
                  <img 
                    src={i === 0 ? logo : printExample} 
                    alt={print.name} 
                    className="w-full h-full object-contain transition-transform duration-500 group-hover:scale-110 mix-blend-multiply" 
                  />
                  <div className="absolute top-2 right-2 opacity-0 group-hover:opacity-100 transition-opacity">
                     <Button size="icon" variant="secondary" className="h-8 w-8 rounded-full shadow-sm">
                        <MoreHorizontal className="h-4 w-4" />
                     </Button>
                  </div>
               </div>
               <CardContent className="p-4">
                  <h3 className="font-medium text-base truncate">{print.name}</h3>
                  <div className="flex flex-wrap gap-1 mt-2">
                     {print.colors.map(c => (
                        <span key={c} className="text-[10px] bg-secondary/20 text-secondary-foreground px-2 py-0.5 rounded-full">{c}</span>
                     ))}
                  </div>
                  <p className="text-xs text-muted-foreground mt-2">Posições: {print.positions.join(", ")}</p>
               </CardContent>
            </Card>
         ))}
         
         {/* Add New Placeholder */}
         <Card className="border-dashed border-2 border-muted hover:border-primary/50 bg-transparent shadow-none cursor-pointer flex flex-col items-center justify-center min-h-[200px] gap-2 text-muted-foreground hover:text-primary transition-colors">
            <div className="h-12 w-12 rounded-full bg-muted/50 flex items-center justify-center">
               <Plus className="h-6 w-6" />
            </div>
            <span className="font-medium text-sm">Adicionar Nova</span>
         </Card>
      </div>
    </Layout>
  );
}
